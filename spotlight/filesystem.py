""" This module contains functions for managing files.
"""

import os
import shutil
import sys

def mkdir(run_dir, change=False):
    """ Makes a directory and optionally changes into it.

    Parameters
    ----------
    run_dir : str
        Path of directory to create.
    change : bool
        Change into directory after creation. Default is ``False``.
    """

    # make temporary directory
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)

    # change into temporary directory
    if change:
        os.chdir(run_dir)
        sys.path.append(os.getcwd())

def cp(paths, dest=None):
    """ Copies files into the current directory and returns a list of the new
    filenames.

    Parameters
    ----------
    paths : {str, list}
        Either a string or list of strings that contain path of files to copy.
    dest : {None, str}
        Destination to copy file. Default is ``None`` and copies to current
        directory.

    Returns
    -------
    paths_out : {str, list}
        Type matches input variable ``paths``. The path to the copied files.
    """

    # make destination directory
    if dest:
        if not os.path.exists(dest):
            os.makedirs(dest)

    # typecast paths to list
    paths_list = [paths] if isinstance(paths, str) else paths

    # copy paths into temporary directory
    for path in paths_list:
        final_path = dest + "/" + os.path.basename(path) if dest \
                         else os.path.basename(path)
        try:
            shutil.copyfile(path, final_path)
        except shutil.SameFileError:
            print("File {} already exists!".format(path))

    # typecast paths to str
    paths_out = [os.path.basename(path) for path in paths_list]
    if isinstance(paths, str):
        paths_out = paths_out[0]

    return paths_out
