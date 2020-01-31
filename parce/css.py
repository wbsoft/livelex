# -*- coding: utf-8 -*-
#
# This file is part of the parce Python package.
#
# Copyright © 2019-2020 by Wilbert Berendsen <info@wilbertberendsen.nl>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
This modules provides StyleSheet, Style and a bunch of utility functions
that help reading from a tree structure parsed by the parce.lang.css module.

StyleSheet represents a list of rules and conditions (nested @-rules) from a
CSS file or string source.

Style represents a resulting list of rules, sorted on specificity, so that
by selecting rules the properties that apply in a certain situation can be
determined and read.

This module will be used by the theme module to provide syntax highlighting
themes based on CSS files.

Workflow:

    1. Instantiate a StyleSheet from a file or other source. If needed,
       combine multiple StyleSheets using the + operator.

    2. (not yet implemented) Filter conditions out, like media, supports
       or document.

    3. Get a Style object through the ``style`` property of the StyleSheet.

    4. Use a ``select`` method (currently only ``select_class``, but more
       can be implemented) to select rules based on their selectors.

    5. Use ``properties()`` to combine the properties of the selected
       rules to get a dictionary of the CSS properties that apply.

Example::

    >>> from parce.css import *
    >>> style = StyleSheet.from_file("parce/themes/default.css").style
    >>> style.select_class("comment").combine_properties()
    {'font-style': [<Context Css.identifier at 1037-1043 (1 children)>],
    'color': [<Token '#666' at 1056:1060 (Literal.Color)>]}

"""


import collections
import functools
import os

from . import *
from .lang.css import Css
from .query import Query


Rule = collections.namedtuple("Rule", "selectors properties")
Condition = collections.namedtuple("Condition", "condition style")


def style_query(func):
    """Make a method result (generator) into a new Style object."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return type(self)(list(func(self, *args, **kwargs)))
    return wrapper


class StyleSheet:
    """Represents a list of style rules and conditions.

    Normall CSS rules are translated into a Rule tuple, and nested rules
    such as @media, @document and @supports are translated into Condition
    tuples.

    A Rule consists of ``selectors`` and ``properties``. The ``selectors``
    are the tokens in a rule before the {. The ``properties`` is a dict
    mapping css property names to the list of tokens representing their
    value.

    A Condition consists of ``condition`` and ``style``; the ``condition``
    is a list of tokens representing all text between the @ and the opening {.
    The ``style`` is another StyleSheet object representing the nested
    style sheet.

    You can combine stylesheets from different files or sources using the +
    operator.

    The ``style`` property returns the Style object representing all combined
    rules, and allowing further queries.

    """
    def __init__(self, rules=None):
        """Initialize a StyleSheet, empty of with the supplied rules/conditions."""
        self.rules = rules or []

    @classmethod
    def from_file(cls, filename, path=None, allow_import=True):
        """Return a new StyleSheet adding Rules and Conditions from a local filename.

        The ``path`` argument is currently unused. If ``allow_import`` is
        False, the ``@import` atrule is ignored.

        """
        text = open(filename).read()  # TODO: handle encoding, currently UTF-8
        return cls.from_text(text, filename, path, allow_import)

    @classmethod
    def from_text(cls, text, filename, path=None, allow_import=True):
        """Return a new StyleSheet adding Rules and Conditions from a string.

        The ``filename`` argument is used to handle ``@import`` rules
        correctly. The ``path`` argument is currently unused. If
        ``allow_import`` is False, the ``@import` atrule is ignored.

        """
        tree = root(Css.root, text)
        return cls.from_tree(tree, filename, path, allow_import)

    @classmethod
    def from_tree(cls, tree, filename, path=None, allow_import=True):
        """Return a new StyleSheet adding Rules and Conditions from a parsed tree.

        The ``filename`` argument is used to handle ``@import`` rules
        correctly. The ``path`` argument is currently unused. If
        ``allow_import`` is False, the ``@import` atrule is ignored.

        """
        rules = []
        for node in tree.query.children(Css.atrule, Css.prelude):
            if node.lexicon is Css.atrule:
                # handle @-rules
                keyword = node.first_token()
                if keyword == "import":
                    if allow_import:
                        for s in node.query.children(Css.dqstring, Css.sqstring):
                            fname = get_string(s)
                            fname = os.path.join(os.path.dirname(filename), fname)
                            rules.extend(cls.from_file(fname, path, True).rules)
                            break
                elif node[-1].lexicon is Css.atrule_nested:
                    s = cls.from_tree(node[-1][-1], filename, path, allow_import)
                    rules.append(Condition(node, s))
            elif len(node) > 1:   # Css.prelude
                # get the selectors (without ending { )
                selectors = list(remove_comments(node[:-1]))
                if selectors:
                    for rule in node.query.right:
                        # get the property declarations:
                        properties = {}
                        for declaration in rule.query.children(Css.declaration):
                            propname = get_ident_token(declaration[0])
                            value = declaration[2:] if declaration[1] == ":" else declaration[1:]
                            properties[propname] = value
                        rules.append(Rule(selectors, properties))
                        break
        return cls(rules)

    def __add__(self, other):
        return type(self)(self.rules + other.rules)

    @property
    def style(self):
        """Return a Style object with the remaining rules.

        All rules that still are behind a condition, are let through.
        The rules are sorted on specificity.

        """
        def gen():
            for r in self.rules:
                if isinstance(r, Condition):
                    yield from r.style.rules
                else:
                    yield r
        rules = sorted(gen(), key=lambda rule: calculate_specificity(rule.selectors))
        rules.reverse()
        return Style(rules)


