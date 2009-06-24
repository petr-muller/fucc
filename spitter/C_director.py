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
import copy
import sys
import exceptions
import grammar
import md5
import operator

def plugLogger(logger):
  Director.logger = logger
  SemanticUnit.logger = logger

class SymbolStack:
  """Represents a stack"""
  def __init__(self):
    self.stack = []

  def append(self,symbol):
    """Appends symbol to a stack"""
    self.stack.append(symbol)

  def pop(self):
    """Pops symbol from the top of the stack"""
    if len(self.stack) > 0:
      return self.stack.pop()
    else:
      return None
  
  def top(self):
    if len(self.stack) > 0:
      return self.stack[-1]
    else:
      return None

# these two classes are abstract only, used only for inheritance

class SemanticUnit:
  def __init__(self, name, variables=None, identifier=None,lang_type=None,ret_type=None,functions=None,params=None): 
    
    # name sets name of semantic unit
    # name is mandatory
    self.name = name
    message = "Semantic unit: %s" % self.name
    
    self.ret_type = ret_type
    if self.ret_type is None:
      message += ", doesn't have return type"
    elif self.ret_type == False:
      message += ", return type not determined yet"
    else:
      message += ", return type %s" % self.ret_type

    # lang_type determines if this unit limits typeness of variables or constants
    # None  = doesn't care
    # True  = doesn't limit
    # False = limits, but still waits for assignment of type
    self.lang_type = lang_type
    if self.lang_type is None:
      message += ", doesn't care about type."
    elif self.lang_type == False:
      message += ", type not determined yet."
    elif self.lang_type == True:
      message += ", doesn't limit type."
    else:
      message += " of type %s." % lang_type

    # variables holds a list of variables in a scope with their type
    # None = doesn't define it's own scope
    # {}   = no variables yet
    if not variables:
      self.variables = None
      message += " Doesn't hold variables."
    else:
      self.variables = {}
      message += " Can hold variables."
    
    if not functions:
      self.functions = None
      message += " Doesn't hold functions."
    else:
      self.functions = {}
      message += " Can hold functions."
    
    if not params:
      self.params = None
      message += " Doesn't have parameters."
    else:
      self.params = []
      message += " Has parameters."

    # identifier defines a identifier if semantic unit
    # None = doesn't have an identifier
    # ""   = no identifier yet
    if not identifier:
      self.identifier = None
      message += " Doesnt' have identifier."
    else:
      self.identifier = ""
      message += " Has identifier "

    self.log(2, message)

  def __addTypeList(self,type):
    self.variables[type] = []

  def addVar(self,iden,type):
    if not self.variables.has_key(type):
      self.__addTypeList(type)
    self.variables[type].append(iden)

  def addFunc(self,iden,type,params):
    if not self.functions.has_key(type):
      self.functions[type] = []
    self.functions[type].append((iden,params))

  def log(self, priority, message,indent=0):
    if Director.logger is None:
      print >> sys.stderr, message
    else:
      Director.logger.log(priority, message,indent)

class SemanticError(exceptions.Exception):
  "Only a exception class for reporting that production branch failed"
  def __init__(self, message=""):
    pass
  
