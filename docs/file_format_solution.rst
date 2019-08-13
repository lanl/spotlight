Solution File
=============

The following describes the solution file (i.e. output file) from ``spotlight_minize``.
Solution files are stored using ``klepto.archive.dir_archive``.
When loaded, this can be treated like a Python ``dict``.

There is a special key ``names`` which is a list of the parameter names.
The remaining keys written are tuples with format ``${RANK}_${NUM_SOLVER}_${TAG}`` where
``${RANK}`` is the process rank, ``${NUM_SOLVER}`` is the index of the solver from
that process, and ``${TAG}`` is a string provided by the ``--tag`` option on the command line.
Each has a tuple with four quantities: a (nsteps,nparams) array of the parameter values, a (nsteps) array of the chi-squared values, a (nparams) array of the best parameter values, and a floating-point number of the best chi-squared value.
A simple interaction reading the keys and printing the ``names`` key from a ``klepto`` file is shown below.

.. code-block:: python

    from klepto import archives
    input_file = "solution.db"
    fp = archives.dir_archive(input_file)
    fp.load()
    print(fp.keys())
    print(fp["names"])

See the ``spotlight.archive.Archive`` class for the function that writes the output files, and a convenience function for reading the data.
