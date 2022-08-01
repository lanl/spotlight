
import matplotlib.pyplot as plt
import numpy
import os
from scipy import stats
from mystic import tools
from mystic.termination import NormalizedChangeOverGeneration
from mystic.solvers import PowellDirectionalSolver
from mystic.ensemble import BuckshotSolver
from mystic.termination import VTR

def func(p):
    """ Executed for each set of drawn parameters in the optimization search.
    """

    # get the x and y values from Mystic
    x = p

    # get value at Gaussian function x and y
    var = stats.multivariate_normal(mean=[4.25], cov=[[1]])
    stat = -50.0 * var.pdf([x])

    # whether to flip sign of function
    # a positive lets you search for minimum
    # a negative lets you search for maximum
    stat *= 1.0

    return stat

# set random seed
tools.random_seed(0)

# a single solver
solver = PowellDirectionalSolver(1)
solver.SetInitialPoints([1])
solver.SetEvaluationLimits(8)
solver.SetStrictRanges((-9.5,), (9.5,))
solver.Solve(func, VTR())

print(dir(solver))

print(solver.bestSolution)

x = numpy.linspace(-9.5, 9.5, 100)
plt.plot(x, [func(i) for i in x])
plt.axvline(solver.bestSolution[0])

plt.savefig(os.path.join(os.path.dirname(__file__), "tmp_single.png"))

