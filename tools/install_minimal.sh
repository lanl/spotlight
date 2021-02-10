#! /bin/bash

set -e

# create and load a virtual environment
conda create --yes --name spotlight python=3.7.3
conda activate spotlight

# install klepto, Mystic, and Spotlight
python -m pip install klepto==0.1.7 https://github.com/uqfoundation/mystic/archive/5b73d70.tar.gz
python -m pip install https://github.com/lanl/spotlight/archive/master.tar.gz
