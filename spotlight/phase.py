"""  This module contains classes for handling phase information.
"""

import numpy

class Phase(object):
    """ This class contains information about a particular phase.
    Any non-required keywords given while initializing an instance will be
    added as attributes.

    Attributes
    ----------
    phase_file : str
        Path to phase file.

    Parameters
    ----------
    phase_file : str
        Path to phase file.
    """

    def __init__(self, phase_file, **kwargs):
        self.phase_file = phase_file
        for key, val in kwargs.items():
            if val.isdigit():
                setattr(self, key, int(val))
            else:
                try:
                    val = float(val)
                    setattr(self, key, val)
                except ValueError:
                    setattr(self, key, val)
