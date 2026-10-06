"""Label wrap masters for O COPO DO SHOW (platform §C.1–§C.3, §C.10; contract in _build/PRODUCTION_BRIEF.md).

    /home/user/venvs/web/bin/python _build/pack/rotulos.py [--only HLF-02]

One master per SKU / personalised unit: 9552 x 2560 px = 238,8 mm circumference x print zone 18,0–82,0 mm at
40 px/mm, transparent, ink pixels only. x = 0 is the centre of the LEFT side gap; front panel x 948–3828, back panel
x 5724–8604. A platform baseline b mm sits at y = (82,0 - b) x 40.

Writes into 02_PRODUTO/rotulos/: <ID>_ROTULO_wrap.png (master), <ID>_ROTULO_wrap.svg (same art as a vector file in
real mm), <ID>_ROTULO_wrap_preview.png (coating colour behind the ink), <ID>_label_copy.json, and for the hero
(HLF-02) and the personalised hero (HLF-CASE-02) a planted-error copy for the fidelity test, written to
02_PRODUTO/rotulos/_controle/ so a printer can never pick it up with the masters.
"""
import os
import sys
import json
import argparse
import datetime

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tipos import (face, Line, Run, run_cap, run_xh, CAPS, FIG, HEART, heart_metrics, fit_tracking, fit_axis, fit_size,
                   place_left, place_right, place_center, placed_paths, Placed, clear_accents)
import raster as R
import textos as T

KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(KIT, '02_PRODUTO', 'rotulos')

PPMM = 40
W_MM, H_MM = 238.8, 64.0          # circumference x print zone height
TOP_MM = 82.0                     # y = 0 of the master is 82,0 mm above the base
MEAS = 72.0
FL, FR = 948 / PPMM, 3828 / PPMM  # front panel 23,7 .. 95,7 mm
BL, BR = 5724 / PPMM, 8604 / PPMM  # back panel 143,1 .. 215,1 mm
HAIR = 0.25
SAFE_TOP = 0.05                   # keep ink this far below the print-zone top (mm)

CN = face('CN')
XP = face('XP')
SH = face('SH')


def SG(wght, wdth):
    return face('SG', wght=wght, wdth=wdth)


def Y(b):
    """platform baseline (mm above the base) -> page y (mm, down from the 82,0 mm line)"""
    return TOP_MM - b


class Panel:
    def __init__(self):
        self.placed = []     # Placed
        self.rects = []      # (x, y, w, h)
        self.log = []        # measurements for label_copy.json
        self.dev = []        # deviations from the platform, with reasons

    def add(self, p, label, **meta):
        self.placed.append(p)
        ink = p.ink()
        m = dict(label=label, ink_mm=[round(v, 3) for v in ink], **meta)
        self.log.append(m)
        return p


# ---------------------------------------------------------------------------------------------------------------------
def split_line(panel, left_runs, right_runs, baseline, x0, x1, label):
    """L/R split to the full measure: left ink edge at x0, right ink edge at x1, one shared baseline. If an accent
    would cross the top of the print zone the WHOLE line moves down just enough (logged as a deviation)."""
    y = Y(baseline)
    L = Line(left_runs)
    Rr = Line(right_runs)
    top = min(L.ink()[1], Rr.ink()[1]) + y
    if top < SAFE_TOP:
        shift = SAFE_TOP - top
        panel.dev.append(dict(line=label, platform_baseline_mm=baseline, used_baseline_mm=round(baseline - shift, 3),
                              reason=f'accent top would sit {(-top):.3f} mm above the 82,0 mm print-zone top '
                                     f'(the master cannot hold it); line lowered by {shift:.3f} mm'))
        y += shift
        baseline -= shift
    pl = place_left(L, x0, y)
    pr = place_right(Rr, x1, y)
    panel.add(pl, label + ' L', baseline_mm=round(baseline, 3), text=''.join(r.text for r in left_runs))
    panel.add(pr, label + ' R', baseline_mm=round(baseline, 3), text=''.join(r.text for r in right_runs))
    gap = pr.ink()[0] - pl.ink()[2]
    panel.log[-1]['gap_to_left_mm'] = round(gap, 3)
    return pl, pr


