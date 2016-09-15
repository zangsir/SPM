#!/bin/bash

#0.01,0.001
#50,75

pitch_step=0.001
pitch_ceiling=50
interpolation='no'
sound_path="/Users/zangsir/Desktop/speech-exp-diuss/test/"

/Applications/Praat.app/Contents/MacOS/Praat ~/Desktop/speech-exp-diuss/get_pitch.praat $pitch_step $pitch_ceiling $interpolation $sound_path

outname='pitch-'$pitch_step'-'$pitch_ceiling'-intp'$interpolation
echo ==============
echo 'finished generating pitch files, now plotting...'
python pitch_plot.py $outname
#open $outname$".pdf"
#python trim_pitch.py $outname
echo =============
echo converting pitch to tab files...
python simple_pitch.py
echo ============
#echo trimming...
#python batch_trim.py $outname
#python batch_interp.py $outname