#   Copyright 2013 Ben Longbons <b.r.longbons@gmail.com>
#
#   This file is part of attoconf.
#
#   attoconf is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   attoconf is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with attoconf.  If not, see <http://www.gnu.org/licenses/>.



from ..classy import ClassyProject
from ..types import ShellList

def flex(build, FLEX):
    # TODO actually test it
    pass

class Flex(ClassyProject):
    __slots__ = ()
    def vars(self):
        super(Flex, self).vars()
        self.add_option('FLEX', init=['flex'],
                type=ShellList, check=flex,
                help='Lexical analyzer command',
                hidden=False)
