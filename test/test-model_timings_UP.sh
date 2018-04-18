timestamp=$(date +%y-%m-%d_%H-%M-%S)

echo "Which board is this test being run on?  Input a string and press [ENTER]"
read board

identification=$board
identification+="_"
identification+=$timestamp

mkdir -p logs/test-model/$identification
echo "This test will take approximately 45 minutes to complete"
echo "The output files can be found in: logs/test-model/$identification"

echo single-core
perf stat -o logs/test-model/$identification/single-core_perf.txt -e cache-misses,cache-references taskset -c 0 python test-model.py 1 > logs/test-model/$identification/single-core.txt &
wait
echo end single-core
sleep 300

echo 2-parallel-single-core
perf stat -o logs/test-model/$identification/2-single-core_cpu0_perf.txt -e cache-misses,cache-references taskset -c 0 python test-model.py 1 > logs/test-model/$identification/2-single-core_cpu0.txt &
perf stat -o logs/test-model/$identification/2-single-core_cpu1_perf.txt -e cache-misses,cache-references taskset -c 1 python test-model.py 1 > logs/test-model/$identification/2-single-core_cpu1.txt &
wait
echo end 2-parallel-single-core
sleep 300

echo 3-parallel-single-core
perf stat -o logs/test-model/$identification/3-single-core_cpu0_perf.txt -e cache-misses,cache-references taskset -c 0 python test-model.py 1 > logs/test-model/$identification/3-single-core_cpu0.txt &
perf stat -o logs/test-model/$identification/3-single-core_cpu1_perf.txt -e cache-misses,cache-references taskset -c 1 python test-model.py 1 > logs/test-model/$identification/3-single-core_cpu1.txt &
perf stat -o logs/test-model/$identification/3-single-core_cpu2_perf.txt -e cache-misses,cache-references taskset -c 2 python test-model.py 1 > logs/test-model/$identification/3-single-core_cpu2.txt &
wait
echo end 3-parallel-single-core
sleep 300

echo 4-parallel-single-core
perf stat -o logs/test-model/$identification/4-single-core_cpu0_perf.txt -e cache-misses,cache-references taskset -c 0 python test-model.py 1 > logs/test-model/$identification/4-single-core_cpu0.txt &
perf stat -o logs/test-model/$identification/4-single-core_cpu1_perf.txt -e cache-misses,cache-references taskset -c 1 python test-model.py 1 > logs/test-model/$identification/4-single-core_cpu1.txt &
perf stat -o logs/test-model/$identification/4-single-core_cpu2_perf.txt -e cache-misses,cache-references taskset -c 2 python test-model.py 1 > logs/test-model/$identification/4-single-core_cpu2.txt &
perf stat -o logs/test-model/$identification/4-single-core_cpu3_perf.txt -e cache-misses,cache-references taskset -c 3 python test-model.py 1 > logs/test-model/$identification/4-single-core_cpu3.txt &
wait
echo end 4-parallel-single-core
sleep 300

echo dual-core
perf stat -o logs/test-model/$identification/dual-core_perf.txt -e cache-misses,cache-references taskset -c 0,1 python test-model.py 2 > logs/test-model/$identification/dual-core.txt &
wait
echo end dual-core
sleep 300

echo 2-parallel-dual-core
perf stat -o logs/test-model/$identification/2-dual-core_cpu01_perf.txt -e cache-misses,cache-references taskset -c 0,1 python test-model.py 2 > logs/test-model/$identification/2-dual-core_cpu01.txt &
perf stat -o logs/test-model/$identification/2-dual-core_cpu23_perf.txt -e cache-misses,cache-references taskset -c 2,3 python test-model.py 2 > logs/test-model/$identification/2-dual-core_cpu23.txt &
wait
echo end 2-parallel-dual-core
sleep 300

echo tri-core
perf stat -o logs/test-model/$identification/tri-core_perf.txt -e cache-misses,cache-references taskset -c 0,1,2 python test-model.py 3 > logs/test-model/$identification/tri-core.txt &
wait
echo end tri-core
sleep 300

echo quad-core
perf stat -o logs/test-model/$identification/quad-core_perf.txt -e cache-misses,cache-references taskset -c 0,1,2,3 python test-model.py 4 > logs/test-model/$identification/quad-core.txt &
wait
echo end quad-core
sleep 300

