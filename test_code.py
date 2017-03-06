from rankRef import *
data_path="test_data/"
data_file='downsample_syl_3_meta_100_MK.txt'

X,k='2','30'
run_MK('',"test_data/downsample_syl_3_meta_100_MK.txt",'2','30')
motif_clusters=get_all_unique_motifs(data_path,data_file,X,k,False)
print 'final list of motif clusters:'
print motif_clusters
