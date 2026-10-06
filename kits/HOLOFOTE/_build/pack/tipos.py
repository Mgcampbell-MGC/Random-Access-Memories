"""HOLOFOTE pack typesetting core (platform §C, §D.2).

Every printed letter on the pack is set here: HarfBuzz shapes the text on the OFFICIAL font files in _build/fonts at the
exact variation coordinates, outlines come straight from the font (no rasterised font engine in between), and every
position is in MILLIMETRES on a y-down page. Lines are measured and fitted on INK edges (the first glyph's left ink edge
and the last glyph's right ink edge), which is what a senior designer means by "fills the measure".

Units: mm everywhere. A face's em size is derived from the platform's cap / x-height / figure height using the metrics
measured on the files: Special Gothic cap 710 (figures 710), Condensed One x-height 509, Shantell x-height 485 (OS/2).
Tracking is in 1/1000 em, applied after every glyph except the last one of a line.
"""
import os
import math
from functools import lru_cache

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import RecordingPen

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
FONTDIR = os.path.join(BUILD, 'fonts')
FILES = {
    'XP': 'SpecialGothicExpandedOne-Regular.ttf',
    'CN': 'SpecialGothicCondensedOne-Regular.ttf',
    'SG': 'SpecialGothic-VF.ttf',
    'SH': 'ShantellSans-VF.ttf',
}
# Shantell print setting, platform §C.2 / §D.2: wght 500, INFM 60, BNCE 0
SHANTELL = {'wght': 500, 'INFM': 60, 'BNCE': 0, 'SPAC': 0}

C = dict(preto='#121014', papel='#FFF8EC', amarelo='#FFE81A', rosa='#FF4FA0', laranja='#FF6A1A',
         violeta='#8424F5', luz='#FFE9C4', cera='#F3E9D6', croma='#0047BB')


def fmt(v):
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


