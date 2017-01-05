#use this script to read edgelist of tuple files from MK DB version output and then it will generate a pdf file with all top k motif clusters plotted (k=15 currently, you can also change it)

import networkx as nx
import matplotlib.pyplot as plt
import sys,re
from os import listdir
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os


def plot_multi_page(data,attrs,all_centers,all_index,threshold,outplotname):
    # The PDF document
    pdf_pages = PdfPages(outplotname)
    print 'plotting motif clusters...'
    # Generate the pages
    nb_plots = len(data)
    print "len data:",nb_plots
    nb_plots_per_page = 2
    nb_pages = int(np.ceil(nb_plots / float(nb_plots_per_page)))
    grid_size = (nb_plots_per_page, 1)
    #data is all_motif_cluster
    #attr is all_motif_cluster_attr
    for i, motif_cluster in enumerate(data):
        # Create a figure instance (ie. a new page) if needed
        if i % nb_plots_per_page == 0:
            fig = plt.figure(figsize=(8.27, 11.69), dpi=100)
        
        #print tones
        # Plot stuffs !
        motif_cluster_attr=attrs[i]
        plt.subplot2grid(grid_size, (i % nb_plots_per_page, 0))
        center=all_centers[i]
        motif_cluster_index=all_index[i]
        #unpack center
        assert len(center)==3
        center_index=center[0]
        center_data=center[1]
        center_attr=center[2]
        #plot motif center first
        plt.plot(center_data,'ro')
        for j in range(len(motif_cluster)):
            motif=motif_cluster[j]
            label_tone=motif_cluster_attr[j][0]
            label_ind=motif_cluster_index[j]
            
            weight=g[center_index][label_ind]['weight']
            label_ind=str(label_ind)
            label=label_ind + '_' + label_tone
            if weight<threshold:
	            plt.plot(motif,label=label)
	            plt.legend()
        plt.title(str(center_index)+" , threshold:"+str(threshold))
        #plt.text(.1,-.4,str(motif_cluster_attr))
        #let's try query the seralized the attributes files without putting them in plots.
        # Close the page if needed
        if (i + 1) % nb_plots_per_page == 0 or (i + 1) == nb_plots:
            plt.tight_layout()
            pdf_pages.savefig(fig)
     
    # Write the PDF document to the disk
    pdf_pages.close()






def get_con_index(tup,target):
    """ in tup (10,13374) returns the index that's not target. target is 13374, then return 0 """
    if len(tup)!=2:
        raise ValueError('tuple length is not 2')
    if tup.index(target)==1:
        return 0
    elif tup.index(target)==0:
        return 1
    else:
        raise ValueError('target not in tuple or tuple length is not 2')





##################################### main 
#read edgelist and build graph
#'mk_txt/downsample_1_meta_100_MK_10_tuple_graph.txt'
mode=sys.argv[1]
if mode=='test':
    path='mk_txt_test'
    print 'test_mode'
else:
    path='mk_txt'
    print 'normal mode'
onlyfiles = [ f for f in listdir(path) if f.endswith("tuple_graph.txt")]
#print onlyfiles
for file_name in onlyfiles:
    print "============"+file_name
    first_name=file_name.replace('_MK_10_tuple_graph.txt','')
    len_ts=first_name.split('_')[-1]
    print "Number of points in TS =",len_ts
    outplotname='plots/'+first_name+"_motif_clusters_threshold.pdf" #final cluster plot name
    if os.path.isfile(outplotname):
        print 'file exists:skipped',outplotname
        continue
    edgelist_file = path + '/' + file_name
    g = nx.read_edgelist(edgelist_file, nodetype=int, data=(('weight',float),))
    #plan is to draw graph and degree distribution separately into pdf files, one per data file; the motifs visualization (clusters) will be drawn into a multi page pdf file.
    #draw graph
    graph_output='plots/'+file_name.replace('.txt','.pdf')
    plt.figure(num=None, figsize=(12, 9), dpi=120, facecolor='w', edgecolor='k')
    nx.draw(g,with_labels=True)
    plt.savefig(graph_output)
    print 'plotted graph'
    
    #plot degree distribution sorted
    degree_output='plots/'+file_name.replace('.txt','_dgr.pdf')
    degree_title=file_name.replace('.txt','')
    in_degrees= g.degree() # dictionary node:degree
    in_values= sorted(set(in_degrees.values()))
    in_hist= [in_degrees.values().count(x) for x in in_values]
    plt.plot(in_values, in_hist, 'ro-') # in-degree
    plt.figure() # you need to first do 'import pylab as plt'
    plt.grid(True)
    plt.loglog(in_values, in_hist, 'ro-') # in-degree
    
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    plt.title('MK_DB motifs(loglog):'+degree_title)
    plt.savefig(degree_output)
    print "plotted degree distribution"
    
    ###################################################
    print 'building cluster dict'
    #build cluster dict
    #print "central node: connected nodes"
    cluster_dict={}#key is the central node, value is the nodes it is connected to
    all_edges=g.edges()
    sort_nodes=sorted(in_degrees,key=in_degrees.get,reverse=True)
    #print 'sorted_nodes:',sort_nodes
    #print 'k=',k
    a=len(sort_nodes)
    k=15 if a>=15 else a
    for i in range(k):
        node=sort_nodes[i]
        
        connected_nodes=[j[get_con_index(j,node)] for j in all_edges if node in j]
        #print node,":",connected_nodes 
        cluster_dict[node]=connected_nodes
        
    
    
    #to visualize motif clusters by their original contours
    #read in pickled data first
    
    #loading original version data file pickles, not the tuple motif pair pickles in the pickle directory
    ori_path='original_ver'
    #data_npy=np.load('original_ver/downsample_1_meta_100_data.npy')
    #attr_npy=np.load('original_ver/downsample_1_meta_100_attr.npy')
    
    
    data_npy_file=ori_path+'/'+first_name+'_data.npy'
    attr_npy_file=ori_path+'/'+first_name+'_attr.npy'
    data_npy=np.load(data_npy_file)
    attr_npy=np.load(attr_npy_file)
    #len(data_npy)
    
    #build a list that contains all cluster data
    all_motif_cluster=[]
    all_motif_cluster_attr=[]
    all_centers=[]
    all_motif_index=[]
    for k in cluster_dict:
        motif_center=data_npy[k]
        center_attr=attr_npy[k]
        this_center=[k]
        this_center.append(motif_center)
        this_center.append(center_attr)
        motif_cluster_ind=cluster_dict[k]
        #print motif_cluster_ind
        motif_cluster=data_npy[motif_cluster_ind]
        motif_cluster_attr=attr_npy[motif_cluster_ind]
        #print motif_cluster_attr
        all_motif_cluster.append(motif_cluster)
        all_motif_cluster_attr.append(motif_cluster_attr)
        all_centers.append(this_center)#this_center contains three things: center_index, center_data, center_attr
        all_motif_index.append(motif_cluster_ind)
    threshold_dict={80:1.5,100:1.5,200:4,300:6,400:9,500:10,600:11}
    threshold=threshold_dict[int(len_ts)]
    plot_multi_page(all_motif_cluster,all_motif_cluster_attr,all_centers,all_motif_index,threshold,outplotname)