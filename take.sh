direc="$1"

if [ -z "$direc" ]; then 
    direc="epochs"
fi

echo "directory=$direc"

if [ ! -f "epoch_id.txt" ]; then
    echo 0 > epoch_id.txt
fi

if [ ! -d "$direc" ]; then
    mkdir $direc 
fi

epoch_id=`cat epoch_id.txt`

cp -v out-video.avi $direc/out-video-${epoch_id}.avi
cp -v out-key.csv $direc/out-key-${epoch_id}.csv
cp -v out-key-btn.csv $direc/out-key-btn-${epoch_id}.csv

epoch_id=`expr ${epoch_id} + 1`
echo ${epoch_id} > epoch_id.txt
