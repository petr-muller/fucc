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

TESTCASE_DIRECTORY="$1"
shift
GOLDEN="$1"
shift
REST="$@"

res=0

for testcase in $REST
do
 if ! diff $TESTCASE_DIRECTORY/$GOLDEN.buildresult $TESTCASE_DIRECTORY/$testcase.buildresult > $TESTCASE_DIRECTORY/$GOLDEN-$testcase-build.diff 
 then
   res=2
 elif [ "`cat $TESTCASE_DIRECTORY/$GOLDEN.buildresult`" != "Successful compilation" ]
 then
   res=4
 elif ! diff $TESTCASE_DIRECTORY/$GOLDEN.termination $TESTCASE_DIRECTORY/$testcase.termination > $TESTCASE_DIRECTORY/$GOLDEN-$testcase-termination.diff || [ "`cat $TESTCASE_DIRECTORY/$GOLDEN.termination`" != "TERMINATION: NORMAL" ]
 then
   res=3
 elif ! diff $TESTCASE_DIRECTORY/$GOLDEN.output $TESTCASE_DIRECTORY/$testcase.output > $TESTCASE_DIRECTORY/$GOLDEN-$testcase-runtime.diff
 then
   SIG8="`cat $TESTCASE_DIRECTORY/*.output | grep "signal number 8" | wc -l`" 
   if [ "$SIG8" != "0" ]
   then
     res=5
   else
     res=1
   fi
 fi
done

exit $res
