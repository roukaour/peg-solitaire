#!/bin/bash

echo Testing performance > perf.txt

for board in boards/g*.txt; do
	if [[ $board == *gcentral.txt ]]; then
		continue
	fi
	echo $board >> perf.txt
	python pegSolitaire.py --input $board --flag 2 >> perf.txt
	python pegSolitaire.py --input $board --flag 3 >> perf.txt
	python pegSolitaire.py --input $board --flag 4 >> perf.txt
	python pegSolitaire.py --input $board --flag 5 >> perf.txt
done
