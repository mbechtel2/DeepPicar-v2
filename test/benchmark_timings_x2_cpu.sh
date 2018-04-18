timestamp=$(date +%y-%m-%d_%H-%M-%S)

echo "Which board is this test being run on?  Input a string and press [ENTER]"
read board

identification=$board
identification+="_"
identification+=$timestamp

mkdir -p logs/test-model-and-benchmark/$identification
echo "This test will take approximately 45 minutes to complete"
echo "The output files can be found in: logs/test-model/$identification"

echo 2-parallel-single-core
./bandwidth -a write -m 16384 -t 10000 -c 3 &
CUDA_VISIBLE_DEVICES='' perf stat -o logs/test-model-and-benchmark/$identification/1-sc-bench_1-sc-model_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model-and-benchmark/$identification/1-sc-bench_1-sc-model_cpu0.txt
jobs -p | xargs kill
echo end 2-parallel-single-core

echo 3-parallel-single-core
./bandwidth -a write -m 16384 -t 10000 -c 3 &
./bandwidth -a write -m 16384 -t 10000 -c 4 &
CUDA_VISIBLE_DEVICES='' perf stat -o logs/test-model-and-benchmark/$identification/2-sc-bench_1-sc-model_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model-and-benchmark/$identification/2-sc-bench_1-sc-model_cpu0.txt
jobs -p | xargs kill
echo end 3-parallel-single-core

echo 4-parallel-single-core
./bandwidth -a write -m 16384 -t 10000 -c 3 &
./bandwidth -a write -m 16384 -t 10000 -c 4 &
./bandwidth -a write -m 16384 -t 10000 -c 5 &
CUDA_VISIBLE_DEVICES='' perf stat -o logs/test-model-and-benchmark/$identification/3-sc-bench_1-sc-model_cpu0_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0 python test-model.py 1 > logs/test-model-and-benchmark/$identification/3-sc-bench_1-sc-model_cpu0.txt
echo end 4-parallel-single-core

echo 1-single-core_1-dual-core
./bandwidth -a write -m 16384 -t 10000 -c 4 &
CUDA_VISIBLE_DEVICES='' perf stat -o logs/test-model-and-benchmark/$identification/1-sc-bench_1-dc-model_cpu03_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,3 python test-model.py 2 > logs/test-model-and-benchmark/$identification/1-sc-bench_1-dc-model_cpu03.txt
jobs -p | xargs kill
echo end 2-parallel-dual-core

echo 2-parallel-dual-core
./bandwidth -a write -m 16384 -t 10000 -c 4 &
./bandwidth -a write -m 16384 -t 10000 -c 5 &
CUDA_VISIBLE_DEVICES='' perf stat -o logs/test-model-and-benchmark/$identification/2-sc-bench_1-dc-model_cpu03_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,3 python test-model.py 2 > logs/test-model-and-benchmark/$identification/2-sc-bench_1-dc-model_cpu03.txt
jobs -p | xargs kill
echo end 2-parallel-dual-core

echo tri-core
./bandwidth -a write -m 16384 -t 10000 -c 5 &
CUDA_VISIBLE_DEVICES='' perf stat -o logs/test-model-and-benchmark/$identification/1-sc-bench_1-tc-model_cpu034_perf.txt -e cache-misses,cache-references,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses taskset -c 0,3,4 python test-model.py 3 > logs/test-model-and-benchmark/$identification/1-sc-bench_1-tc-model_cpu034.txt
jobs -p | xargs kill
echo end tri-core

