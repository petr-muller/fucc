DEFAULT_OPTIONAL_NT_WEIGHT  = 0.5
NONTERMINAL                 = 'NON-TERM'
OPTIONAL_NT                 = 'OPT-NONT'
TERMINAL                    = 'TERMINAL'

def plugLogger(logger):
  Element.logger = logger

class Element:
  def __init__(self):
    Element.logger = None
  def log(self, priority, message):
    if Element.logger == None:
      print >> sys.stderr, message
    else:
      Element.logger.log(priority, message)

class Symbol(Element):
    def __init__(self,symbol,type):
        self.name = symbol
        self.type = type
    def __str__(self):
        if self.type == NONTERMINAL:
            return "<%s>" % self.name
        else:
            return self.name

class OptSymbol(Symbol):
    def __init__(self,symbol,type,weight=DEFAULT_OPTIONAL_NT_WEIGHT):
        Symbol.__init__(self,symbol,type)
        self.weight = weight
    def __str__(self):
        return "<[%s]>{%s}" % (self.name, self.weight)

class Production(Element):
    def __init__(self,symbol_list):
        self.symbols = symbol_list
    def __str__(self):
        return "".join([str(sym) for sym in self.symbols])

class Rule(Element):
    def __init__(self,symbol,productions,weights):
        self.name = symbol
        self.productions = []
        for cnt in range(0,len(productions)):
            try:
                self.productions.append({"production" : productions[cnt], "weight" : weights[cnt]})
            except IndexError:
                self.productions.append({"production" : productions[cnt], "weight" : 1})
    def __str__(self):
        a = "Syntactic rule: <" + self.name + "> ::= "
        ind = len("Syntactic rule: <" + self.name + "> ::")

        for i in self.productions:

            a += str(i["production"]) + " (weight %s)" % (i["weight"]) + "\n" + ind*" " + '| '
        a = a[:-(ind+3)] + ';;;'
        return a

class Grammar(Element):
    def __init__(self,rules):
      self.symbols = {}
      self.symbol_names = []
      for rule in rules:
        self.symbols[rule.name] = rule.productions
        self.symbol_names.append(rule.name)

    def checkSanity(self):
      for rule in self.symbol_names:
        for production in self.symbols[rule]:
          for symbol in production["production"].symbols:
            if symbol.type == NONTERMINAL or symbol.type == OPTIONAL_NT:
              if symbol.name not in self.symbol_names:
                self.log(0,"Error: there's no expansion for nonterminal %s in rule for %s" % (symbol.name, rule))


    def __str__(self):
        return "Grammar containing %s rules" % len(self.symbol_names)
