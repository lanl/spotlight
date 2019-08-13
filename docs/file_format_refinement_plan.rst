Refinement Plan File
====================

The user creates a Python module with a class that inherits from the ``spotlight.plan.BasePlan`` class.

Inside the ``initialize`` function define any upfront operations such as setting a GSAS experiment, adding phases, or background corrections should be performed.

Inside the ``compute`` function define any steps in the refinement plan that will be repeated many times.
At the end, return a value to be minimized such as chi-squared.

The ``spotlight`` Python package interfaces with GSAS through gsaslanguage which is a set of bash wrappers around command line executables.
The Python wrappers around these scripts is in ``spotlight.gsas``.
Several wrappers not included in gsaslanguage are included with Spotlight as well.

See the ``examples`` directory for examples of refinement plans.
An example of a refinement plan file from the alumina example that can be used with ``spotlight_minimize`` using the ``--refinement-plan-file`` option is shown below.

.. literalinclude:: ../examples/alumina/plan_alumina.py
    :language: python
