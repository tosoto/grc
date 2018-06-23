#    This is part of grc module.
#    Copyright (C) 2018  Tomasz Otoka
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

class Edge:
    sourceNode = None
    destinationNode = None
    label = ''

    def __init__(self, sourceNode, destinationNode, label ):
        self.sourceNode = sourceNode
        self.destinationNode = destinationNode
        self.label = label

    def __str__( self ):
        return str( self.__dict__ )

    def __eq__( self, other ):
        return self.__dict__ == other.__dict__
