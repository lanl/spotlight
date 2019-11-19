#! /bin/bash

set -e

# loop over number of local optimizations per thread
for N in 2 8 32; do

# make a temporary directory for analysis
cd ..
mkdir -p tmp_map_${N}
cd tmp_map_${N}
cp ../config_base.ini ../plan_analytical.py .

# random seed
SEED=321

# set the number of threads to use for parallel regions
export OMP_NUM_THREADS=1

# run optimization search in parallel
# profile the execution
mpirun --oversubscribe -n 4 \
    python -m cProfile -o analytical.pstat `which spotlight_minimize` \
    --config-files \
        config_base.ini \
    --config-overrides \
        configuration:seed:${SEED} \
        configuration:tag:${SEED} \
        configuration:num_solvers:${N} \
    --tmp-dir tmp

# random seed
SEED=123

# set the number of threads to use for parallel regions
export OMP_NUM_THREADS=1

# run optimization search in parallel
# profile the execution
mpirun --oversubscribe -n 4 \
    python -m cProfile -o analytical.pstat `which spotlight_minimize` \
    --config-files \
        config_base.ini \
    --config-overrides \
        configuration:seed:${SEED} \
        configuration:tag:${SEED} \
        configuration:num_solvers:${N} \
        surface:sign:-1 \
    --tmp-dir tmp

# plot
python ../spotlight_interpolate.py \
    --input-file solution.db \
    --output-file ../map_${N}.png \
    --abs

done
