#take downsampled as input, output number only versions.

import sys

input_file = sys.argv[1]
comp_len = input_file.split('.')[0].split('_')[-1]
comp_len = int(comp_len)
    

out_file=input_file.split('.')[0] + "_MK.csv"
print 'output file:',out_file
f=open(input_file, 'r').read().split('\n')
total_out=[]
for line in f:
    if line!='':
        if input_file.startswith('downsample_syl'):#whole unigram or ngrams
            l=line.split(',')[:-4]
        elif input_file.startswith('downsample_1_'):#voiced unigram
            l=line.split(',')[:-3]
        assert(len(l)==comp_len)
        total_out.append(l)
g=open(out_file,'w').close()
g=open(out_file,'a')

for line in total_out:
    l=",".join(line)
    g.write(l+'\n')
g.close()
