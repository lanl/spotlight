""" A refinement plan for an analytical response function.
"""

import numpy
from scipy import stats
from spotlight import plan

def gaussian(x, y):
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

    def initialize(self):
        pass

    def compute(self):

        sign = self.surface.sign if hasattr(self, "surface") else 1.0
        stat = analytical_function(self.get("X"), self.get("Y"))
        stat *= sign

        return stat
