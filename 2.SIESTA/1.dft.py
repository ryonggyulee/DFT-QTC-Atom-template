import os, glob
import numpy as np
import shutil


if __name__ == '__main__':

    # input files
    input_siesta = os.path.abspath(f'./origin')
    input_ion = os.path.abspath(glob.glob(f'./origin/input/*.ion')[0])

    input_run = os.path.abspath('./origin/input/RUN-dft.fdf')
    input_run_charged_plus = os.path.abspath('./origin/input/RUN-dft-charged+.fdf') 
    input_run_charged_minus = os.path.abspath('./origin/input/RUN-dft-charged-.fdf')

    # make dirs
    os.makedirs('1.dft', exist_ok = True)

    # neutral
    os.system(f'cp -r {input_siesta} 1.dft/neutral')
    os.system(f'cp -r {input_ion} 1.dft/neutral/input/.')
    os.system(f'cp -r {input_run} 1.dft/neutral/input/RUN.fdf')

    # charged (+)
    os.system(f'cp -r {input_siesta} 1.dft/charged_plus')
    os.system(f'cp -r {input_ion} 1.dft/charged_plus/input/.')
    os.system(f'cp -r {input_run_charged_plus} 1.dft/charged_plus/input/RUN.fdf')

    # charged (-)
    os.system(f'cp -r {input_siesta} 1.dft/charged_minus')
    os.system(f'cp -r {input_ion} 1.dft/charged_minus/input/.')
    os.system(f'cp -r {input_run_charged_minus} 1.dft/charged_minus/input/RUN.fdf')
