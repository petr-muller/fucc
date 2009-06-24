"""This file implements a inner representation of grammar rules. All elements
have their own class"""
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
import sys

DEFAULT_OPTIONAL_NT_WEIGHT  = 0.5
NONTERMINAL                 = 'NON-TERM'
OPTIONAL_NT                 = 'OPT-NONT'
TERMINAL                    = 'TERMINAL'
LOGGER                      = None
def plugLogger(logger):
  """Plugs this module into an instance of a logger"""
  global LOGGER
  LOGGER = logger

def log(priority, message):
  """Logs to a logger, honoring priority. If no logger, then log to stdout"""
  if LOGGER is None:
    print >> sys.stderr, message
  else:
    LOGGER.log(priority, message)

class Symbol():
  """Class representing one symbol"""
  def __init__(self, symbol, symbol_type):
    self.name = symbol
    self.type = symbol_type
  def __str__(self):
    if self.type == NONTERMINAL:
      return "<%s>" % self.name
    else:
      return self.name

class OptSymbol(Symbol):
  """Class representing one symbol with probability configuration"""
  def __init__(self, symbol, symbol_type, weight=DEFAULT_OPTIONAL_NT_WEIGHT):
    Symbol.__init__(self, symbol, symbol_type)
    self.weight = weight
  def __str__(self):
    return "<[%s]>{%s}" % (self.name, self.weight)

class Production():
  """Class representing one possible production = sequence of symbols"""
  def __init__(self, symbol_list):
    self.symbols = symbol_list
  def __str__(self):
    return "".join([str(sym) for sym in self.symbols])

class Rule():
  """Represents one rule = name and a list of possible productions"""
  def __init__(self, symbol, productions, weights):
    self.name = symbol
    self.productions = []
    for cnt in range(0, len(productions)):
      try:
        self.productions.append({ "production" : productions[cnt],
                                  "weight" : weights[cnt]})
      except IndexError:
        self.productions.append({"production" : productions[cnt], "weight" : 1})

  def __str__(self):
    msg = "Syntactic rule: <" + self.name + "> ::= "
    ind = len("Syntactic rule: <" + self.name + "> ::")

    for i in self.productions:
      msg += str(i["production"]) +\
             " (weight %s)\n%s| " % (i["weight"], ind*" ")
    msg = msg[:-(ind+3)] + ';;;'
    return msg

class Grammar():
  """Represents whole grammar = a dictionary of rules"""
  def __init__(self, rules):
    self.symbols = {}
    self.symbol_names = []
    for rule in rules:
      self.symbols[rule.name] = rule.productions
      self.symbol_names.append(rule.name)

  def checkSanity(self):
    """Check if all nonterminal in productions have a rule for generating"""
    for rule in self.symbol_names:
      for production in self.symbols[rule]:
        for symbol in production["production"].symbols:
          if symbol.type == NONTERMINAL or symbol.type == OPTIONAL_NT:
            if symbol.name not in self.symbol_names:
              msg = "Error: no expansion for nonterminal %s, rule for %s"
              log(0, msg % (symbol.name, rule))


  def __str__(self):
    return "Grammar containing %s rules" % len(self.symbol_names)
