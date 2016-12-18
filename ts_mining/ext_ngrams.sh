#!/usr/bin/env bash

#usage:./ext_ngrams.sh N smooth
#example:./ext_ngrams.sh 2 0 means bigram and smooth off.

#for motif discovery, ngrams should not have labels in the end (but you should keep a version with labels of course)

#Each ngrams should be downsampled to N*30 dimensions(or not, since exp. shows that the 30 point performs better than 60, for example, in bigram)

#we want to be able to trace back each ngram to its recording. So ngrams data files should be written with other information in the csv file (append more columns), maybe like an ID or something that identifies the ‘CHJ00001’ for example.



#shell script to pipeline the syllable extraction, smoothing, downsampling

#you can turn off smoothing and do downsampling from the original file.


#######Ngrams
#whole syllable extraction
#input path:'norm_pitch','all_data'
#output path:'syl_csv_norm_whole'
#note:different from voiced unigrams, the whole_syl output for ngrams has two extra cols in the end, label and position ('mid', 'end'), as boundaries for the ngrams extraction 
#python extract_syl_whole.py

#set N in ngrams
N=$1
##########smoothing:this step is omitted in the unsmoothed versioni.if working with unsmoothed, you can still use results from above and simply set smooth to be 0 below.
#input path:'syl_csv_norm_whole'
#output path:'syl_csv_norm_whole_smooth'
smooth=$2
if [ $smooth = 1 ]
then
    unigramPath="syl_csv_norm_whole_smooth"
    unigramAll="syl_norm_split_smooth.csv"
    ngramsOutName=$N'-grams_smooth.csv'
    python smooth_ngrams.py
else
    unigramPath="syl_csv_norm_whole"
    unigramAll="syl_norm_split.csv"
    ngramsOutName=$N'-grams.csv'
fi
#concatenation into one file of variable length syllable pitch contours
#this script resides in the syl_csv_norm_whole directory
#output:syl_norm_split.csv or syl_norm_split_smooth.csv



echo 'concatenating unigrams...'
python concat.py $unigramPath"/*.csv" $unigramAll
wc -l $unigramAll


#echo 'done concatenation...'
echo 'performing ngrams extraction...'
#ngrams extraction from unigram file 
#input: syl_norm_split.csv or syl_norm_split_smooth.csv
#output: trigram_new.csv,or trigram_smooth.csv
#argument:N in ngrams


python extract_ngrams.py $N $unigramAll $ngramsOutName
mv downsample_ngrams_one/* downsample_ngrams_all/
mv $ngramsOutName  downsample_ngrams_one/
#downsample(note that non-neutral tone selection only happens at the downsample stage, not before)
#also note that downsample in unigram takes a directory of indie files and outputs one file; in the ngrams case, we already produced one file (trigram_new.csv or bigram_new.csv) in previous step, but we don't want to change the way downsample.py works, so we just put this one file inside the directory it read from.
#what we do here is that each time, let's say you're downsampling bigrams, so you put the bigram_new.csv into the downsample_ngrams_one/ directory and run downsample.py. All other files (such as trigram_new.csv, or smoothed versions of these) resides in the downsample_ngrams_all/ directory.
#input path (non-smooth):'downsample_ngrams_one/'
#input path (smoothed):'downsample_ngrams_all/'
#output file (option 1, for unigram only):'downsample_syl_noneut.csv'
#output file (option 2, for ngrams):'downsample_syl_tri.csv' or _bi.csv
echo 'downsampling...'
#specify the length of downsampled vector
comp_len=30
#the second argument controls on or off of smoothing
python downsample.py $N $smooth $comp_len
ls -lt | head
#then move your output file (one file) into csv/
