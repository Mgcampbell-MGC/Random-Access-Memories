"""O SINGLE (HLF-02-080) label wrap master (platform §C.9b; same contract as the hero, scaled to its glass).

    /home/user/venvs/web/bin/python _build/pack/single.py

Contract (shared with the 3D team): 7288 x 1960 px = 182,2 mm circumference x print zone 14,0–63,0 mm at 40 px/mm,
transparent, ink pixels only (PRETO-PALCO on AMARELO-CARTAZ). x = 0 is the centre of the LEFT side gap: u = 0,25 is the
front panel centre (x = 1822, panel x 742–2902), u = 0,75 the back (x = 5466, panel x 4386–6546). A platform baseline
b mm sits at y = (63,0 - b) x 40. The SINGLE is re-set, never scaled, and never personalised.

Writes into 02_PRODUTO/rotulos/: HLF-02-080_ROTULO_wrap.png (+ .svg, _preview.png, _ERRO-PLANTADO.png) and
HLF-02-080_label_copy.json.
"""
import os
import sys
import datetime

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tipos import (face, Line, Placed, run_cap, run_xh, CAPS, FIG, fit_tracking, fit_size, place_left, place_right,
                   placed_paths)
import raster as R
import textos as T

KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(KIT, '02_PRODUTO', 'rotulos')

PPMM = 40
CIRC = 182.2
W_MM, H_MM = CIRC, 49.0          # circumference x print zone height (14,0–63,0)
TOP_MM = 63.0
MEAS = 54.0
FC, BC = CIRC * 0.25, CIRC * 0.75            # 45,55 / 136,65 mm
FL, FR = FC - MEAS / 2, FC + MEAS / 2        # 18,55 .. 72,55 mm (px 742 .. 2902)
BL, BR = BC - MEAS / 2, BC + MEAS / 2        # 109,65 .. 163,65 mm (px 4386 .. 6546)
HAIR = 0.25

CN = face('CN')
XP = face('XP')
SH = face('SH')


def SG(wght, wdth):
    return face('SG', wght=wght, wdth=wdth)


def Y(b):
    return TOP_MM - b


# §C.9b exact strings (the SINGLE's own text; the hero's live in textos.py)
S_L1_RIGHT = 'O SINGLE'
S_NET = '80 g'
S_TOUR = [('PRÉZINHO, DIA DAS MÃES', 'PRIMEIRA FILA'),
          ('PRONTO-SOCORRO, 3H', 'SEM INGRESSO. ENTROU.'),
          ('09.05.2027', 'A ATRAÇÃO É ELA')]
S_WARN = ['• Nunca deixe a vela acesa sem supervisão.',
          '• Mantenha fora do alcance de crianças e animais.',
          '• Acenda longe de cortinas, tecidos, papéis',
          '  e correntes de ar, sobre superfície firme',
          '  e resistente ao calor.',
          '• O copo esquenta: não toque nem mova',
          '  a vela acesa.']
S_ODOR = ['ODORIZANTE DE AMBIENTE', 'Perfuma o ambiente com aroma agradável.']


class Panel:
    def __init__(self):
        self.placed, self.rects, self.log, self.dev = [], [], [], []

    def add(self, p, label, **meta):
        self.placed.append(p)
        self.log.append(dict(label=label, ink_mm=[round(v, 3) for v in p.ink()], **meta))
        return p


def split(panel, lruns, rruns, b, x0, x1, label):
    pl = place_left(Line(lruns), x0, Y(b))
    pr = place_right(Line(rruns), x1, Y(b))
    panel.add(pl, label + ' L', baseline_mm=b, text=''.join(r.text for r in lruns))
    panel.add(pr, label + ' R', baseline_mm=b, text=''.join(r.text for r in rruns))
    panel.log[-1]['gap_to_left_mm'] = round(pr.ink()[0] - pl.ink()[2], 3)
    assert pr.ink()[0] - pl.ink()[2] > 2.0, (label, 'L/R collide')
    return pl, pr


def rule(panel, x0, x1, b, label):
    panel.rects.append((x0, Y(b) - HAIR / 2, x1 - x0, HAIR))
    panel.log.append(dict(label=label, rule_mm=[x0, b, x1 - x0, HAIR]))


def leaders(panel, pv, ps, b, x0, cap, pitch, gap=0.62, label=''):
    dot = Line([run_cap('.', CN, cap)])
    db = dot.ink()
    dw = db[2] - db[0]
    a, z = pv.ink()[2] + gap, ps.ink()[0] - gap
    xs, k = [], 0
    while True:
        cx = x0 + (k + 0.5) * pitch
        k += 1
        if cx - dw / 2 < a:
            continue
        if cx + dw / 2 > z:
            break
        xs.append(cx)
    for cx in xs:
        panel.placed.append(Placed(dot, cx - (db[0] + db[2]) / 2, Y(b)))
    length = (xs[-1] - xs[0] + dw) if xs else 0
    panel.log.append(dict(label=label + ' leader', dots=len(xs), leader_mm=round(length, 3)))
    if length < 4.0 * cap / 2.2:
        panel.dev.append(dict(line=label, reason=f'leader {length:.2f} mm is short'))


