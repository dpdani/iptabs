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
from structures import *


# Shared states
source_path = None
lineno = None
source = None
parser = None
chains = {}
current_chain = None
current_action = None
current_rule_id = None
current_rule_value = None


# Parser rules
def p_begin_chain(p):
    "statement : CHAIN"
    global current_chain, current_action, \
           current_rule_id, current_rule_value
    current_chain = Chain(p[1])
    current_action = None
    current_rule_id = None
    current_rule_value = None
    chains[p[1]] = current_chain


def p_begin_action(p):
    "statement : ACTION"
    global current_action, current_rule_id, \
           current_rule_value
    current_rule_id = None
    current_rule_value = None
    if current_chain is None:
        syntax_error(lineno, 'Entering an action before entering a chain.')
    if p[1] == Policy.ACCEPT.value:
        current_action = Policy.ACCEPT
    elif p[1] == Policy.REJECT.value:
        current_action = Policy.REJECT
    elif p[1] == Policy.DROP.value:
        current_action = Policy.DROP
    else:
        syntax_error(lineno, "Unknown action policy '{}'.".format(p[1]))


def p_simple_rule(p):
    "statement : RULE_ID RULE_VALUE"
    if current_chain is None:
        syntax_error(lineno, 'Defining a rule before entering a chain.')
    elif current_action is None:
        syntax_error(lineno, 'Defining a rule before entering an action.')
    else:
        new_rule = Rule(current_action, p[1], p[2])
        current_chain.rules.append(new_rule)
        p[0] = new_rule

def p_rule(p):
    "rule : RULE_ID RULE_VALUE"
    if current_chain is None:
        syntax_error(lineno, 'Defining a rule before entering a chain.')
    elif current_action is None:
        syntax_error(lineno, 'Defining a rule before entering an action.')
    else:
        p[0] = Rule(current_action, p[1], p[2])

def p_simple_rule_log(p):
    """statement : RULE_ID RULE_VALUE DO_LOG
                 | RULE_ID RULE_VALUE DO_LOG LOG_LABEL"""
    if current_chain is None:
        syntax_error(lineno, 'Defining a logging rule before entering a chain.')
    else:
        if len(p) == 5:
            label = p[4]
        else:
            label = ''
        current_chain.log_rules.append(
            Rule(Policy.LOG, p[1], p[2], log_label=label)
        )
    return p_rule(p[:-1])


def p_complex_rule(p):
    """statement : rule RULE_JOINER rule
                 | rule RULE_JOINER rule DO_LOG
                 | rule RULE_JOINER rule DO_LOG LOG_LABEL"""
    if current_chain is None:
        syntax_error(lineno, 'Defining a rule before entering a chain.')
    elif current_action is None:
        syntax_error(lineno, 'Defining a rule before entering an action.')
    else:
        current_chain.rules.append(
            ComplexRule(current_action, p[1], p[3])
        )
        if len(p) >= 5:
            if len(p) == 6:
                label = p[5]
            else:
                label = ''
            current_chain.log_rules.append(
                ComplexRule(Policy.LOG, p[1], p[3], log_label=label)
            )


def p_default_policy(p):
    "statement : DEFAULT_POLICY"
    if current_chain is None:
        syntax_error(lineno, "Defining a default policy before entering a chain.")
    if p[1] == Policy.ACCEPT.value:
        current_chain.default_policy = Policy.ACCEPT
    elif p[1] == Policy.REJECT.value:
        current_chain.default_policy = Policy.REJECT
    elif p[1] == Policy.DROP.value:
        current_chain.default_policy = Policy.DROP
    else:
        syntax_error(lineno, "Unknown default policy '{}'.".format(p[1]))


def p_error(p):
    if p:
        syntax_error(lineno, "Couldn't provide more information.")
    else:  # EOF
        return


# Utilities
def print_chains():
    for chain in chains:
        print('  On', chain, 'chain:')
        if chains[chain].default_policy is not None:
            print("    default => {}".format(chains[chain].default_policy.value))
        for rule in chains[chain].log_rules:
            print('   ', str(rule))
        for rule in chains[chain].rules:
            print('   ', str(rule))


def syntax_error(lineno=0, description=''):
    lineno -= 1
    source_lines = source.split('\n')
    print("\n\nError in file '{}' at line {}:".format(source_path, lineno+1), file=sys.stderr)
    try:
        print('{}|     '.format(lineno), source_lines[lineno-1].rstrip(), file=sys.stderr)
    except IndexError: pass
    print('{}|---> '.format(lineno+1), source_lines[lineno].rstrip(), file=sys.stderr)
    try:
        print('{}|     '.format(lineno+2), source_lines[lineno+1].rstrip(), file=sys.stderr)
    except IndexError: pass
    print(description, end='\n\n', file=sys.stderr)
    print('Current status of chains:')
    print_chains()
    sys.exit(1)


def parse_file(path):
    global source_path, lineno, parser, source
    with open(path, 'r') as f:
        source = f.read()
    source_path = path
    parser = yacc.yacc()
    lineno = 1
    for line in source.split('\n'):
        parser.parse(line)
        lineno += 1


if __name__ == '__main__':
    parse_file(sys.argv[1])
    print('Interpreted chains:')
    print_chains()
