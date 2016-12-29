#input:MK data csv file like downsample_1_meta_100_MK.csv
#output: turn csv file into a space separated file

import sys
from os import listdir

def make_space_ver(input_file,output_file):
    f=open(input_file,'r').read()
    space_ver = f.replace(',',' ')
    g=open(output_file,'w').close()
    g=open(output_file,'a')
    g.write(space_ver)
    g.close()


def main():
    path = sys.argv[1]
    onlyfiles = [ f for f in listdir(path) if f.endswith(".csv")]
    print onlyfiles
    for file_name in onlyfiles:
        print "input:",file_name
        input_file = path + "/" + file_name
        output_file = input_file.replace(".csv",".txt")
        make_space_ver(input_file,output_file)

if __name__ == '__main__':
    main()
