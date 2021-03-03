#! /usr/bin/env python
""" Inspects the contents of a solution file created with Spotlight.
"""

import argparse
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy
import os
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d, Axes3D
from scipy import interpolate
from spotlight import version
from spotlight.io import solution_file

# parse command line
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--input-file", default="tmp_spotlight/solution.db")
parser.add_argument("--output-file", default="tmp.png")
parser.add_argument("--abs", action="store_true")
parser.add_argument("--first-evaluation", action="store_true")
parser.add_argument("--version", action=version.VersionAction)
opts = parser.parse_args()

# style plots
rcParams = {
    "text.usetex": False,
    "figure.dpi": 600,
    "font.size": 10,
    "figure.figsize": (5, 2.5),
    "figure.subplot.left" : 0,
    "axes.titlesize": 10,
    "axes.labelsize": 10,
    "axes.labelpad" : 6,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
}
mpl.rcParams.update(rcParams)

# check that solution file exists
if not os.path.exists(opts.input_file):
    raise IOError("The input file does not exist!")

# read solution file
config, all_x, all_y, best_x, best_y = solution_file.SolutionFile.read_data(opts.input_file)

all_x = numpy.array(all_x)
all_x = numpy.vstack(all_x)
all_y = numpy.array(all_y)
all_y = numpy.hstack(all_y)
print(all_x.shape, all_y.shape)

if opts.abs:
    all_y = numpy.abs(all_y)

print(all_x[0], all_y[0])
print(all_y.max())
print(all_y.min())
print(best_x, best_y)

if opts.first_evaluation:
    all_x = all_x[:, 0, :]
    all_y = all_y[:, 0]

x = numpy.vstack(all_x)
z = numpy.hstack(all_y)
print(x.shape, z.shape)

# add noise to prevent duplicates for interpolation
#if not x.shape[0] == numpy.unique(x).shape[0]:
_x = x + numpy.random.normal(scale=1e-8, size=x.shape)
#else:
#    _x = x

f = interpolate.Rbf(*numpy.vstack((_x.T, z)), smooth=0, function="thin_plate")
interp = f(*x.T)



# create figure
fig = plt.figure(figsize=(5, 2.5))
ax = Axes3D(fig)
#ax = fig.gca(projection="3d")
#ax.autoscale(tight=True)

# parameter indices to plot
axes = (0, 1)

# build grid of points
M = 200
ix = [i for i in range(len(x.T)) if i not in axes]
fix = enumerate(x[numpy.argmin(z)])
fix = numpy.array(tuple(j for (i, j) in fix if i not in axes))
grid = numpy.ones((len(x.T), M, M))
grid[ix] = fix[:, None, None]
del ix, fix

# build the sub-surface of surrogate model to display and apply to the grid
axes = list(axes)
xy = x.T[axes]
S = complex('{}j'.format(M))
grid[axes] = numpy.mgrid[xy[0].min():xy[0].max():S, xy[1].min():xy[1].max():S]
del xy

# evaluate the surrogate on the sub-surface
z_ = f(*grid)

# plot the surface and points
density = 9
d = max(11 - density, 1)
x_ = grid[axes[0]]
y_ = grid[axes[-1]]
ax.plot_surface(x_, y_, z_, rstride=d, cstride=d, cmap=cm.Spectral,
                linewidth=0, antialiased=True)
x_ = x.T[axes[0]]
y_ = x.T[axes[-1]]
#ax.plot(x_, y_, z, "ko", linewidth=2, markersize=4)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$f(x,y)$")
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(0, 30)
ax.set_xticks([-10, -5, 0, 5, 10])
ax.set_yticks([-10, -5, 0, 5, 10])
ax.set_zticks([0, 10, 20, 30])
ax.zaxis.set_rotate_label(False)
ax.view_init(elev=75.0, azim=120.0)
ax.dist = 12.5

plt.tight_layout()

# display
#plt.show()
plt.savefig(opts.output_file)
