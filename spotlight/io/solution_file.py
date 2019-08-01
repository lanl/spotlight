""" This module contains classes for reading and writing output data
using the klepto archive file.
"""

import dill
import numpy
from klepto import archives

class SolutionFile(object):
    """ This class handles reading and writing output data from the
    optimization analysis.

    Attributes
    ----------
    arch : dir_archive
        A Klepto directory-based archive.
    names : list
        A list of names. This list is ordered how packages will return a list.
    restricted_keys : list
        A list of specially named keys.
    path : str
        Path to archive file.

    Parameters
    ----------
    path : str
        Path to archive file.
    names : list
        A list of names. This list is ordered how packages will return a list.
    """

    # special keys
    restricted_keys = ["names"]

    def __init__(self, path, names):

        # store information
        self.path = path
        self.arch = archives.dir_archive(self.path)
        self.names = names

    def save_names(self, names=None):
        """ Writes names of parameters.
 
        Parameters
        ----------
        names : None, list
            The list of names. The index should match the order the parameter is
            stored in the local solver.
        """

        # load new data in archive file
        names_key = "names"
        self.arch.load(names_key)

        # add names of parameters
        if names_key not in self.arch.keys():
            self.arch[names_key] = self.names if names == None else names
            self.arch.dump(names_key)
        else:
            assert(self.names == self.arch[names_key])

    def save_data(self, key, local_solver, time=None):
        """ Writes output data from a local solver. Adds the given solution to
        an archive file.
 
        Parameters
        ----------
        key : iterable
            The ``dict`` key to use for this solution in archive file.
        local_solver : Solver
            A ``Solver`` instance.
        time : float
            An optional argument to store time to completion.
        """

        # load new data in archive file
        self.arch.load(key)

        # add this solution
        sol = list(local_solver.solution) + [None, time] + list(local_solver.diagnostics)
        if key in self.arch.keys():
            self.arch[key][0] += sol[0]
            self.arch[key][1] += sol[1]
            self.arch[key][6] = sol[6]
            self.arch[key][7] = sol[7]
            if sol[3] < self.arch[key][3]:
                self.arch[key][2] = sol[2]
                self.arch[key][3] = sol[3]
            if self.arch[key][5] != None and sol[5] != None:
                self.arch[key][5] += sol[5]
        else:
            self.arch[key] = sol

        # check if termination condition met and store result
        if local_solver.local_solver.Terminated(disp=1, info=True):
            self.arch[key][4] = 1
        else:
            self.arch[key][4] = 0

        # save new data to archive file
        self.arch.dump(key)

    @classmethod
    def read_data(cls, input_files, keys=None, verbose=False):
        """ Reads output data.

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
        names : list
            A list of names. This list is ordered how packages will return
            a list.
        all_x : numpy.array
            A multi-dimensional array with shape ``(npoints, nparams)`` for all
            points. This contains parameter values evaluated.
        all_y : numpy.array
            A one-dimensional array with shape ``(npoints,)`` for all points.
            This contains the minimized cost function value for all points.
        best_x : list
            Best set of parameter values.
        best_y : list
            Best cost function minimized value.
        """

        # initialize some values
        names = None
        all_x = []
        all_y = []
        best_x = None
        best_y = numpy.inf
 
        # loop over data files
        num_files = len(input_files)
        for i, input_file in enumerate(input_files):
            if verbose:
                print("Reading file {} of {} named {}...".format(i + 1,
                                                                 num_files,
                                                                 input_file))

            # open input file
            input_file = archives.dir_archive(input_file)
            if keys:
                input_file.load(*cls.restricted_keys + keys)
            else:
                input_file.load()

            # read parameter names
            if "names" not in input_file.keys():
                print("Could not read parameters names from file!")
                continue
            elif i == 0:
                names = input_file["names"]
            else:
                assert(names == input_file["names"])

            # loop over solvers in file
            for key in input_file.keys():
                if key in cls.restricted_keys:
                    continue
                x = numpy.array([])
                y = numpy.array([])
                vecs, fopts, result_x, result_y = input_file[key][:4]
    
                # check if new best
                if result_y < best_y:
                    best_x, best_y = result_x, result_y
    
                # add to a (npoints, nparams) x-array
                # add to a (npoints,) y-array
                vecs = numpy.vstack([vecs])
                fopts = numpy.array(fopts)
                #x = vecs if x.size == 0 else numpy.vstack([x, vecs])
                #y = fopts if y.size == 0 else numpy.hstack([y, fopts])
                x = vecs
                y = fopts

                # list of results
                all_x.append(numpy.array(x))
                all_y.append(numpy.array(y))
    
        return names, all_x, all_y, best_x, best_y
