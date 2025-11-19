import os, glob
import numpy as np
import shutil


if __name__ == '__main__':

    # input files
    input_alpha = os.path.abspath('./2.alpha') # alpha results
    input_dft = os.path.abspath(glob.glob(f'./1.dft/neutral/OUT/*.ion')[0]) # dft ion
    input_run = os.path.abspath('./origin/input/RUN-single.fdf') # 
    input_slm = os.path.abspath('./origin/slm_*')

    input_run_charged = os.path.abspath('./origin/input/RUN-single-charged.fdf') 

    # occ lists
    occs = os.listdir(input_alpha+'/neutral')
    os.makedirs('4.dft-alpha-dm/neutral', exist_ok = True)
    os.makedirs('4.dft-alpha-dm/charged', exist_ok = True)

    for occ in occs:
        # make dirs
        os.makedirs(f'4.dft-alpha-dm/neutral/{occ}', exist_ok = True)
        os.system(f'cp -r {input_alpha}/neutral/{occ}/input 4.dft-alpha-dm/neutral/{occ}/.') # input
        os.system(f'cp -r {input_alpha}/neutral/{occ}/OUT/*.DM 4.dft-alpha-dm/neutral/{occ}/input/.') # alpha dm
        os.system(f'cp -r {input_slm} 4.dft-alpha-dm/neutral/{occ}/.') # slurm
        os.system(f'cp -r {input_dft} 4.dft-alpha-dm/neutral/{occ}/input/.')
        os.system(f'cp -r {input_run} 4.dft-alpha-dm/neutral/{occ}/input/RUN.fdf')

        # charged
        os.makedirs(f'4.dft-alpha-dm/charged/{occ}', exist_ok = True)
        os.system(f'cp -r {input_alpha}/charged/{occ}/input 4.dft-alpha-dm/charged/{occ}/.') # input
        os.system(f'cp -r {input_alpha}/charged/{occ}/OUT/*.DM 4.dft-alpha-dm/charged/{occ}/input/.') # alpha dm
        os.system(f'cp -r {input_slm} 4.dft-alpha-dm/charged/{occ}/.') # slurm
        os.system(f'cp -r {input_dft} 4.dft-alpha-dm/charged/{occ}/input/.')
        os.system(f'cp -r {input_run_charged} 4.dft-alpha-dm/charged/{occ}/input/RUN.fdf')



