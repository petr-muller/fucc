#!/bin/sh
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


FILES = {
        'BUILD-RESULT'  : 'build-result',
        'BUILD-OUTPUT'  : 'build-output',
        'RUN-RESULT'    : 'run-result',
        'RUN-OUTPUT'    : 'run-output',
        }

ACTIONS = (
    { "name" : "golden-build-failed", 
      "cond" : "GOLDEN BUILD-RESULT CONTAINS Failure" },
    { "name" : "build-different",
      "cond" : "BUILD-RESULT DIFFER" },
    { "name" : "golden-run-killed",
      "cond" : "GOLDEN RUN-RESULT CONTAINS Killed" },
    { "name" : "retcode-different",
      "cond" : "RUN-RESULT DIFFER" },
    { "name" : "output-different",
      "cond" : "RUN-OUTPUT DIFFER" }
    )
# BUILD DIFFERS (bug in either compiler)
# GOLDEN BUILD FAILED (bug in Generator)
# GOLDEN WAS KILLED (we dont care)
# TESTED WAS KILLED (effectivity)
# ZERO KILLED (we dont care)
# RETCODE DIFFERENT (bug)
# OUTPUT DIFFER (bug)
