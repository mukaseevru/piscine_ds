#!/bin/sh

# Partitioner with argument
awk -F '\",\"|T' 'NR==1 {a=$0; next} {b=$2".csv"} !($2 in c) {c[$2]; print a > b} {print >> b}' "$1"

# Partitioner without argument
#awk -F '\",\"|T' 'NR==1 {a=$0; next} {b=$2".csv"} !($2 in c) {c[$2]; print a > b} {print >> b}' "../ex03/hh_positions.csv"
