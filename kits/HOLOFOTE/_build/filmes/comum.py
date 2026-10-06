"""HOLOFOTE · films: shared paths, colour maths and image I/O (pure numpy + OpenCV, web venv).

Colour: every plate is a Khronos PBR Neutral render at exposure -3,0 (the director's transform). To RELIGHT a plate in
2D (the CLAC filament warm-up, the flame's gain in the blackout) the display value is taken back to scene-linear with
the EXACT analytic inverse of PBR Neutral, multiplied there (light is additive and linear in scene space), and sent
forward again. That is a light change, not a brightness filter.
"""
import os, json, math
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..'))
KIT = os.path.abspath(os.path.join(B, '..'))
RENDER = os.path.join(HERE, '_render')            # our 3D frames and crops (git-ignored)
CACHE = os.path.join(HERE, 'cache')               # type layers (git-ignored)
QUADROS = os.path.join(HERE, '_quadros')          # PNG frames before encoding (git-ignored, deleted after)
FILMES = os.path.join(KIT, '04_FILMES')
SOM = os.path.join(FILMES, 'som', 'filmes')
PROD = os.path.join(KIT, '06_PRODUCAO')
FID = os.path.join(PROD, 'fidelidade')
RENDERS = os.path.join(KIT, '02_PRODUTO', 'renders')
AOV_KV = os.path.join(B, 'shots', 'aov')
MASTER = os.path.join(KIT, '02_PRODUTO', 'rotulos', 'HLF-02_ROTULO_wrap.png')
WEB = '/home/user/venvs/web/bin/python'
W, H = 1080, 1920
FPS = 24

HEX = dict(preto='#121014', papel='#FFF8EC', amarelo='#FFE81A')


# ------------------------------------------------------------------------------------------------ I/O
def ler(path):
    """PNG (8 or 16 bit) -> float32 RGB 0..1 (display-referred sRGB)."""
    a = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if a is None:
        raise FileNotFoundError(path)
    if a.ndim == 3 and a.shape[2] == 4:
        a = a[..., :3]
    div = 65535.0 if a.dtype == np.uint16 else 255.0
    return a[..., ::-1].astype(np.float32) / div


def ler_rgba(path):
    a = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if a is None:
        raise FileNotFoundError(path)
    div = 65535.0 if a.dtype == np.uint16 else 255.0
    a = a.astype(np.float32) / div
    if a.shape[2] == 3:
        a = np.dstack([a, np.ones(a.shape[:2], np.float32)])
    return a[..., [2, 1, 0, 3]]


def ao_formato(img):
    """A plate rendered supersampled (e.g. motor.still pct=200) is area-averaged to the film's 1080 x 1920."""
    if img.shape[:2] == (H, W):
        return img
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)


def salvar(path, rgb01):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    a = (np.clip(rgb01, 0, 1) * 255.0 + 0.5).astype(np.uint8)
    cv2.imwrite(path, a[..., ::-1], [cv2.IMWRITE_PNG_COMPRESSION, 1])


# ------------------------------------------------------------------------------------------------ colour
def s2l(v):
    v = np.asarray(v, np.float32)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4).astype(np.float32)


def l2s(v):
    v = np.clip(np.asarray(v, np.float32), 0, None)
    return np.where(v <= 0.0031308, v * 12.92, 1.055 * np.power(v, 1 / 2.4) - 0.055).astype(np.float32)


F0 = 0.04
START = 0.8 - F0
DESAT = 0.15
DD = 1.0 - START


def pbr(c):
    """Khronos PBR Neutral, scene-linear -> display-linear (the same formula as sets/medir.py)."""
    c = np.asarray(c, np.float32)
    x = c.min(axis=-1, keepdims=True)
    off = np.where(x < 2 * F0, x - 6.25 * x * x, F0)
    c = c - off
    peak = c.max(axis=-1, keepdims=True)
    npk = 1.0 - DD * DD / (peak + DD - START)
    safe = np.where(peak > 0, peak, 1.0)
    g = 1.0 - 1.0 / (DESAT * (peak - npk) + 1.0)
    comp = c * (npk / safe) * (1 - g) + npk * g
    return np.where(peak < START, c, comp).astype(np.float32)


def pbr_inv(o):
    """Exact inverse of pbr() (display-linear -> scene-linear)."""
    o = np.clip(np.asarray(o, np.float32), 0, 0.99999)
    npk = o.max(axis=-1, keepdims=True)
    comp = npk >= START
    p = DD * DD / (1.0 - npk) - DD + START
    g = 1.0 - 1.0 / (DESAT * (p - npk) + 1.0)
    cc = (o - g * npk) / np.maximum(1 - g, 1e-6) * (p / np.maximum(npk, 1e-6))
    c = np.where(comp, cc, o)
    m = c.min(axis=-1, keepdims=True)              # = min(x) - offset(min(x))
    xm = np.where(m < 0.04, np.sqrt(np.clip(m, 0, None) / 6.25), m + F0)
    off = np.where(xm < 2 * F0, xm - 6.25 * xm * xm, F0)
    return (c + off).astype(np.float32)


