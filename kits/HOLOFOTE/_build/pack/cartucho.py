"""Carton O INGRESSO (platform §C.9) for HLF-01…04-200: a 96 x 96 x 98 mm reverse-tuck-end carton, SBS 400 g/m²,
two inks (preto + the faixa colour; on ACÚSTICO the type knocks out to the board, never preto on violeta).

    /home/user/venvs/web/bin/python _build/pack/cartucho.py [--only HLF-02]

The front is a giant ticket that repeats the copo's own lineup scaled to the 84 mm measure (x 84/72): MÃE (Expanded
One) over the SKU's show name (SG wght 700 at the copo's solved wdth), so the carton and the glass inside always agree.
For the hero this prints exactly the platform's MÃE AO VIVO / HOLOFOTE AO VIVO; for the other faixas the show name
changes as it does on the glass (§C.2 "Per SKU").

Panels at 20 px/mm, reading orientation:
  frente (main) · lateral-1 (right: MODO DE USO + ADVERTÊNCIAS, cap 1,7) · verso (MANIFESTO, "ver lateral") ·
  lateral-2 (left: holofote nela. · the "não precisava" line · bar block · disposal) · topo (ESTE LADO PRA CIMA ↑) ·
  fundo (flood only)
Outputs in 02_PRODUTO/cartucho/ per SKU: <SKU>_CARTUCHO_<painel>.png, _ATLAS.png (4 x 3, candle_lib.box layout),
_planificado.png (the flat print sheet at 10 px/mm with 3 mm bleed, art in place, top flap turned 180°) and
_planificado_preview.jpg (with the die lines over it), plus _cartucho.json. The die line itself is written by facas.py.
"""
import os
import sys
import math
import json
import argparse

import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, Placed, run_cap, run_xh, CAPS, FIG
import facas
from tipos import clear_accents

PP = 20
W, D, H = 96.0, 96.0, 98.0
MAR = 6.0
X0, X1 = MAR, W - MAR
MEAS = X1 - X0
KS = MEAS / 72.0                     # the copo poster scaled to this measure
ATLAS_PP = 16


class Panel:
    def __init__(self, name, w, h, flood, ink):
        self.name, self.w, self.h, self.flood, self.ink = name, w, h, flood, ink
        self.paths = []
        self.log = []

    def add(self, p, label, **meta):
        b = p.ink() if p.matrix is None and p.per_glyph is None else K.placed_ink_poly(p)
        assert b[0] >= MAR - 0.6 and b[2] <= self.w - MAR + 0.6 and b[1] >= 2.0 and b[3] <= self.h - 2.0, \
            (self.name, label, b)
        self.paths.append(K.placed_paths(p))
        self.log.append(dict(label=label, ink_mm=[round(v, 2) for v in b],
                             text=''.join(r.text for r in p.line.runs), **meta))
        return p

    def raw(self, d):
        self.paths.append(d)


def colours(sku):
    s = T.SKUS[sku]
    flood = T.C[s['coating']]
    ink = T.C['papel'] if s['coating'] == 'violeta' else T.C['preto']
    return flood, ink


def split(P, lruns, rruns, y, label):
    pl = K.place_left(Line(lruns), X0, y)
    pr = K.place_right(Line(rruns), X1, y)
    P.add(pl, label + ' L')
    P.add(pr, label + ' R')
    assert pr.ink()[0] - pl.ink()[2] > 3.0, label
    return pl, pr


