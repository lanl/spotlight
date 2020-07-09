""" This module contains function for making external calls to GSAS.
"""

import numpy
import os
import subprocess

def _external_call(cmd, debug=False, system=False):
    """ This function makes external calls.
    """
    cmd = map(str, cmd)
    if debug:
        print(" ".join(cmd))
    if system and debug:
        os.system(" ".join(cmd))
    elif system:
        os.system(" ".join(cmd) + [">", "/dev/null", "2>&1"]))
    else:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        while True:
            output = p.stdout.readline().decode("utf-8")
            if output == "" and p.poll() == 0:
                break
            if output and debug:
                print(output.strip())

def gsas_add_histogram(obs_file, instrument_file, bank_number,
                       min_d_spacing, max_d_spacing=None, debug=False):
    """ This function adds a histogram.
    """
    cmd = ["gsas_add_histogram", obs_file, instrument_file, bank_number,
           min_d_spacing]
    if max_d_spacing is not None:
        cmd += [max_d_spacing]
    _external_call(cmd, debug)

def gsas_change_absorption(bank_number, function_number, val, debug=False):
    """ Change the absorption parameter.
    """
    cmd = ["gsas_change_absorption", bank_number, function_number, val]
    _external_call(cmd, debug)

def gsas_change_atom(phase_number, atoms, var, val, debug=False):
    """ Change a parameter of an atom.
    """
    cmd = ["gsas_change_atom", phase_number, atoms, var, val]
    _external_call(cmd, debug)

def gsas_change_background(bank_number, bkg_func, num_coeff,
                           debug=False):
    """ Change background function.
    """
    cmd = ["gsas_change_background", bank_number, bkg_func, num_coeff]
    _external_call(cmd, debug)

def gsas_change_background_coeff(bank_number, function_number, num_coeffs,
                                 vals, debug=False):
    """ Change the background coefficients.
    """
    cmd = ["gsas_change_background_coeff",
           bank_number, function_number, num_coeffs]
    cmd += vals
    _external_call(cmd, debug)

def gsas_change_difc(bank_number, dcode, val, debug=False):
    """ Change the diffractometer constant for a histogram.
    """
    cmd = ["gsas_change_DIFC", bank_number, dcode, val]
    _external_call(cmd, debug)

def gsas_change_hscale(bank_number, val, debug=False):
    """ Change the histogram scale parameter.
    """
    cmd = ["gsas_change_hscale", bank_number, val]
    _external_call(cmd, debug)

def gsas_change_lattice(phase_number, value, debug=False):
    """ This function changes the lattice parameters for a phase.
    """
    cmd = ["gsas_change_lattice"]
    if isinstance(value, list) or isinstance(value, numpy.ndarray):
        cmd += [phase_number] + value
    else:
        cmd += [phase_number, value]
    _external_call(cmd, debug)

def gsas_change_max_tof(bank_number, val, debug=False):
    """ This function changes the max time-of-flight for a histogram in 2-theta.
    """
    cmd = ["gsas_change_max_tof", bank_number, val]
    _external_call(cmd, debug)

def gsas_change_microstrain(phase_number, val, debug=False):
    """ This function changes the microstrain for a phase.
    """
    cmd = ["gsas_change_microstrain", phase_number, val]
    _external_call(cmd, debug)

def gsas_change_phase_fraction(bank_number, phase_number, val, debug=False):
    """ This function changes the phase scale for a phase.
    """
    cmd = ["gsas_change_phase_fraction", bank_number, phase_number, val]
    _external_call(cmd, debug)

def gsas_change_profile(bank_number, phase_number, val, debug=False):
    """ This function changes the profile function for a phase.
    """
    cmd = ["gsas_change_profile", bank_number, phase_number, val]
    _external_call(cmd, debug)

def gsas_change_profile_cutoff(bank_number, phase_number, val, debug=False):
    """ This function changes the profile cutoff for a phase.
    """
    cmd = ["gsas_change_profile_cutoff", bank_number, phase_number, val]
    _external_call(cmd, debug)

def gsas_change_profile_parameter(bank_number, phase_number, param_number,
                                  val, debug=False):
    """ This function changes the profile parameter for a phase.
    """
    cmd = ["gsas_change_profile_parameter", bank_number, phase_number,
           param_number, val]
    _external_call(cmd, debug)

def gsas_change_sample_orientation(phase_number, omg, chi, phi, debug=False):
    """ This function changes the sample orientation.
    """
    cmd = ["gsas_change_sample_orientation", phase_number, omg, chi, phi]
    _external_call(cmd, debug)

def gsas_change_sigma1(bank_number, phase_number, val, debug=False):
    """ Change the peak width parameter.
    """
    cmd = ["gsas_change_sigma1", bank_number, phase_number, val]
    _external_call(cmd, debug)

