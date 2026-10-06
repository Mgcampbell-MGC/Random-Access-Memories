"""HOLOFOTE · film timing shared by the Blender side (f15_3d.py) and the compositor (compor.py). Pure Python.

flicker(i)     the flame flicker, loop index 0–23 -> (flame_scale, flame_seed): ±6 % from a sum of 2, 3 and 4 Hz sines,
               periodic in 24 frames at 24 fps (§D.6), and a seed on a closed path, so a 24-frame loop is seamless.
flame_state(f) F15 blackout f210–221: the wick catches f210–215 (scale 0,10 -> 1,0), then the loop (index (f-216) % 24).
"""
import math

IGNICAO = {210: 0.10, 211: 0.28, 212: 0.52, 213: 0.78, 214: 1.04, 215: 1.00}


def flicker(i):
    tau = 2 * math.pi * (i % 24) / 24.0
    n = 0.55 * math.sin(2 * tau + 0.3) + 0.35 * math.sin(3 * tau + 1.7) + 0.25 * math.sin(4 * tau + 4.1)
    nmax = 1.0073            # max |n| over the 24 samples: the excursion is exactly ±6 %
    seed = 0.45 * math.sin(tau) + 0.20 * math.sin(2 * tau + 1.0)
    return 1.0 + 0.06 * n / nmax, seed


def flame_state(f):
    s, seed = flicker((f - 216) % 24)
    if f in IGNICAO:
        s = IGNICAO[f] * (s if f == 215 else 1.0)
    return s, seed
