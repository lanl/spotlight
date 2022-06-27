#! /bin/bash

set -e

# if MPI is installed then use it
if ! [ -x "$(command -v mpirun)" ]; then
    export OMP_NUM_THREADS=1
    EXE="mpirun --oversubscribe -n 4 python -m cProfile -o analytical.pstat `which spotlight_minimize`"
else
    EXE=`which spotlight_minimize`
fi

# loop over number of local optimizations per thread
for N in 2 8 32; do

    # make a temporary directory for analysis
    mkdir -p tmp_map_${N}
    cd tmp_map_${N}
    
    # random seed
    SEED=321
    
    # run optimization search
    ${EXE} --config-files ../config_analytical.py \
           --config-overrides \
               configuration:seed:${SEED} \
               configuration:num_solvers:${N} \
           --tmp-dir tmp
    
    # random seed
    SEED=123
    
    # run optimization search
    ${EXE} --config-files ../config_analytical.py \
           --config-overrides \
               configuration:seed:${SEED} \
               configuration:num_solvers:${N} \
               surface:sign:-1 \
           --tmp-dir tmp
    
    # plot
    python ../spotlight_interpolate.py \
        --input-file solution.db \
        --output-file ../map_${N}.png \
        --abs
    
    # back to original directory
    cd ..

done
