#!/bin/bash
echo "execution started.."

top -b -n 3 | sed -n '8, 12{s/^ *//;s/ *$//;s/  */,/gp;};12q' >> out.txt

while [ true ]; do
    sleep 5
    echo "Stamp Recorded.."
    top -b -n 3 | sed -n '8, 12{s/^ *//;s/ *$//;s/  */,/gp;};12q' >> out.txt
done