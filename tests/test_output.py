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
import Output

class TestStringMethod( unittest.TestCase ):

    def test_output_init( self ):
        try:
            Output.Output()
        except:
            self.assertEqual( 1, '"OutputClass" initialization failed' )


    def test_output_enableDebug( self ):

        output = Output.Output()

        output.enableDebug( True )
        self.assertEqual( output.debugFlag, True )

        output.enableDebug( False )
        self.assertEqual( output.debugFlag, False )


    def test_output_enableTerminalOutput( self ):

        output = Output.Output()

        output.enableTerminalOutput( True )
        self.assertEqual( output.terminalOutput, True )

        output.enableTerminalOutput( False )
        self.assertEqual( output.terminalOutput, False )


    def test_output_clearConsoleOut( self ):

        output = Output.Output()

        output.consoleOut = 'abc'

        output.clearConsoleOut()

        self.assertEqual( output.consoleOut, '' )


    def test_output_getConsole( self ):

        output = Output.Output()

        output.consoleOut = 'abc'

        self.assertEqual( output.getConsole(), 'abc' )



    def test_output_myPrint( self ):

        output = Output.Output()
        output.enableTerminalOutput( False )

        output.myPrint( 'abc' )

        self.assertEqual( output.consoleOut, 'abc' )


    def test_output_printDebug( self ):

        output = Output.Output()
        output.enableTerminalOutput( False )

        output.enableDebug( False )
        output.printDebug( 'abc' )

        self.assertEqual( output.consoleOut, '' )

        output.enableDebug( True )
        output.printDebug( 'def' )

        self.assertEqual( output.consoleOut, 'def' )


    def test_output_printWarning( self ):

        output = Output.Output()
        output.enableTerminalOutput( False )

        output.enableDebug( False )
        output.printWarning( 'abc' )

        self.assertEqual( output.consoleOut, 'Warning: abc\n' )

        output.enableDebug( True )
        output.printWarning( 'def' )

        self.assertEqual( output.consoleOut, 'Warning: abc\nWarning: def\n' )


    def test_output_printError( self ):

        output = Output.Output()
        output.enableTerminalOutput( False )

        sys_exit = False

        try:
            output.printError( 'abc' )
        except SystemExit:
            sys_exit = True

        self.assertEqual( sys_exit, True )
        self.assertEqual( output.consoleOut, 'ERROR: abc' )


if __name__ == '__main__':
    unittest.main()
