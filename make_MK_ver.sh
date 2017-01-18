#!/usr/bin/env bash

#this path is a path you created that contains all csv versions of the DB version ngram files that you want to make a MK version in the MK data format
inputPath=$1
python make_motif_ver.py $inputPath

#turn these off if these exist
#mkdir MK_data/temp_csv
#mkdir MK_data/mk_txt
#mkdir MK_data/mk_csv

mv MK_data/csv_version/*MK.csv MK_data/temp_csv/
ls MK_data/temp_csv

echo start make space ver...
python make_space_ver.py MK_data/temp_csv
mv MK_data/temp_csv/*.txt MK_data/mk_txt
mv MK_data/temp_csv/*.csv MK_data/mk_csv
