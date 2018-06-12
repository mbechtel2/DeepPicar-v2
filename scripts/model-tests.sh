
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
sudo chrt -f 1 taskset -c 0,1 python test-model.py 2 0 > datafiles/2core_01.txt
echo "Finished"

#Tri-Core
echo "Tri-Core"
sudo chrt -f 1 taskset -c 0,1,2 python test-model.py 3 0 > datafiles/3core_012.txt
echo "Finished"

#Quad-Core
echo "Quad-Core"
sudo chrt -f 1 taskset -c 0,1,2,3 python test-model.py 4 0 > datafiles/4core_0123.txt
echo "Finished"

####################################
#####  Multimodel Experiments  #####
####################################

#Dual-Model
echo "Dual-Model"
sudo chrt -f 1 taskset -c 0,1 python test-model.py 2 0 > datafiles/2model_01.txt &
sudo chrt -f 1 taskset -c 2,3 python test-model2.py 2 > datafiles/2model_23.txt &
wait
echo "Finished"

#Quad-Model
echo "Quad-Model"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 0 > datafiles/4model_0.txt &
sudo chrt -f 1 taskset -c 1 python test-model2.py 1 > datafiles/4model_1.txt &
sudo chrt -f 1 taskset -c 2 python test-model3.py 1 > datafiles/4model_2.txt &
sudo chrt -f 1 taskset -c 3 python test-model4.py 1 > datafiles/4model_3.txt &
wait
echo "Finished"

####################################
#####  Co-Runner Experiments   #####
####################################

#+1 Read Co-runner
echo "+1 Read Co-runner"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 1 read > datafiles/ReadCR/1ReadCR_cpu0.txt
echo "Finished"

#+2 Read Co-runner
echo "+2 Read Co-runner"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 2 read > datafiles/ReadCR/2ReadCR_cpu0.txt
echo "Finished"

#+3 Read Co-runner
echo "+3 Read Co-runner"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 3 read > datafiles/ReadCR/3ReadCR_cpu0.txt
echo "Finished"

#+1 Write Co-runner
echo "+1 Write Co-runner"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 1 write > datafiles/WriteCR/1WriteCR_cpu0.txt
echo "Finished"

#+2 Write Co-runner
echo "+2 Write Co-runner"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 2 write > datafiles/WriteCR/2WriteCR_cpu0.txt
echo "Finished"

#+3 Write Co-runner
echo "+3 Write Co-runner"
sudo chrt -f 1 taskset -c 0 python test-model.py 1 3 write > datafiles/WriteCR/3WriteCR_cpu0.txt
echo "Finished"

#Create new dataset directory and move files to it
mkdir datafiles/DataSet-temp
mv datafiles/ReadCR datafiles/WriteCR datafiles/1* datafiles/2* datafiles/3* datafiles/4* datafiles/DataSet-temp
cd scripts