def full_line(panel, runs, baseline, x0, x1, label, mode='tracking', **meta):
    y = Y(baseline)
    ln, tr = fit_tracking(runs, x1 - x0)
    p = place_left(ln, x0, y)
    panel.add(p, label, baseline_mm=baseline, tracking=round(tr, 3), text=''.join(r.text for r in runs), **meta)
    return p


def hairline(panel, x0, x1, b, label):
    y = Y(b)
    panel.rects.append((x0, y - HAIR / 2, x1 - x0, HAIR))
    panel.log.append(dict(label=label, rule_mm=[x0, b, x1 - x0, HAIR]))


# ---------------------------------------------------------------------------------------------------------------------
# §C.10 headliner fit ladder: measure 72,0 mm, baseline 51,0 mm, cap 17,8 mm. First step that works.
# The STEP is decided exactly as the platform verified it (ecd_tools/fit.py): natural advance widths, no kerning, no
# tracking. The LINE is then filled on INK edges by tracking (or, at step 4, set at the decided cap and tracked).
def adv_width(fc, s, cap):
    tot = 0
    parts = s.split(HEART)
    for i, part in enumerate(parts):
        if part:
            for gid, cl, adv, xo, yo in fc.shape(part, {'kern': False}):
                tot += adv
        if i < len(parts) - 1:
            tot += heart_metrics(fc)['adv']
    return tot / fc.cap * cap


def headliner(name, measure=MEAS, cap=17.8, force_step=None):
    feats = dict(CAPS)

    def filled(fc, c, lo=-10, hi=200):
        ln, tr = fit_tracking([run_cap(name, fc, c, 0.0, feats)], measure, lo=lo, hi=hi)
        return ln, tr, ln.ink_width() < measure - 0.01

    step = None
    if adv_width(XP, name, cap) <= measure:
        step, fc, c, wd = 1, XP, cap, 125
    if step is None:
        for w in range(124, 74, -1):
            if adv_width(SG(700, w), name, cap) <= measure:
                step, fc, c, wd = 2, SG(700, w), cap, w
                break
    if step is None and adv_width(CN, name, cap) <= measure:
        step, fc, c, wd = 3, CN, cap, None
    if step is None:
        c4 = measure / adv_width(CN, name, 1.0)
        if c4 >= 12.0:
            step, fc, c, wd = 4, CN, c4, None
    forced = None
    if force_step and force_step != step:
        forced = dict(ladder_step=step, used_step=force_step)
        if force_step == 3:
            step, fc, c, wd = 3, CN, cap, None
        else:
            raise ValueError('only a forced step 3 is supported')
    if step in (1, 2, 3, 4):
        ln, tr, short = filled(fc, c)
        names = {1: 'Special Gothic Expanded One', 2: f'Special Gothic wght 700 wdth {wd}', 3: 'Special Gothic Condensed One',
                 4: 'Special Gothic Condensed One'}
        return dict(step=step, lines=[ln], font=names[step], cap_mm=round(c, 3), tracking=round(tr, 2),
                    centred=short, wdth=wd, natural_advance_mm=round(adv_width(fc, name, c), 3), forced=forced)
    # step 5: two lines, Condensed One cap 8,4, split at a space, each <= 72 (each filled)
    words = name.split(' ')
    best = None
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        wa, wb = adv_width(CN, a, 8.4), adv_width(CN, b, 8.4)
        if wa <= measure and wb <= measure:
            d = abs(wa - wb)
            if best is None or d < best[0]:
                best = (d, a, b)
    if best:
        la, ta = fit_tracking([run_cap(best[1], CN, 8.4, 0.0, feats)], measure, lo=0, hi=200)
        lb, tb = fit_tracking([run_cap(best[2], CN, 8.4, 0.0, feats)], measure, lo=0, hi=200)
        return dict(step=5, lines=[la, lb], font='Special Gothic Condensed One', cap_mm=8.4,
                    tracking=[round(ta, 2), round(tb, 2)], centred=True, wdth=None, forced=None)
    return dict(step=6, lines=[], reject='esse nome não cabe no cartaz. tenta um apelido?')


