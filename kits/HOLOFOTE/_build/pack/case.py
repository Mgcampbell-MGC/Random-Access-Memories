"""O CASE (platform §C.7): every printed panel of the gift road case, set by code, plus the 3D atlases.

    /home/user/venvs/web/bin/python _build/pack/case.py [--only HLF-CASE-02]

Construction: lid box 130 x 130 x 30 and base box 130 x 130 x 102 (2 mm greyboard wrapped in black tolex paper),
silver hot-foil 4 mm on the 12 edges of the closed box, eight 12 x 12 printed foil corner caps, a die-cut hasp tab on
the lid front with a 16 x 3 slot aligned with a slot in the base front.

Panels at 10 px/mm, each drawn at its true aspect in its READING orientation (as the box's UV map shows it):
  lid:  top · front · back · left · right · inside (the dressing-room mirror)
  base: front (main panel) · left (MODO DE USO + ADVERTÊNCIAS) · right (RIDER) · back (MANIFESTO) · underside ·
        top (the EVA interior)
Type: the lid top and the base front are STENCIL. Since the CCO review (round 3, director 6 Oct 2026) a glyph is
bridged only where a stencil needs it: two short vertical 0,05 em bridges per closed counter (through the stroke above
and below it); letters without a counter (E F S C H M T …) stay whole. Legal panels are not stencilled.

Outputs in 02_PRODUTO/case/:
  CASE_<painel>.png / .svg                 common panels (art at 10 px/mm; SVG = the ink and foil layers in mm)
  HLF-CASE-0n_<painel>.png / .svg          the per-unit panels (lid top, base front, base back)
  HLF-CASE-0n_ATLAS_tampa.png / _base.png  4 x 3 atlases for candle_lib.box() (lid 130x130x30, base 130x130x102)
  CASE_ATLAS_<caixa>_foil.png              foil mask (white = silver hot-foil) in the same atlas layout
  CASE_ATLAS_<caixa>_altura16.png          16-bit tolex grain height (foil flattens the grain; corner balls domed)
  CASE_ATLAS_tampa_espelho.png             mirror mask (white = PMMA mirror) in the lid atlas
  CASE_ABA_hasp.png                        the hasp tab (RGBA, die shape and slot in alpha) + its placement in json
  HLF-CASE-0n_PREVIEW_planificado.jpg      review flat-lay of both boxes, shaded
  HLF-CASE-0n_case.json                    every string, size, position and atlas contract
"""
import os
import sys
import math
import json
import argparse
from collections import defaultdict

import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, Run, Placed, run_cap, run_xh, CAPS, FIG
from tipos import Glyph, glyph_path
import marca

PPMM = 10
W, D, H_LID, H_BASE = 130.0, 130.0, 30.0, 102.0
FOIL = 4.0
CAP_SZ = 12.0
MX0, MX1 = 10.0, 120.0           # the text measure on every 130 mm face (clear of foil and corner caps)
MEAS = MX1 - MX0
SLOT = (16.0, 3.0)
TAB = dict(w=52.0, h=16.0, r=3.0)   # hasp tab hanging below the lid front, centred
TAB_X0 = (W - TAB['w']) / 2
SLOT_X0 = TAB_X0 + 5.0
SLOT_Y = 8.0                     # slot centre, mm below the lid's lower edge (= below the base front's top edge)
CELL = 1300                      # atlas cell px (uniform cells; each face is resized into its cell)
SILVER = '#BDBFC2'
EVA = '#0C0B0D'
MIRROR = '#C9CDD1'

UNITS = {
    'HLF-CASE-02_MAE-CORACAO': dict(faixa='02', headliner='MÃE ' + K.HEART),
    'HLF-CASE-01_DONA-CIDA': dict(faixa='01', headliner='DONA CIDA'),
    'HLF-CASE-03_MAINHA': dict(faixa='03', headliner='MAINHA'),
}

PRETO, PAPEL, AMARELO = T.C['preto'], T.C['papel'], T.C['amarelo']


# =====================================================================================================================
class Face:
    """One panel: layers of SVG path data in mm (y down, reading orientation)."""

    def __init__(self, name, w, h, foil_edges='', caps=''):
        self.name, self.w, self.h = name, w, h
        self.L = defaultdict(list)     # layer -> [path d]
        self.bridge = []               # stencil bridge rects (cut from the 'st' layers)
        self.log = []
        self.tex = []                  # raster overlays: (rgba float array, x_mm, y_mm)
        self.foil_edges, self.caps = foil_edges, caps
        self.extra_height = []         # (fn) adding to height maps
        self.foil_frame()

    def foil_frame(self):
        w, h, f = self.w, self.h, FOIL
        e = self.foil_edges
        if 't' in e:
            self.L['foil'].append(K.rect_d(0, 0, w, f))
        if 'b' in e:
            self.L['foil'].append(K.rect_d(0, h - f, w, f))
        if 'l' in e:
            self.L['foil'].append(K.rect_d(0, 0, f, h))
        if 'r' in e:
            self.L['foil'].append(K.rect_d(w - f, 0, f, h))
        for c in self.caps.split(',') if self.caps else []:
            x = 0 if c[1] == 'l' else w - CAP_SZ
            y = 0 if c[0] == 't' else h - CAP_SZ
            self.L['foil'].append(cap_plate_d(x, y, c))

    def add(self, layer, p, label, stencil=False, lower=False, **meta):
        d = K.placed_paths(p)
        self.L[layer].append(d)
        if stencil:
            self.bridge += K.stencil_counter_rects(p)     # CCO review, round 3: vertical bridges per closed counter
        b = p.ink() if p.matrix is None and p.per_glyph is None else K.placed_ink_poly(p)
        self.log.append(dict(label=label, layer=layer, ink_mm=[round(v, 2) for v in b], stencil=stencil,
                             text=''.join(r.text for r in p.line.runs), **meta))
        assert b[0] >= -0.01 and b[2] <= self.w + 0.01 and b[1] >= -0.01 and b[3] <= self.h + 0.01, \
            (self.name, label, b)
        return p


