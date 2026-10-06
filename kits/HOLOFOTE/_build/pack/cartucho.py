"""The retail cartons of HOLOFOTE (platform §C.9, §C.9b), one parametrised generator for all three:

  INGRESSO  O INGRESSO, HLF-01…04-200, 96 x 96 x 98 mm
  SINGLE    O INGRESSO SINGLE, HLF-02-080, 74 x 74 x 76 mm (O SINGLE · PESO LÍQUIDO 80 g · aprox. 16 h)
  REFIL     NOVA TEMPORADA, HLF-REF-01…04, 74 x 74 x 82 mm

    /home/user/venvs/web/bin/python _build/pack/cartucho.py [--only HLF-02-080]

All are reverse-tuck-end cartons in SBS 400 g/m² with two inks: preto + the faixa colour (on ACÚSTICO the type knocks
out to the board, never preto on violeta). Panels at 20 px/mm in reading orientation:
  frente · lateral-1 (right) · verso · lateral-2 (left) · topo (ESTE LADO PRA CIMA ↑) · fundo

INGRESSO / SINGLE front: a giant ticket that repeats the copo's own lineup scaled to the carton's measure (MÃE over the
SKU's show name), so the carton and the glass inside always agree; the hero prints exactly MÃE AO VIVO / HOLOFOTE AO
VIVO. lateral-1 MODO DE USO + ADVERTÊNCIAS (cap 1,7), verso MANIFESTO ("ver lateral"), lateral-2 holofote nela. + the
"não precisava" line + bar block + disposal. The SINGLE's MANIFESTO takes the 80 g line.
REFIL front: NOVA TEMPORADA · faixa name · O copo fica. A turnê continua. · PESO LÍQUIDO 200 g; lateral-1 MODO DE USO,
lateral-2 ADVERTÊNCIAS, verso MANIFESTO (verbatim); the bar block and the disposal symbols go to the fundo.

Outputs in 02_PRODUTO/cartucho/ per SKU: <SKU>_CARTUCHO_<painel>.png/.svg, _ATLAS.png (4 x 3, candle_lib.box()
layout), _planificado.png (flat print sheet at 10 px/mm, 3 mm bleed, art in place, top flap turned 180°),
_planificado_preview.jpg (die lines over it) and _cartucho.json. The die lines themselves are written by facas.py.
"""
import os
import sys
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
ATLAS_PP = 16

# §C.9 / §C.9b strings that only the SINGLE and the refill carton use (exact)
SINGLE_NAME = 'HOLOFOTE AO VIVO · O SINGLE'        # §B.2 "Name (PT, as printed)"
SINGLE_NET = '80 g'
SINGLE_BURN = 'aprox. 16 h'
REF_LINE = ['O copo fica.', 'A turnê continua.']   # §A.8 line 17, one sentence per line
REF_TITLE = 'NOVA TEMPORADA'


class G:
    """Carton geometry: W (front width), D (depth), H (height), the type measure and the copo-poster scale."""

    def __init__(self, W, D, H, mar):
        self.W, self.D, self.H, self.MAR = W, D, H, mar
        self.X0, self.X1 = mar, W - mar
        self.MEAS = self.X1 - self.X0
        self.KS = self.MEAS / 72.0


KINDS = {
    'INGRESSO': dict(geo=G(96.0, 96.0, 98.0, 6.0), faixas=['01', '02', '03', '04'],
                     code=lambda f: f'HLF-{f}-200', net='200 g'),
    'SINGLE': dict(geo=G(74.0, 74.0, 76.0, 5.0), faixas=['02'], code=lambda f: 'HLF-02-080', net=SINGLE_NET),
    'REFIL': dict(geo=G(74.0, 74.0, 82.0, 5.0), faixas=['01', '02', '03', '04'], code=lambda f: f'HLF-REF-{f}',
                  net='200 g'),
}


