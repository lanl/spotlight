import matplotlib.pyplot as plt
import numpy
import os
from scipy import stats

def func(*p):
    """ Executed for each set of drawn parameters in the optimization search.
    """

    # get the x and y values from Mystic
    x = p[0]

    # get value at 2-D Gaussian function x and y
    var = stats.multivariate_normal(mean=[4.25], cov=[[1]])
    stat = -50.0 * var.pdf([x])

    # set sign of function
    # a positive lets you search for minimum
    # a negative lets you search for maximum
    stat *= 1.0

    return stat

x = numpy.linspace(-9.5, 9.5, 100)
plt.plot(x, [func(i) for i in x])

plt.savefig(os.path.join(os.path.dirname(__file__), "tmp_cost.png"))
