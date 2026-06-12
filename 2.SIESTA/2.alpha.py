import os, glob
import numpy as np
import shutil
from omegaconf import DictConfig, OmegaConf


if __name__ == '__main__':

    # executable files
    exec_atm = os.path.abspath('./input/atm')
    exec_gion = os.path.abspath('./input/gion.py')
    exec_gatm = os.path.abspath('./input/gatm.py')

    # All-electron Vs potential
    input_config = OmegaConf.load('input.yaml')
    DB = input_config['VS_DB']
    name = input_config['Species']['DB']
    ion_name = input_config['Species']['ION']

    # input files
    input_siesta = os.path.abspath(f'./origin')
    input_pot = os.path.abspath(f'{DB}/{name}/1.ATOM/output')
    input_run = os.path.abspath('./origin/input/RUN.fdf')
    input_run_charged_plus = os.path.abspath('./origin/input/RUN-charged+.fdf')
    input_run_charged_minus = os.path.abspath('./origin/input/RUN-charged-.fdf')


    # dft reference results
    input_ion = os.path.abspath(glob.glob(f'./1.dft/neutral/OUT/{ion_name}.ion')[0])
    input_dft = os.path.abspath(glob.glob(f'./1.dft/neutral/OUT/*.RHO')[0])
    input_dft_plus = os.path.abspath(glob.glob(f'./1.dft/charged_plus/OUT/*.RHO')[0])
    input_dft_minus = os.path.abspath(glob.glob(f'./1.dft/charged_minus/OUT/*.RHO')[0])

    # ion lists
    occs = os.listdir(input_pot)
    os.makedirs('2.alpha/neutral', exist_ok = True)
    os.makedirs('2.alpha/charged', exist_ok = True)

    # neutral all-electron potential
    input_fae = os.path.abspath(f'{DB}/{name}/1.ATOM/input/FEPOT') # optional

    for occ in occs:

        # alpha all-electron potential
        input_hae = os.path.abspath(f'{DB}/{name}/1.ATOM/output/{occ}/HEPOT')

        # neutral
        os.system(f'cp -r {input_siesta} 2.alpha/neutral/{occ}')
        os.system(f'cp -r {input_dft} 2.alpha/neutral/{occ}/input/DFT.RHO')
        os.system(f'cp -r {input_run}  2.alpha/neutral/{occ}/input/RUN.fdf')
        os.system(f'python {exec_gion} --fae {input_fae} --hae {input_hae} --ion {input_ion} --rout -1.0 --out 2.alpha/neutral/{occ}/input/{ion_name}.ion')

        # charged
        os.system(f'cp -r {input_siesta} 2.alpha/charged/{occ}')
        os.system(f'python {exec_gion} --fae {input_fae} --hae {input_hae} --ion {input_ion} --rout -1.0 --out 2.alpha/charged/{occ}/input/{ion_name}.ion')

        occ_value = float(occ.split('=')[-1])
        if occ_value > 0.0:
            os.system(f'cp -r {input_run_charged_minus}  2.alpha/charged/{occ}/input/RUN.fdf')
            os.system(f'cp -r {input_dft_minus} 2.alpha/charged/{occ}/input/DFT.RHO')

        else:
            os.system(f'cp -r {input_run_charged_plus}  2.alpha/charged/{occ}/input/RUN.fdf')
            os.system(f'cp -r {input_dft_plus} 2.alpha/charged/{occ}/input/DFT.RHO')

