for i in essays/*.txt

do
	filename=$i

	
	echo $filename
	
	extension="${filename##*.}"
	firstname="${filename%.*}"
	newfile=$firstname"_toksent.txt"
	echo $newfile

	./toksent $filename >> essays/$newfile 
done


for i in essays/*toksent.txt

do
	filename=$i

	
	echo $filename
	
	extension="${filename##*.}"
	firstname="${filename%.*}"
	newfile=$firstname"_tokword.txt"
	echo $newfile

	./toksent $filename >> $newfile 
done




for i in essays/*tokword.txt

do
	filename=$i

	
	echo $filename
	
	extension="${filename##*.}"
	firstname="${filename%.*}"
	newfile=$firstname"_pos.txt"
	echo $newfile

	./stanford-postagger.sh stanford-postagger.jar pos-tagger.model $filename >> $newfile 
done