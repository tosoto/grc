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

    def enableDebug(self, state):
        assert type(state) is types.BooleanType, 'state must be a bool'
        self.debugFlag = state

    def enableTerminalOutput(self, state):
        assert type(state) is types.BooleanType, 'state must be a bool'
        self.terminalOutput = state

    def clearConsoleOut(self):
        self.consoleOut = ''

    def getConsole(self):
        return self.consoleOut

    def myPrint(self, text):
        text = str(text)
        if self.terminalOutput:
            print(text)
        else:
            self.consoleOut = self.consoleOut + text

    def printDebug(self, text):
        if self.debugFlag:
            self.myPrint(text)

    def printError(self, text):
        self.myPrint("ERROR: %s" % text)
        quit()

    def printWarning(self, text):
        self.myPrint("Warning: %s\n" % text)
