#showing three ways of downsampling, and their plots
from scipy import signal
import math, scipy
from extract_syl_pitch import *
import random


#padding and averaging then extract first 30 points
def downsample_averaging(ts):
    tsf=[float(i) for i in ts]
    R=math.floor(len(ts)/30.0)
    b=np.array(tsf)
    #print R
    #print len(ts)/R
    pad_size = math.ceil(float(b.size)/R)*R - b.size
    b_padded = np.append(b, np.zeros(pad_size)*np.NaN)
    #print b_padded.shape
    #=> (9,)
    result=scipy.nanmean(b_padded.reshape(-1,R), axis=1)
    return result[:30]



#resample
def plot_matrix_resample(pv,num_per_row,filename):    
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
        x = np.linspace(0,30, len(ts))
        xr = np.linspace(0,30,30)
        #plt.plot(x,ts,'gx')
    
        z=signal.resample(ts,30)
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
def downsample_mix(vec,comp_len):
    #print vec[:10]
    orig_len=len(vec)
    a,b=int(math.floor(len(vec)/float(comp_len))),int(math.ceil(len(vec)/float(comp_len)))
    #print a,b
    if a!=b:
        x=(orig_len-30*b)/(a-b)
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
def plot_matrix_average(pv,num_per_row,filename):    
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
        x = np.linspace(0,30, len(ts), endpoint=False)
        xr = np.linspace(0,30,30)
        #plt.plot(x,ts,'gx')
    
        z=downsample_averaging(ts)
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

def plot_matrix_mix(pv,num_per_row,filename):    
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
        x = np.linspace(0,30, len(ts), endpoint=False)
        xr = np.linspace(0,30,30)
        #plt.plot(x,ts,'gx')
    
        #z=downsample_averaging(ts)
        z=downsample_mix(ts,30)

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


def demo(mode,pv,num_per_row,filename):
    """mode is ave, mix, res"""
    if mode=='ave':
        plot_matrix_average(pv,num_per_row,filename)

    elif mode == 'mix':
        plot_matrix_mix(pv,num_per_row,filename)

    elif mode == 'res':
        plot_matrix_resample(pv,num_per_row,filename)



def main():
    global plot_dir
    plot_dir='plots'
    path='syl_csv_norm'
    #path='test-small'
    #dir='pitch_prob'
    onlyfiles = [ f for f in listdir(path) if f.endswith(".csv")]
    #print onlyfiles
    demo=False
    if demo:
        num_file=4
        SEED = 948
        random.seed(SEED)
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
            demo('ave',pv,2,file_pitch)
            demo('mix',pv,2,file_pitch)
            demo('res',pv,2,file_pitch)
    else:
        open('downsample_syl.csv','w').close()
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
            
            f=open('downsample_syl.csv','a')

            for p in pv:
                ts=p[:-1]
                if len(ts)==0:
                    print "WARNING:error in data file in "+file_pitch
                    continue
                tsd=downsample_mix(ts,30)
                line=','.join(tsd)
                f.write(line+','+p[-1]+'\n')
            f.close()




if __name__=="__main__":
    main()