class Panel:
    def __init__(self, g, name, w, h, flood, ink):
        self.g, self.name, self.w, self.h, self.flood, self.ink = g, name, w, h, flood, ink
        self.paths, self.log, self.dev = [], [], []

    def add(self, p, label, **meta):
        b = p.ink() if p.matrix is None and p.per_glyph is None else K.placed_ink_poly(p)
        m = self.g.MAR
        assert b[0] >= m - 0.6 and b[2] <= self.w - m + 0.6 and b[1] >= 2.0 and b[3] <= self.h - 2.0, \
            (self.name, label, b)
        self.paths.append(K.placed_paths(p))
        self.log.append(dict(label=label, ink_mm=[round(v, 2) for v in b],
                             text=''.join(r.text for r in p.line.runs), **meta))
        return p

    def raw(self, d):
        self.paths.append(d)


def colours(faixa):
    s = T.SKUS[faixa]
    flood = T.C[s['coating']]
    ink = T.C['papel'] if s['coating'] == 'violeta' else T.C['preto']
    return flood, ink


def split(P, lruns, rruns, y, label):
    g = P.g
    pl = K.place_left(Line(lruns), g.X0, y)
    pr = K.place_right(Line(rruns), g.X1, y)
    P.add(pl, label + ' L')
    P.add(pr, label + ' R')
    assert pr.ink()[0] - pl.ink()[2] > 3.0, label
    return pl, pr


def manifesto(faixa, net):
    lines = T.manifesto(faixa, ver='carton')
    return [('PESO LÍQUIDO ' + net) if t == 'PESO LÍQUIDO 200 g' else t for t in lines]


# ------------------------------------------------------------------------------------------------- fronts
def front_ticket(g, faixa, single=False):
    s = T.SKUS[faixa]
    flood, ink = colours(faixa)
    P = Panel(g, 'frente', g.W, g.H, flood, ink)
    KS = g.KS
    sc = g.W / 96.0                             # absolute spacings scale with the carton (INGRESSO = 1)
    cap1 = 2.6 * KS
    y = 7.0 * sc + cap1
    name = SINGLE_NAME if single else 'HOLOFOTE ' + s['show']
    split(P, [run_cap(T.CT_FRONT['ingresso'], K.CN, cap1, 100, CAPS)], [run_cap(name, K.CN, cap1, 80, CAPS)], y, 'L1')
    capm = 17.8 * KS
    ln, tr = K.fit_tracking([run_cap('MÃE', K.XP, capm, 0, CAPS)], g.MEAS, lo=-10, hi=200)
    y += 3.2 * sc + 0.315 * capm + capm
    p2 = P.add(K.place_left(ln, g.X0, y), 'MÃE', cap_mm=round(capm, 3), tracking=round(tr, 2))
    caps3 = 10.0 * KS
    ln, tr3 = K.fit_tracking([run_cap(s['show'], K.SG(700, s['wdth']), caps3, 0, CAPS)], g.MEAS)
    y += 2.4 * KS + caps3                       # the copo L2/L3 gap (2,4 mm), scaled
    p3 = K.place_left(ln, g.X0, y)
    obst = [(p2.x + b[0], p2.x + b[2], p2.y + b[3]) for b in (q.bounds() for q in p2.line.glyphs) if b]
    fix = clear_accents(p3, obst)
    P.add(p3, 'show', cap_mm=round(caps3, 3), wdth=s['wdth'], tracking=round(tr3, 2), accent_fix=fix or None)
    y += 4.0 * sc + 4.0 * KS
    # the date line keeps the copo's proportion unless it would crowd SETOR on a small carton: then its cap steps
    # down (never under 3,0 mm) until the L/R gap is at least 3,2 mm
    capd = 4.0 * KS
    wr = Line([run_cap(T.CT_FRONT['setor'], K.CN, cap1, 80, CAPS)]).ink_width()
    while capd > 3.0 and Line([run_cap(T.CT_FRONT['date'], K.CN, capd, 80, CAPS)]).ink_width() + wr + 3.2 > g.MEAS:
        capd -= 0.05
    if abs(capd - 4.0 * KS) > 1e-6:
        P.dev.append(dict(panel='frente', reason=f'L4 date cap {capd:.2f} mm instead of {4.0 * KS:.2f} (the copo '
                          f'proportion) so DOMINGO · 09.05 clears SETOR: PRIMEIRA FILA by 3,2 mm on the {g.W:.0f} mm front'))
    split(P, [run_cap(T.CT_FRONT['date'], K.CN, capd, 80, CAPS)],
          [run_cap(T.CT_FRONT['setor'], K.CN, cap1, 80, CAPS)], y, 'L4')
    y += 2.6 * sc
    P.raw(K.rect_d(g.X0, y - 0.15, g.MEAS, 0.3))
    y += 2.6 * sc + 4.0
    left = T.L6_LEFT + (' · ' + SINGLE_BURN if single else '')
    split(P, [run_cap(left, K.CN, cap1, 0, FIG)],
          [run_cap(T.L6_RIGHT_CAPS, K.CN, cap1, 80, CAPS), run_cap(SINGLE_NET if single else T.L6_RIGHT_FIG,
                                                                     K.CN, 4.0, 0, FIG)], y, 'L5')
    yp = y + 5.6 * sc
    perf_d, xx = [], 0.0
    while xx < g.W:
        perf_d.append(K.rect_d(xx, yp - 0.2, min(1.2, g.W - xx), 0.4))
        xx += 2.0
    P.raw(' '.join(perf_d))
    ln, cst = K.fit_size(lambda c: Line([run_cap(T.CT_FRONT['stub'], K.CN, c, 100, CAPS)]), g.MEAS, 1, 20)
    ys = yp + (g.H - yp) / 2 + cst / 2
    P.add(K.place_left(ln, g.X0, ys), 'stub', cap_mm=round(cst, 3))
    P.log.append(dict(label='perforation (printed)', y_mm=round(yp, 2), dash_mm=[1.2, 0.8], weight_mm=0.4))
    if single:
        P.dev.append(dict(panel='frente', reason='§C.9b gives the SINGLE carton the INGRESSO text "with PESO LÍQUIDO '
                          '80 g, aprox. 16 h and O SINGLE": O SINGLE joins the product name on L1 as the §B.2 printed '
                          'name "HOLOFOTE AO VIVO · O SINGLE"; aprox. 16 h follows vela aromática on L5'))
    return P


