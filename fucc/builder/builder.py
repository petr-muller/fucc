#!/usr/bin/env python 
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

from os import path,kill
from signal import SIGTERM
from time import sleep
import settings
import subprocess

global DEBUG

def dbug(msg):
  global DEBUG
  if DEBUG:
    print "DEBUG: %s" % msg
    
# a subclass which allows to be killed.
# this is not portable on Windows, so if anyone will ever use this here, this
# will have to be rewritten
class KillablePopen(subprocess.Popen):
  def kill(self, signal=SIGTERM):
    dbug ("Killing")
    kill(self.pid, signal)


def runCommand(command, case_dir, name, timeout=None):  
  outputfile=open(path.join(case_dir,name+"-%s" % settings.OUTPUT_SUFFIX), 'w')
  resultfile=open(path.join(case_dir,name+"-%s" % settings.RESULT_SUFFIX), 'w')
  process = KillablePopen(command, stdout=outputfile, stderr=outputfile)
  still_time = True
  timer = 0  
  dbug(command)
  
  while (process.poll() is None) and (still_time):
    if (timeout is not None) and timer >= timeout:
      still_time=False       
    sleep(1)
    timer+=1
  
  if not still_time:
    resultfile.write(settings.TIMEOUT_MSG)
    process.kill()
    retcode = False
  else:
    RC = process.poll()
    if RC == 0:
      resultfile.write(settings.RETCODE0_MSG)
      retcode = True
    else:
      resultfile.write("%s" % (settings.RETCODE_NOT0_MSG) )
      retcode = False
  
  resultfile.close()
  outputfile.close()

  return retcode

def getConfs():
  configs = {}
  for tag in settings.TAGS:
    configs[tag['name']] = tag['command']  
  return configs

if __name__ == "__main__":
  import sys
  import os
  from optparse import OptionParser

  DEBUG=False
  parser = OptionParser()

  parser.add_option("-t", "--testcase", dest="testcase", default="",
                      help="testcase to process", metavar="FILE")
  parser.add_option("-d", "--directory", dest="directory", default="",
                      help="directory where to build", metavar="DIRECOTRY")
  parser.add_option("-l", "--ttl", dest="ttl", default=5,
                      help="seconds limit for one binary to run", metavar="DIRECOTRY")

  (options, args) = parser.parse_args()

  if options.testcase == "":
    print "Testcase needs to be provided"
    sys.exit(1)
  else:
    testcase = options.testcase

  if options.directory == "":
    print "Working directory is a mandatory argument"
    sys.exit(1)
  else:
    case_dir = options.directory

  TAGS=args
  if len(TAGS) != 2:
    print "Bad number of compilation tags"
    sys.exit(1)

  configs = getConfs()

  for tag in TAGS:
    command = configs[tag]
    #replace the placeholders with source/directory
    command = command.replace("SOURCE", path.join(case_dir,testcase))
    command = command.replace("OUTPUT", path.join(case_dir,tag))
    
    for action in settings.ACTIONS:
      if action == "BUILD":
        if not runCommand(command.split(' '), case_dir, '%s-build' % tag, 10):
          break
      elif action == "RUN":
        runCommand('%s/%s' % (case_dir, tag), case_dir, '%s-run' % tag, options.ttl)
      elif action in settings.ADDITIONAL.keys():
        cmd = settings.ADDITIONAL[action]
        cmd = cmd.replace("SOURCE", path.join(case_dir,testcase))
        cmd = cmd.replace("OUTPUT", path.join(case_dir,tag))
        cmd = cmd.split(' ')
        runCommand(cmd, case_dir, "%s-%s" % (tag,action), 10)
