#! /bin/bash

set -e

# make a temporary directory for analysis
mkdir -p tmp_spotlight
cd tmp_spotlight
cp ../al2o3001.gsa ../alumina.cif ../bt1demo.ins .
cp ../config_base.ini ../config_alumina.ini ../plan_alumina.py .

# convert from CIF to EXP
gsas_convert_cif alumina.cif alumina.exp

# random seed
SEED=123

# set the number of threads to use for parallel regions
export OMP_NUM_THREADS=1

# run optimization search in parallel
# profile the execution
mpirun --oversubscribe -n `getconf _NPROCESSORS_ONLN` \
    python -m cProfile -o alumina.pstat `which spotlight_minimize` \
    --config-files \
        config_base.ini \
        config_alumina.ini \
    --config-overrides \
        phases:phase_1-file:alumina.exp \
        phases:phase_1-number:1 \
    --data-file al2o3001.gsa \
    --refinement-plan-file plan_alumina.py \
    --output-file solution.db \
    --state-file state.db \
    --tmp-dir tmp_alumina \
    --num-solvers 1 \
    --seed ${SEED} \
    --tag alumina_${SEED}

# setup GSAS for global minima from optimization search
# do not plot though
spotlight_plot_minima \
    --input-files solution.db \
    --config-file tmp_alumina_0/config.ini \
    --data-file al2o3001.gsa \
    --refinement-plan-file plan_alumina.py \
    --tmp-dir tmp_minima

# make CSV and plot results for each histogram
cd tmp_minima
for IDX in 1; do
gsas_write_csv ${IDX} TRIAL hist_${IDX}.txt
spotlight_plot_profile \
    --input-file hist_${IDX}.txt \
    --profile-file profile_${IDX}.png \
    --residual-file residual_${IDX}.png \
    --reflections-file reflections_${IDX}.png \
    --phase-labels Alumina
convert -coalesce profile_${IDX}.png reflections_${IDX}.png residual_${IDX}.png alumina_${IDX}.pdf
done

# plot profiling information
# requires gprof2dot which is not an explicit dependency of Spotlight
# so check if it is installed first
if [ -x "$(command -v gprof2dot)" ]; then
for IDX in $(seq 0 $((`getconf _NPROCESSORS_ONLN` - 1))); do
gprof2dot -f pstats tmp_spotlight/tmp_alumina_${IDX}/alumina.pstat | dot -Tpdf -o tmp_pstat_${IDX}.pdf
done
fi

## make PDF
#gsas_done
