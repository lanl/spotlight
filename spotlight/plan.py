""" This module contains classes for creating refinement plans that can be optimized.
"""

from mystic import models

class BasePlan(models.AbstractFunction):
    """ This class describes a refinement plan to optimize. Users should implement
    their own version of this class.

    Attributes
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

    def __init__(self, idxs, bounds, data_file, detector, phases, **kwargs):
        super(BasePlan, self).__init__(**kwargs)

        # store map to parameters
        self.idxs = idxs
        self.bounds = bounds

        # store input files
        self.data_file = data_file
        self.detector = detector
        self.phases = phases

        # setup initial porition of refinement plan
        self.initialize()

    def initialize(self):
        """ Function called once before optimization.
        """
        pass

    def function(self, p):
        """ Function to be optimized.
        """
        raise NotImplementedError("Plan does not have function!")
