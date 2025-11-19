import os, glob, sys
import numpy as np
import shutil
import subprocess

def get_total_energy(path):

    etot = subprocess.run(f"grep 'Total =' {path}/OUT/stdout.txt | awk '{{print $NF}}'", 
                          shell=True,
                          capture_output=True,
                          text=True)
    return float(etot.stdout.strip())


if __name__ == '__main__':

    path = sys.argv[1]

    # input files
    input_scf_alpha = os.path.abspath(f'./{path}/2.alpha/neutral') # alpha results
    input_nscf_alpha = os.path.abspath(f'./{path}/3.alpha-dft-dm/neutral') # alpha results
    input_nscf_dft = os.path.abspath(f'./{path}/4.dft-alpha-dm/neutral') # alpha results

    input_scf_alpha_charged = os.path.abspath(f'./{path}/2.alpha/charged') # alpha results
    input_nscf_alpha_charged = os.path.abspath(f'./{path}/3.alpha-dft-dm/charged') # alpha results
    input_nscf_dft_charged = os.path.abspath(f'./{path}/4.dft-alpha-dm/charged') # alpha results

    # occ lists
    occs  = sorted(os.listdir(input_scf_alpha))

    # total energy lists
    with open('total.txt', 'w') as f:
        data = {}
        for occ in occs:
            print(occ)
            # neutral
            etot1 = get_total_energy(os.path.join(input_scf_alpha,occ))
            etot2 = get_total_energy(os.path.join(input_nscf_alpha,occ))
            etot3 = get_total_energy(os.path.join(input_nscf_dft,occ))
            etot_neutral = etot1 - etot2 + etot3

            print(occ)

            # charged
            etot1 = get_total_energy(os.path.join(input_scf_alpha_charged,occ))
            etot2 = get_total_energy(os.path.join(input_nscf_alpha_charged,occ))
            etot3 = get_total_energy(os.path.join(input_nscf_dft_charged,occ))
            etot_charged = etot1 - etot2 + etot3

            occ_val = float(occ.split('=')[-1])
            data[occ_val] = [etot_neutral, etot_charged]

        data = dict(sorted(data.items()))
        for key, value in data.items():
            f.write(f'{key} \t {value[0]:5.4f} \t {value[1]:5.4f}\n')


