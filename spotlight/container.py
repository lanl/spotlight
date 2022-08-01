""" This module contains classes that act as generic containers holding the attributes
given in its constructor.
"""

class Container:
    """ This class contains information passed in the constructor. For example,
    information about the detector or instrument. Any keywords given to the
    constructor will be added as attributes.
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

