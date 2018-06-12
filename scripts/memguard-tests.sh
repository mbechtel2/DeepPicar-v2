
#Create directories
cd ..
mkdir datafiles/ReadCR
mkdir datafiles/WriteCR

####################################
#####     Solo Experiments     #####
####################################

#Solo - 500 MB/s
echo "Solo - 500 MB/s"
echo mb 500 1000 1000 1000 > /sys/kernel/debug/memguard/limit
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_500MB.txt
echo "Finished"

#Solo - 400 MB/s
echo "Solo - 400 MB/s"
echo mb 400 1000 1000 1000 > /sys/kernel/debug/memguard/limit
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_400MB.txt
echo "Finished"

#Solo - 300 MB/s
echo "Solo - 300 MB/s"
echo mb 300 1000 1000 1000 > /sys/kernel/debug/memguard/limit
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_300MB.txt
echo "Finished"

#Solo - 200 MB/s
echo "Solo - 200 MB/s"
echo mb 200 1000 1000 1000 > /sys/kernel/debug/memguard/limit
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_200MB.txt
echo "Finished"

#Solo - 100 MB/s
echo "Solo - 100 MB/s"
echo mb 100 1000 1000 1000 > /sys/kernel/debug/memguard/limit
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_100MB.txt
echo "Finished"

####################################
#####    BwRead Experiments    #####
####################################

#+3 Read Co-runner - 500 MB/s
echo "+3 Read Co-runner - 500 MB/s"
echo mb 1000 500 500 500 > /sys/kernel/debug/memguard/limit
bandwidth -a read -m 16384 -t 10000 -c 1 &
bandwidth -a read -m 16384 -t 10000 -c 2 &
bandwidth -a read -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/3ReadCR_cpu0_500MB.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Read Co-runner - 400 MB/s
echo "+3 Read Co-runner - 400 MB/s"
echo mb 1000 400 400 400 > /sys/kernel/debug/memguard/limit
bandwidth -a read -m 16384 -t 10000 -c 1 &
bandwidth -a read -m 16384 -t 10000 -c 2 &
bandwidth -a read -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/3ReadCR_cpu0_400MB.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Read Co-runner - 300 MB/s
echo "+3 Read Co-runner - 300 MB/s"
echo mb 1000 300 300 300 > /sys/kernel/debug/memguard/limit
bandwidth -a read -m 16384 -t 10000 -c 1 &
bandwidth -a read -m 16384 -t 10000 -c 2 &
bandwidth -a read -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/3ReadCR_cpu0_300MB.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Read Co-runner - 200 MB/s
echo "+3 Read Co-runner - 300 MB/s"
echo mb 1000 200 200 200 > /sys/kernel/debug/memguard/limit
bandwidth -a read -m 16384 -t 10000 -c 1 &
bandwidth -a read -m 16384 -t 10000 -c 2 &
bandwidth -a read -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/3ReadCR_cpu0_200MB.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Read Co-runner - 100 MB/s
echo "+3 Read Co-runner - 100 MB/s"
echo mb 1000 100 100 100 > /sys/kernel/debug/memguard/limit
bandwidth -a read -m 16384 -t 10000 -c 1 &
bandwidth -a read -m 16384 -t 10000 -c 2 &
bandwidth -a read -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/3ReadCR_cpu0_100MB.txt
killall -SIGINT bandwidth
echo "Finished"

####################################
#####    BwWrite Experiments   #####
####################################

#+3 Write Co-runner - 500 MB/s
echo "+3 Write Co-runner - 500 MB/s"
echo mb 1000 500 500 500 > /sys/kernel/debug/memguard/limit
bandwidth -a write -m 16384 -t 10000 -c 1 &
bandwidth -a write -m 16384 -t 10000 -c 2 &
bandwidth -a write -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/3WriteCR_cpu0_500MB.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Write Co-runner - 400 MB/s
echo "+3 Write Co-runner - 400 MB/s"
echo mb 1000 400 400 400 > /sys/kernel/debug/memguard/limit
bandwidth -a write -m 16384 -t 10000 -c 1 &
bandwidth -a write -m 16384 -t 10000 -c 2 &
bandwidth -a write -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/3WriteCR_cpu0_400MB.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Write Co-runner - 300 MB/s
echo "+3 Write Co-runner - 300 MB/s"
echo mb 1000 300 300 300 > /sys/kernel/debug/memguard/limit
bandwidth -a write -m 16384 -t 10000 -c 1 &
bandwidth -a write -m 16384 -t 10000 -c 2 &
bandwidth -a write -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/3WriteCR_cpu0_300MB.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Write Co-runner - 200 MB/s
echo "+3 Write Co-runner - 200 MB/s"
echo mb 1000 200 200 200 > /sys/kernel/debug/memguard/limit
bandwidth -a write -m 16384 -t 10000 -c 1 &
bandwidth -a write -m 16384 -t 10000 -c 2 &
bandwidth -a write -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/3WriteCR_cpu0_200MB.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Write Co-runner - 100 MB/s
echo "+3 Write Co-runner - 100 MB/s"
echo mb 1000 100 100 100 > /sys/kernel/debug/memguard/limit
bandwidth -a write -m 16384 -t 10000 -c 1 &
bandwidth -a write -m 16384 -t 10000 -c 2 &
bandwidth -a write -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/3WriteCR_cpu0_100MB.txt
killall -SIGINT bandwidth
echo "Finished"

#Create new dataset directory and move files to it
mkdir datafiles/DataSet-temp
mv datafiles/ReadCR datafiles/WriteCR datafiles/1* datafiles/2* datafiles/3* datafiles/4* datafiles/DataSet-temp
cd scripts
