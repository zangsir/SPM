#showing three ways of downsampling, and their plots
from scipy import signal
import math, scipy
from extract_syl_pitch import *
import random
import sys

#padding and averaging then extract first 30 points
def downsample_averaging(ts,comp_len=30):
    tsf=[float(i) for i in ts]
    R=math.floor(len(ts)/comp_len)
    b=np.array(tsf)
    #print R
    #print len(ts)/R
    pad_size = math.ceil(float(b.size)/R)*R - b.size
    b_padded = np.append(b, np.zeros(pad_size)*np.NaN)
    result=scipy.nanmean(b_padded.reshape(-1,R), axis=1)
    return result[:comp_len]



#resample
def plot_matrix_resample(pv,num_per_row,filename,comp_len=30):    
    #num_per_row=2
    #num_file=len(onlyfiles)

    
    num_file=len(pv)
    num_plot=num_file

    #plot num_per_row per row
    while num_plot%num_per_row!=0:
        num_plot+=1
    #plot a by b matrix
    b=num_per_row
    a=num_plot/b


    f, axarr = plt.subplots(a,b)
    i=j=0
    for p in pv:
        #print i,j
        ts=p[:-1]
        x = np.linspace(0,comp_len, len(ts))
        xr = np.linspace(0,comp_len,comp_len)
        #plt.plot(x,ts,'gx')
    
        z=signal.resample(ts,comp_len)
        #plt.plot(xr,z,'ro-')
    
        axarr[i, j].plot(x, ts, 'bx', xr, z, 'ro')
        plt.suptitle('downsample resampled')
        if j==b-1:
            i+=1
            j=0
        else:
            j+=1

    f.savefig(plot_dir+'/'+filename+"_res.pdf")
    print 'saved resampled plots '

#(not exactly)equidistant sampling
def downsample_mix(vec,comp_len=30):
    #print vec[:10]
    orig_len=len(vec)
    a,b=int(math.floor(len(vec)/float(comp_len))),int(math.ceil(len(vec)/float(comp_len)))
    #print a,b
    if a!=b:
        x=(orig_len-comp_len*b)/(a-b)
        y=comp_len-x
    else:
        x=y=comp_len/2
    #print x,y
    #print 'len vec:',orig_len
    #print 'len new vec:',str(a*x+b*y)
    new_vec=[]
    #start sampling from 2nd element, not 0th
    i=b/2
    #ex: a=5,b=4,x=20,y=30
    for k in range(x):
        #repeat this operation k times, each time advance i by a
        new_vec.append(vec[i])
        i+=a

    for k in range(y):
        new_vec.append(vec[i])
        i+=b
    return new_vec

#examing all ts, each one plot
def plot_matrix_average(pv,num_per_row,filename,comp_len=30):    
    #num_per_row=2
    #num_file=len(onlyfiles)
    
    num_file=len(pv)
    num_plot=num_file

    #plot num_per_row per row
    while num_plot%num_per_row!=0:
        num_plot+=1
    #plot a by b matrix
    b=num_per_row
    a=num_plot/b


    f, axarr = plt.subplots(a,b)
    i=j=0
    for p in pv:
        #print i,j
        ts=p[:-1]
        x = np.linspace(0,comp_len, len(ts), endpoint=False)
        xr = np.linspace(0,comp_len,comp_len)
        #plt.plot(x,ts,'gx')
    
        z=downsample_averaging(ts,comp_len)
        #plt.plot(xr,z,'ro-')
    
        axarr[i, j].plot(x, ts, 'bx', xr, z, 'ro')
        plt.suptitle('downsample averaging')

        if j==b-1:
            i+=1
            j=0
        else:
            j+=1

    f.savefig(plot_dir+'/'+filename+"_ave.pdf")
    print 'saved averaged plots '

def plot_matrix_mix(pv,num_per_row,filename,comp_len=30):    
    #num_per_row=2
    #num_file=len(onlyfiles)
    
    num_file=len(pv)
    num_plot=num_file

    #plot num_per_row per row
    while num_plot%num_per_row!=0:
        num_plot+=1
    #plot a by b matrix
    b=num_per_row
    a=num_plot/b


    f, axarr = plt.subplots(a,b)
    i=j=0
    
    for p in pv:
        #print i,j
        ts=p[:-1]
        x = np.linspace(0,comp_len, len(ts), endpoint=False)
        xr = np.linspace(0,comp_len,comp_len)
        #plt.plot(x,ts,'gx')
    
        #z=downsample_averaging(ts)
        z=downsample_mix(ts,comp_len)

        #plt.plot(xr,z,'ro-')
    
        axarr[i, j].plot(x, ts, 'bx', xr, z, 'ro')
        #f.set_title("mixed")
        plt.suptitle('downsample mixed')

        if j==b-1:
            i+=1
            j=0
        else:
            j+=1
    
    f.savefig(plot_dir+'/'+filename+"_mix.pdf")
    print 'saved mixed plots '


