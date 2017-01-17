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

#you should not use original pitch/ for this.
path='norm_pitch_final'
#path='procd_pitch_newtrim_final'
onlyFiles = [ f for f in listdir(path) if f.endswith(".tab")]
long_ts=[]
mode=sys.argv[1]
if mode=='-i':
    interject=[0]*200
    outputfile=sys.argv[2]
elif mode=='-n':
    outputfile=sys.argv[2]
else:
    print 'mode is unknown, valid: -i or -n.bye.'
    sys.exit()
for file_pitch in onlyFiles:
    #print file_pitch
    inputfile=path+'/'+file_pitch
    pitch_vec=get_vec(inputfile)
    long_ts.extend(pitch_vec)
    if mode=='-i':
        long_ts.extend(interject)
#sys.exit()
print 'total ts length:',len(long_ts)

open(outputfile,'w').close()
f=open(outputfile,'a')
for i in long_ts:
    f.write(str(i)+'\n')
f.close()
