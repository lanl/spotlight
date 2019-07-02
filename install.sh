#! /bin/bash

# remove old virtual enviroment
deactivate
VIRTUAL_SRC=${HOME}/opt/spotlight-dev
rm -rf ${VIRTUAL_SRC}

set -e

# create virtual environment
virtualenv --python `which python2.7` ${VIRTUAL_SRC}
source ${VIRTUAL_SRC}/bin/activate

# install MPI
mkdir -p ${VIRTUAL_ENV}/src && cd ${VIRTUAL_ENV}/src
wget https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.3.tar.gz
tar -xvf openmpi-2.1.3.tar.gz
cd openmpi-2.1.3
CFLAGS=-O3 \
CXXFLAGS=-O3 \
./configure --prefix=${VIRTUAL_ENV}
make -j $(getconf _NPROCESSORS_ONLN) install

# install Python packages
pip install --upgrade pip
pip install "matplotlib==2.0.0"
pip install "numpy==1.13.1"
pip install "scipy==1.0.0"
pip install "dill==0.2.8.1"
pip install "klepto==0.1.5.2"
pip install "sympy==1.1.1"
pip install "mpi4py==3.0.0"

# install mystic
mkdir -p ${VIRTUAL_ENV}/src && cd ${VIRTUAL_ENV}/src
git clone https://github.com/uqfoundation/mystic.git
cd mystic
python setup.py install

# install gsas
mkdir -p ${VIRTUAL_ENV}/gsas && cd ${VIRTUAL_ENV}/gsas
curl https://subversion.xray.aps.anl.gov/trac/EXPGUI/browser/gsas/linux/dist/bootstrap.py?format=txt > bootstrap.py
echo $'proxyout.lanl.gov\n8080' >> proxy.txt
python bootstrap.py < proxy.txt
rm proxy.txt

# install gsaslanguage scripts
cd ${VIRTUAL_ENV}/gsas
git clone https://github.com/Svennito/gsaslanguage.git scripts

# update virtual environment
echo export PGPLOT_FONT=\$\{VIRTUAL_ENV\}/pgl/grfont.dat >> ${VIRTUAL_ENV}/bin/activate
echo export gsas=\$\{VIRTUAL_ENV\}/gsas >> ${VIRTUAL_ENV}/bin/activate
echo export PATH=\$\{PATH\}:\$\{gsas\}/exe:\$\{gsas\}/scripts >> ${VIRTUAL_ENV}/bin/activate

