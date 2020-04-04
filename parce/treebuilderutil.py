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
Helper functions and classes for the :mod:`~parce.treebuilder` module.

"""


import collections
import itertools

from parce.lexer import Event, Lexer
from parce.tree import Context
from parce.target import TargetFactory


#: encapsulates the return values of :meth:`TreeBuilder.build_new_tree`
BuildResult = collections.namedtuple("BuildResult", "tree start end offset lexicons")

#: encapsulates the return values of :meth:`TreeBuilder.replace_tree`
ReplaceResult = collections.namedtuple("ReplaceResult", "start end lexicons")


class Changes:
    """Store changes that have to be made to a tree.

    This object is used by
    :meth:`~parce.treebuilder.TreeBuilder.get_changes()`. Calling
    :meth:`add()` merges new changes with the existing changes.

    """
    __slots__ = "text", "root_lexicon", "start", "removed", "added"

    def __init__(self):
        self.text = ""
        self.root_lexicon = False   # meaning no change is requested
        self.start = -1          # meaning no text is altered
        self.removed = 0
        self.added = 0

    def __repr__(self):
        changes = []
        if self.root_lexicon != False:
            changes.append("root_lexicon: {}".format(self.root_lexicon))
        if self.start != -1:
            changes.append("text: {} -{} +{}".format(self.start, self.removed, self.added))
        if not changes:
            changes.append("(no changes)")
        return "<Changes {}>".format(', '.join(changes))

    def add(self, text, root_lexicon=False, start=0, removed=None, added=None):
        """Merge new change with existing changes.

        If added and removed are not given, all text after start is
        considered to be replaced.

        """
        if root_lexicon != False:
            self.root_lexicon = root_lexicon
        if removed is None:
            removed = len(self.text) - start
        if added is None:
            added = len(text) - start
        self.text = text
        if self.start == -1:
            # there were no previous changes
            self.start = start
            self.removed = removed
            self.added = added
            return
        # determine the offset for removed and added
        if start + removed < self.start:
            offset = self.start - start - removed
        elif start > self.start + self.added:
            offset = start - self.start - self.added
        else:
            offset = 0
        # determine which part of removed falls inside existing changes
        start = max(start, self.start)
        end = min(start + removed, self.start + self.added)
        offset -= max(0, end - start)
        # set the new values
        self.start = min(self.start, start)
        self.removed += removed + offset
        self.added += added + offset

    def has_changes(self):
        """Return True when there are actually changes."""
        return self.start != -1 or self.root_lexicon != False

    def new_position(self, pos):
        """Return how the current changes would affect an older start."""
        if pos < self.start:
            return pos
        elif pos < self.start + self.removed:
            return self.start + self.added
        return pos - self.removed + self.added


def find_insert_tokens(tree, text, start):
    """Return the token(group) after which new tokens should be inserted.

    Normally this is the last complete tokengroup just before the start
    position; but in certain cases this can be earlier in the text.

    If this function returns None, you should start at the beginning.

    """
    while start:
        last_token = start_token = find_token_before(tree, start)
        while last_token and last_token.group and last_token.group[-1].end > start:
            last_token = last_token.group[0].previous_token()
        if not last_token:
            return
        # go back at most 10 tokens, to the beginning of a group; if we
        # are at the first token just return 0.
        for start_token in itertools.islice(last_token.backward(), 10):
            pass
        if start_token.group:
            start_token = start_token.group[0]
        start = start_token.pos if start_token.previous_token() else 0
        lexer = get_lexer(start_token) if start else Lexer([tree.lexicon])
        events = lexer.events(text, start)
        # compare the new events with the old tokens; at least one
        # should be the same; if not, go back further if possible
        old_events = events_with_tokens(start_token, last_token)
        prev = None
        for (old, tokens), new in zip(old_events, events):
            if old != new:
                break
            prev = tokens
        if prev:
            return prev


def events_with_tokens(start_token, last_token):
    r"""Yield (Event, tokens) tuples for start_token until and including last_token.

    Events are yielded together with token groups (or single tokens in a
    1-length tuple).

    This can be used to compare an existing token structure with events
    originating from a lexer.

    """
    context, start_trail, end_trail = start_token.common_ancestor_with_trail(last_token)
    if context:

        islice = itertools.islice
        target = TargetFactory()
        get, push, pop = target.get, target.push, target.pop

        def events(context):
            nodes = iter(context)
            for n in nodes:
                if n.is_token:
                    group = n,
                    if n.group:
                        rest = len(n.group) - n.group.index(n) - 1
                        group += tuple(islice(nodes, rest))
                    tokens = tuple((t.pos, t.text, t.action) for t in group)
                    yield Event(get(), tokens), group
                else:
                    push(n.lexicon)
                    yield from events(n)
                    pop()

        for context, slice_ in context.slices(start_trail, end_trail, target):
            yield from events(context[slice_])


def get_lexer(token):
    """Get a Lexer initialized at the token's ancestry."""
    lexicons = [p.lexicon for p in token.ancestors()]
    lexicons.reverse()
    return Lexer(lexicons)


def new_tree(token):
    """Return an empty context with the same ancestry as the token's."""
    c = context = Context(token.parent.lexicon, None)
    for p in token.parent.ancestors():
        n = Context(p.lexicon, None)
        c.parent = n
        n.append(c)
        c = n
    return context


def find_token_before(context, pos):
    """A version of :meth:`~parce.tree.Context.find_token_before` that can handle
    empty contexts.

    The new tree built inside
    :meth:`~parce.treebuilder.BasicTreeBuilder.build_new` can have an empty
    context at the beginning and/or the end. Returns None if there is no token
    left from pos.

    """
    i = 0
    hi = len(context)
    while i < hi:
        mid = (i + hi) // 2
        n = context[mid]
        if n.is_context:
            n = n.first_token() or n    # if no first token, just n itself
        if pos < n.end:
            hi = mid
        else:
            i = mid + 1
    if i > 0:
        i -= 1
        n = context[i]
        return find_token_before(n, pos) if n.is_context else n
