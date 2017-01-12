for i in test/*.flac

do
	filename=$i
	echo $filename
	#filename=$(basename "$fullfile")
	extension="${filename##*.}"
	firstname="${filename%.*}"
	
	newfile=$firstname".wav"
	echo $newfile
	sox $filename $newfile
     

	
done
