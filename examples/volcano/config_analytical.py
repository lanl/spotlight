""" A refinement plan for an analytical response function.
"""

import numpy
from scipy import stats
from spotlight import plan

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
        """ Executed once at the beginning to set up the problem.
        """
        pass

    def compute(self):
        """ Executed for each set of drawn parameters in the optimization search.
        """

        # get the x and y values from Mystic
        x, y = self.get("x"), self.get("y")

        # get value at Gaussian function x and y
        var = stats.multivariate_normal(mean=[0, 0], cov=[[0.5, 0],[0, 0.5]])
        gauss = -50.0 * var.pdf([x, y])

        # get value at volcano function x and y
        r = numpy.sqrt(x**2 + y**2)
        mu, sigma = 5.0, 1.0
        stat = 25.0 * (numpy.exp(-r / 35.0) + 1.0 /
                       (sigma * numpy.sqrt(2.0 * numpy.pi)) *
                        numpy.exp(-0.5 * ((r - mu) / sigma) ** 2)) + gauss

        # whether to flip sign of function
        # a positive lets you search for minimum
        # a negative lets you search for maximum
        stat *= self.surface.sign if hasattr(self, "surface") else 1.0

        return stat
