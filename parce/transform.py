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
Transform/evaluate a tree or a stream of events.

XXX This module is in the planning phase!!

"""

import collections
import functools


#: an Item can both represent a token or an object generated by a
#: transformer; when ``token`` evaluates to True the item is a token,
#: otherwise ``name`` and ``obj`` are the name of the lexicon and the
#: object the transformer generated.
Item = collections.namedtuple("Item", "name obj token")


class Transform:
    """This is the base class for a transform class.

    Currently it has no special behaviour, but that might change in the future.

    A Transform class must have a method for every Lexicon the corresponding
    Language class has.

    """



class Transformer:
    """Evaluate a tree.

    For every context, the transformer calls the corresponding method of the
    transformer with the contents of that context, where sub-contexts are
    already replaced with the transformed result.

    """
    def __init__(self):
        self._transforms = {}

    def transform_tree(self, tree):
        """Evaluate a tree structure."""
        try:
            return tree.cached
        except AttributeError:
            pass

        curlang = tree.lexicon.language
        transform = self.get_transform(curlang)

        stack = []
        node = tree
        items = []
        while True:
            for i in range(len(items), len(node)):
                n = node[i]
                if n.is_token:
                    items.append(Item(None, None, n))
                else:
                    try:
                        items.append(Item(n.lexicon.name, n.cached, None))
                    except AttributeError:
                        stack.append(items)
                        items = []
                        node = n
                        break
            else:
                if curlang is not node.lexicon.language:
                    curlang = node.lexicon.language
                    transform = self.get_transform(curlang)
                name = node.lexicon.name
                try:
                    meth = getattr(transform, name)
                except AttributeError:
                    obj = None
                else:
                    obj = meth(items)
                # caching the obj on the node can be enabled as soon as tree.Node
                # (or tree.Context) supports it
                #node.cached = obj
                if stack:
                    items = stack.pop()
                    items.append(Item(name, obj, None))
                    node = node.parent
                else:
                    break
        return obj

    def get_transform(self, language):
        """Return a Transform class instance for the specified language."""
        try:
            return self._transforms[language]
        except KeyError:
            return None

    def add_transform(self, language, transform):
        """Add a Transform instance for the specified language."""
        self._transforms[language] = transform


def transform_tree(tree, transform):
    """TEMP Convenience function that transforms tree using Transform."""
    t = Transformer()
    t.add_transform(tree.lexicon.language, transform)
    return t.transform_tree(tree)


