import shutil,glob,sys
outfilename=sys.argv[2]
with open(outfilename, 'wb') as outfile:
    pattern=sys.argv[1]
    for filename in glob.glob(pattern):
        if filename == outfilename:
            # don't want to copy the output into the output
            continue
        with open(filename, 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)
