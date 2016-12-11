#!/usr/bin/env bash

#shell script to pipeline the syllable extraction, smoothing, downsampling

#you can turn off smoothing and do downsampling from the original file.
#

#######unigram
#syllable extraction
#input path:'norm_pitch','all_data'
#output path:'syl_csv_norm'
python extract_syl_pitch.py

#smoothing
#input path:'syl_csv_norm'
#output path:'syl_csv_norm_smooth'
#python smooth.py

#downsample
#input path (non-smooth):'syl_csv_norm'
#input path (smoothed):'syl_csv_norm_smooth'
#output file (option 1):'downsample_syl_noneut.csv'
#output file (option 2):''downsample_syl_tri.csv'
python downsample.py

#then move your output file (one file) into csv/


######ngrams
