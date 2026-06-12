import os,glob,sys

path = sys.argv[1]
files = sorted(glob.glob(f'{path}/*'))


for i in files:

    os.chdir(i)
    files2 = glob.glob('*')

    if 'input' in files2:
        if os.path.isdir('OUT'):
            pass
        else:
            os.system('qsub slm_*')
        os.chdir('../..')

    else:
        for j in files2:
            os.chdir(j)

            if os.path.isdir('OUT'):
                pass
            else:
                os.system('qsub slm_*')
            os.chdir('..')

        os.chdir('../..')


