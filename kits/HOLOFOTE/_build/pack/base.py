"""Base underside of O COPO DO SHOW (platform §C.4) and of O SINGLE (§C.9b).

    /home/user/venvs/web/bin/python _build/pack/base.py

1. The moulded relief PRECISAVA. as a 16-bit height map of the recessed panel (40 px/mm, image centre = base centre,
   white = raised 0,4 mm, black = panel floor). It reads when the glass is turned over (viewed from below, the FRONT
   of the candle at the top of the image — the orientation holofote.coating_material(relief=...) maps it in).
   Hero: Ø62 panel, 2480 x 2480 px, Expanded One caps cap 4,5 mm filled to 47,0 mm, baseline 4,0 mm above the centre.
   SINGLE: Ø46 panel, 1840 x 1840 px, cap 3,4 mm filled to 35,5 mm, baseline 3,0 mm above the centre (scaled 46/62).
   The edge of the relief is moulded: a 0,12 mm rounded shoulder, never a vertical step (glass cannot release one).
2. The lot sticker (clear matte PP, printed preto; papel on ACÚSTICO), ink only on transparent:
   hero 40 x 12 mm (1600 x 480 px), SINGLE 32 x 10 mm (1280 x 400 px).
3. A review preview of each base as seen from below under raking light, with the sticker in place.

Writes 02_PRODUTO/base/.
"""
import os
import sys
import json

import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, run_cap, CAPS

PPMM = 40
SS = 2   # supersampling for the relief profile

SIZES = {
    '200': dict(panel=62.0, outer=76.0, cap=4.5, width=47.0, baseline=4.0, sticker=(40.0, 12.0), st_centre=-7.0,
                caps=(1.4, 2.0, 1.4), tag='HLF-BASE-200'),
    '080': dict(panel=46.0, outer=58.0, cap=3.4, width=35.5, baseline=3.0, sticker=(32.0, 10.0), st_centre=-5.2,
                caps=(1.2, 1.7, 1.2), tag='HLF-BASE-080'),
}


