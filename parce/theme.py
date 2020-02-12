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
This module provides the Theme class, which provides text formatting
properties based on the action (standard action) of a Token.

These properties can be used to colorize text according to a language
definition.

By default, the properties are read from a normal CSS (Cascading StyleSheets)
file, although other storage backends could be devised.

A Theme provides CSS ``properties()`` for standard actions, and for three
general situations: ``window()``, which denotes an editor window (or an
encompassing DIV or PRE block in HTML), ``selection()``, which is used for
selected text, and ``currentline()``, which can highlight the current line
the cursor is in in an editor.

From the properties returned by ``selection()`` and ``currentline()``, in
most cases only the background color will be used.

The methods ``window()``, ``selection()`` and ``currentline()`` also accept a
state argument, which can be "default", "focus" or "disabled". A theme always
supports the default state, but can provide separate colors for the "focus"
or "disabled" state, which can be used to change the basic formatting in an
editor window based on its state (in keyboard focus or disabled). If a theme
does not support the "disabled" and/or "focus" state, the default scheme is
used.

In the ``themes/`` directory are bundled CSS themes that can be used.
Instantiate a bundled theme with::

    >>> from parce.theme import Theme
    >>> th = Theme.byname("default")

To use a custom CSS theme file, load it using::

    >>> th = Theme('/path/to/my/custom.css')

Get the CSS properties for an action, use e.g.::

    >>> props = th.properties(String)
    >>> props
    <TextFormat color=Color(r=192, g=0, b=0, a=255)>

A property value is a list of :py:class:`Value <parce.css.Value>` instances.
As CSS colors can be specified in many different ways, you can call
get_color() to get the color values in (r, g, b, a) format.


Mapping actions to CSS classes
------------------------------

Standard actions are mapped to a tuple of classes: the action itself and
the actions it descends from. All CSS rules are combined, the one with
the most matches comes first.

For example, Comment maps to the "comment" CSS class, and Number maps
to ("literal", "number") because Number is a descendant action of Literal.

Some actions might have the same name, e.g. Escape and String.Escape.
Both match CSS rules with the ``.escape`` class selector, but a rule
with ``.string.escape`` will have higher precedence.

The order of the action names does not matter. E.g. an action Text.Comment
will match exactly the same CSS rules as an action Comment.Text. So you
should take some care when designing you action hierachy and not add too much
base action types.

