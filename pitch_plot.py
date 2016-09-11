import re,sys
from os import listdir
import matplotlib.pyplot as plt





def plot_matrix(xs,ys,i,j):
    f, axarr = plt.subplots(i,j)
    axarr[i, j].plot(xs, ys)
    
    
    
def gen_xy(pitch_file):
    """from a pitch file, return a list of times, and a list of pitch values"""
    f=open(pitch_file,'r').read()
    fl=f.split('\n')
    times=[]
    pitches=[]
    for line in fl:
        if re.search('number =',line):
            times.append(line.split(' = ')[1].replace(' ',''))
        if re.search('value =',line):
            pitches.append(line.split(' = ')[1].replace(' ',''))
    assert(len(times)==len(pitches))
    return times,pitches

def gen_simple_pitch_file(pitch_file):
    xs,ys=gen_xy(pitch_file)
    f=open(pitch_file+"_simple.tab",'w')
    f.write("time\tpitch\n" )
    f.close()
    f=open(pitch_file+"_simple.tab",'a')
    for i in range(len(xs)):
        f.write(xs[i]+'\t'+ys[i]+'\n')
    f.close()



if __name__ == "__main__":
    #set this number
    num_per_row=2
    inputname='pitch'
    onlyfiles = [ f for f in listdir(inputname) if f.endswith(".pitch")]
    print "total number of files: ", str(len(onlyfiles))

    outname=sys.argv[1]
    outname=outname+'.pdf'

    num_file=len(onlyfiles)
    num_plot=num_file




    #plot num_per_row per row
    while num_plot%num_per_row!=0:
        num_plot+=1
    #plot a by b matrix
    b=num_per_row
    a=num_plot/b


    f, axarr = plt.subplots(a,b)
    i=j=0
    for file in onlyfiles:
        #print i,j
        xs,ys=gen_xy(inputname+'/'+file)
        axarr[i, j].plot(xs, ys)
        if j==b-1:
            i+=1
            j=0
        else:
            j+=1

    f.savefig(outname)
