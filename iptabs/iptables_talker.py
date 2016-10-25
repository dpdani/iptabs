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

import subprocess
import os
from structures import *


DEBUG_MODE = False


LIST = "iptables -L {} -n"
APPEND = "iptables -A {} --protocol tcp {} -j {}"  # only support TCP for now
DEFAULT_POLICY = "iptables -P {} {}"
CHECK = "iptables -C "
DELETE = "workinprogress"


class NotRootException(Exception):
    def __init__(self):
        super().__init__("You need to be root to make calls to iptables. EUID: {}.".format(os.geteuid()))


def make_call(command):
    if DEBUG_MODE:
        print('[DEBUG]  $', command)
        return
    if os.geteuid() != 0:
        raise NotRootException()
    return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')


def append_rule(chain, rule):
    return make_call(APPEND.format(
        chain,
        "--{} {}".format(rule.command, rule.value),
        rule.action.value + (' --log-prefix {}'.format(rule.log_prefix) if rule.log_prefix else '')
    ))


def append_complex_rule(chain, rule):
    return make_call(APPEND.format(
        chain,
        ' '.join(["--{} {}".format(r.command, r.value) for r in rule.rules]),
        rule.action.value + (' --log-prefix {}'.format(rule.log_prefix) if rule.log_prefix else '')
    ))


def set_default_policy(chain, policy):
    return make_call(DEFAULT_POLICY.format(
        chain, policy.value
    ))


def check_rule():
    pass

# def list_rules(chain=''):
#     rules = make_call(LIST.format(chain))
#     chains = []
#     while True:
#         if rules.startswith('Chain'):
#             rules = rules[rules.find(' ')+1:]
#             chain_name = rules[:rules.find(' ')]
#             rules = rules[rules.find(' ')+1:]
#             default_policy = rules[rules.find(' ')+1:rules.find(')')]
#             if default_policy == Policy.ACCEPT.value:
#                 default_policy = Policy.ACCEPT
#             elif default_policy == Policy.DROP.value:
#                 default_policy = Policy.DROP
#             elif default_policy == Policy.REJECT.value:
#                 default_policy = Policy.REJECT
#             else:
#                 raise RuntimeError("Unknown policy for chain '{}': '{}'.".format(chain_name, default_policy))
#             rules = rules[rules.find('\n')+1:]  # eliminates redundant line
#             rules = rules[rules.find('\n')+1:]  #
#             chain = Chain(chain_name)
#             chain.default_policy = default_policy
#             for i,rule in enumerate(rules.split('\n')):
#                 if rule == '':
#                     continue
#                 if rule.startswith(' '):
#                     continue
#                 action = None
#                 if rule.startswith(Policy.ACCEPT.value):
#                     action = Policy.ACCEPT
#                 elif rule.startswith(Policy.DROP.value):
#                     action = Policy.DROP
#                 elif rule.startswith(Policy.REJECT.value):
#                     action = Policy.REJECT
#                 elif rule.startswith(Policy.LOG.value):
#                     action = Policy.LOG
#                 else:
#                     raise RuntimeError("Unknown policy for chain '{}'#{}.".format(chain_name, i))
#                 # !!! CONTINUE FROM HERE
#             chains.append(chain)
#         else:  # end of chains
#             break
#     return chains
