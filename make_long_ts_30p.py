from os import listdir
import sys


mode=sys.argv[1]
if mode=='-i':
    interject=[0]*200

sent_path = 'syl_csv_norm_whole/'
onlyfiles = [ f for f in listdir(sent_path) if f.endswith(".csv")]
#print onlyfiles
lts=[]
for file_name in onlyfiles:
    input_file=sent_path+file_name
    f=open(input_file,'r').read().split('\n')
    for line in f:
    	if line!='':
    		data=line.split(',')[:-2]
    		data=[float(i) for i in data]
    		lts.extend(data)
if mode=='-i':
    outputfile='all_spk_lts_30p_interj.txt'
elif mode=='-n':
    outputfile='all_spk_lts_30p.txt'

print 'total ts length:',len(lts)

open(outputfile,'w').close()
f=open(outputfile,'a')
for i in lts:
    f.write(str(i)+'\n')
f.close()