def demo(mode,pv,num_per_row,filename,comp_len=30):
    """mode is ave, mix, res"""
    if mode=='ave':
        plot_matrix_average(pv,num_per_row,filename,comp_len)

    elif mode == 'mix':
        plot_matrix_mix(pv,num_per_row,filename,comp_len)

    elif mode == 'res':
        plot_matrix_resample(pv,num_per_row,filename,comp_len)



def main():
    global plot_dir
    plot_dir='plots'
    N=int(sys.argv[1])
    smooth=int(sys.argv[2]) 
    comp_len=int(sys.argv[3])
    mode=sys.argv[4]#voiced or whole

    ##for unigram:input path is a path containing all files
    if N==1:
        if smooth==1:
            if mode=="voiced":
                path='syl_csv_norm_smooth'
            elif mode=='whole':
                path='syl_csv_norm_whole_smooth'
        elif mode=='voiced':
            path='syl_csv_norm_meta'
        elif mode=='whole':
            path='syl_csv_norm_whole_meta'
        else:
            print 'unknown mode'
            sys.exit()
    
    ##for unigram smoothed:
    
    
    #for ngrams path: contains only one file to be downsampled
    elif N>1:
        path='downsample_ngrams_one'
    print 'path:',path
    
    #comp_len=30*N
    #comp_len=30
    
    
    #path='test-small'
    #dir='pitch_prob'
    onlyfiles = [ f for f in listdir(path) if f.endswith(".csv")]
    #print onlyfiles
    demo_mode=False
    no_neutral=False
    
    if N==1:
        if no_neutral:
            #this is just for non-neutral unigram ext.
            outfile='downsample_syl_noneut.csv'
        else:
            if mode=='voiced':
                outfile='donwsample_syl_voiced_meta_%s.csv' %comp_len
            elif mode=='whole':
                outfile='downsample_syl_whole_meta_%s.csv' %comp_len




    elif N>1:
        if smooth=='1':
            outfile='downsample_syl_%s_smooth_meta_%s.csv'%(N,comp_len)
        else:
            outfile='downsample_syl_%s_meta_%s.csv'%(N,comp_len)
    if demo_mode:
        num_file=1
        #SEED = 948
        #random.seed(SEED)
        rand_files=random.sample(onlyfiles,num_file)
        print rand_files
        for file_pitch in rand_files:
            #pv is a vector that collects all syllable contours within one file which is a sentence of multiple syllables
            pv=[]
            inputfile=path+'/'+file_pitch
            f=open(inputfile,'r').read().split('\n')
            for syl in f:
                if syl!='':
                    pv.append(syl.split(','))
            print 'pv generated...'
            demo('ave',pv,2,file_pitch,comp_len)
            demo('mix',pv,2,file_pitch,comp_len)
            demo('res',pv,2,file_pitch,comp_len)
    else:
        open(outfile,'w').close()
        count_error_file=0
        for file_pitch in onlyfiles:
            #print file_pitch
            pv=[]
            inputfile=path+'/'+file_pitch
            f=open(inputfile,'r').read().split('\n')
            for syl in f:
                if syl!='':
                    pv.append(syl.split(','))
            #print 'pv generated...'
            #print pv
            
            f=open(outfile,'a')

            for p in pv:
                if mode=='voiced':
                    ts=p[:-3]
                elif mode=="whole":
                    ts=p[:-4]
                if len(ts)<comp_len:
                    #print "WARNING:error in data file in "+file_pitch
                    count_error_file+=1
                    continue
                if no_neutral:
                    if p[-3]=='0':
                        print '0 skipped(neural tone)'
                        continue
                tsd=downsample_mix(ts,comp_len)
                line=','.join(tsd)
                if mode=="voiced":
                    line_write=line+','+p[-3]+','+p[-2]+','+p[-1]+'\n'
                elif mode=="whole":
                    line_write=line+','+p[-4]+','+p[-3]+','+p[-2]+','+p[-1]+'\n'

                f.write(line_write)
            f.close()
        print "total file ignored:",count_error_file




if __name__=="__main__":
    main()