def front(sku):
    s = T.SKUS[sku]
    flood, ink = colours(sku)
    P = Panel('frente', W, H, flood, ink)
    cap1 = 2.6 * KS
    y = 7.0 + cap1
    split(P, [run_cap(T.CT_FRONT['ingresso'], K.CN, cap1, 100, CAPS)],
          [run_cap('HOLOFOTE ' + s['show'], K.CN, cap1, 80, CAPS)], y, 'L1')
    # MÃE: Expanded One at the copo's cap x KS, filled on ink edges by tracking
    capm = 17.8 * KS
    ln, tr = K.fit_tracking([run_cap('MÃE', K.XP, capm, 0, CAPS)], MEAS, lo=-10, hi=200)
    y += 3.2 + 0.315 * capm + capm
    p2 = P.add(K.place_left(ln, X0, y), 'MÃE', cap_mm=round(capm, 3), tracking=round(tr, 2))
    caps3 = 10.0 * KS
    ln, tr3 = K.fit_tracking([run_cap(s['show'], K.SG(700, s['wdth']), caps3, 0, CAPS)], MEAS)
    y += 2.4 * KS + caps3                       # the copo L2/L3 gap (2,4 mm), scaled
    p3 = K.place_left(ln, X0, y)
    obst = [(p2.x + b[0], p2.x + b[2], p2.y + b[3]) for b in (g.bounds() for g in p2.line.glyphs) if b]
    fix = clear_accents(p3, obst)
    P.add(p3, 'show', cap_mm=round(caps3, 3), wdth=s['wdth'], tracking=round(tr3, 2), accent_fix=fix or None)
    y += 4.0 + 4.0 * KS
    split(P, [run_cap(T.CT_FRONT['date'], K.CN, 4.0 * KS, 80, CAPS)],
          [run_cap(T.CT_FRONT['setor'], K.CN, cap1, 80, CAPS)], y, 'L4')
    y += 2.6
    P.raw(K.rect_d(X0, y - 0.15, MEAS, 0.3))
    y += 2.6 + 4.0
    split(P, [run_cap(T.L6_LEFT, K.CN, cap1, 0)],
          [run_cap(T.L6_RIGHT_CAPS, K.CN, cap1, 80, CAPS), run_cap(T.L6_RIGHT_FIG, K.CN, 4.0, 0, FIG)], y, 'L5')
    # printed perforation and the stub
    yp = y + 5.6
    perf_d = []
    xx = 0.0
    while xx < W:
        perf_d.append(K.rect_d(xx, yp - 0.2, min(1.2, W - xx), 0.4))
        xx += 2.0
    P.raw(' '.join(perf_d))
    ln, cst = K.fit_size(lambda c: Line([run_cap(T.CT_FRONT['stub'], K.CN, c, 100, CAPS)]), MEAS, 1, 20)
    ys = yp + (H - yp) / 2 + cst / 2
    P.add(K.place_left(ln, X0, ys), 'stub', cap_mm=round(cst, 3))
    P.log.append(dict(label='perforation (printed)', y_mm=round(yp, 2), dash_mm=[1.2, 0.8], weight_mm=0.4))
    return P


def side_legal(sku):
    flood, ink = colours(sku)
    P = Panel('lateral-1', D, H, flood, ink)
    hb, bd = K.SG(700, 100), K.SG(400, 100)
    items = [('h', T.MODO_DE_USO[0])] + [('b', t) for t in T.MODO_DE_USO[1:]] + \
            [('h', T.ADVERTENCIAS[0])] + [('b', t) for t in T.ADVERTENCIAS[1:]]

    def run(top, write):
        y = top
        first = True
        for kind, t in items:
            if kind == 'h':
                y += (0 if first else 4.6)
                first = False
                if write:
                    P.add(K.place_left(Line([run_cap(t, hb, 2.2, 40, CAPS)]), X0, y), t, cap_mm=2.2)
                y += 0.5
            else:
                lines, texts = K.para(t, bd, 1.7, MEAS, 0)
                for ln, tx in zip(lines, texts):
                    y += 2.75
                    if write:
                        P.add(K.place_left(ln, X0, y), tx[:30], cap_mm=1.7)
        return y
    end = run(0.0, False)
    top = (H - end) / 2 + 2.2 - 1.0
    run(top, True)
    return P


def back(sku):
    flood, ink = colours(sku)
    P = Panel('verso', W, H, flood, ink)
    lines = T.manifesto(sku, ver='carton')

    def run(top, write):
        ln, cap = K.fit_size(lambda c: Line([run_cap(lines[0], K.CN, c, 100, CAPS)]), MEAS, 1, 20)
        y = top + cap
        if write:
            P.add(K.place_left(ln, X0, y), 'MANIFESTO head', cap_mm=round(cap, 3))
        y += 1.8
        if write:
            P.raw(K.rect_d(X0, y, MEAS, 0.3))
        y += 0.4
        for t in lines[1:]:
            if t == 'INDÚSTRIA BRASILEIRA':
                y += 4.2
                if write:
                    P.add(K.place_left(Line([run_cap(t, K.SG(700, 75), 3.0, 60, CAPS)]), X0, y), t, cap_mm=3.0)
                y += 0.6
                continue
            ls, ts = K.para(t, K.CN, 1.7, MEAS, 0)
            for l2, tx in zip(ls, ts):
                y += 2.72
                if write:
                    P.add(K.place_left(l2, X0, y), tx[:30], cap_mm=1.7)
        return y
    end = run(0.0, False)
    run((H - end) / 2 - 0.5, True)
    return P


