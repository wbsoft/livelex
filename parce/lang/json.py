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
JavaScript Object Notation parser.

Numbers become Number tokens, ``true``, ``false`` and ``null`` become
Name.Constant tokens, strings are yielded in ``string`` contexts, with String
tokens and possibily String.Escape tokens for escaped characters.

Objects (``{ ... }``) become ``object`` contexts with alternating ``key`` and
``value`` child contexts. Arrays (``[ ... ]``) become ``array`` contexts.

"""

import re


from parce import *


class Json(Language):
    @lexicon
    def root(cls):
        yield from cls.values()

    @classmethod
    def values(cls):
        yield r"\{", Delimiter, cls.object
        yield r"\[", Delimiter, cls.array
        yield '"', String, cls.string
        yield r"-?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?", Number
        yield r"\b(?:true|false|null)\b", Name.Constant

    @lexicon
    def object(cls):
        yield r"\}", Delimiter, -1
        yield r"\s+", skip
        yield default_target, cls.key

    @lexicon
    def key(cls):
        yield '"', String, cls.string
        yield ":", Delimiter, -1, cls.value

    @lexicon
    def value(cls):
        yield from cls.values()
        yield ",", Delimiter, -1
        yield r"\}", Delimiter, -2

    @lexicon
    def array(cls):
        yield from cls.values()
        yield ",", Delimiter
        yield "\]", Delimiter, -1

    @lexicon
    def string(cls):
        yield '"', String, -1
        yield r'\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4})', String.Escape
        yield default_action, String


### TEMP XXXXXXXXXXXX, first sketches for a tree transformer/evalutator
from parce.transform import transform, transform_using, Transformer

class JsonTransform(Transformer):

    @transform
    def root(self, items):
        for value in self.values(items):
            return value

    def values(self, items):
        for i in items:
            if i.text:
                if i.action == Number:
                    n = float(i.text)
                    if n.is_integer():
                        n = int(n)
                    yield n
                elif i.action == Name.Constant:
                    yield {
                        'true': True,
                        'false': False,
                        'null': None,
                    }[i.text]
            else:
                yield i.obj

    @transform_using(dict)
    def object(self, items):
        key = None
        for i in items:
            if i.name == "key":
                key = i.obj
            elif i.name == "value":
                if key is not None:
                    yield key, i.obj
                    key = None

    @transform
    def key(self, items):
        for i in items:
            if not i.text:
                return i.obj

    @transform
    def value(self, items):
        for value in self.values(items):
            return value

    @transform_using(list)
    def array(self, items):
        yield from self.values(items)

    @transform_using(''.join)
    def string(self, items):
        for i in items[:-1]:
            if i.text:
                if i.action == String.Escape:
                    if i.text[1] == 'u':
                        yield chr(int(i.text[2:], 16))
                    else:
                        yield i.text[1]
                else:
                    yield i.text

