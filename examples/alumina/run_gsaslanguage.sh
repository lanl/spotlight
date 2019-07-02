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
gsas_add_histogram al2o3001.gsa bt1demo.ins 1 1.0 5.0

# refine background
gsas_change_background 1 1 6
gsas_refine 20

# refine histogram scale
gsas_vary_histogram_scale 1 y
gsas_refine 20

# refine lattice parameters
gsas_vary_lattice 1 y
gsas_refine 20

# refine phase fractions
gsas_vary_phase 1 y
gsas_refine 20

# refine diffractometer constant
gsas_vary_DIFC 1 C
gsas_refine 20

# refine profile parameters
gsas_vary_profile_parameters 1 1 y y y
gsas_refine 20

# refine atomic position and isotropic thermal parameter
gsas_vary_atom 1 1:99 x 9
gsas_vary_atom 1 1:99 u 9
gsas_refine 20

# create PDF
gsas_done
