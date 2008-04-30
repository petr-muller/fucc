
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
