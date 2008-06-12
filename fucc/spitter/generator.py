"""This module contains a generator, which uses EBNF as an input and produces
random sentences as defined by that EBNF"""
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
import random
import grammar
import exceptions
import copy
import sys

LOGGER = None

def plugLogger(logger):
  """Plugs this module into an instance of a logger"""
  global LOGGER
  LOGGER = logger

def log(priority, message, indent=0):
  """Logs to a logger, honoring priority. If no logger, then log to stdout"""
  if LOGGER is None:
    print >> sys.stderr, message
  else:
    LOGGER.log(priority, message, indent)

def spit(message):
  "Spits output. Uses Logger if possible"
  if LOGGER is None:
    print >> sys.stdout, message
  else:
    LOGGER.spit(message)

class ProductionNotPossible(exceptions.Exception):
  "Only a exception class for reporting that production branch failed"
  def __init__(self, msg):
    Exception.__init__(self)
    self.msg = msg
  def __str__(self):
    return self.msg

class Generator:
  "Generator class. Randomly generates sentences defined by a language grammar"
  def __init__(self):
    "Constructor does fairly nothing"
    self.director = None
  
  def plugDirector(self, director):
    "Plug for Director instance"
    self.director = director

  def _select_production(self, productions):
    """Internal method which chooses one production from the list.
       It honors weights"""
    wtotal = sum([x['weight'] for x in productions])
    roll = random.uniform(0, wtotal)
    log(2, "Random choice: roll %s out of %s" % (roll, wtotal))
    # it may happen all productions have weight of 0. Return None then.
    if wtotal == 0:
      return None
    # select which production belongs to random number n
    selected = None
    for prod in productions:
      selected = prod
      if roll <= prod['weight']:
        break
      roll = roll-prod['weight']

    return selected


  def generate(self, symbol):
    """Method for actually generate the sentence."""\
    """"Can backtrack if subbranch fails to generate"""
    # obtain a list of weighted productions
    self.director.reportStart(symbol)
    productions = self.director.getSymbol(symbol)
    success = False

    # while we are not successful, try to generate some production from the list
    while not success:
      # it may happen they are no productions. return None then
      try:
        message = "No valid productions left for symbol <%s>" % symbol
        if len(productions) == 0:
          raise ProductionNotPossible(message)
        success = True
        selected = self._select_production(productions)
        if selected is None:        
          raise ProductionNotPossible(message)
      except ProductionNotPossible, (exc_instance):
        log(2, exc_instance.msg)
        self.director.reportFailure(symbol)
        return None

      try:
        symbol_buffer = []
        # now try to generate all symbols from the production
        for symb in selected['production'].symbols:
          if symb.type == grammar.NONTERMINAL:
            
            # nonterminal - try to generate, raise exception if fails
            symbol_buffer.append(self.generate(symb.name))
            if symbol_buffer[-1] == None:
              raise ProductionNotPossible
          elif symb.type == grammar.OPTIONAL_NT and symb.weight <= 1.0:
            if symb.weight >= random.uniform(0, 1):
              # optional nonterminal - try to generate, omit if fails
              symbol_buffer.append(self.generate(symb.name))
              if symbol_buffer[-1] == None:
                log(2, "Production of optional symbol <%s> not possible, \
omitting" % symb)
                del symbol_buffer[-1]
            else:
              log(1, "Not generating optional symbol")
          elif symb.type not in (grammar.OPTIONAL_NT, grammar.NONTERMINAL):
            # terminals - print
            symbol_buffer.append(symb.name)
            log(2, "Writing nonterminal")
          else:
            # if something weird happens, then report it
            log(1, "Warning: there is some possible error in rules \
for symbol <%s>" % symbol)

      # if some branch failed to generate, try to select another production
      # and try to generate it instead
      except ProductionNotPossible:
        ind = productions.index(selected) 
        log(2, "Production at index %s for symbol <%s> not possible, \
omitting and backtracking" % (ind,symbol))
        success = False

        # we have to deepcopy production
        # we dont want to erase the production from the master grammar
        productions = copy.deepcopy(productions)
        del productions[ind]

    tmp = "".join(symbol_buffer)
    return self.director.reportFinish(symbol, tmp)
