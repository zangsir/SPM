cp ~/Desktop/speech-exp-diuss/*.py *.sh *.praat *.ipynb ~/repo/SPM
cd ~/repo/SPM
git status
git add -A
git commit -m $1
git pull
git push