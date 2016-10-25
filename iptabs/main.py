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

import os
import sys
import argparse
import parser
import iptables_talker
from structures import *


def main(args):
    if args.debug:
        iptables_talker.DEBUG_MODE = True
    parser.parse_file(args.source)
    if not args.silent:
        print("Parsed from file '{}':".format(args.source))
        parser.print_chains()
    chains = parser.chains
    if not args.only_parse:
        if not (args.yes or args.silent):  # confirmation
            while True:
                try:
                    inp = input('Are you sure you want to append these rules to iptables? [y/N] ').lower()
                except (KeyboardInterrupt, EOFError):
                    return 0
                if inp in ('n', ''):
                    return 0
                elif inp == 'y':
                    break
        try:
            for chain in chains:
                if chains[chain].default_policy is not None:
                    iptables_talker.set_default_policy(chain, chains[chain].default_policy)
                for rule in chains[chain].log_rules:  # it is a best practice to put the log rules first
                    if isinstance(rule, ComplexRule):
                        iptables_talker.append_complex_rule(chain, rule)
                    else:
                        iptables_talker.append_rule(chain, rule)
                for rule in chains[chain].rules:
                    if isinstance(rule, ComplexRule):
                        iptables_talker.append_complex_rule(chain, rule)
                    else:
                        iptables_talker.append_rule(chain, rule)
        except iptables_talker.NotRootException:
            print("\n\n[ERROR]  You need to be root to make calls to iptables. EUID: {}.".format(os.geteuid()))
            return 1
    return 0


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('source', help="file from which read configuration")
    args.add_argument('-p', '--only-parse', help="only parse SOURCE file. Do not talk to iptables.",
                      action='store_true')
    args.add_argument('-d', '--debug', help="run in debug mode. This will output the calls iptabs would be "
                                            "attempting to iptables, instead of actually making them.",
                      action='store_true')
    args.add_argument('-y', '--yes', help="do not ask for confirmation", action='store_true')
    args.add_argument('-s', '--silent', help="do not produce any output. Implies '-y'.", action='store_true')
    args = args.parse_args()
    sys.exit(
        main(args)
    )
