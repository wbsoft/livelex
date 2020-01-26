# -*- coding: utf-8 -*-
#
# This file is part of the parce Python package.
#
# Copyright © 2019 by Wilbert Berendsen <info@wilbertberendsen.nl>
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
This module contains some smart functions to build or manipulate regular
expressions:

    ``words2regexp()``
        builds an optimized regular expression from a list of words.

    ``common_suffix()``
        returns the common suffix of the words, if any.

    ``make_trie()``
        makes a dict-based radix tree structure from a list of words.

    ``trie_to_regexp_tuple()``
        converts a trie structure to a regexp tuple.

    ``build_regexp()``
        converts a tuple to a real regular expression.

    ``make_charclass()``
        turns a list of characters into a sensible [a-z] expression.

    ``to_string()``
        to convert a regexp to a normal search string if possible.

"""


import re


def words2regexp(words):
    """Convert the word list to an optimized regular expression."""
    words, suffix = common_suffix(words)
    root = make_trie(words)
    r = trie_to_regexp_tuple(root)
    if suffix:
        r += (suffix,)
    return build_regexp(r)


def trie_to_regexp_tuple(node, reverse=False):
    """Converts the trie node to a tuple of regular expression parts.

    A part is either a plain string expression or a frozenset instance.
    A frozenset instance denotes a group of alternative expressions, and
    consists of plain string expressions or other tuples. If None is also
    present in the frozenset, the expression is optional.

    """
    if reverse:
        combine = lambda r1, r2: r2 + r1
    else:
        combine = lambda r1, r2: r1 + r2

    if len(node) == 1:
        for k, n in node.items():
            if k:
                return combine((k,), trie_to_regexp_tuple(n, reverse))
            return ()
    else:
        seen = []
        keys = []
        groups = set()

        # group the nodes if they have the same leaf node
        for k, n in node.items():
            if k:
                try:
                    i = seen.index(n)
                except ValueError:
                    i = len(seen)
                    seen.append(n)
                    keys.append([k])
                else:
                    keys[i].append(k)
            else:
                groups.add(None)    # means optional group, may end here

        for keys, node in zip(keys, seen):
            if len(keys) == 1:
                if not any(node):
                    groups.add(keys[0])
                else:
                    groups.add(combine((keys[0],), trie_to_regexp_tuple(node, reverse)))
            else:
                if not reverse:
                    # try to optimize the keys backwards
                    r = trie_to_regexp_tuple(make_trie(keys, True), True)
                    if r == (frozenset(keys),) and not any(node):
                        groups.update(keys)
                        continue
                elif not any(node):
                    groups.update(keys)
                    continue
                else:
                    r = (frozenset(keys),)
                groups.add(combine(r, trie_to_regexp_tuple(node, reverse)))
        return groups.pop() if len(groups) == 1 else (frozenset(groups),)


def build_regexp(r):
    """Convert a tuple to a full regular expression pattern string.

    The tuple is described in the trie_to_regexp_tuple() function doc string.

    """
    def get_items(r):
        """Yield regexp items from tuple r in tuples (item, mincount, maxcount).

        An item is either a string like "aa", or a two-tuple(exprs,
        tuples), where exprs is a set of plain strings, and tuples a set of
        tuples that were inside a frozenset. The mincount and maxcount are
        integers and describe the minimal or maximal required count of
        matches.

        """
        for item in r:
            if isinstance(item, str):
                yield item, 1, 1
            else:
                # item is a frozenset
                mincount = 1
                exprs = set()
                tuples = set()
                for k in item:
                    if isinstance(k, str):
                        exprs.add(k)
                    elif isinstance(k, tuple):
                        tuples.add(k)
                    elif k is None:
                        mincount = 0
                # just one expression and no subgroups?
                if len(exprs) == 1 and not tuples:
                    yield exprs.pop(), mincount, 1
                else:
                    item = (exprs, tuples)
                    # optimize for the case of only one subgroup
                    # remove otherwise empty parent group if possible
                    if not exprs and len(tuples) == 1:
                        # there is only one subexpression in the group
                        r = next(iter(tuples))
                        items = merge_items(r)
                        # if our group has no qualifier, just yield the subgroup
                        if mincount:
                            yield from items
                        # if we are optional, check if the qualifier of the subgroup
                        # can be altered. Possible when mincount <= 1.
                        elif len(items) == 1 and items[0][1] <= 1:
                            item, _, maxcount = items[0]
                            yield item, 0, maxcount
                        else:
                            yield item, mincount, 1
                    else:
                        yield item, mincount, 1

    def merge_items(r):
        """Read items-tuples such as yielded by get_items().

        Returns a list of the same items, merging where possible adjacent
        items that are the same. Every list entry is a three-tuple(item,
        mincount, maxcount); where an item is either a string like "aa", or
        a two-tuple(exprs, tuples).

        """
        items = []
        for item, mincount, maxcount in get_items(r):
            if items and items[-1][0] == item:
                items[-1][1] += mincount
                items[-1][2] += maxcount
            else:
                items.append([item, mincount, maxcount])
        return items

    items = merge_items(r)

    # now really construct the regexp string for each item
    result = []
    for item, mincount, maxcount in items:
        # qualifier to use
        if mincount == 1 and maxcount == 1:
            qualifier = ''
        elif mincount == 0 and maxcount == 1:
            qualifier = "?"
        elif mincount == maxcount:
            qualifier = "{{{0}}}".format(maxcount)
        else:
            qualifier = "{{{0},{1}}}".format(mincount or '', maxcount or '')
        # make the rx
        if isinstance(item, str):
            rx = re.escape(item)
            enclose = len(item) > 1 and qualifier
        else:
            exprs, tuples = item
            # separate single characters from longer strings
            chars, strings = set(), set()
            for k in exprs:
                (chars if len(k) == 1 else strings).add(k)
            group = []
            if chars:
                if len(chars) == 1:
                    group.append(re.escape(next(iter(chars))))
                else:
                    group.append('[' + make_charclass(chars) + ']')
            if strings:
                group.extend(map(re.escape, sorted(strings)))
            if tuples:
                group.extend(map(build_regexp, tuples))
            if chars and not strings and not tuples:
                rx = group[0]
                enclose = False
            else:
                rx = '|'.join(group)
                enclose = len(items) > 1 or qualifier
        if enclose:
            rx = '(?:' + rx + ')'
        result.append(rx + qualifier)
    return ''.join(result)


def make_charclass(chars):
    """Return a string with adjacent characters grouped.

    eg ('a', 'b', 'c', 'd', 'f') is turned into '[a-df]'.
    Special characters are properly escaped.

    """
    buf = []
    for c in sorted(map(ord, chars)):
        if buf and buf[-1][1] == c - 1:
            buf[-1][1] = c
        else:
            buf.append([c, c])
    return ''.join(re.escape(chr(a)) if a == b else
                   re.escape(chr(a) + chr(b)) if a == b - 1 else
                   re.escape(chr(a)) + '-' + re.escape(chr(b))
                   for a, b in buf)


def make_trie(words, reverse=False):
    """Return a dict-based radix trie structure from a list of words.

    If reverse is set to True, the trie is made in backward direction,
    from the end of the words.

    """
    if reverse:
        chars = lambda word: word[::-1]
        add = lambda k1, k2: k2 + k1
    else:
        chars = lambda word: word
        add = lambda k1, k2: k1 + k2

    root = {}
    for w in words:
        d = root
        for c in chars(w):
            d = d.setdefault(c, {})
        d[None] = True  # end

    # merge characters that are the only child with their parents
    def merge(node):
        for key, node in node.items():
            if key:
                while len(node) == 1:
                    k, n = next(iter(node.items()))
                    if k:
                        key = add(key, k)
                        node = n
                    else:
                        break
                else:
                    node = dict(merge(node))
            yield key, node

    return dict(merge(root))


def common_suffix(words):
    """Return (words, suffix), where suffix is the common suffix.

    If there is no common suffix, words is unchanged, and suffix is an
    empty string. If there is a common suffix, that is chopped of the returned
    words.

    """
    suffix = []
    for s in map(set, zip(*map(reversed, words))):
        if len(s) != 1:
            break
        suffix.append(s.pop())
    suffix = ''.join(reversed(suffix))
    if suffix:
        i = -len(suffix)
        words = [word[:i] for word in words]
    return words, suffix


def to_string(expr):
    """If the regular expression can be converted to a simple string, return it.

    Otherwise, None is returned. The returned string can be used with
    "".find(), which would be faster than using re.search().

    """
    if set(re.sub(r'\\.', '', expr)) & set("^$|.()[]{}+*?"):
        return  # there are unescaped special characters like (, [, ? etc.
    # handle all escapes, there may be fails, in that case we can't use the expr as string
    pat = (r'\\(?:'
        r'x([0-9a-fA-F]{2})'    # 1 hex
        r'|([afnrtv])'          # 2 normal escaped character like \n
        r'|(\d{1,3})'           # 3 octal , or fail if back ref
        r'|u([0-9a-fA-F]{4})'   # 4 \uxxxx
        r'|U([0-9a-fA-F]{8})'   # 5 \Uxxxxxxxx
        r'|([\^\$\|\.\(\)\[\]\{\}\+\*\?\\])'  # special re char that was escaped
        r'|)')
    def replace_escapes(m):
        if m.group(1):
            return chr(int(m.group(1), 16))
        elif m.group(2):
            return chr({'a':7, 'f':12, 'n':10, 'r':13, 't':9, 'v':11}[m.group(2)])
        elif m.group(3):
            if 0 < int(m.group(3)) <= 99 and not m.group(3).startswith("0"):
                raise ValueError
            return chr(int(m.group(3), 8))  # can also raise ValueError
        elif m.group(4):
            return chr(int(m.group(4), 16))
        elif m.group(5):
            return chr(int(m.group(5), 16))
        elif m.group(6):
            return m.group(6)
        raise ValueError
    try:
        s = re.sub(pat, replace_escapes, expr)
    except ValueError:
        return
    assert re.fullmatch(expr, s)
    return s

