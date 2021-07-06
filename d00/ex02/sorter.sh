#!/bin/sh

# Sorting without argument
head -n 1 "../ex01/hh.csv" > "hh_sorted.csv"
tail -n +2 "../ex01/hh.csv" | sort -t "," -k 2 -k 1n >> "hh_sorted.csv"

# Sorting with argument
#cat < "$1" | head -n 1; cat < "$1" | tail -n +2 | sort -t "," -k 2 -k 1n > hh_sorted.csv
