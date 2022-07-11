""" This module contains classes for managing diffraction analyses.
"""

import configparser
import numpy
import os
import pickle
import sys
from spotlight import filesystem
from spotlight import solver

class Item(object):
    """ This class contains information about the detector or instrument.
    Any non-required keywords given while initializing an instance will be
    added as attributes.

    Attributes
    ----------
    data_file : str
        Path to data file.
    detector_file : str
        Path to detector or instrument file.

    Parameters
    ----------
    data_file : str
        Path to data file.
    detector_file : str
        Path to detector or instrument file.
    """

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if not isinstance(val, str):
                setattr(self, key, val)
            elif val.isdigit():
                setattr(self, key, int(val))
            else:
                try:
                    val = float(val)
                    setattr(self, key, val)
                except ValueError:
                    setattr(self, key, val)

class ConfigurationFile(object):
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

        # if configuration file is in ConfigParser format
        if all([config_file.endswith(".ini") for config_file in config_files]):

            # concatenate configuration files
            self.cp = configparser.ConfigParser()
            self.cp.read(config_files)
            if config_overrides:
                for override in config_overrides:
                    self.apply_override(override)

            # set attributes from configuration file
            self.read_config()

        # else if configuration file is a single Python file
        elif len(config_files) == 1 and config_files[0].endswith(".py"):

            # set attributes from configuration file
            self.read_py_config(config_files[0])
            if config_overrides:
                for override in config_overrides:
                    self.apply_override_py(override)

        # else do not recognize configuration file format
        else:
            raise ValueError("Do not recognize configuration file format!")

        # refinement plan is not loaded until get_refinement_plan is called
        self.refinement_plan = None

        # set atrributes for names and indices of parameters
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
        """ Applies an override to the configuration.
        """
        section, option, value = override.split(":")
        if hasattr(self, "items") and section == "parameters":
            name = option.split("-")[0].upper()
            if option.endswith("-min"):
                self.bounds[name][0] = float(value)
            elif option.endswith("-max"):
                self.bounds[name][1] = float(value)
            else:
                raise KeyError("Do not recognize override {}!".format(override))
        elif hasattr(self, "items"):
            if "-" in section:
                sec, i = section.split("-")
                i = int(i)
                setattr(self.items[sec][i], option, value)
            else:
                setattr(self.items[section], option, value)
        else:
            if option.startswith("-"):
                self.cp.remove_option(section, option)
            if not self.cp.has_section(section):
                self.cp.add_section(section)
            self.cp.set(section, option, value)

    def apply_override_py(self, override):
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

        # copy files to temporary dir
        for key in self.items.keys():
            items = self.items[key] if isinstance(self.items[key], list) \
                        else [self.items[key]]
            for item in items:
                for attr in dir(item):
                    if attr.endswith("_file"):
                        new_file = filesystem.cp(getattr(item, attr), tmp_dir) \
                               if tmp_dir else getattr(item, attr)
                        setattr(item, attr, new_file)

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
                                         initialize=initialize, **self.items)

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

        # read configuration file
        if config_file:
            cp = configparser.ConfigParser()
            cp.readfp(open(config_file, "r"))
        else:
            cp = self.cp

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
            params[name] = [lb, ub]
        self.bounds = params   
 
        # get all sections that will become attributes
        restricted_sections = ["configuration", "solver", "parameters"]
        counts = {}
        items = {}
        secs = cp.sections()
        secs.sort()
        for sec in secs:

            # skip restricted keys
            if sec in restricted_sections:
                continue

            # count number in each section group
            elif "-" in sec:
                sec, _ = sec.split("-")
                if sec not in counts.keys():
                    counts[sec] = 0
                counts[sec] += 1

            # handle single sections
            else:
                kwargs = {opt : cp.get(sec, opt) for opt in cp.options(sec)}
                items[sec] = Item(**kwargs)

        # handle each section group
        for sec, num in counts.items():
            items[sec] = num * [None]
            for i in range(num):
                section_i = "{}-{}".format(sec, i)
                kwargs = {opt : cp.get(section_i, opt) for opt in cp.options(section_i)}
                items[sec][i] = Item(**kwargs)
        self.items = items

        # set attributes from [configuration]
        section = "configuration"
        for option in cp.options(section):
            val = cp.get(section, option)
            if val.isdigit():
                setattr(self, option, int(val))
            else:
                try:
                    val = float(val)
                    setattr(self, option, val)
                except ValueError:
                    setattr(self, option, val)

        # store all options from [solver]
        self.solver_kwargs = {}
        section = "solver"
        for option in cp.options(section):
            val = cp.get(section, option)
            if val.isdigit():
                self.solver_kwargs[option] = int(val)
            else:
                try:
                    val = float(val)
                    self.solver_kwargs[option] = val
                except ValueError:
                    self.solver_kwargs[option] = val

    def read_py_config(self, config_file=None):
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

        # do not handle items since configuration file
        # can have class attributes
        self.items = {}
