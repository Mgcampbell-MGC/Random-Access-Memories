"""Regenerate every printed surface of HOLOFOTE (02_PRODUTO, except renders/) with one command, in order, one
process at a time (the machine's 4 cores are shared).

    /home/user/venvs/web/bin/python _build/pack/tudo.py [--sem-rotulos]

rotulos.py (the seven approved wrap masters) is deterministic: re-running it reproduces the same bytes. Pass
--sem-rotulos to leave them untouched.
"""
import os
import sys
import time
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
STEPS = ['rotulos.py', 'single.py', 'tampa.py', 'base.py', 'case.py', 'cartucho.py', 'refil.py', 'setlist.py',
         'pulseira.py', 'facas.py', 'leia_me.py']


def main():
    skip = '--sem-rotulos' in sys.argv
    for s in STEPS:
        if skip and s == 'rotulos.py':
            continue
        t = time.time()
        print(f'--> {s}', flush=True)
        r = subprocess.run([PY, os.path.join(HERE, s)], cwd=HERE)
        if r.returncode:
            sys.exit(f'{s} failed ({r.returncode})')
        print(f'    {s} ok in {time.time() - t:.0f} s', flush=True)


if __name__ == '__main__':
    main()
