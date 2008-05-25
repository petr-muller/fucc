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

def getConfs(sfile ):
  settings = open(sfile)
  lines = settings.readlines()
  settings.close()
  
  configs = {}
  for line in lines:
    if len(line) > 1 and line[0] != '#':
      tag, config = line.split(':')
      configs[tag.strip()] = config.strip()
  return configs


if __name__ == "__main__":
  import sys
  import os
  from optparse import OptionParser

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

  actpath=os.path.abspath(os.path.dirname(sys.argv[0]))

  configs = getConfs(actpath+"/settings")

  for tag in TAGS:
    command = configs[tag]
    #replace the placeholders with source/directory
    command = command.replace("SOURCE", case_dir+'/'+testcase)
    command = command.replace("OUTPUT", case_dir+'/'+tag)

    #build & log the binary
    whole_command = "%s > %s/%s.build 2>&1" % (command, case_dir,tag)
    built = os.system(whole_command)

    build_result = open("%s/%s.buildresult" % (case_dir,tag),'w')

    #if there was a successful build, run the binary inside a timer
    if built == 0:
      print >> build_result, "Successful compilation"
      command = '%s/timer.sh %s/%s %s' % (actpath, case_dir,tag, int(options.ttl))
      os.system(command)
    else:
      print >> build_result, "Unsuccessful compilation"

    build_result.close()
