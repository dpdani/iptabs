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

import subprocess
from structures import *


class IptablesTalker:
    LIST = "iptables --list {}"
    def __init__(self):
        pass
    
    def make_call(self, command):
        return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')
    
    def list_rules(self, chian=''):
        rules = self.make_call(self.LIST.format(chain))
        chains = []
        while True:
            if rules.startswith('Chain'):
                rules = rules[rules.find(' ')+1:]
                chain_name = rules[:rules.find(' ')]
                rules = rules[rules.find(' ')+1:]
                default_policy = rules[rules.find(' ')+1:rules.find(')')]
                if default_policy == Policy.ACCEPT.value:
                    default_policy = Policy.ACCEPT
                elif default_policy == Policy.DROP.value:
                    default_policy = Policy.DROP
                elif default_policy == Policy.REJECT.value:
                    default_policy = Policy.REJECT
                else:
                    raise RuntimeException("Unkown policy for chain '{}': '{}'.".format(chain_name, default_policy))
                rules = rules[rules.find('\n')+1:]  # eliminates redundant line
                rules = rules[rules.find('\n')+1:]  #
                chain = Chain(chain_name)
                chain.default_policy = default_policy
                for i,rule in enumerate(rules.split('\n')):
                    if rule == '':
                        continue
                    if rule.startswith(' '):
                        continue
                    action = None
                    if rule.startswith(Policy.ACCEPT.value):
                        action = Policy.ACCEPT
                    elif rule.startswith(Policy.DROP.value):
                        action = Policy.DROP
                    elif rule.startswith(Policy.REJECT.value):
                        action = Policy.REJECT
                    elif rule.startswith('LOG'):
                        action = 'LOG'
                    else:
                        raise RuntimeException("Unkown policy for chain '{}'#{}.".format(chain_name, i))
                    # !!! CONTINUE FROM HERE 
                chains.append(chain)
            else:  # end of chains
                break
        return chains