def side_tag(sku):
    flood, ink = colours(sku)
    P = Panel('lateral-2', D, H, flood, ink)
    ln, c1 = K.fit_size(lambda c: Line([run_cap(T.CT_SIDE2[0], K.XP, c, -10)]), MEAS, 1, 30)
    y = 8.0 + c1
    P.add(K.place_left(ln, X0, y), 'tagline', cap_mm=round(c1, 3), font='Expanded One lower case (Locutor)')
    q = T.CT_SIDE2[1]
    cut = q.index('. ') + 1
    qa, qb = q[:cut], q[cut + 1:]
    assert qa + ' ' + qb == q
    f = K.SG(700, 100)
    la, ca = K.fit_size(lambda c: Line([run_cap(qa, f, c, 0)]), MEAS, 1, 30)
    lb, cb = K.fit_size(lambda c: Line([run_cap(qb, f, c, 0)]), MEAS, 1, 30)
    # bar block bottom-left, disposal right; the quote sits centred between the tagline and the bar row
    by = H - 8.0 - 22.0
    qh = ca + 3.0 + cb
    ya = y + (by - y - qh) / 2 + ca
    P.add(K.place_left(la, X0, ya), 'quote a', cap_mm=round(ca, 3))
    P.add(K.place_left(lb, X0, ya + 3.0 + cb), 'quote b', cap_mm=round(cb, 3))
    P.raw(K.bars_d(X0, by, 38.0, 22.0 - 4.0))
    lnb, trb = K.fit_tracking([run_cap(T.BARCODE, K.CN, 2.0, 0, CAPS)], 38.0)
    P.add(K.place_left(lnb, X0, by + 22.0), 'barcode line', cap_mm=2.0)
    xs = [X1 - 32.0, X1 - 18.0, X1 - 4.0]
    for x, lab in zip(xs, ['papel', 'vidro', 'metal']):
        P.raw(K.bin_icon_d(x - 4.5, by + 6.0, 9.0))
        P.add(K.place_center(Line([run_cap(lab, K.CN, 2.0, 0)]), x, by + 22.0), lab, cap_mm=2.0)
    P.log.append(dict(label='bar block', box_mm=[X0, by, 38.0, 22.0], scannable=False))
    return P


def top(sku):
    flood, ink = colours(sku)
    P = Panel('topo', W, D, flood, ink)
    ln, c = K.fit_size(lambda c: Line([run_cap(T.CT_TOP, K.CN, c, 100, CAPS)]), MEAS, 1, 30)
    P.add(K.place_left(ln, X0, D / 2 + c / 2), 'topo', cap_mm=round(c, 3))
    return P


def bottom(sku):
    flood, ink = colours(sku)
    return Panel('fundo', W, D, flood, ink)


def render(P, pp=PP):
    hh, ww = int(round(P.h * pp)), int(round(P.w * pp))
    rgb = np.zeros((hh, ww, 3), np.float32)
    rgb[:] = K.hex01(P.flood)
    if P.paths:
        a, _ = K.raster_paths(P.w, P.h, pp, P.paths)
        rgb = rgb * (1 - a[..., None]) + K.hex01(P.ink)[None, None, :] * a[..., None]
    else:
        a = np.zeros((hh, ww), np.float32)
    return np.clip(rgb, 0, 1), a


def save_rgb(a, path, q=None):
    arr = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
    if q:
        Image.fromarray(arr).save(path, quality=q, subsampling=0)
    else:
        Image.fromarray(arr).save(path, compress_level=6)


def write_panel_svg(P, path):
    doc = R.Doc(P.w, P.h, PP)
    doc.add(f'<rect width="{P.w}" height="{P.h}" fill="{P.flood}"/>')
    doc.add(f'<g id="TINTA" fill="{P.ink}">' + ''.join(f'<path d="{d}"/>' for d in P.paths) + '</g>')
    R.write_svg(doc, path)


def atlas(imgs, fill):
    cw, ch = int(W * ATLAS_PP), int(H * ATLAS_PP)
    A = np.zeros((3 * ch, 4 * cw, 3), np.float32)
    A[:] = fill
    cells = {'top': (1, 0), 'left': (0, 1), 'front': (1, 1), 'right': (2, 1), 'back': (3, 1), 'bottom': (1, 2)}
    for k, im in imgs.items():
        c, r = cells[k]
        A[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] = cv2.resize(im, (cw, ch), interpolation=cv2.INTER_AREA)
    return A


