import numpy as np
import pylab as plt
import random

def compute_complexity(ts):
    """compute complexity of a single TS"""
    #right now I don't need to normalized by length, since all subsequences considered from the same dataset should have the
    #same len, but keep in mind in the future
    return np.sqrt(np.sum((ts[i]-ts[i+1])**2 for i in range(len(ts)-1)))

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
            
def ind_rm(X,indexes,num_run):
    """get a list of indexes to be removed. all motif cluster files to be removed is stored in tbr/"""
    #the indexes argument is the indexes of the motif clusters, such as 'remove the first 5 clutsers', then indexes is [1,2,3,4,5]
    #notice it starts from 1 b/c this is how the motif clusters files are named
    all_indexes_tbr=[]
    for i in indexes:
        si=str(i)
        if num_run>1:
            m='new_mk_data/downsample_syl_2_meta_100_MKrm_sub_txt_0_100_%s.0_%s.txt'%(X,si)
        elif num_run==1:
            m='new_mk_data/downsample_syl_2_meta_100_MK_txt_0_100_%s.0_%s.txt'%(X,si)
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



               
def plot_all_motifs(X,num_motif,file_prefix):
    for i in range(1,num_motif):
        si=str(i)
        m=file_prefix+'_txt_0_100_%s.0_%s.txt'%(X,si)
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
    f=open(file_name,'r').read().split('\n')
    all_texts=''
    all_comp=[]
    for ind in all_ind:
        line=f[int(ind)]
        l=line.split(',')
        data=l[:-4]
        tones,file_name,position=l[-4],l[-2],l[-1]
        text=','.join([tones,file_name,position])
        text+='\n'
        plt.plot(data)
        all_texts+=text
        data=[float(i) for i in data]
        comp_score=compute_complexity(data)
        all_comp.append(comp_score)
    plt.text(.1,-.4,all_texts)
    ave_score=np.mean(all_comp)
    plt.title('mean complexity score:'+str(ave_score))
                       
        
        
def plot_all_motifs_meta(X,num_motif,file_prefix):
    for i in range(1,num_motif):
        si=str(i)
        m="new_mk_data/"+ file_prefix + '_txt_0_100_%s.0_%s.txt'%(X,si)
        print m
        all_ind=inspect_motif(m,True)
        file_prefix_csv=file_prefix.replace('_MK','')
        file_prefix_csv='new_csv_data/'+file_prefix_csv
        plot_originals(all_ind,file_prefix_csv)
        
        
def read_motif_file(motif_file):
    f=open(motif_file,'r').read().split('\n')
    motifs=[]
    all_inds=[]
    for line in f:
        if line!='':
            line=line.strip()
            ts=line.split(' ')[1:]
            ts=[float(i) for i in ts]
            ind=line.split(' ')[0]
            all_inds.append(ind)
            motifs.append(ts)
            ts=[float(i) for i in ts]
         
    return all_inds,motifs

def get_random_selected(bigram):
    f=open(bigram,'r').read().split('\n')
    #random.seed(298)
    selected=random.sample(f,200)
    real_scores=[]
    for line in selected:
        l=line.split(' ')
        l=[float(i) for i in l]
        l=np.array(l)
        l=(l-np.mean(l))/np.std(l)
        score=compute_complexity(l)
        real_scores.append(score)
    return real_scores
    #plt.figure()
    #plt.hist(spu_scores,bins=30,range=[0,2])
    #plt.title('complexity scores of 200 spurious subsequences')
    #plt.figure()
    #plt.hist(real_scores,bins=30,range=[0,2])
    #plt.title("complexity scores of 200 subsequences randomly sampled from corpus")
    



def gen_selected_scores(X,selected_motifs,file_prefix):
    """generate the complexity scores for the spurious data set of X=5 and k=30"""
    #if you want to select all motifs from 1 to 30, for instance, you just go selected_motifs=range(1,31)
    all_complexity_scores=[]
    for i in selected_motifs:
        si=str(i)
        m="new_mk_data/"+ file_prefix + '_txt_0_100_%s.0_%s.txt'%(X,si)
        all_inds,motifs=read_motif_file(m)
        for motif in motifs:
            complexity=compute_complexity(motif)
            all_complexity_scores.append(complexity)
    return all_complexity_scores

    
    
def plot_spu_real():
    #spurious scores
    spu_scores=gen_selected_scores(5,range(1,31),"downsample_syl_2_meta_100_MK")
     
    #random scores
    bigram='downsample_syl_2_meta_100_MK.txt'
    real_scores=get_random_selected(bigram)
    
    #ambiguous scores
    
    #plotting all scores
    data_zip=zip(spu_scores,real_scores)
    data_zip=np.array(data_zip)
    colors = ['tan', 'lime']
    plt.hist(data_zip, 30, normed=1, histtype='bar', color=colors, label=['spurious','random'],range=[0.3,2])
    plt.legend(prop={'size': 10})
    plt.title('Distribution of 200 spurious motifs, randomly sampled subsequences from corpus')
    plt.show()
    
    
    
def main():
    #the point here is that we will not use the original data to compute complexity scores, but use the normalized ts in the motif clusters files. 
    plt_spu_real()
    
if __name__ == '__main__':
    main()
