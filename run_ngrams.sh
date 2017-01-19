#!/usr/bin/env bash

#unigram extraction

#./extract_syl_meta.sh 1 30
./extract_syl_meta.sh 2 30
./extract_syl_meta.sh 2 100


#ngrams extraction
./ext_ngrams.sh 2 0 100
./ext_ngrams.sh 2 0 200
./ext_ngrams.sh 2 0 300
./ext_ngrams.sh 2 0 400
./ext_ngrams.sh 3 0 100
./ext_ngrams.sh 3 0 200
./ext_ngrams.sh 3 0 300
./ext_ngrams.sh 3 0 400
./ext_ngrams.sh 3 0 500


mv downsample*0.csv MK_data/csv_version

#make space ver and make MK ver
./make_MK_ver.sh MK_data/csv_version 




