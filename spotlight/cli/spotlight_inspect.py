#! /usr/bin/env python
""" Inspects the contents of a solution file created with Spotlight.
"""

import argparse
import numpy
import os
import sys
from klepto import archives
from spotlight import version

def main():

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", default="tmp_spotlight/solution.pkl")
    parser.add_argument("--version", action=version.VersionAction)
    opts = parser.parse_args()
    
    # check that solution file exists
    if not os.path.exists(opts.input_file):
        raise IOError("The input file does not exist!")
    
    # read solutions
    print("Reading file", opts.input_file)
    arch = archives.dir_archive(opts.input_file)
    arch.load()
    
    # print information about each local solver
    keys = arch.keys()
    print(keys)
    nsolvers = 0
    nsolvers_terminated = 0
    restricted_keys = ["config"]
    best_val = numpy.inf
    for key in keys:
        if key in restricted_keys:
            continue
        sol = arch[key]
        print("The key is", key)
        print("The shape of the parameters array is", numpy.array(sol[0]).shape)
        print("The shape of the solution array is", numpy.array(sol[1]).shape, sol[1])
        print("The best parameters are:")
        for i, x in enumerate(sol[2]):
            print(arch["config"].names[i], x)
        print("The best cost function value is", sol[3])
        print("The local optimization completion is", sol[4])
        print("The duration in seconds is", sol[5])
        print("The number of optimization algorithm generations is", sol[6])
        print("The number of function evalualtions is", sol[7])
        print()
        nsolvers += 1
        nsolvers_terminated += 1 if sol[4] == True else 0
        if sol[3] < best_val:
            best_key = key
            best_val = sol[3]
    
    # print aggregate information about ensemble of local solvers
    print("{} of {} local solvers have terminated".format(nsolvers_terminated, nsolvers))
    print()
    
    # print best result
    print("The best result is", best_key)
    sol = arch[best_key]
    print("The shape of the parameters array is", numpy.array(sol[0]).shape)
    print("The shape of the solution array is", numpy.array(sol[1]).shape, sol[1])
    print("The best parameters are:")
    for i, x in enumerate(sol[2]):
        print(arch["config"].names[i], x)
    print("The best cost function value is", sol[3])
    print("The local optimization completion is", sol[4])
    print("The duration in seconds is", sol[5])
    print("The number of optimization algorithm generations is", sol[6])
    print("The number of function evalualtions is", sol[7])
    
    # for reference
    #from spotlight.io import solution_file
    #arch = solution_file.SolutionFile.read_data(opts.input_file)

if __name__ == "__main__":
    main()