# ---------------------------------------------------------------------------------------------------------------------
def front(panel, sku, headliner_name, opening, force_step=None):
    s = T.SKUS[sku]
    x0, x1 = FL, FR
    # L1
    split_line(panel, [run_cap(T.L1_LEFT, CN, 2.6, 80, CAPS)], [run_cap(T.L1_RIGHT, CN, 2.6, 80, CAPS)], 79.2, x0, x1,
               'L1')
    # L2 headliner
    h = headliner(headliner_name, force_step=force_step)
    if h.get('forced'):
        panel.dev.append(dict(line='L2', reason=f"fit ladder at cap 17,8 gives step {h['forced']['ladder_step']} "
                              f"(natural advance fits); the brief and the platform example (§C.10, measured by "
                              f"ecd_tools/fit.py at cap 17,9) require step {h['forced']['used_step']}: step "
                              f"{h['forced']['used_step']} is used"))
    if h['step'] == 6:
        raise SystemExit(f'{headliner_name}: {h["reject"]}')
    if h['step'] == 5:
        for ln, b, nm in zip(h['lines'], (63.4, 51.0), ('L2a', 'L2b')):
            pl = place_center(ln, (x0 + x1) / 2, Y(b)) if ln.ink_width() < MEAS - 0.01 else place_left(ln, x0, Y(b))
            panel.add(pl, nm, baseline_mm=b, step=5)
    else:
        ln = h['lines'][0]
        p = place_center(ln, (x0 + x1) / 2, Y(51.0)) if h['centred'] else place_left(ln, x0, Y(51.0))
        panel.add(p, 'L2', baseline_mm=51.0, step=h['step'], font=h['font'], cap_mm=h['cap_mm'],
                  tracking=h['tracking'], text=headliner_name)
    # L3 show name: SG wght 700, wdth as the platform solved it, cap 10,0, filled by tracking
    f3 = SG(700, s['wdth'])
    p3 = full_line(panel, [run_cap(s['show'], f3, 10.0, 0.0, CAPS)], 38.6, x0, x1, 'L3',
                   font=f'SG wght700 wdth{s["wdth"]}', cap_mm=10.0)
    # an accent in the show name (ACÚSTICO) must clear the headliner above it: re-letter that accent only
    l2 = [q for q in panel.placed if q is not p3 and q.y == Y(51.0)]
    obst = [(q.x + gb[0], q.x + gb[2], q.y + gb[3]) for q in l2 for gb in (g.bounds() for g in q.line.glyphs) if gb]
    fix = clear_accents(p3, obst)
    if fix:
        for m in panel.log:
            if m['label'] == 'L3':
                m['ink_mm'] = [round(v, 3) for v in p3.ink()]
        panel.dev.append(dict(line='L3', reason='the show-name accent rose into the headliner line above it (platform '
                              'baselines 51,0 / 38,6 leave 2,4 mm; the accent needs 3,3 mm): that accent alone is '
                              're-lettered to clear the headliner by 0,6 mm; baseline, cap, wdth and spacing unchanged',
                              changes=fix))
    # L4
    op = T.L4_RIGHT_PREFIX + opening
    pl, pr = split_line(panel, [run_cap(T.L4_LEFT, CN, 4.0, 80, CAPS)], [run_xh(op, SH, 1.6)], 32.4, x0, x1, 'L4')
    w_op = pr.ink()[2] - pr.ink()[0]
    if w_op > 34.0:
        raise SystemExit(f'abertura line {op!r} is {w_op:.1f} mm wide (> 34 mm): order refused (§C.10)')
    # rule
    hairline(panel, x0, x1, 30.6, 'rule front')
    # L5
    split_line(panel, [run_cap(s['descriptor'], CN, 2.6, 0)], [run_cap('FAIXA ' + s['faixa'], CN, 2.6, 80, CAPS)],
               26.8, x0, x1, 'L5')
    # L6: figures 4,0 mm, "g" at 100% of the figure size
    split_line(panel, [run_cap(T.L6_LEFT, CN, 2.6, 0)],
               [run_cap(T.L6_RIGHT_CAPS, CN, 2.6, 80, CAPS), run_cap(T.L6_RIGHT_FIG, CN, 4.0, 0, FIG)], 20.0, x0, x1,
               'L6')
    return h


