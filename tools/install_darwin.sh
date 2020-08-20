#! /bin/bash

set -e

# store location of this script
TOOLS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# store Python version
PYTHON_VERSION=3.7.3

# clean env
module purge
module load anaconda/Anaconda3.2019.03

# run install script
cd ${TOOLS_DIR}
bash install.sh

# install glibc and X11 libraries
cd ${CONDA_PREFIX}
git clone git@gitlab.lanl.gov:cmbiwer/spotlight-rpm.git rpms
cd rpms
for RPM in `ls *.rpm`; do rpm2cpio ${RPM} | cpio -id; done
for EXE in `ls ${CONDA_PREFIX}/gsas/exe/*`; do
patchelf --set-interpreter ${PWD}/lib/ld-linux.so.2 ${EXE}
done

