#!/usr/bin/env python

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
    
