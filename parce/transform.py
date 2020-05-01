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


#: an item can both represent a token or an object generated by a transformer,
#: it represents a token when ``text`` evaluates to True
Item = collections.namedtuple("Item", "pos text action obj name")


class Transformer:
    """This is the base class for a transformer class.

    Currently it has no special behaviour, but that might change in the future.

    """



def transform(func):
    """Decorator to make a method a transformer method.

    Does nothing special currently, but it might change in the future.

    """
    return func


def transform_using(constructor):
    """Decorator that calls constructor on the result of the function."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, items):
            return constructor(func(self, items))
        return wrapper
    return decorator


def transform_tree(tree, transformer):
    """Evaluate a tree.

    For every context, calls the corresponding method of the transformer with
    the contents of that context, where sub-contexts are already replaced with
    the transformed result.

    """
    stack = []
    node = tree
    items = []
    while True:
        for i in range(len(items), len(node)):
            n = node[i]
            if n.is_token:
                items.append(Item(n.pos, n.text, n.action, None, None))
            else:
                stack.append(items)
                items = []
                node = n
                break
        else:
            # TODO handle lexicons from other Language, create other Transformer
            name = node.lexicon.lexicon.rules_func.__name__ # TEMP
            obj = getattr(transformer, name)(items) # TODO failsafe
            # TODO cache the obj on the node??
            if stack:
                items = stack.pop()
                items.append(Item(None, None, None, obj, name))
                node = node.parent
            else:
                break
    return obj

