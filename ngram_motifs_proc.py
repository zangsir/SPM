from ngram_motifs_modules import *
import pickle
import sys


def plot_anygram(mk_path,N,comp_len,par,X,file_prefix,data_file,csv_file,gt_file,total_num_motifs,TLC_switch,num_run=1):
    """before we have written specifically for bigram plots, but here we generalize to any gram, any len data"""
    
    output_name=str(N)+"_gram_"+str(comp_len)+"p"
    ground_truth_dict=pickle.load(open(gt_file,'rb'))
    linear=ground_truth_dict['linear']
    qlinear=ground_truth_dict['qlinear']
    nonlinear=ground_truth_dict['nonlinear']
    
    #plot normalized average complexity scores
    linear_scores=get_comp_scores(comp_len,X,linear,num_run,par,data_file,file_prefix,mk_path)
    qlinear_scores=get_comp_scores(comp_len,X,qlinear,num_run,par,data_file,file_prefix,mk_path)
    nonlinear_scores=get_comp_scores(comp_len,X,nonlinear,num_run,par,data_file,file_prefix,mk_path)
    linear_scores_norm=gen_selected_scores(comp_len,par,X,linear,file_prefix,mk_path)
    qlinear_scores_norm=gen_selected_scores(comp_len,par,X,qlinear,file_prefix,mk_path)
    nonlinear_scores_norm=gen_selected_scores(comp_len,par,X,nonlinear,file_prefix,mk_path)
    
    print 'plotting unnorm comp...'
    #un-normed indie complexity scores
    indie_unnorm_comp_out="plots/"+output_name + '_indie_unnorm_comp.pdf'
    plot_three_classes(indie_unnorm_comp_out, linear_scores, qlinear_scores, nonlinear_scores, ['linear','qlinear','nonlinear'], 20, [0,10])
    
    #normed indie comp scores
    print 'plotting normed cpm...'
    indie_norm_comp_out="plots/"+output_name + '_indie_norm_comp.pdf'
    plot_three_classes(indie_norm_comp_out, linear_scores_norm, qlinear_scores_norm, nonlinear_scores_norm,['linear','qlinear','nonlinear'],20,[0,10])
    
    #average complexity scores
    #linear_ave_comp is all the ave_comp scores pooled for this class in this data file
    linear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,linear,mk_path)
    qlinear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,qlinear,mk_path)
    nonlinear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,nonlinear,mk_path)
    #print 'linear ave comp:',linear_ave_comp
    #print 'qlinear ave comp:', qlinear_ave_comp
    #print 'nonlinear ave comp:',nonlinear_ave_comp

    ave_comp_out="plots/"+output_name + "_ave_comp.pdf"
    print 'plotting average cmp...'
    plot_three_classes(ave_comp_out,linear_ave_comp,qlinear_ave_comp,nonlinear_ave_comp,['linear','qlinear','nonlinear'],20,[0,10])
    #average boxplot
    boxplot_ave_out="plots/"+output_name+'_ave_box.pdf'
    print 'plotting boxplot...'
    plt.figure()
    plt.boxplot([linear_ave_comp,qlinear_ave_comp,nonlinear_ave_comp])
    plt.xticks([1, 2, 3], ['linear', 'q-linear', 'non-linear'])
    plt.title('boxplot of average complexity scores of normalized motif clusters')
    plt.savefig(boxplot_ave_out)

    
    
    #TLC
    if not TLC_switch:
        sys.exit()
    #file_prefix='downsample_syl_2_meta_100_MK'
    #csv_file='new_csv_data/downsample_syl_2_meta_100.csv'
    linear_TLC=multi_motifs_TLC(comp_len,par,linear,X,csv_file,file_prefix,mk_path)
    qlinear_TLC=multi_motifs_TLC(comp_len,par,qlinear,X,csv_file,file_prefix,mk_path)
    nonlinear_TLC=multi_motifs_TLC(comp_len,par,nonlinear,X,csv_file,file_prefix,mk_path)
    print 'plotting TLC...'
    #print 'nonlinear TLC scores:',nonlinear_TLC
    #motifs TLC - TLC is just about a motif clusters tone labels, so normalization doesn't matter 
    #class size in number of motif clusters: 43,19,40, 102 motif in total
    TLC_out="plots/"+output_name + "_TLC.pdf"
    plot_three_classes(TLC_out,linear_TLC,qlinear_TLC,nonlinear_TLC,['linear','qlinear','nonlinear'],20,[0,1])
    
    
    
    
    
    
    #plot and calculate correlation
    #file_prefix='downsample_syl_2_meta_100_MK'
    #csv_file='new_csv_data/downsample_syl_2_meta_100.csv'
    all_score_pairs=TLC_by_complexity(comp_len,par,X,total_num_motifs,csv_file,file_prefix,mk_path)
    x=[k[0] for k in all_score_pairs]
    y=[k[1] for k in all_score_pairs]
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
    plt.title('linear regression line showing correlation between complexity and TLC')
    plt.savefig(TLC_corr_out)
    print 'correlation:',np.corrcoef(x,y)
    



