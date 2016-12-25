#for each data file (like bigram 100p), generate a plot of all top motifs and their meta data info.
import matplotlib.pyplot as plt
import sys,re
from os import listdir


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
            pat_label=r',\d?\d,'
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






def main():
    #txt_file='mk_txt/downsample_syl_2_meta_100_MK.txt'
    #total_num=read_MK_file(txt_file)
    #csv_file='original_ver/downsample_syl_2_meta_100.csv'
    #total_ori=read_csv_ori_file(csv_file)
    path='mk_txt_test'
    ori_path='original_ver'
    onlyfiles = [ f for f in listdir(path) if f.endswith("_10_tuple.txt")]
    #print onlyfiles
    for file_name in onlyfiles:
        print file_name
        original_file=file_name.split('_MK_10_tuple')[0]+'.csv'
        input_file = path + "/" + file_name
        #first read in the tuple file to get dist and motif pairs index numbers,
        motif_tuples=read_tuple_file(input_file)
        motif_tuples_unique=get_unique_tuples(motif_tuples)
        #then read original file for pitch track and meta attributes
        numbers,attributes=read_csv_ori_file(ori_path+"/"+original_file)
        #plot the pairs by its index number and also put in the attributes to id where it came from
        

        #set up a plot matrix, then plot one by one for each motif pair
        #set this number
        num_per_row=1
        plot_name=file_name.split('.')[0]+'.png'
        plot_dir='plots'


        num_file=len(motif_tuples_unique)
        num_plot=num_file
        #plot num_per_row per row
        while num_plot%num_per_row!=0:
            num_plot+=1
        #plot a by b matrix
        b=num_per_row
        a=num_plot/b
        f, axarr = plt.subplots(a,b)
        

        
        print "num motifs:",len(motif_tuples_unique)
        for tp in motif_tuples_unique:
            dist=tp[0]
            pair=tp[1:]
            motif=[numbers[int(pair[0])],numbers[int(pair[1])]]
            i=j=0
            #print i,j
            if num_per_row==1:
                axarr[i].plot(motif[0])
                axarr[i].plot(motif[1])
            else:
                axarr[i, j].plot(motif[0])
                axarr[i, j].plot(motif[1])

            if j==b-1 or num_per_row==1:
                i+=1
                j=0
            else:
                j+=1
        f.savefig(plot_dir+'/'+plot_name)
        print 'saved pitch plots ' + plot_name





if __name__ == '__main__':
    main()
