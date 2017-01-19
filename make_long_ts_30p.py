from os import listdir
import sys


mode=sys.argv[1]
if mode=='-i':
    interject=[0]*200

#print onlyfiles
lts=[]
input_file='MK_data/csv_version/downsample_syl_whole_meta_30.csv'
f=open(input_file,'r').read().split('\n')
for line in f:
    if line!='':
        data_line=line.split(',')
        data=data_line[:-4]
        data=[float(i) for i in data]
        lts.extend(data)
        meta_pos=data_line[-1]
        if mode=='-i':
        	if meta_pos=='end':
        		lts.extend(interject)


#outfile name
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

