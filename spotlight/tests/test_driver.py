""" This module constructs tests for the command line driver.
"""

import contextlib
import io
import os
import spotlight
import sys
import unittest
from spotlight import driver

class TestDriver(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_cli_version(self):
        """ Tests the command ``spotlight_minimize --version`` completes.
        """
        d = driver.Driver()
        with self.assertRaises(SystemExit) as cm:
            d.parse_command_line(["--version"])

    def test_parse_command_line(self):
        """ Tests parsing the command line.
        """

        # test override a single argument
        d = driver.Driver()
        d.parse_command_line([
                "--config-file", os.path.join(
                    os.path.dirname(spotlight.__file__),
                    "tests", "configs", "config_hello_world.py"),
                "--config-override", "var2", "Packers"])

