#!/bin/bash

if [ $# -ne 1 ]; then
    echo 'Usage: run.sh $PORT $CONFIG_FILE'
fi

CONF_FILE=$1

python server.py $CONF_FILE
