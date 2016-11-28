#this script extracts n-grams out of unigram syl_norm_sil.csv. in order to only extract within sentence ngrams, we have a separator in that file indicating file split. 
import sys

n=int(sys.argv[1])
unigram_file="syl_norm_split.csv"
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

            
#print "|total",len(ngrams_agg)            
for i in ngrams_agg:
    print i