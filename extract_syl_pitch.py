#input is preprocessed pitch file(.tab) and phons file
#output is N-point pitch contour profiles stored in one file, one syllable per row
#do we need to downsample at this point? does SAX works with variable length input?seems doesn't matter.

#other possibilities of this include writing to files with not only tones appended, but also segment identity and other info.

#currently the tone includes only rhyme segments.

#you can also extract tone n-grams. 

from os import listdir
from plot_spectro import *


#read pitch tab file
def read_pitch(procd_tab):
    #procd_tab='procd_pitch/CHJ000014_proc.tab'
    f=open(procd_tab,'r').read().split('\n')
    time=[]
    pitch=[]
    for line in f[1:]:
        if line!='':
            time.append(line.split('\t')[0])
            pitch.append(line.split('\t')[1])
            
            #the pitch vector contains pitch values (track) of one contour of the sentence
    return time,pitch


#this is voiced segments only,doesn't include consonant portion
def extract_syl(timestamps,time,pitch):
    """input is timestamps and pitch contour of a sentence;output is a list of syl-length pitch vectors extracted 
    from this sentence. later we write these vectors into a file, each row is one syl-length vector of pitch"""
    pitch_vec=[]
    
    for k in range(len(timestamps)):
        tsp=timestamps[k]
        start,end,label=tsp[0],tsp[1],tsp[2]
        #print start,end,label
        m = re.search(r'\d$', label)
        #print label,m
        # if the string ends in digits m will be a Match object, or None otherwise.
        if m is not None:
            #print start,end
            #print tsp
            syl_values=[str(round(float(pitch[i]),3)) for i in range(len(pitch)) \
                        if float(time[i])>=float(start) and float(time[i]) <=float(end) and float(pitch[i])!=1000]

            #append tone label
            syl_values.append(label[-1])
            pitch_vec.append(syl_values)
            #trim_unv_time.extend(syl_times[:])
    

    return pitch_vec





#append to file
def append_syl(pv,outname):
    f=open(outname,'a')
    for row in pv:
        line=','.join(row)
        f.write(line+'\n')
    f.close()

def main():
	#for all sentences;get pv; append lines to the output file
	path='procd_pitch'
	#dir='pitch_prob'
	onlyfiles = [ f for f in listdir(path) if f.endswith(".tab")]
	outdir='syl_csv'
	#print onlyfiles
	for file_pitch in onlyfiles:
	    inputfile=path+'/'+file_pitch
	    print inputfile
	    first_name=file_pitch.split('.tab')[0]
	    first_name=first_name.split('_')[0]
	    phons_file='pitch/'+first_name+'.phons'
	    outname=outdir+'/'+first_name+'_voiced.csv'
	    time,pitch=read_pitch(inputfile)
	    timestamps,xt,labels=get_annos(phons_file)
	    pv=extract_syl(timestamps,time,pitch)
	    append_syl(pv,outname)
	    



if __name__=="__main__":
	main()
