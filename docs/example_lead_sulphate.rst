Quick Start Using GSAS-II
=========================

This is a quick start example on analyzing a lead sulphate (PbSO\ :subscript:`4`) dataset that is originally part of a GSAS-II tutorial.
The example is contained within the ``examples/lead_sulphate`` directory of this repository.
This page provides example commands to execute the example, and subsequent pages describe the file formats.

Spotlight instructions
~~~~~~~~~~~~~~~~~~~~~~

There is an example using Spotlight.
To run, change into the ``examples/lead_sulphate`` directory and then execute the command below.

.. code:: bash

    bash run_spotlight.sh

This script contains the necessary command lines to execute an optimization search with a refinement plan for the lead sulphate dataset.
The script calls ``spotlight_minimize`` to execute the optimization search, ``spotlight_setup_gsas`` to extract the best results from the optimization search as a GSAS-II experiment, and several plotting scripts for the results and code performance.
The script is shown below.

.. literalinclude:: ../examples/lead_sulphate/run_spotlight.sh
    :language: bash

The structure of the configuration, refinement plan, and solution files are the same.
Refer to the Alumina example documentation for more information on the structure of those file types.
However, we show the refinement plan using GSAS-II function calls below.

.. literalinclude:: ../examples/lead_sulphate/plan_pbso4.py
    :language: python

GSAS-II instructions
~~~~~~~~~~~~~~~~~~~~

There is also an example using only GSAS-II as a reference.
To run execute the command below.

.. code:: bash

    bash run_gsasii.sh
