#!/bin/bash

fnames=`cat problematic-files.txt`

for fname in $fnames; do
    echo "copying $fname"
    cp /mnt/raidM2T/project-data/tennis/$fname problematic
done

echo "done"
