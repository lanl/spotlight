""" A refinement plan for Alumina.
"""

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
            gsas.gsas_read_phase(phase_file, phase_number)
            print("READ PHASE")

        # add histograms
        for bank_num in range(self.detector.bank_number):
            gsas.gsas_add_histogram(self.data_file,
                                    self.detector.detector_file,
                                    bank_num + 1,
                                    self.detector.min_d_spacing,
                                    self.detector.max_d_spacing)

    def function(self, p):
        """ Function to be optimized.
        """

        # copy experimental file
        gsas.gsas_copy_expfile(self.name, "TRIAL", "Test Parameters")

        # loop over phases
        for i, phase in enumerate(self.phases):

            # handle alumina phase
            if phase.phase_file == "alumina.exp":

                # set lattice parameters
                gsas.gsas_change_lattice(i + 1, [self.get_value(p, "A_ALUMINA"),
                                                 self.get_value(p, "C_ALUMINA")])

                # set atom positions
                gsas.gsas_change_atom(i + 1, 1, "X", self.get_value(p, "X_ALUMINA"))
                gsas.gsas_change_atom(i + 1, 2, "Z", self.get_value(p, "Z_ALUMINA"))

                # set isotropic thermal
                gsas.gsas_change_atom(i + 1, 1, "UISO", self.get_value(p, "UISO1_ALUMINA"))
                gsas.gsas_change_atom(i + 1, 2, "UISO", self.get_value(p, "UISO2_ALUMINA"))

                # loop over detector banks
                for j in range(self.detector.bank_number):

                    # set phase scales
                    gsas.gsas_change_phase_fraction(
                                        j + 1, i + 1,
                                        self.get_value(p, "PHFR_ALUMINA"))

                    # set profile parameters
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 1,
                                                       self.get_value(p, "PF1_ALUMINA"))
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 2,
                                                       self.get_value(p, "PF2_ALUMINA"))
                    gsas.gsas_change_profile_parameter(j + 1, i + 1, 3,
                                                       self.get_value(p, "PF3_ALUMINA"))

        # loop over detector banks
        for j in range(self.detector.bank_number):

            # set background coefficients
            gsas.gsas_change_background_coeff(j + 1, 1, 6,
                [self.get_value(p, "BK1"), self.get_value(p, "BK2"),
                 self.get_value(p, "BK3"), self.get_value(p, "BK4"),
                 self.get_value(p, "BK5"), self.get_value(p, "BK6")])

            # set histogram scale
            gsas.gsas_change_hscale(j + 1, self.get_value(p, "HSCL"))

        # refine to get chi-squared
        gsas.gsas_refine(2, plot=False)
        chisq = gsas.gsas_get_chisq("TRIAL")

        print(chisq, p)

        return chisq
