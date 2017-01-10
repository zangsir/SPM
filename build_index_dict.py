#use this script to build a dictionary that you can look up a sentence file from a index number in the long TS in MK motif discovery context.
#use -b mode to build the dict and use -q mode to query the dict.


from os import listdir
import sys,pickle
from collections import defaultdict

def get_vec(file):
    #time=[]
    pitch=[]
    f=open(file,'r').read().split('\n')
    for line in f[1:]:
        if line!='':
            l=line.split('\t')
            #time.append(l[0])
            pitch.append(l[1])
    return pitch

def build_dict():
    sent_path='norm_pitch_newtrim/'
    total_index=0

    onlyfiles = [ f for f in listdir(sent_path) if f.endswith(".tab")]
    #print onlyfiles
    index_dict=defaultdict(tuple)
    counter=0

    for file_name in onlyfiles:
        input_file=sent_path+file_name
        first_name=file_name.split('_')[0]
        pitch_vec=get_vec(input_file)
        key=(counter,counter+len(pitch_vec)-1)
        value=first_name
        index_dict[key]=value
        counter=counter+len(pitch_vec)
    pickle.dump(index_dict, open( "index_dict.p", "wb" ) )

def query_dict(query,index_dict):
    #this function can be called from other scripts to query, and then we can go to the file in question and look at the position of the specific point desired and pull its segments.
    for k in index_dict:
        if query>=k[0] and query<=k[1]:
            return k,index_dict[k]
    return 'Error:index number too large or is of wrong format, check your input and run again.'




def main():
    if sys.argv[1]=='-b':
        build_dict()
    elif sys.argv[1]=='-q':
        query=int(sys.argv[2])
        index_dict=pickle.load(open('index_dict.p','rb'))
        print query_dict(query,index_dict)




if __name__ == '__main__':
    main()



