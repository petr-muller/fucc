
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

def plugLogger(logger):
  "Just plugs the logger class here"
  Generator.logger = logger

class ProductionNotPossible(exceptions.Exception):
  "Only a exception class for reporting that production branch failed"
  def __init__(self, message=""):
    pass

class Generator:
  "Generator class. Randomly generates sentences defined by a language grammar"
  def __init__(self):
    "Constructor does fairly nothing"
    Generator.logger = None
    self.director = None
  
  def plugDirector(self,director):
    "Plug for Director instance"
    self.director = director

  def log(self, priority, message, indent=0):
    "Logging method. Uses Logger if possible"
    if Generator.logger is None:
      print >> sys.stderr, message
    else:
      Generator.logger.log(priority, message,indent)
  
  def spit(self, message):
    "Spits output. Uses Logger if possible"
    if Generator.logger is None:
      print >> sys.stdout, message
    else:
      Generator.logger.spit(message)

  def generate(self,symbol):
    "Method for actually generate the sentence.Can backtrack if subbranch fails to generate"
    # obtain a list of weighted productions
    self.director.reportStart(symbol)
    productions = self.director.getSymbol(symbol)
    success = False

    # while we are not successful, try to generate some production from the list
    while not success:
      # it may happen they are no productions. return None then
      if len(productions) == 0:
        self.log(2, "No valid productions left for symbol <%s>" % symbol)
        self.director.reportFailure(symbol)
        return None

      success = True
      # select one production from the list and honor weights
      wtotal = sum([x['weight'] for x in productions])
      n = random.uniform(0, wtotal)
      self.log(2, "Random choice: roll %s out of %s" % (n, wtotal))
      # it may happen all productions have weight of 0. Return None then.
      if wtotal == 0:
        self.log(2, "No valid producitons left for symbol <%s>" % symbol)
        self.director.reportFailure(symbol)
        return None
      # select which production belongs to random number n
      for prod in productions:
        if n <= prod['weight']:
          break
        n = n-prod['weight']

      try:
        buffer = []
        # now try to generate all symbols from the production
        for symb in prod['production'].symbols:
          if symb.type == grammar.NONTERMINAL:
            # nonterminal - try to generate, raise exception if fails
            buffer.append(self.generate(symb.name))
            if buffer[-1] == None:
              raise ProductionNotPossible
          elif symb.type == grammar.OPTIONAL_NT and symb.weight <= 1.0:
            if symb.weight >= random.uniform(0,1):
              # optional nonterminal - try to generate, omit if fails
              buffer.append(self.generate(symb.name))
              if buffer[-1] == None:
                self.log(2, "Production of optional symbol <%s> not possible, omitting" % symb)
                del buffer[-1]
            else:
              self.log(1, "Not generating optional symbol")
          elif symb.type not in (grammar.OPTIONAL_NT, grammar.NONTERMINAL):
            # terminals - print
            buffer.append(symb.name)
            self.log(2, "Writing nonterminal")
          else:
            # if something weird happens, then report it
            self.log(1, "Warning: there is some possible error in rules for symbol <%s>" % symbol)

      # if some branch failed to generate, try to select another production and generate it
      except ProductionNotPossible:
        a = productions.index(prod) 
        self.log(2, "Production at index %s for symbol <%s> not possible, omitting and backtracking" % (a,symbol))
        success = False

        # we have to deepcopy production, as we dont want to erase the production from the master grammar
        productions = copy.deepcopy(productions)
        del productions[a]

    tmp = "".join(buffer)
    return self.director.reportFinish(symbol,tmp)
