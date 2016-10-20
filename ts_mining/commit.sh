#!/usr/bin/env bash
cp ~/Desktop/speech-exp-diuss/*.py *.sh *.praat *.ipynb ~/repo/SPM
cp ~/Desktop/speech-exp-diuss/ts_mining/*.py *.sh ~/repo/SPM/ts_mining/
cd ~/repo/SPM
git status
git add -A
git commit -m $1
git pull
git push