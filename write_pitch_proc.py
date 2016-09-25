from plot_spectro import *
import sys
from os import listdir


#cmd line arg: give the directory where pitch tab and phons file exist
#pitch_path=sys.argv[1]
#phons_path=sys.argv[2]
pitch_path=phons_path='pitchtest'
outdir='procd_pitch'
onlyfiles = [ f for f in listdir(phons_path) if f.endswith(".phons")]
for phons_file in onlyfiles:
    print phons_file
    first_name=phons_file.split('.phons')[0]
    phons_file=phons_path+'/'+phons_file
    pitch_tab_file=pitch_path+'/'+'pitc'+first_name+'.tab'
    interp_time,interp_pitch=pitch_proc_chain(pitch_tab_file,phons_file)
    outname=first_name+"_proc.tab"
    g=open(outdir+'/'+outname,'w')
    g.write('time\tpitch\n')
    g.close()
    f=open(outdir+'/'+outname,'a')
    for i in range(len(interp_time)):
        f.write(str(interp_time[i])+'\t'+str(interp_pitch[i])+'\n')
    f.close()
