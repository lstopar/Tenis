#!/bin/bash

for fname in problematic/*; do
    echo "processing file $fname"
    res=`python test.py $fname`
    # req=`cat $fname`

    req=`echo $res | tail -n +1 | head -n 1`
    # echo "req:\n$req"
    node check-result.js "$res"
done
