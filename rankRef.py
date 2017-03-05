from ngram_motifs_modules import *
import sys
import subprocess
import re
from os import listdir

#you must at least run MK once before you run this script. Otherwise, you don't know in advance what the file names are for the derived motif cluster files, especially the first number, there is no way of knowing in advance. Therefore we need to take the output of MK as input to this script and also supply that number in command line args.

def run_MK(path,input_file,X,k):
    print 'running MK'
    num_ts=str(get_num_of_lines(path,input_file))
    len_ts=input_file.split('_MK')[0].split('_')[-1]
    args='mk_ng.exe %s%s %s %s %s %s 10 1' %(path,input_file,num_ts,len_ts,X,k)
    print args
    #sys.exit()
    results=subprocess.check_output(args, shell=True)
    print results

def get_num_of_lines(path,input_file):
    input_full=path+input_file
    f=open(input_full,'r').read().split('\n')
    c=0
    for line in f:
        c+=1
    return c    

def get_all_motif_files(data_path,data_file):
    #this should return a list of all distinct motif files
    #first run MK
    #then we get all these motif cluster files
    X,k=2,200
    run_MK(data_path,data_file,X,k)
    
    #get the file names
    file_start=data_file.replace('.','_')
    onlyfiles = [ f for f in listdir(dir) if f.startswith(file_start)]
    print onlyfiles
    num_distinct_motifs=get_distinct_motifs(onlyfiles)
    return onlyfiles[:num_distinct_motifs]

    



def get_distinct_motifs_old(par,X,path,file_prefix,comp_len,k=200):
    """get number of distinct motif cluster files"""
    for i in range(1,k):
        
        si_this=str(i)
        si_next=str(i+1)
        this_file=path+file_prefix+'_txt_%s_%s_%s.0_%s.txt'%(par,comp_len,X,si_this)
        next_file=path+file_prefix+'_txt_%s_%s_%s.0_%s.txt'%(par,comp_len,X,si_next)
        #print this_file
        this_inds=inspect_motif(this_file)
        next_inds=inspect_motif(next_file)
        if this_inds==next_inds:
            return i
    return -1
        

def get_distinct_motifs(data_files_list):
    """get number of distinct motif cluster files"""
    for i in range(len(data_files_list)-1):
        this_file=data_files_list[i]
        next_file=data_files_list[i+1]
        
        #print this_file
        this_inds=inspect_motif(this_file)
        next_inds=inspect_motif(next_file)
        if this_inds==next_inds:
            return i
    return -1

def get_final_rank(motif_clusters):
    #in the final iteration, take all motif clusters (presumbly no linear classes) and classify them using 2C2 and produce a final ranking.
    pass



#this function is supposed to take all 200 motif clusters and then sort out their class. From a data object perspective,all motif clusters derived from running MK on a ngram data file will have the same field values except for the final 'i', and this is exactly what the class NgramData is designed for. Note that it is called "NgramData", one data file covers all the motif clusters discovered from it. so using the data object is perfect here.
#this takes one single argument because all motif clusters are derived from this one data file.
def iter_prune(data_file):
    spurious=True
    all_inds_rm=[]# we will need to remove indie subsequences one by one, so that the linear objects are deleted from db
    
    #idea: if you put one data file in one directory, then after you run MK, simply get all files in the same directory that begins with the predictable string of file name, and you can get the list of all motif cluster files, and you can refer to any one of them by index. It seems like this idea is simpler and could work in place of the complicated data object with many attributes and par that cannot be known before hand.
    #we need a clf to classify at run time and we need to extract features at runtime. (well, just complexities?)
    while spurious==True:
        #in this step you're supposed to re-run MK and get all the new motif cluster files
        motif_clusters=get_all_motif_files(data_path)
        for mc in motif_clusters:
            #each time process one motif cluster, classify it
            #load a model
            clf_2C1=pickle.load(open('model2c1.pkl','r'))
            clf_2C2=pickle.load(open('model2c2.pkl','r'))
            #extract features so we can classify
            complexity=average_complexity(mc)
            TLC=motif_clust_TLC(motif_cluster_file,csv_file)
            #are you using one feature or two?
            data=[[complexity,TLC]]
            y_pred=clf_2C1.predict(data)
            #we are making a prediction for one cluster as a whole, not indie members.
            if y_pred=="SP":
                this_indexes=inspect_motif(m,False)
                this_indexes=[int(j) for j in this_indexes]
                all_inds_rm.extend(this_indexes)
        if len(all_inds_rm)!=0:
            update_data()
        else:
            spurious=False
    #this is supposed to be a function to go through all final motif clusters, classify them, then rank them, return the rank by index and plot each cluster for evaluation (human) and then compute MAP score.
    new_rank=get_final_rank(motif_clusters)   