def relief(P):
    D = P['panel']
    pp = PPMM * SS
    ln, tr = K.fit_tracking([run_cap(T.PRECISAVA, K.XP, P['cap'], 0.0, CAPS)], P['width'], lo=-20, hi=200)
    # centred horizontally on the ink, baseline `baseline` mm ABOVE the centre (toward the image top = front)
    p = K.place_center(ln, D / 2, D / 2 - P['baseline'])
    a, doc = K.raster_paths(D, D, pp, [K.placed_paths(p)])
    # rounded moulded shoulder: height = smoothstep of the inside distance over 0,12 mm
    inside = (a > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(inside, cv2.DIST_L2, 5) / pp       # mm to the edge
    sh = 0.12
    x = np.clip(dist / sh, 0, 1)
    h = x * x * (3 - 2 * x)
    h = np.maximum(h * inside, 0) + (1 - inside) * 0.0
    h = np.where(inside > 0, np.maximum(h, 0.18 * a), a * 0.18)   # keep the antialiased skirt at the foot
    h = cv2.resize(h.astype(np.float32), (int(D * PPMM), int(D * PPMM)), interpolation=cv2.INTER_AREA)
    cov = cv2.resize(a.astype(np.float32), (int(D * PPMM), int(D * PPMM)), interpolation=cv2.INTER_AREA)
    yy, xx = np.mgrid[0:h.shape[0], 0:h.shape[1]]
    rr = np.hypot(xx + 0.5 - h.shape[1] / 2, yy + 0.5 - h.shape[0] / 2) / PPMM
    assert cov[rr > D / 2 - 1.0].max() < 1e-3, 'relief too close to the panel wall'
    b = p.ink()
    info = dict(text=T.PRECISAVA, font='Special Gothic Expanded One', cap_mm=P['cap'], tracking=round(tr, 2),
                ink_width_mm=round(b[2] - b[0], 3), platform_width_mm=P['width'],
                baseline_mm_above_centre=P['baseline'], relief_mm=0.4, shoulder_mm=sh,
                ink_box_mm_from_centre=[round(b[0] - D / 2, 3), round(D / 2 - b[3], 3), round(b[2] - D / 2, 3),
                                        round(D / 2 - b[1], 3)])
    return h, cov, info, doc


def sticker(P, ink):
    w, hgt = P['sticker']
    c1, c2, c3 = P['caps']
    margin = 2.3 if w == 40.0 else 1.8
    meas = w - 2 * margin
    l1, t1 = K.fit_tracking([run_cap(T.STICKER[0], K.CN, c1, 0, CAPS)], meas, lo=0, hi=200)
    l3, t3 = K.fit_tracking([run_cap(T.STICKER[2], K.CN, c3, 0, CAPS)], meas, lo=0, hi=200)
    l2 = Line([run_cap(T.STICKER[1], K.SG(700, 75), c2, 100, CAPS)])
    gap = (hgt - 2 * margin * 0.9 - (c1 + c2 + c3)) / 2
    top = (hgt - (c1 + c2 + c3 + 2 * gap)) / 2
    y1 = top + c1
    y2 = y1 + gap + c2
    y3 = y2 + gap + c3
    pl = [K.place_left(l1, margin, y1), K.place_center(l2, w / 2, y2), K.place_left(l3, margin, y3)]
    a, doc = K.raster_paths(w, hgt, PPMM, [K.placed_paths(q) for q in pl])
    for q in pl:
        b = q.ink()
        assert b[0] >= margin - 0.01 and b[2] <= w - margin + 0.01 and b[1] > 0.5 and b[3] < hgt - 0.5, b
    info = dict(lines=list(T.STICKER), caps_mm=[c1, c2, c3], measure_mm=meas, tracking=[round(t1, 1), 100,
                round(t3, 1)], baselines_mm_from_top=[round(y1, 3), round(y2, 3), round(y3, 3)],
                fonts=['Special Gothic Condensed One', 'Special Gothic wdth 75 wght 700 (com destaque)',
                       'Special Gothic Condensed One'], line2='centred (legal mark), lines 1 and 3 fill the measure')
    doc_ink = R.Doc(w, hgt, PPMM)
    for q in pl:
        doc_ink.path(K.placed_paths(q), fill=ink)
    return a, info, doc_ink


def preview(P, h, cov, st_a, st_ink_hex, coat_hex, path):
    """The underside seen from below: coated base disc, the 1 mm recessed panel, the relief under raking light from
    the upper left, the clear matte sticker at its place. Review only (the 3D team renders the real thing)."""
    Dout, Dp = P['outer'], P['panel']
    N = int(Dout * PPMM)
    coat = K.hex01(coat_hex)
    yy, xx = np.mgrid[0:N, 0:N]
    rr = np.hypot(xx + 0.5 - N / 2, yy + 0.5 - N / 2) / PPMM
    disc = np.clip((Dout / 2 - rr) * PPMM + 0.5, 0, 1).astype(np.float32)
    panel = np.clip((Dp / 2 - rr) * PPMM + 0.5, 0, 1).astype(np.float32)
    H = np.zeros((N, N), np.float32)
    o = (N - h.shape[0]) // 2
    H[o:o + h.shape[0], o:o + h.shape[1]] = h * 0.4
    H += (1 - panel) * 1.0                                  # the rim around the panel stands 1,0 mm proud
    H = cv2.GaussianBlur(H, (0, 0), 1.2)
    gy, gx = np.gradient(H * PPMM)                          # slope (mm/mm)
    nx, ny, nz = -gx, -gy, np.ones_like(H)
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    L = np.array([-0.62, -0.62, 0.48])
    L /= np.linalg.norm(L)
    sh = (nx * L[0] + ny * L[1] + nz * L[2]) / n
    shade = 0.97 + 0.55 * (sh - L[2])
    chamfer = np.clip((rr - (Dout / 2 - 1.5)) / 1.5, 0, 1)
    shade = shade * (1 - 0.25 * chamfer)
    rgb = coat[None, None, :] * shade[..., None]
    # gloss sheen: one broad soft highlight
    hl = np.exp(-(((xx - N * 0.33) / (N * 0.22)) ** 2 + ((yy - N * 0.30) / (N * 0.16)) ** 2))
    rgb = rgb + (1 - rgb) * (0.22 * hl)[..., None]
    # sticker (image orientation = reading orientation), centred at st_centre mm (negative = below the centre)
    w, hgt = P['sticker']
    sx0 = int(round((Dout / 2 - w / 2) * PPMM))
    sy0 = int(round((Dout / 2 - P['st_centre'] - hgt / 2) * PPMM))
    film = np.zeros((N, N), np.float32)
    film[sy0:sy0 + st_a.shape[0], sx0:sx0 + st_a.shape[1]] = 1.0
    ink = np.zeros((N, N), np.float32)
    ink[sy0:sy0 + st_a.shape[0], sx0:sx0 + st_a.shape[1]] = st_a
    rgb = rgb * (1 - 0.10 * film[..., None]) + 0.10 * film[..., None] * np.array([0.92, 0.92, 0.92])
    rgb = R.over(rgb * 255.0, ink, st_ink_hex) / 255.0
    R.save_png(K.rgba_from(np.clip(rgb, 0, 1), disc), path)


def main():
    od = K.out('base', 'x')
    od = os.path.dirname(od)
    meta = {}
    for key, P in SIZES.items():
        h, cov, info, doc = relief(P)
        tag = P['tag']
        K.save16(h, os.path.join(od, f'{tag}_PRECISAVA_altura16.png'))
        R.write_svg(doc, os.path.join(od, f'{tag}_PRECISAVA.svg'))
        stinfo = {}
        for ink_name in ('preto', 'papel'):
            a, sinfo, sdoc = sticker(P, T.C[ink_name])
            w, hgt = P['sticker']
            suffix = '' if ink_name == 'preto' else '_PAPEL-ACUSTICO'
            if key == '080' and ink_name == 'papel':
                continue           # the SINGLE exists only in AO VIVO (amarelo): no papel sticker
            name = f'{tag}_ETIQUETA-LOTE{suffix}'
            R.save_png(R.ink_rgba(a, T.C[ink_name]), os.path.join(od, name + '.png'))
            R.write_svg(sdoc, os.path.join(od, name + '.svg'))
            stinfo[ink_name] = dict(file=name + '.png', px=list(a.shape[::-1]), size_mm=[w, hgt], **sinfo)
            if ink_name == 'preto':
                a_preto = a
        coat = 'amarelo'
        preview(P, h, cov, a_preto, T.C['preto'], coat, os.path.join(od, f'{tag}_preview_por-baixo.png'))
        meta[tag] = dict(relief=dict(file=f'{tag}_PRECISAVA_altura16.png', px=list(h.shape[::-1]), ppmm=PPMM,
                                     panel_diameter_mm=P['panel'], **info,
                                     orientation='viewed from below; image top = FRONT of the candle (-Y)'),
                         sticker=stinfo, sticker_centre_mm=P['st_centre'],
                         sticker_note='centre on the panel axis, st_centre mm BELOW the centre in the reading view '
                                      '(toward the BACK of the candle, +Y), so it never covers PRECISAVA.')
        print(tag, info['tracking'], info['ink_width_mm'], stinfo['preto']['tracking'])
    with open(os.path.join(od, 'HLF-BASE.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
