from ngram_motifs_modules import *
import numpy as np
import sys,pickle

def get_quantile(number,q_1,q_2,q_3):
    if number<q_1:
        return 'q1'
    elif number>q_1 and number<q_2:
        return 'q2'
    elif number>q_2 and number<q_3:
        return 'q3'
    else:
        return 'q4'


def get_label(ind,l,ql,nl):
    if ind in l:
        return 'linear'
    elif ind in ql:
        return 'qlinear'
    elif ind in nl:
        return 'nonlinear'


def gen_dataset(gt_file):
    linear,qlinear,nonlinear=get_ground_truth(gt_file)
    all_inds=linear+qlinear+nonlinear
    q_1 = np.percentile(all_inds, 25)
    q_2 = np.percentile(all_inds, 50)
    q_3 = np.percentile(all_inds, 75)
    dataset=[]
    for i in all_inds:
        quantile=get_quantile(i,q_1,q_2,q_3)
        class_label=get_label(i,linear,qlinear,nonlinear)
        this_ind=[str(i),quantile,class_label]
        dataset.append(this_ind)
    return dataset



def main():
    gt_file=sys.argv[1]
    dataset=gen_dataset(gt_file)
    print 'rank,quantile,class'
    for i in dataset:
        print ','.join(i)

if __name__ == '__main__':
    main()

