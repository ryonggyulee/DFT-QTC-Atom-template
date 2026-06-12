import os
import numpy as np
import shutil
import subprocess

def run_atm(exec_atm, input_inp, output_ion):

    os.makedirs('./tmp', exist_ok = True)
    os.chdir('./tmp')
    shutil.copy(input_inp, '.')
    os.system(f'{exec_atm}')
    shutil.move(f'AEPOT', output_ion)
    os.chdir('..')

    shutil.move('tmp', output_ion + '_tmp')   
#    shutil.rmtree('./tmp')

def check_error(path):

    etot = subprocess.run(f"grep -a 'Total number of iterations needed for electron screening potential ' {path}/HEPOT_tmp/OUT | awk '{{print $NF}}'",
                          shell=True,
                          capture_output=True,
                          text=True)
    number = int(etot.stdout.strip())

    print(number)

    if number > 98:
        return False
    else:
        return True

if __name__ == '__main__':

    # executable files
    exec_atm = os.path.abspath('./input/atm')
    exec_gion = os.path.abspath('./input/gion.py')
    exec_gatm = os.path.abspath('./input/gatm.py')

    # input files
    input_inp = os.path.abspath('./input/INP')
    input_fae = os.path.abspath('./input/FEPOT') # optional

    # calculate FEPOT
    if not os.path.exists(input_fae):
        run_atm(exec_atm, input_inp, input_fae)

    # which orbital to be corrected (rm/add)?
    orb_l = [1, 1]

    # range of occ.
    occs = np.linspace(-1,1, 41)

    for iocc in range(len(occs)):
        occ = occs[iocc]
        print(occ)

        # make dirs
        path = os.path.abspath(f'output/occ={occ:3.2f}')
        os.makedirs(path, exist_ok =True)

        # make inp
        if occ <= 0.0:
            os.system(f'python {exec_gatm} --atm {input_inp} --orb {orb_l[0]} --occ {occ} --out {path}/INP')
        else:
            os.system(f'python {exec_gatm} --atm {input_inp} --orb {orb_l[1]} --occ {occ} --out {path}/INP') 

        # calculate HEPOT
        run_atm(exec_atm, f'{path}/INP', f'{path}/HEPOT')

        print(path)

        if check_error(path):
            pass
        else:
            shutil.rmtree(f'{path}')
