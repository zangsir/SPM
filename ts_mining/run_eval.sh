#!/usr/bin/env bash
n=10
echo ========================== >> qbc_res.txt
for i in $(seq 1 $n)
do
    echo $i
    python ts_mining.py >> qbc_res.txt

done