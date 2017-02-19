#two directories containing the training files with the same name. merge them. 

def merge(path_1,path_2,out_path='merged_train_data/'):
	onlyfiles = [ f for f in listdir(path_1) if f.endswith(".csv")]
	#print onlyfiles
	for filename in onlyfiles:
		print filename
		file_1=path_1 + filename
		file_2=path_2 + filename
		f1=open(file_1,'r').read()
		f2=open(file_2,'r').read().split('class\n')[1]
		outfile=out_path + path_1[:-1] + "_" + path_2[:-1] + "_" + filename 
		g=open(outfile,'w').close()
		g=open(outfile,'a')
		g.write(f1 + '\n')
		g.write(f2)


def main():
	path_1=sys.argv[1]
	path_2=sys.argv[2]
	merge(path_1,path_2)

