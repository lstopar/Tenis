#!/bin/bash

fname=$1
content=`cat $fname`

node brute-force.js "$content"