def cap_plate_d(x, y, corner):
    """12 x 12 foil corner cap: square at the box corner, the inner corner rounded R4."""
    s, r = CAP_SZ, 4.0
    # build in local coords with the box corner at (0,0) and the plate toward +x,+y, then mirror
    pts = f'M0,0 H{s} V{s - r} A{r},{r} 0 0 1 {s - r},{s} H0 Z'
    sx = 1 if corner[1] == 'l' else -1
    sy = 1 if corner[0] == 't' else -1
    ox = x if sx == 1 else x + s
    oy = y if sy == 1 else y + s
    # apply the mirror by transforming the few coordinates (simple path, absolute commands)
    def tx(px, py):
        return ox + sx * px, oy + sy * py
    a = tx(0, 0)
    b = tx(s, 0)
    c = tx(s, s - r)
    d_ = tx(s - r, s)
    e = tx(0, s)
    sweep = 1 if sx * sy > 0 else 0
    return (f'M{a[0]:.3f},{a[1]:.3f} L{b[0]:.3f},{b[1]:.3f} L{c[0]:.3f},{c[1]:.3f} '
            f'A{r},{r} 0 0 {sweep} {d_[0]:.3f},{d_[1]:.3f} L{e[0]:.3f},{e[1]:.3f} Z')


# =====================================================================================================================
# type helpers
def fill_size(text, fc, meas, tracking, feats=CAPS, lo=0.5, hi=60):
    ln, cap = K.fit_size(lambda c: Line([run_cap(text, fc, c, tracking, feats)]), meas, lo, hi)
    return ln, cap


def wordmark(face, x0, baseline, ink_w=70.0, bridge=True):
    """HOLOFOTE wordmark (§D.3): Expanded One caps, tracking -10, papel letters, the THIRD O lit (its outer contour
    filled amarelo). Filled to ink_w mm. On O CASE the letters take the stencil bridge; the lit O is a lamp, not a
    letter, and stays whole."""
    ln, cap = K.fit_size(lambda c: Line([run_cap('HOLOFOTE', K.XP, c, -10, CAPS)]), ink_w, 1, 30)
    p = K.place_left(ln, x0, baseline)
    os_ = [i for i, g in enumerate(ln.glyphs) if g.fc.name(g.gid) == 'O']
    lit_i = os_[2]
    letters = []
    for i, g in enumerate(ln.glyphs):
        if i == lit_i:
            ops = g.fc.outline(g.gid)
            conts, cur = [], []
            for op in ops:
                cur.append(op)
                if op[0] in ('closePath', 'endPath'):
                    conts.append(cur)
                    cur = []

            def area(c):
                pts = [pt for op in c for pt in op[1]]
                xs, ys = [q[0] for q in pts], [q[1] for q in pts]
                return (max(xs) - min(xs)) * (max(ys) - min(ys))
            outer = max(conts, key=area)
            g2 = Glyph(g.fc, g.gid, g.x, g.y, g.em, ops=outer)
            face.L['amarelo'].append(glyph_path(g2, p.x, p.y))
        else:
            letters.append(glyph_path(g, p.x, p.y))
    face.L['papel_st' if bridge else 'papel'].append(' '.join(letters))
    if bridge:
        # bridge only the letters with a closed counter (the first two O's), never the lamp (CCO review, round 3)
        lb = ln.glyphs[lit_i].bounds()
        lx0, lx1 = p.x + lb[0], p.x + lb[2]
        face.bridge += [r for r in K.stencil_counter_rects(p) if not (lx0 - 0.01 <= r[0] <= lx1)]
    b = p.ink()
    face.log.append(dict(label='wordmark', ink_mm=[round(v, 2) for v in b], cap_mm=round(cap, 3), tracking=-10,
                         lit='third O, amarelo', stencil=bridge))
    return p, cap


def gaffer_x(face, cx, cy, strip_len_mm, seed=927):
    """A MARCA (brand generator, seed 0927): the amarelo gaffer X, textured, as a raster overlay."""
    S = int(round(strip_len_mm * PPMM))
    img, meta, tiras = marca.gerar(S=S, semente=seed)
    face.tex.append((img.astype(np.float32), cx - strip_len_mm / 2, cy - strip_len_mm / 2))
    face.log.append(dict(label='A MARCA (gaffer X)', centre_mm=[cx, cy], strip_mm=[strip_len_mm,
                         round(strip_len_mm / 3.75, 2)], seed=seed))


def block(face, layer, lines_spec, x0, y0, measure, label):
    """lines_spec: list of ('head'|'body'|'gap', text, fc, cap, tracking). Body paragraphs are broken to the measure
    (balanced, no orphans). Returns the y after the block."""
    y = y0
    for kind, text, fc, cap, tr, lead in lines_spec:
        if kind == 'gap':
            y += cap
            continue
        if kind == 'head':
            ln = Line([run_cap(text, fc, cap, tr, CAPS)])
            y += lead
            face.add(layer, K.place_left(ln, x0, y), f'{label} {text[:24]}', cap_mm=cap)
            continue
        lines, texts = K.para(text, fc, cap, measure, tr)
        for ln, tx in zip(lines, texts):
            y += lead
            face.add(layer, K.place_left(ln, x0, y), f'{label} {tx[:24]}', cap_mm=cap)
    return y


