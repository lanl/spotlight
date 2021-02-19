""" This module contains classes for creating refinement plans that can be optimized.
"""

from mystic import models

class BasePlan(models.AbstractFunction):
    """ This class describes a refinement plan to optimize. Users should implement
    their own subclass of this class.

    Attributes
    ----------
    idxs : dict
        A ``dict`` with key parameter and value index of parameter.
    bounds : dict
        A ``dict`` with key parameter name and value a tuple of lower and upper
        bounds.
    detectors : list
        A list of ``Dectector`` instances.
    phases : list
        A list of ``Phase`` instances.
    _p : list
        A list of the latest parameters sent to the optimized function. The list should
        be indexed by ``idxs``.

    Parameters
    ----------
    idxs : dict
        A ``dict`` with key parameter and value index of parameter.
    bounds : dict
        A ``dict`` with key parameter name and value a tuple of lower and upper
        bounds.
    data_file : str
        Path to experimental data file.
    detector : Detector
        A ``Dectector`` instance.
    phases : list
        A list of ``Phase`` instances.
    """

    def __init__(self, idxs, bounds, ndim, initialize=True, **kwargs):
        super(BasePlan, self).__init__(ndim=ndim)

        # store map to parameters
        self.idxs = idxs
        self.bounds = bounds
        self._p = None

        # store input files
        for key, val in kwargs.items():
            setattr(self, key, val)

        # setup initial porition of refinement plan
        if initialize:
            self.initialize()

    def initialize(self):
        """ Function called once before optimization.
        """
        pass

    def function(self, p):
        """ Function used by Mystic for optimization.

        Parameters
        ----------
        p : list
            A `list` of the floating-point values. 

        Returns
        -------
        float
           The value of the evaluated cost function.
        """
        self._p = p
        return self.compute()
        
    def compute(self):
        """ Function to be optimized.
        
        Returns
        -------
        float
           The value of the evaluated cost function.
        """
        raise NotImplementedError("Plan does not have a compute function!")

    def constraint(self, p):
        """ Applies constraints.

        Parameters
        ----------
        p : list
            A `list` of the floating-point values.

        Returns
        -------
        p : list
            A `list` of the floating-point values.
        """
        return p

    def get(self, name):
        """ Helper function for returning the value of the variable.

        Parameters
        ----------
        p : list
            A `list` of the floating-point values.
        name : str
            Name of the parameter to query.

        Returns
        -------
        float
           The floating-point value for the variable.
        """
        return self._p[self.idxs[name]]
