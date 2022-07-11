
class Container(object):
    """ This class contains information about the detector or instrument.
    Any non-required keywords given while initializing an instance will be
    added as attributes.

    Attributes
    ----------
    data_file : str
        Path to data file.
    detector_file : str
        Path to detector or instrument file.

    Parameters
    ----------
    data_file : str
        Path to data file.
    detector_file : str
        Path to detector or instrument file.
    """

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if not isinstance(val, str):
                setattr(self, key, val)
            elif val.isdigit():
                setattr(self, key, int(val))
            else:
                try:
                    val = float(val)
                    setattr(self, key, val)
                except ValueError:
                    setattr(self, key, val)

