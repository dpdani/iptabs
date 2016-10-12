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

import lexer

with open('../examples/simple_input.ipbs', 'r') as f:
    data = f.read()

lexer.lexer.input(data)

tokens = []
while True:
    tok = lexer.lexer.token()
    if not tok:
        break
    tokens.append(tok)
    print(tok)


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
current_rule_value = False

for tok in tokens:
    if tok.type == 'CHAIN':
        current_chain = tok.value
        chains[current_chain] = Chain(current_chain)
    elif tok.type == 'ACTION':
        current_action = tok.value
    elif tok.type == 'RULE_ID':
        current_rule_id = tok.value
    elif tok.type == 'RULE_VALUE':
        current_rule_value = tok.value
        chains[current_chain].rules.append(
            Rule(current_action, current_rule_id, tok.value)
        )
    elif tok.type == 'DO_LOG':
        chains[current_chain].log_rules.append(
            Rule('LOG', current_rule_id, current_rule_value)
        )

print("\n\n=== done parsing ===")

for chain in chains:
    print('On', chain, 'chain:')
    for rule in chains[chain].log_rules:
        print(' ', rule.export())
    for rule in chains[chain].rules:
        print(' ', rule.export())
