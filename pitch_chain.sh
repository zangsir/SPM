#!/usr/bin/env bash


#build speaker dicts
#if you changed pitch ceiling or step, the pitch distribution is changed, so we'll need to rebuild dicts of fil_std, threshold, mean, all_pitch,etc.
echo building speaker dicts...
python speaker_dict.py -all

#write pitch chain
#input: pitch/
#output:procd_pitch*
echo producing procd pitch...
python write_pitch_proc.py pitch all_data


#normalize
echo normalizing...
#input: input_path (procd pitch), output path
python norm_spk.py procd_pitch_newtrim_final/ norm_pitch_final/
python build_index_dict.py -b

#make long ts version, -i for interject
python make_long_ts.py -n all_spk_lts_norm.txt

#build dictionary for long ts lookup
python build_index_dict.py -b norm_pitch_newtrim

#make other versions of DB version data files
#unigram - mode 1 is voiced; 2 is whole; comp_len
./extract_syl_meta.sh 1 30
#ngrams - 2 0 100 means bigram and smooth off, extracting with comp_len=100.
./ext_ngrams.sh 2 0 100



#make space and MK ver
./make_MK_ver.sh MK_data/csv_version
