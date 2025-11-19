import os, glob
import numpy as np
import shutil


if __name__ == '__main__':

    # input files
    input_siesta = os.path.abspath(f'./origin')
    input_ion = os.path.abspath(glob.glob(f'../1.ATOM/input/*.ion')[0])

    input_run = os.path.abspath('./origin/input/RUN.fdf')
    input_run_charged = os.path.abspath('./origin/input/RUN-charged.fdf') 


    # make dirs
    os.makedirs('1.dft', exist_ok = True)

    # neutral
    os.system(f'cp -r {input_siesta} 1.dft/neutral')
    os.system(f'cp -r {input_ion} 1.dft/neutral/input/.')

    # charged
    os.system(f'cp -r {input_siesta} 1.dft/charged')
    os.system(f'cp -r {input_ion} 1.dft/charged/input/.')
    os.system(f'cp -r {input_run_charged} 1.dft/charged/input/RUN.fdf')


