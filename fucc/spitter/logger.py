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

class Logger:
  # o/output    - standard output for program
  # l/loger     - place where log should go
  # p/priority  - determines treshold of how serious messages should be logged
  def __init__(self, o = None, l = None, p = 1 ):
    self.output   = o
    self.loger    = l
    self.priority = p
    self.indent = 0
  
  # private method, determines if the instance is valid
  def _isValid(self):
    return self.output and self.loger
  
  # spits something to output, whatever it is
  def spit(self, message):
    print >> self.output, message,

  # log by priority and indentation
  def log(self, priority, message, indent=0):
    if priority <= self.priority:
      if indent < 0:
        self.indent += indent
      print >> self.loger, " "*self.indent + message
      if indent > 0:
        self.indent += indent

  # close all file handlers
  def kill(self):
    if self._isValid():
      self.output.close()
      self.output.close()
