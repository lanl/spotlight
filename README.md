# Spotlight

This is a Python package with wrappers around GSAS and Mystic for parallelized
optimization of Rietveld refinement plans.

## Installation

Requirements for these instructions:
  * Python 2.7
  * Pip
  * Virtualenv (eg. `pip install virtualenv --user`)
  * X11 (GSAS requires the 32-bit version)

There is a Python package ``spotlight`` included in Spotlight which installs
like most Python packages.

There is a script ``install.sh`` which shows an example of installing Spotlight
into a virtual environment with its dependencies.
To try on your system do:
```
PATH=${HOME}/.local/bin:${PATH}
bash install.sh
source ${HOME}/opt/spotlight-dev/bin/activate
python setup.py install
```

To test your installation, you should be able to run scripts from the
``examples`` directory.
These examples have their own documentation on how to run them.

## Classes

The top-level interface to GSAS and refinement plans in the ``spotlight``
Python package is the ``spotlight.diffraction.Diffraction`` class.
This class handles several operations.
First, some filesystem management is required for GSAS.
Second, packages such as Mystic pass a list of parameter values without keys.
Therefore, this class keeps track of what parameters are associated with which
index in these lists.
Third, this class handles reading configuration files.

The top-level interface to Mystic and optimization setup in the ``spotlight``
Python package is the ``spotlight.solver.Solver`` class.
This class configures the optimization plan in Mystic.

Refinement plans are created by the user as a Python module where each module
contains a ``Plan`` class.
These classes define the refinement plan.

The reading and writing of output data files from the optimization analysis is
handled in the ``spotlight.archive.Archive`` class.

There are two other classes ``spotlight.detector.Dectector`` and
``spotlight.phase.Phase``.
These classes are created after reading information from a configuration file.
They are a bit superficial and could be absorbed into the
``spotlight.diffraction.Diffraction`` class.
In the future, a wrapper around ``klepto.archive.archive_file`` should be
considered as well.

## GSAS interface

The ``spotlight`` Python package interfaces with GSAS through GSASLanguage
which is a set of bash wrappers around command line executables.

The Python wrappers around these scripts is in ``spotlight.gsas``.
Several wrappers not included in GSASLanguage are included with Spotlight as
well.

## Configuration file format

The configuration file sets information about the refinement plan.
The configuration file should be written to work with ``ConfigParser`` module.
The five sections are ``[solver]``, ``[refinement]``, ``[detector]``,
``[phases]``, and ``[parmeters]``.

The ``[solver]`` section is required to have a ``local_solver`` and
``sampling_method`` option.
Any other options are added as attributes to a ``spotlight.solver.Solver``
instance and passed as a keyword argument to ``Solver.solve`` function.

The ``[refinement]`` section is required to have a ``refinement_plan`` option.
This is the name of the refinement plan to use.

The ``[detector]`` section is required to have a ``detector_file`` option.
Any other options are added as attributes to a ``spotlight.detector.Dectector``
instance and passed to the refinement plan class.

The ``[phases]`` section is required to have a ``phase_${I}-file`` and
``phase_${I}-number`` for each phase, where ``${I}`` refers to the interger of
the i-th phase.
The order of the phases corresponds to the order of the phases in the
refinement plan class.

The ``[parameters]`` section is required to have a ``${PARAM}-min`` and
``${PARAM}-max`` options for each parameter, where ``${PARAM}`` is the
parameter name.
There are no assigned parameter names so any string may be added to the
configuration file and refinement plan class.

See the ``examples`` directory for examples of analyses.

See the ``spotlight.diffraction.Diffraction`` class for the function that reads
the configuration file.

## Refinement plans file format

The user creates a module with a ``Plan`` class.

Refinement plans available are:
  * The ``plan_alumina.py`` refinement plan shows how to optimize all parameters
with Mystic for the alumina analysis.

Inside the ``__init__`` class function define any upfront operations such as
GSAS initialization, adding phases, or background corrections.

Inside the ``function`` class function define any steps in the refinement
plan that will be repeated many times.
At the end, return a value to be minimized such as chi-squared.

See the ``examples`` directory for examples of refinement plans.

## Output data file format

Output files are stored as a ``klepto.archive.archive_file``.
When loaded, this can be treated like a ``dict``.

There is a special key ``names`` which is a list of the parameter names.
The remaining keys are tuples with format ``(rank, num_solver, tag)`` where
``rank`` is the process rank, ``num_solver`` is the index of the solver from
that process, and ``tag`` is a string provided on the command line.
Each has a tuple with four quantities: a (nsteps,nparams) array of the parameter
values, a (nsteps) array of the chi-squared values, a (nparams) array of the best
parameter values, and a floating-point number of the best chi-squared value.
The simplest interaction with a ``klepto`` file is
```
from klepto import archives
fp = archives.file_archives(input_file)
fp.load()
print(fp["names"])
```

See the ``spotlight.archive.Archive`` class for the function that
writes the output files, and a convenience function for reading the data.

## Executables

Executables available are:
  * The executable ``spotlight_minimize`` optimizes a Rietveld refinement plan
with Mystic.
  * The executable ``spotlight_plot_minima`` produces a PDF of the refinement.
  * The executable ``spotlight_plot_chisq`` produces a scatter plot matrix of
chi-square value versus parameter value.

See the ``examples`` directory for examples using these scripts, and use the
``--help`` option for command line options.

## Local solvers

There are a couple choices of local solvers:
  * ``neadler_mead`` : Does Neadler-Mead optimization.
  * ``powell`` : Does Powell optimization.

The ``neadler_mead`` solver can be passed a ``radius`` keyword argument which
changes the size of the intitial simplex values.

See the ``spotlight.solver`` module for more details.

## Sampling methods

Mystic places solvers in the parameter space.
There are a couple choices available for placing new points:
  * ``uniform`` : Draws from uniform distribution.
  * ``tolerance`` : Places a point furthest from existing set of points.

Inside the ``spotlight.sampling`` module is a ``dict`` that allows access to
these sampling methods via the command line of some executables with the
``--sampling-method`` option.
If you add a new sampling method, you should update this module to include
your new sampling method function.

See the ``spotlight.sampling`` module for more details.
