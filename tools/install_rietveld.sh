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

# add GSAS-II to Python
export PYTHONPATH=${PYTHONPATH}:${CONDA_PREFIX}/GSASII:${CONDA_PREFIX}/GSASII/fsource

# set path to MAUD for MILK
export MAUD_PATH=/path/to/my/Maud.app

## you can also append to the Anaconda env
## activation script to set env variables when loaded
#mkdir -p ${CONDA_PREFIX}/etc/conda/activate.d
#echo export PYTHONPATH=\$\{PYTHONPATH\}:\$\{CONDA_PREFIX\}/GSASII:\$\{CONDA_PREFIX\}/GSASII/fsource >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
#echo export MAUD_PATH=/path/to/my/Maud.app >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
