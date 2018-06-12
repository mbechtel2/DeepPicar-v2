
﻿#Create directories
cd ..
mkdir datafiles/ReadCR
mkdir datafiles/WriteCR

####################################
#####  Multicore Experiments   #####
####################################

#Solo
echo "Solo"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/1core_0.txt
echo "Finished"

#Dual-Core
echo "Dual-Core"
sudo chrt -f 1 taskset -c 0,3 python test-model.py 2 0 > datafiles/2core_03.txt
echo "Finished"

#Tri-Core
echo "Tri-Core"
sudo chrt -f 1 taskset -c 0,3,4 python test-model.py 3 0 > datafiles/3core_034.txt
echo "Finished"

#Quad-Core
echo "Quad-Core"
sudo chrt -f 1 taskset -c 0,3,4,5 python test-model.py 4 0 > datafiles/4core_0345.txt
echo "Finished"

####################################
#####  Multimodel Experiments  #####
####################################

#Dual-Model
echo "Dual-Model"
sudo chrt -f 1 taskset -c 0,3 python test-model.py 2 0 > datafiles/2model_03.txt &
sudo chrt -f 1 taskset -c 4,5 python test-model2.py 2 > datafiles/2model_45.txt &
wait
echo "Finished"

#Quad-Model
echo "Quad-Model"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/4model_0.txt &
sudo chrt -f 1 taskset -c 3 python test-model2.py 1 > datafiles/4model_3.txt &
sudo chrt -f 1 taskset -c 4 python test-model3.py 1 > datafiles/4model_4.txt &
sudo chrt -f 1 taskset -c 5 python test-model4.py 1 > datafiles/4model_5.txt &
wait
echo "Finished"

####################################
#####  Co-Runner Experiments   #####
####################################

#+1 Read Co-runner
echo "+1 Read Co-runner"
bandwidth -a read -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/1ReadCR_cpu0.txt
echo "Finished"

#+2 Read Co-runner
echo "+2 Read Co-runner"
bandwidth -a read -m 16384 -t 10000 -c 3 &
bandwidth -a read -m 16384 -t 10000 -c 4 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/2ReadCR_cpu0.txt
echo "Finished"

#+3 Read Co-runner
echo "+3 Read Co-runner"
bandwidth -a read -m 16384 -t 10000 -c 3 &
bandwidth -a read -m 16384 -t 10000 -c 4 &
bandwidth -a read -m 16384 -t 10000 -c 5 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/ReadCR/3ReadCR_cpu0.txt
echo "Finished"

#+1 Write Co-runner
echo "+1 Write Co-runner"
bandwidth -a write -m 16384 -t 10000 -c 3 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/1WriteCR_cpu0.txt
echo "Finished"

#+2 Write Co-runner
echo "+2 Write Co-runner"
bandwidth -a write -m 16384 -t 10000 -c 3 &
bandwidth -a write -m 16384 -t 10000 -c 4 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/2WriteCR_cpu0.txt
echo "Finished"

#+3 Write Co-runner
echo "+3 Write Co-runner"
bandwidth -a write -m 16384 -t 10000 -c 3 &
bandwidth -a write -m 16384 -t 10000 -c 4 &
bandwidth -a write -m 16384 -t 10000 -c 5 &
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/WriteCR/3WriteCR_cpu0.txt
echo "Finished"

#Create new dataset directory and move files to it
mkdir datafiles/DataSet-temp
mv datafiles/ReadCR datafiles/WriteCR datafiles/1* datafiles/2* datafiles/3* datafiles/4* datafiles/DataSet-temp
cd scripts
