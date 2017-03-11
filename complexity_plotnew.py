import numpy as np
import pylab as plt

def compute_complexity(ts):
    """compute complexity of a single TS"""
    #right now I don't need to normalized by length, since all subsequences considered from the same dataset should have the
    #same len, but keep in mind in the future
    return np.sqrt(np.sum((ts[i]-ts[i+1])**2 for i in range(len(ts)-1)))



# the best way to do this is to have an in-memory model of all subsequences and then write selected to new versions of files
#for running the mk_ng.exe

#read data file
def read_txt_data(data_file):
    f=open(data_file,'r').read().split('\n')
    all_txt_data=[]
    for line in f:
        if line=='':
            continue
        l=line.split(' ')
        l=[float(i) for i in l]
        all_txt_data.append(l)
    return all_txt_data

def read_csv_data_meta(data_file):
    f=open(data_file,'r').read().split('\n')
    all_csv_data=[]
    for line in f:
        if line=='':
            continue
        l=line.split(',')
        #l=[float(i) for i in l]
        all_csv_data.append(l)
    return all_csv_data


#read in the motif file, then select if you want the subsequences in this motif cluster to be removed and discarded.
            
def ind_rm(par,X,indexes,num_run):
    """get a list of indexes to be removed. all motif cluster files to be removed is stored in tbr/"""
    #the indexes argument is the indexes of the motif clusters, such as 'remove the first 5 clutsers', then indexes is [1,2,3,4,5]
    #notice it starts from 1 b/c this is how the motif clusters files are named
    all_indexes_tbr=[]
    for i in indexes:
        si=str(i)
        if num_run>1:
            m='new_mk_data/downsample_syl_2_meta_100_MKrm_sub_txt_%s_100_%s.0_%s.txt'%(par,X,si)
        elif num_run==1:
            m='new_mk_data/downsample_syl_2_meta_100_MK_txt_%s_100_%s.0_%s.txt'%(par,X,si)
        #get indexes of subseqs from one motif cluster
        this_indexes=inspect_motif(m,False)
        this_indexes=[int(j) for j in this_indexes]
        all_indexes_tbr.extend(this_indexes[:])
    return all_indexes_tbr

def remove_elements_by_ind(ori_list,indices):
    return [i for j, i in enumerate(ori_list) if j not in indices]

def write_to_newtxt(outfile,new_txt_data):
    f=open(outfile,'w').close()
    f=open(outfile,'a')
    for motif in new_txt_data:
        motif=[str(i) for i in motif]
        line=' '.join(motif)
        f.write(line+'\n')
        
    f.close()
    
def write_to_newcsv(outcsvfile,new_csv_data):
    f=open(outcsvfile,'w').close()
    f=open(outcsvfile,'a')
    for motif in new_csv_data:
        motif=[str(i) for i in motif]
        line=','.join(motif)
        f.write(line+'\n')
        
    f.close()
    
#run this process of removing the selected subsequences
def update_data(data_file,csv_file,num_run,X,indexes_tbr):
    all_txt_data=read_txt_data(data_file)
    all_csv_data=read_csv_data_meta(csv_file)
    all_ind_tbr=ind_rm(X,indexes_tbr,num_run)
    print 'number of subsequences to be removed:',len(all_ind_tbr)
    new_txt_data=remove_elements_by_ind(all_txt_data,all_ind_tbr)
    new_csv_data=remove_elements_by_ind(all_csv_data,all_ind_tbr)
    if data_file.endswith('rm_sub.txt'):
        outfile=data_file
    else:
        outfile=data_file.split('.')[0]+'rm_sub.txt'
    if csv_file.endswith('rm_sub.csv'):
        outcsvfile=csv_file
    else:
        outcsvfile=csv_file.split('.')[0]+'rm_sub.csv'
    write_to_newtxt(outfile,new_txt_data)
    write_to_newcsv(outcsvfile,new_csv_data)
    
    
    
    
def inspect_motif(motif_file,plott):
    f=open(motif_file,'r').read().split('\n')
    c=0
    if plott:
        plt.figure()
        print len(f)
    all_ind=[]
    
    for line in f:
        c+=1

        if line!='':
            #print c
            line=line.strip()
            ts=line.split(' ')[1:]
            ind=line.split(' ')[0]
            all_ind.append(ind)
            ts=[float(i) for i in ts]
            #print len(ts)
            if plott:
                plt.plot(ts)
                plt.title(motif_file)
    return all_ind

               
def plot_all_motifs(par,X,num_motif,file_prefix):
    for i in range(1,num_motif):
        si=str(i)
        m=file_prefix+'_txt_%s_100_%s.0_%s.txt'%(par,X,si)
        print m
        all_ind=inspect_motif(m,True)
        plot_originals(all_ind,file_prefix)
        
        



def inspect_motif(motif_file,plott):
    f=open(motif_file,'r').read().split('\n')
    c=0
    if plott:
        plt.figure()
        print len(f)
    all_ind=[]
    
    for line in f:
        c+=1

        if line!='':
            #print c
            line=line.strip()
            ts=line.split(' ')[1:]
            ind=line.split(' ')[0]
            all_ind.append(ind)
            ts=[float(i) for i in ts]
            #print len(ts)
            if plott:
                plt.plot(ts)
                plt.title(motif_file)
    return all_ind

def plot_originals(all_ind,file_prefix):
    plt.figure()
    file_name=file_prefix+'.csv'
    print 'original file:',file_name
    f=open(file_name,'r').read().split('\n')
    all_texts=''
    all_comp=[]
    all_tones=[]
    for ind in all_ind:
        line=f[int(ind)]
        l=line.split(',')
        data=l[:-4]
        tones,file_name,position=l[-4],l[-2],l[-1]
        all_tones.append(tones)
        text=','.join([tones,file_name,position])
        text+='\n'
        plt.plot(data)
        all_texts+=text
        data=[float(i) for i in data]
        comp_score=compute_complexity(data)
        all_comp.append(comp_score)
    plt.text(.1,-.4,all_texts)
    ave_score=np.mean(all_comp)
    TLC,sim=compute_TLC(all_tones)
    plt.title('mean complexity score:'+str(ave_score)+"|TLC:"+str(TLC))
                       
        
        
def plot_all_motifs_meta(par,X,num_motif,file_prefix,path='new_mk_data/'):
    for i in range(1,num_motif):
        si=str(i)
        #path could be 'new_mk_data' or if just in mk_ng directory, use ""
        m=path+ file_prefix + '_txt_%s_100_%s.0_%s.txt'%(par,X,si)
        print m
        all_ind=inspect_motif(m,True)
        file_prefix_csv=file_prefix.replace('_MK','')
        file_prefix_csv='new_csv_data/'+file_prefix_csv
        plot_originals(all_ind,file_prefix_csv)

        
        
        