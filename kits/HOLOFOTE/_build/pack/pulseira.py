"""A PULSEIRA (platform §C.6): the woven jacquard band and its paper seal.

    /home/user/venvs/web/bin/python _build/pack/pulseira.py

Band: black woven polyester 15 x 350 mm, jacquard text in amarelo, repeating and NEVER cut mid-word:
  ACESSO TOTAL · ATRAÇÃO · 09.05.27 · HOLOFOTE ·
The woven zone runs from 14 mm (clear of the one-way clasp) to 340 mm (10 mm heat-sealed tail). It holds exactly
two whole repeats between two O FOCO marks (§D.3: O FOCO is the woven band's symbol); the size is solved so the
zone is filled exactly, so nothing is ever truncated. Type: Special Gothic wght 700 wdth 75 caps (a jacquard needs
the sturdy cut; Condensed One's hairline joins would break up at a 0,2 mm thread pitch).
Seal: 60 x 15 mm uncoated papel-cartaz, wrapped round band and tail. Outer face (front): amarelo, "pode rasgar."
(Expanded One lower case, cap 4,0, preto). Inner face (back, revealed when torn): papel, "o que se guarda é a
pulseira." (Shantell 500, x-height 1,8, preto).

Outputs in 02_PRODUTO/pulseira/ at 20 px/mm: PULSEIRA_padrao.png (the two-colour jacquard design, 7000 x 300),
PULSEIRA_padrao.svg, PULSEIRA_tecido.png (woven render: weft floats, warp ground, selvedges), PULSEIRA_tecido_altura16.png,
PULSEIRA_SELO_frente.png / _verso.png (+ .svg), PULSEIRA.json.
"""
import os
import sys
import math

import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, run_cap, run_xh, CAPS

PP = 20
L, Wb = 350.0, 15.0
Z0, Z1 = 14.0, 340.0
REPEATS = 2
TRACK = 60
WEFT, WARP = 0.25, 0.20          # thread pitch (mm): weft across the band, warp along it


def layout(cap):
    f = K.SG(700, 75)
    ln = Line([run_cap(' '.join([T.BAND] * REPEATS), f, cap, TRACK, CAPS)])
    d = cap * 0.52                                      # O FOCO: the whole mark (2,2 d) is 1,15 x the cap height
    fw = 2.4 * d
    gap = Line([run_cap(' · ', f, cap, TRACK, CAPS)]).advance * 0.5
    total = fw + gap + ln.ink_width() + gap + fw
    return ln, d, fw, gap, total


def band():
    lo, hi = 2.0, 8.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if layout(mid)[4] > Z1 - Z0:
            hi = mid
        else:
            lo = mid
    cap = lo
    ln, d, fw, gap, total = layout(cap)
    assert cap <= 6.5, cap
    yb = Wb / 2 + cap / 2
    x = Z0
    paths = []
    foco1, fwid, fh = K.foco_d(x + fw / 2, Wb / 2 - 1.1 * d, d)
    paths.append(foco1)
    x += fw + gap
    p = K.place_left(ln, x, yb)
    paths.append(K.placed_paths(p))
    x = p.ink()[2] + gap
    foco2, _, _ = K.foco_d(x + fw / 2, Wb / 2 - 1.1 * d, d)
    paths.append(foco2)
    end = x + fw
    assert abs(end - Z1) < 0.05, end
    a, _ = K.raster_paths(L, Wb, PP, paths)
    # check: whole repeats only (count each word, every one complete)
    words = ' '.join([T.BAND] * REPEATS).split(' ')
    assert words.count('ACESSO') == REPEATS and words.count('HOLOFOTE') == REPEATS
    return a, paths, dict(cap_mm=round(cap, 3), tracking=TRACK, repeats=REPEATS, zone_mm=[Z0, Z1],
                          foco_disc_mm=round(d, 3), text_ink_mm=[round(p.ink()[0], 3), round(p.ink()[2], 3)],
                          baseline_mm_from_edge=round(yb, 3))


def woven(a):
    """Jacquard render: the design is quantised to the thread grid (that is what a loom does), amarelo weft floats
    where the pattern is, a black warp-faced twill elsewhere, a 0,6 mm selvedge on each edge."""
    hh, ww = a.shape
    pw, ph = WEFT * PP, WARP * PP                  # 5 x 4 px cells
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    ci = np.floor(xx / pw).astype(int)
    cj = np.floor(yy / ph).astype(int)
    # sample the design at each cell centre
    cx = np.clip(((ci + 0.5) * pw).astype(int), 0, ww - 1)
    cy = np.clip(((cj + 0.5) * ph).astype(int), 0, hh - 1)
    m = (a[cy, cx] > 0.5).astype(np.float32)
    fx = (xx / pw) - ci                              # 0..1 inside a weft cell
    fy = (yy / ph) - cj
    weft_shape = np.sin(np.pi * fx) ** 0.7           # a weft float is round across its width
    warp_shape = np.sin(np.pi * fy) ** 0.7
    twill = ((ci + cj) % 3 == 0).astype(np.float32)  # 2/1 twill on the black ground
    am = K.hex01('amarelo')
    bk = np.array([0.055, 0.05, 0.06], np.float32)
    rnd = np.random.default_rng(927)
    jitter = rnd.normal(0, 0.035, (cj.max() + 2, ci.max() + 2)).astype(np.float32)[cj, ci]
    lum_a = 0.80 + 0.26 * weft_shape + jitter
    lum_b = 0.75 + 0.55 * (warp_shape * (1 - twill) + weft_shape * twill) + jitter * 2
    rgb = m[..., None] * am[None, None, :] * lum_a[..., None] + (1 - m)[..., None] * bk[None, None, :] * lum_b[..., None]
    hgt = m * (0.55 + 0.45 * weft_shape) + (1 - m) * (0.35 + 0.35 * (warp_shape * (1 - twill) + weft_shape * twill))
    # selvedges
    sel = ((yy < 0.6 * PP) | (yy > hh - 0.6 * PP)).astype(np.float32)
    rgb = rgb * (1 - sel[..., None]) + sel[..., None] * bk[None, None, :] * (0.8 + 0.5 * warp_shape)[..., None]
    hgt = hgt * (1 - sel) + sel * (0.5 + 0.3 * warp_shape)
    return np.clip(rgb, 0, 1), np.clip(hgt, 0, 1)


