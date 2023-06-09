Spotlight
=========

**Spotlight** is a Python package for parallelized optimization of Rietveld analysis.
Spotlight leverages an optimization package called `Mystic <https://github.com/uqfoundation/mystic>`_ for optmization and includes additional modules that can be useful for Rietveld analysis.
This documentation contains a tutorial with several sections for: guidance in installation, how to use some basic functionality in Mystic, and how to apply Mystic to Rietveld analysis using `MILK <https://github.com/lanl/MILK>`_.
The sections following the tutorial give source code documentation for Spotlight.

.. toctree::
    :caption: MILK Tutorial
    :maxdepth: 1

    tutorial_introduction
    tutorial_installation
    notebooks/tutorial_mystic_single.ipynb
    notebooks/tutorial_mystic_multi.ipynb
    notebooks/tutorial_mystic_surrogate.ipynb
    notebooks/tutorial_milk_surrogate.ipynb

.. toctree::
    :caption: GSAS-II Tutorial
    :maxdepth: 1

    notebooks/tutorial_gsas2.ipynb

.. toctree::
    :caption: Code Documentation
    :maxdepth: 1

    executables
    spotlight
    py-modindex
    genindex
    search

The Spotlight version used to generate this documentation is shown below.

.. program-output:: spotlight_inspect --version

Citation
~~~~~~~~

If you use Spotlight, we ask that you please use the citation below.

.. literalinclude:: spotlight.bib
   :language: latex

Acknowledgements
~~~~~~~~~~~~~~~~

This work was initially funded at Los Alamos National Laboratory (LANL) by the LANL Laboratory Directed Research and Development project 20170029DR.
LANL is operated by Triad National Security, LLC, for the National Nuclear Security Administration of the U.S. DOE under Contract No. 89233218CNA000001.
