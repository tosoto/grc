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
sys.path.append('../grc')
import Output

class TestStringMethod(unittest.TestCase):

    def test_output_init(self):
        try:
            Output.Output()
        except:
            self.assertEqual(1, '"OutputClass" initialization failed')


    def test_output_enableDebug(self):

        output = Output.Output()

        output.enable_debug(True)
        self.assertEqual(output.debugFlag, True)

        output.enable_debug(False)
        self.assertEqual(output.debugFlag, False)


    def test_output_enableTerminalOutput(self):

        output = Output.Output()

        output.enable_terminal_output(True)
        self.assertEqual(output.terminalOutput, True)

        output.enable_terminal_output(False)
        self.assertEqual(output.terminalOutput, False)


    def test_output_clearConsoleOut(self):

        output = Output.Output()

        output.consoleOut = 'abc'

        output.clear_console_out()

        self.assertEqual(output.consoleOut, '')


    def test_output_getConsole(self):

        output = Output.Output()

        output.consoleOut = 'abc'

        self.assertEqual(output.get_console(), 'abc')



    def test_output_myPrint(self):

        output = Output.Output()
        output.enable_terminal_output(False)

        output.my_print('abc')

        self.assertEqual(output.consoleOut, 'abc')


    def test_output_printDebug(self):

        output = Output.Output()
        output.enable_terminal_output(False)

        output.enable_debug(False)
        output.print_debug('abc')

        self.assertEqual(output.consoleOut, '')

        output.enable_debug(True)
        output.print_debug('def')

        self.assertEqual(output.consoleOut, 'def')


    def test_output_printWarning(self):

        output = Output.Output()
        output.enable_terminal_output(False)

        output.enable_debug(False)
        output.print_warning('abc')

        self.assertEqual(output.consoleOut, 'Warning: abc\n')

        output.enable_debug(True)
        output.print_warning('def')

        self.assertEqual(output.consoleOut, 'Warning: abc\nWarning: def\n')


    def test_output_printError(self):

        output = Output.Output()
        output.enable_terminal_output(False)

        sys_exit = False

        try:
            output.print_error('abc')
        except SystemExit:
            sys_exit = True

        self.assertEqual(sys_exit, True)
        self.assertEqual(output.consoleOut, 'ERROR: abc')


if __name__ == '__main__':
    unittest.main()
