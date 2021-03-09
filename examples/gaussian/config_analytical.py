""" A refinement plan for an analytical response function.
"""

import numpy
from scipy import stats
from spotlight import plan

def gaussian_2d(x, y, scale=-30, mean=[2, 3]):
    """ Returns a 2-dimensional Gaussian with user-specificed mean,
    and a scale factor that multiples the PDF.
    """
    var = stats.multivariate_normal(mean=mean, cov=[[0.5, 0], [0, 0.5]])
    return scale * var.pdf([x, y])

def analytical_function(x, y):
    """ The analytical response function to evaluate.
    """
    return gaussian_2d(x, y)

class Plan(plan.BasePlan):

    # required to have solution_file, state_file, num_solvers, and tag
    seed = 0
    configuration = {
        "solution_file" : "solution.db",
        "state_file" : "state.db",
        "checkpoint_stride" : 1,
        "num_solvers" : 16,
        "seed" : seed,
        "tag" : seed,
    }

    # required to have local solver and sampling method
    # all other special options get added to a Solver instance
    # any non-special options are passed to the Solver.solve function
    solver = {
        "local_solver" : "powell",
        "stop_change" : 0.1,
        "stop_generations" : 5,
        "sampling_method" : "uniform",
    }

    # parameters names and bounds
    # in compute function use self.get("x") to use optimizer's value for "x"
    parameters = {
        "x" : [-9.5, 9.5],
        "y" : [-9.5, 9.5],
    }

    def initialize(self):
        """ Function that is executed once before the optimization for setup.
        """
        pass

    def compute(self):
        """ Function that is executed many times within optimization loop.
        """
        # retrieve the Gaussian function at (x, y) coordinates
        # and find the minimum (i.e. multiply by -1)
        stat = analytical_function(self.get("x"), self.get("y"))
        return stat
