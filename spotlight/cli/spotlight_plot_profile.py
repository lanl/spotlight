#! /usr/bin/env python
""" Plots the diffraction profile, residual, and reflection positions.
"""

import argparse
import itertools
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy
from spotlight import version

def main():

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file")
    parser.add_argument("--profile-file")
    parser.add_argument("--residual-file")
    parser.add_argument("--reflections-file")
    parser.add_argument("--phase-labels", nargs="+")
    parser.add_argument("--xlim", type=float, nargs=2, default=None)
    parser.add_argument("--version", action=version.VersionAction)
    opts = parser.parse_args()
    
    # load data
    data = numpy.loadtxt(opts.input_file, comments="#")
    
    # style plots
    rcParams = {
        "text.usetex": False,
        "figure.dpi": 600,
        "font.size": 10,
        "figure.figsize": (5, 2.5),
        "figure.subplot.left" : 0,
        "axes.titlesize": 10,
        "axes.labelsize": 10,
        "axes.labelpad" : 1,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
    }
    mpl.rcParams.update(rcParams)
    
    # determine range for plots
    if opts.xlim:
        x_min, x_max = opts.xlim
    else:
        x_min = data[:, 1].min()
        x_max = data[:, 1].max()
    
    # create profile plot
    if opts.profile_file:
    
        # create figure
        fig = plt.figure()
        
        # plot patterns
        plt.plot(data[:, 1], data[:, 2], "-", c="blue")
        plt.plot(data[:, 1], data[:, 3], "-", c="orange")
        
        # format
        plt.xlabel(r"D-spacing ($\AA$)")
        plt.ylabel(r"Normalized Counts")
        plt.xlim(x_min, x_max)
        plt.grid()
        plt.tight_layout()
        position = (0.12, 0.15, 0.82, 0.77)
        fig.axes[0].set_position(position)
        
        # save
        plt.savefig(opts.profile_file)
        plt.close()
    
    # create residual plot
    if opts.residual_file:
    
        # create figure
        fig = plt.figure()
        
        # plot residual
        plt.plot(data[:, 1], data[:, 4], "-", c="red")
        
        # format
        plt.xlabel(r"D-spacing ($\AA$)")
        plt.ylabel(r"Residual Normalized Counts")
        plt.xlim(x_min, x_max)
        plt.grid()
        plt.tight_layout()
        fig.axes[0].set_position(position)
        
        # save
        plt.savefig(opts.residual_file)
        plt.close()
    
    # create reflections plot
    if opts.reflections_file:
    
        # create figure
        fig = plt.figure()
        
        def powerset(iterable):
            "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
            s = list(iterable)  # allows duplicate elements
            return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
        
        # reflections are coded by sum of their values
        # 0 = none
        # 1 = zeroed
        # 4 = 1
        # 8 = 2
        # 12 = 1 + 2
        # 16 = 3
        # 20 = 3 + 1
        # 24 = 3 + 2
        # 32 = 4
        # 36 = 4 + 1
        # 40 = 4 + 2
        # 44 = 4 + 2 + 1
        # 48 = 4 + 3
        # 52 = 4 + 3 + 1
        # 56 = 4 + 3 + 2
        # 60 = 4 + 3 + 2 + 1
        # and more
        def phases_from_icode(val, n_phases, test_vals=None):
            phase_vals = [4]
            for n in range(n_phases):
                phase_vals.append(phase_vals[-1] * 2)
            test_vals = powerset(phase_vals) if test_vals == None else test_vals
            for powervals in powerset(phase_vals):
                if numpy.sum(powervals) == val:
                    result = []
                    for icode in powervals:
                        result.append(phase_vals.index(icode))
                    return result
        
        # plot reflections
        categories_in_order = [r"{}".format(label) for label in opts.phase_labels]
        colors = ["blue", "orange", "gray", "red"]
        for x, y in zip(data[:, 1], data[:, 5]):
            phase_ticks = phases_from_icode(y, len(categories_in_order))
            if phase_ticks == None:
                continue
            for t in phase_ticks:
                plt.scatter(x, t, marker="|", c=colors[t])
        
        # format
        plt.yticks(range(len(categories_in_order)), categories_in_order)
        plt.xlabel(r"D-spacing ($\AA$)")
        plt.xlim(x_min, x_max)
        plt.ylim(-1, len(categories_in_order))
        plt.grid()
        plt.tight_layout()
        fig.axes[0].set_position(position)
        
        # save
        plt.savefig(opts.reflections_file)
        plt.close()

if __name__ == "__main__":
    main()
