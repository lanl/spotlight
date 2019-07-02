"""  This module contains classes for handling detector or instrument
information.
"""

class Detector(object):
    """ This class contains information about the detector or instrument. The
    only required parameter is ``detector_file``, otherwise any keywords given
    while initializing an instance will be added as attributes.

    Attributes
    ----------
    detector_file : str
        Path to detector or instrument file.

    Parameters
    ----------
    detector_file : str
        Path to detector or instrument file.
    """

    def __init__(self, detector_file, **kwargs):
        self.detector_file = detector_file
        for key, val in kwargs.items():
            if val.isdigit():
                setattr(self, key, int(val))
            else:
                try:
                    val = float(val)
                    setattr(self, key, val)
                except ValueError:
                    setattr(self, key, val)
