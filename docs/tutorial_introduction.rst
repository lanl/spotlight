Introduction
============

.. contents:: :local:

Rietveld analysis of tens or hundreds of powder diffraction datasets from parametric or time-resolved experiments often poses a bottleneck.
High temperature annealing studies, during which phase transformations occur and lattice parameters may change due to repartitioning of elements, are prime examples where automation by a simple phase identification from a database of room temperature structures or automation by sequential refinements is likely to fail. 
To address this problem, we present a Python packaged named Spotlight which uses optimization algorithms to guide an ensemble of refinements to the best fit parameters over many subprocesses and across machines which allows the analyst to harness the computational capacity of high-performance computing clusters for Rietveld analyses.
The parallel execution of many refinements with varying starting values enables: the prediction of initial parameter values for designing refinement plans and identification of phases.
The following tutorial package demonstrates:
 * How to use Mystic, an optimization framework, to map response surfaces,
 * How to apply Mystic to a Rietveld analysis using MILK,
 * And how to do these searches in parallel.

Illustration of the sampling of a complex parameter space with Spotlight using.
The surface of a two-dimensional volcano function, denoted ``f(x,y)``, mapped using an ensemble of local optimizations.
The surface is interpolated on a uniform grid.
The more local optimizations (i.e. more sampling) then the higher the resolution of the surface.
For Rietveld refinements, this same strategy can map the ``\chi^{2}(\vec{x})`` or R-factor surface where the global minimum of the surface corresponds the best-fit parameters.
From left to right: 16 local optimizations (8 to find minimums and 8 to find maximums), 32 local optimizations (16 to find minimums and 16 to find maximums), and 128 local optimizations (64 to find minimums and 64 to find maximums).

.. image:: _static/map_2.png
   :width: 600

.. image:: _static/map_8.png
   :width: 600

.. image:: _static/map_32.png
   :width: 600

Mystic can be used to simplify non-convex optimization problems by transforming away nonlinearities through user-built kernel transforms.
This tutorial demonstrates using Mystic for machine learning with automated dimensional-reduction, using embarrasingly parallel solver ensembles to find an accurate interpolated surrogate for a nonlinear surface, and the determination of worst-case bounds on expectation value of an objective function under uncertainty.
The image below shows an optimization loop.

Using packages like Mystic, in conjunction with supporting packages ``pathos``, ``pyina``, and ``klepto``, we can provide massively-parallel scalable workflows for quickly solving optimization problems in complex nonlinear spaces.
The optimization loop shown below on the left can write results to a database using ``klepto``.
We extend this for multiple processes storing the results to a central database as shown on the right.

.. image:: _static/search_workflow.png
   :width: 600

.. image:: _static/search_distributed.png
   :width: 600

