#take downsampled as input, output number only versions.

import sys
from os import listdir
import os

path = sys.argv[1]

onlyfiles = [ f for f in listdir(path) if f.endswith("0.csv")]
#print onlyfiles
for file_name in onlyfiles:
    print file_name
    input_file = path + "/" + file_name

    comp_len = file_name.split('.')[0].split('_')[-1]
    print 'comp len:',comp_len
    comp_len = int(comp_len)
    out_file=input_file.split('.')[0] + "_MK.csv"
    if os.path.isfile(out_file):
        print 'file exists:',out_file
        continue
    print 'output file:',out_file
    f=open(input_file, 'r').read().split('\n')
    total_out=[]
    for line in f:
        if line!='':
            if 'voiced' in file_name:#whole unigram or ngrams
                l=line.split(',')[:-3]
            else:#voiced unigram
                l=line.split(',')[:-4]
            assert(len(l)==comp_len)
            total_out.append(l)
    g=open(out_file,'w').close()
    g=open(out_file,'a')

    for line in total_out:
        l=",".join(line)
        g.write(l+'\n')
    g.close()
