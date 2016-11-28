import re,sys
from os import listdir
import numpy as np
import matplotlib.pyplot as plt
from bisect import bisect_left
from batch_interp import *
from scipy.interpolate import interp1d
from scipy.io.wavfile import read

#sample usage:
#python plot_spectro.py pitch/pitcCHJ000038.tab all_data/CHJ000038.phons all_data/CHJ000038.wav

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError


def get_annos(phons_file):
    #input could be phons or qphons file
    g=open(phons_file,'r').read().split('\n')
    timestamps=[]
    for line in g:
        l=line.split()
        if line!='' and not line.startswith('begin'):
            timestamps.append(l)
    xt=[]
    labels=[]
    for l in timestamps:
        xt.append(l[1])
        labels.append(l[2])
    return timestamps,xt,labels


def gen_annos(time,xt,labels):
    """xt is a set of end time stamps where labels are located """
    my_xticks = [""]*len(time)
    prev=0
    for k in range(len(xt)):
        t=float(xt[k])
        if t>=time[0]:
            #print "t=",t
            lt=bisect_left(time,t)-5
            #print "lt=",lt
            #print 'prev=',prev
            lta=(lt+prev)/2
            prev=lt

            #print 'lta=',lta

            my_xticks[lta]=labels[k]
            #print "label=",labels[k]
    return my_xticks




def plot_spectro(time,pitch,my_xticks,timestamps,audio_file,plotname):
    #input: a time and a pitch object (list), and the set of xticks
    input_data = read(audio_file)
    fs=16000

    S, freqs, bins, im = plt.specgram(input_data[1], NFFT=1024, Fs=fs, noverlap=512)
    #maxp=np.max(pitch)
    #minp=np.min(pitch)
    plt.xticks(time, my_xticks)
    plt.scatter(time,pitch)
    for l in timestamps:
        #print l
        plt.plot((l[0],l[0]),(50,300),'k-')
    plt.ylim([50,300])
    plt.savefig(plotname+'-spectro.pdf')


def gen_qphons(timestamps,trim_pitch,time):
    #trim_pitch and time should have the same length, which they should, because after you trimmed it, the deleted values are interpolated using time as the x-axis
    qphons=[]
    for tsp in timestamps:
        start,end,label=tsp[0],tsp[1],tsp[2]

        m = re.search(r'\d$', label)
        #print label,m
        # if the string ends in digits m will be a Match object, or None otherwise.
        if m is not None:
            #print start,end
            #print tsp
            syl_values=[trim_pitch[i] for i in range(len(trim_pitch)) \
                        if time[i]>=float(start) and time[i] <=float(end)]
            #voiced[label]=syl_values
            interp_time=np.arange(float(start),float(end),0.001)
            pitch_ratio=round(float(len(syl_values))/len(interp_time),3)
            #print len(syl_values),len(interp_time)
            qphons.append([str(start),str(end),label,str(pitch_ratio)])
        else:
            tsp.append('na')
            #print tsp
            qphons.append(tsp)
    return qphons



def write_qphons_file(filename,qph):
    g=open(filename,'w')
    g.write('begin,end,label,p_ratio\n')
    g.close()
    g=open(filename,'a')
    for line in qph:
        l='\t'.join(line)
        g.write(l+'\n')
    g.close()


#added trim-plot and interp-plot functions in plot_spectro.py. The former will show uninterpolated trimmed pitch track while the latter shows the entire time (as indicated by .phons file) with interpolated pitch. for visibility, extrapolation is set at 1000, but maybe reset to 0 when showing this to others.
def do_plot(audio_file,pitch_tab_file,phons_file):
    timestamps,xt,labels=get_annos(phons_file)
    #get some time and pitch files
    b=timestamps[0][0]
    e=timestamps[-1][1]
    #first trim(and interpolate to adjusted time)
    time,adjusted_time,pitch,trim_pitch=trim(pitch_tab_file)
    #then trim unvoiced pitch
    second_adjusted_time,trim_unv_pitch=trim_unvoiced(timestamps,adjusted_time,trim_pitch)
    #interpolate to .phons file time with extrapolation on beginning and end at a high(for visibility in plot) constant value
    interp_time,interp_pitch=interpolate_pitch(b,e,second_adjusted_time,trim_unv_pitch)
    #get the labels and label positions for the plot
    my_xticks_interp=gen_annos(interp_time,xt,labels)
    my_xticks = gen_annos(time,xt,labels)
    plot_spectro(second_adjusted_time,trim_unv_pitch,my_xticks,timestamps,audio_file,"trim")
    plot_spectro(interp_time,interp_pitch,my_xticks_interp,timestamps,audio_file,"interp")


