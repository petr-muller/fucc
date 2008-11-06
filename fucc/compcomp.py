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

from builder.builder import getConfs
from optparse import OptionParser
import os
import settings
import sys
import tempfile

TAG_NOT_FOUND = """Conf tag %s not provided in builder settings
Please check your builder/settings file"""

def dbug(msg):
  global DEBUG
  if DEBUG:
    print "ADEBUG: %s" % msg

def cleanDirectory(dirname):
  for root, dirs, files in os.walk(dirname, topdown=False):
    for name in files:
      os.remove(os.path.join(root, name))
    for name in dirs:
      os.rmdir(os.path.join(root, name))

class OptError(Exception):
  def __init__(self, msg):
    self.msg = msg
  def __str__(self):
    return self.msg

if __name__ == "__main__":
  usage = "usage: %prog -i COUNT -g GOLDEN <TAG1> [TAG2]....[TAGn]"
  options = OptionParser(usage, version="%prog version 0.1")

  options.add_option("-i", "--iterations", dest="iterations", metavar="COUNT",
                      help="Do COUNT iterations")
  options.add_option("-g", "--golden", dest="golden", metavar="TAG",
                      help="TAG is treated as golden run (we trust it more)")
  options.add_option("-X", dest="debug", action="store_true", default=False,
                      help="Switch on the debugging output")
  
  (options, args) = options.parse_args()
  global DEBUG
  DEBUG = options.debug
  
  try:
    if not options.iterations:
      raise OptError("Iterations have to be provided")  
    try:
      iterations = int(options.iterations)
    except ValueError:
      raise OptError("Iterations have to be a number")

    if not options.golden:
      raise OptError("GOLDEN has to be specified")

    if len(args) < 1:
      raise OptError("You have to provide at least one other conf tag")

    configs = getConfs().keys()
    if options.golden not in configs:
      raise OptError(TAG_NOT_FOUND % options.golden)

    for tag in args:
      if tag not in configs:
        raise OptError(TAG_NOT_FOUND % options.golden)
  except OptError, (instance):
    print >> sys.stderr, instance.msg
    sys.exit(1)
  
  dbug("Iterations:         %s" % iterations)
  dbug("Golden run:         %s" % options.golden)
  dbug("Processed tags:     %s" % args)

  test_dir = tempfile.mkdtemp()
  res_dir = tempfile.mkdtemp()
  dbug("Testing dir:        %s" % test_dir)
  dbug("Results dir:        %s" % res_dir)

  metrics = {}

  for run in xrange(iterations):
    run +=1
    cleanDirectory(test_dir)
    testfile = settings.TESTFILE_TEMPLATE % run
    
    GENERATOR=settings.GENERATOR
    GENERATOR="%s>%s/%s" % (GENERATOR,test_dir,testfile)
    dbug("Generator command:\n'%s'" % GENERATOR)
    print ("\r" + ( "Testcase (%s/%s)" % (run, iterations)).ljust(20) + "GENERATING".ljust(15)),
    sys.stdout.flush()
    os.system(GENERATOR)

    BUILDER="builder/builder.py --testcase %s --directory %s --ttl 5 %s %s" % (testfile, test_dir, options.golden, " ".join(args))
    dbug("Builder command:\n'%s'" % BUILDER)
    print ("\r" + ("Testcase (%s/%s)" % (run, iterations)).ljust(20) + "BUILDING".ljust(15)),
    sys.stdout.flush()
    sys.stdout.flush()
    os.system(BUILDER)

    COMPARE="comparator/compare.sh %s %s %s" % (test_dir, options.golden, " ".join(args))
    dbug("Compare command:\n'%s'" % COMPARE)
    print ("\r" + ("Testcase (%s/%s)" % (run, iterations)).ljust(20) + "COMPARING".ljust(15)),
    sys.stdout.flush()
    sys.stdout.flush()
    rc = os.system(COMPARE) / 256

    result = settings.RESULTS[rc]
    print ("\r" + ("Testcase (%s/%s)" % (run, iterations)).ljust(20) + result.ljust(15))
    sys.stdout.flush()
    if settings.STORE[result]:
      os.system("%s %s %s %s '%s'" % (settings.STORE_COMMAND, run, test_dir, res_dir, result ))

    if not metrics.has_key(result):
      metrics[result] = 0

    metrics[result] += 1

print "*" * 60
for res in metrics.keys():
  print (res+": ").ljust(30) + str(metrics[res])
print "*" * 60
print "Your results are here: %s" % res_dir


