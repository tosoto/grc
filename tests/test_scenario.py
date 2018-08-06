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
import Scenario
import Step
import ControllWords
import Output

class TestStringMethod(unittest.TestCase):

    def test_scenario_init(self):

        control_words = ControllWords.ControlWords(Output.Output())

        steps = [Step.Step(7, "abc\n\code: ghi", "def\n\code:jkl", control_words)]
        scenario = Scenario.Scenario(3, "scn", steps, control_words)

        self.assertEqual(scenario.id, 3)
        self.assertEqual(scenario.name, "scn")
        self.assertEqual(scenario.steps, steps)


    def test_scenario_addStep(self):

        control_words = ControllWords.ControlWords(Output.Output())

        steps = [Step.Step(7, "abc\n\code: ghi", "def\n\code:jkl", control_words)]
        scenario = Scenario.Scenario(3, "scn", steps, control_words)

        scenario.add_step("act", "nod")

        self.assertEqual(scenario.steps[1].action.description, ["act"])
        self.assertEqual(scenario.steps[1].node.description, ["nod"])


    def test_scenario_getSteps(self):

        control_words = ControllWords.ControlWords(Output.Output())

        steps = [Step.Step(7, "abc\n\code: ghi", "def\n\code:jkl", control_words)]
        scenario = Scenario.Scenario(3, "scn", steps, control_words)

        self.assertEqual(scenario.get_steps(), [scenario.steps[0]])

    def test_scenario_get_id(self):

        control_words = ControllWords.ControlWords(Output.Output())

        steps = [Step.Step(7, "abc\n\code: ghi", "def\n\code:jkl", control_words)]

        scenario1 = Scenario.Scenario(1, "scn", steps, control_words)
        scenario9 = Scenario.Scenario(9, "scn", steps, control_words)
        scenario10 = Scenario.Scenario(10, "scn", steps, control_words)
        scenario99 = Scenario.Scenario(99, "scn", steps, control_words)
        scenario100 = Scenario.Scenario(100, "scn", steps, control_words)
        scenario999 = Scenario.Scenario(999, "scn", steps, control_words)
        scenario1000 = Scenario.Scenario(1000, "scn", steps, control_words)
        scenario9999 = Scenario.Scenario(9999, "scn", steps, control_words)

        self.assertEqual(scenario1.get_id_str(), '0001')
        self.assertEqual(scenario9.get_id_str(), '0009')
        self.assertEqual(scenario10.get_id_str(), '0010')
        self.assertEqual(scenario99.get_id_str(), '0099')
        self.assertEqual(scenario100.get_id_str(), '0100')
        self.assertEqual(scenario999.get_id_str(), '0999')
        self.assertEqual(scenario1000.get_id_str(), '1000')
        self.assertEqual(scenario9999.get_id_str(), '9999')


if __name__ == "__main__":
    unittest.main()
