import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import sys
from os import listdir



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
    fp=interp1d(new_time,new_pitch,bounds_error=False, fill_value=-0.001)
    return time,adjusted_time,pitch,fp(adjusted_time)


def plot_orig_trim(orig_time,adjusted_time,orig_pitch,trim_pitch,outname):
    plot_dir='plots'
    f, (ax1, ax2) = plt.subplots(2, 1,sharey=True)
    #ax2.plot(new_time, new_pitch)
    #ax2.set_title("after trimming")
    ax1.scatter(adjusted_time, trim_pitch)
    ax1.set_title("linear interpolation")
    ax2.scatter(orig_time,orig_pitch)
    ax2.set_title("original")
    outfile=plot_dir+"/"+'trim-'+outname+'.pdf'
    f.savefig(outfile)
    plt.close()
    print 'saved trim plot ' + outfile



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
        outname_mod=outname+file_pitch.split('.')[0]
        plot_orig_trim(time,adjusted_time,pitch,trim_pitch,outname_mod)























