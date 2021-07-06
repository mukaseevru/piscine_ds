#!/bin/sh

# Grab hh.ru with argument
if [ $# -eq 1 ]; then
	curl -k "https://api.hh.ru/vacancies?text=${1// /%20}&page=0&per_page=20" | jq '.' > hh.json
else
	echo "Usage: ./hh.sh 'data scientist'"
fi

# Grab hh.ru without argument
#curl -k "https://api.hh.ru/vacancies?text=data%20scientist&page=0&per_page=20" | jq '.' > hh.json
