Installation
============

This page describes the requirements and instructions for installing Spotlight.

Dependencies
~~~~~~~~~~~~

Spotlight has several external dependencies for diffraction model generation and parallelization, as well as external dependencies from the Python packages Spotlight uses.
This includes

* `GSAS <https://subversion.xray.aps.anl.gov/trac/EXPGUI>`_ (rev1253) for diffraction model generation,
* `gsaslanguage <https://github.com/Svennito/gsaslanguage>`_ (@8f09750) for scripting with GSAS,
* `OpenMPI <https://www.open-mpi.org/>`_ (v2.3.1) for parallelization,
* and `pkg-config <https://www.freedesktop.org/wiki/Software/pkg-config/>`_ (v0.29.2) is required by some Python depedencies such as Matplotlib.

Furthermore, Spotlight has several Python dependencies which are listed in the ``requirements.txt`` file in the top-level of the repository.
We list them below.

.. literalinclude:: ../requirements.txt

Installation with Anaconda3
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We include a script in the ``tools/`` dir to demonstrate how Spotlight can be installed inside an Anaconda3 environment; this script has been tested using Anaconda3 v4.7.10.
Upon completion of the script below, the environment can be loaded with the command ``activate spotlight``.
Note that this script assumes you have Anaconda3 installed.

.. literalinclude:: ../tools/install.sh
    :language: bash