def front_refil(g, faixa):
    s = T.SKUS[faixa]
    flood, ink = colours(faixa)
    P = Panel(g, 'frente', g.W, g.H, flood, ink)
    ln, c1 = K.fit_size(lambda c: Line([run_cap(REF_TITLE, K.CN, c, 100, CAPS)]), g.MEAS, 1, 30)
    y = 7.0 + c1
    P.add(K.place_left(ln, g.X0, y), REF_TITLE, cap_mm=round(c1, 3))
    y += 2.4
    P.raw(K.rect_d(g.X0, y - 0.15, g.MEAS, 0.3))
    f = K.SG(700, s['wdth'])
    ln, c2 = K.fit_size(lambda c: Line([run_cap(s['show'], f, c, 0, CAPS)]), g.MEAS, 1, 40)
    acc = 0.34 * c2 if any(ch in s['show'] for ch in 'ÁÉÍÓÚÂÊÔÃÕ') else 0.0
    y += 4.4 + acc + c2
    P.add(K.place_left(ln, g.X0, y), 'faixa', cap_mm=round(c2, 3), wdth=s['wdth'])
    f2 = K.SG(700, 100)
    la, ca = K.fit_size(lambda c: Line([run_cap(REF_LINE[0], f2, c, 0)]), g.MEAS, 1, 30)
    lb, cb = K.fit_size(lambda c: Line([run_cap(REF_LINE[1], f2, c, 0)]), g.MEAS, 1, 30)
    # bottom block first, then the Locutor line centred in the space left
    yb = g.H - 6.0
    pl = K.place_left(Line([run_cap(T.REF_LID[2], K.CN, 2.6, 0, FIG)]), g.X0, yb)
    pr = K.place_right(Line([run_cap(T.L6_RIGHT_CAPS, K.CN, 2.6, 80, CAPS), run_cap(T.L6_RIGHT_FIG, K.CN, 4.0, 0,
                                                                                    FIG)]), g.X1, yb)
    yr = yb - 4.0 - 2.4
    top = y + 0.9
    qh = ca + 2.4 + cb
    ya = top + (yr - top - qh) / 2 + ca
    P.add(K.place_left(la, g.X0, ya), REF_LINE[0], cap_mm=round(ca, 3))
    P.add(K.place_left(lb, g.X0, ya + 2.4 + cb), REF_LINE[1], cap_mm=round(cb, 3))
    P.raw(K.rect_d(g.X0, yr - 0.15, g.MEAS, 0.3))
    P.add(pl, 'vela aromática · refil')
    P.add(pr, 'PESO LÍQUIDO 200 g')
    P.dev.append(dict(panel='frente', reason='§C.9 lists the refill front as NOVA TEMPORADA · O copo fica. A turnê '
                      'continua. · faixa name · PESO LÍQUIDO 200 g; "vela aromática · refil" (the peel lid\'s own '
                      'string) is added beside the net weight so the main panel names the product'))
    return P


