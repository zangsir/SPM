import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import sys

outname=sys.argv[1]

dir='pitch'
#input .tab file
filename=sys.argv[2]
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

#use adjusted time(which ends the same time as the new_time but o/w has the same timestamps as time) to avoid spurious interpolation beyond end range    
adjusted_time=[i for i in time if i<=new_time[-1]]
 
#plt.plot(new_time,new_pitch)
fp=interp1d(new_time,new_pitch,bounds_error=False, fill_value=0.001)
f, (ax1, ax2,ax3) = plt.subplots(3, 1,sharey=True)
ax1.scatter(new_time, new_pitch)
ax1.set_title("after trimming")
ax2.scatter(adjusted_time, fp(adjusted_time))
ax2.set_title("linear interpolation")
ax3.scatter(time,pitch)
ax3.set_title("original")
outfile='trim-'+outname+'.pdf'
f.savefig(outfile)
print 'saved trim plot ' + outfile