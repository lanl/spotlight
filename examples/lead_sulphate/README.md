# Spotlight + GSAS2 example: PbSO4

This example shows Spotlight + [GSAS2][gsas2] applied to PbSO4

# Example using conda

First, you will need [conda][conda] installed on your machine.

Use either the local `environment.yaml` or the `../../environment_gsas2.yaml` files to create a [conda][conda] environment:
```
conda env create -n spotlight-gsas2-pbso4 -f environment.yml
```

Activate the environment:
```
conda activate spotlight-gsas2-pbso4
```

Install GSAS2 using revsion 5609 (tested version):
```
svn export -r 5609 https://subversion.xray.aps.anl.gov/pyGSAS/install/bootstrap.py
python ./bootstrap.py noproxy
```
_DISCLAIMER: This will install all the GSAS2 files in the current directory_

Run the example:
```
bash ./run_spotlight.sh
```

# Example using docker (on linux)

First, you will need [Docker][docker] installed on your machine.

Build the container image:
```
docker build -t spotlight-gsas2-pbso4 .
```

Then, you can run the example while mounting the output directory to your host machine:
```
docker run -v ./output:/app/tmp_spotlight_123 spotlight-gsas2-pbso4
```

_DISCLAIMER: you may need to delete the `output/` directory using `sudo`_
_i.e. `sudo rm -rf output/`_
_This is due to `root` writing these files inside the container._

[gsas2]: https://subversion.xray.aps.anl.gov/trac/pyGSAS
[conda]: https://docs.conda.io/en/latest/
[docker]: https://docs.docker.com/
