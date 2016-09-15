#interpolate a single pitch file and plot it and save it
import numpy as np
from scipy.interpolate import interp1d
from batch_trim import *
import matplotlib.pyplot as plt
import sys

def interpolate_pitch(begin,end,pitch):
    interp_time=np.arange(float(begin),float(end),0.001)
    fp=interp1d(time,pitch,bounds_error=False, fill_value=-0.001)
    interp_pitch=fp(interp_time)
    return interp_time,interp_pitch





if __name__ == '__main__':
    pfile=sys.argv[1]
    time,pitch,new_pitch=trim(pfile)
    begin=time[0]
    end=time[-1]
    interp_time,interp_pitch=interpolate_pitch(begin,end,new_pitch)
    plt.plot(interp_time,interp_pitch)
    plt.savefig(pfile+".pdf")
