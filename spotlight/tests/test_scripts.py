""" This module constructs tests for all Python scripts
stored in the ``fusion/tests/scripts`` directory.
"""

import glob
import importlib
import os
import shutil
import subprocess
import sys
import unittest

class TestScripts(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestScripts, self).__init__(*args, **kwargs)

        # set the path to data files and script files
        data_dir = os.path.dirname(__file__) + "/data"
        script_dir = os.path.dirname(__file__) + "/scripts"

        # add dirs with script files to path
        sys.path.append(script_dir)

    def tearDown(self):
        """ Upon exiting each test.
        """
        os.chdir("..")

def make_test_function(tmp_dir, script_file=None, mod_name=None,
                       language="python"):
    """ This function returns a function that executes a test of
    a Python or Bash script. It simply creates a temporary directory,
    changes into it, and executes the script.

    Parameters
    ----------
    tmp_dir : str
        Path to the directory to perform the test.
    script_name : str
        The Bash script name; only used if ``language`` is ``bash``.
    mod_name: str
        The Python module name; only used if ``language`` is ``python``.
    language : str
        Either ``python`` or ``bash``.

    Returns
    -------
    _function : function
        A function to execute the test.
    """
    if language == "python":
        def _function(self):
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            os.makedirs(tmp_dir)
            os.chdir(tmp_dir)
            mod = importlib.import_module(mod_name)
    elif language == "bash":
        def _function(self):
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            os.makedirs(tmp_dir)
            os.chdir(tmp_dir)
            exit_code = _external_call(["bash", script_file], debug=True)
            if exit_code != 0:
                sys.exit(exit_code)
    else:
        raise ValueError("The langauge must be either 'python' or 'bash'!")
    return _function

def _external_call(cmd, log_file=None, debug=True):
    """ This function makes external calls.
    """
    if debug:
        print(cmd)
    cmd = cmd.split() if isinstance(cmd, str) else cmd
    cmd = list(map(str, cmd))
    fp = open(log_file, "w") if log_file else subprocess.PIPE
    p = subprocess.Popen(cmd,
                         stdin=fp,
                         stdout=fp,
                         stderr=fp)
    stdout, stderr = p.communicate()
    if debug:
        print(stdout)
        print(stderr)
    return p.returncode

# loop over configuration files
test_names = []
script_dir = os.path.dirname(__file__) + "/scripts"
script_files = glob.glob(os.path.join(script_dir, "*.py"))
script_files += glob.glob(os.path.join(script_dir, "*.sh"))
for script_file in script_files:

    # since script dir is in path get module name for import
    # scripts are assumed to be a Python script
    mod_name = os.path.basename(script_file)[:-len(".py")]
    language = "python" if script_file.endswith(".py") else "bash"

    # make test function for this script file
    # and append to test instance
    name = "test_" + os.path.basename(script_file).replace(".", "_")
    tmp_dir = "tmp_" + name
    _function = make_test_function(tmp_dir, script_file=script_file,
                                   mod_name=mod_name, language=language)
    setattr(TestScripts, name, _function)

