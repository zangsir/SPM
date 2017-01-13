import pickle,os





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

fil_std_dict={}
for spk in all_pitch_dict:
    all_pitch_spk=all_pitch_dict[spk]
    hist,bin_edges=np.histogram(all_pitch_spk,bins=20,density=True)

    max_ind=np.argmax(hist)
    
    for i in range(len(hist)):
        if i>max_ind and hist[i]<1e-4:
            threshold=bin_edges[i+1]
            print hist[i-1],hist[i],bin_edges[i+1]
            break
    all_pitch_spk_fil=[j for j in all_pitch_spk if j<=threshold]
    #plt.figure()
    #plt.hist(all_pitch_dict[spk],bins=20)
    #plt.axvline(x=threshold)
    #plt.figure()
    #plt.hist(all_pitch_spk_fil,bins=20)
    #plt.title(spk+",std:"+str(np.std(all_pitch_spk_fil)))
    fil_std_dict[spk]=np.std(all_pitch_spk_fil)
    
if not os.path.isfile(pickle_file): 
    print 'dumping spk mean dict...'
    pickle.dump(spk_mean_dict, open( pickle_file, "wb" ) )
if not os.path.isfile(pickle_file_ap):    
    print 'dumping all pitch dict...'
    pickle.dump(all_pitch_dict, open( pickle_file_ap, "wb" ) )
if not os.path.isfile(pickle_file_std):
    print 'dumping std dict...'
    pickle.dump(std_dict, open( pickle_file_std, "wb" ) )
if not os.path.isfile(pickle_file_fil_std):
    pickle.dump(fil_std_dict, open( pickle_file_fil_std, "wb" ) )
