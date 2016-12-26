#for each data file (like bigram 100p), generate a plot of all top motifs and their meta data info.
import matplotlib.pyplot as plt
import sys,re
from os import listdir
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os

def get_attributes(index_array):
    #get the attributes for a pair of motifs, e.g.
    all_attr=[]
    for idx in index_array:
        print total_ori[idx][-4:]
        all_attr.append(total_ori[idx][-4:])
    return all_attr


#pair=[8617,52211]
def peek(pair):
    #f, axarr = plt.subplots(1,2)
    #axarr[0, 0].plot(total_num[pair[1]])
    #axarr[0, 1].plot(total_num[pair[0]])
    plt.plot(total_num[pair[0]],'r')
    plt.plot(total_num[pair[1]],'b')
    plt.show()
    all_attr=get_attributes(pair)


#see original csv file and if they match with altered file

def read_MK_file(inputfile):
    #numbers only each line
    if inputfile.endswith('.csv'):
        sep=','
    elif inputfile.endswith('.txt'):
        sep=' '
    f=open(inputfile,'r').read().split('\n')
    total=[]
    for k in range(len(f)):
        line=f[k]
        #print k
        if line!='':
            l=line.split(sep)
            l=[float(i) for i in l]
            total.append(l)
    return total


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


def read_tuple_file(tuple_file):
    f=open(tuple_file,'r').read().split('\n')
    total=[]
    for line in f[1:]:
        if line!='':
            l=line.split(',')
            total.append(l)
    return total

def get_unique_tuples(tuples_list):
    seen=[]
    unique=[]
    for i in tuples_list:
        if set(i) not in seen:
            seen.append(set(i))
            unique.append(i)
    return unique

def plot_multi_page(data,dists,attrs,outplotname):
    # The PDF document
    pdf_pages = PdfPages(outplotname)
     
    # Generate the pages
    nb_plots = len(data)
    nb_plots_per_page = 5
    nb_pages = int(np.ceil(nb_plots / float(nb_plots_per_page)))
    grid_size = (nb_plots_per_page, 1)
     
    for i, samples in enumerate(data):
        # Create a figure instance (ie. a new page) if needed
        if i % nb_plots_per_page == 0:
            fig = plt.figure(figsize=(8.27, 11.69), dpi=100)
        tones=attrs[i][0][0] + "(red)|" + attrs[i][1][0]
        #print tones
        # Plot stuffs !
        plt.subplot2grid(grid_size, (i % nb_plots_per_page, 0))
        plt.plot(samples[0],'r')
        plt.plot(samples[1])
        plt.title(str(i) + ","+ str(dists[i]) + ",tones: " + tones)


        # Close the page if needed
        if (i + 1) % nb_plots_per_page == 0 or (i + 1) == nb_plots:
            plt.tight_layout()
            pdf_pages.savefig(fig)
     
    # Write the PDF document to the disk
    pdf_pages.close()




def main():
    #txt_file='mk_txt/downsample_syl_2_meta_100_MK.txt'
    #total_num=read_MK_file(txt_file)
    #csv_file='original_ver/downsample_syl_2_meta_100.csv'
    #total_ori=read_csv_ori_file(csv_file)
    path='mk_txt'
    ori_path='original_ver'
    onlyfiles = [ f for f in listdir(path) if f.endswith("_10_tuple.txt")]
    #print onlyfiles
    for file_name in onlyfiles:
        print "============"+file_name
        firstname=file_name.split('.')[0]
        outplotname='plots/'+firstname+'.pdf'
        original_file=file_name.split('_MK_10_tuple')[0]+'.csv'
        if os.path.isfile(outplotname):
            continue
        input_file = path + "/" + file_name
        #first read in the tuple file to get dist and motif pairs index numbers,
        motif_tuples=read_tuple_file(input_file)
        motif_tuples_unique=get_unique_tuples(motif_tuples)
        
        
        attr_pickle_file='pickle/'+firstname+'_attr.npy'
        data_pickle_file='pickle/'+firstname+'_data.npy'
        dist_pickle_file='pickle/'+firstname+'_dist.npy'


        #then read original file for pitch track and meta attributes
        numbers,attributes=read_csv_ori_file(ori_path+"/"+original_file)
        #plot the pairs by its index number and also put in the attributes to id where it came from
        
        print "num motifs:",len(motif_tuples_unique)
        if os.path.isfile(attr_pickle_file):
            print 'loading saved data objects...'
            all_attr=np.load(attr_pickle_file)
            all_data=np.load(data_pickle_file)
            all_dist=np.load(dist_pickle_file)    
        else:
            print 'extracting and pickling data objects...'
            all_data=[]
            all_dist=[]
            all_attr=[]
            for tp in motif_tuples_unique:
                dist=tp[0]
                pair=tp[1:]
                motif_pair=[numbers[int(pair[0])],numbers[int(pair[1])]]
                attr_pair=[attributes[int(pair[0])],attributes[int(pair[1])]]
                all_data.append(motif_pair)
                all_dist.append(dist)
                all_attr.append(attr_pair)
            np.save(data_pickle_file, all_data)
            np.save(attr_pickle_file, all_attr)
            np.save(dist_pickle_file, all_dist)
        #print data[4],len(data)
        #sys.exit()
        plot_multi_page(all_data,all_dist,all_attr,outplotname)
            





if __name__ == '__main__':
    main()