"""


import itertools
import functools

from . import css
from . import themes
from . import util


class Theme:
    """A Theme maps a StandardAction to a TextFormat with CSS properties."""
    def __init__(self, filename):
        """Instantiate Theme from a CSS file."""
        self._filename = filename
        self.TextFormat = TextFormat

    @classmethod
    def byname(cls, name="default"):
        """Create Theme by name, that should reside in the themes/ directory."""
        return cls(themes.filename(name))

    @util.cached_property
    def _stylesheet(self):
        """Load and cache the StyleSheet."""
        return css.StyleSheet.from_file(self._filename)

    @util.cached_property
    def style(self):
        """The stylesheet style rules (see :py:class:`css.Style <parce.css.Style>`)."""
        return self._stylesheet.style

    def filenames(self):
        """Return the list of filenames of the used stylesheet when instantiated"""
        return self._stylesheet.filenames()

    @functools.lru_cache()
    def window(self, state="default"):
        """Return the default textformat.

        This is intended to be used for the editor window or encompassing DIV
        element. The state argument may be "default", "focus", or "disabled".

        """
        e = css.Element(class_="parce")
        if state in ("focus", "disabled"):
            e.pseudo_classes = [state]
        return self.TextFormat(self.style.select_element(e).properties())

    @functools.lru_cache()
    def selection(self, state="default"):
        """Return the default textformat for selected text.

        This is intended to be used for the editor window or encompassing DIV
        element. The state argument may be "default", "focus", or "disabled".

        """
        e = css.Element(class_="parce", pseudo_elements=["selection"])
        if state in ("focus", "disabled"):
            e.pseudo_classes = [state]
        return self.TextFormat(self.style.select_element(e).properties())

    @functools.lru_cache()
    def currentline(self, state="default"):
        """Return the default textformat for the current line.

        This is intended to be used for the editor window or encompassing DIV
        element, probably only the background color. The state argument may be
        "default", "focus", or "disabled".

        """
        e = css.Element(class_="parce current-line")
        if state in ("focus", "disabled"):
            e.pseudo_classes = [state]
        return self.TextFormat(self.style.select_element(e).properties())

    @functools.lru_cache()
    def textformat(self, action):
        """Return the TextFormat for the specified action."""
        classes = css_classes(action)
        return self.TextFormat(self.style.select_class(*classes).properties())


class MetaTheme:
    """A Theme that encapsulates a default Theme and per-language sub-Themes."""
    def __init__(self, theme):
        """Instantiate with default theme."""
        self.theme = theme
        self.themes = {}

    def add_theme(self, language, theme):
        """Add a specific Theme for the specified Language."""
        self.themes[language] = theme

    def window(self, state="default"):
        """Return the window TextFormat for the state of the default theme."""
        return self.theme.window(state)

    def selection(self, state="default"):
        """Return the selection TextFormat for the state of the default theme."""
        return self.theme.selection(state)

    def currentline(self, state="default"):
        """Return the currentline TextFormat for the state of the default theme."""
        return self.theme.currentline(state)

    def textformat(self, action):
        """Return the TextFormat for the specified action of the default theme."""
        return self.theme.textformat(action)




class TextFormat:
    """Simple textformat that reads CSS properties and supports a subset of those.

    This factory is used by default by Theme, but you can implement your own.
    Such a factory only needs to implement an ``__init__`` method that reads
    the dictionary of property Value lists returned by Style.properties().

    A TextFormat has a False boolean value if no single property is set.

    """
    color = None                    #: the foreground color as Color(r, g, b, a) tuple
    background_color = None         #: the background color (id)
    text_decoration_color = None    #: the color for text decoration
    text_decoration_line = ()       #: underline, overline and/or line-through
    text_decoration_style = None    #: solid, double, dotted, dashed or wavy
    font_family = ()                #: family or generic name
    font_kerning = None             #: font kerning
    font_size = None                #: font size
    font_size_unit = None           #: font size unit if given
    font_stretch = None             #: font stretch value (keyword or float, 1.0 is normal)
    font_style = None               #: normal, italic or oblique
    font_style_angle = None         #: oblique slant if given
    font_style_angle_unit = None    #: oblique slant unit if given
    font_variant_caps = None        #: all kind of small caps
    font_variant_position = None    #: normal, sub or super
    font_weight = None              #: 100 - 900 or keyword like ``bold``

    dispatch = util.Dispatcher()

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__,
            ", ".join("{}={}".format(key, repr(value))
                                for key, value in sorted(self.__dict__.items())))

    def __init__(self, properties):
        for prop, values in properties.items():
            self.dispatch(prop, values)

    def __bool__(self):
        """Return True if at least one property is set."""
        return bool(self.__dict__)

    def __sub__(self, other):
        """Return a new TextFormat with the properties removed that are the same in ``other``."""
        new = type(self)({})
        for props in (
            ('color',),
            ('background_color',),
            ('text_decoration_color', 'text_decoration_line', 'text_decoration_style'),
            ('font_family',),
            ('font_kerning',),
            ('font_size', 'font_size_unit'),
            ('font_stretch',),
            ('font_style', 'font_style_angle', 'font_style_angle_unit'),
            ('font_variant_caps',),
            ('font_variant_position',),
            ('font_weight',),
        ):
            if any(prop in self.__dict__ for prop in props) and \
                    any(self.__dict__.get(prop) != other.__dict__.get(prop) for prop in props):
                for prop in props:
                    try:
                        new.__dict__[prop] = self.__dict__[prop]
                    except KeyError:
                        pass
        return new

    def css_properties(self):
        """Return a dict usable to write out a CSS rule with our properties."""
        return dict(itertools.chain(
            self.write_color(),
            self.write_text_decoration(),
            self.write_font(),
        ))

    def write_color(self):
        """Yield color and background color as CSS properties, if set."""
        if self.color:
            yield "color", css.color2hex(self.color)
        if self.background_color:
            yield "background-color", css.color2hex(self.background_color)

    def write_text_decoration(self):
        """Yield a text-decoration property, if set."""
        props = []
        props.extend(self.text_decoration_line)
        if self.text_decoration_style:
            props.append(self.text_decoration_style)
        if self.text_decoration_color:
            props.append(css.color2hex(self.text_decoration_color))
        if props:
            yield "text-decoration", " ".join(props)

    def write_font(self):
        """Yield all font-xxxx properties, if set."""
        if self.font_family:
            yield "font-family", ", ".join(map(css.quote_if_needed, self.font_family))
        if self.font_size:
            yield "font-size", "{}{}".format(
                self.font_size, self.font_size_unit or "")
        if self.font_style == "oblique" and self.font_style_angle:
            slant = self.font_style_angle
            unit = self.font_style_angle_unit or ""
            yield "font-style", "oblique {}{}".format(slant, unit)
        elif self.font_style:
            yield "font-style", self.font_style
        if self.font_stretch:
            yield "font-stretch", format(self.font_stretch)
        if self.font_kerning:
            yield "font-kerning", self.font_kerning
        if self.font_variant_caps:
            yield "font-variant-caps", self.font_variant_caps
        if self.font_variant_position:
            yield "font-variant-position", self.font_variant_position
        if self.font_weight:
            yield "font-weight", format(self.font_weight)

    @dispatch("color")
    def read_color(self, values):
        for v in values:
            c = v.get_color()
            if c:
                self.color = c
                return

    @dispatch("background-color")
    def read_background_color(self, values):
        for v in values:
            c = v.get_color()
            if c:
                self.background_color = c
                return

    @dispatch("background")
    def read_background(self, values):
        self.read_background_color(values)

    @dispatch("text-decoration-color")
    def read_text_decoration_color(self, values):
        for v in values:
            c = v.get_color()
            if c:
                self.text_decoration_color = c
                return

    @dispatch("text-decoration-line")
    def read_text_decoration_line(self, values):
        decos = []
        for v in values:
            if v.text in ("underline", "overline", "line-through"):
                decos.append(v.text)
            elif v.text == "none":
                decos.clear()
        self.text_decoration_line = decos

    @dispatch("text-decoration-style")
    def read_text_decoration_style(self, values):
        for v in values:
            if v.text in ("solid", "double", "dotted", "dashed", "wavy"):
                self.text_decoration_style = v.text
                return

    @dispatch("text-decoration")
    def read_text_decoration(self, values):
        self.read_text_decoration_color(values)
        self.read_text_decoration_line(values)
        self.read_text_decoration_style(values)

    @dispatch("font-family")
    def read_font_family(self, values):
        families = []
        for v in values:
            if v.text and (v.quoted or v.text in (
                "serif",
                "sans-serif",
                "monospace",
                "cursive",
                "fantasy",
                "system-ui",
                "math",
                "emoji",
                "fangsong",
            )):
                families.append(v.text)
        self.font_family = families

    @dispatch("font-kerning")
    def read_font_kerning(self, values):
        for v in values:
            if v.text in ("auto", "normal", "none"):
                self.font_kerning = v.text
                return

    @dispatch("font-size")
    def read_font_size(self, values):
        for v in values:
            if v.text in ("xx-small", "x-small", "small", "medium",
                          "large", "x-large", "xx-large", "xxx-large",
                          "larger", "smaller"):
                self.font_size = v.text
                return
            elif v.number is not None:
                self.font_size = v.number
                self.font_size_unit = v.unit
                return

    @dispatch("font-stretch")
    def read_font_stretch(self, values):
        for v in values:
            if v.text in ("ultra-condensed", "extra-condensed", "condensed",
                          "semi-condensed", "semi-expanded", "expanded",
                          "extra-expanded", "ultra-expanded"):
                self.font_stretch = v.text
            elif v.number is not None and v.unit == "%":
                self.font_stretch = v.number

    @dispatch("font-style")
    def read_font_style(self, values):
        v = values[0]
        for n in values[1:] + [None]:
            if v.text in ("normal", "italic"):
                self.font_style = v.text
                return
            elif v.text == "oblique":
                self.font_style = v.text
                if n and n.number is not None:
                    self.font_style_angle = n.number
                    self.font_style_angle_unit = n.unit
                    return
            v = n

    @dispatch("font-variant-caps")
    def read_font_variant_caps(self, values):
        for v in values:
            if v.text in ("normal", "small-caps", "all-small-caps", "petite-caps",
                          "all-petite-caps", "unicase", "titling-caps"):
                self.font_variant_caps = v.text
                return

    @dispatch("font-variant-position")
    def read_font_variant_position(self, values):
        for v in values:
            if v.text in ("normal", "sub", "super"):
                self.font_variant_position = v.text
                return

    @dispatch("font-weight")
    def read_font_weight(self, values):
        for v in values:
            if v.text in ("normal", "bold", "lighter", "bolder"):
                self.font_weight = v.text
                return
            elif v.number is not None:
                self.font_weight = v.number
                return

    @dispatch("font")
    def read_font(self, values):
        self.read_font_style(values)
        numvalues = []
        for v in values:
            if v.text in ("caption", "icon", "menu", "message-box",
                          "small-caption", "status-bar"):
                self.font_family = [v.text]
                return
            elif v.text in ("normal", "small-caps"):
                self.font_variant_caps = v.text
            elif v.text in ("ultra-condensed", "extra-condensed", "condensed",
                            "semi-condensed", "semi-expanded", "expanded",
                            "extra-expanded", "ultra-expanded"):
                self.font_stretch = v.text
            elif v.text in ("bold", "lighter", "bolder"):
                self.font_weight = v.text
            elif v.number is not None:
                numvalues.append((v.number, v.unit))
        self.read_font_family(values)
        # if more than one size was given, weight is the first
        if len(numvalues) == 1:
            self.font_size, self.font_size_unit = numvalues[0]
        elif len(numvalues) > 1:
            if self.font_weight is None:
                self.font_weight = numvalues[0][0]
            self.font_size, self.font_size_unit = numvalues[1]


def css_classes(action):
    """Return a tuple of lower-case CSS class names for the specified standard action."""
    return tuple(a._name.lower() for a in action)


