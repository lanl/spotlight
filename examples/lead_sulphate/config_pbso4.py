""" A refinement plan for lead sulphate.
"""

import io
import sys
import GSASIIlattice as lattice
import GSASIIscriptable as gsasii
from spotlight import plan
from spotlight.container import Container

def silent_stdout(func):
    """ Decorator to silence stdout.
    """
    def _wrapper(*args, **kwargs):

        # create a text trap and redirect stdout
        silent_stdout = io.StringIO()
        sys.stdout = silent_stdout

        # execute
        out = func(*args, **kwargs)

        # now restore stdout function
        sys.stdout = sys.__stdout__

        return out

    return _wrapper

class Plan(plan.BasePlan):
    name = "plan_pbso4"
    gpx = None

    # required to have solution_file, state_file, and num_solvers
    configuration = {
        "solution_file" : "solution.db",
        "state_file" : "state.db",
        "num_solvers" : 3,
        "checkpoint_stride" : 1,
    }

    # required to have local solver and sampling method
    # all other special options get added to a Solver instance
    # any non-special options are passed to the Solver.solve function
    solver = {
        "local_solver" : "powell",
        "max_evaluations" : 25,
        "sampling_method" : "uniform",
    }

    # define a list of detectors
    detectors = [Container(data_file="../PBSO4.xra",
                           detector_file="../INST_XRY.prm",
                           min_two_theta=16.0,
                           max_two_theta=158.4),
                 Container(data_file="../PBSO4.cwn",
                           detector_file="../inst_d1a.prm",
                           min_two_theta=19.0,
                           max_two_theta=153.0)]

    phases = [Container(phase_file="../PbSO4-Wyckoff.cif",
                        phase_label="PBSO4")]

    # parameters names and bounds
    # in compute function use self.get("x") to use optimizer's value for "x"
    parameters = {
        "PBSO4_A" : [7.6266, 9.3214], # 8.474 +/- 10%
        "PBSO4_B" : [4.8546, 5.9334], # 5.394 +/- 10%
        "PBSO4_C" : [6.2586, 7.6494], # 6.954 +/- 10%
    }

    @silent_stdout
    def initialize(self):

        # create a GSAS-II project
        self.gpx = gsasii.G2Project(newgpx="{}.gpx".format(self.name))
        
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

    @silent_stdout
    def compute(self):

        # create a GSAS-II project
        self.gpx = gsasii.G2Project("step_1.gpx")
        self.gpx.save("step_2.gpx")

        # change lattice parameters
        for phase in self.gpx["Phases"].keys():

            # ignore data key
            if phase == "data":
                continue

            # handle PBSO4 phase
            elif phase == "PBSO4":
                cell = self.gpx["Phases"][phase]["General"]["Cell"]
                a, b, c = self.get("PBSO4_A"), self.get("PBSO4_B"), self.get("PBSO4_C")
                t11, t22, t33 = cell[1] / a, cell[2] / b, cell[3] / c
                self.gpx["Phases"][phase]["General"]["Cell"][1:] = lattice.TransformCell(
                    cell[1:7], [[t11, 0.0, 0.0],
                                [0.0, t22, 0.0],
                                [0.0, 0.0, t33]])

            # otherwise raise error because refinement plan does not support this phase
            else:
                raise NotImplementedError("Refinement plan cannot handle phase {}".format(phase))

        # turn on unit cell refinement
        args = {
            "set": {
                "Cell" : True,
            }
        }
        
        # refine
        self.gpx.set_refinement(args)
        self.gpx.do_refinements([{}])

        # get histograms and phases
        hist1, hist2 = self.gpx.histograms()
        phase1 = self.gpx.phases()[0]

        # turn on Dij terms (HAP) for phase 1 only
        args6 = {
            "set" : {
                "HStrain" : True
            },
            "histograms" : [hist1],
            "phases" : [phase1],
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
        }
        
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
            "histograms" : [hist2],
        }

        # change data limits and instrument parmeter refinements (Hist)
        args9a = {
            "set": {
                "Limits" : [16.0, 158.4],
            },
            "histograms" : [hist1],
            "skip": True,
        }
        args9b = {
            "set": {
                "Limits" : [19.0, 153.0],
            },
            "histograms" : [hist2],
            "skip": True,
        }
        args9c = {
            "set": {
                "Instrument Parameters" : ["U", "V", "W"],
            },
        }

        # change number of cycles and radius
        self.gpx.data["Controls"]["data"]["max cyc"] = 8
        hist2.data["Sample Parameters"]["Gonio. radius"] = 650.0

        # refine
        args_list = [args6, args7, args8a, args8b, args9a, args9b, args9c]
        self.gpx.do_refinements(args_list)

        # get minimization statistic
        stat = self.gpx["Covariance"]["data"]["Rvals"]["Rwp"]

        return stat
