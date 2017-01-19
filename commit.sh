#!/usr/bin/env bash

##### MUST SUPPLY A COMMIT MESSAGE!!!!!
cp *.py *.sh *.praat *.ipynb ~/repo/SPM
#cp ts_mining/*.py *.sh ~/repo/SPM/ts_mining/
cp ~/Desktop/2017/diss_report/motif_disc/motif_diss.tex ~/repo/SPM
cd ~/repo/SPM
git status
git add -A
git commit -m $1
git pull
git push
