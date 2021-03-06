""" This module contains functions that return a new, single point in a given
parameter space. In general, these functions are not used to return
multi-dimensional arrays. These functions are intended to be called only a
few times.
"""

import numpy
from mystic import math

def uniform(lower_bounds, upper_bounds):
    """ Returns a new, single point via uniform distribution.

    Parameters
    ----------
    lower_bounds : list
        List of ``float`` that are lower bounds. List is indexed by parameter.
    upper_bounds : list
        List of ``float`` that are upper bounds. List is indexed by parameter.

    Returns
    -------
    pts : numpy.array
        An array with new point.
    """
    ndim = len(lower_bounds)
    pts = numpy.zeros(ndim)
    for j in range(ndim):
        lb = lower_bounds[j]
        ub = upper_bounds[j]
        pts[j] = numpy.random.uniform(lb, ub)
    return pts

def tolerance(lower_bounds, upper_bounds, data=None):
    """ Returns a new, single point some tolerence away from existing points.

    Parameters
    ----------
    lower_bounds : list
        List of ``float`` that are lower bounds. List is indexed by parameter.
    upper_bounds : list
        List of ``float`` that are upper bounds. List is indexed by parameter.
    data : {None, list}
        List of tuples. Each tuple is a list of ``float`` that are previous
        data points.

    Returns
    -------
    pts : numpy.array
        An array with new point.
    """
    rtol = None
    dist = None
    n_new_pts = 1
    data = [] if data == None else data
    if len(data) == 0:
        return uniform(lower_bounds, upper_bounds)
    pts = math.fillpts(lower_bounds, upper_bounds, n_new_pts, data, rtol, dist)
    return pts[0]

def midpoint(lower_bounds, upper_bounds):
    """ Returns a new, single point at the center.

    Parameters
    ----------
    lower_bounds : list
        List of ``float`` that are lower bounds. List is indexed by parameter.
    upper_bounds : list
        List of ``float`` that are upper bounds. List is indexed by parameter.

    Returns
    -------
    pts : numpy.array
        An array with new point.
    """
    ndim = len(lower_bounds)
    pts = numpy.zeros(ndim)
    for j in range(ndim):
        lb = lower_bounds[j]
        ub = upper_bounds[j]
        pts[j] = (ub - lb) / 2.0 + lb
    return pts

# dict of sampling methods
sampling_methods = {
    "uniform" : uniform,
    "tolerance" : tolerance,
}
