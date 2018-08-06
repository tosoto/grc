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
    control_words = ''

    def __init__(self, _id, name, steps, control_words):
        self.id = _id
        self.name = name
        self.steps = steps
        self.control_words = control_words

    def __str__(self):
        return str(self.__dict__)

    def add_step(self, action_description, state_description):
        self.steps.append(Step.Step(len(self.steps), action_description, state_description, self.control_words))

    def get_steps(self):
        return self.steps

    def get_id_str(self):
        output = str(self.id)
        if self.id < 10:
            output = '0' + output
        if self.id < 100:
            output = '0' + output
        if self.id < 1000:
            output = '0' + output
        return output
