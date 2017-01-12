import pickle,os
train_path='all_data/'
all_speaker=get_all_speaker(train_path)
pitch_path='pitch/'
#print onlyfiles
pickle_file='spk_mean_dict.p'
pickle_file_ap='all_pitch_dict.p'
pickle_file_std='std_dict.p'
spk_mean_dict={}
all_pitch_dict={}
std_dict={}
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

    
if not os.path.isfile(pickle_file): 
    print 'dumping spk mean dict...'
    pickle.dump(spk_mean_dict, open( pickle_file, "wb" ) )
if not os.path.isfile(pickle_file_ap):    
    print 'dumping all pitch dict...'
    pickle.dump(all_pitch_dict, open( pickle_file_ap, "wb" ) )
if not os.path.isfile(pickle_file_std):
    print 'dumping std dict...'
    pickle.dump(std_dict, open( pickle_file_std, "wb" ) )
