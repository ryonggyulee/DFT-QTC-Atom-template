import os, glob
import numpy as np
import shutil


if __name__ == '__main__':

    # input files
    input_alpha = os.path.abspath('./2.alpha') # alpha results
    input_dft = os.path.abspath(glob.glob(f'./1.dft/neutral/OUT/*.DM')[0]) # dft dm
    input_run = os.path.abspath('./origin/input/RUN-single.fdf') # 
    input_slm = os.path.abspath('./origin/slm_*')

    input_dft_charged = os.path.abspath(glob.glob(f'./1.dft/charged/OUT/*.DM')[0]) # dft dm
    input_run_charged = os.path.abspath('./origin/input/RUN-single-charged.fdf') #


    # occ lists
    occs = os.listdir(input_alpha+'/neutral')
    os.makedirs('3.alpha-dft-dm/neutral', exist_ok = True)
    os.makedirs('3.alpha-dft-dm/charged', exist_ok = True)

    for occ in occs:
        # neutral
        os.makedirs(f'3.alpha-dft-dm/neutral/{occ}', exist_ok = True)
        os.system(f'cp -r {input_alpha}/neutral/{occ}/input 3.alpha-dft-dm/neutral/{occ}/.')
        os.system(f'cp -r {input_slm} 3.alpha-dft-dm/neutral/{occ}/.')
        os.system(f'cp -r {input_dft} 3.alpha-dft-dm/neutral/{occ}/input/.')
        os.system(f'cp -r {input_run} 3.alpha-dft-dm/neutral/{occ}/input/RUN.fdf')

        # charged
        os.makedirs(f'3.alpha-dft-dm/charged/{occ}', exist_ok = True)
        os.system(f'cp -r {input_alpha}/charged/{occ}/input 3.alpha-dft-dm/charged/{occ}/.')
        os.system(f'cp -r {input_slm} 3.alpha-dft-dm/charged/{occ}/.')
        os.system(f'cp -r {input_dft_charged} 3.alpha-dft-dm/charged/{occ}/input/.')
        os.system(f'cp -r {input_run_charged} 3.alpha-dft-dm/charged/{occ}/input/RUN.fdf')

