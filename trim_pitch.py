import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import sys

outname=sys.argv[1]

dir='pitch'
filename='pitcCHJ000032.pitch_simple.tab'
f=open(dir+'/'+filename,'r').read().split('\n')

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
ydata=[item.get_ydata() for item in B['whiskers']]
upper=ydata[1][1] #this is the upper whisker

new_pitch=[]
new_time=[]
for i in range(len(pitch)):
    if pitch[i]<=upper:
        new_pitch.append(pitch[i])
        new_time.append(time[i])
    
        
#plt.plot(new_time,new_pitch)
fp=interp1d(new_time,new_pitch)
f, (ax1, ax2,ax3) = plt.subplots(3, 1,sharey=True)
ax1.plot(new_time, new_pitch)
ax1.set_title("after trimming")
ax2.plot(time, fp(time), '-')
ax2.set_title("linear interpolation")
ax3.plot(time,pitch)
ax3.set_title("original")
outfile='trim-'+outname+'.pdf'
f.savefig(outfile)
print 'saved trim plot ' + outfile