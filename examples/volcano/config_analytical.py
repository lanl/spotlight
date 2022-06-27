""" A refinement plan for an analytical response function.
"""

import numpy
from scipy import stats
from spotlight import plan

def gaussian(x, y):
    """ Creates a Gaussian.
    """
    var = stats.multivariate_normal(mean=[0, 0], cov=[[0.5, 0],[0, 0.5]])
    return -50.0 * var.pdf([x, y])

def analytical_function(*p):
    """ The analytical response function to evaluate.
    """
    r = numpy.sqrt(p[0]**2 + p[1]**2)
    mu, sigma = 5.0, 1.0
    return 25.0 * (numpy.exp(-r / 35.0) + 1.0 /
                   (sigma * numpy.sqrt(2.0 * numpy.pi)) *
                    numpy.exp(-0.5 * ((r - mu) / sigma) ** 2)) + gaussian(*p)

class Plan(plan.BasePlan):

    # required to have solution_file, state_file, num_solvers, and tag
    seed = 0
    configuration = {
        "solution_file" : "solution.db",
        "state_file" : "state.db",
        "checkpoint_stride" : 1,
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
        pass

    def compute(self):

        sign = self.surface.sign if hasattr(self, "surface") else 1.0
        stat = analytical_function(self.get("x"), self.get("y"))
        stat *= sign

        return stat
