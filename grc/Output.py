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


import types


class Output:
    consoleOut = ''
    debugFlag = False
    terminalOutput = True

    def enable_debug(self, state):
        assert type(state) is types.BooleanType, 'state must be a bool'
        self.debugFlag = state

    def enable_terminal_output(self, state):
        assert type(state) is types.BooleanType, 'state must be a bool'
        self.terminalOutput = state

    def clear_console_out(self):
        self.consoleOut = ''

    def get_console(self):
        return self.consoleOut

    def my_print(self, text):
        text = str(text)
        if self.terminalOutput:
            print(text)
        else:
            self.consoleOut = self.consoleOut + text

    def print_debug(self, text):
        if self.debugFlag:
            self.my_print(text)

    def print_error(self, text):
        self.my_print("ERROR: %s" % text)
        quit()

    def print_warning(self, text):
        self.my_print("Warning: %s\n" % text)
