import sys
import pylab as plt

inputfile=sys.argv[1]
outfile=inputfile.split('.')[0]+'.png'
lts=open(inputfile,'r').read().split('\n')
lts=[float(i) for i in lts[:-1]]#last line is newline character
print len(lts)
plt.plot(lts)
plt.savefig(outfile)
