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

""" Parser for iptabs syntax.
For reference examples of the syntax visit the examples/ folder.
Uses PLY-3 (https://github.com/dabeaz/ply)."""

import sys
from ply import yacc
import lexer
from lexer import tokens


with open(sys.argv[1], 'r') as f:
    source = f.read()

# lexer.lexer.input(data)
#
# toks = []
# while True:
#     tok = lexer.lexer.token()
#     if not tok:
#         break
#     toks.append(tok)
#     print(tok)


class Chain:
    def __init__(self, name):
        self.name = name
        self.log_rules = []
        self.rules = []


class Rule:
    def __init__(self, action, command, value):
        self.action = action
        self.command = command
        self.value = value

    def export(self):
        ''' Export this rule to an iptables command '''
        return '{}: {} => {}'.format(self.command, self.value, self.action)


chains = {}
current_chain = None
current_action = None
current_rule_id = None
current_rule_value = None


def p_begin_chain(p):
    "statement : CHAIN"
    global current_chain, current_action, \
           current_rule_id, current_rule_value
    print('--- chain: {}'.format(p[1]))
    current_chain = Chain(p[1])
    current_action = None
    current_rule_id = None
    current_rule_value = None
    chains[p[1]] = current_chain


def p_begin_action(p):
    "statement : ACTION"
    global current_action, current_rule_id, \
           current_rule_value
    print('--- action: {}'.format(p[1]))
    current_rule_id = None
    current_rule_value = None
    if current_chain is None:
        syntax_error(p.lexer.lineno, 'Entering an action before entering a chain.')
    current_action = p[1]


def p_rule(p):
    "statement : RULE_ID RULE_VALUE"
    print('--- rule: {}:{}'.format(p[1], p[2]))
    if current_chain is None:
        syntax_error(p.lexer.lineno, 'Defining a rule before entering a chain.')
    elif current_action is None:
        syntax_error(p.lexer.lineno, 'Defining a rule before entering an action.')
    else:
        current_chain.rules.append(
            Rule(current_action, p[1], p[2])
        )


def p_error(p):
    syntax_error(p.lineno, "Couldn't provide more information.")


def print_chains():
    for chain in chains:
        print('  On', chain, 'chain:')
        for rule in chains[chain].log_rules:
            print('   ', rule.export())
        for rule in chains[chain].rules:
            print('   ', rule.export())


def syntax_error(lineno=0, description=''):
    lineno -= 1
    print("\n\nError in file '{}' at line {}:".format(sys.argv[1], lineno+1), file=sys.stderr)
    try:
        print('{}|     '.format(lineno), source.split('\n')[lineno-1].rstrip(), file=sys.stderr)
    except IndexError: pass
    print('{}|---> '.format(lineno+1), source.split('\n')[lineno].rstrip(), file=sys.stderr)
    try:
        print('{}|     '.format(lineno+2), source.split('\n')[lineno+1].rstrip(), file=sys.stderr)
    except IndexError: pass
    print(description, end='\n\n', file=sys.stderr)
    print("Current status of chains:")
    print_chains()
    sys.exit(1)


yacc.yacc()
parser = yacc.parse(source)