#    Simple graph crawler walking on all graph edges and showing them as tests scenarios. Use GraphML files.
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


import time
import argparse
import types
import xml.etree.ElementTree
import os
import PluginList
from Output import *
from Edge import *
from Node import *
from Step import *
from Scenario import *
import sys
import ControllWords


class GrcClass:
    stdOut = Output()

    PYEXCEL_OUTPUT = True
    outputPlugin = ''
    outputPluginLang = ''
    TEST_SCRIPTS_DIR = 'TEST_SCRIPTS'
    GENERATE_CODE = False
    GRAPH_NAME = ''
    STOP_AT_REPEATED_NODE = False
    LIST_PLUGINS = False
    REDUCE_PATHS = False

    nodeList = []
    edgeList = []
    startNode = []
    endNode = []
    start_edge = []
    end_edge = []
    pathList = []
    scenariosList = []

    scenarios = {}

    control_words = []

    plugin = ''

    def enable_terminal_output(self, state):
        assert isinstance(state, bool), '"state" must be bool type'
        self.stdOut.enable_terminal_output(state)

    def edge_label(self, source_node, destination_node):
        for edge in self.edgeList:
            if (source_node == edge.sourceNode) and (destination_node == edge.destinationNode):
                return edge.label
        return ''

    def get_node_label(self, _id):
        for node in self.nodeList:
            if node.id == _id:
                return node.label

    def find_start_end_nodes(self):

        for node in self.nodeList:
            if str(self.control_words.start) in node.label:
                self.startNode.append(node.id)
                self.stdOut.print_debug("Start node id: %s" % self.startNode[-1])
            if not node.related_edges:
                self.endNode.append(node.id)
                self.stdOut.print_debug('End node id: %s' % self.endNode[-1])

        for nodeId in self.startNode:
            for edge in self.edgeList:
                if edge.sourceNode == nodeId:
                    self.start_edge.append(edge)

        for nodeId in self.endNode:
            for edge in self.edgeList:
                if edge.destinationNode == nodeId:
                    self.end_edge.append(edge)

        if not self.startNode:
            self.stdOut.print_error('"%s" node not found' % self.control_words.start)

    def generate_paths(self):

        for singleStartEdge in self.start_edge:
            self.pathList.append([singleStartEdge])

        self.stdOut.print_debug('Path list: + ' + str(self.pathList))

        for x in range(0, len(self.pathList)):
            self.add_path(x)

        self.stdOut.print_debug(self.pathList)

    def print_scenarios_on_std_out(self):
        max_length_step = 0
        max_length_action = 0
        max_length_state = 0
        for scenario in self.scenariosList:
            for step in scenario.steps:
                if len(str(step.id)) > max_length_step:
                    max_length_step = len(str(step.id))
                for line in step.action.label.split('\n'):
                    if len(line) > max_length_action:
                        max_length_action = len(line)
                for line in step.node.label.split('\n'):
                    if len(line) > max_length_state:
                        max_length_state = len(line)

        scenario_bar = ''
        scenario_bar_length = len('| Step  |  |  |') + max_length_step + max_length_state + max_length_action
        for s in range( 0, scenario_bar_length):
            scenario_bar += '-'

        self.stdOut.my_print(scenario_bar)
        for scenario in self.scenariosList:
            self.stdOut.my_print("Scenario: %s" % (scenario.id))
            for step in scenario.steps:

                step_action_lines = step.action.label.split('\n')
                step_node_lines = step.node.label.split('\n')

                if len(step_action_lines) < len(step_node_lines):
                    for l in range( len(step_action_lines), len(step_node_lines)):
                        step_action_lines.append('\n')
                elif len(step_node_lines) < len(step_action_lines):
                    for l in range( len(step_node_lines), len(step_action_lines)):
                        step_node_lines.append('\n')

                max_step_height = len(step_node_lines)

                for line_id in range(0, max_step_height):

                    step_id = str(step.id)
                    step_action_line = step_action_lines[line_id]
                    step_node_line = step_node_lines[line_id]

                    for l in range(len(str(step_id)), max_length_step):
                        step_id += ' '
                    for l in range(len(step_action_line), max_length_action):
                        step_action_line += ' '

                    for l in range(len(step_node_line), max_length_state):
                        step_node_line += ' '

                    if line_id == 0:
                        self.stdOut.my_print( "| Step %s | %s | %s |" % (step_id, step_action_line, step_node_line))
                    else:
                        self.stdOut.my_print( "|         | %s | %s |" % (step_action_line, step_node_line))

            self.stdOut.my_print(scenario_bar)

    def parse_cmd_params(self):
        parser = argparse.ArgumentParser(description = 'Crawl over provided graph all edges and displayed them as test scenarios')
        parser.add_argument('-i', '--input', type=str, help='GraphML file name, this graph will be analyzed by the program')
        parser.add_argument('-d', '--debug', action = 'store_true', help = 'Enables debug. Do not use it unless you develope program ;)')
        parser.add_argument('-o', '--outputType', type=str, help = 'File type format to save scenarios. Default it ods.')
        parser.add_argument('-e', '--extension', type=str, help='File type extension format to save scenarios. Default it ods.')
        parser.add_argument('-s', '--stopatrepeatednode', action = 'store_true', help = 'Stops at repeated node, does not finishes path')
        parser.add_argument('-l', '--listplugins', action = 'store_true', help = 'Lists all available plugins')
        parser.add_argument('-r', '--reduce_scenarios', action = 'store_true', help='leaves only scenarios with at least one step not covered by other scenario')

        args = parser.parse_args()

        if args.input is not None:
            self.GRAPH_NAME = args.input
        else:
            self.GRAPH_NAME = 'examples/browser'

        if 'graphml' not in self.GRAPH_NAME:
            self.GRAPH_NAME = self.GRAPH_NAME + '.graphml'

        self.stdOut.enable_debug(args.debug)

        if args.extension is not None:
            self.outputPlugin = args.extension
        else:
            self.outputPlugin = 'stdOut'

        if args.outputType is not None:
            self.outputPluginLang = args.outputType
        else:
            self.outputPluginLang = 'stdOut'

        self.STOP_AT_REPEATED_NODE = args.stopatrepeatednode

        if args.listplugins is not None:
            self.LIST_PLUGINS = args.listplugins

        if args.reduce_scenarios is not None:
            self.REDUCE_PATHS = args.reduce_scenarios

        self.stdOut.print_debug('GRAPH_NAME: %s' % self.GRAPH_NAME)

    def get_node_list_from_graph_file(self):
        extension = self.GRAPH_NAME.split('.')[1]
        params = {'file_name': self.GRAPH_NAME, 'output': self.stdOut}
        self.edgeList, self.nodeList = self.plugin.run_by_extension(extension, params)

    def add_path(self, path_list_pointer):

        node = self.pathList[path_list_pointer][-1].destinationNode

        self.stdOut.print_debug("1: addPath: node: %s pointer: %s" % (node, path_list_pointer))
        self.stdOut.print_debug("2:path list: %s" % self.pathList)

        for rel_edge in self.nodeList[node].related_edges:
            self.stdOut.print_debug('3: addPath: rel_edge: %s' % rel_edge)
            path = list(self.pathList[path_list_pointer])

            loop_detected = rel_edge in path

            self.stdOut.print_debug("4: path: %s" % path)
            self.pathList.append(path)
            self.pathList[-1].append(rel_edge)

            self.stdOut.print_debug('5. rel_edge: %s' % rel_edge)
            self.stdOut.print_debug('6. path: %s' % path)
            if not loop_detected:
                self.add_path(len(self.pathList) - 1)

    def find_finished_paths_with_node(self, node):
        for path in self.pathList:
            if node in path:
                for endNode in self.endNode:
                    if endNode in path:
                        return path
        return False

    def find_finished_paths_with_edge(self, edge):
        for path in self.pathList:
            if edge in path:
                for end_edge in self.end_edge:
                    if end_edge in path:
                        return path
        return False

    def finish_paths(self):
        for pathPointer in range(0, len(self.pathList)):
            end_edge_found = False
            for end_edge in self.end_edge:
                if end_edge in self.pathList[pathPointer]:
                    end_edge_found = True
            if not end_edge_found:
                finished_path = self.find_finished_paths_with_edge(self.pathList[pathPointer][-1])
                if finished_path:
                    copy_from_element_index = finished_path.index(self.pathList[pathPointer][-1])

                    for x in range(copy_from_element_index + 1, len(finished_path)):
                        self.pathList[pathPointer].append(finished_path[x])

    def remove_repeated_paths(self):
        new_path_list = []
        for path in self.pathList:
            if path not in new_path_list:
                new_path_list.append(path)
        self.pathList = new_path_list

    def reduce_paths(self):
        path_removed = True
        while path_removed:
            path_removed = False
            for path in self.pathList:
                unique_edge_found = False
                for edge in path:
                    found_counter = 0
                    for another_path in self.pathList:
                        if not (another_path == path):
                            if edge in another_path:
                               found_counter += 1
                               break
                    if found_counter == 0:
                        unique_edge_found = True
                if not unique_edge_found:
                    self.pathList.remove(path)
                    path_removed = True

    def create_scenarios(self):

        for pathId in range(0, len(self.pathList)):

            scenario = Scenario(pathId + 1, '', [], self.control_words)

            for edge in self.pathList[pathId]:

                scenario.add_step(edge.label, self.get_node_label(edge.destinationNode))

            self.scenariosList.append(scenario)

    def remove_paths_with_excluded_elements(self):
        path_list_without_excluded_elements = []
        for path in self.pathList:
            excluded_element_detected = False
            for edge in path:
                if str(self.control_words.excluded_path) in edge.label:
                    excluded_element_detected = True
                if str(self.control_words.excluded_path) in self.get_node_label(edge.destinationNode):
                    excluded_element_detected = True

            if not excluded_element_detected:
                path_list_without_excluded_elements.append(path)

        self.pathList = path_list_without_excluded_elements

    def clear_labels_of_exclued_elements(self):
        path_list_excluded_edges = []
        for path in self.pathList:
            path_excuded_edges = []
            for edge in path:
                if str(self.control_words.excluded_node) in edge.label:
                    edge.label = ''
                path_excuded_edges.append(edge)
            path_list_excluded_edges.append(path_excuded_edges)
        self.pathList = path_list_excluded_edges
        node_list_excluded = []
        for node in self.nodeList:
            if str(self.control_words.excluded_node) in node.label:
                node.label = ''
            node_list_excluded.append(node)
        self.nodeList = node_list_excluded


    def go(self):

        crawler_start_time = time.time()

        self.plugin = PluginList.init()

        self.parse_cmd_params()

        if self.LIST_PLUGINS:
            self.plugin.list_plugins()
            quit()

        self.stdOut.print_debug('GRAPH_NAME: %s' % self.GRAPH_NAME)

        self.get_node_list_from_graph_file()
        self.stdOut.print_debug('Node list: ')
        for node in self.nodeList:
            self.stdOut.print_debug(str(node))

        self.find_start_end_nodes()

        self.generate_paths()

        self.remove_paths_with_excluded_elements()
        self.clear_labels_of_exclued_elements()

        if not self.STOP_AT_REPEATED_NODE:
            self.finish_paths()
            self.remove_repeated_paths()

        if self.REDUCE_PATHS:
            self.reduce_paths()

        self.create_scenarios()

        if self.stdOut.debugFlag:
            for scenario in self.scenariosList:
                self.stdOut.print_debug('Scenario: %s ------------------' % scenario.id)
                for step in scenario.steps:
                    self.stdOut.print_debug('step.action.label: %s' % step.action.label)
                    self.stdOut.print_debug('step.action.code: %s' % step.action.code)
                    self.stdOut.print_debug('step.node.label: %s' % step.node.label)
                    self.stdOut.print_debug('step.node.code: %s' % step.node.code)

        if self.outputPluginLang != 'stdOut':
            self.plugin.run_by_language(self.outputPluginLang, {'scenarios': self.scenariosList, 'stdOut': self.stdOut})
        elif self.outputPlugin != 'stdOut':
            self.plugin.run_by_extension(self.outputPlugin, {'scenarios': self.scenariosList, 'stdOut': self.stdOut})
        else:
            self.print_scenarios_on_std_out()

        self.stdOut.my_print("--- %s scenarios generated" % len(self.scenariosList))
        self.stdOut.my_print("--- Crawler finised in %s seconds ---" % (time.time() - crawler_start_time))

    def __init__(self):
        sys.path.append('plugins/')
        self.control_words = ControllWords.ControlWords(self.stdOut)

if __name__ == '__main__':
    grc = GrcClass()
    grc.go()
