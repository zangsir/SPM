import numpy as np
from collections import defaultdict
import pylab as plt


def compute_complexity(ts):
    """compute complexity of a single TS"""
    #right now I don't need to normalized by length, since all subsequences considered from the same dataset should have the
    #same len, but keep in mind in the future
    return np.sqrt(np.sum((ts[i]-ts[i+1])**2 for i in range(len(ts)-1)))



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
            
def ind_rm(comp_len,par,X,indexes,num_run,file_prefix,mk_path):
    """get a list of indexes to be removed. all motif cluster files to be removed is stored in tbr/"""
    #the indexes argument is the indexes of the motif clusters, such as 'remove the first 5 clutsers', then indexes is [1,2,3,4,5]
    #notice it starts from 1 b/c this is how the motif clusters files are named
    all_indexes_tbr=[]
    for i in indexes:
        si=str(i)
        if num_run>1:
            m=mk_path + file_prefix + 'rm_sub_txt_%s_%s_%s.0_%s.txt'%(par,str(comp_len),X,si)
        elif num_run==1:
            m=mk_path + file_prefix + '_txt_%s_%s_%s.0_%s.txt'%(par,str(comp_len),X,si)
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
def update_data(comp_len,data_file,csv_file,num_run,X,indexes_tbr,file_prefix,mk_path):
    all_txt_data=read_txt_data(data_file)
    all_csv_data=read_csv_data_meta(csv_file)
    all_ind_tbr=ind_rm(comp_len,X,indexes_tbr,num_run,file_prefix,mk_path)
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
                       
        
        
def plot_all_motifs_meta(par,X,num_motif,file_prefix,length,csv_path,path='new_mk_data/'):
    #length: subsequence length, 100p, 200p, etc.
    for i in range(1,num_motif):
        si=str(i)
        subs_length=str(length)
        #path could be 'new_mk_data' or if just in mk_ng directory, use ""
        m=path+ file_prefix + '_txt_%s_%s_%s.0_%s.txt'%(par,subs_length,X,si)
        print m
        all_ind=inspect_motif(m,True)
        file_prefix_csv=file_prefix.replace('_MK','')
        file_prefix_csv=csv_path+file_prefix_csv
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
            ind=int(ind)
            all_inds.append(ind)
            motifs.append(ts)
            ts=[float(i) for i in ts]
         
    return all_inds,motifs


def gen_selected_scores(comp_len,par,X,selected_motifs,file_prefix,mk_path='new_mk_data/'):
    """generate the complexity scores(normalized) from the motif files directly"""
    #if you want to select all motifs from 1 to 30, for instance, you just go selected_motifs=range(1,31)
    all_complexity_scores=[]
    for i in selected_motifs:
        si=str(i)
        m=mk_path+ file_prefix + '_txt_%s_%s_%s.0_%s.txt'%(par,str(comp_len),X,si)
        all_inds,motifs=read_motif_file(m)
        for motif in motifs:
            complexity=compute_complexity(motif)
            all_complexity_scores.append(complexity)
    return all_complexity_scores

    
    
def plot_spu_real(selected_motifs,mk_path):
    #spurious scores
    spu_scores=gen_selected_scores('52',2,selected_motifs,"downsample_syl_2_meta_100_MK",mk_path)
     
    #random scores
    bigram='downsample_syl_2_meta_100_MK.txt'
    
    #ambiguous scores
    
    #plotting all scores
    data_zip=zip(spu_scores,real_scores)
    data_zip=np.array(data_zip)
    colors = ['tan', 'lime']
    plt.hist(data_zip, 30, normed=1, histtype='bar', color=colors, label=['spurious','random'],range=[0.3,2])
    plt.legend(prop={'size': 10})
    plt.title('Distribution of 200 spurious motifs, randomly sampled subsequences from corpus')
    plt.show()
    
def plot_three_classes(outfilename,score_1,score_2,score_3,class_labels,num_bins=20,range_x=[0,2]):
    plt.figure()
    data_zip=zip(score_1,score_2,score_3)
    data_zip=np.array(data_zip)
    colors = ['red', 'lime','blue']
    plt.hist(data_zip, num_bins, normed=1, histtype='bar', color=colors, label=class_labels,range=range_x)
    plt.legend(prop={'size': 10})
    #plt.title('Distribution of complexity scores from CMN corpus')
    #plt.show()
    plt.savefig(outfilename)
    
    
    
    
    

def equal_bin(a,b):
    if a==b:
        return 1
    else:
        return 0

