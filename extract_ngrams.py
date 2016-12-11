#this script extracts n-grams out of unigram syl_norm_split.csv. in order to only extract within sentence ngrams, we have a separator in that file indicating file split. 
import sys
 
#append to file
def append_line(pv,outname):
    g=open(outname,'w')
    g.write('')
    g.close

    f=open(outname,'a')
    for line in pv:
        f.write(line+'\n')
    f.close()

n=int(sys.argv[1])
ndict={1:'unigram',2:'bigram',3:'trigram'}
unigram_file="syl_norm_split_smooth.csv"
output_file=sys.argv[2]
#unigram_file="snapshot-uni.csv"
sents=open(unigram_file,'r').read().split(',end\n')

ngrams_agg=[]
for s in sents:
    #each time processing one sentence
    #unigs is the list version of s, a string
    unigs=s.split('\n')
    unigs[-1]+=',end'
    if len(unigs)<n:
            continue
    #print len(unigs)
    
    for i in range(len(unigs)-n+1):
        #process one syllable as the starting point, at each time 
        data=[]
        labels=[]
        for j in range(n):
            uni_data=unigs[i+j].split(',')[:-2]
            uni_label=unigs[i+j].split(',')[-2]
            data.extend(uni_data)
            labels.extend(uni_label)
        ngram_label="_".join(labels)
        ngram_data=",".join(data)
        ngram_line=ngram_data+","+ngram_label
        ngrams_agg.append(ngram_line)
        #print "=====",i,len(ngrams_agg)
                        

            
print "|total",len(ngrams_agg)            
print 'starting writing to file...'
#for i in ngrams_agg:
#   print i

append_line(ngrams_agg,output_file)