# =====================================================================================================================
# the panels
def lid_top(u):
    """Road-case lid: brand and headliner as one lockup top-left, the case serial bottom-left, the gaffer X
    bottom-right. All type stencilled (display sizes only: cap >= 5 mm)."""
    f = Face('tampa_topo', W, D, 'tblr', 'tl,tr,bl,br')
    base1 = 25.0
    p, wcap = wordmark(f, MX0, base1)
    text = T.CASE_CAMARIM + u['headliner']

    def hrun(c):                  # a heart in this line takes the glass label's heart (Expanded One proportions)
        r = run_cap(text, K.CN, c, 80, CAPS)
        r.heart_ref = K.XP
        return r
    # fills the 110 mm measure: rule 1 ("ela é sempre a maior palavra") outranks a flush lockup (director, round 3:
    # the round-3 flush version was reverted, the lockup stays ragged)
    ln, cap = K.fit_size(lambda c: Line([hrun(c)]), MEAS, 0.5, 60)
    y2 = base1 + 7.5 + cap
    f.add('papel_st', K.place_left(ln, MX0, y2), 'CAMARIM', stencil=True, cap_mm=round(cap, 3), tracking=80)
    assert cap > wcap, f'headliner line cap {cap:.2f} must stay above the wordmark cap {wcap:.2f} (rule 1)'
    f.log.append(dict(label='name line vs wordmark', name_cap_mm=round(cap, 3), wordmark_cap_mm=round(wcap, 3)))
    ln = Line([run_cap(T.CASE_NO, K.CN, 5.0, 100, CAPS)])
    f.add('papel_st', K.place_left(ln, MX0, 114.0), 'CASE Nº', stencil=True, cap_mm=5.0, tracking=100)
    gaffer_x(f, 93.0, 95.0, 42.0)
    return f


def lid_side(name, front=False):
    f = Face(name, W, H_LID, 'tlr', 'tl,tr')
    return f


def tab_face():
    """The hasp tab as its own die-cut piece: black tolex, foil-free, the slot, 'acesso restrito' beside it."""
    f = Face('aba', TAB['w'], TAB['h'], '', '')
    sx = SLOT_X0 - TAB_X0
    f.L['furo'].append(K.rrect_d(sx, SLOT_Y - SLOT[1] / 2, SLOT[0], SLOT[1], SLOT[1] / 2))
    ln = Line([run_cap(T.CASE_LID_FRONT, K.CN, 3.0, 0)])
    xh = K.CN.xh * ln.runs[0].em / 1000
    base = SLOT_Y + xh / 2                    # x-height centred on the slot's axis
    f.add('amarelo', K.place_left(ln, sx + SLOT[0] + 4.0, base), 'acesso restrito', cap_mm=3.0)
    b = f.log[-1]['ink_mm']
    assert b[2] < TAB['w'] - 3.5, b
    f.L['die'].append(tab_outline_d(0, 0))
    return f


def tab_outline_d(x0, y0):
    w, h, r = TAB['w'], TAB['h'], TAB['r']
    return (f'M{x0},{y0} H{x0 + w} V{y0 + h - r} A{r},{r} 0 0 1 {x0 + w - r},{y0 + h} H{x0 + r} '
            f'A{r},{r} 0 0 1 {x0},{y0 + h - r} Z')


def lid_inside():
    """O ESPELHO DE CAMARIM: 100 x 100 mirror inset in the 126 x 126 inner lid, a 13 mm black frame with ten printed
    bulbs (3 top, 3 bottom, 2 each side; matte papel discs Ø9 with a grey filament line)."""
    f = Face('tampa_dentro', W, D, '', '')
    inner0 = 2.0                                   # greyboard wall
    m0 = inner0 + 13.0                             # mirror from 15 to 115
    f.L['espelho'].append(K.rect_d(m0, m0, 100.0, 100.0))
    c0, c1 = inner0 + 6.5, W - inner0 - 6.5        # bulb centre line 8,5 .. 121,5
    mid = (c0 + c1) / 2
    pts = [(c0, c0), (mid, c0), (c1, c0), (c0, c1), (mid, c1), (c1, c1)]
    for k in (1, 2):
        yk = c0 + (c1 - c0) * k / 3
        pts += [(c0, yk), (c1, yk)]
    assert len(pts) == 10
    for (x, y) in pts:
        f.L['papel'].append(K.circle_d(x, y, 4.5))
        f.L['cinza'].append(filament_d(x, y))
    # the line under her reflection
    ln = Line([run_xh(T.CASE_MIRROR, K.SH, 3.5)])
    p = K.place_center(ln, W / 2, m0 + 100.0 - 7.0)
    f.add('papel', p, 'olha a atração.', xh_mm=3.5, where='printed on the mirror, centred 7 mm above its lower edge')
    f.log.append(dict(label='bulbs', centres_mm=[[round(a, 2), round(b, 2)] for a, b in pts], diameter_mm=9.0))
    return f


def filament_d(cx, cy):
    """grey filament, the way a clear bulb shows it: a tight horizontal coil strung between two support wires that
    converge to the base (stroke 0,22 mm, as filled outlines)."""
    s = 0.22
    d = []
    x0, x1, yc, amp = cx - 1.7, cx + 1.7, cy - 0.3, 0.32
    xs = np.linspace(x0, x1, 61)
    ys = yc + amp * np.sin((xs - x0) / (x1 - x0) * 2 * np.pi * 6)
    for i in range(len(xs) - 1):
        d.append(seg_d(xs[i], ys[i], xs[i + 1], ys[i + 1], s))
    d.append(seg_d(x0, yc, cx - 0.55, cy + 2.7, s))
    d.append(seg_d(x1, yc, cx + 0.55, cy + 2.7, s))
    return ' '.join(d)


