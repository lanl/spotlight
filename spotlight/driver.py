""" This module contains functions for handling the command line interface
to Spotlight.
"""

import argparse
try:
    from spotlight import version
    version_action = version.VersionAction
except ImportError:
    from spotlight import _version
    version_action = _version.NoVersionAction

class Driver:
    """ Driver to execute a pipeline from command line interface.

    Attributes
    ----------
    opts : argparse.Namespace
        The command line arguments.
    """

    def __init__(self):
        self.opts = None

    def parse_command_line(self, opts_list=None):
        """ Generates the command line options for the driver.

        Parameters
        ----------
        opts_list : list
            A ``list`` of ``str`` that can be passed as options to parser.

        Returns
        -------
        opts : argparse.Namespace
            The namespace from argparse returned. This is returned
            from ``argparse.parse_args``.
        """
        parser = argparse.ArgumentParser(description="Executes a minimization")
        parser.add_argument("--config-files", nargs="+", required=True)
        parser.add_argument("--config-overrides", nargs="+")
        parser.add_argument("--tmp-dir", default="tmp")
        parser.add_argument("--verbose", action="store_true")
        parser.add_argument("--version", action=version.VersionAction)
        self.opts = parser.parse_args(opts_list)
        return self.opts

    def minimize(self, opts=None):
        pass