def leaders(panel, venue_p, status_p, baseline, x0, cap=2.2, pitch=0.9, gap=0.75, label=''):
    """Dot leaders: Condensed One '.' on a 0,9 mm pitch anchored to the panel's left edge, so the dots line up in
    columns from line to line. A dot is drawn only where its ink clears both texts by `gap`."""
    dot = Line([run_cap('.', CN, cap)])
    b = dot.ink()
    dw = b[2] - b[0]
    a = venue_p.ink()[2] + gap
    z = status_p.ink()[0] - gap
    xs = []
    k = 0
    while True:
        cx = x0 + (k + 0.5) * pitch
        k += 1
        if cx - dw / 2 < a:
            continue
        if cx + dw / 2 > z:
            break
        xs.append(cx)
    y = Y(baseline)
    for cx in xs:
        panel.placed.append(place_center(Line([run_cap('.', CN, cap)]), cx, y))
    length = (xs[-1] - xs[0] + dw) if xs else 0
    panel.log.append(dict(label=label + ' leader', dots=len(xs), leader_mm=round(length, 3)))
    if length < 4.0:
        panel.dev.append(dict(line=label, reason=f'leader {length:.2f} mm < 4,0 mm minimum'))
    return length


def back(panel, estreia_venue):
    x0, x1 = BL, BR
    # B1: SG wght700 wdth125, fills 72,0 (cap solved on ink; the platform's 3,54 mm was solved on advances)
    f = SG(700, 125)
    ln, cap = fit_size(lambda c: Line([run_cap(T.B1, f, c, 0.0, CAPS)]), MEAS, 2.0, 6.0)
    panel.add(place_left(ln, x0, Y(78.3)), 'B1', baseline_mm=78.3, cap_mm=round(cap, 4), text=T.B1,
              platform_cap_mm=3.54)
    split_line(panel, [run_cap(T.B2_LEFT, CN, 2.0, 80, CAPS)], [run_cap(T.B2_RIGHT, CN, 2.0, 80, CAPS)], 74.6, x0, x1,
               'B2')
    panel.dev.append(dict(line='B2 left', **T.B2_FIX))
    panel.dev.append(dict(line='T2 venue', **T.TOUR_FIX))
    hairline(panel, x0, x1, 73.1, 'rule back top')
    tour = [(estreia_venue, T.ESTREIA_STATUS)] + T.TOUR
    st = SG(700, 75)
    widest = 0
    for i, (venue, status) in enumerate(tour):
        b = round(69.6 - 3.4 * i, 4)
        pv = place_left(Line([run_cap(venue, CN, 2.2, 0, CAPS)]), x0, Y(b))
        ps = place_right(Line([run_cap(status, st, 2.2, 0, CAPS)]), x1, Y(b))
        panel.add(pv, f'T{i + 1} venue', baseline_mm=b, text=venue)
        panel.add(ps, f'T{i + 1} status', baseline_mm=b, text=status)
        text_w = (pv.ink()[2] - pv.ink()[0]) + (ps.ink()[2] - ps.ink()[0])
        widest = max(widest, text_w)
        leaders(panel, pv, ps, b, x0, label=f'T{i + 1}')
    panel.log.append(dict(label='tour widest text', mm=round(widest, 3)))
    hairline(panel, x0, x1, 43.6, 'rule back bottom')
    panel.add(place_left(Line([run_cap(T.ATENCAO, SG(700, 100), 1.9, 60, CAPS)]), x0, Y(40.6)), 'ATENCAO',
              baseline_mm=40.6, text=T.ATENCAO)
    # warnings: SG wdth 100 wght 400, sentence case, cap 1,9; bullets hang, the continuation aligns with the text
    w4 = SG(400, 100)
    bullet = Line([run_cap('• ', w4, 1.9)])
    indent = bullet.advance  # pen position of the first letter after "• "
    bx = x0 - bullet.ink()[0]  # bullet ink-left on the measure
    for i, txt in enumerate(T.WARNINGS):
        b = round(37.8 - 2.8 * i, 4)
        if txt.startswith('• '):
            ln = Line([run_cap(txt, w4, 1.9)])
            p = Placed(ln, bx, Y(b))
        else:
            ln = Line([run_cap(txt.strip(), w4, 1.9)])
            p = Placed(ln, bx + indent, Y(b))
        panel.add(p, f'W{i + 1}', baseline_mm=b, text=txt)
    panel.add(place_left(Line([run_cap(T.B_FULL, CN, 1.9, 0, FIG)]), x0, Y(23.6)), 'B_FULL', baseline_mm=23.6,
              text=T.B_FULL)
    panel.add(place_left(Line([run_cap(T.B_ODOR, CN, 1.9, 0, FIG)]), x0, Y(20.6)), 'B_ODOR', baseline_mm=20.6,
              text=T.B_ODOR)


