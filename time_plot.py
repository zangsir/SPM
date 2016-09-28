import time
from plot_spectro import *

start = time.time()
# run your code
audio_file='MacAir-orig-data/cmn_phonetic_segmentation_tone/data/train/DOH001372.wav'
pitch_tab_file='procd_pitch/DOH001372_proc.tab'
phons_file='MacAir-orig-data/cmn_phonetic_segmentation_tone/data/train/DOH001372.phons'
do_plot(audio_file,pitch_tab_file,phons_file)
end = time.time()

elapsed = end - start
print elapsed