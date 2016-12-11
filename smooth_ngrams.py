#takes all the normalized (but not downsampled) pitch files in syl_csv_norm and smooth them, output to syl_csv_norm_smooth/
#from smooth_demo import *
from os import listdir
import random,sys
from scipy.ndimage import filters
from scipy.signal import gaussian
import numpy as np
import matplotlib.pyplot as plt
from smooth_demo import plot_demo

def smooth_convolution(y, npts, M, std):
    """npts is the number of points in the time-series"""
    b = gaussian(M, std)
    ga = filters.convolve1d(y, b/b.sum())
    return ga

#append to file
def append_syl(pv,outname):
    g=open(outname,'w')
    g.write('')
    g.close

    f=open(outname,'a')
    for row in pv:
        row=[str(i) for i in row]
        line=','.join(row)
        f.write(line+'\n')
    f.close()

def smooth_file(inputfile):
    """smoothes one utterance file containing several syllable pitch lines"""
    f=open(inputfile,'r').read().split('\n')
    pitch_vec_smooth=[]
    pitch_vec_orig=[]

    for line in f:
        if line!='':
            l=line.split(',')[:-1]
            lf=[float(i) for i in l]
            ga=smooth_convolution(np.array(lf),len(lf), 10, 5)
            label=line.split(',')[-2]
	    position=line.split(',')[-1]
            lfl=list(lf)
            gal=list(ga)
            lfl.append(label)
            gal.append(label)
	    lfl.append(position)
	    gal.append(position)
            pitch_vec_orig.append(lfl)
            pitch_vec_smooth.append(gal)
    return pitch_vec_orig,pitch_vec_smooth

            

def demo_plot(inputfile):
    print "file name:",inputfile
    lf,ga = smooth_file(inputfile)
    print "label:",ga[1][-1]
    plot_demo(lf[1][:-1],ga[1][:-1])



def main():
    """for all files in syl_csv_norm, process smoothing"""
    path='syl_csv_norm_whole'
    onlyFiles = [ f for f in listdir(path) if f.endswith(".csv")]
    outdir='syl_csv_norm_whole_smooth'
    #outdir='test_qphons'
    demo=False
    if demo:
        file=random.choice(onlyFiles)
        inputfile=path+'/'+file
        demo_plot(inputfile)
        sys.exit()


    print onlyFiles
    for file_pitch in onlyFiles:
        inputfile=path+'/'+file_pitch
        orig, smoothed = smooth_file(inputfile)
        #print smoothed
        first_name=file_pitch.split('.')[0]
        outname=outdir+'/'+first_name+'_smoothed.csv'
        append_syl(smoothed,outname)



        

if __name__ == '__main__':
    main()
