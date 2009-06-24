#!/bin/sh


RUN=$1
SRCDIR=$2
RESDIR=$3
RESULT=$4

if [ ! -d "$RESDIR/$RESULT" ]
then
  mkdir -p "$RESDIR/$RESULT"
fi

mkdir "$RESDIR/$RESULT/$RUN"

cp $SRCDIR/* "$RESDIR/$RESULT/$RUN"


