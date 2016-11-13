FILE = Name of the ascii text file that contains the database of time series.
m = number of time series
n = length of individual time series 
R = number of reference points
v = 0 for suppressing the statistics(default) / 1 for printing the statistics
A = 0 for NOT using Early Abandonning / 1 for using Early Abandonning(default)



Usage for mk_d:
===============

mk_d.exe FILE m n R [V]


Sample command for mk_d:
------------------------

mk_d.exe d.txt 1000 1024 10 1




Usage for BF_d:
===============

BF_d.exe FILE m n [A | A V]


Sample commands for BF_d:
------------------------

BF_d.exe d.txt 1000 1024 0 1

BF_d.exe d.txt 1000 1024 1


Notes:
******

1. The output statistics may not be appeared correctly in 32 bit processors. For 64 bit processors it is guaranteed to give correct output.
2. The motif pair will be output irrespective of the platform.
3. To Compile the codes any version of gcc should be fine.
4. Please report bugs to mueen@cs.ucr.edu
 