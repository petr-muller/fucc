"""This file provides a simple output interface for the rest of the module.
It handles logging with priority treshold and various destinations of output"""
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

class Logger:
  """Simple class, which plugs itself to other files and handles their output
  according standard setting"""
  # o/output    - standard output for program
  # l/loger     - place where log should go
  # p/priority  - determines treshold of how serious messages should be logged
  def __init__(self, output = None, logger = None, priority = 1 ):
    self.output   = output
    self.loger    = logger
    self.priority = priority
    self.indent = 0
  
  def _isValid(self):
    """private method, determines if the instance is valid"""
    return self.output and self.loger
  
  def spit(self, message):
    """spits something to output, whatever it is"""
    print >> self.output, message,

  def log(self, priority, message, indent=0):
    """log by priority and indentation"""
    if priority <= self.priority:
      if indent < 0:
        self.indent += indent
      print >> self.loger, " "*self.indent + message
      if indent > 0:
        self.indent += indent

  def kill(self):
    """close all file handlers"""
    if self._isValid():
      self.output.close()
      self.output.close()
