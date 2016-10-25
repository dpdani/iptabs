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
    LOG = 'LOG'


class Chain:
    def __init__(self, name):
        self.name = name
        self.log_rules = []
        self.rules = []
        self.default_policy = None


class Rule:
    def __init__(self, action, command, value, *, log_label=''):
        if not isinstance(action, Policy):
            raise TypeError("expected argument 'action' to be a Policy instance.")
        self.action = action
        self.command = command
        self.value = value
        if action == Policy.LOG:
            self.log_label = log_label
        else:
            self.log_label = None

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, str(self))

    def __str__(self):
        return '{}: {} => {}'.format(self.command, self.value, self.action.value) + (' ({})'.format(self.log_label)
                                                                                     if self.log_label else '')


class ComplexRule(Rule):
    def __init__(self, action, *args, log_label=''):
        for i,arg in enumerate(args):
            if not isinstance(arg, Rule):
                print(arg)
                raise TypeError("arguments expected to be instances of Rule. Check item #{}.".format(i))
        self.rules = args
        # actions defined in self.rules are ignored
        super().__init__(action, None, None, log_label=log_label)

    def __str__(self):
        return ' && '.join([str(rule)[:str(rule).find('=')-1] for rule in self]) + ' => ' + str(self.action.value) + \
               (' ({})'.format(self.log_label) if self.log_label else '')

    def __iter__(self):
        return iter(self.rules)
