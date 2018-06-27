#    This is part of grc module. Plugin loads graphml file into nodes and edges list.
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


import xml.etree.ElementTree
import Output
import Node
import Edge

#---------- OBLIGATORY ------------
# extension = <file extension for plugin>
# type = <value> - please see 'Plugin.py'

extension = 'graphml'
type = 1 # input file
language = 'yed'
#----------------------------------

edgeList = []
nodeList = []

def run(parameters):

    file_name = parameters['file_name']
    stdOut = parameters['output']

    ns = {'xmlns' : 'http://graphml.graphdrawing.org/xmlns', 'graphml' : 'http://www.yworks.com/xml/graphml'}

    try:
        graph = xml.etree.ElementTree.parse(file_name)
    except IOError,e:
        stdOut.print_error("Could not open specified file\nDetails:" + str(e))

    graphRoot = graph.getroot()
    g = graphRoot.find('xmlns:graph', ns)

    nodes = g.findall('xmlns:node', ns)
    edges = g.findall('xmlns:edge', ns)

    for node in nodes:
        data = node.findall('xmlns:data', ns)
        for dataElement in data:
            nodeType = dataElement.find('graphml:GenericNode', ns)

            if nodeType is not None:
                id = int(node.attrib['id'].strip('n'))
                label = nodeType.find('graphml:NodeLabel', ns).text
                nodeList.append(Node.Node(id, [], label))

    for edge in edges:
        data = edge.findall('xmlns:data', ns)
        for dataElement in data:
            edgeType =  dataElement.find('graphml:PolyLineEdge', ns)

        if edgeType is not None:
            id = int(edge.attrib['id'].strip('e'))
            source = int(edge.attrib['source'].strip('n'))
            target = int(edge.attrib['target'].strip('n'))
            label = edgeType.find('graphml:EdgeLabel', ns)
            if label is not None:
                label_text = label.text
            else:
                label_text = ''

            edgeList.append(Edge.Edge(source, target, label_text))
            nodeList[source].relatedNodes.append(target)
        else:
            stdOut.print_debug("EDGE NOT KNOWN: \n[%s, %s, %s, %s, %s]" % (edgeType, id, source, target, label))

    return edgeList, nodeList