def seg_d(x0, y0, x1, y1, s):
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * s / 2, dx / L * s / 2
    return (f'M{x0 + nx:.3f},{y0 + ny:.3f} L{x1 + nx:.3f},{y1 + ny:.3f} L{x1 - nx:.3f},{y1 - ny:.3f} '
            f'L{x0 - nx:.3f},{y0 - ny:.3f} Z')


def base_front(u):
    s = T.SKUS[u['faixa']]
    f = Face('base_frente', W, H_BASE, 'blr', 'bl,br')
    # the base front's own slot, hidden under the tab when closed
    f.L['furo'].append(K.rrect_d(SLOT_X0, SLOT_Y - SLOT[1] / 2, SLOT[0], SLOT[1], SLOT[1] / 2))
    text = T.CASE_FRONT_SHOW + s['show']
    ln, cap = fill_size(text, K.CN, MEAS, 80)
    y1 = 50.0
    f.add('papel_st', K.place_left(ln, MX0, y1), 'HOLOFOTE · show', stencil=True, cap_mm=round(cap, 3))
    y2 = y1 + 9.5
    pl = K.place_left(Line([run_cap(T.L6_LEFT, K.CN, 2.6, 0)]), MX0, y2)
    pr = K.place_right(Line([run_cap(T.L6_RIGHT_CAPS, K.CN, 2.6, 80, CAPS),
                             run_cap(T.L6_RIGHT_FIG, K.CN, 4.0, 0, FIG)]), MX1, y2)
    # the net-weight line is legal-size type: never bridged (a 0,13 mm bridge at cap 2,6 reads as strike-through)
    f.add('papel', pl, 'vela aromática', cap_mm=2.6)
    f.add('papel', pr, 'PESO LÍQUIDO 200 g', cap_mm='2,6 / figures 4,0')
    ln, tr = K.fit_tracking([run_cap(T.CASE_FRAGIL, K.CN, 6.0, 0, CAPS)], MEAS)
    f.add('amarelo_st', K.place_left(ln, MX0, 86.0), 'FRÁGIL', stencil=True, cap_mm=6.0, tracking=round(tr, 1))
    assert 60 <= tr <= 130, tr
    return f


def base_left():
    f = Face('base_esquerda', W, H_BASE, 'blr', 'bl,br')
    hb, bd = K.SG(700, 100), K.CN              # the body in Condensed One, tracking 0 (the Produção; round 3)

    def spec_for(top):
        sp = [('head', T.MODO_DE_USO[0], hb, 2.4, 40, top)]
        sp += [('body', t, bd, 1.8, 0, 3.0) for t in T.MODO_DE_USO[1:]]
        sp += [('head', T.ADVERTENCIAS[0], hb, 2.4, 40, 6.6)]
        sp += [('body', t, bd, 1.8, 0, 3.0) for t in T.ADVERTENCIAS[1:]]
        return sp
    # measure the block, then centre it between the top edge and the bottom foil band + corner caps
    y_end = block(Face('tmp', W, H_BASE * 3), 'papel', spec_for(2.6), MX0, 0.0, MEAS, 'x') - 0.2
    top = (H_BASE - CAP_SZ - (y_end - 2.4)) / 2 + 2.4
    block(f, 'papel', spec_for(top), MX0, 0.0, MEAS, 'MODO/ADV')
    return f


def base_right():
    f = Face('base_direita', W, H_BASE, 'blr', 'bl,br')
    ln, cap = fill_size(T.RIDER_HEAD, K.CN, MEAS, 100)
    y = 16.0 + cap
    f.add('papel', K.place_left(ln, MX0, y), 'RIDER head', cap_mm=round(cap, 3), tracking=100)
    y += 2.4
    f.L['papel'].append(K.rect_d(MX0, y, MEAS, 0.35))
    y += 1.4
    st = K.SH
    for venue, status in T.RIDER:
        y += 5.0
        pv = K.place_left(Line([run_cap(venue, K.CN, 3.0, 0)]), MX0, y)
        ps = K.place_right(Line([run_xh(status, st, 2.15)]), MX1, y)
        f.add('papel', pv, f'rider {venue}', cap_mm=3.0)
        f.add('papel', ps, f'rider {status}', xh_mm=2.15)
        leader(f, pv, ps, y, MX0, 3.0, 1.2)
    # the fictional bar block (38 x 22) and its line, bottom left
    by = y + 5.6
    f.L['papel'].append(K.bars_d(MX0, by, 38.0, 22.0 - 4.2))
    lnb = Line([run_cap(T.BARCODE, K.CN, 2.2, 60, CAPS)])
    lnb, trb = K.fit_tracking([run_cap(T.BARCODE, K.CN, 2.2, 0, CAPS)], 38.0)
    f.add('papel', K.place_left(lnb, MX0, by + 22.0), 'barcode line', cap_mm=2.2, tracking=round(trb, 1))
    f.log.append(dict(label='bar block', box_mm=[MX0, by, 38.0, 22.0], scannable=False))
    assert by + 22.0 < H_BASE - CAP_SZ - 1.0
    return f


def leader(f, pv, ps, y, x0, cap, pitch, gap=0.9):
    dot = Line([run_cap('.', K.CN, cap)])
    db = dot.ink()
    dw = db[2] - db[0]
    a, z = pv.ink()[2] + gap, ps.ink()[0] - gap
    k, xs = 0, []
    while True:
        cx = x0 + (k + 0.5) * pitch
        k += 1
        if cx - dw / 2 < a:
            continue
        if cx + dw / 2 > z:
            break
        xs.append(cx)
    for cx in xs:
        f.L['papel'].append(K.placed_paths(Placed(dot, cx - (db[0] + db[2]) / 2, y)))


