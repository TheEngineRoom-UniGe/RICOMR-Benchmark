#!/bin/bash
echo "execution started.."

while [ true ]; do
    echo "Stamp Recorded.."
    top -b -n 3 | sed -n '8, 12{s/^ *//;s/ *$//;s/  */,/gp;};12q' >> top.txt
    echo -e "---------------------------" >> top.txt

    mpstat -P ALL >> mpstat.txt
    echo -e  "---------------------------" >> mpstat.txt
    sleep 5
done
