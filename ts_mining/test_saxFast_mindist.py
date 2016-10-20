
# MIN_DIST demo
print "the result obtained from these tests should be the same as if you run it on the original SAX implementation in Matlab"
from saxpyFast import *

s=SAX(alphabetSize = 4, wordSize = 8, windowSize = 32)
table = s.build_dist_table()
# print table

print '========== test the dist matrix given symbolic vectors as input'

sA = [3,4,2,1,1,3,4,2]
sB = [1,1,3,4,3,1,1,4]

print np.sum(table[np.array(sA)-1,np.array(sB)-1])

test_ts=     [0,    0.3146,    0.5972,    0.8192,    0.9580,    0.9996,    0.9396,    0.7843,    0.5494,    0.2586,   -0.0584,   -0.3694,   -0.6430,   -0.8513,   -0.9731,   -0.9962,   -0.9181,   -0.7468,   -0.4996,   -0.2018,    0.1165,    0.4231,    0.6866,    0.8805,    0.9849,    0.9894,    0.8934,    0.7067,    0.4482,    0.1443,   -0.1743,   -0.4752,   -0.7279,   -0.9066,   -0.9933,   -0.9792,   -0.8656,   -0.6642,   -0.3953,   -0.0863,    0.2315,    0.5258,    0.7667,    0.9297,    0.9984,    0.9657,    0.8349,    0.6194,    0.3410,    0.0280,   -0.2879,   -0.5745,   -0.8028,   -0.9496,   -1.0000,   -0.9488,   -0.8014,   -0.5725,   -0.2855,    0.0304,    0.3433,    0.6213,    0.8363]

sA=np.array(test_ts[3:35])
sB=np.array(test_ts[14:46])

sA = (sA - np.mean(sA))/np.std(sA,ddof=1)
sB = (sB - np.mean(sB))/np.std(sB,ddof=1)

print sA
print sB
print "+++++++++++++++ test the entire pipeline of first converting to SAX symbols from raw TS and then doing MIN_DIST"
saxA, pA = s.to_letter_rep(sA)
saxB, pB = s.to_letter_rep(sB)



print saxA
print saxB



print '------------------'
mindist = s.min_dist(saxA[0], saxB[0])

print 'mindist:', mindist
