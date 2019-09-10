#! /bin/bash

set -e

# run refinement
python gsasii_refine.py

# plot
python gsasii_plot.py
