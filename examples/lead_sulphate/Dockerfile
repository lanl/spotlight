ARG CONDA_VERSION=23.3.1-0
FROM continuumio/miniconda3:${CONDA_VERSION} as gsas2-setup

ARG CONDA_ENV=spotlight-gsas2
ENV PATH /opt/conda/envs/$CONDA_ENV/bin:$PATH

WORKDIR /app

# Install wxpython GSAS2 dependency
RUN apt update \
    && apt install -y \
        libxxf86vm-dev \
        libwxgtk3.0-gtk3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY environment.yaml .
RUN conda env create --name ${CONDA_ENV} -f environment.yaml

RUN echo "conda activate $CONDA_ENV" >> ~/.bashrc

#-------------------------------------------------------------------------------#
FROM gsas2-setup as gsas2-env

ENV NO_MPIRUN="true"

# Version of spotlight to use (from 2023-06-08)
ARG SPOTLIGHT_VERSION="ecf0ae092aef0d632f05e372c2619ebc70dfc630"
ARG GSAS2_VERSION="5609"
ARG GSAS2_PATH="/gsas2"
ENV PYTHONPATH="${PYTHONPATH}:${GSAS2_PATH}:${GSAS2_PATH}/bindist"

# Install GSAS-II
RUN mkdir -p ${GSAS2_PATH} \
    && cd ${GSAS2_PATH} \
    && svn export -r ${GSAS2_VERSION} https://subversion.xray.aps.anl.gov/pyGSAS/install/bootstrap.py \
    && python ./bootstrap.py noproxy

# Get Spotlight repo for examples (change this to just git clone -b <tag> when we want to use a tagged version instead of by commit)
RUN git clone https://github.com/lanl/spotlight.git \
    && cd spotlight \
    && git checkout ${SPOTLIGHT_VERSION}

# Copy in PbSO4 example
COPY . .

CMD ["sh", "./run_spotlight.sh"]
