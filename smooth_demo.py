from scipy.ndimage import filters
from scipy.signal import gaussian
import random
import numpy as np
import matplotlib.pyplot as plt


def testGauss(x, y, s, npts):
    """this plots the results of the smoothing by convolution"""
    b = gaussian(39, 10)
    ga = filters.convolve1d(y, b/b.sum())
    plt.plot(x, ga)
    plt.scatter(x,ga)
    plt.show()
    #print "gaerr", ssqe(ga, s, npts)
    return ga


#for demo usage, see Tone-ngrams.ipynb on github

def smooth_convolution(y, npts):
    """npts is the number of points in the time-series"""
    b = gaussian(10, 5)
    ga = filters.convolve1d(y, b/b.sum())
    return ga


def noisy_data_demo():
    npts = 1024
    end = 8
    dt = end/float(npts)
    nyf = 0.5/dt
    sigma = 0.5 
    x = np.linspace(0,end,npts)
    n = np.random.normal(scale = sigma, size=(npts))
    s = np.sin(2*np.pi*x)
    y = s + n
    plt.plot(x,s)#signal
    plt.plot(x,y,ls='none',marker='.')#signal and noise
    testGauss(x,y,s,npts)

def tone_ngrams_demo():
    """plot the original trigram overlaid with the smoothed curce"""
    f=open('csv/trigram_new.csv','r').read().split('\n')
    i=random.choice(range(17))
    i=0
    print 'i=',i
    test=f[i].split(',')[:-1]
    x=range(len(test))
    plt.plot(x,test,'gx',label='original')
    test=[float(i) for i in test]
    #ga=testGauss(np.array(x),np.array(test),np.array(test),len(test))
    ga=smooth_convolution(np.array(test),len(test))
    plt.scatter(x,ga,label='smoothed')
    plt.title('tone trigram gaussian(39,10)')
    plt.legend(loc='upper center', shadow=True)
    plt.show()

def plot_demo(orig_y,smoothed_y):
    plt.plot(orig_y,'gx',label='original')
    plt.plot(smoothed_y,'yo',label='smoothed')
    plt.legend(loc='upper right')
    plt.show()


def main():
    #print "generating noisy data demo..."
    #noisy_data_demo()
    
    print "generating tone trigram demo..."
    tone_ngrams_demo()
    



if __name__ == '__main__':
    main()