def gsas_change_spherical_harmonic_coeff(phase_number, l, m, n,
                                        val, debug=False):
    """ Change the spherical harmonic coefficient.
    """
    cmd = ["gsas_change_spherical_harmonic_coeff", phase_number, l, m, n, val]
    _external_call(cmd, debug)

def gsas_change_spherical_harmonic_order(phase_number, val, debug=False):
    """ Change the spherical haromonic order.
    """
    cmd = ["gsas_change_spherical_harmonic_order", phase_number, val]
    _external_call(cmd, debug)

def gsas_constrain_atom(*args, **kwargs):
    """ Constrains atom parameters.
    """
    debug = kwargs["debug"] if "debug" in kwargs.keys() else False
    cmd = ["gsas_constrain_atom"]
    cmd += ["multi"] if len(args) > 1 else []
    cmd += args
    _external_call(cmd, debug)

def gsas_constrain_phase(phase_number, debug=False):
    """ This function sets phase scale same in all histograms.
    """
    cmd = ["gsas_constrain_phase", phase_number]
    _external_call(cmd, debug)

def gsas_copy_expfile(target, name, label, debug=False):
    """ Copies an ``EXP`` file.
    """
    cmd = ["gsas_copy_expfile", target, name, label]
    _external_call(cmd, debug)

def gsas_done(debug=False):
    """ Creates ``PDF`` file from refinement.
    """
    cmd = ["gsas_done"]
    _external_call(cmd, debug)

def gsas_exclude_region(bank_number, start, end, debug=False):
    """ Excludes a region of histogram.
    """
    cmd = ["gsas_exclude_region", bank_number, start, end]
    _external_call(cmd, debug)

def gsas_get_chisq(name, debug=False):
    """ Finds the chi-squared value after refining.
    """
    cmd = ["grep", "'Reduced'", name + ".LST",
           "| tail -n 1 | awk -v x=4 '{print $x}'"]
    cmd = " ".join(map(str, cmd))
    if debug:
        print(cmd)
    chisq = subprocess.check_output(cmd, shell=True)
    return float(chisq)

def gsas_initialize(name, label, debug=False):
    """ This function initializes a ``EXP`` file.
    """
    cmd = ["gsas_initialize", name, label]
    _external_call(cmd, debug)

def gsas_read_phase(phase_file, phase_number, debug=False):
    """ This function adds a new phase to the diffraction pattern.
    """
    cmd = ["gsas_read_phase", phase_file, phase_number]
    _external_call(cmd, debug)

def gsas_refine(n=0, plot=True, debug=False):
    """ This function refines the data.
    """
    no_plot = "" if plot else "noplot"
    cmd = ["gsas_refine", n, no_plot]
    _external_call(cmd, debug)

def gsas_vary_absorption(phase_number, absorption_function,
                         refinement_flag, damping_flag="", debug=False):
    """ This function varies the absorption coefficients.
    """
    cmd = ["gsas_vary_absorption", phase_number,
           absorption_function, damping_flag]
    _external_call(cmd, debug)

def gsas_vary_atom(phase_number, atoms, refinement_flag,
                   damping_flag="", debug=False):
    """ This function varies atom parameters.
    """
    cmd = ["gsas_vary_atom", phase_number, atoms,
           refinement_flag, damping_flag]
    _external_call(cmd, debug)

def gsas_vary_difc(bank_number, value, debug=False):
    """ This function varies the diffractometer constants.
    """
    cmd = ["gsas_vary_DIFC", bank_number, value]
    _external_call(cmd, debug)

def gsas_vary_lattice(phase_number, refinement_flag,
                      damping_flag="", debug=False):
    """ This function varies the lattice parameters.
    """
    cmd = ["gsas_vary_lattice", phase_number, refinement_flag, damping_flag]
    _external_call(cmd, debug)

def gsas_vary_phase(phase_number, refinement_flag, damping_flag, debug=False):
    """ This function varies the phase scales.
    """
    cmd = ["gsas_vary_phase", phase_number, refinement_flag, damping_flag]
    _external_call(cmd, debug)

def gsas_vary_sigma1(bank_number, phase_number, refinement_flag, damping_flag, debug=False):
    """ This function varies the peak width.
    """
    cmd = ["gsas_vary_sigma1", bank_number, phase_number, refinement_flag, damping_flag]
    _external_call(cmd, debug)

def gsas_write_csv(hist, gsas_exp, output_file_base, debug=False):
    """ This function generates an ASCII file of a simulated diffraction
    pattern.
    """
    cmd = ["gsas_write_csv", hist, gsas_exp, output_file_base]
    _external_call(cmd, debug)
    return output_file_base + ".TXT"

def gsas_simulate_histogram(hist_file, bank, min_d, max_d, debug=False):
    """ This function simulates a diffraction pattern for a histogram.
    """
    cmd = ["gsas_simulate_histogram", hist_file, bank, min_d, max_d]
    _external_call(cmd, debug)
