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