class Director:
  def __init__(self):
    Director.logger = None
    self.scopest = SymbolStack()
    self.cnt = 0;
    self.nextExpression = None
    self.symbolst = SymbolStack()
    self.expressionDepth = 0
    self.MAXDEPTH=5
    self.MAXFUNCTION=1
    self.EXPRDEPTH=5
    self.functionUsage = {}
    self.type_to_format = { 
        'unsigned char'     : "%hhu",
        'unsigned short'    : "%hu",
        'unsigned int'      : "%u",
        'unsigned long'     : "%lu",
        'unsigned long long': "%llu",
        'signed char'       : "%hhi",
        'signed short'      : "%hi",
        'signed int'        : "%i",
        'signed long'       : "%li",
        'signed long long'  : "%lli",
        'float'            : "%G",
        'double'           : "%G",
        ' char'             : "%hhi",
        ' short'            : "%hi",
        ' int'              : "%i",
        ' long'             : "%li",
        ' long long'        : "%lli"
        }
    self.basic_type_hierarchy = {
        'unsigned char' : 0,
        'signed char' : 0,
        'char' : 0,
        'unsigned short' : 1,
        'signed short' : 1,
        'short' : 1,
        'unsigned int' : 2,
        'signed int' : 2,
        'int' : 2,
        'unsigned long' : 3,
        'signed long' : 3,
        'long' : 3,
        'unsigned long long' : 5,
        'signed long long' : 5,
        'long long' : 5,
        'float' : 6,
        'double' : 7
        }
    self.unitialized_vars = []

  def setMaxDepth(self, depth):
    """Sets maximum number of block repetition"""
    self.MAXDEPTH = depth

  def setMaxFunction(self, calls):
    """Set maximum number of the same function calls"""
    self.MAXFUNCTION = calls

  def setExprDepth(self, depth):
    """Sets treshold from which Director starts to prefer values over expressions"""
    self.EXPRDEPTH = depth

  def counter(self):
    """Counter for block identification"""
    #FIXME: Migrate to Semantic unit
    self.cnt += 1
    return self.cnt

  def log(self, priority, message,indent=0):
    """Log a message, considering priority"""
    if Director.logger is None:
      print >> sys.stderr, message
    else:
      Director.logger.log(priority, message,indent)

  def loadGrammar(self, my_grammar):
    """Loads a grammar from Grammar instance and checks it's sanity"""
    self.grammar = my_grammar
    self.grammar.checkSanity()

  def checkIfNotOverused(self, iden):
    """Check if a function is not called too much"""
    self.functionUsage[iden] = self.functionUsage.get(iden,0) + 1
    if self.functionUsage[iden] > self.MAXFUNCTION:
      return False
    else:
      return True

  def findTypeConstraint(self):
    """Find nearest type constraint"""
    types = [ x.lang_type for x in self.scopest.stack ]
    types.reverse()
    for i in types:
      if i is not None:
        return i

  def addVariableToNearestScope(self,type,name):
    """Adds a variable to nearest SU in a stack, which has a variable scope"""
    for i in range(1,len(self.scopest.stack)+1):
      if self.scopest.stack[-i].variables == None:
        continue
      self.scopest.stack[-i].addVar(name,type)
      self.log(2,"Added variable %s of type %s to scope %s" % (name, type, self.scopest.stack[-i].name))
      return

    raise SemanticError("Haven't found a scope to add a variable. This shouldn't be possible :)")
  
  def addFunctionToNearestScope(self,type,name,params):
    """Adds a function to nearest SU in a scope, which has a function scope"""
    for i in range(1,len(self.scopest.stack)+1):
      if self.scopest.stack[-i].functions == None:
        continue
      self.scopest.stack[-i].addFunc(name,type,params)
      self.log(2,"Added function %s(%s) of type %s to scope %s" % (name, params, type, self.scopest.stack[-i].name))
      return

    raise SemanticError("Haven't found a scope to add a function. This shouldn't be possible :)")
  
  def typeOfVariable(self,variable):
    """Gets type of a variable"""
    for i in range(1,len(self.scopest.stack)+1):
      if self.scopest.stack[-i].variables is not None:
        for type in self.scopest.stack[-i].variables.keys():
          for iden in self.scopest.stack[-i].variables[type]:
            if iden == variable:
              return type

  def getParamType(self, function, param_index):
    """Gets type of parameter param_index of function"""
    for type in self.scopest.stack[0].functions.keys():
      for func_tuple in self.scopest.stack[0].functions[type]:
        if func_tuple[0] == function:
          return func_tuple[1][param_index]

  def propagateType(self, type):
    """If we create a value of some type, try to assign this type to some parent
       SU which has the type still nondetermined"""
    for i in range(2,len(self.scopest.stack)+1):
      if self.scopest.stack[-i].lang_type == False:
        self.scopest.stack[-i].lang_type == type
        break
      if self.scopest.stack[-i].lang_type == True:
        break
      if self.scopest.stack[-i].lang_type == None:
        continue
      if self.scopest.stack[-1].lang_type == type:
        break
      else:
        #FIXME: this is probably bogus. fction param in an expression can have different type
        raise SemanticError("Type mismatch")
    return

  def assignTypeToTop(self, type):
    """Assigns a data type to SU on top of a stack"""
    if self.scopest.top().lang_type == False or self.scopest.top().lang_type == type:
      self.scopest.top().lang_type = type
      self.propagateType(type)
    else:
      raise SemanticError("Attempt to assign type to semantic unit which doesn't accept type")

  def getCurrentReturnType(self):
    """Gets return type of a function inside it's block"""
    #FIXME: not 1 - should be searching through a stack
    return self.scopest.stack[1].ret_type 

  def assignReturnTypeToTop(self, type):
    """Assigns return type to SU on top of a stack"""
    if self.scopest.top().ret_type != None:
      self.scopest.top().ret_type = type
    else:
      raise SemanticError("Attempt to assign type to semantic unit which doesn't accept type")

  def assignIdentifierToTop(self, iden):
    """Assigns indetifier to SU on top of a stack"""
    if self.scopest.top().identifier != None:
      self.scopest.top().identifier = iden
    else:
      raise SemanticError("Attempt to assign identifier to semantic unit which doesn't accept identifier")

  def printfVariablesFromScope(self, scope):
    """Generates a printf command for all variables defined in this scope"""
    exp = ""
    for type in scope.variables.keys():
      for variable in scope.variables[type]:
        #FIXME: Would be nice to have this somewhere defined as data, not code
        exp += '\n  printf("%s: %s\\n", %s);' % (variable, self.type_to_format[type], variable)
    return exp

  def allVariablesList(self):
    """Returns a list of all variables visible in this place"""
    returneth = []
    for i in range(1,len(self.scopest.stack)+1):
      if self.scopest.stack[-i].variables is not None:
        returneth.extend(self.scopest.stack[-i].variables.values())

    return returneth
  
  def getAllVariablesOfType(self,supertype):
    """Returns list of all variables of certain type (or compatible) visible in this place"""
    returneth = []
    for i in range(1, len(self.scopest.stack)+1):
      if self.scopest.stack[-i].variables is not None:
        for type in self.scopest.stack[-i].variables.keys():
          if self.canBe(supertype,type):
            returneth.extend(self.scopest.stack[-i].variables[type])
    return returneth

  def getAllFunctionsOfType(self,supertype):
    """Returns all functions of certain type (or compatible) visible in this place"""
    returneth = []
    for i in range(1, len(self.scopest.stack)+1):
      if self.scopest.stack[-i].functions is not None:
        for type in self.scopest.stack[-i].functions.keys():
          if self.canBe(supertype,type):
            returneth.extend( self.scopest.stack[-i].functions[type])
    return returneth

  def canBe(self,supertype,type):
    """Determines if two types are compatible"""
    if supertype == True or supertype == False or supertype == type:
      return True
    if supertype.strip() not in self.basic_type_hierarchy or type.strip() not in self.basic_type_hierarchy:
      return False
    
    return self.basic_type_hierarchy[type.strip()] <= self.basic_type_hierarchy[supertype.strip()]
  
  def initializeAllToNull(self):
    """Generates a initializing statements for all unitialized variables"""
    line = "";
    for var in self.unitialized_vars:
      line = line + "%s %s = %s;\n" % (var[0], var[1], 1);
    return line;

  def logStackSize(self):
    """Logs a size of stack of semantic units"""
    self.log(1, "Semantic stack size: %s, Top: %s" % (len(self.scopest.stack), self.scopest.top().name))

  def pushSemanticUnit(self, SU):
    """Adds SU to a stack"""
    self.scopest.append(SU)
    self.logStackSize()

  def popSemanticUnit(self):
    """Popds SU from a stack"""
    self.scopest.pop()
    self.logStackSize()

  def getSymbol(self,symbol):
    """This is a method generator calls to get a list of productions for symbol"""
    self.log(2, "Selecting production for symbol <%s>" % symbol)
    # if we generate a constant, we make sure we generate only those of compatible type
    if symbol == "constant":
      candidates = copy.deepcopy(self.grammar.symbols[symbol])
      supertype = self.findTypeConstraint()
      self.log(2, "Constraint found: <%s>" % supertype)
      for production in candidates:
        for symb in production['production'].symbols:
        #FIXME variable symbols
        # do not generate floats in non-float expresions
          if symb.name == 'floating_constant':
            if supertype not in [ 'float', 'double', False ]:
              self.log(2,"Stripped production with floating point constant")
              production['weight'] = 0
            else:
              # if we are in float expression, triple the probability (in float EXPR we want floats
              production['weight'] *= 3
    # if we want some existing value, then we should use variables and fction calls of compatible type
    elif symbol == "existing_value":
      candidates = copy.deepcopy(self.grammar.symbols[symbol])
      supertype = self.findTypeConstraint()
      self.log(2, "Constraint found: <%s>" % supertype)
      possible_variables = self.getAllVariablesOfType(supertype)
      self.log(1, "We could use following variables: %s for type %s" % (possible_variables, supertype))
      possible_functions = self.getAllFunctionsOfType(supertype)
      self.log(1, "We could use following functions: %s for type %s. All functions: %s" % (possible_functions, supertype, self.scopest.stack[0].functions))
      for var in possible_variables:
        self.log(1, "Appending identifier %s to production list")
        # creating production with a variable
        prod = { "production" : grammar.Production([grammar.Symbol(var, grammar.TERMINAL)]), "weight" : 1 }
        candidates.append(prod)
      for var in possible_functions:
        # creating productions with a function call
        # params are represented as nonterminal <param/function/index>
        # when we get a reportStart for such symbol, we create expression with type of index-th parameter of function
        if self.checkIfNotOverused(var[0]):
          self.log(1, "Appending function %s to production list")
          prod = { "production" : grammar.Production([grammar.Symbol(var[0]+'(', grammar.TERMINAL)] +
            reduce(operator.add, 
                   [[ grammar.Symbol('CDIR_param/%s/%s' % (var[0],x), grammar.NONTERMINAL), 
                      grammar.Symbol(', ',grammar.TERMINAL) ] for x in range(len(var[1])) ])[:-1] +
            [ grammar.Symbol(')', grammar.TERMINAL)]), 'weight' : 1 }

          candidates.append(prod)
      candidates[0]['weight'] = len(candidates)
      if self.expressionDepth > self.EXPRDEPTH:
        # prefer constants if we are too deep in an expression
        candidates[0]['weight'] += self.expressionDepth - 5

    elif symbol[:11] == "CDIR_param/":
      # this represents a generator's request for parameter of a function
      # treat as expression
      fction, index = symbol[11:].split('/')
      self.nextExpression = self.getParamType(fction, int(index))
      symbols = [grammar.Symbol('expression', grammar.NONTERMINAL)]
      prod = grammar.Production(symbols)
      candidates = []
      candidates.append({ "production" : prod, "weight" : 1 })
    elif symbol == "assignment":
      # Request for assignment. give some variable for the left side. 
      # If we don't have any, then create declaration instead
      available_variables = self.allVariablesList()
      if len(available_variables) == 0:
        candidates = self.grammar.symbols["ass_to_dec_transition"]
        self.log(2, "No identifiers available here. Generating assigning declaration instead")
      else:
        candidates = self.grammar.symbols[symbol]

    elif self.scopest.top().name == 'Assignment' and symbol == 'identifier':
      available_variables = self.allVariablesList()
      self.log(2, "Identifiers in this scope: %s" % available_variables)
      candidates = []
      for lis in available_variables:
        for identifier in lis:
          a = grammar.Symbol(identifier, grammar.TERMINAL)
          candidates.append({"production" : grammar.Production([a]), 'weight' : 1})

    elif symbol == "expression":
    # expression.
    # at the beginning, prefer expressions over values
    # with increasing depth, start prefering values
      unary_probability = 1
      binary_probability = self.EXPRDEPTH - self.expressionDepth

      if binary_probability < 1:
        unary_probability += 1 - binary_probability
        binary_probability = 1
      candidates = copy.deepcopy(self.grammar.symbols[symbol])
      candidates[0]['weight'] = unary_probability
      candidates[1]['weight'] = binary_probability

    elif symbol == "return":
      # generate a return statement with correct type of return value
      candidates = []
      self.unitialized_vars.append((' int', 'DEPTH_stopper%s' % self.cnt))
      symbols = [grammar.Symbol('DEPTH_stopper%s--;\n' % self.cnt, grammar.TERMINAL),
                 grammar.Symbol('return ', grammar.TERMINAL),
                 grammar.Symbol('expression', grammar.NONTERMINAL),
                 grammar.Symbol(';', grammar.TERMINAL)]
      prod = grammar.Production(symbols)
      candidates = []
      candidates.append({ "production" : prod, "weight" : 1 })
      self.nextExpression = self.getCurrentReturnType()
    
    else:
      candidates = self.grammar.symbols[symbol]
    return candidates

