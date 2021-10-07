# fair2.1-calibrate
Re-calibration of FaIR v2.0 to updated Cummins calibration and inclusion of ocean heat content

## installation

### requirements
- `anaconda` for `python3`
- a reasonably modern version of `R` (4.1.1 used here)

### python and jupyter notebooks
```
conda env create -f environment.yml
conda activate fair2.1-calibrate
nbstripout --install
```

### R scripts

Open the R console and set the working directory to the `r_scripts` directory of your local repository.

```
source("setup.r")
source("calibrate_cummins_3layer.r")
```

## reproduction

1. The `010_download-data.ipynb` notebook is run first.
2. Then, `r_scripts/calibrate_cummins_3layer.r` is run.
3. Finally, the remaining notebooks are run in numerical order.