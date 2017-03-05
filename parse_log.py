import re
from collections import defaultdict



def print_latex_table(log_file):
    splitter='++++++++++++++++++++++++++++++++++++++\n'
    f=open(log_file,'r').read().split(splitter)
    total_dict=defaultdict(dict)
    for line in f:

        if line!='':
            l=line.split('\n')
            path=l[0].split('/')[0]
            file=l[0].split('/')[1].split('.')[0]
            value=str(round(float(l[2]),2))+'/'+str(round(float(l[-3]),2))
            total_dict[path][file]=value

            #print "{:.2f}".format(float(l[2]))+'/'+"{:.2f}".format(float(l[-3]))
    #print total_dict
    a='2C1 & 2C2 & 3C & ' *5 
    header=a[:-2]+ '\\\\'

    single_feature=''
    double_feature=''
    keys=[]
    for k in total_dict:
        #keys.append(k)
        print k
        print total_dict[k]['comp_2cl1'] + " & " + total_dict[k]['comp_2cl2'] + ' & ' + total_dict[k]['comp_3cl'] + '\\\\'
        print total_dict[k]['comp_tlc_2cl1'] + " & " + total_dict[k]['comp_tlc_2cl2'] + ' & ' + total_dict[k]['comp_tlc_3cl'] + '\\\\'

    keys_str=' & '.join(keys)
    #print keys_str + '\\\\'
    #print header
    #print single_feature[:-2] + '\\\\'
    #print double_feature[:-2]




def main():
    BWK='train_data_BWK/classification_log_BWK.txt'
    LSSE='train_data_LSSE/classification_log_LSSE.txt'
    print_latex_table(BWK)
    print "==============="
    print_latex_table(LSSE)


if __name__ == '__main__':
    main()