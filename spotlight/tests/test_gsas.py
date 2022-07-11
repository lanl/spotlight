""" Test for the GSAS module that connects to gsaslanguage. Most of these tests
will raise an error without GSAS installed.
"""

import unittest
from spotlight import gsas

class TestGSAS(unittest.TestCase):

    def test_gsas_add_histogram(self):
        with self.assertRaises(FileNotFoundError) as cm:
            gsas.gsas_add_histogram("testfile.txt", "testfile.txt", 2,
                                    1.0, max_d_spacing=2.0, debug=False)

