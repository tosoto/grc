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


import Step

class Scenario:
    id = None
    name = None
    steps = []

    def __init__( self, id, name, steps ):
        self.id = id
        self.name = name
        self.steps = steps

    def __str__( self ):
        return str( self.__dict__ )

    def addStep( self, actionDescription, stateDescription ):
        self.steps.append( Step.Step( len( self.steps ), actionDescription, stateDescription ) )

    def getSteps( self ):
        return self.steps
