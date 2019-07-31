# Alumina

This is a quick start example on analyzing an alumina (AlO2) dataset.

## Spotlight instructions

There is an example using Spotlight.
To run do:
```
bash run_spotlight.sh
```

Alternatively, on a Slurm cluster, to run do:
```
sbatch -N 1 -t 600 run_spotlight.sh 
```

You can inspect results as they run, to run do:
```
spotlight_inspect --input-file tmp_spotlight/alumina_solution.pkl
```

Once the example has completed, then you can view the results:
```
display tmp_spotlight/tmp_minima/alumina.pdf
```

## gsaslanguage instructions

There is also an example using gsaslanguage.
To run do:
```
bash run_gsaslanguage.sh
```
