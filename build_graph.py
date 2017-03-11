from sklearn.metrics.pairwise import euclidean_distances
from collections import defaultdict
import networkx as nx
from os import listdir
import pickle,os,sys

def divide_data(all_data):
    #take a list of all data, then divide into a dictionary where key is the tone ngram label, value is a matrix of vec
    ngram_dict=defaultdict(list)
    for d in all_data:
        key=d[-4]
        ngram_dict[key].append(d)
    return ngram_dict


def read_csv(data_file):
    f=open(data_file,'r').read().split('\n')
    all_data=[]
    for line in f:
        if line!="":
            l=line.split(',')
            all_data.append(l)
    return all_data


def serialize_dict(data_path,ngram_data_file):
    all_data=read_csv(data_path+ngram_data_file)
    ngram_dict=divide_data(all_data)

    
    for k in ngram_dict.keys():
        print k
        outfile='subdata/'+ngram_data_file.replace('.csv','_'+k+'.csv')
        
        if '6' in k:
            continue
        f=open(outfile,'a')
        for i in ngram_dict[k]:
            dataline=','.join(i)
            f.write(dataline+'\n')
        f.close()




def build_dist_matrix(ngram_dict):
    ngram_data_dict=defaultdict(list)
    for k in ngram_dict.keys():
        data=ngram_dict[k]
        for i in data:
            this_data=[float(j) for j in i[:-4]]
            ngram_data_dict[k].append(this_data)
    ngram_dist_matrix_dict=defaultdict(list)
    for k in ngram_data_dict.keys():
        X=ngram_data_dict[k]
        dist_matrix=euclidean_distances(X, X)
        ngram_dist_matrix_dict[k]=dist_matrix
    return ngram_dist_matrix_dict


def build_graph(ngram_data_file):
    all_data=read_csv(ngram_data_file)
    ngram_dict=divide_data(all_data)
    ngram_dist_matrix_dict=build_dist_matrix(ngram_dict)
    #all_graphs=[]
    for key in ngram_dist_matrix_dict.keys():
        graph_pkl=ngram_data_file.replace('.csv','_'+key+'.pkl')
        if os.path.isfile(graph_pkl):
            print 'skipping '+key
            continue
        print key
        delta=ngram_dist_matrix_dict[key]
        G = nx.from_numpy_matrix(delta)
        nx.write_gpickle(G,graph_pkl)
        print 'pickled:'+key
        #all_graphs.append(G)

def build_graph_less_memory(sub_dataset,graph_pkl):
    #each time read one subdataset and build one distance matrix for this subdata
    sub_data=read_csv(sub_dataset)
    data_vecs=[]
    for i in sub_data:
        this_data=[float(j) for j in i[:-4]]
        data_vecs.append(this_data)
    dist_matrix=euclidean_distances(data_vecs, data_vecs)
    G = nx.from_numpy_matrix(dist_matrix)
    nx.write_gpickle(G,graph_pkl)





def main():
    #data_path='ngram_data/'
    mode=sys.argv[1]
    if mode=='-build':
        print 'building graph mode...'
        subdata_path='subdata/'
        #datafiles = [ f for f in listdir(data_path) if f.endswith('csv')]
        subdatafiles = [ f for f in listdir(subdata_path) if f.endswith('csv')]
        for sub_datafile in subdatafiles:
            print sub_datafile
            key=sub_datafile.split('_')[-1].split('.')[0]
            graph_pkl=sub_datafile.replace('.csv','.pkl')
            if os.path.isfile(subdata_path+graph_pkl):
                print 'skipping '+key
                continue
            #print key
            build_graph_less_memory(subdata_path+sub_datafile,subdata_path+graph_pkl)
    elif mode=='-sub':
        print 'serialize sub data set...'
        serialize_dict('ngram_data/','downsample_syl_3_meta_200.csv')








if __name__ == '__main__':
    main()