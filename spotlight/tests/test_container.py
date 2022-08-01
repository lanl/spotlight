""" Test for the ``Container`` class.
"""

import unittest
from spotlight import container

class TestContainer(unittest.TestCase):

    def test_container(self):
        c = container.Container(a=1, b="hello", c=3.2)
        self.assertTrue(c.a, 1)
        self.assertTrue(c.b, "hello")
        self.assertTrue(c.c, 3.2)

