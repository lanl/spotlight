Quick Start
===========

This is a quick start example on analyzing an alumina (Al\ :subscript:`2`\ O\ :subscript:`3`) dataset.
The example is contained within the ``examples/alumina`` directory of this repository.
This page provides example commands to execute the example, and subsequent pages describe the file formats.

Spotlight instructions
~~~~~~~~~~~~~~~~~~~~~~

There is an example using Spotlight.
To run, change into the ``examples/alumina`` directory and then execute the command below.

.. code:: bash

    bash run_spotlight.sh

This script contains the necessary command lines to execute an optimization search with a refinement plan for the alumina dataset.
The script calls ``spotlight_minimize`` to execute the optimization search, ``spotlight_plot_minima`` to extract the best results from the optimization search as a GSAS experiment, and several plotting scripts for the results and code performance.
The script is shown below.

.. literalinclude:: ../examples/alumina/run_spotlight.sh
    :language: bash

Inspecting the results
~~~~~~~~~~~~~~~~~~~~~~

You can inspect results of each local optimization as they run, to run execute the command below.

.. code:: bash

    spotlight_inspect --input-file tmp_spotlight/solution.db

Once the example has completed, then you can view a PDF of the best results with the command below.

.. code:: bash

    display tmp_spotlight/tmp_minima/alumina_1.pdf

Submission to a distributed-computing network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, on a Slurm cluster, to run execute the command below.

.. code:: bash

    sbatch -N 1 -t 600 run_spotlight.sh 

gsaslanguage instructions
~~~~~~~~~~~~~~~~~~~~~~~~~

There is also an example using gsaslanguage as a reference.
To run execute the command below.

.. code:: bash

    bash run_gsaslanguage.sh