def base_back(u, top=None):
    if top is None:
        y_end = base_back(u, top=14.0).log[-1]['y_mm']
        top = (H_BASE - CAP_SZ - (y_end - 14.0)) / 2
    f = Face('base_tras', W, H_BASE, 'blr', 'bl,br')
    lines = T.manifesto(u['faixa'], ver='case')
    ln, cap = fill_size(lines[0], K.CN, MEAS, 100)
    y = top + cap
    f.add('papel', K.place_left(ln, MX0, y), 'MANIFESTO head', cap_mm=round(cap, 3), tracking=100)
    y += 2.2
    f.L['papel'].append(K.rect_d(MX0, y, MEAS, 0.35))
    y += 0.6
    for t in lines[1:]:
        if t == 'INDÚSTRIA BRASILEIRA':
            y += 4.6
            ln = Line([run_cap(t, K.SG(700, 75), 3.0, 60, CAPS)])
            f.add('papel', K.place_left(ln, MX0, y), 'INDÚSTRIA BRASILEIRA', cap_mm=3.0)
            y += 0.8
            continue
        texts_lines, texts = K.para(t, K.CN, 1.8, MEAS, 0)
        for l2, tx in zip(texts_lines, texts):
            y += 2.95
            f.add('papel', K.place_left(l2, MX0, y), f'manifesto {tx[:22]}', cap_mm=1.8)
    assert y < H_BASE - CAP_SZ - 0.5, y
    f.log.append(dict(label='manifesto bottom', y_mm=round(y, 2)))
    return f


def base_under():
    f = Face('base_fundo', W, D, 'tblr', 'tl,tr,bl,br')
    ln = Line([run_cap(T.CASE_UNDER, K.CN, 3.0, 0)])
    f.add('papel', K.place_center(ln, W / 2, 56.0), 'O copo é seu', cap_mm=3.0)
    # the disposal block (CCO review, round 3): one Condensed One caps line per material, centred, no pictograms
    for k, t in enumerate(T.DISPOSAL_CASE):
        l2 = Line([run_cap(t, K.CN, 2.6, 80, CAPS)])
        f.add('papel', K.place_center(l2, W / 2, 66.0 + 5.2 * k), f'descarte {t[:12]}', cap_mm=2.6, tracking=80)
    return f


def case_decisions(u):
    """Director's decisions after the copy/compliance review (6 Oct 2026) that this unit prints."""
    d = [dict(panel='base esquerda (MODO DE USO)', **T.MODO_FIX),
         dict(panel='base fundo', **T.CASE_UNDER_FIX),
         dict(panel='base fundo', used=list(T.DISPOSAL_CASE), **T.DISPOSAL_FIX),
         dict(panel='base esquerda (MODO DE USO)', **T.BODY_PRODUCAO),
         dict(panel='tampa topo / base frente', kind=T.DD, platform='one horizontal 0,05 em bridge at 50 % cap through '
              'every glyph', used='two short vertical bridges (0,05 em) per closed counter only; letters without a '
              'counter stay whole', reason='the 50 % bridge cut the E/F middle arms into hairlines and halved S and C: '
              'it read as a strike-through'),
         dict(panel='tampa topo', kind=T.DD, status='REVERTED',
              tried='CAMARIM 1 · <name> filled to the wordmark ink width (70 mm) so the lockup is flush',
              used='CAMARIM 1 · <name> filled to the 110 mm measure (as before round 3); the lockup stays ragged',
              reason='§D rule 1 ("Ela é sempre a maior palavra") outranks a flush lockup: the flush version put the '
                     'name below the wordmark cap'),
         dict(panel='base trás (MANIFESTO)', **T.ALERG_FIX),
         dict(panel='base trás (MANIFESTO)', **T.INGREDIENT_BREAK)]
    if K.HEART in u['headliner']:
        d.append(dict(panel='tampa topo', kind=T.DD, platform='heart drawn to the Condensed One O (a narrow teardrop)',
                      used='the glass label heart: same vector, Expanded One O proportions, Condensed One bearings',
                      reason='the case-lid heart must match the heart on the glass'))
    return d


def base_top():
    """The EVA interior seen from above (box top face): 2 mm board rim, black EVA, the Ø92 cut-out for the copo with its
    lid, and the 3 mm setlist slot along the back."""
    f = Face('base_topo_EVA', W, D, '', '')
    f.L['eva'].append(K.rect_d(2.0, 2.0, W - 4.0, D - 4.0))
    f.L['eva_furo'].append(K.circle_d(W / 2, D / 2 + 4.0, 46.0))
    f.L['eva_furo'].append(K.rect_d((W - 106.0) / 2, 7.0, 106.0, 3.0))
    f.log.append(dict(label='EVA', cutout_mm=[W / 2, D / 2 + 4.0, 92.0], slot_mm=[(W - 106.0) / 2, 7.0, 106.0, 3.0],
                      note='image top = back of the case'))
    return f


# =====================================================================================================================
# raster
LAYER_ORDER = ['foil', 'espelho', 'eva', 'eva_furo', 'papel', 'papel_st', 'cinza', 'amarelo', 'amarelo_st', 'furo']


def raster_face(f):
    out = {}
    for name in set(f.L) | ({'bridge'} if f.bridge else set()):
        if name == 'die':
            continue
        if name == 'bridge':
            a, _ = K.raster_paths(f.w, f.h, PPMM, [], f.bridge)
        else:
            a, _ = K.raster_paths(f.w, f.h, PPMM, f.L[name])
        out[name] = a
    br = out.pop('bridge', None)
    for st in ('papel_st', 'amarelo_st'):
        if st in out and br is not None:
            out[st] = out[st] * (1 - br)
    hh, ww = int(round(f.h * PPMM)), int(round(f.w * PPMM))
    tex = np.zeros((hh, ww, 4), np.float32)
    for img, x, y in f.tex:
        x0, y0 = int(round(x * PPMM)), int(round(y * PPMM))
        h_, w_ = img.shape[:2]
        tex[y0:y0 + h_, x0:x0 + w_] = img
    out['_tex'] = tex
    return out


