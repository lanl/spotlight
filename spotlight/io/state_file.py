""" This module contains classes for reading and writing local optimization
state data using the klepto archive file.
"""

import dill
import numpy
from klepto import archives

class StateFile(object):
    """ This class handles reading and writing local optimization state data
    from the optimization analysis.

    Attributes
    ----------
    arch : dir_archive
        A Klepto directory-based archive.
    path : str
        Path to archive file.

    Parameters
    ----------
    path : str
        Path to archive file.
    """

    # special keys
    restricted_keys = ["names"]

    def __init__(self, path):

        # store information
        self.path = path
        self.arch = archives.dir_archive(self.path)

        # load new data in archive file
        self.arch.load()

    def save_state(self, key, local_solver):
        """ Writes state data from a local solver.
 
        Parameters
        ----------
        key : iterable
            The ``dict`` key to use for this solution in archive file.
        local_solver : Solver
            A ``Solver`` instance.
        """

        # load new data in archive file
        self.arch.load(key)

        # check if termination condition met
        # if not then add the local_solver instance
        # clear cost function from local solver due to pickling issues
        if local_solver.local_solver.Terminated(disp=1, info=True):
            self.arch[key] = None
        else:
            local_solver._cost = None
            self.arch[key] = local_solver

        # save new data to archive file
        self.arch.dump(key)

    @classmethod
    def read_state(cls, input_files, keys=None, verbose=False):
        """ Reads state data.

        Parameters
        ----------
        input_files : list
            List of files to read.
        keys : {None, list}
            List of specific keys to load instead of all keys.
        verbose : bool
            Print some messages to ``stdout``.

        Returns
        -------
        state : Solver
            A ``Solver`` instance for the local solver.
        """
        raise NotImplementedError("Read state function not implemented!")
