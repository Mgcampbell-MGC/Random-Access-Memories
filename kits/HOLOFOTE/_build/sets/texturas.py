"""Procedural textures for the HOLOFOTE sets, drawn in numpy/PIL with fixed seeds (deterministic, regenerable).

Written once into _build/sets/_tex/ (a cache: regenerate, don't commit). Every function returns the PNG path.
    palco_riscos()   tileable 0,5 m scratch height map for the stage lacquer (fine, mostly along X)
    palco_decal()    1,2 m decal centred on the X: R = road-case scuff arcs, G = tape-residue ghost, B = foot-traffic dust
    rugas_cartaz()   paste-wrinkle height map for a placeholder lambe poster
    reboco()         tileable 1 m plaster height/albedo variation for O MURO
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_tex')


def _out(name):
    os.makedirs(TEX, exist_ok=True)
    return os.path.join(TEX, name)


def _save16(arr, path):
    a = np.clip(arr, 0, 1)
    Image.fromarray((a * 65535).astype(np.uint16)).save(path)


def palco_riscos(seed=11, px=4096, tile_m=0.5, force=False):
    """Scratch height map, white = scratch (the shader turns it into grooves). Tileable."""
    path = _out('palco_riscos_%d.png' % seed)
    if os.path.exists(path) and not force:
        return path
    ss = 2
    W = px * ss
    ppm = W / (tile_m * 1000)                       # px per mm at supersample
    rng = np.random.default_rng(seed)
    im = Image.new('L', (W, W), 0)
    d = ImageDraw.Draw(im)

    def line(pts, val, width):
        for ox in (-W, 0, W):
            for oy in (-W, 0, W):
                d.line([(x + ox, y + oy) for x, y in pts], fill=int(val), width=width)

    # 1. road-case drag scratches: long, mostly along X (stage left-right), slightly curved
    for _ in range(1400):
        L = float(np.clip(rng.lognormal(math.log(45), 0.8), 6, 320)) * ppm
        ang = rng.normal(0, 0.14) if rng.random() < 0.7 else rng.uniform(0, math.pi)
        x0, y0 = rng.uniform(0, W, 2)
        bend = rng.normal(0, 0.06)
        n = 5
        pts = []
        for i in range(n + 1):
            t = i / n
            a = ang + bend * (t - 0.5)
            pts.append((x0 + math.cos(a) * L * t, y0 + math.sin(a) * L * t))
        line(pts, rng.uniform(70, 255), int(rng.choice([1, 1, 2, 2, 3])))
    # 2. micro-scratch satin: thousands of short random hairlines, faint
    for _ in range(26000):
        L = rng.uniform(0.8, 7.0) * ppm
        a = rng.uniform(0, math.pi)
        x0, y0 = rng.uniform(0, W, 2)
        line([(x0, y0), (x0 + math.cos(a) * L, y0 + math.sin(a) * L)], rng.uniform(25, 90), 1)
    im = im.resize((px, px), Image.BOX)
    im.save(path)
    return path


def palco_decal(seed=5, px=2048, size_m=1.2, arcs=None, residue=None, force=False):
    """Decal centred on the floor mark (the X centre). Coordinates in metres, +X right, +Y away from camera.
    arcs: [(cx, cy, radius, a0_deg, a1_deg, width_m)]  residue: (cx, cy, w, h, rot_deg)"""
    arcs = arcs or [(-0.36, -0.30, 0.40, 18, 74, 0.030),     # sweeps through the front-left gap of the X
                    (0.52, 0.30, 0.47, 200, 236, 0.026)]     # crosses the pool's right edge, behind the X arm
    residue = residue or (0.118, -0.050, 0.048, 0.160, 74.0)
    key = 'palco_decal_%d_%s.png' % (seed, abs(hash((tuple(arcs), residue))) % 10 ** 8)
    path = _out(key)
    if os.path.exists(path) and not force:
        return path
    rng = np.random.default_rng(seed)
    ys, xs = np.mgrid[0:px, 0:px]
    X = (xs + 0.5) / px * size_m - size_m / 2
    Y = size_m / 2 - (ys + 0.5) / px * size_m        # image top = +Y (away from camera)
    R = np.zeros((px, px), np.float32)
    for (cx, cy, r, a0, a1, w) in arcs:
        dx, dy = X - cx, Y - cy
        rr = np.hypot(dx, dy)
        ang = np.degrees(np.arctan2(dy, dx)) % 360
        lo, hi = a0 % 360, a1 % 360
        if lo <= hi:
            inside = (ang >= lo) & (ang <= hi)
            t = np.clip((ang - lo) / max(hi - lo, 1e-3), 0, 1)
        else:
            inside = (ang >= lo) | (ang <= hi)
            t = np.clip(((ang - lo) % 360) / max((hi - lo) % 360, 1e-3), 0, 1)
        fade = np.sin(np.pi * t) ** 0.6 * inside
        m = np.zeros_like(R)
        for k in range(9):                       # a band of streaks, the wheel's tread and grit
            off = rng.normal(0, w * 0.32)
            sw = rng.uniform(0.0012, 0.0055)
            amp = rng.uniform(0.25, 1.0)
            ph = rng.uniform(0, 6.28)
            gaps = 0.55 + 0.45 * np.sin(ang * rng.uniform(0.6, 2.4) + ph)
            m = np.maximum(m, amp * np.exp(-((rr - r - off) / sw) ** 2) * np.clip(gaps, 0, 1))
        R = np.maximum(R, m * fade)
    G = np.zeros((px, px), np.float32)
    cx, cy, w, h, rot = residue
    a = math.radians(rot)
    u = (X - cx) * math.cos(a) + (Y - cy) * math.sin(a)
    v = -(X - cx) * math.sin(a) + (Y - cy) * math.cos(a)
    # ragged torn ends along u, straight factory edges along v
    jag = 0.0015 * np.sin(v * 2900) + 0.0012 * np.sin(v * 1700 + 1.0)
    du = np.abs(u) - (h / 2 + jag)
    dv = np.abs(v) - w / 2
    dist = np.maximum(du, dv)
    body = np.clip(-dist / 0.002, 0, 1)
    edge = np.exp(-(dist / 0.0011) ** 2)          # adhesive ridge that holds dust
    G = np.clip(0.55 * body + 0.9 * edge, 0, 1).astype(np.float32)
    # patchy: residue missing in places
    n = Image.fromarray((rng.random((px // 32, px // 32)) * 255).astype(np.uint8)).resize((px, px), Image.BICUBIC)
    G *= np.clip(np.asarray(n, np.float32) / 255 * 1.6 - 0.15, 0.2, 1)
    # B: foot-traffic dust, low frequency, heavier downstage (toward camera)
    n1 = Image.fromarray((rng.random((24, 24)) * 255).astype(np.uint8)).resize((px, px), Image.BICUBIC)
    n2 = Image.fromarray((rng.random((96, 96)) * 255).astype(np.uint8)).resize((px, px), Image.BICUBIC)
    n1 = n1.filter(ImageFilter.GaussianBlur(px / 40))
    n2 = n2.filter(ImageFilter.GaussianBlur(px / 160))
    B = 0.65 * np.asarray(n1, np.float32) / 255 + 0.35 * np.asarray(n2, np.float32) / 255
    B = (B - B.min()) / (B.max() - B.min() + 1e-6)
    B = np.clip((B - 0.35) * 1.8, 0, 1) * np.clip(0.6 - Y * 0.6, 0.2, 1)
    rgb = np.dstack([R, G, B])
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), 'RGB').save(path)
    return path


def rugas_cartaz(seed=3, w=1024, h=1448, force=False):
    """Paste wrinkles for a placeholder poster: long creases, a few bubbles, a brush-ridge field. 16-bit, 0.5 = flat."""
    path = _out('rugas_%d_%dx%d.png' % (seed, w, h))
    if os.path.exists(path) and not force:
        return path
    rng = np.random.default_rng(seed)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    hgt = np.zeros((h, w), np.float32)
    diag = math.hypot(w, h)
    for _ in range(rng.integers(5, 9)):            # creases: ridges along random lines, fading along their length
        x0, y0 = rng.uniform(0, w), rng.uniform(0, h)
        a = rng.uniform(0, math.pi)
        nx, ny = -math.sin(a), math.cos(a)
        dperp = (xs - x0) * nx + (ys - y0) * ny
        dpar = (xs - x0) * math.cos(a) + (ys - y0) * math.sin(a)
        L = rng.uniform(0.15, 0.55) * diag
        width = rng.uniform(2.5, 7.0)
        prof = np.exp(-(dperp / width) ** 2) - 0.45 * np.exp(-(dperp / (width * 2.6)) ** 2)
        hgt += rng.uniform(0.5, 1.0) * prof * np.exp(-(dpar / L) ** 2)
    for _ in range(rng.integers(3, 7)):            # air bubbles
        x0, y0 = rng.uniform(0.05, 0.95) * w, rng.uniform(0.05, 0.95) * h
        rx, ry = rng.uniform(12, 45), rng.uniform(8, 30)
        a = rng.uniform(0, math.pi)
        u = ((xs - x0) * math.cos(a) + (ys - y0) * math.sin(a)) / rx
        v = (-(xs - x0) * math.sin(a) + (ys - y0) * math.cos(a)) / ry
        hgt += rng.uniform(0.6, 1.2) * np.clip(1 - u * u - v * v, 0, 1) ** 0.7
    n = Image.fromarray((rng.random((h // 40 + 2, w // 40 + 2)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    hgt += 0.25 * (np.asarray(n, np.float32) / 255 - 0.5)
    brush = np.sin(ys / h * rng.uniform(40, 70) + 2.0 * np.sin(xs / w * 6.0)) * 0.04
    hgt += brush
    hgt = (hgt - hgt.min()) / (hgt.max() - hgt.min() + 1e-6)
    _save16(hgt, path)
    return path


def reboco(seed=2, px=2048, force=False):
    """Plaster: R = height (chapisco grain + trowel swirls), G = stain/dirt, B = paint wear. Tileable 1 m."""
    path = _out('reboco_%d.png' % seed)
    if os.path.exists(path) and not force:
        return path
    rng = np.random.default_rng(seed)

    def tile_noise(cells, smooth=Image.BICUBIC):
        a = rng.random((cells, cells))
        a = np.pad(a, 3, mode='wrap')
        im = Image.fromarray((a * 255).astype(np.uint8)).resize(((cells + 6) * px // cells,) * 2, smooth)
        o = 3 * px // cells
        return np.asarray(im, np.float32)[o:o + px, o:o + px] / 255

    grain = 0.45 * tile_noise(512) + 0.35 * tile_noise(256) + 0.2 * tile_noise(96)
    swirl = tile_noise(14)
    hgt = 0.75 * grain + 0.25 * swirl
    stain = tile_noise(8) * 0.7 + tile_noise(40) * 0.3
    # vertical streaks of rain dirt
    cols = rng.random(px)
    cols = np.convolve(np.pad(cols, 20, mode='wrap'), np.ones(21) / 21, 'same')[20:-20]
    streak = np.tile(cols[None, :], (px, 1)) * (0.6 + 0.4 * tile_noise(6))
    stain = np.clip(0.6 * stain + 0.5 * (streak - 0.5) + 0.2, 0, 1)
    wear = np.clip((tile_noise(20) - 0.62) * 4, 0, 1)
    rgb = np.dstack([hgt, stain, wear])
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), 'RGB').save(path)
    return path