def compose_art(f, ras):
    """Albedo art for the 3D (opaque RGB): preto tolex paper, silver foil, mirror placeholder, EVA, inks."""
    hh, ww = int(round(f.h * PPMM)), int(round(f.w * PPMM))
    rgb = np.zeros((hh, ww, 3), np.float32)
    rgb[:] = K.hex01('preto')

    def lay(name, col, alpha=None):
        nonlocal rgb
        a = ras.get(name) if alpha is None else alpha
        if a is None:
            return
        c = K.hex01(col) if isinstance(col, str) else col
        rgb = rgb * (1 - a[..., None]) + c[None, None, :] * a[..., None]
    lay('foil', SILVER)
    lay('espelho', MIRROR)
    lay('eva', EVA)
    if 'eva_furo' in ras:
        lay('eva_furo', np.array([0.02, 0.02, 0.022], np.float32))
    lay('papel', 'papel')
    lay('papel_st', 'papel')
    if 'cinza' in ras:   # 45% preto tint printed over the papel bulb
        lay('cinza', K.hex01('papel') * 0.55 + K.hex01('preto') * 0.45)
    t = ras['_tex']
    if t[..., 3].max() > 0:
        rgb = rgb * (1 - t[..., 3:4]) + t[..., :3] * t[..., 3:4]
    lay('amarelo', 'amarelo')
    lay('amarelo_st', 'amarelo')
    if 'furo' in ras:
        lay('furo', np.array([0.01, 0.01, 0.012], np.float32))
    return np.clip(rgb, 0, 1)


def height_face(f, ras, seed):
    """Tolex grain 0..1 with the foil flattening it, corner-cap balls domed and riveted, slots cut."""
    hh, ww = int(round(f.h * PPMM)), int(round(f.w * PPMM))
    hgt = K.tolex(hh, ww, PPMM, seed) * 0.7 + 0.15
    if 'foil' in ras:
        fo = ras['foil']
        hgt = hgt * (1 - fo) + 0.45 * fo           # hot foil presses the grain flat, just under its peaks
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32) / PPMM
    for c in f.caps.split(',') if f.caps else []:
        cx = 0.0 if c[1] == 'l' else f.w
        cy = 0.0 if c[0] == 't' else f.h
        r = np.hypot(xx - cx, yy - cy)
        dome = np.sqrt(np.clip(1 - (r / 7.0) ** 2, 0, 1))
        hgt = np.maximum(hgt, 0.45 + 0.55 * dome * (r < 7.0))
        rx = cx + (8.6 if c[1] == 'l' else -8.6)
        ry = cy + (8.6 if c[0] == 't' else -8.6)
        rv = np.hypot(xx - rx, yy - ry)
        hgt = np.maximum(hgt, 0.45 + 0.30 * np.sqrt(np.clip(1 - (rv / 0.85) ** 2, 0, 1)))
    if 'furo' in ras:
        hgt = hgt * (1 - ras['furo'])
    if 'eva' in ras:
        eva = ras['eva']
        r_ = K.ruido.rng(seed + 7)
        cells = np.abs(K.ruido.valor(hh, ww, 0.35 * PPMM, r_))
        hgt = hgt * (1 - eva) + eva * (0.5 + 0.08 * cells)
        if 'eva_furo' in ras:
            hgt = hgt * (1 - ras['eva_furo'])
    if 'espelho' in ras:
        hgt = hgt * (1 - ras['espelho']) + 0.5 * ras['espelho']
    return np.clip(hgt, 0, 1)


def shade_preview(art, hgt, foil, mirror=None):
    """Review render: tolex lit from the upper left, foil as brushed silver, mirror as a dark reflection."""
    gy, gx = np.gradient(cv2.GaussianBlur(hgt, (0, 0), 0.8) * 2.0)
    n = np.dstack([-gx, -gy, np.ones_like(hgt)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = np.array([-0.5, -0.6, 0.62])
    L /= np.linalg.norm(L)
    lam = np.clip((n @ L), 0, 1)
    out = art * (0.55 + 0.6 * lam[..., None])
    spec = np.clip(n @ (L + np.array([0, 0, 1])) / np.linalg.norm(L + np.array([0, 0, 1])), 0, 1) ** 40
    out = out + (0.12 * spec * (1 - foil) + 0.55 * spec * foil)[..., None]
    if mirror is not None:
        hh, ww = mirror.shape
        yy = np.linspace(0, 1, hh)[:, None]
        refl = np.zeros((hh, ww, 3), np.float32) + (0.10 + 0.08 * (1 - yy))[..., None]
        out = out * (1 - mirror[..., None]) + refl * mirror[..., None]
    return np.clip(out, 0, 1)


# =====================================================================================================================
def to_cell(img, interp=cv2.INTER_CUBIC):
    return cv2.resize(img, (CELL, CELL), interpolation=interp)


def atlas(faces_imgs, fill):
    """faces_imgs: dict face -> image (float, HxW[xC]); returns the 4 x 3 atlas (row 0 at the image top)."""
    sample = next(iter(faces_imgs.values()))
    shape = (3 * CELL, 4 * CELL) + sample.shape[2:]
    A = np.zeros(shape, np.float32)
    A[:] = fill
    cells = {'top': (1, 0), 'left': (0, 1), 'front': (1, 1), 'right': (2, 1), 'back': (3, 1), 'bottom': (1, 2)}
    for k, im in faces_imgs.items():
        c, r = cells[k]
        A[r * CELL:(r + 1) * CELL, c * CELL:(c + 1) * CELL] = to_cell(im)
    return A


def save_rgb(a, path, q=None):
    arr = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
    if q:
        Image.fromarray(arr).save(path, quality=q, subsampling=0)
    else:
        Image.fromarray(arr).save(path, compress_level=6)


def save_mask(a, path):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), 'L').save(path)


