#! /bin/bash

set -e

# clean env
module purge
module load openmpi/2.1.3-gcc_6.4.0
module load anaconda/Anaconda3.2019.03
source deactivate
conda env remove -y -n spotlight

# create Anaconda env
conda create -y -n spotlight  python=2.7
source activate spotlight

# install Python packages
pip install --upgrade pip
pip install "matplotlib==2.0.0"
pip install "numpy==1.13.1"
pip install "scipy==1.0.0"
pip install "dill==0.2.8.1"
pip install "klepto==0.1.5.2"
pip install "sympy==1.1.1"

# install mpi4py
mkdir -p ${CONDA_PREFIX}/src && cd ${CONDA_PREFIX}/src
git clone -b 3.0.0 https://github.com/mpi4py/mpi4py.git
cd mpi4py
python setup.py install

# install mystic
mkdir -p ${CONDA_PREFIX}/src && cd ${CONDA_PREFIX}/src
git clone https://github.com/uqfoundation/mystic.git
cd mystic
python setup.py install

# install gsas
mkdir -p ${CONDA_PREFIX}/gsas && cd ${CONDA_PREFIX}/gsas
curl https://subversion.xray.aps.anl.gov/trac/EXPGUI/browser/gsas/linux/dist/bootstrap.py?format=txt > bootstrap.py
echo $'proxyout.lanl.gov\n8080' >> proxy.txt
python bootstrap.py < proxy.txt
rm proxy.txt

# install gsaslanguage scripts
cd ${CONDA_PREFIX}/gsas
git clone https://github.com/Svennito/gsaslanguage.git scripts
chmod +x ${CONDA_PREFIX}/gsas/scripts/gsas_get_current_wtfrac_esd

# install patchelf
cd ${CONDA_PREFIX}/src
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

# update virtual environment
mkdir -p ${CONDA_PREFIX}/etc/conda/activate.d
echo module load openmpi/2.1.3-gcc_6.4.0 > ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export PGPLOT_FONT=\$\{CONDA_PREFIX\}/pgl/grfont.dat >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export gsas=\$\{CONDA_PREFIX\}/gsas >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export PATH=\$\{PATH\}:\$\{gsas\}/exe:\$\{gsas\}/scripts >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
echo export LD_LIBRARY_PATH=\$\{CONDA_PREFIX\}/rpms/lib:\$\{CONDA_PREFIX\}/rpms/usr/lib:\$\{LD_LIBRARY_PATH\} >> ${CONDA_PREFIX}/etc/conda/activate.d/post.sh
