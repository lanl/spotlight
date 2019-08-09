Alumina example
===============

This is a quick start example on analyzing an alumina (Al\ :subscript:`2`\ O\ :subscript:`3`) dataset.
The example is contained within the ``examples/alumina`` directory of this repository.

Spotlight instructions
~~~~~~~~~~~~~~~~~~~~~~

There is an example using Spotlight.
To run execute the command below.

.. code:: bash

    bash run_spotlight.sh

Alternatively, on a Slurm cluster, to run execute the command below.

.. code:: bash

    sbatch -N 1 -t 600 run_spotlight.sh 

You can inspect results as they run, to run execute the command below.

.. code:: bash

    spotlight_inspect --input-file tmp_spotlight/solution.db

Once the example has completed, then you can view the results with the command below.

.. code:: bash

    display tmp_spotlight/tmp_minima/alumina_1.pdf

gsaslanguage instructions
~~~~~~~~~~~~~~~~~~~~~~~~~

There is also an example using gsaslanguage.
To run execute the command below.

.. code:: bash

    bash run_gsaslanguage.sh