def plot_controller(N,comp_len,TLC_switch):
    if N==2 and comp_len==100:
        file_prefix='downsample_syl_2_meta_100_MK'
        csv_file='new_csv_data/downsample_syl_2_meta_100.csv'
        data_file='downsample_syl_2_meta_100_MK.txt'
        gt_file="bigram100p_gtruth.p"
        total_num_motifs=102
        mk_path='new_mk_data/'
        plot_anygram(mk_path,N,comp_len,"52",2,"downsample_syl_2_meta_100_MK",data_file,csv_file,gt_file,total_num_motifs,TLC_switch)
    if N==2 and comp_len==200:
        file_prefix='downsample_syl_2_meta_200_MK'
        csv_file='csv_version/downsample_syl_2_meta_200.csv'
        data_file='mk_txt/downsample_syl_2_meta_200_MK.txt'
        gt_file="bigram200p_gtruth.p"
        total_num_motifs=70
        par='56'
        X=2
        mk_path='mk_txt/'
        plot_anygram(mk_path,N,comp_len,par,X,file_prefix,data_file,csv_file,gt_file,total_num_motifs,TLC_switch)

    if N==3 and comp_len==200:
        file_prefix='downsample_syl_3_meta_200_MK'
        csv_file='csv_version/downsample_syl_3_meta_200.csv'
        data_file='mk_txt/downsample_syl_3_meta_200_MK.txt'
        gt_file="trigram200p_gtruth.p"
        total_num_motifs=46
        par='0'
        X=2
        mk_path='mk_txt/'
        plot_anygram(mk_path,N,comp_len,par,X,file_prefix,data_file,csv_file,gt_file,total_num_motifs,TLC_switch)

    if N==3 and comp_len==300:
        file_prefix='downsample_syl_3_meta_300_MK'
        csv_file='csv_version/downsample_syl_3_meta_300.csv'
        data_file='mk_txt/downsample_syl_3_meta_300_MK.txt'
        gt_file="trigram300p_gtruth.p"
        total_num_motifs=38
        par='2115404940'
        X=2
        mk_path='mk_txt/'
        plot_anygram(mk_path,N,comp_len,par,X,file_prefix,data_file,csv_file,gt_file,total_num_motifs,TLC_switch)






def main():
    # I thought of using mode to either run this script by supplying command line args or supply everything within the script. 
    # but right now it seems the command line args would be too many and too long. Let's not do it now.
    # but I don't want to run all parts on all data every time, there should be an easy way to control which data set to run on. 
    # perhaps we could define it in terms of data, for ex, "bi 100" could mean run on the bigram 100p data set. 

    N=sys.argv[1]
    comp_len=sys.argv[2]
    print 'len(argv):',len(sys.argv)
    if len(sys.argv)>3:
        TLC_switch=bool(sys.argv[3])#if this is off, we don't do TLC, since it is time consuming
    else:
        TLC_switch=True
    #total_num_motifs=sys.argv[3]#how many true motif clusters among the top 200 motifs
    plot_controller(int(N),int(comp_len),TLC_switch)

if __name__ == '__main__':
    main()