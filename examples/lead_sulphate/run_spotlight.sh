#! /bin/bash
#SBATCH --constraint cpu_model:E5-2660_v3
#SBATCH --time 600
#SBATCH --nodes 1
#SBATCH --ntasks-per-core 40

set -e

# Can be used to override using MPI ("" for true, false otherwise)
USE_MPI=""

# random seed
SEED=${1}
SEED=${SEED:=123}

# if MPI is installed then use it
if [ -x "$(command -v mpirun)" ] && [ $USE_MPIRUN ]; then
    export OMP_NUM_THREADS=1
    EXE="mpirun --oversubscribe -n 4 python -m cProfile -o analytical.pstat `which spotlight_minimize`"
else
    EXE=`which spotlight_minimize`
fi

# make a temporary directory for analysis
mkdir -p tmp_spotlight_${SEED}
cd tmp_spotlight_${SEED}
cp ../INST_XRY.prm ../inst_d1a.prm ../PBSO4.cwn ../PBSO4.xra ../PbSO4-Wyckoff.cif .
cp ../config_pbso4.py .

# run optimization search
${EXE} \
    --config-files \
        config_pbso4.py \
    --config-overrides \
        configuration:seed:${SEED} \
        configuration:tag:${SEED} \
    --tmp-dir tmp

# setup GSAS-II for global minima from optimization search
spotlight_gsas_setup \
    --input-files solution.db \
    --tmp-dir tmp_minima

# make CSV file and plot results for each histogram
# create a PDF containing all images
# requires convert which is not an explicit dependency of Spotlight
# so check if it is installed first
cd tmp_minima
for IDX in 0 1; do
gsasii_write_csv \
    --input-file step_2.gpx \
    --output-file hist_${IDX}.txt \
    --histogram ${IDX}
spotlight_plot_profile \
    --input-file hist_${IDX}.txt \
    --profile-file profile_${IDX}.png \
    --residual-file residual_${IDX}.png \
    --reflections-file reflections_${IDX}.png \
    --phase-labels PBSO4
if [ -x "$(command -v convert)" ]; then
convert -coalesce profile_${IDX}.png reflections_${IDX}.png residual_${IDX}.png lead_sulphate_${IDX}.pdf
fi
done
mv *.png *.pdf ..
cd ..

