#! /bin/bash

set -e

# store location of this script
TOOLS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# load Anaconda and GCC
module purge
module load anaconda/Anaconda3.2019.03 gcc/6.4.0

# run install script
cd ${TOOLS_DIR}
source install.sh --proxy 'proxyout.lanl.gov\n8080'

# install glibc and X11 libraries
cd ${CONDA_PREFIX}
git clone git@gitlab.lanl.gov:cmbiwer/spotlight-rpm.git rpms
cd rpms
for RPM in `ls *.rpm`; do rpm2cpio ${RPM} | cpio -id; done
for EXE in `ls ${CONDA_PREFIX}/gsas/exe/*`; do
    patchelf --set-interpreter ${PWD}/lib/ld-linux.so.2 ${EXE}
done

