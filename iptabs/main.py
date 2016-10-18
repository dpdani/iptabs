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

import sys
import parser
import argparse


def main(args):
    if args.only_parse:
        parser.parse_file(args.source)
        print("Parsed from file '{}':".format(args.source))
        parser.print_chains()
    else:
        print("Work in progress.")
    return 0


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('source', help="file from which read configuration")
    args.add_argument('-p', '--only-parse', help="only parse SOURCE file. Do not talk to iptables.",
                      action='store_true')
    args = args.parse_args()
    sys.exit(
        main(args)
    )