class Style:
    """Represents the list of rules created by the StyleSheet object.

    All ``select``-methods/properties return a new Style object with the
    narrowed-down selection of rules.

    Use ``properties()`` to get the dictionary of combined properties that
    apply to the selected rules.

    """
    def __init__(self, rules):
        self.rules = rules

    @style_query
    def select_class(self, *classes):
        """Select the rules that match at least one of the class names.

        Just looks at the last class name in a selector, does not use combinators.
        (Enough for internal styling :-).

        """
        for rule in self.rules:
            c = Query.from_nodes(rule.selectors).all(Css.class_selector).pick_last()
            if c and get_ident_token(c) in classes:
                yield rule

    def properties(self):
        """Return the combined properties of the current set of rules. (Endpoint.)

        Returns a dictionary with the properties. Comments, closing delimiters and
        "!important" flags are removed from the property values.

        """
        result = {}
        for rule in self.rules:
            for key, value in rule.properties.items():
                if key not in result or (
                     "!important" in value and "!important" not in result[key]):
                    result[key] = list(remove_comments(value))
        for value in result.values():
            while value and value[-1] in (";", "!important"):
                del value[-1]
        return result


def css_classes(action):
    """Return a tuple of lower-case CSS class names for the specified standard action."""
    return tuple(a._name.lower() for a in action)


def remove_comments(nodes):
    """Yield the nodes with comments removed."""
    for n in nodes:
        if (n.is_token and n.action is Comment) or (
            n.is_context and n.lexicon is Css.comment):
            continue
        yield n


def unescape(text):
    """Return the unescaped character, text is the contents of an Escape token."""
    value = text[1:]
    if value == '\n':
        return ''
    try:
        codepoint = int(value, 16)
    except ValueError:
        return value
    return chr(codepoint)


def get_ident_token(context):
    """Return the ident-token represented by the context.

    The context can be a selector, property, attribute, id_selector or
    class_selector, containing Name and/or Escape tokens.

    """
    def gen():
        for t in context:
            yield unescape(t.text) if t.action is Escape else t.text
    return ''.join(gen())


def get_string(context):
    """Get the string contexts represented by context (dqstring or sqstring)."""
    def gen():
        for t in context[:-1]:  # closing quote is not needed
            yield unescape(t.text) if t.action is String.Escape else t.text
    return ''.join(gen())


def get_url(context):
    """Get the url from the context, which is an url_function context."""
    def gen():
        for n in context[:-1]:
            if n.is_token:
                if t.action is Escape:
                    yield unescape(t.text)
                elif action is Literal.Url:
                    yield t.text
                elif action is String:
                    yield get_string(n.right_sibling())
    return ''.join(gen())


def calculate_specificity(selectors):
    """Calculate the specificity of the list of selectors.

    Returns a three-tuple (ids, clss, elts), where ids is the number of ID
    selectors, clss the number of class, attribute or pseudo-class selectors,
    and elts the number of element or pseudo-elements.

    Currently, does not handle functions like :not(), :is(), although that
    would not be difficult to implement.

    """
    # selector list?
    try:
        i = selectors.index(",")
    except ValueError:
        pass
    else:
        return max(calculate_specificity(selectors[:i]), calculate_specificity(selectors[i+1:]))
    q = Query.from_nodes(selectors).all
    ids = q(Css.id_selector).count()
    clss = q(Css.attribute_selector, Css.class_selector, Css.pseudo_class).count()
    elts = q(Css.element_selector, Css.pseudo_element).count()
    return (ids, clss, elts)


