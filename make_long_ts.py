from os import listdir
import sys

def get_vec(file):
    #time=[]
    pitch=[]
    f=open(file,'r').read().split('\n')
    for line in f[1:]:
        if line!='':
            l=line.split('\t')
            #time.append(l[0])
            pitch.append(l[1])
    return pitch

path='norm_pitch'
onlyFiles = [ f for f in listdir(path) if f.endswith(".tab")]
long_ts=[]
for file_pitch in onlyFiles:
    print file_pitch
    inputfile=path+'/'+file_pitch
    pitch_vec=get_vec(inputfile)
    long_ts.extend(pitch_vec)
sys.exit()
outputfile='all_spk_lts.txt'

print 'total ts length:',len(long_ts)

open(outputfile,'w').close()
f=open(outputfile,'a')
for i in long_ts:
    f.write(str(i)+'\n')
f.close()