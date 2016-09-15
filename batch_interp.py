import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import sys
from os import listdir
import numpy as np

#adjusted time just ends earlier than time
#this interpolate_pitch() and the interpolation at the end of trim() is: in the latter, which was applied first, the time variable has a lot of gaps, namely, the segments from praat's pitch estimation without voicing and therefore no pitch values. The former, applied later, will fill in all the value with a continuous time start to end with 0.001s step.
def interpolate_pitch(begin,end,time,pitch):
    interp_time=np.arange(float(begin),float(end),0.001)
    fp=interp1d(time,pitch,bounds_error=False, fill_value=1000)
    interp_pitch=fp(interp_time)
    return interp_time,interp_pitch


def pitch_floor(interp_pitch):
    for i in range(len(interp_pitch)):
        if interp_pitch[i]<50:
            interp_pitch[i]=50
    return interp_pitch



def trim(inputfile):
    """input should be a pitch.tab file"""
    
    #filename='pitcCHJ000032.pitch_simple.tab'
    f=open(inputfile,'r').read().split('\n')

    time=[]
    pitch=[]
    for i in range(1,len(f)):
        line=f[i]
        if line!="":
            split=line.split('\t')
            #print split
            time.append(float(split[0]))
            pitch.append(float(split[1]))


    B=plt.boxplot(pitch)
    plt.savefig(inputfile+'box.pdf')
    plt.close() 
    ydata=[item.get_ydata() for item in B['whiskers']]
    upper=ydata[1][1] #this is the upper whisker

    new_pitch=[]
    new_time=[]
    for i in range(len(pitch)):
        if pitch[i]<=upper:
            new_pitch.append(pitch[i])
            new_time.append(time[i])
        
    adjusted_time=[i for i in time if i<=new_time[-1]]
        
    #plt.plot(new_time,new_pitch)
    fp=interp1d(new_time,new_pitch,bounds_error=False, fill_value=1000)
    ####important: at first when I invented adjusted_time, I used that to interpolate the entire pitch track so the end won't get interpolated in an out-of-bounds manner. But then for the sake of working with textgrids, we changed to doing the interpolation using the entire time of the original track. So beware the fp(time) vs. fp(adjusted_time ) below. 
    return time,adjusted_time,pitch,fp(adjusted_time)


def plot_orig_interp(orig_time,orig_pitch,trim_time,trim_pitch,outname):
    plot_dir='plots'
    f, (ax1, ax2) = plt.subplots(2, 1,sharey=True)
    #ax2.plot(new_time, new_pitch)
    #ax2.set_title("after trimming")
    ax1.scatter(interp_time, interp_pitch)
    ax1.set_title("linear interpolation")
    ax2.scatter(orig_time,orig_pitch)
    ax2.set_title("original")
    outfile=plot_dir+"/"+'interp-'+outname+'.pdf'
    f.savefig(outfile)
    plt.close()
    print 'saved interp plot ' + outfile



if __name__=='__main__':
    outname=sys.argv[1]
    dir='pitch'
    #dir='pitch_prob'
    onlyfiles = [ f for f in listdir(dir) if f.endswith(".tab")]
    print onlyfiles
    for file_pitch in onlyfiles:
        inputfile=dir+'/'+file_pitch
        print inputfile
        time,adjusted_time,pitch,trim_pitch=trim(inputfile)
        begin,end=adjusted_time[0],adjusted_time[-1]
        interp_time,interp_pitch=interpolate_pitch(begin,end,time,trim_pitch)
        interp_pitch=pitch_floor(interp_pitch)
        outname_mod=outname+file_pitch.split('.')[0]
        plot_orig_interp(time,pitch,interp_time,interp_pitch,outname_mod)























