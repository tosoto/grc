#    This is part of grc module. Class provides plugins handling.
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

import importlib
import sys

class Plugin:
    #--- Plugin types:
    UNKNOWN_TYPE_MODULE = 0
    INPUt_MODULE = 1
    OUTPUT_MODULE = 2
    PROCESSING_MODULE = 3
    #-----------------

    name = ''
    type = UNKNOWN_TYPE_MODULE
    handle = ''
    extension = ''
    language = ''

    def __init__( self, name ):
        self.name = name

        sys.path.append( 'plugins/' )

        try:
            self.handle = importlib.import_module( self.name )
            self.extension = self.handle.extension
            self.language = self.handle.language
            self.type = self.handle.type
        except Exception,e:
            print( "Error in plugin: %s" % self.name )
            print( e )
            quit()

    def run( self, parameters ):
        self.handle.run( parameters )
