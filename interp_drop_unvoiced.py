from batch_interp import *

# first trim
time,adjusted_time,pitch,trim_pitch=trim(pitch_tab_file)

# then get rid of unvoiced seg - set to 0
