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
COUNT=$1
shift
GOLDEN_TAG="$1"
shift

TESTCASE_NUMBER=0
TESTCASE_DIRECTORY=testcase
RESULTS_DIRECTORY=results
FCDIR=$RESULTS_DIRECTORY/Different-Compilations
FRDIR=$RESULTS_DIRECTORY/Different-Outputs
FTDIR=$RESULTS_DIRECTORY/Different-Termination
CFDIR=$RESULTS_DIRECTORY/Failed-Compilations
S8DIR=$RESULTS_DIRECTORY/Zero-Division

rm -rf $RESULTS_DIRECTORY
mkdir -p $FCDIR
mkdir -p $FRDIR
mkdir -p $FTDIR
mkdir -p $CFDIR
mkdir -p $S8DIR

OK=0
FC=0
FR=0
FT=0
CF=0
S8=0


for run in `seq $COUNT`
do  
  rm -f $TESTCASE_DIRECTORY/*
  GRAMMAR_FILE=spitter/grammars/c_grammar_modified.g

  GENERATOR="spitter/main.py -g $GRAMMAR_FILE >$TESTCASE_DIRECTORY/tc$TESTCASE_NUMBER.c"

  BUILDER=builder/builder.py

  COMPARATOR=comparator/compare.sh
  echo -ne "GENERATING TESTCASE    $run/$COUNT\r"
  eval $GENERATOR

  echo -ne "BUILDING TESTCASE      $run/$COUNT\r"
  $BUILDER --testcase tc$TESTCASE_NUMBER.c --directory testcase --ttl 5 $GOLDEN_TAG $1

  echo -ne "COMPARING              $run/$COUNT\r"
  $COMPARATOR testcase $GOLDEN_TAG $@
  res=$?

  echo -ne "TESTING TESTCASE       $run/$COUNT\r"

  if [ "$res" == "0" ]
  then
    OK=$(($OK+1))
  elif [ "$res" == "1" ]
  then
    FR=$((FR+1))
    tar cfz $FRDIR/$TESTCASE_NUMBER.tar.gz testcase/*
    echo -e "\n=============================== $TESTCASE_NUMBER =============================\n" >> $FRDIR/report
    for file in testcase/*.output
    do
      echo "\n=============== $file ===============\n" >> $FRDIR/report
      cat $file >> $FRDIR/report
    done
    echo "================ DIFF ===============" >> $FRDIR/report
    cat testcase/*runtime.diff >> $FRDIR/report

  elif [ "$res" == "3" ]
  then
    FT=$((FT+1))
    tar cfz $FTDIR/$TESTCASE_NUMBER.tar.gz testcase/*
    echo -e "\n=============================== $TESTCASE_NUMBER ==============================\n" >> $FTDIR/report
    for file in testcase/*.termination
    do
      echo "=============== $file ===============" >> $FTDIR/report
      cat $file >> $FTDIR/report
    done
    echo "=============== DIFF ===============" >> $FTDIR/report
    cat testcase/*termination.diff >> $FTDIR/report
  elif [ "$res" == "4" ]
  then
    CF=$((CF+1))
    tar cfz $CFDIR/$TESTCASE_NUMBER.tar.gz testcase/*
    echo -e "\n=============================== $TESTCASE_NUMBER ==============================\n" >> $CFDIR/report
    for file in testcase/*.build
    do
      echo "=============== $file ===============" >> $CFDIR/report
      cat $file >> $CFDIR/report
    done
    echo "=============== DIFF ===============" >> $CFDIR/report
    cat testcase/*build.diff >> $CFDIR/report
  elif [ "$res" == "5" ]
  then
    S8=$((S8+1))
    tar cfz $S8DIR/$TESTCASE_NUMBER.tar.gz testcase/*
    echo -e "\n=============================== $TESTCASE_NUMBER ==============================\n" >> $S8DIR/report
    for file in testcase/*.output
    do
      echo "=============== $file ===============" >> $S8DIR/report
      cat $file >> $S8DIR/report
    done
    echo "=============== DIFF ===============" >> $S8DIR/report
    cat testcase/*runtime.diff >> $S8DIR/report
    
  else
    FC=$((FC+1))
    tar cfz $FCDIR/$TESTCASE_NUMBER.tar.gz testcase/*
    echo -e "\n=============================== $TESTCASE_NUMBER ==============================\n" >> $FCDIR/report
    for file in testcase/*.build
    do
      echo "=============== $file ================" >> $FCDIR/report
      cat $file >> $FCDIR/report
    done
    echo "================= DIFF ================" >> $FCDIR/report
    cat testcase/*build.diff >> $FCDIR/report
  fi

  TESTCASE_NUMBER=$(($TESTCASE_NUMBER+1))
done
killall $GOLDEN_TAG $@ >/dev/null 2>&1

echo "=================================================================="
echo "= FINISHED TESTCASES      : $TESTCASE_NUMBER"
echo "= GOOD                    : $OK"
echo "= FAILED COMPILATIONS     : $CF"
echo "= COMPILATION ANOMALIES   : $FC"
echo "= TERMINATION ANOMALIES   : $FT"
echo "= RUNTIME ANOMALIES       : $FR"
echo "= ZERO DIVISON            : $S8"