class Face:
    """One font instance (file + variation coordinates)."""
    _cache = {}

    def __new__(cls, key, **var):
        k = (key, tuple(sorted(var.items())))
        if k in cls._cache:
            return cls._cache[k]
        self = super().__new__(cls)
        cls._cache[k] = self
        self.key, self.var = key, dict(var)
        path = os.path.join(FONTDIR, FILES[key])
        self.path = path
        blob = hb.Blob.from_file_path(path)
        self.hbface = hb.Face(blob)
        self.font = hb.Font(self.hbface)
        if var:
            self.font.set_variations(var)
        self.upm = self.hbface.upem
        self.cap = 700 if key == 'SH' else 710
        self.xh = {'CN': 509, 'SH': 485, 'XP': 514, 'SG': 504}[key]
        self._outlines = {}
        self._ext = {}
        return self

    def __init__(self, key, **var):
        pass

    def __repr__(self):
        return f'Face({self.key},{self.var})'

    # sizes
    def em_from_cap(self, cap_mm):
        return cap_mm * self.upm / self.cap

    def em_from_xh(self, xh_mm):
        return xh_mm * self.upm / self.xh

    def outline(self, gid):
        if gid not in self._outlines:
            rp = RecordingPen()
            self.font.draw_glyph_with_pen(gid, rp)
            self._outlines[gid] = rp.value
        return self._outlines[gid]

    def extents(self, gid):
        if gid not in self._ext:
            e = self.font.get_glyph_extents(gid)
            self._ext[gid] = None if (e is None or e.width == 0) else (e.x_bearing, e.y_bearing + e.height,
                                                                       e.x_bearing + e.width, e.y_bearing)
        return self._ext[gid]  # xmin, ymin, xmax, ymax in font units (y up)

    def gid(self, ch):
        return self.font.get_nominal_glyph(ord(ch))

    def name(self, gid):
        return self.font.get_glyph_name(gid)

    def shape(self, text, features):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, features)
        return [(i.codepoint, i.cluster, p.x_advance, p.x_offset, p.y_offset)
                for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


def face(key, **var):
    if key == 'SH' and not var:
        var = SHANTELL
    return Face(key, **var)


# --------------------------------------------------------------------------------------------------------------------
# The heart: Special Gothic has no ♥ (platform §C.10, §D.2). It is drawn here as a code vector glyph that takes the
# rhythm of the face it sits in: cap height (with the round overshoot of O, -12..722) and a width equal to the 'O'
# ink width of the same instance, with the O's side bearings. So it condenses with wdth like the letters do.
HEART_UNIT = [  # unit box, y up; bottom point at (0.5, 0)
    ('moveTo', (0.5, 0.0)),
    ('curveTo', (0.40, 0.10), (0.0, 0.36), (0.0, 0.67)),
    ('curveTo', (0.0, 0.88), (0.14, 1.0), (0.28, 1.0)),
    ('curveTo', (0.39, 1.0), (0.47, 0.94), (0.5, 0.835)),
    ('curveTo', (0.53, 0.94), (0.61, 1.0), (0.72, 1.0)),
    ('curveTo', (0.86, 1.0), (1.0, 0.88), (1.0, 0.67)),
    ('curveTo', (1.0, 0.36), (0.60, 0.10), (0.5, 0.0)),
    ('closePath',),
]
HEART = '♥'


def heart_metrics(fc):
    o = fc.gid('O')
    ex = fc.extents(o)
    adv = fc.font.get_glyph_h_advance(o)
    w = (ex[2] - ex[0])
    return dict(lsb=ex[0], w=w, adv=adv, ymin=-12, ymax=722)


def heart_ops(fc):
    m = heart_metrics(fc)
    ops = []
    for op in HEART_UNIT:
        if op[0] == 'closePath':
            ops.append(('closePath', ()))
            continue
        pts = [(m['lsb'] + x * m['w'], m['ymin'] + y * (m['ymax'] - m['ymin'])) for x, y in op[1:]]
        ops.append((op[0], tuple(pts)))
    return ops, (m['lsb'], m['ymin'], m['lsb'] + m['w'], m['ymax']), m['adv']


# --------------------------------------------------------------------------------------------------------------------
class Run:
    """A piece of text in one face at one size. size = em in mm."""

    def __init__(self, text, fc, em, tracking=0.0, features=None, tag='ink'):
        self.text, self.fc, self.em, self.tracking, self.tag = text, fc, em, tracking, tag
        f = {'kern': True}
        if features:
            f.update(features)
        self.features = f


def run_cap(text, fc, cap_mm, tracking=0.0, features=None, tag='ink'):
    return Run(text, fc, fc.em_from_cap(cap_mm), tracking, features, tag)


def run_xh(text, fc, xh_mm, tracking=0.0, features=None, tag='ink'):
    return Run(text, fc, fc.em_from_xh(xh_mm), tracking, features, tag)


CAPS = {'case': True, 'tnum': True}   # caps setting: case forms (raised · « » - etc.) and tabular figures
FIG = {'tnum': True}


class Glyph:
    __slots__ = ('fc', 'gid', 'x', 'y', 'em', 'ops', 'ext', 'tag', 'run')

    def __init__(self, fc, gid, x, y, em, ops=None, ext=None, tag='ink', run=None):
        self.fc, self.gid, self.x, self.y, self.em = fc, gid, x, y, em
        self.ops, self.ext, self.tag, self.run = ops, ext, tag, run

    def bounds(self):
        """ink bounds in mm, relative to the line origin, y DOWN (baseline at 0)."""
        ext = self.ext if self.ext is not None else self.fc.extents(self.gid)
        if ext is None:
            return None
        s = self.em / self.fc.upm
        return (self.x + ext[0] * s, self.y - ext[3] * s, self.x + ext[2] * s, self.y - ext[1] * s)


class Line:
    """Runs on one baseline. Layout gives glyph positions in mm relative to the pen origin (0, 0 = baseline)."""

    def __init__(self, runs):
        self.runs = runs if isinstance(runs, list) else [runs]
        self.layout()

    def layout(self):
        gl = []
        x = 0.0
        nr = len(self.runs)
        for ri, r in enumerate(self.runs):
            s = r.em / r.fc.upm
            parts = r.text.split(HEART) if HEART in r.text else [r.text]
            for pi, part in enumerate(parts):
                if part:
                    for gid, cl, adv, xo, yo in r.fc.shape(part, r.features):
                        gl.append(Glyph(r.fc, gid, x + xo * s, -yo * s, r.em, tag=r.tag, run=r))
                        x += adv * s + r.tracking / 1000.0 * r.em
                if pi < len(parts) - 1:   # a heart goes here
                    ops, ext, adv = heart_ops(r.fc)
                    gl.append(Glyph(r.fc, -1, x, 0.0, r.em, ops=ops, ext=ext, tag=r.tag, run=r))
                    x += adv * s + r.tracking / 1000.0 * r.em
        # remove the trailing tracking of the very last glyph
        if self.runs:
            r = self.runs[-1]
            x -= r.tracking / 1000.0 * r.em
        self.glyphs = gl
        self.advance = x

    def ink(self):
        bs = [g.bounds() for g in self.glyphs]
        bs = [b for b in bs if b]
        if not bs:
            return (0, 0, 0, 0)
        return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))

    def ink_width(self):
        b = self.ink()
        return b[2] - b[0]

    def ngaps(self):
        return max(0, len(self.glyphs) - 1)


