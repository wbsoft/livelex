# -*- coding: utf-8 -*-
#
# This file is part of the livelex Python module.
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
The action module defines Action and its subclasses.

If an instance of Action is encountered in a rule, it is called to return the 
desired action. Nesting is possible in most cases, only some actions require 
the match object to be present; and such actions can't be used as default
action, or inside subgroup_actions.

"""


# used to suppress a token
skip = object()


class Action:
    def __init__(self, *args):
        self.args = args
    
    def filter_actions(self, lexer, pos, text, match):
        raise NotImplementedError


class Subgroup(Action):
    """Yield actions from subgroups in a match.

    When there are multiple tokens yielded from one match object, it is not
    possible to resume parsing after a token that is not the last one.
    To signal that, the stage_change field is set to None for all except
    the last token.

    """
    def filter_actions(self, lexer, pos, text, match):
        for i, action in enumerate(self.args, match.lastindex + 1):
            yield from lexer.filter_actions(action, match.start(i), match.group(i), None)
        

class Match(Action):
    """Expects a function as argument that is called with the match object.
    
    The function should return the desired action.
    
    """
    def __init__(self, func):
        self.func = func

    def filter_actions(self, lexer, pos, text, match):
        action = self.func(match)
        yield from lexer.filter_actions(action, pos, text, match)


class Text(Action):
    """Expects a function as argument that is called with the matched text.
    
    The function should return the desired action.
    
    """
    def __init__(self, func):
        self.func = func

    def filter_actions(self, lexer, pos, text, match):
        action = self.func(text)
        yield from lexer.filter_actions(action, pos, text, None)


