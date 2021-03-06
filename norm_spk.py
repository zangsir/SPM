from os import listdir
import numpy as np
from downsample import *
import random,os,pickle,sys
import matplotlib.pyplot as plt

#argv: input path, outpath

def hertz_to_bark(pitch):
    return 7.0 * np.log (pitch/650.0 + np.sqrt (1 + (pitch/650.0)**2))

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 

def get_speaker_mean(speaker,path):
    """path contains all pitch files, and we'll pick out files for this speaker to normalize"""
    onlyfiles = [ f for f in listdir(path) if f.startswith(speaker) and f.endswith('.tab')]
    all_pitch=[]
    for file_pitch in onlyfiles:
        time,pitch=get_vec_noext(path+file_pitch)

        pitch_float=[float(i) for i in pitch]
        #pitch_bark=hertz_to_bark(pitch_float)
        all_pitch.extend(pitch_float[:])
    return np.mean(all_pitch)


def normalize(pitch,spk_mean):
    """let's normalize one file for now"""
    #normalize,log,downsample,smooth
    #for this speaker, normalize all files of this spk
    #print pitch[:100],'here'
    pitch_float=[float(i) for i in pitch]
    pitch=np.array(pitch_float)
    bark_pitch=hertz_to_bark(pitch)
    norm_pitch=(bark_pitch- hertz_to_bark(spk_mean))
    #if you want to scale, uncomment this line and delete these comments, leave:/np.std(bark_pitch)
    #log_pitch=np.log(norm_pitch)
    #down_pitch=downsample_mix(log_pitch,30)
    return norm_pitch





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



def test_plot(pitch):
    x = np.linspace(0,30, len(pitch))
    plt.plot(x, pitch, 'bo-')
    plt.show()



def main():
    train_path='all_data/'
    all_speaker=get_all_speaker(train_path)
    pickle_file = 'procd_spk_mean_dict.p'
    #pitch_path='procd_pitch_newtrim_sec_3/'
    #outpath='norm_pitch_newtrim/'
    pitch_path=sys.argv[1]
    outpath=sys.argv[2]

    procd_spk_mean_dict={}
    #print onlyfiles
    for speaker in all_speaker:
        #working with one speaker
        if os.path.isfile(pickle_file):
            procd_spk_mean_dict=pickle.load(open(pickle_file,'rb'))
            spk_mean = procd_spk_mean_dict[speaker]
            print 'loaded speaker mean...'
        else:
            spk_mean=get_speaker_mean(speaker,pitch_path)
            procd_spk_mean_dict[speaker]=spk_mean
        print speaker+'mean:'+str(spk_mean)
        #print spk_mean
        #normalize,log,downsample,smooth
        #test with a file of this speaker
        #in a real situation, you'll get all files of the speaker, and call normalize and save them one by one.
        onlyfiles = [ f for f in listdir(pitch_path) if f.startswith(speaker) and f.endswith('.tab')]
        rand_files=random.sample(onlyfiles,1)
        #testing using rand_files, otherwise use onlyfiles 
        testing=False
        if testing:
        
            for file_pitch in rand_files:
                print file_pitch
                
                time,pitch=get_vec_noext(pitch_path+file_pitch)
                norm_pitch=normalize(pitch,spk_mean)
                test_plot(pitch)
                test_plot(norm_pitch)

        else:
            for file_pitch in onlyfiles:
                #print file_pitch
                file_name=file_pitch.split('_proc')[0]
                outname=file_name+'_norm.tab'
                
                time,pitch=get_vec_noext(pitch_path+file_pitch)
                norm_pitch=normalize(pitch,spk_mean)
                f=open(outpath+outname,'w')
                f.write('time\tnorm_pitch\n')
                f.close()

                f=open(outpath+outname,'a')
                for i in range(len(time)):
                    f.write(time[i]+'\t'+str(norm_pitch[i])+'\n')
                f.close()
    if not os.path.isfile(pickle_file): 
        print 'dumping spk mean dict...'
        pickle.dump(procd_spk_mean_dict, open( pickle_file, "wb" ) )
















if __name__ == '__main__':
    main()



