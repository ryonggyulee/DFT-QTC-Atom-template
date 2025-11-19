

## Prerequirement

### (1) Add reference SIESTA `ion` file 

**Path**: `1.ATOM/input/{name}.ion` 

### (2)  Modifiy electron configuration file (neutral) 

**Path**: `1.ATOM/input/INP` 


### (3) Modify ion generation python code 

**Path**: `1.ATOM/run.py` 

Specifiy the name of `ion` file and orbital channels to be corrected. 

```
name = 'In.ion' # Name of the reference ion file
orb_l = [1, 1]  # orbital channel of electron to be remove or add (l = 0, 1, 2, 3)

```

### (4) Update SIESTA input files 

**Structure file**: `2.SIESTA/origin/input/STRUCT.fdf` 
**Slurm file**: `2.SIESTA/origin/slm_siesta_run` 


## How to Use the code

### (1) Generate corrected ion files for serveral `occ` values 

- `1.ATOM/` 

```
python run.py

```

### (2) Perform DFT-QTC calculation for atoms 

- `2.SIESTA/` 

**DFT calculation**: 

```
python 1.dft.py
python qsub.py 1.dft

```

**DFT-QTC calculation (SCF)**: 

```
python 2.alpha.py
python qsub.py 2.alpha
```

** NSCF calculations**: 

```
python 3.alpha-dft-dm.py  4.dft-alpha-dm.py  5.get_eig.py
python qsub.py 3.alpha-dft-dm

python 4.dft-alpha-dm.py
python qsub.py 4.dft-alpha-dm

```

### (3) Find the optimal `occ` value satisfying **Koopman condition**  


- Eigenvalues (HOMO and LUMO)

`python 5.get_eig.py`


- Total energy

`python 1.get_total_energy_dm.py 2.SIESTA`

