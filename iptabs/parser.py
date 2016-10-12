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