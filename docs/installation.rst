Installation
============

This page describes the requirements and instructions for installing Spotlight.

Minimal Installation
~~~~~~~~~~~~~~~~~~~~

*If you already have Anaconda3 and GSAS or GSAS-II installed, then you can follow the instructions in this subsection.*
If you do not have GSAS or GSAS-II, then we provide an example of an advanced installation script below that also installs these packages in the virtual environment.
You can create and load a virtual environment that contains Spotlight using the commands below.

.. literalinclude:: ../tools/install_minimal.sh

Dependencies
~~~~~~~~~~~~

Spotlight has several external dependencies for diffraction model generation and parallelization, as well as external dependencies from the Python packages Spotlight uses.
This includes

* `GSAS <https://subversion.xray.aps.anl.gov/trac/EXPGUI>`_ (rev1253) for diffraction model generation,
* `gsaslanguage <https://github.com/Svennito/gsaslanguage>`_ (@fe73549) for scripting with GSAS,
* `GSAS-II <https://subversion.xray.aps.anl.gov/trac/pyGSAS>`_ (rev4123) for diffraction model generation (an alternative to GSAS),
* `OpenMPI <https://www.open-mpi.org/>`_ (v2.3.1) for parallelization,
* and `pkg-config <https://www.freedesktop.org/wiki/Software/pkg-config/>`_ (v0.29.2) is required by some Python depedencies such as Matplotlib.

Furthermore, Spotlight has several Python dependencies which are listed in the ``requirements.txt`` file in the top-level of the repository.
This includes: Klepto for Parallel I/O, Matplotlib for visualization, MPI for Python, Numpy for numerical methods, Sphinx for documentation, and Mystic for optimization functions.
We list them below with their versions.

.. literalinclude:: ../requirements.txt

Optional Packages
~~~~~~~~~~~~~~~~~

There are certain software packages that users may find valuable, but they are not required to run Spotlight's core funtionality.
In the examples, you will see references to these packages (e.g. the commands ``convert`` and ``gprof2dot``), but we strive to make not make them a requirement in order to run the examples.
Though in our installation examples below, we show how they can be installed.
This includes

* `ImageMagick <https://imagemagick.org/index.php>`_ (7.0.8) for image processing,
* and `gprof2dot <https://github.com/jrfonseca/gprof2dot>`_ (2017.9.19) for rendering DOT graphs for performance evaluation.

Advanced Installation with Anaconda3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We include a script in the ``tools/`` directory to demonstrate how Spotlight can be installed inside an Anaconda3 environment; this script has been tested using Anaconda3 v4.7.10.
Upon completion of the script below, the environment can be loaded with the command ``conda activate spotlight``.
Note that this script assumes you have Anaconda3 installed.

.. literalinclude:: ../tools/install.sh
    :language: bash
