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
import Step
import ControllWords
import Output

class TestStringMethod(unittest.TestCase):

    def test_step_stepObj_init(self):

        control_words = ControllWords.ControlWords(Output.Output())

        stepObj = Step.Step.StepObj("lab\n\code:cod", control_words)

        self.assertEqual(stepObj.description, ['lab', '\code:cod'])
        self.assertEqual(stepObj.label, 'lab')
        self.assertEqual(stepObj.code, 'cod')


    def test_step_stepObj_addCodeLine(self):

        control_words = ControllWords.ControlWords(Output.Output())

        stepObj = Step.Step.StepObj('', control_words)

        stepObj.add_code_line('cod')

        self.assertEqual(stepObj.code, 'cod\n')


    def test_step_stepObj_addLabelLine(self):

        control_words = ControllWords.ControlWords(Output.Output())

        stepObj = Step.Step.StepObj('', control_words)

        stepObj.add_label_line('lab')

        self.assertEqual(stepObj.label, 'lab\n')


    def test_step_stepObj_str(self):

        control_words = ControllWords.ControlWords(Output.Output())

        stepObj = Step.Step.StepObj("lab\n\code:cod", control_words)

        self.assertEqual(str(stepObj), "{'code': 'cod', 'description': ['lab', '\\\\code:cod'], 'label': 'lab'}")

    def test_step_init(self):

        control_words = ControllWords.ControlWords(Output.Output())

        step = Step.Step(7, 'abc\n\code: ghi', 'def\n\code:jkl', control_words)

        self.assertEqual(step.id, 7)

        self.assertEqual(step.action.description, ['abc', '\code: ghi'])
        self.assertEqual(step.action.label, 'abc')
        self.assertEqual(step.action.code, ' ghi')

        self.assertEqual(step.node.description, ['def', '\code:jkl'])
        self.assertEqual(step.node.label, 'def')
        self.assertEqual(step.node.code, 'jkl')


    def test_step_str(self):

        control_words = ControllWords.ControlWords(Output.Output())

        step = Step.Step(7, 'abc\n\code: ghi', 'def\n\code:jkl', control_words)

        self.assertEqual("'action': " in str(step), True)
        self.assertEqual("'node': " in str(step), True)
        self.assertEqual("'id': 7" in str(step), True)

if __name__ == "__main__":
    unittest.main()