def seal():
    w, h = 60.0, 15.0
    ln = Line([run_cap(T.SEAL_FRONT, K.XP, 4.0, 0)])
    # optical centring on the x-height band of the lower case line
    xh = K.XP.xh * ln.runs[0].em / 1000
    pf = K.place_center(ln, w / 2, h / 2 + xh / 2)
    lb = Line([run_xh(T.SEAL_BACK, K.SH, 1.8)])
    pb = K.place_center(lb, w / 2, h / 2 + 1.8 / 2)
    for p, nm in ((pf, 'front'), (pb, 'back')):
        b = p.ink()
        assert b[0] > 2.0 and b[2] < w - 2.0, (nm, b)
    af, _ = K.raster_paths(w, h, PP, [K.placed_paths(pf)])
    ab, _ = K.raster_paths(w, h, PP, [K.placed_paths(pb)])
    return (af, ab, [K.placed_paths(pf)], [K.placed_paths(pb)],
            dict(front=dict(text=T.SEAL_FRONT, cap_mm=4.0, ink_mm=[round(v, 2) for v in pf.ink()]),
                 back=dict(text=T.SEAL_BACK, xh_mm=1.8, ink_mm=[round(v, 2) for v in pb.ink()])))


def main():
    od = os.path.dirname(K.out('pulseira', 'x'))
    a, paths, info = band()
    hh, ww = a.shape
    rgb = np.zeros((hh, ww, 3), np.float32) + K.hex01('preto')
    rgb = rgb * (1 - a[..., None]) + K.hex01('amarelo') * a[..., None]
    R.save_png(K.rgba_from(rgb, np.ones_like(a)), os.path.join(od, 'PULSEIRA_padrao.png'))
    doc = R.Doc(L, Wb, PP)
    doc.add(f'<rect width="{L}" height="{Wb}" fill="{T.C["preto"]}"/>')
    doc.add(f'<g id="AMARELO-JACQUARD" fill="{T.C["amarelo"]}">' + ''.join(f'<path d="{d}"/>' for d in paths) + '</g>')
    R.write_svg(doc, os.path.join(od, 'PULSEIRA_padrao.svg'))
    wv, hg = woven(a)
    R.save_png(K.rgba_from(wv, np.ones_like(a)), os.path.join(od, 'PULSEIRA_tecido.png'))
    K.save16(hg, os.path.join(od, 'PULSEIRA_tecido_altura16.png'))
    af, ab, pfp, pbp, sinfo = seal()
    for al, flood, nm, pp_ in ((af, 'amarelo', 'frente', pfp), (ab, 'papel', 'verso', pbp)):
        r_ = np.zeros(al.shape + (3,), np.float32) + K.hex01(flood)
        r_ = r_ * (1 - al[..., None]) + K.hex01('preto') * al[..., None]
        R.save_png(K.rgba_from(r_, np.ones_like(al)), os.path.join(od, f'PULSEIRA_SELO_{nm}.png'))
        d2 = R.Doc(60.0, 15.0, PP)
        d2.add(f'<rect width="60" height="15" fill="{T.C[flood]}"/>')
        d2.add(f'<g id="PRETO" fill="{T.C["preto"]}">' + ''.join(f'<path d="{d}"/>' for d in pp_) + '</g>')
        R.write_svg(d2, os.path.join(od, f'PULSEIRA_SELO_{nm}.svg'))
    R.write_json(dict(band=dict(size_mm=[Wb, L], ppmm=PP, px=[ww, hh], text=T.BAND, font='Special Gothic wght 700 '
                                'wdth 75 caps', colours=dict(ground='preto (black polyester)', jacquard='amarelo'),
                                thread_pitch_mm=dict(weft=WEFT, warp=WARP), **info,
                                orientation='x = along the band from the clasp end; y = across (15 mm)'),
                     seal=dict(size_mm=[60.0, 15.0], ppmm=PP, stock='uncoated papel-cartaz',
                               front_flood='amarelo', back_flood='papel (unprinted)', **sinfo,
                               use='wrapped round band and tail; the back is the inside face, read once torn'),
                     generator='_build/pack/pulseira.py'), os.path.join(od, 'PULSEIRA.json'))
    print('pulseira', info)


if __name__ == '__main__':
    main()
