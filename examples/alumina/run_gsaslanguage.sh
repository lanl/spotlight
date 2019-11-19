#! /bin/bash

set -e

# make a temporary directory for analysis
mkdir -p tmp_gsaslanguage
cd tmp_gsaslanguage
cp ../al2o3001.gsa ../alumina.cif ../bt1demo.ins .

# intialize the experiment
gsas_initialize al2o3001 "Alumina"

# convert from CIF to EXP
gsas_convert_cif alumina.cif alumina.exp
gsas_read_phase alumina.exp 1

# add histogram
gsas_add_histogram al2o3001.gsa bt1demo.ins 1 0.7

# change the maximum angle to match tutorial
gsas_change_max_tof 1 155

# change initial isotropic termal parameter to match tutorial
gsas_change_atom 1 1:99 UISO 0.025

# refine background
gsas_change_background 1 1 6
gsas_refine 2

# refine lattice parameters
gsas_vary_lattice 1 y
gsas_refine 6
gsas_refine 6

# refine diffractometer zero correction
gsas_vary_DIFC 1 Z
gsas_refine 6

# refine profile parameters
gsas_vary_profile_parameters 1 1 y y y
gsas_refine 6
gsas_refine 4

# constrain thermal motion of all phases and all atoms to be the same
gsas_constrain_atom 1 UISO 1:99
gsas_change_atom 1 1:99 UISO 0.025

# refine atomic position and isotropic thermal parameter
gsas_vary_atom 1 1:99 x
gsas_vary_atom 1 1:99 u
gsas_refine 5

# remove constraint
gsas_constrain_delete 1

# change background
gsas_change_background 1 1 12

# change profile function
gsas_change_profile 1 1 3

# set initial values of profile parameters to match tutorial
gsas_change_profile_parameter 1 1 1 217.09
gsas_change_profile_parameter 1 1 2 -248.45
gsas_change_profile_parameter 1 1 3 158.42
gsas_change_profile_cutoff 1 1 0.5

# refine profile parameters
gsas_vary_profile_parameters 1 1 y y y n n n n n n n n n n n n n n n n n
gsas_refine 4

# create CSV
gsas_write_csv 1 `cat GSAS_EXP` hist1.txt

# plot
spotlight_plot_profile \
    --input-file hist1.txt \
    --profile-file profile.png \
    --residual-file residual.png \
    --reflections-file reflections.png \
    --phase-labels Alumina
convert -append profile.png reflections.png residual.png alumina.pdf

## create PDF
#gsas_done