# ------------------------------------------------------------------------------------------------- the other panels
def legal(g, faixa, items, name):
    """Legal text in SG wght 400 at cap 1,7. If the block does not fit the panel at wdth 100, the WIDTH axis is
    solved down (never the cap height): the largest wdth in 100…75 whose block fits."""
    flood, ink = colours(faixa)
    P = Panel(g, name, g.D, g.H, flood, ink)
    hb = K.SG(700, 100)

    def run(top, write, bd):
        y = top
        first = True
        for kind, t in items:
            if kind == 'h':
                y += (0 if first else 4.6)
                first = False
                if write:
                    P.add(K.place_left(Line([run_cap(t, hb, 2.2, 40, CAPS)]), g.X0, y), t, cap_mm=2.2)
                y += 0.5
            else:
                lines, texts = K.para(t, bd, 1.7, g.MEAS, 0)
                for ln, tx in zip(lines, texts):
                    y += 2.75
                    if write:
                        P.add(K.place_left(ln, g.X0, y), tx[:30], cap_mm=1.7)
        return y
    avail = g.H - 2 * 5.5
    wd = 100
    while wd > 75 and run(0.0, False, K.SG(400, wd)) > avail:
        wd -= 5
    bd = K.SG(400, wd)
    end = run(0.0, False, bd)
    assert end <= avail + 0.5, (name, end, avail)
    run((g.H - end) / 2 + 2.2 - 1.0, True, bd)
    P.log.append(dict(label='legal width', font=f'Special Gothic wght 400 wdth {wd}', cap_mm=1.7))
    if wd != 100:
        P.dev.append(dict(panel=name, reason=f'MODO DE USO + ADVERTÊNCIAS need {run(0.0, False, K.SG(400, 100)):.1f} mm '
                          f'of height at wdth 100 on this {g.D:.0f} mm panel ({avail:.0f} mm available); the width axis '
                          f'is solved to wdth {wd} so the cap height stays at the platform\'s 1,7 mm'))
    return P


def back(g, faixa, net):
    flood, ink = colours(faixa)
    P = Panel(g, 'verso', g.W, g.H, flood, ink)
    lines = manifesto(faixa, net)

    def run(top, write):
        ln, cap = K.fit_size(lambda c: Line([run_cap(lines[0], K.CN, c, 100, CAPS)]), g.MEAS, 1, 20)
        y = top + cap
        if write:
            P.add(K.place_left(ln, g.X0, y), 'MANIFESTO head', cap_mm=round(cap, 3))
        y += 1.8
        if write:
            P.raw(K.rect_d(g.X0, y, g.MEAS, 0.3))
        y += 0.4
        for t in lines[1:]:
            if t == 'INDÚSTRIA BRASILEIRA':
                li = Line([run_cap(t, K.SG(700, 75), 3.0, 60, CAPS)])
                acc = -min(b[1] for b in (q.bounds() for q in li.glyphs) if b)        # Ú accent top over baseline
                dsc = max(b[3] for b in (q.bounds() for q in Line([run_cap('(gjpq@', K.CN, 1.7, 0, FIG)]).glyphs)
                          if b)                                                    # deepest 1,7 mm descender
                y += acc + dsc + 0.6                    # the Ú clears any descender above it by 0,6 mm
                if write:
                    P.add(K.place_left(li, g.X0, y), t, cap_mm=3.0)
                y += 0.6
                continue
            ls, ts = K.para(t, K.CN, 1.7, g.MEAS, 0)
            for l2, tx in zip(ls, ts):
                y += 2.72
                if write:
                    P.add(K.place_left(l2, g.X0, y), tx[:30], cap_mm=1.7)
        return y
    end = run(0.0, False)
    run((g.H - end) / 2 - 0.5, True)
    return P


