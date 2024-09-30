#!bin/bash

grep -e "#" input.txt | sort -du > output.txt
