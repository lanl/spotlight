#! /usr/bin/env python
""" The setup file for the spotlight project.
"""

import os
import subprocess
from distutils import core
try:
    from setuptools.command import install as _install
except:
    from distutils.command import install as _install

def find_package_data(dirname):
    """ Returns a list of all relative file paths under ``dirname`` for files
    that do not end in ``.py`` or ``.pyc``.

    Parameters
    ----------
    dirname : str
        Path of directory to check.

    Returns
    -------
    list
        A ``list`` of relative file paths.
    """
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith((".py", ".pyc")):
                items.append(path)
        return items
    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]

# call run function from setup
def do_setup(*args):
    return True
_install.install._called_from_setup = do_setup

# meta-data about the package
project_name = "spotlight"
#project_version = "0.dev1"
project_url = "https://gitlab.lanl.gov/cmbiwer/mystic-gsas"
project_description = "A package for Rietveld refinement."
project_keywords = ["crystallography"]

# a list of required packages to run project
install_requires = [
]

# a list of all executables to be installed
scripts_list = [
    "bin/gsas/gsas_change_absorption",
    "bin/gsas/gsas_change_background_coeff",
    "bin/gsas/gsas_change_difc",
    "bin/gsas/gsas_change_hscale",
    "bin/gsas/gsas_change_phase_fraction",
    "bin/gsas/gsas_change_microstrain",
    "bin/gsas/gsas_change_sample_orientation",
    "bin/gsas/gsas_change_sigma1",
    "bin/gsas/gsas_change_spherical_harmonic_order",
    "bin/gsas/gsas_change_spherical_harmonic_coeff",
    "bin/gsas/gsas_write_csv",
    "bin/spotlight_inspect",
    "bin/spotlight_minimize",
    "bin/spotlight_plot_chisq",
    "bin/spotlight_plot_minima",
    "bin/spotlight_plot_profile",
]

# a list of all python packages to be installed
packages_list = [
    "spotlight",
]

# a dict of all data to be installed
data_dict = {
    "spotlight" : find_package_data("spotlight"),
}

# a dict for commands
cmd_dict = {
}

# test suite
test_suite = None

# run setup
core.setup(name=project_name,
           description=project_description,
           url=project_url,
           keywords=project_keywords,
           install_requires=install_requires,
           scripts=scripts_list,
           packages=packages_list,
           package_data=data_dict,
           test_suite=test_suite,
           cmdclass=cmd_dict,
           zip_safe=False)
