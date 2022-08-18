# /bin/bash

set -e 

# install and load Anaconda env
conda env create -f environment_rietveld.yaml
conda activate spotlight-rietveld

# set path to MAUD for MILK
export MAUD_PATH=/path/to/my/Maud.app

