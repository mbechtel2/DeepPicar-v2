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
perf stat -o logs/test-model/$identification/single-core_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model/$identification/single-core.txt &
wait
echo end single-core

echo 2-parallel-single-core
perf stat -o logs/test-model/$identification/2-single-core_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model/$identification/2-single-core_cpu0.txt &
perf stat -o logs/test-model/$identification/2-single-core_cpu3_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 3 python test-model.py 1 > logs/test-model/$identification/2-single-core_cpu3.txt &
wait
echo end 2-parallel-single-core

echo 3-parallel-single-core
perf stat -o logs/test-model/$identification/3-single-core_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model/$identification/3-single-core_cpu0.txt &
perf stat -o logs/test-model/$identification/3-single-core_cpu3_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 3 python test-model.py 1 > logs/test-model/$identification/3-single-core_cpu3.txt &
perf stat -o logs/test-model/$identification/3-single-core_cpu4_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 4 python test-model.py 1 > logs/test-model/$identification/3-single-core_cpu4.txt &
wait
echo end 3-parallel-single-core

echo 4-parallel-single-core
perf stat -o logs/test-model/$identification/4-single-core_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model/$identification/4-single-core_cpu0.txt &
perf stat -o logs/test-model/$identification/4-single-core_cpu3_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 3 python test-model.py 1 > logs/test-model/$identification/4-single-core_cpu3.txt &
perf stat -o logs/test-model/$identification/4-single-core_cpu4_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 4 python test-model.py 1 > logs/test-model/$identification/4-single-core_cpu4.txt &
perf stat -o logs/test-model/$identification/4-single-core_cpu5_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 5 python test-model.py 1 > logs/test-model/$identification/4-single-core_cpu5.txt &
wait
echo end 4-parallel-single-core

echo dual-core
perf stat -o logs/test-model/$identification/dual-core_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,3 python test-model.py 2 > logs/test-model/$identification/dual-core.txt &
wait
echo end dual-core

echo 2-parallel-dual-core
perf stat -o logs/test-model/$identification/2-dual-core_cpu03_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,3 python test-model.py 2 > logs/test-model/$identification/2-dual-core_cpu03.txt &
perf stat -o logs/test-model/$identification/2-dual-core_cpu45_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 4,5 python test-model.py 2 > logs/test-model/$identification/2-dual-core_cpu45.txt &
wait
echo end 2-parallel-dual-core

echo tri-core
perf stat -o logs/test-model/$identification/tri-core_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,3,4 python test-model.py 3 > logs/test-model/$identification/tri-core.txt &
wait
echo end tri-core

echo quad-core
perf stat -o logs/test-model/$identification/quad-core_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,3,4,5 python test-model.py 4 > logs/test-model/$identification/quad-core.txt &
wait
echo end quad-core

