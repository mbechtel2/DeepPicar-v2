
#Enable PALLOC
sudo ./palloc-setup.sh

#Create directories
cd ..
mkdir datafiles/ReadCR
mkdir datafiles/WriteCR

####################################
#####     Solo Experiments     #####
####################################

#Solo - 100%
echo "Solo - 100%"
echo $$ > /sys/fs/cgroup/palloc/part8/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_100.txt
echo "Finished"

#Solo - 75%
echo "Solo - 75%"
echo $$ > /sys/fs/cgroup/palloc/part7/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_75.txt
echo "Finished"

#Solo - 50%
echo "Solo - 50%"
echo $$ > /sys/fs/cgroup/palloc/part5/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_50.txt
echo "Finished"

#Solo - 25%
echo "Solo - 25%"
echo $$ > /sys/fs/cgroup/palloc/part1/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0_25.txt
echo "Finished"

####################################
#####  Co-Runner Experiments   #####
####################################

#+1 Read Co-runner
echo "+1 Read Co-runner"
echo $$ > /sys/fs/cgroup/palloc/part2/tasks
bandwidth -a write -m 16384 -t 10000 -c 1 &

echo $$ > /sys/fs/cgroup/palloc/part1/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/1ReadCR_cpu0.txt
killall -SIGINT bandwidth
echo "Finished"

#+2 Read Co-runner
echo "+2 Read Co-runner"
echo $$ > /sys/fs/cgroup/palloc/part2/tasks
bandwidth -a write -m 16384 -t 10000 -c 1 &

echo $$ > /sys/fs/cgroup/palloc/part3/tasks
bandwidth -a write -m 16384 -t 10000 -c 2 &

echo $$ > /sys/fs/cgroup/palloc/part1/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/2ReadCR_cpu0.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Read Co-runner
echo "+3 Read Co-runner"
echo $$ > /sys/fs/cgroup/palloc/part2/tasks
bandwidth -a write -m 16384 -t 10000 -c 1 &

echo $$ > /sys/fs/cgroup/palloc/part3/tasks
bandwidth -a write -m 16384 -t 10000 -c 2 &

echo $$ > /sys/fs/cgroup/palloc/part4/tasks
bandwidth -a write -m 16384 -t 10000 -c 3 &

echo $$ > /sys/fs/cgroup/palloc/part1/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0> datafiles/ReadCR/3ReadCR_cpu0.txt
killall -SIGINT bandwidth
echo "Finished"

#+1 Write Co-runner
echo "+1 Write Co-runner"
echo $$ > /sys/fs/cgroup/palloc/part2/tasks
bandwidth -a write -m 16384 -t 10000 -c 1 &

echo $$ > /sys/fs/cgroup/palloc/part1/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/1WriteCR_cpu0.txt
killall -SIGINT bandwidth
echo "Finished"

#+2 Write Co-runner
echo "+2 Write Co-runner"
echo $$ > /sys/fs/cgroup/palloc/part2/tasks
bandwidth -a write -m 16384 -t 10000 -c 1 &

echo $$ > /sys/fs/cgroup/palloc/part3/tasks
bandwidth -a write -m 16384 -t 10000 -c 2 &

echo $$ > /sys/fs/cgroup/palloc/part1/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/2WriteCR_cpu0.txt
killall -SIGINT bandwidth
echo "Finished"

#+3 Write Co-runner
echo "+3 Write Co-runner"
echo $$ > /sys/fs/cgroup/palloc/part2/tasks
bandwidth -a write -m 16384 -t 10000 -c 1 &

echo $$ > /sys/fs/cgroup/palloc/part3/tasks
bandwidth -a write -m 16384 -t 10000 -c 2 &

echo $$ > /sys/fs/cgroup/palloc/part4/tasks
bandwidth -a write -m 16384 -t 10000 -c 3 &

echo $$ > /sys/fs/cgroup/palloc/part1/tasks
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/3WriteCR_cpu0.txt
killall -SIGINT bandwidth
echo "Finished"

#Create new dataset directory and move files to it
mkdir datafiles/DataSet-temp
mv datafiles/ReadCR datafiles/WriteCR datafiles/1* datafiles/DataSet-temp
cd scripts
