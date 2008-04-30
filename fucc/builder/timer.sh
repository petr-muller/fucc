#!/bin/sh

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

