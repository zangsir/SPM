from ngram_motifs_modules import *
import pickle
import sys






def plot_pooled_ave_comp(l,ql,nl,output_name):
    ave_comp_out="plots/"+output_name + "_ave_comp.pdf"
    print 'plotting average cmp...'
    plot_three_classes(ave_comp_out,l,ql,nl,['linear','qlinear','nonlinear'],20,[0,10])
    #average boxplot
    boxplot_ave_out="plots/"+output_name+'_ave_box.pdf'
    print 'plotting boxplot...'
    plt.figure()
    plt.boxplot([l,ql,nl])
    plt.xticks([1, 2, 3], ['linear', 'q-linear', 'non-linear'])
    plt.title('boxplot of average complexity scores of normalized motif clusters')
    plt.savefig(boxplot_ave_out)




def multiple_dataset_ave_comp_pool(data_list):
    """compute average_complexity_scores for all specified input files(e.g.bigram100p,trigram200p,etc put together) and return the accumulated scores of three classes"""
    #for each data file, we get three lists of scores, and then we pool together scores for the same class
    all_linear_ave_comp=[]
    all_qlinear_ave_comp=[]
    all_nonlinear_ave_comp=[]
    #input is a list of NgramData objects
    for d in data_list:
        linear_ave_comp,qlinear_ave_comp,nonlinear_ave_comp=ave_comps(d.comp_len,d.gt_file,d.par,d.X,d.file_prefix,d.mk_path)
        all_linear_ave_comp.extend(linear_ave_comp)
        all_qlinear_ave_comp.extend(qlinear_ave_comp)
        all_nonlinear_ave_comp.extend(nonlinear_ave_comp)
    return all_linear_ave_comp,all_qlinear_ave_comp,all_nonlinear_ave_comp




def ave_comps(comp_len,gt_file,par,X,file_prefix,mk_path):
    """compute average complexity scores of three classes for one data file, such as bigram200p"""
    linear,qlinear,nonlinear=get_ground_truth(gt_file)
    #average complexity scores
    linear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,linear,mk_path)
    qlinear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,qlinear,mk_path)
    nonlinear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,nonlinear,mk_path)
    return linear_ave_comp,qlinear_ave_comp,nonlinear_ave_comp


def TLC_one_dataset(comp_len,gt_file,par,X,file_prefix,csv_file,mk_path):
    """computes all TLC scores for all motif clusters of one dataset"""
    linear,qlinear,nonlinear=get_ground_truth(gt_file)
    linear_TLC=multi_motifs_TLC(comp_len,par,linear,X,csv_file,file_prefix,mk_path)
    qlinear_TLC=multi_motifs_TLC(comp_len,par,qlinear,X,csv_file,file_prefix,mk_path)
    nonlinear_TLC=multi_motifs_TLC(comp_len,par,nonlinear,X,csv_file,file_prefix,mk_path)
    return linear_TLC,qlinear_TLC,nonlinear_TLC


def multi_dataset_TLC(data_list):
    all_linear_TLC=[]
    all_qlinear_TLC=[]
    all_nonlinear_TLC=[]
    #input is a list of NgramData objects
    for d in data_list:
        linear_TLC,qlinear_TLC,nonlinear_TLC=TLC_one_dataset(d.comp_len,d.gt_file,d.par,d.X,d.file_prefix,d.csv_file,d.mk_path)
        all_linear_TLC.extend(linear_TLC)
        all_qlinear_TLC.extend(qlinear_TLC)
        all_nonlinear_TLC.extend(nonlinear_TLC)
    return all_linear_TLC,all_qlinear_TLC,all_nonlinear_TLC


def plot_pooled_TLC(linear_TLC,qlinear_TLC,nonlinear_TLC,output_name):
    print 'plotting TLC...'
    TLC_outname="plots/"+output_name + "_TLC.pdf"
    plot_three_classes(TLC_outname,linear_TLC,qlinear_TLC,nonlinear_TLC,['linear','qlinear','nonlinear'],20,[0,1])
    
    
def correlation_pooled_TbyC(x,y,output_name):
    x=np.array(x)
    y=np.array(y)
    plt.figure()
    print 'plotting correlation...'
    plt.plot(x,y,'x')
    m, b = np.polyfit(x, y, 1)
    TLC_corr_out="plots/"+output_name+"_corr.pdf"
    plt.plot(x, m*x + b, '-')
    plt.xlabel('complexity score')
    plt.ylabel('TLC score')
    plt.title('linear regression line showing correlation between complexity and TLC, correlation:'+str(np.corrcoef(x,y)))
    plt.savefig(TLC_corr_out)
    print 'correlation:',np.corrcoef(x,y)



def main():
    #mk_path,N,comp_len,par,X,file_prefix,data_file,csv_file,gt_file,total_num_motifs,num_run
    bigram_200p=NgramData('mk_txt/',2,200,'56',2,'downsample_syl_2_meta_200_MK','mk_txt/downsample_syl_2_meta_200_MK.txt','csv_version/downsample_syl_2_meta_200.csv',"bigram200p_gtruth.p",70,1)
    bigram_100p=NgramData('new_mk_data/',2,100,'52',2,'downsample_syl_2_meta_100_MK','mk_txt/downsample_syl_2_meta_100_MK.txt','csv_version/downsample_syl_2_meta_100.csv',"bigram100p_gtruth.p",102,1)
    trigram_200p=NgramData('mk_txt/',3,200,'0',2,'downsample_syl_3_meta_200_MK','mk_txt/downsample_syl_3_meta_200_MK.txt','csv_version/downsample_syl_3_meta_200.csv',"trigram200p_gtruth.p",46,1)
    trigram_300p=NgramData('mk_txt/',3,300,'2115404940',2,'downsample_syl_3_meta_300_MK','mk_txt/downsample_syl_3_meta_300_MK.txt','csv_version/downsample_syl_3_meta_300.csv',"trigram300p_gtruth.p",38,1)
    data_list=[bigram_100p,bigram_200p,trigram_200p,trigram_300p]
    l,ql,nl=multiple_dataset_ave_comp_pool(data_list)
    output_name='pooled'
    plot_pooled_ave_comp(l,ql,nl,output_name)
    l_tlc,ql_tlc,nl_tlc=multi_dataset_TLC(data_list)
    plot_pooled_TLC(l_tlc,ql_tlc,nl_tlc,output_name)
    x_comp=l+ql+nl
    y_tlc=l_tlc+ql_tlc+nl_tlc
    correlation_pooled_TbyC(x_comp,y_tlc,output_name)



if __name__ == '__main__':
    main()