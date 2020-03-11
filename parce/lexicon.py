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
A Lexicon groups rules to match.

A LexiconDescriptor is created by decorating a function yielding rules with the
`@lexicon` decorator. When a LexiconDescriptor is accessed for the first time
via a Language subclass, a Lexicon for that class is created and cached, and
returned each time that attribute is accessed.

The Lexicon can parse text according to the rules. When parsing for the first
time, the rules-function is run with the language class as argument, and the
rules it creates are cached.

This makes it possible to inherit from a Language class and only re-implement
some lexicons, the others keep working as in the base class.
"""

import itertools
import re
import threading

import parce.pattern
import parce.regex
from .target import TargetFactory
from .rule import DynamicItem, DynamicRuleItem, ArgRuleItem


class LexiconDescriptor:
    """The LexiconDescriptor creates a Lexicon when called via a class."""
    __slots__ = ('rules_func', 'lexicons', '_lock', 're_flags')

    def __init__(self, rules_func,
                       re_flags=0,
        ):
        """Initializes with the rules function.

        The rules function accepts the Language class as argument, and yields
        the pattern, action, target, ... tuples.

        """
        self.rules_func = rules_func
        self.re_flags = re_flags
        self.lexicons = {}
        self._lock = threading.Lock()

    def __get__(self, instance, owner):
        """Called when accessed as a descriptor, via the Language class."""
        if instance:
            raise RuntimeError('Language should never be instantiated')
        try:
            return self.lexicons[owner]
        except KeyError:
            # prevent instantiating the same Lexicon multiple times
            with self._lock:
                try:
                    lexicon = self.lexicons[owner]
                except KeyError:
                    lexicon = self.lexicons[owner] = Lexicon(self, owner)
                return lexicon


class Lexicon:
    """A Lexicon is tied to a particular class.

    This makes it possible to inherit from a Language class and change
    only some Lexicons.

    Call Lexicon.parse(text, pos) to do the actual parsing work.
    This function is created as soon as it is called for the first time.

    """
    __slots__ = ('lexicon', 'language', 'parse', '_lock', '_variants')

    arg = None

    def __init__(self, lexicon, language):
        self.lexicon = lexicon
        self.language = language
        self._variants = {}
        # lock is used when creating a variant and/or the parse() instance function
        self._lock = threading.Lock()

    def __call__(self, arg=None):
        """Create a LexiconDerivate with argument ``arg``.

        The argument should be a simple, hashable singleton object, such as a
        string, an integer or a standard action. The created LexiconDerivate
        is cached. The argument is accessible using special pattern and rule
        item types, so a LexiconDerivate can parse text based on rules
        that are defined at parse time, which is useful for things like
        here documents, where you only get to know the end token after the
        start token has been found.

        When comparing Lexicons with '==', a derivative lexicon compares equal
        with the Lexicon that created them, although they co-exist as separate
        objects.

        If arg is None, self is returned.

        """
        if arg is None:
            return self
        try:
            return self._variants[arg]
        except KeyError:
            with self._lock:
                try:
                    lexicon = self._variants[arg]
                except KeyError:
                    lexicon = self._variants[arg] = LexiconDerivate(self, arg)
            return lexicon

    def __eq__(self, other):
        if isinstance(other, Lexicon):
            return self.lexicon is other.lexicon and self.language is other.language
        return super().__eq__(other)

    def __ne__(self, other):
        if isinstance(other, Lexicon):
            return self.lexicon is not other.lexicon or self.language is not other.language
        return super().__ne__(other)

    def __iter__(self):
        """Yield the rules."""
        return self.lexicon.rules_func(self.language) or ()

    def __repr__(self):
        return self.name()

    def name(self):
        """Return the 'Language.lexicon' name of this bound lexicon."""
        return '.'.join((self.language.__name__, self.lexicon.rules_func.__name__))

    def __getattr__(self, name):
        """Implemented to create the parse() function when called for the first time.

        The function is created by _get_parser_func() and is set as instance
        variable, so __getattr__ is not called again.

        """
        if name == "parse":
            with self._lock:
                try:
                    return object.__getattribute__(self, name)
                except AttributeError:
                    self.parse = self._get_parser_func()
                    return self.parse
        return object.__getattribute__(self, name)

    @property
    def re_flags(self):
        """The re_flags set on instantiation."""
        return self.lexicon.re_flags

    def _get_parser_func(self):
        """Compile the pattern rules and return a parse(text, pos) func."""
        patterns = []
        rules = []
        default_action = None
        default_target = None
        # make lists of pattern, action and possible targets
        for pattern, *rule in self:
            while isinstance(pattern, parce.pattern.Pattern):
                pattern = pattern.build(self.arg)
            if pattern is parce.default_action:
                default_action = rule[0]
            elif pattern is parce.default_target:
                default_target = TargetFactory.make(self, rule)
            elif pattern is not None and pattern not in patterns:
                # skip rule when the pattern is None or already seen
                patterns.append(pattern)
                # recursively replace ArgRuleItem instances
                def replace_arg_items(items):
                    for i in items:
                        if isinstance(i, ArgRuleItem):
                            yield from replace_arg_items(i.replace(self.arg))
                        elif isinstance(i, DynamicRuleItem):
                            i.itemlists = [list(replace_arg_items(l)) for l in i.itemlists]
                            yield i
                        else:
                            yield i
                rule = list(replace_arg_items(rule))
                rules.append(rule)

        # handle the empty lexicon case
        if not patterns:
            if default_action:
                def parse(text, pos):
                    yield pos, text[pos:], None, default_action, None
            elif default_target:
                def parse(text, pos):
                    if pos < len(text):
                        yield pos, "", None, None, default_target
            else:
                # just quits parsing
                def parse(text, pos):
                    yield from ()
            return parse

        # if there is only one pattern, and no dynamic action or target,
        # see if the pattern is simple enough to just use str.find
        if len(patterns) == 1 and not any(isinstance(item, DynamicItem)
                                          for item in rules[0]):
            needle = parce.regex.to_string(patterns[0])
            if needle:
                l= len(needle)
                action, *rule = rules[0]
                target = TargetFactory.make(self, rule)
                if default_action:
                    def parse(text, pos):
                        """Parse text, using a default action for unknown text."""
                        while True:
                            i = text.find(needle, pos)
                            if i > pos:
                                yield pos, text[pos:i], None, default_action, None
                            elif i == -1:
                                break
                            yield i, needle, None, action, target
                            pos = i + l
                        if pos < len(text):
                            yield pos, text[pos:], None, default_action, None
                elif default_target:
                    def parse(text, pos):
                        """Parse text, stopping with the default target at unknown text."""
                        while needle == text[pos:pos+l]:
                            yield pos, needle, None, action, target
                            pos += l
                        if pos < len(text):
                            yield pos, "", None, None, default_target
                else:
                    def parse(text, pos):
                        """Parse text, skipping unknown text."""
                        while True:
                            i = text.find(needle, pos)
                            if i == -1:
                                break
                            yield i, needle, None, action, target
                            pos = i + l
                return parse

        # compile the regexp for all patterns
        rx = re.compile("|".join("(?P<g_{0}>{1})".format(i, pattern)
            for i, pattern in enumerate(patterns)), self.re_flags)
        # make a fast mapping list from matchObj.lastindex to the rules.
        # rules that contain DynamicRuleItem instances are put in the dynamic index
        indices = sorted(v for k, v in rx.groupindex.items() if k.startswith('g_'))
        static = [None] * (indices[-1] + 1)
        dynamic = [None] * (indices[-1] + 1)
        for i, rule in zip(indices, rules):
            if any(isinstance(item, DynamicRuleItem) for item in rule):
                dynamic[i] = rule
            else:
                action, *target = rule
                static[i] = (action, TargetFactory.make(self, target))

        # for rule containing no dynamic stuff, static has the rule, otherwise
        # falls back to dynamic, which is then immediately executed
        def token(m):
            """Return pos, text, match, *rule for the match object."""
            return (m.start(), m.group(), m, *(static[m.lastindex] or replace(m)))

        def replace(m):
            """Recursively replace dynamic rule items in the rule pointed to by match object."""
            def inner_replace(items):
                for i in items:
                    if isinstance(i, DynamicRuleItem):
                        yield from inner_replace(i.replace(m.group(), m))
                    else:
                        yield i
            action, *target = inner_replace(dynamic[m.lastindex])
            return action, TargetFactory.make(self, target)

        if default_action:
            def parse(text, pos):
                """Parse text, using a default action for unknown text."""
                for m in rx.finditer(text, pos):
                    if m.start() > pos:
                        yield pos, text[pos:m.start()], None, default_action, None
                    yield token(m)
                    pos = m.end()
                if pos < len(text):
                    yield pos, text[pos:], None, default_action, None
        elif default_target:
            def parse(text, pos):
                """Parse text, stopping with the default target at unknown text."""
                while True:
                    m = rx.match(text, pos)
                    if m:
                        yield token(m)
                        pos = m.end()
                    else:
                        if pos < len(text):
                            yield pos, "", None, None, default_target
                        break
        else:
            def parse(text, pos):
                """Parse text, skipping unknown text."""
                for m in rx.finditer(text, pos):
                    yield token(m)
        return parse


class LexiconDerivate(Lexicon):
    """A Lexicon created by calling a normal Lexicon with an argument.

    The argument is stored in the ``arg`` attibute, which is None for a normal
    Lexicon.

    There exist special Pattern and rule item types that make the ``arg``
    attribute accessible, so you can make rules dependent on the argument,
    which is useful to parse e.g. here documents and other content types where
    you want to inject values at parse time in the rules set.

    """
    __slots__ = ('arg',)
    def __init__(self, lexicon, arg):
        super().__init__(lexicon.lexicon, lexicon.language)
        self.arg = arg

    def __call__(self, arg=None):
        """Always return self."""
        return self

    def __repr__(self):
        return super().__repr__() + '*'


