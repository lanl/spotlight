""" This module contains classes for managing diffraction analyses.
"""

import configparser
import numpy
import os
import pickle
import sys
from spotlight import filesystem
from spotlight import solver

class ConfigurationFile:
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
    refinement_plan_file : str
        Path to refinement plan file.
    refinement_plan : Plan
        The loaded refinement plan module.
    bounds : dict
        A ``dict`` with key parameter name and value a tuple of lower and upper
        bounds.
    names : list
        A list of names. This list is ordered how packages will return a list.
    idxs : dict
        A ``dict`` with key parameter and value index of parameter.
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

    def __init__(self, config_files, tmp_dir=None, names=None, change=True,
                 copy=True, config_overrides=None):

        # configuration file is a single Python file
        if len(config_files) == 1:

            # set attributes from configuration file
            self.read_config(config_files[0])
            if config_overrides:
                for override in config_overrides:
                    self.apply_override(override)

        # otherwise too many configuration files
        else:
            raise ValueError("You can only supply a single configuration file!")

        # refinement plan is not loaded until get_refinement_plan is called
        self.refinement_plan = None

        # set attributes for names and indices of parameters
        self.names = list(names if names is not None else self.bounds.keys())
        self.idxs = {name : i for i, name in enumerate(self.names)}

        # copy files to temporary dir
        # move to temporary dir
        if copy:
            self.setup_dir(tmp_dir, change=change)
        else:
            self.config_file = config_files

    @property
    def lower_bounds(self):
        return [self.bounds[name][0] for name in self.names]

    @property
    def upper_bounds(self):
        return [self.bounds[name][1] for name in self.names]

    def apply_override(self, override):
        """ Applies an override to thie configuration.
        """
        section, option, value = override.split(":")
        if value.isdigit():
            val = int(value)
        else:
            try:
                val = float(value)
            except ValueError:
                pass
        if section == "configuration":
            setattr(self, option, val)
        else:
            if not hasattr(self, section):
                setattr(self, section, {})
            obj = getattr(self, section)
            obj[option] = value

    def setup_dir(self, tmp_dir=None, change=True):
        """ Copy files to temporary directory.
        """

        # create temporary dir
        if tmp_dir:
            filesystem.mkdir(tmp_dir)
        else:
            tmp_dir = "."

        # copy refinement plan file to temporary dir
        self.refinement_plan_file = filesystem.cp(self.refinement_plan_file, tmp_dir) \
                             if tmp_dir else self.refinement_plan_file

        # write configuration file to temporary dir
        self.config_file = os.path.join(tmp_dir, "config.ini") \
                               if tmp_dir else "config.ini"
        if hasattr(self, "cp"):
            with open(self.config_file, "w") as fp:
                self.cp.write(fp)
        self.config_file = os.path.basename(self.config_file) if change else self.config_file

        # move to temporary dir
        if tmp_dir is not None:
            filesystem.mkdir(tmp_dir, change=change)

    def get_refinement_plan(self, initialize=True, reimport=True):
        """ Returns instance of requested refinement plan.

        Returns
        -------
        cost : Plan
            A refinement plan instance.
        """

        # import refinement plan
        if self.refinement_plan is None or reimport:
            sys.dont_write_bytecode = True
            if self.refinement_plan_file == None and self.refinement_plan == None:
                raise ValueError("There is no refinement plan to load!")
            elif self.refinement_plan == None:
                sys.path.append(os.path.dirname(self.refinement_plan_file))
                self.refinement_plan = __import__(
                        os.path.basename(self.refinement_plan_file).rstrip(".py"))
            sys.dont_write_bytecode = False

        # initialize refinement plan
        ndim = len(self.names)
        cost = self.refinement_plan.Plan(self.idxs, self.bounds, ndim=ndim,
                                         initialize=initialize)

        return cost

    def get_solver(self, **kwargs):
        """ Returns instance of requested solver.

        Returns
        -------
        local_solver : Solver
            A ``Solver`` instance.
        """

        # include [solver] configuration file
        tmp = self.solver_kwargs
        tmp.update(kwargs)

        # initialize solver
        local_solver = solver.Solver(self.lower_bounds, self.upper_bounds,
                                     **tmp)

        return local_solver

    def read_config(self, config_file=None):
        """ Reads information from configuration file.
    
        Parameters
        ----------
        config_file : {None, str}
           Path of configuration file to read. Default is ``None`` which reads
           attribute ``config_file``.
        """

        # import configuration file
        sys.path.append(os.path.dirname(config_file))
        sys.dont_write_bytecode = True
        mod = __import__(os.path.basename(config_file).rstrip(".py"))
        config = mod.Plan
        sys.dont_write_bytecode = False

        # set configuration file as refinement plan
        self.refinement_plan_file = config_file

        # set parameter bounds
        self.bounds = config.parameters

        # handle configuration dict
        for option, val in config.configuration.items():
            setattr(self, option, val)

        # handle solver dict
        self.solver_kwargs = {option : val
                              for option, val in config.solver.items()}

