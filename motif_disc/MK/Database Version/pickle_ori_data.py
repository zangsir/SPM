import matplotlib.pyplot as plt
import sys,re
from os import listdir
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os

def read_csv_ori_file(csv_file):
    #each line has numbers and string attributes
    f=open(csv_file,'r').read().split('\n')
    all_attributes=[]
    all_pitch=[]
    for k in range(len(f)):
        line=f[k]
        #print k
        if line!='':
            #l=line.split(',')
            #get numbers and get attributes
            pat_label=r',\d+,'
            m=re.search(pat_label,line)
            num_end=m.start()
            numbers=line[:num_end]
            attributes=line[num_end+1:]
            num_list=numbers.split(',')
            attr_list=attributes.split(',')
            fl_num=[float(i) for i in num_list]
            all_pitch.append(fl_num)
            all_attributes.append(attr_list)
    return all_pitch,all_attributes


def main():
    
    ori_path='original_ver'
    onlyfiles = [ f for f in listdir(ori_path) if f.endswith(".csv")]
    #print onlyfiles
    for file_name in onlyfiles:
        original_file=ori_path+'/'+file_name
        print "============"+file_name
        outfile_num=original_file.split('.')[0]+'_data.npy'
        outfile_attr=original_file.split('.')[0]+'_attr.npy'
        print "writing to..." + outfile_attr + " , " + outfile_num
        numbers,attributes=read_csv_ori_file(original_file)
        np.save(outfile_num,numbers)
        np.save(outfile_attr,attributes)
        
        
        
        


if __name__ == '__main__':
    main()