def write_face_svg(f, path):
    """The print layers of one panel as a vector file in mm: foil, papel, amarelo, grey tint, cut lines. Stencil
    bridges are applied with a mask so the separations stay true knock-outs."""
    doc = R.Doc(f.w, f.h, PPMM)
    if f.bridge:
        rects = ''.join(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="#000"/>'
                        for x, y, w, h in f.bridge)
        doc.defs.append(f'<mask id="ponte" maskUnits="userSpaceOnUse" x="0" y="0" width="{f.w}" height="{f.h}">'
                        f'<rect width="{f.w}" height="{f.h}" fill="#fff"/>{rects}</mask>')
    doc.add(f'<rect width="{f.w}" height="{f.h}" fill="{PRETO}"/>')
    names = dict(foil=('FOIL-PRATA', SILVER), espelho=('ESPELHO', MIRROR), eva=('EVA', EVA),
                 eva_furo=('EVA-CORTE', '#000000'), papel=('TINTA-PAPEL', PAPEL), papel_st=('TINTA-PAPEL-STENCIL', PAPEL),
                 cinza=('TINTA-PRETO-45', '#8C8986'), amarelo=('TINTA-AMARELO', AMARELO),
                 amarelo_st=('TINTA-AMARELO-STENCIL', AMARELO), furo=('FACA-FURO', 'none'), die=('FACA', 'none'))
    for k in LAYER_ORDER + ['die']:
        if k not in f.L or not f.L[k]:
            continue
        nm, col = names[k]
        m = ' mask="url(#ponte)"' if k.endswith('_st') else ''
        if k in ('furo', 'die'):
            doc.add(f'<g id="{nm}" fill="none" stroke="#FF00FF" stroke-width="0.1">' +
                    ''.join(f'<path d="{d}"/>' for d in f.L[k]) + '</g>')
        else:
            doc.add(f'<g id="{nm}" fill="{col}"{m}>' + ''.join(f'<path d="{d}"/>' for d in f.L[k]) + '</g>')
    R.write_svg(doc, path)


def render_face(f, seed, outdir, prefix):
    ras = raster_face(f)
    art = compose_art(f, ras)
    hgt = height_face(f, ras, seed)
    foil = ras.get('foil', np.zeros(hgt.shape, np.float32))
    mirror = None
    if 'espelho' in ras:
        mirror = ras['espelho'] * (1 - ras.get('papel', 0))
    save_rgb(art, os.path.join(outdir, f'{prefix}_{f.name}.png'))
    write_face_svg(f, os.path.join(outdir, f'{prefix}_{f.name}.svg'))
    return dict(art=art, hgt=hgt, foil=foil, mirror=mirror, log=f.log, px=[art.shape[1], art.shape[0]])


def net_preview(lid, base, path):
    """Flat-lay review: lid net (left) and base net (right), shaded, on a neutral studio grey."""
    def sh(r):
        return shade_preview(r['art'], r['hgt'], r['foil'], r['mirror'])
    s = 0.5
    def rs(im):
        return cv2.resize(im, (int(im.shape[1] * s), int(im.shape[0] * s)), interpolation=cv2.INTER_AREA)
    pad = 40
    c = int(1300 * s)
    hl, hb = int(300 * s), int(1020 * s)
    Wt = pad * 3 + 4 * c * 2 + pad
    Ht = pad * 2 + c * 2 + hb + 220
    canvas = np.zeros((Ht, Wt, 3), np.float32) + 0.36
    def put(im, x, y):
        canvas[y:y + im.shape[0], x:x + im.shape[1]] = im
    # lid: top over front-row of sides; inside below
    x0, y0 = pad, pad
    put(rs(sh(lid['top'])), x0 + c, y0)
    for i, k in enumerate(['left', 'front', 'right', 'back']):
        put(rs(sh(lid[k])), x0 + i * c, y0 + c)
    put(rs(sh(lid['bottom'])), x0 + c, y0 + c + hl + pad)
    x1 = x0 + 4 * c + pad * 2
    put(rs(sh(base['top'])), x1 + c, y0)
    for i, k in enumerate(['left', 'front', 'right', 'back']):
        put(rs(sh(base[k])), x1 + i * c, y0 + c)
    put(rs(sh(base['bottom'])), x1 + c, y0 + c + hb)
    save_rgb(canvas, path, q=92)