def flat_sheet(imgs, flood, path_png, path_prev):
    """The flat print sheet at 10 px/mm: art on each panel, flood on flaps, 3 mm bleed, die lines on the preview."""
    pp = 10
    net = facas.tuck_end(W, D, H)
    bl = 3.0
    Wt, Ht = net['w'] + 2 * bl, net['h'] + 2 * bl
    sheet = np.ones((int(round(Ht * pp)), int(round(Wt * pp)), 3), np.float32)
    # flood everything inside the outline (+ bleed), then place the panel art
    def ras(el):
        doc = R.Doc(Wt, Ht, pp)
        doc.add(f'<g transform="translate({bl},{bl})">{el}</g>')
        return R.rasterise(doc)
    out_a = ras(f'<path d="{net["cut"]}"/>')
    grow = cv2.dilate((out_a > 0.5).astype(np.uint8), np.ones((int(bl * pp) * 2 + 1,) * 2, np.uint8)).astype(np.float32)
    fl = K.hex01(flood)
    sheet = sheet * (1 - grow[..., None]) + fl[None, None, :] * grow[..., None]
    glue = net['panels']['cola']
    gx0, gy0, gw, gh = [int(round((v + bl) * pp)) for v in (glue[0], glue[1], glue[2], glue[3])]
    sheet[gy0:gy0 + gh, gx0:gx0 + gw] = 1.0                   # glue flap: unprinted board
    for key, (k2, rot) in dict(frente=('front', 0), lateral1=('right', 0), verso=('back', 0),
                               lateral2=('left', 0), topo=('top', 180), fundo=('bottom', 0)).items():
        x, y, w, h = net['panels'][key]
        im = imgs[k2]
        im = cv2.resize(im, (int(round(w * pp)), int(round(h * pp))), interpolation=cv2.INTER_AREA)
        if rot == 180:
            im = im[::-1, ::-1]
        xi, yi = int(round((x + bl) * pp)), int(round((y + bl) * pp))
        sheet[yi:yi + im.shape[0], xi:xi + im.shape[1]] = im
    sheet *= np.maximum(grow, 0)[..., None]
    sheet += (1 - grow)[..., None]
    save_rgb(sheet, path_png)
    # preview with die lines
    cut_a = ras(f'<path d="{net["cut"]}" fill="none" stroke="#000" stroke-width="0.3"/>')
    prev = sheet * (1 - cut_a[..., None]) + np.array([0.86, 0.05, 0.2])[None, None, :] * cut_a[..., None]
    cr_a = ras(''.join(f'<path d="{c}" fill="none" stroke="#000" stroke-width="0.3" stroke-dasharray="3 1.5"/>'
                       for c in net['crease']))
    prev = prev * (1 - cr_a[..., None]) + np.array([0.1, 0.35, 0.9])[None, None, :] * cr_a[..., None]
    save_rgb(prev, path_prev, q=92)
    return net


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    a = ap.parse_args()
    od = os.path.dirname(K.out('cartucho', 'x'))
    for sku in ('01', '02', '03', '04'):
        code = T.SKUS[sku]['sku']
        if a.only and not code.startswith(a.only):
            continue
        flood, ink = colours(sku)
        panels = dict(front=front(sku), right=side_legal(sku), back=back(sku), left=side_tag(sku), top=top(sku),
                      bottom=bottom(sku))
        imgs = {}
        meta = dict(sku=code, faixa=sku, size_mm=[W, D, H], stock='SBS 400 g/m²', inks=['preto', T.SKUS[sku]['coating']],
                    flood=flood, type_ink=ink, knockout=(sku == '04'), ppmm=PP, panels={},
                    atlas=dict(file=f'{code}_CARTUCHO_ATLAS.png', cell_px=[int(W * ATLAS_PP), int(H * ATLAS_PP)],
                               layout='[., top, ., .] / [left, front, right, back] / [., bottom, ., .] '
                                      '(candle_lib.box); top: image top = back; bottom: image top = front'),
                    generator='_build/pack/cartucho.py')
        names = dict(front='frente', right='lateral-1', back='verso', left='lateral-2', top='topo', bottom='fundo')
        for k, P in panels.items():
            rgb, _ = render(P)
            imgs[k] = rgb
            save_rgb(rgb, os.path.join(od, f'{code}_CARTUCHO_{names[k]}.png'))
            write_panel_svg(P, os.path.join(od, f'{code}_CARTUCHO_{names[k]}.svg'))
            meta['panels'][names[k]] = P.log
        save_rgb(atlas(imgs, K.hex01(flood)), os.path.join(od, f'{code}_CARTUCHO_ATLAS.png'))
        flat_sheet(imgs, flood, os.path.join(od, f'{code}_CARTUCHO_planificado.png'),
                   os.path.join(od, f'{code}_CARTUCHO_planificado_preview.jpg'))
        R.write_json(meta, os.path.join(od, f'{code}_cartucho.json'))
        print(code, 'done')


if __name__ == '__main__':
    main()
