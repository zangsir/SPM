import pickle,os
import numpy as np
import sys
from os import listdir

#argv[1]: mode, -t (threshold) or -s (speaker dict)
def get_all_speaker(train_path):
    
    onlyfiles = [ f for f in listdir(train_path) if f.endswith(".flac")]
    all_speaker=set()
    for file_sound in onlyfiles:
        speaker=file_sound[:3]
        if speaker not in all_speaker:
            all_speaker.add(speaker)
    return all_speaker



def get_vec_noext(file):
    """don't get extrapolated values"""
    time=[]
    pitch=[]
    f=open(file,'r').read().split('\n')
    #print 'line number:',len(f)
    for line in f[1:]:
        if line!='':
            l=line.split('\t')
            if float(l[1])!=1000:
                time.append(l[0])
                pitch.append(l[1])
    return time,pitch

def get_speaker_mean(speaker,path):
    """path contains all pitch files, and we'll pick out files for this speaker to normalize"""
    onlyfiles = [ f for f in listdir(path) if f.startswith('pitc'+speaker) and f.endswith('.tab')]
    #print onlyfiles
    all_pitch=[]
    for file_pitch in onlyfiles:
        time,pitch=get_vec_noext(path+file_pitch)

        pitch_float=[float(i) for i in pitch]
        #pitch_bark=hertz_to_bark(pitch_float)
        all_pitch.extend(pitch_float[:])
    return all_pitch,np.mean(all_pitch)



def build_spk_dicts():
    print 'building spk dicts ...'

    train_path='all_data/'
    all_speaker=get_all_speaker(train_path)
    pitch_path='pitch/'
    #print onlyfiles
    pickle_file='spk_mean_dict.p'
    pickle_file_ap='all_pitch_dict.p'
    pickle_file_std='std_dict.p'
    pickle_file_fil_std='fil_std_dict.p'
    spk_mean_dict={}
    all_pitch_dict={}
    std_dict={}
    fil_std_dict={}
    for speaker in all_speaker:
        #working with one speaker
        if not os.path.isfile(pickle_file):
            all_pitch,spk_mean=get_speaker_mean(speaker,pitch_path)
            print speaker+'mean:'+str(spk_mean)
            spk_mean_dict[speaker]=spk_mean
        if not os.path.isfile(pickle_file_ap):
            all_pitch_dict[speaker]=all_pitch
        if not os.path.isfile(pickle_file_std):
            std_dict[speaker]=np.std(all_pitch)
        #sys.exit()
    
    if not os.path.isfile(pickle_file): 
        print 'dumping spk mean dict...'
        pickle.dump(spk_mean_dict, open( pickle_file, "wb" ) )
    if not os.path.isfile(pickle_file_ap):    
        print 'dumping all pitch dict...'
        pickle.dump(all_pitch_dict, open( pickle_file_ap, "wb" ) )
    if not os.path.isfile(pickle_file_std):
        print 'dumping std dict...'
        pickle.dump(std_dict, open( pickle_file_std, "wb" ) )
    



def build_threshold_dicts_old():
    """we can build a dict of the thresholds for spurious pitch values based on speaker's pitch distribution density curve as a byproduct of when we were doing the same for cutting of those spurious values and computing filtered_std for speakers"""
    print 'building threshold dict...'
    print 'loading all pitch...'
    all_pitch_dict=pickle.load(open('all_pitch_dict.p','rb'))
    threshold_dict={}
    threshold_dict_pickle = 'threshold_dict.p'
    for spk in all_pitch_dict:
        print 'processing speaker ',spk
        all_pitch_spk=all_pitch_dict[spk]
        hist,bin_edges=np.histogram(all_pitch_spk,bins=20,density=True)
        max_ind=np.argmax(hist)
        
        for i in range(len(hist)):
            if i>max_ind and hist[i]<1e-4:
                threshold=bin_edges[i]
                #print hist[i-1],hist[i],bin_edges[i+1]
                break
            if i==len(hist)-1:
                #print 'no threshold found'
                threshold=bin_edges[-1]
        threshold_dict[spk]=threshold

    if not os.path.isfile(threshold_dict_pickle):
        pickle.dump(threshold_dict, open(threshold_dict_pickle, "wb") )


def build_threshold_dict():
    #ref:newtrim_long_ts.ipynb
    threshold_dict_pickle = 'threshold_dict.p'
    if os.path.isfile(threshold_dict_pickle):
        sys.exit()
    all_pitch_dict=pickle.load(open('all_pitch_dict.p','rb'))
    threshold_dict={}
    
    for spk in all_pitch_dict:
        all_pitch_spk=all_pitch_dict[spk]
        hist,bin_edges=np.histogram(all_pitch_spk,bins=20,density=True)
        #print hist,bin_edges

        max_ind=np.argmax(hist)
        
        for i in range(len(hist)):
            if i>max_ind and hist[i]<1e-4:
                threshold=bin_edges[i]
                #print spk,hist[i-1],hist[i],threshold
                break
        if i==len(hist)-1:
            #print 'no threshold found'
            threshold=bin_edges[-1]
        
        #all_pitch_spk_fil=[j for j in all_pitch_spk if j<=threshold]
        #fil_std_dict[spk]=np.std(all_pitch_spk_fil)
        threshold_dict[spk]=threshold
    if not os.path.isfile(threshold_dict_pickle):
        pickle.dump(threshold_dict, open(threshold_dict_pickle, "wb") )


def build_fil_std_dict():
    print 'building fil std dict...'
    fil_std_dict={}
    all_pitch_dict=pickle.load(open('all_pitch_dict.p','rb'))
    for spk in all_pitch_dict:
        all_pitch_spk=all_pitch_dict[spk]
        hist,bin_edges=np.histogram(all_pitch_spk,bins=20,density=True)
        max_ind=np.argmax(hist)
        
        for i in range(len(hist)):
            if i>max_ind and hist[i]<1e-4:
                threshold=bin_edges[i]
                #print hist[i-1],hist[i],bin_edges[i+1]
                break
        if i==len(hist)-1:
            #print 'no threshold found'
            threshold=bin_edges[-1]
        all_pitch_spk_fil=[j for j in all_pitch_spk if j<=threshold]
        fil_std_dict[spk]=np.std(all_pitch_spk_fil)
    pickle_file_fil_std='fil_std_dict.p'
    pickle.dump(fil_std_dict, open( pickle_file_fil_std, "wb" ) )

def main():
    mode=sys.argv[1]
    #mode: -t for threshold dict, -s for other speaker dicts
    if mode == '-t':
        build_threshold_dicts()
    elif mode == '-s':
        build_spk_dicts()
    elif mode == '-all':
        #ideally this is just used for all once, we don't need to use other modes
        #if you do, you have to change the code
        build_spk_dicts()
        build_fil_std_dict()
        build_threshold_dict()
    elif mode == '-f':
        build_fil_std_dict()

if __name__ == '__main__':
    main()

