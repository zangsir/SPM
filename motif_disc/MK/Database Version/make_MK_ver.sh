#!/usr/bin/env bash


inputPath=$1
python make_motif_ver.py $inputPath

mv MK_data/*MK.csv MK_data/temp_csv/
ls MK_data/temp_csv

echo start make space ver...
python make_space_ver.py MK_data/temp_csv
mv MK_data/temp_csv/*.txt MK_data/mk_txt
mv MK_data/temp_csv/*.csv MK_data/mk_csv
