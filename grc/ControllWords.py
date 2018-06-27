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


class ControlWord:
    word = ''
    description = ''
    prefix = '\\'

    def __init__(self, word, description):
        self.word = "%s%s" % (self.prefix, word)
        self.description = description

    def return_description(self):
        return self.description

    def __str__(self):
        return self.word

    def get_word_with_description(self):
        return '%s\t%s' % (self.word, self.description)


class ControlWords:
    stdOut = ''
    code = ControlWord('code:', 'Insert your code just after this word. \
                                Code will be inserted in the processed scenario files')
    start = ControlWord('start', 'Grc will start processing from node marked with this word.\
                                 Not obligarory')
    do_not_process = ControlWord('#', 'Exclude node from processing. No path containing excluded node\
                                      will be saved')

    def __init__(self, stdOut):
        self.stdOut = stdOut
        self.stdOut.print_debug("ControlWords class initialization")

    def display_control_words(self):
        self.stdOut.my_print('This words can be used on graph to enable following features:')
        self.stdOut.my_print('\t%s' % self.start.get_word_with_description())
        self.stdOut.my_print('\t%s' % self.code.get_word_with_description())
        self.stdOut.my_print('\t%s' % self.do_not_process.get_word_with_description())
