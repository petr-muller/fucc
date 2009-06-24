
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

from ply import lex
from ply import yacc
import sys
import grammar

tokens = (
        "NT",         # <nt>            -  nonterminal
        "OPTNT",      # <optnt>{0.5}    -  optional nonterminal
        "WHITESPACE", # all whitespace
        "TERMINAL",   # any character
        "SEPARATOR",  # |               - sign used to separate productions
        "FINISHER",   # ;;;             - sign used to mark finish of a rule
        "ASSIGNATOR", # ::=             - as in '<symbol> ::= <rule>'
        "OPTWEIGHT",  # {0.5}           - used for weighting OPTNT
        "WEIGHTATOR", # %%%             - sign for weighting part start 
        "WEIGHTS"     # (1,2,3)         - tuple with weight
        )

# the following are functions used by PLY lexer module
# each function matches one of the tokens above
# the RE string is the rule for matching tokens

def t_WEIGHTATOR(t):
    r"\s*%%%\s*"
    return t

def t_ASSIGNATOR(t):
    r"\s*::=\s*"
    t.value = t.value.strip()
    return t

def t_FINISHER(t):
    r"\s*;;;\s*"
    return t

def t_SEPARATOR(t):
    r"\s*\|\s*"
    return t

def t_NT(t):
    r"<[a-zA-Z_]+[a-zA-Z0-9_]*>"
    t.value = t.value[1:-1]
    return t

def t_OPTNT(t):
    r"<\[[a-zA-Z_]+[a-zA-Z0-9_]*\]>"
    t.value = t.value[2:-2]
    return t

def t_OPTWEIGHT(t):
    r"\{[01]\.\d\}"
    t.value = float(t.value[1:-1])
    return t

def t_WHITESPACE(t):
    r"\s+"
    return t

def t_WEIGHTS(t):
    r"\((\d+,)*\d+\)\s*"
    return t

def t_TERMINAL(t):
    r"[^\s][^\s<]*"
    return t

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lex.lex()

# these are functions 

def p_final_grammar(p):
    """
    final_grammar : grammar
    """
    p[0] = grammar.Grammar(p[1])

def p_grammar(p):
    """
    grammar : grammar rule
    grammar : rule
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_rule(p):
    """
    rule : NT ASSIGNATOR production_list WEIGHTATOR WEIGHTS FINISHER
    rule : NT ASSIGNATOR production_list FINISHER
    """
    if len(p) == 7:
        p[0] = grammar.Rule(p[1], p[3], eval(p[5]))
    else:
        p[0] = grammar.Rule(p[1], p[3], (1,)*len(p[3]))


def p_production_list_s(p):
    """
    production_list : production_list SEPARATOR total_production
    production_list : total_production
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_total_production(p):
    """
    total_production : production
    """
    p[0] = grammar.Production(p[1])

def p_production(p):
    """
    production : production symbol
    """
    p[0] = p[1] + [p[2]]

def p_symbols(p):
    """
    production : symbol
    """
    p[0] = [p[1]]

def p_single_symbol_(p):
    """
    symbol : symbolnt
    symbol : symbolont
    symbol : symbolws
    symbol : symbolterm
    """
    p[0] = p[1]

def p_symbolnt(p):
    """
    symbolnt : NT
    """
    p[0] = grammar.Symbol(p[1],grammar.NONTERMINAL)

def p_symbolont(p):
    """
    symbolont : OPTNT OPTWEIGHT
    symbolont : OPTNT
    """
    if len(p) == 3:
        p[0] = grammar.OptSymbol(p[1], grammar.OPTIONAL_NT, p[2])
    else:
        p[0] = grammar.OptSymbol(p[1], grammar.OPTIONAL_NT)

def p_symbolws(p):
    """
    symbolws : WHITESPACE
    """
    p[0] = grammar.Symbol(p[1],grammar.TERMINAL)

def p_symbolterm(p):
    """
    symbolterm : TERMINAL
    """
    p[0] = grammar.Symbol(p[1], grammar.TERMINAL)


def p_error(p):
    raise TypeError ("Unknown text at %r" % (p.value,))

yacc.yacc()
