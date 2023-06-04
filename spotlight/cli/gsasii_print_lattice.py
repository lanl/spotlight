#! /usr/bin/env python
""" Writes a CSV file with the observed and modeled histograms, as well as the
reflections. Meant to mimic the output from ``gsas_write_csv``.
"""

import argparse
import numpy
import GSASIIscriptable as gsasii
from spotlight import version

def main():

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--version", action=version.VersionAction)
    opts = parser.parse_args()
    
    # read project
    gpx = gsasii.G2Project(opts.input_file)
    
    # print lattice parameters
    for phase in gpx.phases():
        if phase == "data":
            continue
        cell = gpx["Phases"][phase.name]["General"]["Cell"]
        print("Phase {} has lattice parameters: {} {} {}".format(
                  phase.name, cell[1], cell[2], cell[3]))
    
    # print varied parameters
    print("Varied Parameters:")
    for key, val in zip(gpx["Covariance"]["data"]["varyList"], gpx["Covariance"]["data"]["variables"]):
        print("{} = {}".format(key, val))
    
    # print statistic
    stat = gpx["Covariance"]["data"]["Rvals"]["Rwp"]
    print("The Rwp is: {}".format(stat))

if __name__ == "__main__":
    main()

