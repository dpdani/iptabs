#!/usr/bin/python3
#
# iptabs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tBB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Data structures for iptabs. """

from enum import Enum


class Policy(Enum):
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'
    DROP = 'DROP'


class Chain:
    def __init__(self, name):
        self.name = name
        self.log_rules = []
        self.rules = []
        self.default_policy = None


class Rule:
    def __init__(self, action, command, value):
        self.action = action
        self.command = command
        self.value = value

    def __repr__(self):
        return "<Rule {}>".format(str(self))

    def __str__(self):
        if self.action == 'LOG':
            action = 'LOG'
        else:
            action = self.action.value
        return '{}: {} => {}'.format(self.command, self.value, action)
