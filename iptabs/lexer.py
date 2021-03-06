#!/usr/bin/python3
#
# iptabs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iptabs is distributed in the hope that it will be useful,
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
    'DEFAULT_POLICY',
    'RULE_ID',
    'RULE_VALUE',
    'DO_LOG',
    'LOG_PREFIX',
    'COMMENT',
    'RULE_JOINER',
    'BEHAVIOUR',
)

t_RULE_VALUE = r'[a-zA-Z_0-9./]+'
t_DO_LOG = r'\?'
t_RULE_JOINER = r'&&'
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

def t_DEFAULT_POLICY(t):
    # do place above t_RULE_ID for correct tokenization
    r'default:\s*[a-zA-Z_][a-zA-Z_0-9]+'
    # remove 'default: ' and any unnecessary space
    t.value = t.value.replace('default:', '').replace(' ', '').replace('\t', '')
    return t

def t_RULE_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*:'
    t.value = t.value[:-1]  # remove the ':' character
    return t


def t_LOG_PREFIX(t):
    r'\([a-zA-Z_][a-zA-Z_0-9]*\)'
    t.value = t.value[1:-1]
    return t


def t_BEHAVIOUR(t):
    r'%[a-zA-Z]+'
    t.value = t.value[1:]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError('illegal character "{}" at line {}.'.format(t.value[0], t.lexer.lineno))

lexer = lex.lex()
