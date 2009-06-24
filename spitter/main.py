#!/usr/bin/env python
"""This script is a driving script for Spitter, the random C sentences 
generator."""
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
from optparse import OptionParser

if __name__ == "__main__":
  opt = OptionParser()
  opt.add_option("-g", "--grammar", dest="grammar",
                        help="use grammar defined in FILE", metavar="FILE")
  opt.add_option("-v", "--verbose", default=0, dest="verbose",
                        help="Verbosity level (0-2)", metavar="LEVEL")
  opt.add_option("-b", "--blockdepth", default=5, dest="bd", metavar="DEPTH",
                        help="Sets maximum of block repetition")
  opt.add_option("-f", "--functions", default=1, dest="fc", metavar="MAX",
                        help="Sets maximum of single function calls")
  opt.add_option("-e", "--exptdepth", default=5, dest="ed", metavar="DEPTH",
                        help="Sets average recursivity of expressions")

  (options, args) = opt.parse_args()
  if not options.grammar:
    print >> sys.stderr, "Grammar file must be supplied"
    sys.exit(1)
  gram_file = open(options.grammar)
  gram = gram_file.read()
  gram_file.close()

  my_logger = logger.Logger(sys.stdout, sys.stderr, int(options.verbose))
  grammar.plugLogger(my_logger)

  my_grammar = yacc.parse(gram)

  direct = C_director.Director()
  C_director.plugLogger(my_logger)
  direct.loadGrammar(my_grammar)
  direct.setMaxDepth(int(options.bd))
  direct.setMaxFunction(int(options.fc))
  direct.setExprDepth(int(options.ed))

  my_gen = generator.Generator()
  generator.plugLogger(my_logger)
  my_gen.plugDirector(direct)
  print my_gen.generate('program')
    
