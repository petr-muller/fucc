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

TAG=$1
CHECKTIME=$2

{ 
  $TAG >> $TAG.output 2>&1 &
} >> $TAG.output 2>&1

pid=$!

for i in `seq $CHECKTIME`
do
# check if our pid is still running 
  ps $pid >/dev/null
  if [ "$?" != "0" ]
  then
    echo "TERMINATION: NORMAL" > $TAG.termination
    exit
  fi
  sleep 1
done

kill $pid 2>/dev/null
echo "TERMINATION: KILLED" > $TAG.termination

