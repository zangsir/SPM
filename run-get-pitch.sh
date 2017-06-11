#!/bin/bash

#0.01,0.001
#50,75
#this script is the pipeline of pitch preprocessing, including pitch estimation, format conversion, trimming, unvoiced trim, interpolation, with the options in the middle to plot stuff

pitch_step=0.001
pitch_floor=50
interpolation='no'
sound_path="/Users/zangsir/Desktop/thai-CHILDES/CRSLP/processed"

/Applications/Praat.app/Contents/MacOS/Praat ~/Desktop/speech-exp-diuss/get_pitch.praat $pitch_step $pitch_floor $interpolation $sound_path

#outname='pitch-'$pitch_step'-'$pitch_floor'-intp'$interpolation
echo ==============
#echo 'finished generating pitch files, now plotting...'
#python pitch_plot.py $outname
#open $outname$".pdf"
#python trim_pitch.py $outname
#echo =============
echo converting pitch to tab files...
python simple_pitch.py
echo ============
#echo trimming...
#python batch_trim.py $outname
#python batch_interp.py $outname
#echo processing pitch...
#assumes pitch tab file and phons file are both in the pitch/ directory(currently turned off), or must give these paths:pitch_path,phons_path
#python write_pitch_proc.py 'pitch' $sound_path
#the result of the operations above will be the trimmed and interpolated preprocessed pitch file, two col format, with extrapolation 1000, and without unvoiced frames. one file per sentence.