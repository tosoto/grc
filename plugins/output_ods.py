#    This is part of grc module. Plugin provides export scenarios to text files. Only descriptions are saved.
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


import os
import Scenario
import Step
import collections

#---------- OBLIGATORY ------------
# extension = <file extension for plugin>
# type = <value> - please see 'Plugin.py'
extension = 'ods'
type = 2 # output module
language = 'libreoffice_calc'
#----------------------------------

def run(parameters):
    stdOut = parameters['stdOut']
    scenarios = parameters['scenarios']

    outName = 'Scenarios.ods'

    try:
        import pyexcel_ods
    except:
        stdOut.print_error("Couldn't import pyexcel-ods - scnearios export to the ods format would not be possible\nPlease install pyexcel-ods")

    data = collections.OrderedDict()
    exportSheetSteps = [ ['Scenario name','Step', 'Action', 'State'] ]

    for scenario in scenarios:

        scenarioSteps = [['Step', 'Action', 'State']]

        for step in scenario.steps:
            scenarioSteps.append([ step.id, step.action.label, step.node.label ])
            exportSheetSteps.append([ 'Scenaio %s' % scenario.id, step.id, step.action.label, step.node.label ])

        data.update({ 'Scenario %s' % scenario.id : scenarioSteps })

    data.update({ 'Export sheet' : exportSheetSteps })
    pyexcel_ods.save_data(outName, data)
    stdOut.my_print('%s scenarios saved to "%s"' % (len(scenarios), outName))
