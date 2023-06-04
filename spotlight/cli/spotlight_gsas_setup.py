#! /usr/bin/env python
""" Setup a GSAS or GSAS-II experiment for the best match from an optimization search.
Optionally for GSAS, creates a PDF for best match.
"""

import argparse
import matplotlib as mpl; mpl.use("Agg")
import numpy
from matplotlib import pyplot as plt
from spotlight import gsas
from spotlight import version
from spotlight.io import solution_file

def main():

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-files", nargs="+", required=True)
    parser.add_argument("--tmp-dir", default="tmp")
    parser.add_argument("--gsas-done", action="store_true")
    parser.add_argument("--version", action=version.VersionAction)
    opts = parser.parse_args()
    
    # read data
    config, _, _, best_x, best_y = solution_file.SolutionFile.read_data(opts.input_files,
                                                                        verbose=True)
    
    # print best parameters
    print("Best parameters are...")
    print("CHISQ {}".format(best_y))
    for name, val in zip(config.names, best_x):
        print("{} {}".format(name, val))
    
    # move to temporary dir, read configuration file, and get refinement plan
    print("Run refinement plan to get output...")
    config.setup_dir(opts.tmp_dir)
    cost = config.get_refinement_plan()
    
    # set random seed
    numpy.random.seed(config.seed)
    
    # run refinement plan
    cost.function(best_x)
    
    # create PDF file
    if opts.gsas_done:
        print("Creating PDF...")
        gsas.gsas_refine(1)
        gsas.gsas_done()
    
    # print statement
    print("Done!")

if __name__ == "__main__":
    main()
