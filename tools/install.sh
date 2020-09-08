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

# install GSAS-II
# must be installed from base environment
conda install --yes --channel briantoby --name spotlight gsas2pkg=1.1

# enter Anaconda env
conda activate spotlight

# install GSAS which requires Python 2.7 for installation scripts
conda install --yes --channel anaconda svn==1.9.7
mkdir -p ${CONDA_PREFIX}/gsas && cd ${CONDA_PREFIX}/gsas
curl https://subversion.xray.aps.anl.gov/trac/EXPGUI/browser/gsas/linux/dist/bootstrap.py?format=txt > bootstrap.py
echo $'proxyout.lanl.gov\n8080' >> proxy.txt
python2 bootstrap.py < proxy.txt
rm proxy.txt

# install gsaslanguage scripts and fix some issues
cd ${CONDA_PREFIX}/gsas
git clone https://github.com/Svennito/gsaslanguage.git scripts
cd scripts
git reset --hard fe73549
chmod +x ${CONDA_PREFIX}/gsas/scripts/gsas_get_current_wtfrac_esd

# install OpenMPI
conda install --yes gxx_linux-64
mkdir -p ${CONDA_PREFIX}/src && cd ${CONDA_PREFIX}/src
wget https://www.open-mpi.org/software/ompi/v3.0/downloads/openmpi-3.0.6.tar.gz
tar -xvf openmpi-3.0.6.tar.gz
cd openmpi-3.0.6
CFLAGS=-O3 \
CXXFLAGS=-O3 \
./configure --prefix=${CONDA_PREFIX}
make -j $(getconf _NPROCESSORS_ONLN) install

# install Python packages for Spotlight
python -m pip install --upgrade pip
python -m pip install --requirement ${TOOLS_DIR}/../requirements.txt

# construct GSAS-II
conda install --yes scons==3.1.0
cd ${CONDA_PREFIX}/GSASII/fsource
scons

# install required packages
conda install --yes pkg-config==0.29.2

# install optional packages
conda install --yes --channel conda-forge imagemagick
python -m pip install gprof2dot==2017.9.19

# install Spotlight
cd ${TOOLS_DIR}/..
python setup.py install

# install TeX Live
YEAR=2020
cd ${CONDA_PREFIX}/src
wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
tar -zxvf install-tl-unx.tar.gz
cd install-tl-${YEAR}*
export TEXLIVE_INSTALL_TEXDIR=${CONDA_PREFIX}/texlive/${YEAR}
export TEXLIVE_INSTALL_PREFIX=${CONDA_PREFIX}/texlive
echo i > temp.txt
./install-tl < temp.txt

# append env activation script
mkdir -p ${CONDA_PREFIX}/etc/conda/activate.d
echo export PGPLOT_FONT=\$\{CONDA_PREFIX\}/pgl/grfont.dat >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export gsas=\$\{CONDA_PREFIX\}/gsas >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export PYTHONPATH=\$\{PYTHONPATH\}:\$\{CONDA_PREFIX\}/GSASII:\$\{CONDA_PREFIX\}/GSASII/fsource >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export PATH=\$\{PATH\}:\$\{gsas\}/exe:\$\{gsas\}/scripts >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
