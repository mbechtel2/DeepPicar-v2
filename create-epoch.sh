ID=$1

if [ ! -e epochs/out-key-$ID.csv ] && [ ! -e epochs/out-video-$ID.avi ]
then
	mv out-key.csv epochs/out-key-$ID.csv
	mv out-video.avi epochs/out-video-$ID.avi
else
	echo "Epoch $ID already exists"
fi