def pairwise_TLC_score(l_1,l_2):
    assert len(l_1)==len(l_2)
    score=0
    for i in range(len(l_1)):
        score+=equal_bin(l_1[i],l_2[i])
    return score    

def max_score(input_len,len_label):
    """input_len=how many labels;N=len of each label"""    
    return len_label*(input_len * (input_len-1))/2
    
    
    
def get_comp_scores(comp_len,X,indexes_tbr,num_run,par,data_file,file_prefix,mk_path):    
    """get complexity scores from the original subsequences in new_mk_data/"""
    #X=2
    #indexes_tbr=motif_class_inds
    #num_run=1
    #get indexes of the subsequences found in motif clusters from the original data file 
    all_ind_tbr=ind_rm(comp_len,par,X,indexes_tbr,num_run,file_prefix,mk_path)
    #complexity scores of three classes
    all_txt_data=read_txt_data(data_file)
    scores=[]
    for i in all_ind_tbr:
        subs=all_txt_data[int(i)]
        complexity_score=compute_complexity(subs)
        scores.append(complexity_score)
    return scores



def get_tone_labels(all_inds,csv_file):
    all_labels=[]
    all_csv_data=read_csv_data_meta(csv_file)
    for i in all_inds:
        line=all_csv_data[i]
        label=line[-4]
        all_labels.append(label)
    return all_labels

def motif_clust_TLC(motif_cluster_file,csv_file):
    """get TLC score for one motif cluster.
    TLC is not a measure of one subsequence but a measure of a cluster"""
    #for each motif cluster, we need to compute a TLC score by extracting all of its members' 
    #tone labels
    #for each cluster, we extract all indexes of its members, then access those indexes in 
    #original csv file, compile a list of labels, to feed to compute TLC algorithm
    
    #get all indexes from motif cluster file
    all_inds,motifs=read_motif_file(motif_cluster_file)
    #get the tone labels of these index from original csv version file
    tone_labels=get_tone_labels(all_inds,csv_file)
    TLC,sim=compute_TLC(tone_labels)
    
    return TLC

def multi_motifs_TLC(comp_len,par,class_indx,X,csv_file,file_prefix,path='new_mk_data/'):
    """compute TLC scores for a list of motif clusters, input by index of motif cluster files"""
    #for example, class_indx can be all indexes from a x=2,k=200 motif files
    
    #for each motif cluster file given by the class_indx, get a cluster TLC score
    all_scores=[]
    for i in class_indx:
        si=str(i)
        motif_file=path+file_prefix + '_txt_%s_%s_%s.0_%s.txt'%(par,comp_len,X,si)
        #print motif_file
        score=motif_clust_TLC(motif_file,csv_file)
        all_scores.append(score)
    return all_scores

            
def average_complexity(motif_file):
    """compute average complexity for a motif cluster using normalized score"""
    all_mot=open(motif_file,'r').read().split('\n')
    all_comp=[]
    for line in all_mot:
        if line!='':
            l=line.strip().split(' ')
            #compute complexity score for one subsequence at a time
            data=[float(i) for i in l[1:]]
            complexity=compute_complexity(data)
            all_comp.append(complexity)
    return np.mean(all_comp)            


def TLC_by_complexity(comp_len,par,X,k,csv_file,file_prefix,path='new_mk_data/'):
    """in order to see the correlation of complexity and TLC we use this function to output all pairs of ave_comp,TLC scores 
    for each motif cluster"""
    #for ex, if there are 102 actual motif clusters from the current data set, we use k=103
    all_score_pairs=[]
    for i in range(1,k+1):
        si=str(i)
        motif_file=path+file_prefix + '_txt_%s_%s_%s.0_%s.txt'%(par,str(comp_len),X,si)
        TLC_score=motif_clust_TLC(motif_file,csv_file)
        ave_comp=average_complexity(motif_file)
        all_score_pairs.append((ave_comp,TLC_score))
    return all_score_pairs

def multiple_average_complexity(comp_len,par,X,file_prefix,indexes,path='new_mk_data/'):
    """given a list of indexes of motif cluster files of a particular class 
    (such as motif cluster 1,4,6..), return a list of average 
    complexity scores for all the motif cluster files in this class"""
    all_scores=[]
    for i in indexes:
        si=str(i)
        motif_file=path+file_prefix + '_txt_%s_%s_%s.0_%s.txt'%(par,str(comp_len),X,si)
        ave_comp=average_complexity(motif_file)
        all_scores.append(ave_comp)
    return all_scores


