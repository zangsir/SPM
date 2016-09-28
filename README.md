# SPM
speech prosody mining using time-series mining techniques

# Data Set
from LDC is generally not shared here. Another data set is stored in MCtone-learning repo.

# Usage

### to do pitch estimation and plot pitch contours from sound files in a directory
currently I use praat autocorrelation to do pitch estimation. run the shell scripts to run praat pitch estimation, and python plots (generating pdf files of pitch contour plot matrixes of the input sound files). Currently it is hardwired to read *.flac files from the CMN corpus, but can be changed. Use pitch_plot.py. 


### pitch track computation
The general procedure is to first do pitch estimation with time step =0.001, floor,ceiling=50,600, in Praat and output the .pitch file. This is doen without interpolation so the time is discontinuous on unvoiced segments. Then, we first trim the pitch by getting rid of everything above the pitch distribution boxplot's upper whisker for this sentence. We also trim a second time to get rid of values in the unvoiced segments (according to .phons file) to avoid picking up spurious values in those segs. Then we interpolate using original time for the trim_pitch. This will give us a time dimension the same as original time. At this point we can evaluate the quality of the pitch estimation, by computing the .qphons file, described below. Then, to obtain the final continuous-time pitch track we generate a continous time from begin to end of the sound file using time step 0.001s, and we interpolate pitch values using this interp_time, and we interpolate all the pitch values for the unvoiced segments. Use batch_interp.py. Use write_pitch_proc.py to write final computed pitch into two-col format, tab separated file: time and pitch cols. 

### pitch pre-processing
Use norm_spk.py to do speaker-based normalization. This will pool all files from the same speaker and compute mean and sd. The result is used in next step: extract syllable sized contours.

### extracting syllable-sized pitch contours
Using extract_syl_pitch.py, we can extract these from the tab files generated in the prev step into a csv file. Each row represents one syllable contour, with the last value being its true label of tone. Currently we extract only the rhyme part of the syllable. May vary according to our needs later.

### other preprocessing
Should do log (or Cent) conversion, smoothing(?), downsampling for Euclidean dist, and no downsampling for SAX.

### why do we need adjusted time or second adjusted time?
If we trimmed pitch, yielding trim_pitch, then we want to interpolate back so the number of values is consistent to time. However, if the beginning or ending time points of pitch values got trimmed, then it’ll fall back to interpolation and you can get a 0 (if the default extrapolation values is 0) or a couple of 0s at beginning and end. Then, in the next step when you do further unvoiced seg interpolation, the result will be bad. that’s why we want adjusted_time to end at the actual last point of trimmed pitch, possibly before time ends, and the second_adjusted_time for the beginning, same story.



### visualize trimmed and interpolated pitch
This can be done with batch_trim.py and batch_interp.py. You can view pitch tracks side by side.


### generate .qphons file from .phons file and pitch .tab files
This is pertaining to LDC-CMN corpus. The .qphons file contains one more col than .phons file, which indicates the ratio of the duration of good pitch estimation to the duration of the voiced segment in question. This will indicate whether this syllable/segment will provide reliable pitch estimation in future exp. pitch .tab files are simple two-column format time-pitch files converted from Praat's .pitch file. Use plot_spectro.py and supply a directory that contains all the .phons files. This assumes your pitch .tab files are stored in pitch/. 

### plot spectrogram overlaid with pitch track and segmentation
This would give you the capability to visualize spectrogram, segmentation, text annotation, and pitch track in one image. Crucially, this pitch track will be whatever pitch track you have supplied, not like in Praat where you can only visualize the pitch track computed by Praat. Use plot_spectro.py and supply three args: pitch_tab_file,phons_file,audio_file, in this order. 
