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
python make_long_ts.py -n

#build dictionary for long ts lookup
python build_index_dict.py -b norm_pitch_newtrim

#make other versions of DB version data files
