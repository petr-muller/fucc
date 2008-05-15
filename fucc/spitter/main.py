#!/usr/bin/env python
#------------------------------------------------------------------------------#
#    This file is part of fucc.                                                #
#                                                                              #
#    fucc is free software: you can redistribute it and/or modify              #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, version 3 of the License.                   #
#                                                                              #
#    fucc is distributed in the hope that it will be useful,                   #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with fucc.  If not, see <http://www.gnu.org/licenses/>.             # 
#------------------------------------------------------------------------------#

from bnf_parser import yacc
import sys
import grammar
import logger
import C_director
import generator

if __name__ == "__main__":
    gram_file = open(sys.argv[1])
    gram = gram_file.read()
    gram_file.close()

    my_logger = logger.Logger(sys.stdout, sys.stderr, int(sys.argv[2]))
    grammar.plugLogger(my_logger)

    my_grammar = yacc.parse(gram)

    direct = C_director.Director()
    C_director.plugLogger(my_logger)
    direct.loadGrammar(my_grammar)
    direct.setMaxDepth(5)


    my_gen = generator.Generator()
    generator.plugLogger(my_logger)
    my_gen.plugDirector(direct)
    print my_gen.generate('program')
    
