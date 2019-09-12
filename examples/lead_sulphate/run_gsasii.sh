#! /bin/bash

set -e

# run refinement
python gsasii_refine.py

# make CSV file and plot results for each histogram
# create a PDF containing all images
# requires convert which is not an explicit dependency of Spotlight
# so check if it is installed first
cd tmp_gsasii
for IDX in 1; do
gsasii_write_csv \
    --input-file final.gpx \
    --output-file hist_${IDX}.txt \
    --histogram ${IDX}
spotlight_plot_profile \
    --input-file hist_${IDX}.txt \
    --profile-file profile_${IDX}.png \
    --residual-file residual_${IDX}.png \
    --reflections-file reflections_${IDX}.png \
    --phase-labels PBSO4
if [ -x "$(command -v convert)" ]; then
convert -coalesce profile_${IDX}.png reflections_${IDX}.png residual_${IDX}.png alumina_${IDX}.pdf
fi
done