# =====================================================================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    a = ap.parse_args()
    od = os.path.dirname(K.out('case', 'x'))
    # ----- common panels (identical on every unit)
    common = {}
    seeds = dict(top=11, front=12, back=13, left=14, right=15, bottom=16)
    lid_faces = dict(front=lid_side('tampa_frente', True), back=lid_side('tampa_tras'),
                     left=lid_side('tampa_esquerda'), right=lid_side('tampa_direita'), bottom=lid_inside())
    base_faces = dict(left=base_left(), right=base_right(), bottom=base_under(), top=base_top())
    for k, f in lid_faces.items():
        common[('lid', k)] = render_face(f, seeds[k], od, 'CASE')
    for k, f in base_faces.items():
        common[('base', k)] = render_face(f, seeds[k] + 100, od, 'CASE')
    # hasp tab
    tf = tab_face()
    ras = raster_face(tf)
    art = compose_art(tf, ras)
    die, _ = K.raster_paths(tf.w, tf.h, PPMM, tf.L['die'])
    alpha = die * (1 - ras['furo'])
    tab_rgba = K.rgba_from(art, alpha)
    R.save_png(tab_rgba, os.path.join(od, 'CASE_ABA_hasp.png'))
    write_face_svg(tf, os.path.join(od, 'CASE_ABA_hasp.svg'))
    print('common panels done')
    for uid, u in UNITS.items():
        if a.only and not uid.startswith(a.only):
            continue
        lid = {('lid', k): v for (b_, k), v in common.items() if b_ == 'lid'}
        lid_r = {k: v for (b_, k), v in common.items() if b_ == 'lid'}
        base_r = {k: v for (b_, k), v in common.items() if b_ == 'base'}
        lid_r['top'] = render_face(lid_top(u), seeds['top'], od, uid.split('_')[0])
        base_r['front'] = render_face(base_front(u), seeds['front'] + 100, od, uid.split('_')[0])
        base_r['back'] = render_face(base_back(u), seeds['back'] + 100, od, uid.split('_')[0])
        # closed-case front: show the tab over the base front in the atlas (the tab is a separate die-cut piece)
        bf = base_r['front']['art'].copy()
        tx0, ty0 = int(round(TAB_X0 * PPMM)), 0
        ta = tab_rgba.astype(np.float32) / 255.0
        hh, ww = ta.shape[:2]
        bf[ty0:ty0 + hh, tx0:tx0 + ww] = bf[ty0:ty0 + hh, tx0:tx0 + ww] * (1 - ta[..., 3:4]) + ta[..., :3] * ta[..., 3:4]
        base_closed = dict(base_r)
        base_closed['front'] = dict(base_r['front'], art=bf)
        pref = uid.split('_')[0]
        A = atlas({k: v['art'] for k, v in lid_r.items()}, K.hex01('preto'))
        save_rgb(A, os.path.join(od, f'{pref}_ATLAS_tampa.png'))
        A = atlas({k: v['art'] for k, v in base_closed.items()}, K.hex01('preto'))
        save_rgb(A, os.path.join(od, f'{pref}_ATLAS_base.png'))
        if uid.startswith('HLF-CASE-02'):
            # common masks and heights (geometry is the same on every unit)
            for box, faces in (('tampa', lid_r), ('base', base_r)):
                A = atlas({k: v['foil'] for k, v in faces.items()}, 0.0)
                save_mask(A, os.path.join(od, f'CASE_ATLAS_{box}_foil.png'))
                A = atlas({k: v['hgt'] for k, v in faces.items()}, 0.5)
                K.save16(A, os.path.join(od, f'CASE_ATLAS_{box}_altura16.png'))
            mir = {k: (v['mirror'] if v['mirror'] is not None else np.zeros_like(v['foil'])) for k, v in lid_r.items()}
            save_mask(atlas(mir, 0.0), os.path.join(od, 'CASE_ATLAS_tampa_espelho.png'))
        net_preview(lid_r, base_closed, os.path.join(od, f'{pref}_PREVIEW_planificado.jpg'))
        meta = dict(
            unit=uid, faixa=u['faixa'], headliner=u['headliner'], ppmm=PPMM,
            boxes=dict(tampa=[W, D, H_LID], base=[W, D, H_BASE]),
            atlas=dict(layout='4 x 3 cells, row 0 at the image top: [., top, ., .] / [left, front, right, back] / '
                              '[., bottom, ., .]; each face drawn at its true aspect then resized into its cell, '
                              'exactly as candle_lib.box() maps it', cell_px=CELL, px=[4 * CELL, 3 * CELL],
                       orientation='top: image top = back · bottom (lid inside / base underside): image top = front · '
                                   'sides: upright, read from outside'),
            atlas_note='the base atlas shows the case CLOSED: the hasp tab is drawn over the base front. '
                       'CASE_ABA_hasp.png is the tab alone for an open-case model.',
            tab=dict(file='CASE_ABA_hasp.png', size_mm=[TAB['w'], TAB['h']], corner_radius_mm=TAB['r'],
                     x_mm_from_left=TAB_X0, hangs_below_lid_front_mm=TAB['h'],
                     slot_mm=dict(size=list(SLOT), x_from_left=SLOT_X0, centre_below_lid_edge=SLOT_Y)),
            foil=dict(width_mm=FOIL, colour_preview=SILVER, corner_caps_mm=CAP_SZ),
            panels={k: v['log'] for k, v in list(lid_r.items()) + list(base_r.items())},
            strings=dict(lid_top=[T.CASE_NO, T.CASE_CAMARIM + u['headliner']], lid_front=T.CASE_LID_FRONT,
                         base_front=[T.CASE_FRONT_SHOW + T.SKUS[u['faixa']]['show'], T.L6_LEFT,
                                     T.L6_RIGHT_CAPS + T.L6_RIGHT_FIG, T.CASE_FRAGIL],
                         base_left=[T.MODO_DE_USO, T.ADVERTENCIAS],
                         base_right=[T.RIDER_HEAD] + [list(r) for r in T.RIDER] + [T.BARCODE],
                         base_back=T.manifesto(u['faixa'], 'case'), base_under=[T.CASE_UNDER] + T.DISPOSAL_CASE,
                         mirror=T.CASE_MIRROR),
            deviations=case_decisions(u),
            generator='_build/pack/case.py')
        R.write_json(meta, os.path.join(od, f'{pref}_case.json'))
        print(uid, 'done')


if __name__ == '__main__':
    main()
