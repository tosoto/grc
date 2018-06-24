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

class TestStringMethod(unittest.TestCase):

    def test_scenario_init(self):

        steps = [Step.Step(7, "abc\n\code: ghi", "def\n\code:jkl")]
        scenario = Scenario.Scenario(3, "scn", steps)

        self.assertEqual(scenario.id, 3)
        self.assertEqual(scenario.name, "scn")
        self.assertEqual(scenario.steps, steps)


    def test_scenario_addStep(self):

        steps = [Step.Step(7, "abc\n\code: ghi", "def\n\code:jkl")]
        scenario = Scenario.Scenario(3, "scn", steps)

        scenario.add_step("act", "nod")

        self.assertEqual(scenario.steps[1].action.description, ["act"])
        self.assertEqual(scenario.steps[1].node.description, ["nod"])


    def test_scenario_getSteps(self):

        steps = [Step.Step(7, "abc\n\code: ghi", "def\n\code:jkl")]
        scenario = Scenario.Scenario(3, "scn", steps)

        self.assertEqual(scenario.get_steps(), [scenario.steps[0]])

if __name__ == "__main__":
    unittest.main()
