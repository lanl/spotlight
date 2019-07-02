#! /bin/bash

set -e

# make a temporary directory for analysis
mkdir -p tmp_spotlight
cd tmp_spotlight
cp ../al2o3001.gsa ../alumina.cif ../bt1demo.ins .
cp ../config_base.ini ../config_alumina.ini ../plan_alumina.py .

# convert from CIF to EXP
gsas_convert_cif alumina.cif alumina.exp

# run
mpirun -n 4 spotlight_minimize \
    --config-overrides \
        phases:phase_1-file:alumina.exp \
        phases:phase_1-number:1 \
    --output-file solution_alumina.pkl \
    --config-files \
        config_base.ini \
        config_alumina.ini \
    --data-file al2o3001.gsa \
    --refinement-plan-file plan_alumina.py \
    --tag alumina \
    --tmp-dir tmp_alumina \
    --num-solvers 1 \
    --seed 123

