Configuration File
==================

The configuration file sets information about the refinement plan.
The configuration file should be written to work with the built-in ``configparser`` Python module.
The sections are: ``[solver]``, ``[detector]``, ``[phases]``, and ``[parmeters]``.

The ``[solver]`` section is required to have a ``local_solver`` and ``sampling_method`` option.
Any other options are added as attributes to a ``spotlight.solver.Solver`` instance and passed as a keyword argument to ``Solver.solve`` function.

There are a couple choices of local solvers listed below.

 * ``neadler_mead`` : Does Neadler-Mead optimization.
 * ``powell`` : Does Powell optimization.

The ``neadler_mead`` solver should be passed a ``radius`` keyword argument which changes the size of the intitial simplex values.
See the ``spotlight.solver`` module for more details.

Spotlight has a couple choices for placing solvers in the parameter space.
There are a couple choices available for placing new points listed below.

 * ``uniform`` : Draws from uniform distribution.
 * ``tolerance`` : Places a point furthest from existing set of points.

Inside the ``spotlight.sampling`` module is a ``dict`` that allows access to these sampling methods via the command line of some executables with the
``--sampling-method`` option.
See the ``spotlight.sampling`` module for more details.

The ``[detector]`` section is required to have a ``detector_file`` option.
Any other options are added as attributes to a ``spotlight.detector.Dectector`` instance and passed to the refinement plan class.

The ``[phases]`` section is required to have a ``phase_${I}-file`` and ``phase_${I}-number`` for each phase, where ``${I}`` refers to the interger of the i-th phase.
The order of the phases corresponds to the order of the phases in the refinement plan class.

The ``[parameters]`` section is required to have a ``${PARAM}-min`` and ``${PARAM}-max`` options for each parameter, where ``${PARAM}`` is the parameter name.
There are no assigned parameter names so any string may be added to the configuration file and refinement plan class.

See the ``spotlight.diffraction.Diffraction`` class for the function that reads the configuration file.

See the ``examples`` directory for examples of analyses.
An example of two configuration files from the alumina example that can be concatenated with ``spotlight_minimize`` using the ``--config-files`` option are shown below.
Note that the ``[phases]`` section is missing since this is added on the command line in the example.

.. literalinclude:: ../examples/alumina/config_base.ini
    :language: ini

.. literalinclude:: ../examples/alumina/config_alumina.ini
    :language: ini
