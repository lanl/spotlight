#! /usr/bin/env python
""" Example GSAS-II refinement. Based on tutorial at:
https://subversion.xray.aps.anl.gov/pyGSAS/Tutorials/PythonScript/Scripting.htm
"""

import matplotlib.pyplot as plt
import os
import sys
import GSASIIscriptable as gsasii

def print_stats(gpx):
    """ Prints profile r-factors for all histograms.
    """
    print(u"*** profile Rwp, " + os.path.split(gpx.filename)[1])
    for hist in gpx.histograms():
        print("\t{:20s}: {:.2f}".format(hist.name,hist.get_wR()))
    print("")

# where files will be written
work_dir = "tmp_gsasii"
if not os.path.exists(work_dir):
    os.mkdir(work_dir)

# where data files are stored
data_dir = os.getcwd()

# create a GSAS-II project
gpx = gsasii.G2Project(newgpx=os.path.join(work_dir, "PbSO4.gpx"))

# add histograms
hist1 = gpx.add_powder_histogram(
                          os.path.join(data_dir,"PBSO4.XRA"),
                          os.path.join(data_dir,"INST_XRY.PRM"))
hist2 = gpx.add_powder_histogram(
                          os.path.join(data_dir,"PBSO4.CWN"),
                          os.path.join(data_dir,"inst_d1a.prm"))

# add phase
phase1 = gpx.add_phase(os.path.join(data_dir, "PbSO4-Wyckoff.cif"),
                       phasename="PbSO4",
                       histograms=[hist1, hist2])

# increase number of cycles to improve convergence
gpx.data["Controls"]["data"]["max cyc"] = 8

# turn on background refinement (Hist)
args = {
        "Background": {
            "no. coeffs" : 3,
            "refine": True,
        }
}

# refine
gpx.save(os.path.join(work_dir, "step_4.gpx"))
for hist in gpx.histograms():
    hist.set_refinements(args)
gpx.do_refinements([{}])
print_stats(gpx)

# turn on unit cell refinement
gpx.save(os.path.join(work_dir, "step_4.gpx"))
args = {
    "set": {
        "Cell" : True,
    }
}

# refine
gpx.set_refinement(args)
gpx.do_refinements([{}])
print_stats(gpx)

# turn on Dij terms (HAP) for phase 1 only
args6 = {
    "set" : {
        "HStrain" : True
    },
    "histograms" : [hist1],
    "phases" : [phase1],
    "output" : os.path.join(work_dir, "step6.gpx"),
    "call" : print_stats,
}

# turn on size and strain broadening (HAP) for histogram 1 only 
args7 = {
    "set" : {
        "Mustrain" : {
            "type" : "isotropic",
            "refine" : True,
        },
        "Size" : {
            "type" : "isotropic",
            "refine" : True},
        },
        "histograms" : [hist1],
        "output" : os.path.join(work_dir, "step7.gpx"),
        "call" : print_stats}

# turn on sample parameters and radius (Hist)
# turn on atom parameters (phase)
args8a = {
    "set" : {
        "Sample Parameters" :
            ["Shift"]
    },
    "histograms" : [hist1],
    "skip": True,
}
args8b = {
    "set": {
        "Atoms" : {
            "all" : "XU",
        },
        "Sample Parameters" : ["DisplaceX", "DisplaceY"],
    },
    "histograms":[hist2],      # histogram 2 only 
    "output" : os.path.join(work_dir, "step8.gpx"),
    "call" : print_stats,
}

# change data limits & instrument parmeter refinements (Hist) 
args9a = {
    "set": {
        "Limits" : [16.0, 158.4],
    },
    "histograms":[hist1],
    "skip": True,
}
args9b = {
    "set": {
        "Limits" : [19.0, 153.0],
    },
    "histograms":[hist2],
    "skip": True,
}
args9c = {
    "set": {
        "Instrument Parameters" : ['U', 'V', 'W'],
    },
    "output" : os.path.join(work_dir, "step9.gpx"),
    "call" : print_stats,
}

# change number of cycles and radius
gpx.data["Controls"]["data"]["max cyc"] = 8
hist2.data["Sample Parameters"]["Gonio. radius"] = 650.0

# refine
args_list = [args6, args7, args8a, args8b, args9a, args9b, args9c]
gpx.do_refinements(args_list)

# plot
x = gpx.histogram(0).getdata("x")
y_obs = gpx.histogram(0).getdata("yobs")
y_calc = gpx.histogram(0).getdata("ycalc")
plt.plot(x, y_obs, c="red")
plt.plot(x, y_calc, c="blue")

# display
plt.show()
