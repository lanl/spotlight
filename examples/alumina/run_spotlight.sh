#! /bin/bash

set -e

# make a temporary directory for analysis
mkdir -p tmp_spotlight
cd tmp_spotlight
cp ../al2o3001.gsa ../alumina.cif ../bt1demo.ins .
cp ../config_base.ini ../config_alumina.ini ../plan_alumina.py .

# convert from CIF to EXP
gsas_convert_cif alumina.cif alumina.exp

# run optimazation search
mpirun --oversubscribe -n `getconf _NPROCESSORS_ONLN` spotlight_minimize \
    --config-files \
        config_base.ini \
        config_alumina.ini \
    --config-overrides \
        phases:phase_1-file:alumina.exp \
        phases:phase_1-number:1 \
    --data-file al2o3001.gsa \
    --refinement-plan-file plan_alumina.py \
    --output-file solution_alumina.pkl \
    --tmp-dir tmp_alumina \
    --num-solvers 1 \
    --seed 123 \
    --tag alumina

# setup gsas for global minima
# do not plot though
spotlight_plot_minima \
    --input-files solution_alumina.pkl \
    --config-file tmp_alumina_0/config.ini \
    --data-file al2o3001.gsa \
    --refinement-plan-file plan_alumina.py \
    --tmp-dir tmp_minima

# make CSV
cd tmp_minima
gsas_write_csv 1 TRIAL hist1.txt

# plot
spotlight_plot_profile \
    --input-file hist1.TXT \
    --profile-file profile.png \
    --residual-file residual.png \
    --reflections-file reflections.png \
    --phase-labels Alumina
convert -append profile.png reflections.png residual.png alumina.pdf

## make PDF
#gsas_done
