from os import listdir

#take all csv files corresponding to each sentence, and concate all so you have all syllables from all sents. 

path='syl_csv'
#dir='pitch_prob'
onlyfiles = [ f for f in listdir(path) if f.endswith(".csv")]
outdir='syl_csv'
outname='test_data.csv'
#print onlyfiles
for file_pitch in onlyfiles:
    inputfile=path+'/'+file_pitch
    f=open(inputfile,'r').read()
    g=open(outname,'a')
    g.write(f)
    g.close()