def bars_and_bins(P, by):
    """The fictional bar block and the three disposal marks on one row. On the 96 mm carton the block is 38 x 22 (as
    on O CASE); on the 74 mm cartons it is 30 x 20 (an EAN-13 at ~80%) and the marks size to their slot."""
    g = P.g
    if g.W >= 90:
        bw, bh, size = 38.0, 22.0, 9.0
        xs = [g.X1 - 32.0, g.X1 - 18.0, g.X1 - 4.0]
    else:
        bw, bh = 30.0, 20.0
        x_start = g.X0 + bw + 5.0
        step = (g.X1 - x_start) / 3.0
        size = min(9.0, step - 1.8)
        xs = [x_start + step * (i + 0.5) for i in range(3)]
    P.raw(K.bars_d(g.X0, by, bw, bh - 4.0))
    lnb, trb = K.fit_tracking([run_cap(T.BARCODE, K.CN, 2.0, 0, CAPS)], bw)
    P.add(K.place_left(lnb, g.X0, by + bh), 'barcode line', cap_mm=2.0)
    for x, lab in zip(xs, ['papel', 'vidro', 'metal']):
        iy = by + (bh - 4.0) - 3.0 - size            # icon foot 3 mm above the foot of the bars (as on INGRESSO)
        P.raw(K.bin_icon_d(x - size / 2, iy, size))
        P.add(K.place_center(Line([run_cap(lab, K.CN, 2.0, 0)]), x, by + bh), lab, cap_mm=2.0)
    P.log.append(dict(label='bar block', box_mm=[g.X0, by, bw, bh], scannable=False))


def aspas(s):
    """ASCII double quotes to typographic aspas, opening then closing, in pairs."""
    out, open_ = [], True
    for ch in s:
        if ch == '"':
            out.append('\u201c' if open_ else '\u201d')
            open_ = not open_
        else:
            out.append(ch)
    assert open_, 'unpaired quote'
    return ''.join(out)


def side_tag(g, faixa):
    flood, ink = colours(faixa)
    P = Panel(g, 'lateral-2', g.D, g.H, flood, ink)
    ln, c1 = K.fit_size(lambda c: Line([run_cap(T.CT_SIDE2[0], K.XP, c, -10)]), g.MEAS, 1, 30)
    y = 8.0 * g.H / 98.0 + c1
    P.add(K.place_left(ln, g.X0, y), 'tagline', cap_mm=round(c1, 3), font='Expanded One lower case (Locutor)')
    q = T.CT_SIDE2[1]
    cut = q.index('. ') + 1
    qa, qb = q[:cut], q[cut + 1:]
    assert qa + ' ' + qb == q
    qa = aspas(qa)   # typesetting, not a string change: the platform's ASCII " set as Brazilian aspas “ ”
    f = K.SG(700, 100)
    la, ca = K.fit_size(lambda c: Line([run_cap(qa, f, c, 0)]), g.MEAS, 1, 30)
    lb, cb = K.fit_size(lambda c: Line([run_cap(qb, f, c, 0)]), g.MEAS, 1, 30)
    by = g.H - 8.0 * g.H / 98.0 - (22.0 if g.W >= 90 else 20.0)
    qh = ca + 3.0 + cb
    ya = y + (by - y - qh) / 2 + ca
    P.add(K.place_left(la, g.X0, ya), 'quote a', cap_mm=round(ca, 3))
    P.add(K.place_left(lb, g.X0, ya + 3.0 + cb), 'quote b', cap_mm=round(cb, 3))
    bars_and_bins(P, by)
    return P


