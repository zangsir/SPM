cp ~/Desktop/speech-exp-diuss/*.py *.sh *.praat ~/repo/SPM
cd ~/repo/SPM
git status
git add -A
git commit -m 'implemented trim unvoiced seg'
git pull
git push