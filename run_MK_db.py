#extract dist, ts1, ts2 tuples from MK db version output file
#mk_d.exe d.txt 1000 1024 10 1
# mk_d.exe mk_txt\downsample_syl_2_meta_100_MK.txt 88828 100 100 1 >> mk_output.txt
import sys
import subprocess
import re
from os import listdir


def run_MK_db(path, input_file, num_iter):
    all_log=[]
    for i in range(num_iter):
        num_ts=str(get_num_of_lines(path,input_file))
        #output_file=input_file.split('.')[0]+'_log.txt'
        num_ref='100'
        len_ts=input_file.split('_MK')[0].split('_')[-1]
        args='mk_d.exe %s/%s %s %s %s 1' %(path,input_file,num_ts,len_ts,num_ref)
        print i,args
        #sys.exit()
        results=subprocess.check_output(args, shell=True)
        all_log.append(results)
    return all_log
    

def get_num_of_lines(path,input_file):
    input_full=path+'/'+input_file
    f=open(input_full,'r').read().split('\n')
    c=0
    for line in f:
        c+=1
    return c            

def extract_tuples(log_file):
    g=open(log_file,'r').read().split('\n')
    outfile=log_file.split('_log')[0]+'_tuple.txt'

    dist_pat=r'\d*\.\d+'
    dist_pair=r'\d+ , \d+'
    groups=[]
    for line in g:
        this_group=[]
        if line!="":
            if line.startswith('New best-so-far'): 
                m=re.search(dist_pat,line)
                n=re.search(dist_pair,line)
                if m:
                    this_group.append(float(m.group()))
                if n:
                    this_group.append((int(n.group().split(',')[0])))
                    this_group.append((int(n.group().split(',')[1])))
                groups.append(this_group)                      
            #if line.startswith("Number of Time Series"):
             #   print "\n=============\n"

    sort_groups=sorted(groups,key=lambda x: x[0])       

    #outfile='MK_MotifPairs_bigram_100.csv'
    f=open(outfile,'w')
    f.write('distance,ts1,ts2\n')
    f.close()
    f=open(outfile,'a')
    for run in sort_groups:
        run_float=[str(i) for i in run]
        line=','.join(run_float)
        f.write(line+'\n')
    f.close()
    print 'written to motifs tuple file:', outfile
    
    
    
def main():
    #input_file='downsample_syl_2_meta_100_MK.txt'
    num_iter=int(sys.argv[1])
    
    path='mk_txt'
    onlyfiles = [ f for f in listdir(path) if f.endswith("_MK.txt")]
    #print onlyfiles
    for input_file in onlyfiles:
        log=run_MK_db(path,input_file,num_iter)
        #log of results
        log_file=input_file.split('.')[0] + "_" + str(num_iter) + '_log.txt'
        g=open(path+'/'+log_file,'a')
        for results in log:
            g.write("\n\n===========\n\n")
            g.write(results)
        g.close()

        extract_tuples(path+'/'+log_file)




if __name__ == '__main__':
    main()