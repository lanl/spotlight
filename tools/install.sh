#! /bin/bash

set -e

# store location of this script
TOOLS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# store Python version
PYTHON_VERSION=3.7.3

# import Anaconda functions into bash script
source ${CONDA_PREFIX}/etc/profile.d/conda.sh

# clean env
conda activate
conda env remove --yes --name spotlight

# create Anaconda env
conda create --yes --name spotlight python=${PYTHON_VERSION}
conda activate spotlight

# install GSAS which requires Python 2.7 for installation scripts
conda install --yes python==2.7.16
mkdir -p ${CONDA_PREFIX}/gsas && cd ${CONDA_PREFIX}/gsas
cp ${TOOLS_DIR}/bootstrap.py .
echo $'proxyout.lanl.gov\n8080' >> proxy.txt
python bootstrap.py < proxy.txt
rm proxy.txt
conda install --yes python==${PYTHON_VERSION}

# install gsaslanguage scripts and fix some issues
cd ${CONDA_PREFIX}/gsas
git clone https://github.com/Svennito/gsaslanguage.git scripts
cd scripts
git reset --hard 8f09750
chmod +x ${CONDA_PREFIX}/gsas/scripts/gsas_get_current_wtfrac_esd
OS_NAME=`uname -a`
if [[ ${OS_NAME} =~ "Darwin" ]]; then
    sed -i '' '42s/^/#/' ${CONDA_PREFIX}/gsas/scripts/gsas_vary_profile_parameters
else
    sed -i '42s/^/#/' ${CONDA_PREFIX}/gsas/scripts/gsas_vary_profile_parameters
fi

# install required packages
conda install --yes pkg-config==0.29.2

# install optional packages
conda install --yes --channel conda-forge imagemagick

# install OpenMPI
mkdir -p ${CONDA_PREFIX}/src && cd ${CONDA_PREFIX}/src
wget https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.3.tar.gz
tar -xvf openmpi-2.1.3.tar.gz
cd openmpi-2.1.3
CFLAGS=-O3 \
CXXFLAGS=-O3 \
./configure --prefix=${CONDA_PREFIX}
make -j $(getconf _NPROCESSORS_ONLN) install

# install Python packages
python -m pip install --upgrade pip
python -m pip install --requirement ${TOOLS_DIR}/../requirements.txt

# install Spotlight
cd ${TOOLS_DIR}/..
python setup.py install

# append env activation script
mkdir -p ${CONDA_PREFIX}/etc/conda/activate.d
echo export PGPLOT_FONT=\$\{CONDA_PREFIX\}/pgl/grfont.dat >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export gsas=\$\{CONDA_PREFIX\}/gsas >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export PATH=\$\{PATH\}:\$\{gsas\}/exe:\$\{gsas\}/scripts >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
