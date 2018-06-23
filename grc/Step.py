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


class Step:

    class StepObj:
        description = None
        label = ''
        code = ''

        def __init__(self, description):
            self.description = description.split('\n')
            for line in self.description:
                if '\code:' in line:
                    self.addCodeLine(line.replace('\code:', ''))
                else:
                    self.addLabelLine(line)

            self.label = self.label[:-1]
            self.code = self.code[:-1]

        def __str__(self):
            return str(self.__dict__)

        def addCodeLine(self, line):
            self.code = self.code + line + '\n'

        def addLabelLine(self, line):
            self.label = self.label + line + '\n'

    id = 1
    action = None
    node = None

    def __init__(self, id, actionDescription, stateDescription):
        self.id = id

        self.action = self.StepObj(actionDescription)
        self.node = self.StepObj(stateDescription)

    def __str__(self):
        return str(self.__dict__)
