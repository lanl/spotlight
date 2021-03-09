#! /bin/bash

set -e

# make a temporary directory for analysis
mkdir -p tmp
cd tmp

# set the number of threads to use for parallel regions
export OMP_NUM_THREADS=1

# run optimization search in parallel
# profile the execution
mpirun spotlight_minimize --config-files ../config_analytical.py

# print best result
spotlight_inspect --input-file solution.db

# plot
python ../spotlight_interpolate.py \
    --input-file solution.db \
    --output-file gauss2d.png

# back to original directory
cd ..

