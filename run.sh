#!/bin/bash

if [ $# -ne 1 ]; then
    echo 'Usage: run.sh $CONFIG_FILE'
    exit 1
fi

CONF_FILE=$1

while true; do
    python server.py $CONF_FILE
    sleep 1
done