def para_cena(rgb01):
    return pbr_inv(s2l(rgb01))


def para_tela(scene):
    return l2s(pbr(np.clip(scene, 0, None)))


def kelvin_rgb(k):
    """Blackbody colour (linear Rec.709, luminance 1) by Planck's law integrated against the CIE 1931 2-degree
    observer (Wyman, Sloan & Shirley 2013 multi-lobe fit)."""
    lam = np.arange(380, 781, 5, dtype=np.float64)

    def g(x, mu, s1, s2):
        return np.exp(-0.5 * ((x - mu) / np.where(x < mu, s1, s2)) ** 2)
    xb = 1.056 * g(lam, 599.8, 37.9, 31.0) + 0.362 * g(lam, 442.0, 16.0, 26.7) - 0.065 * g(lam, 501.1, 20.4, 26.2)
    yb = 0.821 * g(lam, 568.8, 46.9, 40.5) + 0.286 * g(lam, 530.9, 16.3, 31.1)
    zb = 1.217 * g(lam, 437.0, 11.8, 36.0) + 0.681 * g(lam, 459.0, 26.0, 13.8)
    l = lam * 1e-9
    pl = 1.0 / (l ** 5 * (np.exp(1.4388e-2 / (l * k)) - 1.0))
    X, Y, Z = (pl * xb).sum(), (pl * yb).sum(), (pl * zb).sum()
    M = np.array([[3.2404542, -1.5371385, -0.4985314], [-0.9692660, 1.8760108, 0.0415560], [0.0556434, -0.2040259, 1.0572252]])
    rgb = M @ np.array([X, Y, Z]) / Y
    return np.clip(rgb, 1e-4, None)


def tinta_quente(kelvin, balance=3300.0):
    """The colour a blackbody at `kelvin` records through a camera balanced for `balance` (von Kries, luminance 1):
    the same 'balanced' convention as sets_lib.balanced()."""
    a, b = kelvin_rgb(kelvin), kelvin_rgb(balance)
    c = a / b
    lum = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    return (c / lum).astype(np.float32)


# ------------------------------------------------------------------------------------------------ compositing
def sobre(fundo, rgba, dx=0.0, dy=0.0, blur=0.0):
    """Straight-alpha RGBA layer over an RGB image, in display sRGB (as the browser composites the KV type over its plate).
    dx/dy translate the layer (sub-pixel); blur = vertical motion-blur length in px (a 180-degree shutter on a fly-out)."""
    a = rgba[..., 3:4]
    pm = np.concatenate([rgba[..., :3] * a, a], axis=-1)
    if dx or dy:
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        pm = cv2.warpAffine(pm, M, (pm.shape[1], pm.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    if blur and blur > 1.0:
        n = int(round(blur))
        k = np.ones((n, 1), np.float32) / n
        pm = cv2.filter2D(pm, -1, k, borderType=cv2.BORDER_CONSTANT)
    return fundo * (1 - pm[..., 3:4]) + pm[..., :3]


def empurrar_M(s, centro):
    """2x3 affine of a 2D dolly push: scale s about `centro` (x, y)."""
    cx, cy = centro
    return np.float32([[s, 0, cx * (1 - s)], [0, s, cy * (1 - s)]])


def empurrar(img, s, centro, interp=cv2.INTER_CUBIC):
    if abs(s - 1.0) < 1e-6:
        return img
    return cv2.warpAffine(img, empurrar_M(s, centro), (img.shape[1], img.shape[0]), flags=interp,
                          borderMode=cv2.BORDER_REPLICATE)


def mascara_caixa(h, w, pena):
    """Feathered rectangle mask (1 inside, ramps to 0 over `pena` px at the edges)."""
    y = np.minimum(np.arange(h), np.arange(h)[::-1]).astype(np.float32)
    x = np.minimum(np.arange(w), np.arange(w)[::-1]).astype(np.float32)
    m = np.minimum(y[:, None], x[None, :])
    m = np.clip((m - 2) / max(pena, 1), 0, 1)
    return (m * m * (3 - 2 * m))[..., None]


_CENTRO = {}


def centro_push(aov_path=None):
    """Centre of the 2D dolly push on the KV-45 plate: x 540 and 90 px below the top of the print (the label's upper
    half), read from the plate's own label AOV so it follows any re-framing of KV-45. The flame keeps clear of the type."""
    aov_path = aov_path or os.path.join(AOV_KV, 'KV-45_aceso', '0001.exr')
    if aov_path not in _CENTRO:
        import OpenEXR
        ch = OpenEXR.File(aov_path).parts[0].channels
        m = next(v.pixels for k, v in ch.items() if k.split('.')[0] == 'label_mask')
        m = m[..., 0] if m.ndim == 3 else m
        k = m.shape[0] / H                        # a supersampled AOV (pct 200) is measured in film pixels
        ys = np.nonzero((m > 0.5).any(axis=1))[0]
        _CENTRO[aov_path] = (540.0, float(ys.min()) / k + 90.0)
    return _CENTRO[aov_path]
