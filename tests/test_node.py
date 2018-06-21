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


import unittest
import sys
sys.path.append( '../grc')
import Node

class TestStringMethod( unittest.TestCase ):

    def test_node_init( self ):

        node = Node.Node( 2, [5,6], 'test node' )

        self.assertEqual( node.id, 2 )
        self.assertEqual( node.relatedNodes, [ 5, 6 ] )
        self.assertEqual( node.label, 'test node' )

    def test_node_str( self ):

        node = Node.Node( 2, [5,6], 'test node' )

        self.assertEqual( str( node ), "{'relatedNodes': [5, 6], 'id': 2, 'label': 'test node'}" )

    def test_node_eq( self ):

        node1 = Node.Node( 2, [5,6], 'test node' )
        node2 = Node.Node( 2, [5,6], 'test node' )
        node3 = Node.Node( 2, [5,6], 'different test node' )

        self.assertEqual( node1 == node2, True )
        self.assertEqual( node1 == node3, False )

if __name__ == '__main__':
    unittest.main()
