#! /bin/bash

set -e

# store location of this script
TOOLS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# store Python version
PYTHON_VERSION=3.7.3

# clean env
module purge
module load anaconda/Anaconda3.2019.03
source deactivate
conda env remove --yes --name spotlight

# create Anaconda env
conda create --yes --name spotlight python=${PYTHON_VERSION}
source activate spotlight

# install OpenMPI
mkdir -p ${CONDA_PREFIX}/src && cd ${CONDA_PREFIX}/src
wget https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-3.0.6.tar.gz
tar -xvf openmpi-3.0.6.tar.gz
cd openmpi-3.0.6
CFLAGS=-O3 \
CXXFLAGS=-O3 \
./configure --prefix=${CONDA_PREFIX}
make -j $(getconf _NPROCESSORS_ONLN) install

# install GSAS which requires Python 2.7 for installation scripts
conda install --yes python==2.7.16
mkdir -p ${CONDA_PREFIX}/gsas && cd ${CONDA_PREFIX}/gsas
curl https://subversion.xray.aps.anl.gov/trac/EXPGUI/browser/gsas/linux/dist/bootstrap.py?format=txt > bootstrap.py
echo $'proxyout.lanl.gov\n8080' >> proxy.txt
python bootstrap.py < proxy.txt
rm proxy.txt
conda install --yes python==${PYTHON_VERSION}

# install gsaslanguage scripts and fix some issues
cd ${CONDA_PREFIX}/gsas
git clone https://github.com/Svennito/gsaslanguage.git scripts
cd scripts
git reset --hard fe73549
chmod +x ${CONDA_PREFIX}/gsas/scripts/gsas_get_current_wtfrac_esd

# install Python packages for Spotlight
python -m pip install --upgrade pip
python -m pip install --requirement ${TOOLS_DIR}/../requirements.txt

# install GSAS-II
# note proxy input is broken in GSAS-II bootstrap script
conda install --yes pyopengl==3.1.1a1 wxpython==4.0.4
python -m pip install scipy==1.3.1
mkdir -p ${CONDA_PREFIX}/gsasii && cd ${CONDA_PREFIX}/gsasii
curl https://subversion.xray.aps.anl.gov/pyGSAS/install/bootstrap.py > bootstrap.py
echo $'proxyout.lanl.gov\n8080' >> proxy.txt
python bootstrap.py < proxy.txt
rm proxy.txt
cd fsource
scons

# install required packages
conda install --yes pkg-config==0.29.2

# install optional packages
conda install --yes --channel conda-forge imagemagick
pip install gprof2dot==2017.9.19

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

# install Spotlight
cd ${TOOLS_DIR}/..
python setup.py install

# install TeX Live
YEAR=2019
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
echo export PATH=\$\{PATH\}:\$\{gsas\}/exe:\$\{gsas\}/scripts:$\{CONDA_PREFIX\}/rpms/usr/bin:$\{CONDA_PREFIX\}/texlive/2019/bin/x86_64-linux >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export PYTHONPATH=\$\{PYTHONPATH\}:\$\{CONDA_PREFIX\}/gsasii:\$\{CONDA_PREFIX\}/gsasii/fsource >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export LD_LIBRARY_PATH=\$\{CONDA_PREFIX\}/rpms/lib:\$\{CONDA_PREFIX\}/rpms/usr/lib:\$\{LD_LIBRARY_PATH\} >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
