from ngram_motifs_modules import *
import pickle,sys
#create a data set for classification of spurious vs others classes using complexity score
#by decision tree it helps us select a boundary optimalis

def get_comp_scores(comp_len,par,X,file_prefix,class_indexes,mk_path):
    #class_indexes should a list with three inner lists:linear,qlinear,nonlinear,from reading pickle files annotated three classes.
    linear,qlinear,nonlinear=class_indexes[0],class_indexes[1],class_indexes[2]
    linear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,linear,mk_path)
    qlinear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,qlinear,mk_path)
    nonlinear_ave_comp=multiple_average_complexity(comp_len,par,X,file_prefix,nonlinear,mk_path)
    return linear_ave_comp,qlinear_ave_comp,nonlinear_ave_comp


def get_TLC_scores(comp_len,par,X,file_prefix,class_indexes,mk_path,csv_file):
    linear,qlinear,nonlinear=class_indexes[0],class_indexes[1],class_indexes[2]
    linear_TLC=multi_motifs_TLC(comp_len,par,linear,X,csv_file,file_prefix,mk_path)
    qlinear_TLC=multi_motifs_TLC(comp_len,par,qlinear,X,csv_file,file_prefix,mk_path)
    nonlinear_TLC=multi_motifs_TLC(comp_len,par,nonlinear,X,csv_file,file_prefix,mk_path)
    return linear_TLC, qlinear_TLC, nonlinear_TLC


def gen_data_sets(comp_len,par,X,file_prefix,gt_file,mk_path,csv_file,outpath):
    ground_truth_dict=pickle.load(open(gt_file,'rb'))
    linear=ground_truth_dict['linear']
    qlinear=ground_truth_dict['qlinear']
    nonlinear=ground_truth_dict['nonlinear']
    class_indexes=[linear,qlinear,nonlinear]
    linear_ave_comp,qlinear_ave_comp,nonlinear_ave_comp=get_comp_scores(comp_len,par,X,file_prefix,class_indexes,mk_path)

    linear_TLC, qlinear_TLC, nonlinear_TLC=get_TLC_scores(comp_len,par,X,file_prefix,class_indexes,mk_path,csv_file)


    #one or two feature
    #2-class-1,3-class,2-class-2
    outputfiles=['comp_2cl1.csv','comp_3cl.csv','comp_2cl2.csv','comp_tlc_2cl1.csv','comp_tlc_3cl.csv','comp_tlc_2cl2.csv']
    #one feature:complexity, 2 class1
    print 'writing file 1'
    f=open(outpath+outputfiles[0],'w')
    f.write('complexity,class\n')
    f.close()
    f=open(outpath+outputfiles[0],'a')
    for i in linear_ave_comp:
        f.write(str(i)+",SP\n")
    for i in qlinear_ave_comp:
        f.write(str(i) + ",NS\n")
    for i in nonlinear_ave_comp:
        f.write(str(i) + ",NS\n")
    f.close()
    
    print 'writing file 2'
    #one feature:complexity, 3 class
    f=open(outpath+outputfiles[1],'w')
    f.write('complexity,class\n')
    f.close()
    f=open(outpath+outputfiles[1],'a')
    for i in linear_ave_comp:
        f.write(str(i)+",SP\n")
    for i in qlinear_ave_comp:
        f.write(str(i) + ",AMB\n")
    for i in nonlinear_ave_comp:
        f.write(str(i) + ",GD\n")
    f.close()

    print 'writing file 3'
    #one feature:complexity, 2 class2
    f=open(outpath+outputfiles[2],'w')
    f.write('complexity,class\n')
    f.close()
    f=open(outpath+outputfiles[2],'a')
    #this one doesn't have linear data, it is already pruned
    for i in qlinear_ave_comp:
        f.write(str(i) + ",AMB\n")
    for i in nonlinear_ave_comp:
        f.write(str(i) + ",GD\n")
    f.close()

    

    print 'writing file 4'
    #two features:complexity,TLC, 2 class1
    f=open(outpath+outputfiles[3],'w')
    f.write('complexity,TLC,class\n')
    f.close()
    f=open(outpath+outputfiles[3],'a')
    for i in range(len(linear_ave_comp)):
        f.write(str(linear_ave_comp[i])+ "," + str(linear_TLC[i]) +",SP\n")
    for i in range(len(qlinear_ave_comp)):
        f.write(str(qlinear_ave_comp[i])+ "," + str(qlinear_TLC[i]) +",NS\n")
    for i in range(len(nonlinear_ave_comp)):
        f.write(str(nonlinear_ave_comp[i])+ "," + str(nonlinear_TLC[i]) +",NS\n")
    f.close()


    print 'writing file 5'
    #two feature:complexity,TLC, 3 classes
    f=open(outpath+outputfiles[4],'w')
    f.write('complexity,TLC,class\n')
    f.close()
    f=open(outpath+outputfiles[4],'a')
    for i in range(len(linear_ave_comp)):
        f.write(str(linear_ave_comp[i])+ "," + str(linear_TLC[i]) +",SP\n")
    for i in range(len(qlinear_ave_comp)):
        f.write(str(qlinear_ave_comp[i])+ "," + str(qlinear_TLC[i]) +",AMB\n")
    for i in range(len(nonlinear_ave_comp)):
        f.write(str(nonlinear_ave_comp[i])+ "," + str(nonlinear_TLC[i]) +",GD\n")
    f.close()

    print 'writing file 6'
    #two feature:complexity,TLC, 2 class2
    f=open(outpath+outputfiles[5],'w')
    f.write('complexity,TLC,class\n')
    f.close()
    f=open(outpath+outputfiles[5],'a')
    #this one doesn't have linear data, it is already pruned
    for i in range(len(qlinear_ave_comp)):
        f.write(str(qlinear_ave_comp[i])+ "," + str(qlinear_TLC[i]) +",AMB\n")
    for i in range(len(nonlinear_ave_comp)):
        f.write(str(nonlinear_ave_comp[i])+ "," + str(nonlinear_TLC[i]) +",GD\n")
    f.close()


def main():
    N=sys.argv[1]
    comp_len=sys.argv[2]
    if N=='2' and comp_len=='100':
        par='52'
        X=2
        file_prefix='downsample_syl_2_meta_100_MK'
        csv_file='new_csv_data/downsample_syl_2_meta_100.csv'
        data_file='downsample_syl_2_meta_100_MK.txt'
        gt_file="bigram100p_gtruth.p"
        total_num_motifs=102
        mk_path='new_mk_data/'
        
        outpath='bigram_100p_train/'
        gen_data_sets(comp_len,par,X,file_prefix,gt_file,mk_path,csv_file,outpath)
    if N=='2' and comp_len=='200':
        file_prefix='downsample_syl_2_meta_200_MK'
        csv_file='csv_version/downsample_syl_2_meta_200.csv'
        data_file='mk_txt/downsample_syl_2_meta_200_MK.txt'
        gt_file="bigram200p_gtruth.p"
        total_num_motifs=70
        par='56'
        X=2
        mk_path='mk_txt/'        
        outpath='bigram_200p_train/'
        gen_data_sets(comp_len,par,X,file_prefix,gt_file,mk_path,csv_file,outpath)

if __name__ == '__main__':
    main()