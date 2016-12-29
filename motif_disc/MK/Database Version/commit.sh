#!/usr/bin/env bash

##### MUST SUPPLY A COMMIT MESSAGE!!!!!
cp *.py *.sh *.praat *.ipynb ~/repo/SPM
cp motif_disc/MK/Database\ Version/*.py *.sh ~/repo/SPM/motif_disc/MK/Database\ Version/
cd ~/repo/SPM
git status
git add -A
git commit -m $1
git pull
git push
