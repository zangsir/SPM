#we want to put meta info into the individual utterance files, each containing a number of pitch contours.

#### unigram:only voiced parts
#modified to add meta and position in the end
#output is indivial utterance files in syl_csv_norm_meta/

#mode: 1 is voiced, 2 is whole

mode=$1
if [ $mode = 1 ]

then
echo voiced mode...

#voiced only
python extract_syl_pitch.py
#concatenate all files under syl_csv_norm_meta into one file.
python concat.py syl_csv_norm_meta/*.csv syl_norm_meta.csv

wc -l syl_norm_meta.csv
python downsample_meta.py 1 0 100

#there is only 74411 data points in this, comparing to the syl_csv_norm_whole based data file of 100161 lines. keep in mind that the current extraction is voiced part only and the other one is whole syllable extraction. If you look into syl_csv_norm vs. syl_csv_norm_meta, these directories actually have a number of 0-byte files (and should have the same number of lines) but it turns into non-zero in syl_csv_norm_whole. in a word, the current extraction of voiced parts filters out those unreliable pitch detection syllables.
#next we can move on down the list of the motif disc. files we want,of course first we need to finish this one by downsampling to 100 points..

else

echo whole mode...
#whole
#output directory is specified in this script to match the input of next py script.
echo extracting whole syllables...
#python extract_syl_whole.py
#echo concat...
#python concat.py "syl_csv_norm_whole_meta/*.csv" "syl_norm_whole_meta.csv"
#wc -l syl_norm_whole_meta.csv
echo downsampling...
python downsample_meta.py 1 0 80 whole
ls -lt | head
#wc -l downsample_syl_whole_meta.csv
fi
