#! /bin/bash

set -e

# make a temporary directory for analysis
mkdir -p tmp
cd tmp

# run optimization search in parallel
spotlight_minimize --config-files ../config_analytical.py

# print best result
spotlight_inspect --input-file solution.db

# plot
python ../spotlight_interpolate.py \
    --input-file solution.db \
    --output-file gauss2d.png

# back to original directory
cd ..