def pitch_proc_chain(pitch_tab_file,phons_file):
    #in pitch preprocess, you need phons file because you want to filter out the unvoiced pitch estimation at first, then interpolate back those.
    timestamps,xt,labels=get_annos(phons_file)
    #get some time and pitch files
    b=timestamps[0][0]
    e=timestamps[-1][1]
    #first trim(and interpolate to adjusted time)
    time,adjusted_time,pitch,trim_pitch=trim(pitch_tab_file)
    #then trim unvoiced pitch
    second_adjusted_time,trim_unv_pitch=trim_unvoiced(timestamps,adjusted_time,trim_pitch)
    #interpolate to .phons file time with extrapolation on beginning and end at a high(for visibility in plot) constant value
    interp_time,interp_pitch=interpolate_pitch(b,e,second_adjusted_time,trim_unv_pitch)
    return interp_time,interp_pitch




def trim_unvoiced(timestamps,adjusted_time,trim_pitch):
    #adjusted_time and trim_pitch must have same length
    "further trim all unvoiced segments in case it picked up pitch values on those"
    trim_unv_pitch=[]
    trim_unv_time=[]
    ok_label=['m','n','l']

    for k in range(len(timestamps)):
        tsp=timestamps[k]
        prev_con_label=timestamps[k-1][2]
        if prev_con_label in ok_label:
            start=timestamps[k-1][0]
            end,label=tsp[1],tsp[2]

        else:
            start,end,label=tsp[0],tsp[1],tsp[2]
        m = re.search(r'\d$', label)
        #print label,m
        # if the string ends in digits m will be a Match object, or None otherwise.
        if m is not None:
            #print start,end
            #print tsp

            syl_values=[trim_pitch[i] for i in range(len(trim_pitch)) \
                        if adjusted_time[i]>=float(start) and adjusted_time[i] <=float(end)]
            syl_times=[adjusted_time[i] for i in range(len(adjusted_time)) \
                        if adjusted_time[i]>=float(start) and adjusted_time[i] <=float(end)]
            trim_unv_pitch.extend(syl_values[:])
            trim_unv_time.extend(syl_times[:])
    second_adjusted_time=[time for time in adjusted_time if time>=trim_unv_time[0] and time<=trim_unv_time[-1]]

    fp=interp1d(trim_unv_time,trim_unv_pitch)

    return second_adjusted_time,fp(second_adjusted_time)






if __name__=="__main__":
    if len(sys.argv)==4:#use this mode to plot spectrogram overlaid with pitch contour and segmentation for individual file
        #python plot_spectro.py pitch/pitcCHX000040.tab test/CHX000040.phons test/CHX000040.wav 
        #warning: to plot spectorgram it must take .wav file, not flac
        audio_file=sys.argv[3]
        pitch_tab_file=sys.argv[1]
        phons_file=sys.argv[2]
        do_plot(audio_file,pitch_tab_file,phons_file)
    if len(sys.argv)==2:
        #use this option to write to qphons files that adds a col to phons file to indicate the pitch est. to syllable dur. ratio 
        dir_phons=sys.argv[1]
        onlyfiles = [ f for f in listdir(dir_phons) if f.endswith(".phons")]
        print onlyfiles
        for phons_file in onlyfiles:
            firstname=phons_file.split('.')[0]
            qphons_output=dir_phons+'/'+firstname+'.qphons'
            pitch_tab_file='pitch/pitc'+firstname+'.tab'

            #write to the qphons file: there is no unvoiced interpolation yet. 
            timestamps,xt,labels=get_annos(dir_phons+'/'+phons_file)
            #get some time and pitch files
            time,adjusted_time,pitch,trim_pitch=trim(pitch_tab_file)
            qph=gen_qphons(timestamps,trim_pitch,adjusted_time)#keep in mind trim_pitch has same len as adjusted_time,b/c it was interpolated using adjusted_time. in this function they must have the same len.adjusted time ends earlier than time, o/w they are identical.
            write_qphons_file(qphons_output,qph)
            












