import os, glob
import numpy as np
import shutil


if __name__ == '__main__':

    # input files
    input_siesta = os.path.abspath(f'./origin')
    input_ion = os.path.abspath('../1.ATOM/output')
    input_run = os.path.abspath('./origin/input/RUN.fdf')
    input_run_charged = os.path.abspath('./origin/input/RUN-charged.fdf')

    # ion lists
    occs = os.listdir(input_ion)
    os.makedirs('2.alpha/neutral', exist_ok = True)
    os.makedirs('2.alpha/charged', exist_ok = True)

    for occ in occs:

        # neutral
        os.system(f'cp -r {input_siesta} 2.alpha/neutral/{occ}')
        os.system(f'cp -r {input_ion}/{occ}/*.ion  2.alpha/neutral/{occ}/input/.')

        # charged
        os.system(f'cp -r {input_siesta} 2.alpha/charged/{occ}')
        os.system(f'cp -r {input_ion}/{occ}/*.ion  2.alpha/charged/{occ}/input/.')
        os.system(f'cp -r {input_run_charged}  2.alpha/charged/{occ}/input/RUN.fdf')
