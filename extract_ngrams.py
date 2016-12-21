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
print 'extracting:',ndict[n]
unigram_file=sys.argv[2]
#such as "syl_norm_split_smooth.csv"
output_file=sys.argv[3]
#unigram_file="snapshot-uni.csv"
sents=open(unigram_file,'r').read().split(',end\n')

ngrams_agg=[]
for s in sents:
    #each time processing one sentence
    #unigs is the list version of s, a string
    unigs=s.split('\n')
    #add this end because above when reading the one input file, we first split the file into units separated by ',end\n', so in that case, in each unit after split, the last one 'end' is the splitter thus is missing, so we need to add that back in for subsequent processing convenience. 
    unigs[-1]+=',end'
    if len(unigs)<n:
            continue
    #for i in range(len(unigs)):
     #   print i
      #  print unigs[i]
    #sys.exit()
    
    for i in range(len(unigs)-n+1):
        #process one syllable as the starting point, at each time 
        data=[]
        labels=[]
        metas=[]
        positions=[]
        type_pos=[]
        for j in range(n):
            if len(unigs[i+j].split(','))<4:
                print 'error case ignored...'
                continue
            uni_data=unigs[i+j].split(',')[:-4]
            uni_label=unigs[i+j].split(',')[-4]
            uni_typepos=unigs[i+j].split(',')[-1]
            uni_meta=unigs[i+j].split(',')[-3]
            uni_position=unigs[i+j].split(',')[-2]
            data.extend(uni_data)
            type_pos.append(uni_typepos)
            positions.append(uni_position)
            labels.append(uni_label)
            metas.append(uni_meta)
        #print 'metas:',metas
        ngram_label="".join(labels)
        ngram_meta=metas[0]
        ngram_data=",".join(data)
        ngram_pos="_".join(positions)
        ngram_typepos="_".join(type_pos)

        ngram_line=ngram_data+","+ngram_label+","+ngram_typepos+","+ngram_meta+","+ngram_pos
        ngrams_agg.append(ngram_line)
        #print "=====",i,len(ngrams_agg)
                        

            
print "|total",len(ngrams_agg)            
print 'starting writing to file...'
#for i in ngrams_agg:
#   print i

append_line(ngrams_agg,output_file)