def top(g, faixa):
    flood, ink = colours(faixa)
    P = Panel(g, 'topo', g.W, g.D, flood, ink)
    ln, c = K.fit_size(lambda c: Line([run_cap(T.CT_TOP, K.CN, c, 100, CAPS)]), g.MEAS, 1, 30)
    P.add(K.place_left(ln, g.X0, g.D / 2 + c / 2), 'topo', cap_mm=round(c, 3))
    return P


def bottom(g, faixa, with_bars=False):
    flood, ink = colours(faixa)
    P = Panel(g, 'fundo', g.W, g.D, flood, ink)
    if with_bars:
        bars_and_bins(P, (g.D - 20.0) / 2)
        P.dev.append(dict(panel='fundo', reason='§C.9 gives the refill carton\'s other panels as MODO DE USO, '
                          'ADVERTÊNCIAS and MANIFESTO; the fictional bar block and the disposal marks (side 2 on O '
                          'INGRESSO) go on the bottom, the one panel left free; the top keeps O INGRESSO\'s '
                          '"ESTE LADO PRA CIMA ↑"'))
    return P


# ------------------------------------------------------------------------------------------------- raster and files
def render(P, pp=PP):
    hh, ww = int(round(P.h * pp)), int(round(P.w * pp))
    rgb = np.zeros((hh, ww, 3), np.float32)
    rgb[:] = K.hex01(P.flood)
    if P.paths:
        a, _ = K.raster_paths(P.w, P.h, pp, P.paths)
        rgb = rgb * (1 - a[..., None]) + K.hex01(P.ink)[None, None, :] * a[..., None]
    return np.clip(rgb, 0, 1)


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


def atlas(g, imgs, fill):
    cw, ch = int(g.W * ATLAS_PP), int(g.H * ATLAS_PP)
    A = np.zeros((3 * ch, 4 * cw, 3), np.float32)
    A[:] = fill
    cells = {'top': (1, 0), 'left': (0, 1), 'front': (1, 1), 'right': (2, 1), 'back': (3, 1), 'bottom': (1, 2)}
    for k, im in imgs.items():
        c, r = cells[k]
        A[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] = cv2.resize(im, (cw, ch), interpolation=cv2.INTER_AREA)
    return A


def flat_sheet(g, imgs, flood, path_png, path_prev):
    """The flat print sheet at 10 px/mm: art on each panel, flood on flaps, 3 mm bleed, die lines on the preview."""
    pp = 10
    net = facas.tuck_end(g.W, g.D, g.H)
    bl = 3.0
    Wt, Ht = net['w'] + 2 * bl, net['h'] + 2 * bl

    def ras(el):
        doc = R.Doc(Wt, Ht, pp)
        doc.add(f'<g transform="translate({bl},{bl})">{el}</g>')
        return R.rasterise(doc)
    out_a = ras(f'<path d="{net["cut"]}"/>')
    grow = cv2.dilate((out_a > 0.5).astype(np.uint8), np.ones((int(bl * pp) * 2 + 1,) * 2, np.uint8)).astype(np.float32)
    sheet = np.ones((out_a.shape[0], out_a.shape[1], 3), np.float32)
    fl = K.hex01(flood)
    sheet = sheet * (1 - grow[..., None]) + fl[None, None, :] * grow[..., None]
    glue = net['panels']['cola']
    gx0, gy0, gw, gh = [int(round((v + bl) * pp)) for v in (glue[0], glue[1], glue[2], glue[3])]
    sheet[gy0:gy0 + gh, gx0:gx0 + gw] = 1.0                   # glue flap: unprinted board
    for key, (k2, rot) in dict(frente=('front', 0), lateral1=('right', 0), verso=('back', 0),
                               lateral2=('left', 0), topo=('top', 180), fundo=('bottom', 0)).items():
        x, y, w, h = net['panels'][key]
        im = cv2.resize(imgs[k2], (int(round(w * pp)), int(round(h * pp))), interpolation=cv2.INTER_AREA)
        if rot == 180:
            im = im[::-1, ::-1]
        xi, yi = int(round((x + bl) * pp)), int(round((y + bl) * pp))
        sheet[yi:yi + im.shape[0], xi:xi + im.shape[1]] = im
    sheet *= np.maximum(grow, 0)[..., None]
    sheet += (1 - grow)[..., None]
    save_rgb(sheet, path_png)
    cut_a = ras(f'<path d="{net["cut"]}" fill="none" stroke="#000" stroke-width="0.3"/>')
    prev = sheet * (1 - cut_a[..., None]) + np.array([0.86, 0.05, 0.2])[None, None, :] * cut_a[..., None]
    cr_a = ras(''.join(f'<path d="{c}" fill="none" stroke="#000" stroke-width="0.3" stroke-dasharray="3 1.5"/>'
                       for c in net['crease']))
    prev = prev * (1 - cr_a[..., None]) + np.array([0.1, 0.35, 0.9])[None, None, :] * cr_a[..., None]
    save_rgb(prev, path_prev, q=92)
    return net


