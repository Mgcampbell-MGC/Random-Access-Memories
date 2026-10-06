"""Refill NOVA TEMPORADA (platform §C.9): the Ø66 heat-sealed peel lid of each refill capsule, and the laser-marked
LOTE · FAB · VAL band on the capsule wall.

    /home/user/venvs/web/bin/python _build/pack/refil.py

Peel lid: paper/foil, printed ONE colour on the faixa colour (preto; papel on ACÚSTICO). Text, exact:
  NOVA TEMPORADA · [faixa name] · PESO LÍQUIDO 200 g (figures 4,0 mm) · vela aromática · refil ·
  Use dentro do copo HOLOFOTE.
Set as a lineup inside the circle: the two display lines fill their chord; the small lines are centred.
A 14 x 9 mm pull tab at 3 o'clock (die shape in alpha). 40 px/mm.

Capsule band: Ø68 capsule, wrap 213,6 x 10 mm at 40 px/mm, black anodised; the line is laser-marked (light grey)
centred on the front (u = 0,25, same convention as the copo).

Writes 02_PRODUTO/refil/.
"""
import os
import sys
import math
import json

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, run_cap, CAPS, FIG

PP = 40
D = 66.0
RR = D / 2
TAB_W, TAB_H = 9.0, 14.0             # tab sticks out 9 mm at 3 o'clock, 14 mm tall
CW, CH = D + TAB_W + 2.0, D          # canvas mm (disc left, tab right)
CX, CY = RR, RR
LASER = '#C9C8C5'
ANOD = '#141416'


def chord(dy, margin=3.2):
    r = RR - margin
    return 2 * math.sqrt(max(0.0, r * r - dy * dy))


def die_d():
    """disc + pull tab (rounded 3 mm), one outline"""
    a = math.asin((TAB_H / 2) / RR)
    x0 = CX + RR * math.cos(a)
    yt, yb = CY - TAB_H / 2, CY + TAB_H / 2
    xr = CX + RR + TAB_W
    r = 3.0
    return (f'M{x0:.3f},{yt:.3f} L{xr - r:.3f},{yt:.3f} A{r},{r} 0 0 1 {xr:.3f},{yt + r:.3f} '
            f'L{xr:.3f},{yb - r:.3f} A{r},{r} 0 0 1 {xr - r:.3f},{yb:.3f} L{x0:.3f},{yb:.3f} '
            f'A{RR},{RR} 0 1 1 {x0:.3f},{yt:.3f} Z')