# ---------------------------------------------------------------------------------------------------------------------
def build(uid, sku, headliner_name='MÃE', opening=T.OPENING_DEFAULT, estreia=None, planted=False, write=True,
          force_step=None):
    """estreia: None (retail line) or (date 'DD.MM.AAAA', time 'HH:MM' or None)"""
    s = T.SKUS[sku]
    ink = T.C[s['ink']]
    coat = T.C[s['coating']]
    fp, bp = Panel(), Panel()
    h = front(fp, sku, headliner_name, opening, force_step)
    if estreia is None:
        venue = T.ESTREIA_RETAIL
        e_date = e_time = None
    else:
        e_date, e_time = estreia
        venue = f'ESTREIA · {e_date}' + (f' · {e_time}' if e_time else '')
    back(bp, venue)

    doc = R.Doc(W_MM, H_MM, PPMM)
    for p in fp.placed + bp.placed:
        doc.path(placed_paths(p))
    for x, y, w, hh in fp.rects + bp.rects:
        doc.rect(x, y, w, hh)
    # every ink pixel must sit inside its panel
    for p in fp.placed:
        b = p.ink()
        assert b[0] > FL - 0.02 and b[2] < FR + 0.02 and b[1] >= 0 and b[3] <= H_MM, ('front overflow', b)
    for p in bp.placed:
        b = p.ink()
        assert b[0] > BL - 0.02 and b[2] < BR + 0.02 and b[1] >= 0 and b[3] <= H_MM, ('back overflow', b)

    a = R.rasterise(doc)
    master = R.ink_rgba(a, ink)
    base = os.path.join(OUT, f'{uid}_ROTULO_wrap')
    res = dict(uid=uid)
    if write:
        R.save_png(master, base + '.png')
        R.write_svg(doc, base + '.svg')
        prev = R.flat(a.shape[0], a.shape[1], coat)
        R.over(prev, a, ink)
        R.save_png(np.clip(np.round(prev), 0, 255).astype(np.uint8), base + '_preview.png')
        res['master'] = base + '.png'
    if planted and write:
        # the deliberately wrong copy lives in rotulos/_controle/, never beside the masters a printer picks up
        ctl = os.path.join(OUT, '_controle')
        os.makedirs(ctl, exist_ok=True)
        res['planted'] = plant_error(master, fp, os.path.join(ctl, f'{uid}_ROTULO_wrap_ERRO-PLANTADO.png'))
        stale = base + '_ERRO-PLANTADO.png'
        if os.path.exists(stale):
            os.remove(stale)

    tour_pairs = [(venue, T.ESTREIA_STATUS)] + T.TOUR
    copy = dict(
        sku=s['sku'] if not uid.startswith('HLF-CASE') else uid.split('_')[0],
        faixa=s['faixa'],
        headliner=headliner_name,
        headliner_step=h['step'],
        show_name=s['show'],
        show_wdth=s['wdth'],
        descriptor=s['descriptor'],
        opening_act=opening,
        estreia_date=e_date,
        estreia_time=e_time,
        tour_lines=[f'{v} ........ {st}' for v, st in tour_pairs],
        warnings=list(T.WARNINGS),
        net_weight=T.NET_WEIGHT,
        lot=T.LOT, fab=T.FAB, val=T.VAL,
        master_hash=R.sha256(base + '.png') if write else None,
        # everything else printed on the master, verbatim
        front_lines=dict(L1=[T.L1_LEFT, T.L1_RIGHT], L2=headliner_name, L3=s['show'], L4=[T.L4_LEFT, T.L4_RIGHT_PREFIX +
                         opening], L5=[s['descriptor'], 'FAIXA ' + s['faixa']], L6=[T.L6_LEFT, T.L6_RIGHT_CAPS +
                         T.L6_RIGHT_FIG]),
        back_lines=dict(B1=T.B1, B2=[T.B2_LEFT, T.B2_RIGHT], tour=[list(t) for t in tour_pairs], atencao=T.ATENCAO,
                        warnings=list(T.WARNINGS), full=T.B_FULL, odorizante=T.B_ODOR),
        ink=dict(name=s['ink'], hex=ink), coating=dict(name=s['coating'], hex=coat),
        contract=dict(px=[9552, 2560], ppmm=PPMM, front_px=[948, 3828], back_px=[5724, 8604],
                      y_rule='y = (82,0 - baseline_mm) x 40'),
        headliner_fit=dict(step=h['step'], font=h.get('font'), cap_mm=h.get('cap_mm'), tracking=h.get('tracking'),
                           centred=h.get('centred'), natural_advance_mm=h.get('natural_advance_mm'),
                           forced=h.get('forced'), fill='ink edges on 72,0 mm by tracking'),
        measurements=dict(front=fp.log, back=bp.log),
        deviations=fp.dev + bp.dev,
        planted_error=res.get('planted'),
        generated=datetime.date.today().isoformat(),
        generator='_build/pack/rotulos.py',
    )
    if write:
        R.write_json(copy, os.path.join(OUT, f'{uid}_label_copy.json'))
    res['copy'] = copy
    return res


