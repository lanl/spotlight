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

        # fit background
        for det in self.detectors:
            gsas.gsas_change_background(1, 1, 12) 
        gsas.gsas_refine(12, plot=False)

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

            # otherwise raise error because refinement plan does not support this phase
            else:
                raise NotImplementedError("Refinement plan cannot handle phase {}".format(phase))

        # refine to get chi-squared
        gsas.gsas_refine(1, plot=False)
        chisq = gsas.gsas_get_chisq("TRIAL")

        ## print statement
        #print(chisq, p)

        return chisq
