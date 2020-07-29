#! /bin/bash

set -e

# set name of env
ENV_NAME="spotlight"

# store location of this script
TOOLS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# clean env
module purge
module load anaconda/Anaconda3.2019.03
source deactivate
conda env remove --yes --name ${ENV_NAME}

# create Anaconda env
cd ${TOOLS_DIR}
bash install.sh ${ENV_NAME}

# load anaconda env
source activate ${ENV_NAME}

# install patchelf
mkdir -p ${CONDA_PREFIX}/src && cd ${CONDA_PREFIX}/src
git clone -b 0.10 https://github.com/NixOS/patchelf.git
cd patchelf
./bootstrap.sh
./configure --prefix=${CONDA_PREFIX}
make install

# install glibc and X11 libraries
cd ${CONDA_PREFIX}
git clone git@gitlab.lanl.gov:cmbiwer/spotlight-rpm.git rpms
cd rpms
for RPM in `ls *.rpm`; do rpm2cpio ${RPM} | cpio -id; done
for EXE in `ls ${CONDA_PREFIX}/gsas/exe/*`; do
patchelf --set-interpreter ${PWD}/lib/ld-linux.so.2 ${EXE}
done
