timestamp=$(date +%y-%m-%d_%H-%M-%S)

echo "Which board is this test being run on?  Input a string and press [ENTER]"
read board

identification=$board
identification+="_"
identification+=$timestamp

mkdir -p logs/test-model-and-benchmark/$identification
echo "This test will take approximately 30 minutes to complete"
echo "The output files can be found in: logs/test-model/$identification"

echo 2-parallel-single-core
./bandwidth -a write -m 16384 -t 10000 -c 1 &
perf stat -o logs/test-model-and-benchmark/$identification/1-sc-bench_1-sc-model_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model-and-benchmark/$identification/1-sc-bench_1-sc-model_cpu0.txt
jobs -p | xargs kill
echo end 2-parallel-single-core
sleep 300

echo 3-parallel-single-core
./bandwidth -a write -m 16384 -t 10000 -c 1 &
./bandwidth -a write -m 16384 -t 10000 -c 2 &
perf stat -o logs/test-model-and-benchmark/$identification/2-sc-bench_1-sc-model_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model-and-benchmark/$identification/2-sc-bench_1-sc-model_cpu0.txt
jobs -p | xargs kill
echo end 3-parallel-single-core
sleep 300

echo 4-parallel-single-core
./bandwidth -a write -m 16384 -t 10000 -c 1 &
./bandwidth -a write -m 16384 -t 10000 -c 2 &
./bandwidth -a write -m 16384 -t 10000 -c 3 &
perf stat -o logs/test-model-and-benchmark/$identification/3-sc-bench_1-sc-model_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model-and-benchmark/$identification/3-sc-bench_1-sc-model_cpu0.txt
echo end 4-parallel-single-core
sleep 300

echo 1-single-core_1-dual-core
./bandwidth -a write -m 16384 -t 10000 -c 2 &
perf stat -o logs/test-model-and-benchmark/$identification/1-sc-bench_1-dc-model_cpu01_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,1 python test-model.py 2 > logs/test-model-and-benchmark/$identification/1-sc-bench_1-dc-model_cpu01.txt
jobs -p | xargs kill
echo end 2-parallel-dual-core
sleep 300

echo 2-parallel-dual-core
./bandwidth -a write -m 16384 -t 10000 -c 2 &
./bandwidth -a write -m 16384 -t 10000 -c 3 &
perf stat -o logs/test-model-and-benchmark/$identification/2-sc-bench_1-dc-model_cpu01_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,1 python test-model.py 2 > logs/test-model-and-benchmark/$identification/2-sc-bench_1-dc-model_cpu01.txt
jobs -p | xargs kill
echo end 2-parallel-dual-core
sleep 300

echo tri-core
./bandwidth -a write -m 16384 -t 10000 -c 3 &
perf stat -o logs/test-model-and-benchmark/$identifcation/1-sc-bench_1-tc-model_cpu012_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,1,2 python test-model.py 3 > logs/test-model-and-benchmark/$identification/1-sc-bench_1-tc-model_cpu012.txt
jobs -p | xargs kill
echo end tri-core

