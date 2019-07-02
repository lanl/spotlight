""" This module contains classes for managing diffraction analyses.
"""

import ConfigParser
import numpy
import os
import pickle
import sys
from spotlight import detector
from spotlight import filesystem
from spotlight import phase

class Diffraction(object):
    """ This class manages a refinement plan. This is the top-level interface
    for interacting with a refinement.

    Upon initializing, a temporary directory can be created and files copied to
    this directory. Some files such as the detector file need to be in the same
    directory as the refinement with GSAS. This is the reason for filesystem
    management.

    Additionally, packages such as Mystic only return a ``list``. Therefore,
    a primary purpose of this class is to keep track of how parameters that
    are being varied are indexed in these lists.

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

    def __init__(self, config_files, refinement_plan_file=None, data_file=None,
                 tmp_dir=None, names=None, change=True, config_overrides=None):

        # create temporary dir
        filesystem.mkdir(tmp_dir)

        # concatenate configuration files
        # copy to temporary dir
        cp = ConfigParser.ConfigParser()
        cp.read(config_files)
        if config_overrides:
            for override in config_overrides:
                section, option, value = override.split(":")
                if not cp.has_section(section):
                    cp.add_section(section)
                cp.set(section, option, value)
        self.config_file = "config.ini"
        with open(tmp_dir + "/" + self.config_file, "w") as fp:
            cp.write(fp)

        # copy files to temporary dir
        self.data_file = filesystem.cp(data_file, tmp_dir) \
                             if tmp_dir else data_file
        self.refinement_plan_file = \
                             filesystem.cp(refinement_plan_file, tmp_dir) \
                             if tmp_dir else data_file

        # read configuration
        self.bounds, self.det, self.phases = self.read_config(tmp_dir + "/" + self.config_file)
        self.names = names if names is not None else self.bounds.keys()
        self.idxs = {name : i for i, name in enumerate(self.names)}

        # copy more files
        detector_file = filesystem.cp(self.det.detector_file, tmp_dir) \
                            if tmp_dir else self.det.detector_file
        self.det.detector_file = detector_file
        phase_files = filesystem.cp([p.phase_file for p in self.phases],
                                          tmp_dir) \
                               if tmp_dir else [p.phase_file
                                                for p in self.phases]
        for p, new_file in zip(self.phases, phase_files):
            p.phase_file = new_file

        # move to temporary dir
        if tmp_dir is not None:
            filesystem.mkdir(tmp_dir, change=change)

        # import refinement plan
        sys.dont_write_bytecode = True
        if self.refinement_plan_file != None:
            self.refinement_plan = __import__(
                    os.path.basename(self.refinement_plan_file).rstrip(".py"))
        else:
            self.refinement_plan = None
        sys.dont_write_bytecode = False

    @property
    def lower_bounds(self):
        return [self.bounds[name][0] for name in self.names]

    @property
    def upper_bounds(self):
        return [self.bounds[name][1] for name in self.names]

    def get_refinement_plan(self):
        """ Returns instance of requested refinement plan.

        Returns
        -------
        cost : Plan
            A refinement plan instance.
        """
        ndim = len(self.names)
        cost = self.refinement_plan.Plan(self.idxs, self.bounds,
                                         self.data_file,
                                         self.det, self.phases, ndim=ndim)
        return cost

    def read_config(self, config_file=None):
        """ Reads information from configuration file.
    
        Parameters
        ----------
        config_file : {None, str}
           Path of configuration file to read. Default is ``None`` which reads
           attribute ``config_file``.
    
        Returns
        -------
        params : dict
           A ``dict`` with parameters from the ``[parameters]`` section of the
           configuration file. The keys are the parameter names and the values
           are tuples of the bounds to search ``(lower_bound, upper_bound)``.
        det : Detector
           A ``Detector`` instance. Contains all options from the
           ``[detector]`` section.
        phases : list
           A ``list`` of ``Phase`` instances. Reads options from the
           ``[phases]`` section.
        """

        # get path
        config_file = config_file if config_file \
                          is not None else self.config_file

        # read configuration file
        cp = ConfigParser.ConfigParser()
        cp.readfp(open(config_file, "r"))

        # read parameter names from [parameters]
        section = "parameters"
        names = []
        for option in cp.options(section):
            name = option.split("-")[0].upper()
            if name not in names:
                names.append(name)
    
        # make a dict of max and min boundaries for parameters in [parameters]
        params = {}
        for name in names:
            lb = cp.getfloat(section, name + "-min")
            ub = cp.getfloat(section, name + "-max")
            params[name] = (lb, ub)
    
        # get all detector information from [detector]
        section = "detector"
        restricted_opts = ["detector_file"]
        kwargs = {opt : cp.get(section, opt)
                  for opt in cp.options(section) if opt not in restricted_opts}
        detector_file = cp.get(section, "detector_file")
        det = detector.Detector(detector_file, **kwargs)

        # get phase file and number in file from [phases]
        section = "phases"
        phases = []
        options = cp.options(section)
        num_phases = len(options) / 2
        for i in range(num_phases):
            j = i + 1
            phase_file = cp.get(section, "phase_{}-file".format(j))
            phase_number = cp.getint(section, "phase_{}-number".format(j))
            phases.append(phase.Phase(phase_file, phase_number))

        return params, det, phases