# --------------------------------------------------------------------------------------------------------------------
# Fitting. All solvers return a new Line plus what they solved, and are exact to well under 0,5 px at 40 px/mm.
def set_tracking(runs, tr):
    for r in runs:
        r.tracking = tr
    return Line(runs)


def fit_tracking(runs, measure, lo=-60, hi=400):
    """Solve one tracking value (1/1000 em) shared by all runs so the ink width equals measure. Ink width is linear
    in tracking, so one secant step is exact; a second refines float noise."""
    a = set_tracking(runs, 0.0)
    w0 = a.ink_width()
    b = set_tracking(runs, 100.0)
    w1 = b.ink_width()
    tr = 100.0 * (measure - w0) / (w1 - w0) if w1 != w0 else 0.0
    tr = max(lo, min(hi, tr))
    ln = set_tracking(runs, tr)
    return ln, tr


def fit_size(make, measure, lo=0.1, hi=200.0, tol=1e-5):
    """make(size) -> Line; ink width is monotonic in size. Bisection."""
    for _ in range(100):
        mid = (lo + hi) / 2
        w = make(mid).ink_width()
        if abs(w - measure) < tol:
            break
        if w > measure:
            hi = mid
        else:
            lo = mid
    return make(mid), mid


def fit_axis(make, measure, lo, hi, tol=1e-5):
    """make(value) -> Line, ink width increasing in value (e.g. wdth). Largest value whose width <= measure."""
    if make(lo).ink_width() > measure:
        return None, None
    if make(hi).ink_width() <= measure:
        return make(hi), hi
    for _ in range(80):
        mid = (lo + hi) / 2
        w = make(mid).ink_width()
        if w > measure:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return make(lo), lo


# --------------------------------------------------------------------------------------------------------------------
# Placement and SVG output.
class Placed:
    """A Line placed on the page: x = pen origin (mm), y = baseline (mm, y down). Optional affine (a,b,c,d,e,f) maps
    line coordinates (mm, y down) to page coordinates, for rotated or curved text."""

    def __init__(self, line, x, y, fill='#000', name='', matrix=None, per_glyph=None):
        self.line, self.x, self.y, self.fill, self.name = line, x, y, fill, name
        self.matrix = matrix
        self.per_glyph = per_glyph  # optional list of matrices, one per glyph (curved text)

    def ink(self):
        b = self.line.ink()
        return (b[0] + self.x, b[1] + self.y, b[2] + self.x, b[3] + self.y)


