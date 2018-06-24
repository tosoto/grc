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

    plugin = ''


    def enableTerminalOutput(self, state):
        assert type(state) == types.BooleanType, '"state" must be boolean type'
        self.stdOut.enable_terminal_output(state)

    def edgeLabel(self, sourceNode, destinationNode):
        for edge in self.edgeList:
            if (sourceNode == edge.sourceNode) and (destinationNode == edge.destinationNode):
                return edge.label
        return ''

    def getNodeLabel(self, id):
        for node in self.nodeList:
            if node.id == id:
                return node.label

    def findStartEndNodes(self):

        for node in self.nodeList:
            if node.label == 'Start':
                self.startNode.append(node.id)
                self.stdOut.print_debug("Start node id: %s" % self.startNode[-1])
            if node.relatedNodes == []:
                self.endNode.append(node.id)
                self.stdOut.print_debug('End node id: %s' % self.endNode[-1])

    def generatePaths(self):

        for singleStartNode in self.startNode:
            self.pathList.append([ singleStartNode ])

        self.stdOut.print_debug('Path list: + ' + str(self.pathList))

        for x in range(0, len(self.pathList)):
            self.addPath(x)

        self.stdOut.print_debug(self.pathList)

    def printScenariosOnStdOut(self):
        for pathId in range(0, len(self.pathList)):
            self.stdOut.my_print("Scenario: %s" % (pathId + 1))
            self.stdOut.my_print("Step\t|\tAction \t\t\t|\tState")
            step = 1
            sourceNode = None
            for nodeId in self.pathList[ pathId ]:
                self.stdOut.my_print("Step: %s\t|\t%s\t|\t%s" % (step, self.edgeLabel(sourceNode, nodeId), self.getNodeLabel(nodeId)))
                step = step + 1
                sourceNode = nodeId
            self.stdOut.my_print('**************************************************************************************************')

    def parseCmdParams(self):
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

        if not 'graphml' in self.GRAPH_NAME:
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

    def getNodeListFromGraphFile(self):

        self.edgeList, self.nodeList = self.plugin.runByExtension(self.GRAPH_NAME.split('.')[1], { 'file_name':self.GRAPH_NAME, 'output':self.stdOut })

    def addPath(self, pathListPointer):

        node = self.pathList[ pathListPointer ][-1]

        self.stdOut.print_debug("1: addPath: node: %s pointer: %s" % (node, pathListPointer))
        self.stdOut.print_debug("2:path list: %s" % (self.pathList))

        for childNode in self.nodeList[ node ].relatedNodes:
            self.stdOut.print_debug('3: addPath: childNode: %s' % (childNode))
            path = list(self.pathList[ pathListPointer ])

            loopDetected = childNode in path

            self.stdOut.print_debug("4: path: %s" % (path))
            self.pathList.append(path)
            self.pathList[ -1 ].append(childNode)

            self.stdOut.print_debug('5. childNode: %s' % childNode)
            self.stdOut.print_debug('6. path: %s' % path)
            if not loopDetected:
                self.addPath(len(self.pathList) - 1)

    def findFinishedPathsWithNode(self, node):
        for path in self.pathList:
            if node in path:
                for endNode in self.endNode:
                    if endNode in path:
                        return path
        return False

    def finishPaths(self):
        for pathPointer in range(0, len(self.pathList)):
            endNodeFound = False
            for endNode in self.endNode:
                if endNode in self.pathList[pathPointer]:
                    endNodeFound = True
            if not endNodeFound:
                finishedPath = self.findFinishedPathsWithNode(self.pathList[pathPointer][-1])
                copyFromElementIndex = finishedPath.index(self.pathList[pathPointer][-1])

                for x in range(copyFromElementIndex + 1, len(finishedPath)):
                    self.pathList[pathPointer].append(finishedPath[x])

    def removeRepeatedPaths(self):
        newPathList = []
        for path in self.pathList:
            if not path in newPathList:
                newPathList.append(path)
        self.pathList = newPathList

    def createScenarios(self):

        for pathId in range(0, len(self.pathList)):

            sourceNode = None

            scenario = Scenario(pathId, '', [])

            for nodeId in self.pathList[ pathId ]:

                scenario.addStep(self.edgeLabel(sourceNode, nodeId), self.getNodeLabel(nodeId))
                sourceNode = nodeId

            self.scenariosList.append(scenario)

    def go(self):

        crawlerStartTime = time.time()

        self.plugin = PluginList.init()

        self.parseCmdParams()

        if self.LIST_PLUGINS:
            self.plugin.listPlugins()
            quit()

        self.stdOut.print_debug('GRAPH_NAME: %s' % self.GRAPH_NAME)

        self.getNodeListFromGraphFile()
        self.stdOut.print_debug('Node list: ')
        for node in self.nodeList:
            self.stdOut.print_debug(str(node))

        self.findStartEndNodes()

        self.generatePaths()

        if not self.STOP_AT_REPEATED_NODE:
            self.finishPaths()
            self.removeRepeatedPaths()

        self.createScenarios()

        if self.stdOut.debugFlag:
            for scenario in self.scenariosList:
                self.stdOut.print_debug('Scenario: %s ------------------' % scenario.id)
                for step in scenario.steps:
                    self.stdOut.print_debug('step.action.label: %s' % step.action.label)
                    self.stdOut.print_debug('step.action.code: %s' % step.action.code)
                    self.stdOut.print_debug('step.node.label: %s' % step.node.label)
                    self.stdOut.print_debug('step.node.code: %s' % step.node.code)

        if self.outputPluginLang != 'stdOut':
            self.plugin.runByLanguage(self.outputPluginLang, { 'scenarios':self.scenariosList, 'stdOut':self.stdOut})
        elif self.outputPlugin != 'stdOut':
             self.plugin.runByExtension(self.outputPlugin, { 'scenarios':self.scenariosList, 'stdOut':self.stdOut })
        else:
            self.printScenariosOnStdOut()

        self.stdOut.my_print("--- Crawler finised in %s seconds ---" % (time.time() - crawlerStartTime))


if __name__ == '__main__':
    grc = GrcClass()
    grc.go()
