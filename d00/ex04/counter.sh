#!/bin/sh
# Counter without argument
echo '"name","count"' > hh_uniq_positions.csv
tail -n +2 "../ex03/hh_positions.csv" | cut -f 3 -d ',' | sort | uniq -ci | while read -r line ; do words=($line); echo "${words[1]}","${words[0]}" >> hh_uniq_positions.csv ; done

# Counter with argument
#if [ "$1" ] ; then
#echo '"name","count"' > hh_uniq_positions.csv
#tail -n +2 "$1" | cut -f 3 -d ',' | sort | uniq -ci | while read -r line ; do words=($line); echo \""${words[1]}"\","${words[0]}" >> hh_uniq_positions.csv ; done
#else
#  echo "Usage: ./counter.sh '../ex03/hh_positions.csv'"
#fi