# def __init__(self, name, variables=None, identifier=None,lang_type=None,ret_type=None,functions=None,params=None): 

  def reportStart(self,symbol):
    """Generator gives an echo when starting generating a symbol via this method
       It mainly creates proper SU for symbols which create them"""
    self.log(1, "Starting to generate symbol <%s>" % symbol, 1)
    if symbol == "declaration":
      self.pushSemanticUnit(SemanticUnit("SimpleDeclaration", None, True, False))
    if symbol == "ass_declaration":
      self.pushSemanticUnit(SemanticUnit("AssigningDeclaration", None, True, False))
    if symbol == "program":
      self.pushSemanticUnit(SemanticUnit("Program", True, None, True,None,True))
    if symbol == "mainfunction":
      self.pushSemanticUnit(SemanticUnit("Main", True, None, True))
    if symbol == "expression":
      if self.nextExpression is None:
        type = self.findTypeConstraint()
      else:
        type = self.nextExpression
        self.nextExpression = None

      self.pushSemanticUnit(SemanticUnit("Expression", False, False, type)) 
      self.expressionDepth += 1

    if symbol == "assignment":
      self.pushSemanticUnit(SemanticUnit("Assignment", False, False, False))
    if symbol == "block" or symbol == "augmented_block":
      self.pushSemanticUnit(SemanticUnit("Block", True, None, True))
    if symbol == "function_definition":
      self.pushSemanticUnit(SemanticUnit("Function",True,True,True,False,None,True))
    if symbol == "augmented_function_block":
      self.pushSemanticUnit(SemanticUnit("Block", True, None, True, None, None, None))
      self.scopest.top().variables = self.scopest.stack[-2].variables
      self.scopest.stack[-2].variables = None

    self.symbolst.append(symbol)
  
  def reportFinish(self,symbol,expanded):
    """Generator reports that it finished generation of some symbol via this method
       Director can modify it and return it to generator"""
    if self.scopest.top().name == 'SimpleDeclaration' or self.scopest.top().name == "AssigningDeclaration":
      if symbol == "type":
        self.assignTypeToTop(expanded)
      elif symbol == "identifier":
        self.assignIdentifierToTop(expanded)
      elif symbol == "declaration" or symbol == "ass_declaration":
        decl = self.scopest.pop()
        self.addVariableToNearestScope(decl.lang_type, decl.identifier) 
        self.log(2, "Semantic stack size: %s, Top: %s" % (len(self.scopest.stack), self.scopest.top().name))
      if symbol == "declaration":
        if self.scopest.top().name == "Function":
          self.scopest.top().params.append(decl.lang_type)
        else:
          self.unitialized_vars.append((decl.lang_type, decl.identifier))
    elif self.scopest.top().name == 'Function':
      if symbol == "type" and self.scopest.top().ret_type == False:
        self.assignReturnTypeToTop(expanded)
      elif symbol == "identifier":
        self.assignIdentifierToTop(expanded)
      elif symbol == "function_definition":
        decl = self.scopest.pop()
        self.addFunctionToNearestScope(decl.ret_type, decl.identifier, decl.params)
        self.log(2, "Semantic stack size: %s, Top: %s" % (len(self.scopest.stack), self.scopest.top().name))
    elif self.scopest.top().name == 'Expression':
      if symbol == 'expression':
        self.popSemanticUnit()
        self.expressionDepth -= 1

    elif self.scopest.top().name == 'Main':
      if symbol == "main_epilogue":
        main = self.scopest.top()
        expanded += self.printfVariablesFromScope(self.scopest.top())
      elif symbol == 'global_epilogue':
        self.popSemanticUnit()
        expanded += self.printfVariablesFromScope(self.scopest.top())
        self.log(2, "In scope 'Main': generated epilogue")
    elif self.scopest.top().name == 'Block':
      if symbol  == 'block_epilogue':
        ID = "stopper"+str(self.counter())
        expanded = expanded.replace('ID',ID)
        expanded += self.printfVariablesFromScope(self.scopest.top())
        self.popSemanticUnit()
      elif symbol == 'augmented_block_epilogue':
        ID = "stopper" + str(self.counter())
        self.addVariableToNearestScope(" int", "DEPTH_%s" % ID)
        self.unitialized_vars.append((" int", "DEPTH_%s" % ID))
        expanded = expanded.replace('ID',ID)
        expanded += self.printfVariablesFromScope(self.scopest.top())
        expanded += "if (DEPTH_%s > MAXDEPTH)\nbreak;\nelse\nDEPTH_%s++;" % (ID,ID)
        self.popSemanticUnit()
      elif symbol == 'augmented_function_prologue':
        ID = "stopper" + str(self.counter())
        expanded = expanded.replace('ID',ID)
        self.unitialized_vars.append((" int", "DEPTH_%s" % ID))
        expanded += 'printf("%%i\\n", DEPTH_%s);\n' % ID
        expanded += 'if (DEPTH_%s > MAXDEPTH)\n{\n DEPTH_%s--;\nreturn DEPTH_%s+1;\n}\nelse\nDEPTH_%s++;' % (ID,ID,ID,ID)

    elif self.scopest.top().name == 'Assignment':
      if symbol == 'assignment':
        self.popSemanticUnit()
      elif symbol == 'identifier':
        self.scopest.top().lang_type = self.typeOfVariable(expanded)
    elif symbol == 'program':
      expanded = self.initializeAllToNull() + expanded;
      expanded = ("#define MAXDEPTH %s\n" % self.MAXDEPTH) + expanded

    self.symbolst.pop()
    self.log(1, "Finished generating symbol <%s>: %s" % (symbol,expanded), -1)
    return expanded
