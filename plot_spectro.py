import re,sys
from os import listdir
import numpy as np
import matplotlib.pyplot as plt
from bisect import bisect_left
from batch_interp import *
from scipy.io.wavfile import read

#sample usage:
#python plot_spectro.py pitch/pitcCHX000040.tab test/CHX000040.phons test/CHX000040.wav 

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError


def get_annos(phons_file):
    g=open(phons_file,'r').read().split('\n')
    timestamps=[]
    for line in g:
        l=line.split()
        if line!='':
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




def plot_spectro(time,pitch,my_xticks,timestamps,audio_file):
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
        plt.plot((l[0],l[0]),(50,1500),'k-')
    plt.ylim([50,1500])
    plt.savefig('spectro.pdf')


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



def do_plot(audio_file,pitch_tab_file,phons_file):
    timestamps,xt,labels=get_annos(phons_file)
    #get some time and pitch files
    time,adjusted_time,pitch,trim_pitch=trim(pitch_tab_file)
    my_xticks=gen_annos(time,xt,labels)
    plot_spectro(time,pitch,my_xticks,timestamps,audio_file)




if __name__=="__main__":
    if len(sys.argv)==4:
        audio_file=sys.argv[3]
        pitch_tab_file=sys.argv[1]
        phons_file=sys.argv[2]
        do_plot(audio_file,pitch_tab_file,phons_file)
    if len(sys.argv)==2:
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
            qph=gen_qphons(timestamps,trim_pitch,time)
            write_qphons_file(qphons_output,qph)
            












