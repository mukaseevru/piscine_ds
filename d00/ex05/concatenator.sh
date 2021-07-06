#!/bin/sh

echo "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"" > hh_positions.csv
cat 20*.csv | sed -En '/^"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"$/!p' >> hh_positions.csv
