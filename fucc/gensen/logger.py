
import sys

class Logger:
  def __init__(self, o = None, l = None, p = 1 ):
    self.output   = o
    self.loger    = l
    self.priority = p
    self.indent = 0

  def __isValid(self):
    return self.output and self.loger

  def spit(self, message):
    print >> self.output, message,

  def log(self, priority, message, indent=0):
    if priority <= self.priority:
      if indent < 0:
        self.indent += indent
      print >> self.loger, " "*self.indent + message
      if indent > 0:
        self.indent += indent
  def kill(self):
    if self.__isValid():
      self.output.close()
      self.output.close()
