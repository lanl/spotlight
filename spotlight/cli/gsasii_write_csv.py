#! /usr/bin/env python
""" Writes a CSV file with the observed and modeled histograms, as well as the
reflections. Meant to mimic the output from ``gsas_write_csv``.
"""

import argparse
import numpy
import GSASIIscriptable as gsasii
from spotlight import version

def find_nearest(array, value):
    """ Returns the index of the nearest value in the array.
    """
    array = numpy.asarray(array)
    idx = (numpy.abs(array - value)).argmin()
    return idx

def main():

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--histogram", type=int, default=0)
    parser.add_argument("--version", action=version.VersionAction)
    opts = parser.parse_args()
    
    # delimiter of CSV file
    delimiter = "\t"
    
    # header of CSV file
    header = """
    #TITLE(1) =
    #TITLE(2) =
    #TITLE(3) =
    #X-AXIS LABEL = 
    #Y-AXIS LABEL = Norm. Counts
    #       X            YOBS           YCALC          YDIFF           ICODE
    """
    
    # read project
    gpx = gsasii.G2Project(opts.input_file)
    
    # read histograms
    x = gpx.histogram(opts.histogram).getdata("x")
    c = numpy.arange(x.size, dtype=int) + 1
    y_obs = gpx.histogram(opts.histogram).getdata("yobs")
    y_calc = gpx.histogram(opts.histogram).getdata("ycalc")
    y_diff = y_obs - y_calc
    
    # read reflections
    nphases = len(gpx.histogram(opts.histogram).reflections().keys())
    icode = numpy.zeros(x.size, dtype=int)
    for i, phase in enumerate(gpx.histogram(opts.histogram).reflections()):
        marked = numpy.zeros(x.size, dtype=int)
        for xi in gpx.histogram(opts.histogram).reflections()[phase]["RefList"][:, 5]:
            j = find_nearest(x, xi)
            if marked[j] == 0:
                icode[j] += (i + 1) * 4
                marked[j] += 1
     
    # save data
    data = numpy.vstack([c, x, y_obs, y_calc, y_diff, icode])
    data = numpy.transpose(data)
    fmt = ["%d", "%.8e", "%.8e", "%.8e", "%.8e", "%d"]
    numpy.savetxt(opts.output_file, data, header=header, delimiter=delimiter, fmt=fmt)

if __name__ == "__main__":
    main()