def lid(faixa):
    s = T.SKUS[faixa]
    ink = T.C['papel'] if s['coating'] == 'violeta' else T.C['preto']
    placed, log = [], []

    def fill_line(text, fc, y_base, cap_guess, feats, by='size', tr=0):
        # measure on the chord at the line's cap top (narrower than at the baseline above the centre)
        for _ in range(3):
            top = y_base - cap_guess
            m = min(chord(top - CY), chord(y_base - CY))
            if by == 'size':
                ln, cap_guess = K.fit_size(lambda c: Line([run_cap(text, fc, c, tr, feats)]), m, 0.5, 30)
            else:
                ln, trk = K.fit_tracking([run_cap(text, fc, cap_guess, 0, feats)], m, lo=40, hi=260)
        p = K.place_center(ln, CX, y_base)
        placed.append(p)
        log.append(dict(text=text, cap_mm=round(cap_guess, 3), measure_mm=round(m, 2), baseline_mm=round(y_base, 2)))
        return p, cap_guess

    # vertical rhythm: built from the top, then the whole stack is centred on the disc
    def build(y0):
        placed.clear()
        log.clear()
        y = y0
        p1, c1 = fill_line(T.REF_LID[0], K.CN, y, 3.4, CAPS, by='tracking')
        y += 3.0
        y_show = y + 11.0
        p2, c2 = fill_line(s['show'], K.SG(700, s['wdth']), y_show, 11.0, CAPS, by='size')
        y = y_show + 7.0
        p3 = K.place_center(Line([run_cap(T.REF_LID[2], K.CN, 3.0, 0)]), CX, y)
        placed.append(p3)
        log.append(dict(text=T.REF_LID[2], cap_mm=3.0, baseline_mm=round(y, 2)))
        y += 7.0
        p4 = K.place_center(Line([run_cap(T.L6_RIGHT_CAPS, K.CN, 2.6, 80, CAPS),
                                  run_cap(T.L6_RIGHT_FIG, K.CN, 4.0, 0, FIG)]), CX, y)
        placed.append(p4)
        log.append(dict(text=T.REF_LID[1], cap_mm='2,6 / figures 4,0', baseline_mm=round(y, 2)))
        y += 5.6
        p5 = K.place_center(Line([run_cap(T.REF_LID[3], K.CN, 2.4, 0)]), CX, y)
        placed.append(p5)
        log.append(dict(text=T.REF_LID[3], cap_mm=2.4, baseline_mm=round(y, 2)))
        top = p1.ink()[1]
        bot = max(q.ink()[3] for q in placed)
        return top, bot
    top, bot = build(10.0)
    shift = (CY - (top + bot) / 2)
    top, bot = build(10.0 + shift)
    # every ink inside the disc with a 2,4 mm margin
    for q in placed:                         # glyph by glyph (a line box is too coarse on a circle)
        for g in q.line.glyphs:
            b = g.bounds()
            if not b:
                continue
            for (x, y) in ((b[0], b[1]), (b[2], b[1]), (b[0], b[3]), (b[2], b[3])):
                assert math.hypot(x + q.x - CX, y + q.y - CY) < RR - 2.4, (q.line.runs[0].text, x, y)
    paths = [K.placed_paths(q) for q in placed]
    a, _ = K.raster_paths(CW, CH, PP, paths)
    die, _ = K.raster_paths(CW, CH, PP, [die_d()])
    flood = K.hex01(s['coating'])
    rgb = np.zeros(a.shape + (3,), np.float32) + flood
    rgb = rgb * (1 - a[..., None]) + K.hex01(ink)[None, None, :] * a[..., None]
    code = f'HLF-REF-{faixa}'
    od = os.path.dirname(K.out('refil', 'x'))
    R.save_png(K.rgba_from(rgb, die), os.path.join(od, f'{code}_TAMPA-PEEL.png'))
    R.save_png(R.ink_rgba(a, ink), os.path.join(od, f'{code}_TAMPA-PEEL_tinta.png'))
    doc = R.Doc(CW, CH, PP)
    doc.add(f'<path d="{die_d()}" fill="{T.C[s["coating"]]}"/>')
    doc.add(f'<g id="TINTA" fill="{ink}">' + ''.join(f'<path d="{d}"/>' for d in paths) + '</g>')
    doc.add(f'<path d="{die_d()}" fill="none" stroke="#E5004F" stroke-width="0.2"/>')
    R.write_svg(doc, os.path.join(od, f'{code}_TAMPA-PEEL.svg'))
    return dict(sku=code, file=f'{code}_TAMPA-PEEL.png', px=list(a.shape[::-1]), ppmm=PP, disc_mm=D,
                tab_mm=[TAB_W, TAB_H], flood=s['coating'], ink=ink, lines=log,
                strings=[T.REF_LID[0], s['show'], T.REF_LID[1], T.REF_LID[2], T.REF_LID[3]])


def band():
    C = math.pi * 68.0
    Hb = 10.0
    ln, tr = K.fit_tracking([run_cap(T.REF_BAND, K.CN, 2.0, 0, CAPS)], 62.0)
    p = K.place_center(ln, C * 0.25, Hb / 2 + 1.0)
    a, _ = K.raster_paths(C, Hb, PP, [K.placed_paths(p)])
    od = os.path.dirname(K.out('refil', 'x'))
    R.save_png(R.ink_rgba(a, LASER), os.path.join(od, 'HLF-REF_CAPSULA_faixa-laser.png'))
    prev = np.zeros(a.shape + (3,), np.float32) + K.hex01(ANOD)
    prev = prev * (1 - a[..., None]) + K.hex01(LASER)[None, None, :] * a[..., None]
    R.save_png(K.rgba_from(prev, np.ones_like(a)), os.path.join(od, 'HLF-REF_CAPSULA_faixa-laser_preview.png'))
    return dict(file='HLF-REF_CAPSULA_faixa-laser.png', px=list(a.shape[::-1]), ppmm=PP,
                circumference_mm=round(C, 3), height_mm=Hb, text=T.REF_BAND, cap_mm=2.0, tracking=round(tr, 1),
                centre_u=0.25, mark='laser on black anodised (render the ink as the bare-aluminium tone)',
                placement='band centred 12 mm below the capsule lip (UNVERIFIED with the capsule supplier)')


def main():
    meta = dict(lids=[lid(f) for f in ('01', '02', '03', '04')], band=band(), generator='_build/pack/refil.py')
    R.write_json(meta, os.path.join(os.path.dirname(K.out('refil', 'x')), 'HLF-REF_refil.json'))
    for l in meta['lids']:
        print(l['sku'], [(x['text'], x['cap_mm']) for x in l['lines'][:2]])


if __name__ == '__main__':
    main()
