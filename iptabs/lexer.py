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

""" Lexer for iptabs syntax.
For reference examples of the syntax visit the examples/ folder.
Uses PLY-3 (https://github.com/dabeaz/ply)."""

from ply import lex

tokens = (
    'CHAIN',
    'ACTION',
    'RULE_ID',
    'RULE_VALUE',
    'DO_LOG',
    'COMMENT'
)

t_RULE_VALUE = r'[a-zA-Z_0-9]+'
t_DO_LOG = r'\?'
t_ignore_COMMENT = r'\#.*'

t_ignore = ' \t'


def t_CHAIN(t):
    r'\~[a-zA-Z_][a-zA-Z_0-9]*'
    t.value = t.value[1:]  # remove the '~' character
    return t

def t_ACTION(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*>'
    t.value = t.value[:-1]  # remove the '>' character
    return t

def t_RULE_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*:'
    t.value = t.value[:-1]  # remove the ':' character
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()