def front(panel):
    s = T.SKUS['02']
    x0, x1 = FL, FR
    split(panel, [run_cap(T.L1_LEFT, CN, 2.0, 80, CAPS)], [run_cap(S_L1_RIGHT, CN, 2.0, 80, CAPS)], 60.8, x0, x1, 'L1')
    # L2 headliner: Expanded One cap 13,4, filled on ink edges by tracking
    ln, tr = fit_tracking([run_cap('MÃE', XP, 13.4, 0.0, CAPS)], MEAS, lo=-10, hi=200)
    p = place_left(ln, x0, Y(40.8))
    tilde_top = TOP_MM - p.ink()[1]
    panel.add(p, 'L2', baseline_mm=40.8, font='Special Gothic Expanded One', cap_mm=13.4, tracking=round(tr, 2),
              text='MÃE', tilde_top_mm=round(tilde_top, 3), platform_tilde_top_mm=58.4)
    # L3 AO VIVO: SG wght 700 wdth 125 cap 7,5 (53,6 mm natural), filled on ink edges by tracking
    ln, tr = fit_tracking([run_cap(s['show'], SG(700, 125), 7.5, 0.0, CAPS)], MEAS)
    panel.add(place_left(ln, x0, Y(31.2)), 'L3', baseline_mm=31.2, font='SG wght700 wdth125', cap_mm=7.5,
              tracking=round(tr, 2), text=s['show'])
    # L4
    pl, pr = split(panel, [run_cap(T.L4_LEFT, CN, 3.0, 80, CAPS)],
                   [run_xh(T.L4_RIGHT_PREFIX + T.OPENING_DEFAULT, SH, 1.4)], 26.2, x0, x1, 'L4')
    rule(panel, x0, x1, 24.8, 'rule front')
    split(panel, [run_cap(s['descriptor'], CN, 2.2, 0)], [run_cap('FAIXA ' + s['faixa'], CN, 2.2, 80, CAPS)],
          21.6, x0, x1, 'L5')
    split(panel, [run_cap(T.L6_LEFT, CN, 2.2, 0)],
          [run_cap(T.L6_RIGHT_CAPS, CN, 2.2, 80, CAPS), run_cap(S_NET, CN, 4.0, 0, FIG)], 15.2, x0, x1, 'L6')
    g_bottom = TOP_MM - panel.placed[-1].ink()[3]
    panel.log.append(dict(label='L6 g descender bottom', mm_above_base=round(g_bottom, 3), platform=14.2))


def back(panel):
    x0, x1 = BL, BR
    f = SG(700, 125)
    ln, cap = fit_size(lambda c: Line([run_cap(T.B1, f, c, 0.0, CAPS)]), MEAS, 1.5, 5.0)
    panel.add(place_left(ln, x0, Y(60.2)), 'B1', baseline_mm=60.2, cap_mm=round(cap, 4), platform_cap_mm=2.66,
              text=T.B1)
    rule(panel, x0, x1, 58.6, 'rule back top')
    st = SG(700, 75)
    widest = 0
    for i, (venue, status) in enumerate(S_TOUR):
        b = round(56.0 - 2.8 * i, 4)
        pv = place_left(Line([run_cap(venue, CN, 1.8, 0, CAPS)]), x0, Y(b))
        ps = place_right(Line([run_cap(status, st, 1.8, 0, CAPS)]), x1, Y(b))
        panel.add(pv, f'T{i + 1} venue', baseline_mm=b, text=venue)
        panel.add(ps, f'T{i + 1} status', baseline_mm=b, text=status)
        widest = max(widest, (pv.ink()[2] - pv.ink()[0]) + (ps.ink()[2] - ps.ink()[0]))
        leaders(panel, pv, ps, b, x0, 1.8, 0.75, label=f'T{i + 1}')
    panel.log.append(dict(label='tour widest text', mm=round(widest, 3)))
    rule(panel, x0, x1, 48.6, 'rule back bottom')
    panel.add(place_left(Line([run_cap(T.ATENCAO, SG(700, 100), 1.7, 60, CAPS)]), x0, Y(46.2)), 'ATENCAO',
              baseline_mm=46.2, text=T.ATENCAO)
    w4 = SG(400, 100)
    bullet = Line([run_cap('• ', w4, 1.7)])
    indent = bullet.advance
    bx = x0 - bullet.ink()[0]
    widest_w = 0
    for i, txt in enumerate(S_WARN):
        b = round(43.7 - 2.5 * i, 4)
        if txt.startswith('• '):
            p = Placed(Line([run_cap(txt, w4, 1.7)]), bx, Y(b))
        else:
            p = Placed(Line([run_cap(txt.strip(), w4, 1.7)]), bx + indent, Y(b))
        panel.add(p, f'W{i + 1}', baseline_mm=b, text=txt)
        widest_w = max(widest_w, p.ink()[2] - x0)
    panel.log.append(dict(label='warnings widest', mm=round(widest_w, 3)))
    for txt, b, lab in ((T.B_FULL, 26.0, 'B_FULL'), (S_ODOR[0], 23.5, 'ODOR1'), (S_ODOR[1], 21.0, 'ODOR2')):
        p = place_left(Line([run_cap(txt, CN, 1.7, 0, FIG)]), x0, Y(b))
        panel.add(p, lab, baseline_mm=b, text=txt)
        widest_w = max(widest_w, p.ink()[2] - x0)
    panel.log.append(dict(label='widest back line', mm=round(widest_w, 3), platform_mm=50.6))


