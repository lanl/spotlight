""" A refinement plan for lead sulphate.
"""

import GSASIIscriptable as gsasii
from spotlight import plan

class Plan(plan.BasePlan):
    name = "plan_pbso4"
    gpx = None

    def initialize(self):

        # create a GSAS-II project
        self.gpx = gsasii.G2Project(newgpx=self.name)
        
        # add histograms
        for det in self.detectors:
            self.gpx.add_powder_histogram(det.data_file, det.detector_file)
        
        # add phases
        for phase in self.phases:
            self.gpx.add_phase(phase.phase_file, phase.phase_label,
                               histograms=self.gpx.histograms())

        # turn on background refinement
        args = {
                "Background": {
                    "no. coeffs" : 3,
                    "refine": True,
                }
        }
        for hist in self.gpx.histograms():
            hist.set_refinements(args)

        # refine
        self.gpx.do_refinements([{}])
        self.gpx.save("step_1.gpx")

    def compute(self):

        # get minimization statistic
        stat = self.gpx["Covariance"]["data"]["Rvals"]["Rwp"]

        return stat
