""" This module contains classes for creating refinement plans that can be optimized.
"""

from mystic import models

class BasePlan(models.AbstractFunction):
    """ This class describes a refinement plan to optimize. Users should implement
    their own version of this class.

    Attributes
    ----------
    config_file : str
        Path to concatenated configuration file.
    data_file : str
        Path to experimental data file.
    bounds : dict
        A ``dict`` with key parameter name and value a tuple of lower and upper
        bounds.
    names : list
        A list of names. This list is ordered how packages will return a list.
    idxs : dict
        A ``dict`` with key parameter and value index of parameter.
    det : Detector
        A ``Dectector`` instance.
    phases : list
        A list of ``Phase`` instances.
    lower_bounds : list
        A list of lower bound values. This list is ordered how packages will
        return a list.
    upper_bounds : list
        A list of upper bound values. This list is ordered how packages will
        return a list.

    Parameters
    ----------
    config_files : list
        Paths to configuration files.
    refinement_plan_file : str
        Path to refinement plan file.
    data_file : str
        Path to experimental data file.
    tmp_dir : str
        Temporary directory to do refinement.
    names : {None, list}
        A list of parameter names in preferred ordered.
    change : bool
        Change into temporary directory. Default is ``True``.
    config_overrides : {None, list}
        A list of `str` delimited by colons to add options to the configuration
        file. The format is "section:option:value".
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
        self.num_phases = len(self.phases)

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
