#extract both unvoiced and voiced part as a syllable

from plot_spectro import *


#read pitch tab file, original this is procd, but then it became norm_pitch
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


def extract_syl(timestamps,time,pitch,ngrams=True):

    """input is timestamps and pitch contour of a sentence;output is a list of syl-length pitch vectors extracted from this sentence. later we write these vectors into a file, each row is one syl-length vector of pitch"""

    #ngrams: if turned on, this will append an extra col to indicate if this is syl precedes a 'sil' so we can split them by silence; in unigram case (False), we don't want this extra complication to change data format.

    pitch_vec=[]
    k=0
    while k<len(timestamps):
        #print k
        this_syl_values,label = get_syl_vec(timestamps[k],pitch,time)
        
        #print "this:",this_syl_values
        
        if label=='sil':
            k+=1
            continue
        
        m = re.search(r'\d$', label)
        if m is not None:
            #print 'vowel case'
            if k+1<len(timestamps):
                next_label = timestamps[k+1][2]
                if next_label=="sil":
                    position='end'
                else:
                    position='mid'
            else:
                position='end'

            if ngrams:
                this_syl_values.append(position)
            pitch_vec.append(this_syl_values)
            k+=1
        else:
            if k+2<len(timestamps):
                next_next_label = timestamps[k+2][2]
                if next_next_label=="sil":
                    position='end'
                else:
                    position='mid'
            else:
                position='end'
            
            next_syl_values,label_next = get_syl_vec(timestamps[k+1],pitch,time)
            #print 'NEXT:',next_syl_values
            combined_label=label+label_next
            #print combined_label
            combined_syl = this_syl_values[:-1]
            combined_syl.extend(next_syl_values)
            if ngrams:
                combined_syl.append(position)
            pitch_vec.append(combined_syl)
            k+=2
            
    return pitch_vec

def get_syl_vec(tsp,pitch,time):
    start, end, label = tsp[0], tsp[1], tsp[2] 
    syl_values=[str(round(float(pitch[i]),3)) for i in range(len(pitch)) \
                if float(time[i])>=float(start) and float(time[i]) <=float(end) and float(pitch[i])!=1000]
    syl_values.append(label[-1])
    return syl_values,label



#append to file
def append_syl(pv,outname):
    g=open(outname,'w')
    g.write('')
    g.close

    f=open(outname,'a')
    for i in range(len(pv)):
        row=pv[i][:-1]
        #append meta information
        row.append(outname.split('.')[0])
        row.append(str(i))
        row.append(pv[i][-1])

        line=','.join(row)
        f.write(line+'\n')
    f.close()

def main():
    
    #for all sentences;get pv(pitch vector); append lines to the output file
    #path is pitch_path
    path='norm_pitch_newtrim'
    #path='test_qphons'
    data_path='all_data'
    #data_path='test_qphons'
    #dir='pitch_prob'
    onlyFiles = [ f for f in listdir(path) if f.endswith(".tab")]
    outdir='syl_csv_norm_whole_meta'
    #outdir='test_qphons'
    #print onlyFiles
    for file_pitch in onlyFiles:
        inputfile=path+'/'+file_pitch
        #print inputfile
        first_name=file_pitch.split('.tab')[0]
        first_name=first_name.split('_')[0]
        phonsFile=data_path +'/'+first_name+'.qphons'
        outname=outdir+'/'+first_name+'_whole.csv'
        times,pitch=read_pitch(inputfile)
        timeStamps,xts,labelss=get_annos(phonsFile)
        pv=extract_syl(timeStamps,times,pitch)
        append_syl(pv,outname)



if __name__=="__main__":
    main()

