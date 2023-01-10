#!/usr/bin/env bash

# find all 'all.txt' log files under a directory specified in LOGBASEDIR env var
# merge those files into one file

if [ -z "$LOGBASEDIR" ];
then
  echo "Error: please set LOGBASEDIR"
  exit 1
fi

ONEFILE="$LOGBASEDIR/merged.txt"

if [ -f "$ONEFILE" ];
then
  echo "Error: $ONEFILE already exists"
  exit 1
fi

find "$LOGBASEDIR" -name 'all.txt' | xargs -I '{}' cat '{}' >> "$ONEFILE"

echo "All 'all.txt' files found under $LOGBASEDIR are merged into $ONEFILE"
