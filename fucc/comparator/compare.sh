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
 if ! diff -u $TESTCASE_DIRECTORY/$GOLDEN-build-result $TESTCASE_DIRECTORY/$testcase-build-result > $TESTCASE_DIRECTORY/$GOLDEN-$testcase-build.diff 
 then
   res=2
 elif [ "`cat $TESTCASE_DIRECTORY/$GOLDEN-build-result`" != "Success" ]
 then
   res=4
 elif ! diff -u $TESTCASE_DIRECTORY/$GOLDEN-run-result $TESTCASE_DIRECTORY/$testcase-run-result > $TESTCASE_DIRECTORY/$GOLDEN-$testcase-termination.diff || [ "`cat $TESTCASE_DIRECTORY/$GOLDEN-run-result`" == "Killed" ]
 then
   res=3
 elif ! diff -u $TESTCASE_DIRECTORY/$GOLDEN-run-output $TESTCASE_DIRECTORY/$testcase-run-output > $TESTCASE_DIRECTORY/$GOLDEN-$testcase-runtime.diff
 then
   SIG8="`cat $TESTCASE_DIRECTORY/*-run-output | grep "signal number 8" | wc -l`" 
   if [ "$SIG8" != "0" ]
   then
     res=5
   else
     res=1
   fi
 fi
done

exit $res
