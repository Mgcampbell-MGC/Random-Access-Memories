"""Fidelidade por copo — runs tools/fidelidade_uv.py on ONE candle of a multi-candle render.

The print materials of a shot built by campanha.py write an extra AOV, `label_id` (1, 2, 3 ... one value per candle),
next to the director's label_uv / label_ink / label_mask. This wrapper restricts the label mask to the pixels whose
id matches, so each candle is compared with ITS OWN master (and its own planted error), never with a neighbour's.
It can also export the Cycles Diffuse Color pass (albedo) as an 8-bit sRGB PNG, for the flame-lit check of §D.7.3.

    python fid_multi.py --master M.png --aov 0001.exr --asset shot.png [--id 2] [--coat #FFE81A] [--ink #121014]
                        [--json out.json] [--debug out.png] [--film]
    python fid_multi.py --albedo 0001.exr out.png        (export DiffCol as sRGB)
"""
import argparse
import json
import os
import sys

import numpy as np
import OpenEXR

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import fidelidade_uv as F  # noqa: E402

_orig_load = F.load_aov
ID = None


def _channel(path, name):
    ch = OpenEXR.File(path).parts[0].channels
    for k, v in ch.items():
        if k == name or k.startswith(name + '.') or k.split('.')[0] == name:
            return v.pixels
    raise KeyError(name)


def _load(path):
    uv, ink, mask = _orig_load(path)
    if ID is not None:
        lid = _channel(path, 'label_id')
        lid = lid[..., 0] if lid.ndim == 3 else lid
        idv = lid / np.clip(mask, 1e-6, None)
        mask = mask * (np.abs(idv - ID) < 0.25)
    return uv, ink, mask


F.load_aov = _load


def albedo(exr, out):
    import cv2
    d = _channel(exr, 'DiffCol').astype(np.float64)
    if d.ndim == 3 and d.shape[2] >= 3:
        d = d[..., :3]
    d = np.clip(d, 0, 1)
    s = np.where(d <= 0.0031308, 12.92 * d, 1.055 * np.power(d, 1 / 2.4) - 0.055)
    cv2.imwrite(out, (s[..., ::-1] * 255 + 0.5).astype(np.uint8))
    return out


def main():
    global ID
    if '--albedo' in sys.argv:
        i = sys.argv.index('--albedo')
        print(albedo(sys.argv[i + 1], sys.argv[i + 2]))
        return
    ap = argparse.ArgumentParser()
    ap.add_argument('--master', required=True)
    ap.add_argument('--aov', required=True)
    ap.add_argument('--asset', required=True)
    ap.add_argument('--id', type=float, default=None)
    ap.add_argument('--coat', default=None)
    ap.add_argument('--ink', default='#121014')
    ap.add_argument('--film', action='store_true')
    ap.add_argument('--json')
    ap.add_argument('--debug')
    a = ap.parse_args()
    ID = a.id
    r = F.check(a.master, a.aov, a.asset, a.coat, a.ink, a.film, a.debug)
    r['pass'] = r.pop('pass_')
    r['label_id'] = a.id
    txt = json.dumps([r], indent=2, ensure_ascii=False)
    print(txt)
    if a.json:
        open(a.json, 'w').write(txt)


if __name__ == '__main__':
    main()
