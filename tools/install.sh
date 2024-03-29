#! /bin/bash

set -e

# parse command line
PROXY=""
while [ "${1}" != "" ]; do
    case ${1} in
        --proxy )
            shift
            PROXY=${1}
            ;;
    esac
    shift
done

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

# enter Anaconda env
conda activate spotlight

# install GSAS-II
OSNAME=`uname`
case ${OSNAME} in
    "Darwin")
        GSASII_SCRIPT_URL="https://subversion.xray.aps.anl.gov/admin_pyGSAS/downloads/gsas2full-Latest-MacOSX-x86_64.sh"
        ;;
    "Linux")
        GSASII_SCRIPT_URL="https://subversion.xray.aps.anl.gov/admin_pyGSAS/downloads/gsas2full-Latest-Linux-x86_64.sh"
        ;;
esac
curl ${GSASII_SCRIPT_URL} > ${CONDA_PREFIX}/gsas2full-Latest-x86_64.sh
printf $"${PROXY}" >> proxy.txt
bash ${CONDA_PREFIX}/gsas2full-Latest-x86_64.sh -b -p ${CONDA_PREFIX}/gsasii < proxy.txt
rm proxy.txt

# install GSAS which requires Python 2.7 for installation scripts
conda install --yes --channel anaconda svn==1.9.7
mkdir -p ${CONDA_PREFIX}/gsas && cd ${CONDA_PREFIX}/gsas
curl https://subversion.xray.aps.anl.gov/trac/EXPGUI/browser/gsas/linux/dist/bootstrap.py?format=txt > bootstrap.py
if [ ${PROXY} ]; then
    printf $"${PROXY}" >> proxy.txt
    python2 bootstrap.py < proxy.txt
    rm proxy.txt
else
    python2 bootstrap.py noproxy
fi

# install gsaslanguage scripts and fix some issues
cd ${CONDA_PREFIX}/gsas
git clone https://github.com/Svennito/gsaslanguage.git scripts
cd scripts
git reset --hard fe73549
chmod +x ${CONDA_PREFIX}/gsas/scripts/gsas_get_current_wtfrac_esd

# install OpenMPI
case ${OSNAME} in
    "Linux")
        conda install --yes gxx_linux-64
        ;;
esac
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
cd ${CONDA_PREFIX}/gsasii/GSASII/fsource
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
YEAR=`date +%Y`
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
