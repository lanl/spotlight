# /bin/bash

set -e 

# install and load Anaconda env
conda env create -f environment_rietveld.yaml
conda activate spotlight-rietveld

# build GSAS-II
cd ${CONDA_PREFIX}/GSASII
./bootstrap.py
cd fsource
scons

# append env activation script
mkdir -p ${CONDA_PREFIX}/etc/conda/activate.d
echo export PYTHONPATH=\$\{PYTHONPATH\}:\$\{CONDA_PREFIX\}/GSASII:\$\{CONDA_PREFIX\}/GSASII/fsource >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export MAUD=/opt/Maud_2p99 >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
