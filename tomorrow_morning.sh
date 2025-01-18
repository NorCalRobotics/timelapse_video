#!/usr/bin/env bash

TOMORROW=$(date --date='tomorrow' +%Y%m%d)
DEFAULT_TIME="${TOMORROW}${1:-0700}"
SPECIFIED_TIME="${2:-$DEFAULT_TIME}"

while [ $(date +%Y%m%d%H%M) -lt "${SPECIFIED_TIME}" ] ; do
    date | tr '\n' '\r'
    sleep 1
done
