#there are 1621 pitch files where syllables at the end are chopped off in the process of procd_pitch. These are cases where we need to restore the pitch values from the original pitch/ files. Use this script to do so.

from scipy.interpolate import interp1d
import numpy as np

def read_tab_only(inputfile):
    
    f=open(inputfile,'r').read().split('\n')

    time=[]
    pitch=[]
    for i in range(1,len(f)):
        line=f[i]
        if line!="":
            split=line.split('\t')
            #print split
            time.append(float(split[0]))
            pitch.append(float(split[1]))
    
    #plt.plot(pitch,'gx')
    return time,pitch


def extend_pitch(pitch_file,procd_file):

    #pitch file:'pitch/pitcCHX000490.tab'
    time,pitch=read_tab_only(pitch_file)

    #plt.plot(time,pitch)

    #procd file:'procd_pitch_newtrim_final/CHX000490_proc.tab'
    t,p=read_tab_only(procd_file)
    #plt.plot(t,p,'x')
    extend_pitch=[pitch[i] for i in range(len(time)) if time[i]>t[-1]]
    extend_time=[time[i] for i in range(len(time)) if time[i]>t[-1]]

    if extended_time==[]:
        return t,p


    fp=interp1d(extend_time,extend_pitch)
    begin,end=extend_time[0],extend_time[-1]
    interp_time=np.arange(float(begin)+0.001,float(end)-0.001,0.001)
    interp_pitch=fp(interp_time)
    t.extend(interp_time[:])
    p.extend(interp_pitch[:])
    #plt.plot(time,pitch)
    #plt.plot(t,p,'x')
    return t,p


def read_file_list(error_file):
    all_lines=open(error_file,'r').read().split('\n')
    file_list=[]
    for line in all_lines:
        len_syl=line.split(' ')[1]
        if len_syl!='0':
            continue
        file_name=line.split('_')[0]
        file_list.append(file_name)
    return file_list





def main():
    error_file = 'lennew.txt'
    file_list=read_file_list(error_file)
    print file_list
    pitch_path='pitch/'
    procd_path='procd_pitch_newtrim_final/'
    extend_path='extended_procd'
    for file_name in file_list:
        print file_name
        pitch_file = pitch_path + 'pitc' + file_name + '.tab'
        procd_file = procd_path + file_name + '_proc.tab'
        out_file = extend_path + file_name + '_proc.tab'
        new_time,new_pitch = extend_pitch(pitch_file, procd_file)
        #write this to new procd pitch file with the same name
        f=open(out_file,'w')
        f.write('time\tpitch\n')
        f.close()

        f=open(out_file,'a')
        for i in range(len(new_time)):
            f.write(str(new_time[i]) + '\t' + str(new_pitch[i]) + '\n')
        f.close()




if __name__ == '__main__':
    main()