def plant_error(master, fp, path):
    """§D.7 control: mirror a lettered 226 x 226 px patch (the hero's 300 px scaled 13,4/17,8) on the E of MÃE."""
    p = [q for q in fp.placed if q.line.runs[0].text == 'MÃE'][0]
    g = [g for g in p.line.glyphs if g.bounds()][-1]
    b = g.bounds()
    size = 226
    cx = (p.x + b[0] + (b[2] - b[0]) * 0.30) * PPMM
    cy = (p.y + (b[1] + b[3]) / 2) * PPMM
    x0, y0 = int(round(cx - size / 2)), int(round(cy - size / 2))
    out = master.copy()
    out[y0:y0 + size, x0:x0 + size] = master[y0:y0 + size, x0:x0 + size][:, ::-1]
    R.save_png(out, path)
    return dict(file=os.path.basename(path), patch_px=[x0, y0, size, size], mirrored='horizontal',
                on_glyph=g.fc.name(g.gid), alpha_pixels_changed=int((out[..., 3] != master[..., 3]).sum()))


def main():
    s = T.SKUS['02']
    fp, bp = Panel(), Panel()
    front(fp)
    back(bp)
    doc = R.Doc(W_MM, H_MM, PPMM)
    for p in fp.placed + bp.placed:
        doc.path(placed_paths(p))
    for x, y, w, h in fp.rects + bp.rects:
        doc.rect(x, y, w, h)
    for p in fp.placed:
        b = p.ink()
        assert b[0] > FL - 0.02 and b[2] < FR + 0.02 and b[1] >= 0 and b[3] <= H_MM, ('front overflow', b)
    for p in bp.placed:
        b = p.ink()
        assert b[0] > BL - 0.02 and b[2] < BR + 0.02 and b[1] >= 0 and b[3] <= H_MM, ('back overflow', b)
    a = R.rasterise(doc)
    assert a.shape == (1960, 7288), a.shape
    ink, coat = T.C['preto'], T.C['amarelo']
    master = R.ink_rgba(a, ink)
    base = os.path.join(OUT, 'HLF-02-080_ROTULO_wrap')
    R.save_png(master, base + '.png')
    R.write_svg(doc, base + '.svg')
    prev = R.flat(a.shape[0], a.shape[1], coat)
    R.over(prev, a, ink)
    R.save_png(np.clip(np.round(prev), 0, 255).astype(np.uint8), base + '_preview.png')
    planted = plant_error(master, fp, base + '_ERRO-PLANTADO.png')
    copy = dict(
        sku='HLF-02-080', faixa='02', headliner='MÃE', headliner_step=1, show_name=s['show'], show_wdth=125,
        descriptor=s['descriptor'], opening_act=T.OPENING_DEFAULT, estreia_date=None, estreia_time=None,
        tour_lines=[f'{v} ........ {st}' for v, st in S_TOUR], warnings=list(S_WARN), net_weight=S_NET,
        lot=T.LOT, fab=T.FAB, val=T.VAL, master_hash=R.sha256(base + '.png'),
        front_lines=dict(L1=[T.L1_LEFT, S_L1_RIGHT], L2='MÃE', L3=s['show'],
                         L4=[T.L4_LEFT, T.L4_RIGHT_PREFIX + T.OPENING_DEFAULT], L5=[s['descriptor'], 'FAIXA 02'],
                         L6=[T.L6_LEFT, T.L6_RIGHT_CAPS + S_NET]),
        back_lines=dict(B1=T.B1, tour=[list(t) for t in S_TOUR], atencao=T.ATENCAO, warnings=list(S_WARN),
                        full=T.B_FULL, odorizante=S_ODOR),
        ink=dict(name='preto', hex=ink), coating=dict(name='amarelo', hex=coat),
        contract=dict(px=[7288, 1960], ppmm=PPMM, circumference_mm=CIRC, print_zone_mm=[14.0, 63.0],
                      front_px=[742, 2902], back_px=[4386, 6546], front_centre_u=0.25, back_centre_u=0.75,
                      y_rule='y = (63,0 - baseline_mm) x 40'),
        measurements=dict(front=fp.log, back=bp.log), deviations=fp.dev + bp.dev, planted_error=planted,
        personalised=False, generated=datetime.date.today().isoformat(), generator='_build/pack/single.py')
    R.write_json(copy, os.path.join(OUT, 'HLF-02-080_label_copy.json'))
    for d in copy['deviations']:
        print('DEV', d)
    print('HLF-02-080 written', base + '.png')
    for m in fp.log + bp.log:
        if m['label'] in ('L2', 'L3', 'B1', 'widest back line', 'tour widest text', 'L6 g descender bottom'):
            print('  ', m)


if __name__ == '__main__':
    main()
