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

def get_es(path):

    etot = subprocess.run(f"grep '(RHO_QTC - RHO_base)  =' {path}/OUT/stdout.txt | tail -n 1 | awk '{{print $NF}}'",
                          shell=True,
                          capture_output=True,
                          text=True)
    print(etot.stdout.strip())
    return float(etot.stdout.strip())


if __name__ == '__main__':


    # input files
    input_dft = os.path.abspath(f'1.dft/neutral') # dft results
    input_dft_charged_plus = os.path.abspath(f'1.dft/charged_plus') # dft results
    input_dft_charged_minus = os.path.abspath(f'1.dft/charged_minus') # dft results

    # qtc results
    input_scf_alpha = os.path.abspath(f'./2.alpha/neutral') # alpha results
    input_scf_alpha_charged = os.path.abspath(f'./2.alpha/charged') # alpha results

    # occ lists
    occs  = sorted(os.listdir(input_scf_alpha))

    # total energy lists
    with open('total.txt', 'w') as f:
        data = {}
        for occ in occs:
            print(occ)
            # neutral
            etot0 = get_total_energy(input_dft)
            etot1 = get_total_energy(os.path.join(input_scf_alpha,occ))
            etot2 = get_es(os.path.join(input_scf_alpha,occ))
            etot_neutral = 2*etot1 + etot2 - etot0

            print(occ)

            # charged
            occ_value = float(occ.split('=')[-1])
            if occ_value > 0.0:
                etot0 = get_total_energy(input_dft_charged_minus)
            else:
                etot0 = get_total_energy(input_dft_charged_plus)

            etot1 = get_total_energy(os.path.join(input_scf_alpha_charged,occ))
            etot2 = get_es(os.path.join(input_scf_alpha_charged,occ))
            etot_charged = 2*etot1 + etot2 - etot0

            occ_val = float(occ.split('=')[-1])
            data[occ_val] = [etot_neutral, etot_charged]

        data = dict(sorted(data.items()))
        for key, value in data.items():
            f.write(f'{key} \t {value[0]:5.4f} \t {value[1]:5.4f}\n')


