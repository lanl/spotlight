""" A refinement plan for alumina.
"""

import os
from spotlight import gsas
from spotlight import plan
from spotlight.container import Container

class Plan(plan.BasePlan):
    name = "alumina_plan"
    debug = False

    # required to have solution_file, state_file, and num_solvers
    configuration = {
        "solution_file" : "solution.db",
        "state_file" : "state.db",
        "num_solvers" : 10,
        "checkpoint_stride" : 1,
    }

    # required to have local solver and sampling method
    # all other special options get added to a Solver instance
    # any non-special options are passed to the Solver.solve function
    solver = {
        "local_solver" : "powell",
        "stop_change" : 0.1,
        "stop_generations" : 3,
        "sampling_method" : "uniform",
    }

    # define a list of detectors
    detectors = [Container(data_file="../al2o3001.gsa",
                           detector_file="../bt1demo.ins",
                           bank_number=1,
                           min_d_spacing=0.7,
                           max_tof=155)]

    # define a list of phase items
    phases = [Container(phase_file="../alumina.exp",
                        phase_number=1)]

    # parameters names and bounds
    # in compute function use self.get("x") to use optimizer's value for "x"
    parameters = {
        "HSCL" : [13284.8, 14683.2], # 13984.0 +/- 5%
        "BK1" : [47.11297, 52.07223], # 49.5926 +/- 5%
        "BK2" : [-9.127671, -8.258369], # -8.69302 +/- 5%
        "BK3" : [19.20159, 21.22281], # 20.2122 +/- 5%
        "BK4" : [-7.858662, -7.110218], # -7.48444 +/- 5%
        "BK5" : [7.1434205, 7.8953595], # 7.51939 +/- 5%
        "BK6" : [-3.917193, -3.544127], # -3.73066 +/- 5%
        "BK7" : [3.2067155, 3.5442645], # 3.37549 +/- 5%
        "BK8" : [0.21431145, 0.23687055], # 0.225591 +/- 5%
        "BK9" : [1.681519, 1.858521], # 1.77002 +/- 5%
        "BK10" : [-1.0265913, -0.9288207], # -0.977706 +/- 5%
        "BK11" : [-0.5971455, -0.5402745], # -0.568710 +/- 5%
        "BK12" : [-0.8116731, -0.7343709], # -0.773022 +/- 5%
        "DIFC_Z" : [1.254, 1.386], # 1.32 +/- 5%
        "UISO_AL_ALUMINA" : [0.0023268825, 0.0025718175], # 0.00244935 +/- 5%
        "UISO_O_ALUMINA" : [0.003143417, 0.003474303], # 0.00330886 +/- 5%
        "X_O_ALUMINA" : [0.29115125, 0.32179875], # 0.306475 +/- 5%
        "Z_AL_ALUMINA" : [0.3343525, 0.3695475], # 0.351950 +/- 5%
        "A_ALUMINA" : [4.52257665, 4.99863735], # 4.760607 +/- 5%
        "C_ALUMINA" : [12.3469334, 12.3469334], # 12.996772 +/- 5%
        "GU_ALUMINA" : [205.82415, 227.48985], # 216.657 +/- 5%
        "GV_ALUMINA" : [-260.31705, -235.52495], # -247.921 +/- 5%
        "GW_ALUMINA" : [150.1608, 165.9672], # 158.064 +/- 5%
    }

    def initialize(self):

        # initialize
        gsas.gsas_initialize(self.name, "Alumina Example")

        # add phases
        phase_files = [p.phase_file for p in self.phases]
        phase_numbers = [p.phase_number for p in self.phases]
        for phase_file, phase_number in zip(phase_files, phase_numbers):
            gsas.gsas_read_phase(phase_file, phase_number, debug=self.debug)

        # add histograms
        for det in self.detectors:
            for bank_num in range(det.bank_number):
                gsas.gsas_add_histogram(det.data_file,
                                        det.detector_file,
                                        bank_num + 1,
                                        det.min_d_spacing, debug=self.debug)
                gsas.gsas_change_max_tof(bank_num + 1, det.max_tof)

        # change profile function
        for i, _ in enumerate(self.phases):
            for j, _ in enumerate(self.detectors):
                gsas.gsas_change_profile(j + 1, i + 1, 3)

    def compute(self):

        # copy experimental file
        gsas.gsas_copy_expfile(self.name, "TRIAL", "Test Parameters")

        # loop over phases
        for i, phase in enumerate(self.phases):

            # handle alumina phase
            if phase.phase_file == "../alumina.exp":

                # set lattice parameters
                gsas.gsas_change_lattice(i + 1, [self.get("A_ALUMINA"),
                                                 self.get("C_ALUMINA")], debug=self.debug)

                # set atom positions
                gsas.gsas_change_atom(i + 1, 1, "Z", self.get("Z_AL_ALUMINA"))
                gsas.gsas_change_atom(i + 1, 2, "X", self.get("X_O_ALUMINA"), debug=self.debug)

                # set isotropic thermal
                gsas.gsas_change_atom(i + 1, 1, "UISO", self.get("UISO_AL_ALUMINA"))
                gsas.gsas_change_atom(i + 1, 2, "UISO", self.get("UISO_O_ALUMINA"), debug=self.debug)

                # loop over detector banks
                # only one detector section
                for j in range(self.detectors[0].bank_number):

                    ## set phase scales
                    #gsas.gsas_change_phase_fraction(
                    #                    j + 1, i + 1,
                    #                    self.get("PHFR_ALUMINA"))

                    # set profile parameters
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 1,
                                                       self.get("GU_ALUMINA"), debug=self.debug)
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 2,
                                                       self.get("GV_ALUMINA"), debug=self.debug)
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 3,
                                                       self.get("GW_ALUMINA"), debug=self.debug)

                    # set profile cutoff
                    gsas.gsas_change_profile_cutoff(j + 1, i + 1, 0.00500, debug=self.debug)

            # otherwise raise error because refinement plan does not support this phase
            else:
                raise NotImplementedError("Refinement plan cannot handle phase {}".format(phase.phase_file))

        # loop over detector banks
        # only one detector section
        for j in range(self.detectors[0].bank_number):

            # set diffractometer zero correction
            gsas.gsas_change_difc(j + 1, "Z", self.get("DIFC_Z"), debug=self.debug)

            # set background coefficients
            gsas.gsas_change_background_coeff(j + 1, 1, 12,
                [self.get("BK1"), self.get("BK2"),
                 self.get("BK3"), self.get("BK4"),
                 self.get("BK5"), self.get("BK6"),
                 self.get("BK7"), self.get("BK8"),
                 self.get("BK9"), self.get("BK10"),
                 self.get("BK11"), self.get("BK12")], debug=self.debug)

            # set histogram scale
            gsas.gsas_change_hscale(j + 1, self.get("HSCL"), debug=self.debug)

        # refine to get chi-squared
        gsas.gsas_refine(1, plot=False, debug=self.debug)
        chisq = gsas.gsas_get_chisq("TRIAL", debug=self.debug)

        # print statement
        print(chisq)

        return chisq