def build(kind, faixa, od):
    K_ = KINDS[kind]
    g = K_['geo']
    code = K_['code'](faixa)
    flood, ink = colours(faixa)
    modo = [('h', T.MODO_DE_USO[0])] + [('b', t) for t in T.MODO_DE_USO[1:]]
    adv = [('h', T.ADVERTENCIAS[0])] + [('b', t) for t in T.ADVERTENCIAS[1:]]
    if kind == 'REFIL':
        panels = dict(front=front_refil(g, faixa), right=legal(g, faixa, modo, 'lateral-1'), back=back(g, faixa, K_['net']),
                      left=legal(g, faixa, adv, 'lateral-2'), top=top(g, faixa), bottom=bottom(g, faixa, True))
    else:
        panels = dict(front=front_ticket(g, faixa, kind == 'SINGLE'), right=legal(g, faixa, modo + adv, 'lateral-1'),
                      back=back(g, faixa, K_['net']), left=side_tag(g, faixa), top=top(g, faixa),
                      bottom=bottom(g, faixa))
    names = dict(front='frente', right='lateral-1', back='verso', left='lateral-2', top='topo', bottom='fundo')
    meta = dict(sku=code, kind=kind, faixa=faixa, size_mm=[g.W, g.D, g.H], stock='SBS 400 g/m²',
                inks=['preto', T.SKUS[faixa]['coating']], flood=flood, type_ink=ink, knockout=(faixa == '04'),
                ppmm=PP, panels={}, deviations=[],
                atlas=dict(file=f'{code}_CARTUCHO_ATLAS.png', cell_px=[int(g.W * ATLAS_PP), int(g.H * ATLAS_PP)],
                           layout='[., top, ., .] / [left, front, right, back] / [., bottom, ., .] '
                                  '(candle_lib.box); top: image top = back; bottom: image top = front'),
                dieline=f'02_PRODUTO/facas/FACA_CARTUCHO_{g.W:.0f}x{g.D:.0f}x{g.H:.0f}.svg',
                generator='_build/pack/cartucho.py')
    imgs = {}
    for k, P in panels.items():
        rgb = render(P)
        imgs[k] = rgb
        save_rgb(rgb, os.path.join(od, f'{code}_CARTUCHO_{names[k]}.png'))
        write_panel_svg(P, os.path.join(od, f'{code}_CARTUCHO_{names[k]}.svg'))
        meta['panels'][names[k]] = P.log
        meta['deviations'] += P.dev
    save_rgb(atlas(g, imgs, K.hex01(flood)), os.path.join(od, f'{code}_CARTUCHO_ATLAS.png'))
    flat_sheet(g, imgs, flood, os.path.join(od, f'{code}_CARTUCHO_planificado.png'),
               os.path.join(od, f'{code}_CARTUCHO_planificado_preview.jpg'))
    R.write_json(meta, os.path.join(od, f'{code}_cartucho.json'))
    print(code, 'done', [d['panel'] for d in meta['deviations']])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    a = ap.parse_args()
    od = os.path.dirname(K.out('cartucho', 'x'))
    for kind, K_ in KINDS.items():
        for f in K_['faixas']:
            code = K_['code'](f)
            if a.only and not code.startswith(a.only):
                continue
            build(kind, f, od)


if __name__ == '__main__':
    main()
