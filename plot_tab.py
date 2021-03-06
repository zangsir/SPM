import sys
import matplotlib.pyplot as plt
def get_vec(file):
    time=[]
    pitch=[]
    f=open(file,'r').read().split('\n')
    for line in f[1:]:
        if line!='':
            l=line.split('\t')
            time.append(l[0])
            pitch.append(l[1])
    return time,pitch


def get_vec_noext(file):
    time=[]
    pitch=[]
    f=open(file,'r').read().split('\n')
    for line in f[1:]:
        if line!='':
            l=line.split('\t')
            if l[1]!="1000":
                time.append(l[0])
                pitch.append(l[1])
    return time,pitch

def main():
    inputfile=sys.argv[1]
    time,pitch=get_vec(inputfile)
    plt.plot(time,pitch)
    plt.show()
if __name__ == '__main__':
    main()
