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


import os
import importlib
from Plugin import *

PLUGINS_MAIN_FOLDER = 'plugins'
PLUGINS_INIT = '__init__.py'
PLUGINS_INIT_FULL_PATH = '%s/%s' % (PLUGINS_MAIN_FOLDER, PLUGINS_INIT)

class PluginList:

    pluginList = []

    def __init__(self):

        if not os.path.exists(PLUGINS_MAIN_FOLDER):
            os.makedirs(PLUGINS_MAIN_FOLDER)
        if not os.path.exists(PLUGINS_INIT_FULL_PATH):
            open(PLUGINS_INIT_FULL_PATH, 'a').close()

        self.loadPlugins()

    def reloadPlugins(self):
        self.loadPlugins()

    def loadPlugins(self):
        potentialPlugins = os.listdir(PLUGINS_MAIN_FOLDER)
        potentialPlugins.remove(PLUGINS_INIT)

        self.pluginList = []
        for pluginName in potentialPlugins:
            if not (PLUGINS_INIT in pluginName) and not ('Plugin.py' in pluginName):
                if ('.py' in pluginName) and (not '.pyc' in pluginName):
                    pluginName = pluginName.replace('.py', '')
                    self.pluginList.append(Plugin(pluginName))

    def listPlugins(self):
        for plugin in self.pluginList:
            print('-----------------------------------------------------------------------------------')
            print('Plugin: %s\n  Extension: %s\n  Type: %s\n  Language: %s' % (plugin.name, plugin.extension, plugin.type, plugin.language))

    def runByName(self, name, parameters):
        for plugin in self.pluginList:
            if name == plugin.name:
                return plugin.handle.run(parameters)
        return False

    def runByExtension(self, extension, parameters):
        for plugin in self.pluginList:
            if extension == plugin.extension:
                return plugin.handle.run(parameters)
        print("Plugin %s not found!" % extension)
        return False

    def runByLanguage(self, language, parameters):
        for plugin in self.pluginList:
            if language == plugin.language:
                return plugin.handle.run(parameters)
        print("Plugin for language %s not found!" % language)
        return False

def init():
    return PluginList()

if __name__ == '__main__':
    pluginList = init()
