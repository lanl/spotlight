#! /usr/bin/env python
""" Plots a histogram from a GSAS-II refinement.
"""

import matplotlib.pyplot as plt
import numpy
import GSASIIscriptable as gsasii

# labels
phase_labels = {
    "PbSO4" : "PbSO$_{4}$",
}

# read project
gpx = gsasii.G2Project("tmp_gsasii/final.gpx")

# create figure
fig = plt.figure()

# plot histogram
x = gpx.histogram(0).getdata("x")
y_obs = gpx.histogram(0).getdata("yobs")
y_calc = gpx.histogram(0).getdata("ycalc")
plt.plot(x, y_obs, c="red")
plt.plot(x, y_calc, c="blue")

# display
#plt.show()
plt.savefig("tmp_gsasii/histogram.png")
plt.close()

# create figure
fig = plt.figure()

# plot reflections
categories_in_order = [r"{}".format(label) for label in phase_labels]
categories_in_order.sort()
colors = ["blue", "orange", "gray", "red"]
for i, phase in enumerate(categories_in_order):
    two_theta = gpx.histogram(0).reflections()[phase]["RefList"][:, 5]
    height = numpy.array(two_theta.size * [i])
    plt.scatter(two_theta, height, marker="|", c=colors[i])

# format
plt.yticks(range(len(categories_in_order)), categories_in_order)
plt.xlabel(r"$2 \theta$")
plt.ylim(-1, len(categories_in_order))
plt.grid()
plt.tight_layout()
position = (0.12, 0.15, 0.82, 0.77)
fig.axes[0].set_position(position)

# display
#plt.show()
plt.savefig("tmp_gsasii/reflections.png")
plt.close()

# create figure
fig = plt.figure()

# plot histogram
plt.plot(x, y_obs - y_calc, c="red")

# display
#plt.show()
plt.savefig("tmp_gsasii/residual.png")
plt.close()