def place_left(line, x, y, **kw):
    """ink-left edge at x"""
    b = line.ink()
    return Placed(line, x - b[0], y, **kw)


def place_right(line, x, y, **kw):
    b = line.ink()
    return Placed(line, x - b[2], y, **kw)


def place_center(line, x, y, **kw):
    b = line.ink()
    return Placed(line, x - (b[0] + b[2]) / 2, y, **kw)


def glyph_path(g, ox, oy, matrix=None):
    """SVG path data for one glyph, in page mm. matrix maps (line-relative mm, y down) -> page."""
    s = g.em / g.fc.upm
    # font units (y up) -> line mm (y down): (s, 0, 0, -s, g.x, g.y)
    if matrix is None:
        t = (s, 0, 0, -s, g.x + ox, g.y + oy)
    else:
        a, b, c, d, e, f = matrix
        # page = M * (line) where line = (s*u + gx, -s*v + gy)   (u, v font units)
        t = (a * s, b * s, -c * s, -d * s, a * g.x + c * g.y + e, b * g.x + d * g.y + f)
    sp = SVGPathPen(None, ntos=fmt)
    tp = TransformPen(sp, t)
    ops = g.ops if g.ops is not None else g.fc.outline(g.gid)
    for op, args in ops:
        if op == 'closePath':
            tp.closePath()
        elif op == 'endPath':
            tp.endPath()
        else:
            getattr(tp, op)(*args)
    return sp.getCommands()


def placed_paths(p):
    out = []
    for i, g in enumerate(p.line.glyphs):
        if g.ops is None and g.fc.extents(g.gid) is None:
            continue  # spaces
        if p.per_glyph is not None:
            d = glyph_path(g, 0, 0, p.per_glyph[i])
        elif p.matrix is not None:
            a, b, c, d_, e, f = p.matrix
            # translate inside: line coords offset by (p.x, p.y) then matrix
            m = (a, b, c, d_, a * p.x + c * p.y + e, b * p.x + d_ * p.y + f)
            d = glyph_path(g, 0, 0, m)
        else:
            d = glyph_path(g, p.x, p.y)
        if d:
            out.append(d)
    return ' '.join(out)


def rotation(deg, cx=0.0, cy=0.0):
    """affine rotating by deg (clockwise on a y-down page) about (cx, cy)"""
    r = math.radians(deg)
    a, b, c, d = math.cos(r), math.sin(r), -math.sin(r), math.cos(r)
    return (a, b, c, d, cx - a * cx - c * cy, cy - b * cx - d * cy)


def compose(m1, m2):
    """m1 after m2 (apply m2 first)"""
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return (a1 * a2 + c1 * b2, b1 * a2 + d1 * b2, a1 * c2 + c1 * d2, b1 * c2 + d1 * d2,
            a1 * e2 + c1 * f2 + e1, b1 * e2 + d1 * f2 + f1)


def stencil_bands(p, frac=0.5, gap_em=0.05):
    """O CASE stencil: one horizontal gap of gap_em at frac of cap height through every glyph (§C.7). Returns rects
    (x, y, w, h) in page mm, one per run, spanning that run's ink, to be cut out of the ink by a mask."""
    rects = []
    for r in p.line.runs:
        gs = [g for g in p.line.glyphs if g.run is r and g.bounds()]
        if not gs:
            continue
        bs = [g.bounds() for g in gs]
        capmm = r.em * r.fc.cap / r.fc.upm
        yc = p.y - frac * capmm
        h = gap_em * r.em
        x0 = min(b[0] for b in bs) + p.x - 0.5
        x1 = max(b[2] for b in bs) + p.x + 0.5
        rects.append((x0, yc - h / 2, x1 - x0, h))
    return rects
