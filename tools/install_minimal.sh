#! /bin/bash

# create and load a virtual environment
conda create --yes --name spotlight python=3.7.3
conda activate spotlight

# install MPI with Python bindings, Mystic, and Spotlight
conda install --yes mpi4py==3.0.3
python -m pip install klepto==0.1.7 https://github.com/uqfoundation/mystic/archive/5b73d70.tar.gz
python -m pip install https://github.com/lanl/spotlight/archive/28128d9.tar.gz
