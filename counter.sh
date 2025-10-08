#!/bin/sh

CSV_PATH=/var/gopher/guestbook/guestbook.csv
COUNT=$(cat ${CSV_PATH} | wc -l)
# The first line contains the CSV column headers, so it doesn't count
echo "Visitors wrote $((COUNT-1)) messages here since October 2025."
