#!/bin/sh

# Convert json to csv without argument
jq -rf filter.jq "../ex00/hh.json" > hh.csv

# Convert json to csv with argument
#jq -rf filter.jq "$1" > hh.csv