from pitch_plot import gen_xy
from os import listdir

#'pitch/pitcCHJ000032.pitch'



def gen_simple_pitch(inputfile):
    x,y=gen_xy(inputfile)
    newfile=inputfile.split('.')[0]+'.tab'
    f=open(newfile,'w')
    f.write("time\tpitch\n")
    f.close()
    f=open(newfile,'a')

    for i in range(len(x)):
        line=x[i]+'\t'+y[i]
        f.write(line+'\n')
    f.close()


dir='pitch'
onlyfiles = [ f for f in listdir(dir) if f.endswith(".pitch")]
print onlyfiles
for filename in onlyfiles:
    gen_simple_pitch(dir+'/'+filename)