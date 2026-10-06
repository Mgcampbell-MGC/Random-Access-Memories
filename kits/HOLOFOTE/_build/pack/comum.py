"""Shared helpers for the HOLOFOTE printed surfaces (02_PRODUTO): curved text, stencil cuts, text blocks with good
line breaks, simple vector devices (O FOCO, arrows, hearts), the fictional bar block, and procedural textures.

Everything is in millimetres on a y-down page, like tipos.py. Raster work goes through raster.py (Chromium coverage
masks) and numpy.
"""
import os
import sys
import math

import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
KIT = os.path.dirname(BUILD)
PROD = os.path.join(KIT, '02_PRODUTO')
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(BUILD, 'brand'))

from tipos import (face, Line, Run, Placed, run_cap, run_xh, CAPS, FIG, fit_tracking, fit_size, place_left,  # noqa
                   place_right, place_center, placed_paths, glyph_path, stencil_bands, HEART, fmt)
import raster as R  # noqa: E402
import textos as T  # noqa: E402
import ruido  # noqa: E402  (brand team's deterministic noise)

CN = face('CN')
XP = face('XP')
SH = face('SH')


def SG(wght, wdth):
    return face('SG', wght=wght, wdth=wdth)


def out(*parts):
    p = os.path.join(PROD, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


# --------------------------------------------------------------------------------------------------- curved text
def arc_bottom(line, cx, cy, r_base, centre_deg=0.0):
    """Set a Line on a circle so it reads upright at the BOTTOM of the circle (6 o'clock), letters' tops toward the
    centre, baseline on radius r_base. centre_deg rotates the text's centre counter-clockwise from 6 o'clock.
    Returns a Placed with per-glyph matrices (page mm)."""
    b = line.ink()
    mid = (b[0] + b[2]) / 2
    mats = []
    for g in line.glyphs:
        adv_mid = g.x + _adv(g) / 2
        s = adv_mid - mid
        al = s / r_base + math.radians(centre_deg)
        a, bb, c, d = math.cos(al), -math.sin(al), math.sin(al), math.cos(al)
        px, py = cx + r_base * math.sin(al), cy + r_base * math.cos(al)
        mats.append((a, bb, c, d, px - a * adv_mid, py - bb * adv_mid))
    return Placed(line, 0, 0, per_glyph=mats)


def arc_top(line, cx, cy, r_base, centre_deg=0.0):
    """Text on a circle reading upright at 12 o'clock (letters' tops pointing outward)."""
    b = line.ink()
    mid = (b[0] + b[2]) / 2
    mats = []
    for g in line.glyphs:
        adv_mid = g.x + _adv(g) / 2
        s = adv_mid - mid
        al = s / r_base + math.radians(centre_deg)
        a, bb, c, d = math.cos(al), math.sin(al), -math.sin(al), math.cos(al)
        px, py = cx + r_base * math.sin(al), cy - r_base * math.cos(al)
        mats.append((a, bb, c, d, px - a * adv_mid, py - bb * adv_mid))
    return Placed(line, 0, 0, per_glyph=mats)


def _adv(g):
    if g.ops is not None:
        from tipos import heart_metrics
        return heart_metrics(g.fc)['adv'] * g.em / g.fc.upm
    return g.fc.font.get_glyph_h_advance(g.gid) * g.em / g.fc.upm


def rotated(line, x, y, deg, anchor='left'):
    """A Line rotated by deg (clockwise on the y-down page) about its anchor point (ink-left / centre at baseline)."""
    b = line.ink()
    ax = b[0] if anchor == 'left' else (b[0] + b[2]) / 2 if anchor == 'center' else b[2]
    r = math.radians(deg)
    a, bb, c, d = math.cos(r), math.sin(r), -math.sin(r), math.cos(r)
    # page = Rot * (p - (ax, 0)) + (x, y)
    return Placed(line, 0, 0, matrix=(a, bb, c, d, x - a * ax, y - bb * ax))


def placed_ink_poly(p):
    """Approximate page-space ink bounds of a Placed with a matrix (for asserts): returns (x0, y0, x1, y1)."""
    pts = []
    for i, g in enumerate(p.line.glyphs):
        bb = g.bounds()
        if not bb:
            continue
        m = p.per_glyph[i] if p.per_glyph is not None else p.matrix
        for (u, v) in ((bb[0], bb[1]), (bb[2], bb[1]), (bb[0], bb[3]), (bb[2], bb[3])):
            if m is None:
                pts.append((u + p.x, v + p.y))
            else:
                a, b, c, d, e, f = m
                pts.append((a * u + c * v + e, b * u + d * v + f))
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return min(xs), min(ys), max(xs), max(ys)


# --------------------------------------------------------------------------------------------------- stencil
NO_BRIDGE = {'period', 'comma', 'colon', 'semicolon', 'periodcentered', 'periodcentered.case', 'quotesingle',
             'quotedbl', 'quoteright', 'quoteleft', 'space'}


def stencil_rects(p, frac=0.5, gap_em=0.05, lower_xh=False):
    """O CASE stencil bridge (§C.7): one horizontal gap of gap_em at frac of the CAP height through every glyph. For a
    lower-case run (lower_xh=True) the bridge sits at frac of the x-height, where a stencil cutter bridges a, e, o.
    One rect per glyph, so dots and the drawn heart are never cut (a bridged middle dot reads '=', a bridged heart
    reads broken)."""
    rects = []
    for g in p.line.glyphs:
        b = g.bounds()
        if not b or g.ops is not None or g.fc.name(g.gid) in NO_BRIDGE:
            continue
        r = g.run
        ref = (r.fc.xh if lower_xh else r.fc.cap) * r.em / r.fc.upm
        yc = p.y - frac * ref
        h = gap_em * r.em
        if b[1] > -frac * ref + h or b[3] < -frac * ref - h:
            continue                     # the glyph does not reach the bridge line (e.g. º)
        rects.append((p.x + b[0] - 0.05, yc - h / 2, b[2] - b[0] + 0.1, h))
    return rects


# --------------------------------------------------------------------------------------------------- text blocks
def break_words(words, widthf, measure, min_last=2):
    """Balanced ragged-right breaking: minimum squared slack, a bonus for ending a line at a sentence end, a penalty
    for a last line under half the measure, and never a single-word last line (no orphans).
    widthf(list_of_words) -> ink width in mm. Returns list of word lists."""
    n = len(words)
    INF = float('inf')
    best = [INF] * (n + 1)
    nxt = [None] * (n + 1)
    best[n] = 0.0
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            w = widthf(words[i:j])
            if w > measure:
                break
            last = j == n
            if last and (j - i) < min_last and i > 0:
                continue
            if last:
                slack = 0.0 if i == 0 else max(0.0, measure * 0.5 - w) ** 2
            else:
                slack = (measure - w) ** 2
                if words[j - 1].endswith(('.', ';', ':', '·', '—')):
                    slack *= 0.25          # a line that ends a sentence, or at a · / — separator, may be shorter
            cost = slack + best[j]
            if cost < best[i]:
                best[i], nxt[i] = cost, j
    if best[0] == INF:
        lines, cur = [], []
        for w in words:
            if cur and widthf(cur + [w]) > measure:
                lines.append(cur)
                cur = [w]
            else:
                cur.append(w)
        lines.append(cur)
        return lines
    lines, i = [], 0
    while i < n:
        j = nxt[i]
        lines.append(words[i:j])
        i = j
    return lines


UNITS = {'mm', 'cm', 'g', 'h', 'horas', 'minutos', 'kg', 'ml'}


def bind_words(words):
    """Tokens that must never be split across a line: 'nº' + its number, a number + its unit (5 mm, 4 horas,
    200 g), and a separator (· — /) stays at the end of its line rather than starting the next."""
    out = []
    i = 0
    while i < len(words):
        w = words[i]
        if w in ('·', '—', '/', '–') and out:
            out[-1] = out[-1] + ' ' + w
            i += 1
            continue
        if w.lower() in ('nº', 'n.º') and i + 1 < len(words):
            out.append(w + ' ' + words[i + 1])
            i += 2
            continue
        if w[:1].isdigit() and i + 1 < len(words) and words[i + 1].strip('.,;:)(').lower() in UNITS:
            out.append(w + ' ' + words[i + 1])
            i += 2
            continue
        out.append(w)
        i += 1
    return out


def para(text, fc, cap, measure, tracking=0.0, features=None, min_last=2):
    """Return a list of Lines for a paragraph broken to a measure (ink width)."""
    words = bind_words(text.split(' '))
    feats = dict(FIG)
    if features:
        feats.update(features)

    def wf(ws):
        return Line([run_cap(' '.join(ws), fc, cap, tracking, feats)]).ink_width()
    lines = break_words(words, wf, measure, min_last)
    return [Line([run_cap(' '.join(ws), fc, cap, tracking, feats)]) for ws in lines], [' '.join(ws) for ws in lines]


# --------------------------------------------------------------------------------------------------- vector devices
def circle_d(cx, cy, r):
    return (f'M{fmt(cx - r)},{fmt(cy)} A{fmt(r)},{fmt(r)} 0 1,0 {fmt(cx + r)},{fmt(cy)} '
            f'A{fmt(r)},{fmt(r)} 0 1,0 {fmt(cx - r)},{fmt(cy)} Z')


def ellipse_d(cx, cy, rx, ry):
    return (f'M{fmt(cx - rx)},{fmt(cy)} A{fmt(rx)},{fmt(ry)} 0 1,0 {fmt(cx + rx)},{fmt(cy)} '
            f'A{fmt(rx)},{fmt(ry)} 0 1,0 {fmt(cx - rx)},{fmt(cy)} Z')


def rect_d(x, y, w, h):
    return f'M{fmt(x)},{fmt(y)} h{fmt(w)} v{fmt(h)} h{fmt(-w)} Z'


def rrect_d(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return (f'M{fmt(x + r)},{fmt(y)} H{fmt(x + w - r)} A{fmt(r)},{fmt(r)} 0 0 1 {fmt(x + w)},{fmt(y + r)} '
            f'V{fmt(y + h - r)} A{fmt(r)},{fmt(r)} 0 0 1 {fmt(x + w - r)},{fmt(y + h)} H{fmt(x + r)} '
            f'A{fmt(r)},{fmt(r)} 0 0 1 {fmt(x)},{fmt(y + h - r)} V{fmt(y + r)} A{fmt(r)},{fmt(r)} 0 0 1 '
            f'{fmt(x + r)},{fmt(y)} Z')


def foco_d(cx, top, d):
    """O FOCO (§D.3): the lit disc (diameter d) over a flat floor ellipse 2,4d x 0,8d, gap 0,5d. top = disc top."""
    disc = circle_d(cx, top + d / 2, d / 2)
    ell = ellipse_d(cx, top + d + 0.5 * d + 0.4 * d, 1.2 * d, 0.4 * d)
    return disc + ' ' + ell, 2.4 * d, 2.2 * d


def bars_d(x, y, w, h, seed=927):
    """CÓDIGO DE BARRAS FICTÍCIO: a bar block that cannot scan — random module widths that are NOT EAN-quantised,
    no guard patterns, no quiet zone, and a gap pattern that breaks every symbology's start code."""
    r = np.random.default_rng(seed)
    d = []
    xx = x
    while True:
        bw = float(r.choice([0.19, 0.33, 0.46, 0.61, 0.27]))
        gap = float(r.choice([0.21, 0.36, 0.52, 0.29]))
        if xx + bw > x + w:
            break
        d.append(rect_d(xx, y, bw, h))
        xx += bw + gap
    return ' '.join(d)


def bin_icon_d(x, y, s):
    """A plain disposal-bin pictogram (s mm tall): lid bar, handle, tapered body with two ribs. Drawn as outlines so
    it reads at 8 mm. (Generic pictogram; the exact ABNT NBR 16182 artwork was not available — UNVERIFIED.)"""
    u = s / 10.0
    p = []
    p.append(rect_d(x + 1.2 * u, y + 1.4 * u, 7.6 * u, 0.9 * u))           # lid
    p.append(rect_d(x + 3.8 * u, y + 0.5 * u, 2.4 * u, 0.9 * u))           # handle
    # body: trapezoid outline (outer minus inner)
    ox0, ox1, oy0, oy1 = x + 1.8 * u, x + 8.2 * u, y + 2.7 * u, y + 10 * u
    t = 0.75 * u
    outer = (f'M{fmt(ox0)},{fmt(oy0)} L{fmt(ox1)},{fmt(oy0)} L{fmt(ox1 - 0.7 * u)},{fmt(oy1)} '
             f'L{fmt(ox0 + 0.7 * u)},{fmt(oy1)} Z')
    inner = (f'M{fmt(ox0 + t)},{fmt(oy0 + t)} L{fmt(ox0 + 0.7 * u * 0.9 + t * 0.6)},{fmt(oy1 - t)} '
             f'L{fmt(ox1 - 0.7 * u * 0.9 - t * 0.6)},{fmt(oy1 - t)} L{fmt(ox1 - t)},{fmt(oy0 + t)} Z')
    p.append(outer + ' ' + inner)
    for k in (0.38, 0.62):
        cx = ox0 + (ox1 - ox0) * k
        p.append(rect_d(cx - 0.3 * u, oy0 + 1.6 * u, 0.6 * u, 4.6 * u))
    return ' '.join(p)


# --------------------------------------------------------------------------------------------------- textures
def tolex(h, w, ppmm, seed, pebble_mm=0.72):
    """Tolex / levant leatherette grain as a height field 0..1: a dense field of rounded pebbles (cellular: jittered
    seeds every ~0,72 mm, each domed by its distance to the nearest seed) with narrow valleys between them, a slow
    undulation and a fine crinkle. This is what the embossed 120 g/m2 black paper of O CASE looks like under raking
    light."""
    r = ruido.rng(seed)
    step = pebble_mm * ppmm
    gh, gw = int(h / step) + 3, int(w / step) + 3
    jy = (np.arange(gh)[:, None] + 0.5 + r.uniform(-0.42, 0.42, (gh, gw))) * step - step
    jx = (np.arange(gw)[None, :] + 0.5 + r.uniform(-0.42, 0.42, (gh, gw))) * step - step
    seeds = np.ones((h, w), np.uint8)
    yi = np.clip(np.round(jy).astype(int), 0, h - 1)
    xi = np.clip(np.round(jx).astype(int), 0, w - 1)
    seeds[yi, xi] = 0
    dist = cv2.distanceTransform(seeds, cv2.DIST_L2, 5) / step       # 0 at a seed, ~0,5–0,7 at a valley
    size = 0.85 + 0.3 * (ruido.valor(h, w, 3 * step, r) * 0.5 + 0.5)
    peb = np.sqrt(np.clip(1 - (dist / (0.62 * size)) ** 2, 0, 1))
    und = ruido.fractal(h, w, 8 * ppmm, r, 3) * 0.5 + 0.5
    crk = ruido.valor(h, w, 0.18 * ppmm, r) * 0.5 + 0.5
    hgt = 0.78 * peb + 0.14 * und + 0.08 * crk
    hgt = cv2.GaussianBlur(hgt.astype(np.float32), (0, 0), max(0.35, 0.05 * ppmm))
    hgt -= hgt.min()
    hgt /= max(1e-6, hgt.max())
    return hgt


def paper_grain(h, w, ppmm, seed, strength=1.0):
    """Uncoated board: fibre grain + mottle, mean 0, for previews (luminance multiplier around 1)."""
    r = ruido.rng(seed)
    fib = ruido.anisotropico(h, w, 1.6 * ppmm, 0.18 * ppmm, r)
    mot = ruido.fractal(h, w, 6 * ppmm, r, 3)
    fine = ruido.valor(h, w, 0.12 * ppmm, r)
    return strength * (0.012 * fib + 0.018 * mot + 0.010 * fine)


def save16(height01, path):
    arr = np.clip(np.round(height01 * 65535), 0, 65535).astype(np.uint16)
    return R.save_png(arr, path, bits16=True)


def rgba_from(rgb01, alpha01):
    out = np.zeros(rgb01.shape[:2] + (4,), np.uint8)
    out[..., :3] = np.clip(np.round(rgb01 * 255), 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(np.round(alpha01 * 255), 0, 255).astype(np.uint8)
    return out


def hex01(h):
    return R.hex2rgb(T.C.get(h, h)) / 255.0


def raster_paths(w_mm, h_mm, ppmm, paths, rects=()):
    """Coverage of a list of SVG path strings (and rects) on a w x h mm page."""
    doc = R.Doc(w_mm, h_mm, ppmm)
    for d in paths:
        doc.path(d)
    for (x, y, w, h) in rects:
        doc.rect(x, y, w, h)
    return R.rasterise(doc), doc


def crop_save(img, box, path, scale=1.0):
    """debug/preview helper: crop (x0, y0, x1, y1) px and save"""
    from PIL import Image
    im = Image.fromarray(img).crop(box)
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(path)
