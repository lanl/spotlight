"""  This module contains classes for handling phase information.
"""

import numpy

class Phase(object):
    """ This class contains information about a particular phase.

    Attributes
    ----------
    phase_file : str
        Path to phase file.
    phase_number : int
        Number of this phase in phase file.

    Parameters
    ----------
    phase_file : str
        Path to phase file.
    phase_number : int
        Number of this phase in phase file.
    """

    def __init__(self, phase_file, phase_number):
        self.phase_file = phase_file
        self.phase_number = phase_number
