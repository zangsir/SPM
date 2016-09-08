#!/bin/bash

/Applications/Praat.app/Contents/MacOS/Praat ~/Desktop/speech-exp-diuss/get_pitch.praat 

outname='pitch-001-75'
echo 'finished generating pitch files, now plotting...'
python pitch-plot.py $outname
open $outname$".pdf"