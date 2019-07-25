""" This module contains classes for reading and writing output data.
"""

import numpy
from klepto import archives

class Archive(object):
    """ This class handles reading and writing output data from the
    optimization analysis.

    Attributes
    ----------
    arch : file_archive
        A Klepto file archive.
    names : list
        A list of names. This list is ordered how packages will return a list.
    path : str
        Path to archive file.

    Parameters
    ----------
    path : str
        Path to archive file.
    names : list
        A list of names. This list is ordered how packages will return a list.
    """

    def __init__(self, path, names):
        self.path = path
        self.arch = archives.file_archive(path)
        self.names = names

    def save_data(self, key, local_solver):
        """ Writes output data from a local solver. Adds the given solution to
        an archive file.
 
        Parameters
        ----------
        key : iterable
            The ``dict`` key to use for this solution in archive file.
        local_solver : Solver
            A ``Solver`` instance.
        """

        # load new data in archive file
        self.arch.load()

        # add names of parameters
        names_key = "names"
        if names_key not in self.arch.keys():
            self.arch[names_key] = self.names
        else:
            assert(self.names == self.arch[names_key])

        # add this solution
        sol = list(local_solver.solution) + [None]
        if key in self.arch.keys():
            self.arch[key][0] += sol[0]
            self.arch[key][1] += sol[1]
            if sol[3] < self.arch[key][3]:
                self.arch[key][2] = sol[2]
                self.arch[key][3] = sol[3]
        else:
            self.arch[key] = sol

        # check if termination condition met
        # if not then add the local_solver instance
        if local_solver.local_solver.Terminated(disp=1, info=True):
            self.arch[key][4] = None
        else:
            self.arch[key][4] = local_solver

        # save new data to archive file
        self.arch.dump()

    @classmethod
    def read_data(cls, input_files, verbose=False):
        """ Reads output data.

        Parameters
        ----------
        input_files : list
            List of files to read.
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

        # keys to ignore
        restricted_keys = ["names"]

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
            input_file = archives.file_archive(input_file)
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
                if key in restricted_keys:
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