def plant_error(master, fp, path, size=300):
    """Fidelity control (§D.7): mirror a lettered 300 x 300 px patch on the headliner. The patch is centred on the
    left part of the LAST letter of the headliner (E in MÃE: an asymmetric letter, so a mirror is a real change)."""
    L2 = [p for p in fp.placed if p in fp.placed and p.line.glyphs and any(r for r in p.line.runs if r.em > 20)]
    p = L2[0]
    # last glyph with ink that is a letter
    gs = [g for g in p.line.glyphs if g.bounds() and g.ops is None]
    g = gs[-1]
    b = g.bounds()
    cx = (p.x + b[0] + (b[2] - b[0]) * 0.30) * PPMM
    cy = (p.y + (b[1] + b[3]) / 2) * PPMM
    x0 = int(round(cx - size / 2))
    y0 = int(round(cy - size / 2))
    out = master.copy()
    out[y0:y0 + size, x0:x0 + size] = master[y0:y0 + size, x0:x0 + size][:, ::-1]
    R.save_png(out, path)
    changed = int((out[..., 3] != master[..., 3]).sum())
    return dict(file=os.path.relpath(path, OUT), patch_px=[x0, y0, size, size], mirrored='horizontal',
                on_glyph=p.line.glyphs[p.line.glyphs.index(g)].fc.name(g.gid), alpha_pixels_changed=changed,
                note='fidelity control only: NOT a print master')


UNITS = {
    'HLF-01': dict(sku='01'),
    'HLF-02': dict(sku='02', planted=True),
    'HLF-03': dict(sku='03'),
    'HLF-04': dict(sku='04'),
    # personalised units (§C.10). Only the MÃE ♥ birth data is from the platform (C02 example line);
    # DONA CIDA and MAINHA carry FICTIONAL sample order data (date required, time optional) to show both variants.
    'HLF-CASE-02_MAE-CORACAO': dict(sku='02', headliner_name='MÃE ' + HEART, estreia=('03.08.2003', '14:32'),
                                    planted=True),
    'HLF-CASE-01_DONA-CIDA': dict(sku='01', headliner_name='DONA CIDA', estreia=('21.11.1999', '06:40')),
    'HLF-CASE-03_MAINHA': dict(sku='03', headliner_name='MAINHA', estreia=('14.02.2005', None), force_step=3),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    a = ap.parse_args()
    for uid, kw in UNITS.items():
        if a.only and not uid.startswith(a.only):
            continue
        r = build(uid, **kw)
        c = r['copy']
        print(uid, 'step', c['headliner_step'], c['headliner_fit'], 'dev', len(c['deviations']))
        for d in c['deviations']:
            print('   DEV', d)


if __name__ == '__main__':
    main()
