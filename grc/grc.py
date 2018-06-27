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

    nodeList = []
    edgeList = []
    startNode = []
    endNode = []
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
            if node.label == str(self.control_words.start):
                self.startNode.append(node.id)
                self.stdOut.print_debug("Start node id: %s" % self.startNode[-1])
            if not node.relatedNodes:
                self.endNode.append(node.id)
                self.stdOut.print_debug('End node id: %s' % self.endNode[-1])

        if not self.startNode:
            self.stdOut.print_error('"%s" node not found' % self.control_words.start)

    def generate_paths(self):

        for singleStartNode in self.startNode:
            self.pathList.append([singleStartNode])

        self.stdOut.print_debug('Path list: + ' + str(self.pathList))

        for x in range(0, len(self.pathList)):
            self.add_path(x)

        self.stdOut.print_debug(self.pathList)

    def print_scenarios_on_std_out(self):
        for pathId in range(0, len(self.pathList)):
            self.stdOut.my_print("Scenario: %s" % (pathId + 1))
            self.stdOut.my_print("Step\t|\tAction \t\t\t|\tState")
            step = 1
            source_node = None
            for nodeId in self.pathList[pathId]:
                self.stdOut.my_print("Step: %s\t|\t%s\t|\t%s" % (step, self.edge_label(source_node, nodeId), self.get_node_label(nodeId)))
                step = step + 1
                source_node = nodeId
            self.stdOut.my_print('**************************************************************************************************')

    def parse_cmd_params(self):
        parser = argparse.ArgumentParser(description = 'Crawl over provided graph all edges and displayed them as test scenarios')
        parser.add_argument('-i', '--input', type=str, help='GraphML file name, this graph will be analyzed by the program')
        parser.add_argument('-d', '--debug', action = 'store_true', help = 'Enables debug. Do not use it unless you develope program ;)')
        parser.add_argument('-o', '--outputType', type=str, help = 'File type format to save scenarios. Default it ods.')
        parser.add_argument('-e', '--extension', type=str, help='File type extension format to save scenarios. Default it ods.')
        parser.add_argument('-s', '--stopatrepeatednode', action = 'store_true', help = 'Stops at repeated node, does not finishes path')
        parser.add_argument('-l', '--listplugins', action = 'store_true', help = 'Lists all available plugins')

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

        self.stdOut.print_debug('GRAPH_NAME: %s' % self.GRAPH_NAME)

    def get_node_list_from_graph_file(self):
        extension = self.GRAPH_NAME.split('.')[1]
        params = {'file_name': self.GRAPH_NAME, 'output': self.stdOut}
        self.edgeList, self.nodeList = self.plugin.run_by_extension(extension, params)

    def add_path(self, path_list_pointer):

        node = self.pathList[path_list_pointer][-1]

        self.stdOut.print_debug("1: addPath: node: %s pointer: %s" % (node, path_list_pointer))
        self.stdOut.print_debug("2:path list: %s" % self.pathList)

        for childNode in self.nodeList[node].relatedNodes:
            self.stdOut.print_debug('3: addPath: childNode: %s' % childNode)
            path = list(self.pathList[path_list_pointer])

            loop_detected = childNode in path

            self.stdOut.print_debug("4: path: %s" % path)
            self.pathList.append(path)
            self.pathList[-1].append(childNode)

            self.stdOut.print_debug('5. childNode: %s' % childNode)
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

    def finish_paths(self):
        for pathPointer in range(0, len(self.pathList)):
            end_node_found = False
            for endNode in self.endNode:
                if endNode in self.pathList[pathPointer]:
                    end_node_found = True
            if not end_node_found:
                finished_path = self.find_finished_paths_with_node(self.pathList[pathPointer][-1])
                copy_from_element_index = finished_path.index(self.pathList[pathPointer][-1])

                for x in range(copy_from_element_index + 1, len(finished_path)):
                    self.pathList[pathPointer].append(finished_path[x])

    def remove_repeated_paths(self):
        new_path_list = []
        for path in self.pathList:
            if path not in new_path_list:
                new_path_list.append(path)
        self.pathList = new_path_list

    def create_scenarios(self):

        for pathId in range(0, len(self.pathList)):

            source_node = None

            scenario = Scenario(pathId, '', [], self.control_words)

            for nodeId in self.pathList[pathId]:

                scenario.add_step(self.edge_label(source_node, nodeId), self.get_node_label(nodeId))
                source_node = nodeId

            self.scenariosList.append(scenario)

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

        if not self.STOP_AT_REPEATED_NODE:
            self.finish_paths()
            self.remove_repeated_paths()

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

        self.stdOut.my_print("--- Crawler finised in %s seconds ---" % (time.time() - crawler_start_time))

    def __init__(self):
        sys.path.append('plugins/')
        self.control_words = ControllWords.ControlWords(self.stdOut)

if __name__ == '__main__':
    grc = GrcClass()
    grc.go()