def compute_TLC(input_label):
    similarity = defaultdict(lambda:-1)
    total_score=0
    for i in range(len(input_label)):
        for j in range(len(input_label)):
            if similarity[(j,i)]!= -1 or i==j:
                continue
            similarity_ij=pairwise_TLC_score(input_label[i],input_label[j])
            similarity[(i,j)]=similarity_ij
            total_score+=similarity_ij
    return float(total_score)/max_score(len(input_label),len(input_label[0])),similarity



def plot_bigram_100p_ipynb_original_procedure():
    #bigram 100p ground truth
    bi_100p_gt_file = "bigram100p_gtruth.p"
    ground_truth_dict=pickle.load(open(bi_100p_gt_file,'rb'))
    linear=ground_truth_dict['linear']
    qlinear=ground_truth_dict['qlinear']
    nonlinear=ground_truth_dict['nonlinear']
    
    #plot normalized average complexity scores
    data_file='downsample_syl_2_meta_100_MK.txt'
    par='52'
    mk_path='new_mk_data/'
    linear_scores=get_comp_scores(2,linear,1,par,data_file,mk_path)
    qlinear_scores=get_comp_scores(2,qlinear,1,par,data_file,mk_path)
    nonlinear_scores=get_comp_scores(2,nonlinear,1,par,data_file,mk_path)
    
    # we also want the complexity scores of the normalized motifs in cluster
    linear_scores_norm=gen_selected_scores('52',2,linear,"downsample_syl_2_meta_100_MK",mk_path)
    qlinear_scores_norm=gen_selected_scores('52',2,qlinear,"downsample_syl_2_meta_100_MK",mk_path)
    nonlinear_scores_norm=gen_selected_scores('52',2,nonlinear,"downsample_syl_2_meta_100_MK",mk_path)
    #print len(linear_scores_norm),len(qlinear_scores_norm),len(nonlinear_scores_norm)
    
    #un-normed indie complexity scores
    plot_three_classes(linear_scores,qlinear_scores,nonlinear_scores,['linear','qlinear','nonlinear'],20,[0,0.55])
    
    #normed indie comp scores
    plot_three_classes(linear_scores_norm,qlinear_scores_norm,nonlinear_scores_norm,['linear','qlinear','nonlinear'],20,[0.3,1])
    
    #average complexity scores
    linear_ave_comp=multiple_average_complexity(par,X,file_prefix,linear)
    qlinear_ave_comp=multiple_average_complexity(par,X,file_prefix,qlinear)
    nonlinear_ave_comp=multiple_average_complexity(par,X,file_prefix,nonlinear)
    plot_three_classes(linear_ave_comp,qlinear_ave_comp,nonlinear_ave_comp,['linear','qlinear','nonlinear'],20,[0.37,0.8])
    #average boxplot
    plt.boxplot([linear_ave_comp,qlinear_ave_comp,nonlinear_ave_comp])
    plt.xticks([1, 2, 3], ['linear', 'q-linear', 'non-linear'])
    plt.title('boxplot of average complexity scores of normalized motif clusters')
      
    
        
    

    #TLC
    file_prefix='downsample_syl_2_meta_100_MK'
    csv_file='new_csv_data/downsample_syl_2_meta_100.csv'
    linear_TLC=multi_motifs_TLC('52',linear,2,csv_file,file_prefix)
    qlinear_TLC=multi_motifs_TLC('52',qlinear,2,csv_file,file_prefix)
    nonlinear_TLC=multi_motifs_TLC('52',nonlinear,2,csv_file,file_prefix)
        
    #motifs TLC - TLC is just about a motif clusters tone labels, so normalization doesn't matter 
    #class size in number of motif clusters: 43,19,40, 102 motif in total
    plot_three_classes(linear_TLC,qlinear_TLC,nonlinear_TLC,['linear','qlinear','nonlinear'],20,[0,1])
    
    
    
    
    
    #plot and calculate correlation
    file_prefix='downsample_syl_2_meta_100_MK'
    csv_file='new_csv_data/downsample_syl_2_meta_100.csv'
    all_score_pairs=TLC_by_complexity('52',2,102,csv_file,file_prefix)
    x=[k[0] for k in all_score_pairs]
    y=[k[1] for k in all_score_pairs]
    x=np.array(x)
    y=np.array(y)
    plt.plot(x,y,'x')
    m, b = np.polyfit(x, y, 1)
    
    plt.plot(x, m*x + b, '-')
    plt.xlabel('complexity score')
    plt.ylabel('TLC score')
    plt.title('linear regression line showing correlation between complexity and TLC')
    
    print 'correlation:',np.corrcoef(x,y)