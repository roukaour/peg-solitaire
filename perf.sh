#!/bin/bash

OUTFILE="perf.txt"

echo Testing performance > $OUTFILE

for board in boards/g*.txt; do
	# gcentral.txt would take too long for IDDFS, so test it manually
	if [[ $board == *gcentral.txt ]]; then continue; fi
	echo $board >> $OUTFILE
	echo $(fgrep -o X $board | wc -l) pegs >> $OUTFILE
	python pegSolitaire.py --input $board --flag 0 >> $OUTFILE
done
