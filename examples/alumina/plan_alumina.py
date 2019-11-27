""" A refinement plan for alumina.
"""

import os
from spotlight import gsas
from spotlight import plan

class Plan(plan.BasePlan):
    name = "alumina_plan"

    def initialize(self):

        # initialize
        gsas.gsas_initialize(self.name, "Alumina Example")

        # add phases
        phase_files = [p.phase_file for p in self.phases]
        phase_numbers = [p.phase_number for p in self.phases]
        for phase_file, phase_number in zip(phase_files, phase_numbers):
            gsas.gsas_read_phase(os.path.basename(phase_file), phase_number)

        # add histograms
        for det in self.detectors:
            for bank_num in range(det.bank_number):
                gsas.gsas_add_histogram(os.path.basename(det.data_file),
                                        os.path.basename(det.detector_file),
                                        bank_num + 1,
                                        det.min_d_spacing)
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
            if os.path.basename(phase.phase_file) == "alumina.exp":

                # set lattice parameters
                gsas.gsas_change_lattice(i + 1, [self.get("A_ALUMINA"),
                                                 self.get("C_ALUMINA")])

                # set atom positions
                gsas.gsas_change_atom(i + 1, 1, "Z", self.get("Z_AL_ALUMINA"))
                gsas.gsas_change_atom(i + 1, 2, "X", self.get("X_O_ALUMINA"))

                # set isotropic thermal
                gsas.gsas_change_atom(i + 1, 1, "UISO", self.get("UISO_AL_ALUMINA"))
                gsas.gsas_change_atom(i + 1, 2, "UISO", self.get("UISO_O_ALUMINA"))

                # loop over detector banks
                # only one detector section
                for j in range(self.detectors[0].bank_number):

                    ## set phase scales
                    #gsas.gsas_change_phase_fraction(
                    #                    j + 1, i + 1,
                    #                    self.get("PHFR_ALUMINA"))

                    # set profile parameters
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 1,
                                                       self.get("GU_ALUMINA"))
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 2,
                                                       self.get("GV_ALUMINA"))
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 3,
                                                       self.get("GW_ALUMINA"))

                    # set profile cutoff
                    gsas.gsas_change_profile_cutoff(j + 1, i + 1, self.get("CUTOFF"))

            # otherwise raise error because refinement plan does not support this phase
            else:
                raise NotImplementedError("Refinement plan cannot handle phase {}".format(phase))

        # loop over detector banks
        # only one detector section
        for j in range(self.detectors[0].bank_number):

            # set diffractometer zero correction
            gsas.gsas_change_difc(j + 1, "Z", self.get("DIFC_Z"))

            # set background coefficients
            gsas.gsas_change_background_coeff(j + 1, 1, 12,
                [self.get("BK1"), self.get("BK2"),
                 self.get("BK3"), self.get("BK4"),
                 self.get("BK5"), self.get("BK6"),
                 self.get("BK7"), self.get("BK8"),
                 self.get("BK9"), self.get("BK10"),
                 self.get("BK11"), self.get("BK12")])

            # set histogram scale
            gsas.gsas_change_hscale(j + 1, self.get("HSCL"))

        # refine to get chi-squared
        gsas.gsas_refine(1, plot=False)
        chisq = gsas.gsas_get_chisq("TRIAL")

        ## print statement
        #print(chisq, p)

        return chisq
