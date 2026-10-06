"""Colour measurement for the HOLOFOTE sets: sRGB <-> linear, Khronos PBR Neutral, CIEDE2000, patch stats.

Pure numpy (works in the Blender venv and the web venv). Used by calibrar.py and the set tests to check that a
coating reads at its faixa hex in the lit area, and by the LOJA compositor.
"""
import numpy as np

FAIXA_HEX = {'01': '#FF4FA0', '02': '#FFE81A', '03': '#FF6A1A', '04': '#8424F5'}
PAPEL = '#FFF8EC'


def hex_rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float64) / 255.0


def srgb_to_lin(v):
    v = np.asarray(v, np.float64)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(v):
    v = np.clip(np.asarray(v, np.float64), 0, None)
    return np.where(v <= 0.0031308, v * 12.92, 1.055 * np.power(v, 1 / 2.4) - 0.055)


def pbr_neutral(c):
    """Khronos PBR Neutral tone mapper (scene-linear Rec.709 in, display-linear out). c: (..., 3)."""
    c = np.asarray(c, np.float64)
    F0 = 0.04
    start = 0.8 - F0
    desat = 0.15
    x = c.min(axis=-1, keepdims=True)
    offset = np.where(x < 2 * F0, x - 6.25 * x * x, F0)
    c = c - offset
    peak = c.max(axis=-1, keepdims=True)
    d = 1.0 - start
    new_peak = 1.0 - d * d / (peak + d - start)
    safe = np.where(peak > 0, peak, 1.0)
    cc = c * (new_peak / safe)
    g = 1.0 - 1.0 / (desat * (peak - new_peak) + 1.0)
    comp = cc * (1 - g) + new_peak * g
    return np.where(peak < start, c, comp)


def display(scene_lin, exposure=-3.0):
    """Scene-linear radiance -> 0..1 sRGB display value, the way the sets are rendered."""
    return lin_to_srgb(pbr_neutral(np.asarray(scene_lin) * 2.0 ** exposure))


# ------------------------------------------------------------------------------------------------ CIE Lab / dE00
def _xyz(rgb_lin):
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    return rgb_lin @ M.T


def lab(srgb01):
    xyz = _xyz(srgb_to_lin(srgb01)) / np.array([0.95047, 1.0, 1.08883])
    e = 216 / 24389
    k = 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], -1)


def de2000(lab1, lab2):
    L1, a1, b1 = np.moveaxis(np.asarray(lab1, np.float64), -1, 0)
    L2, a2, b2 = np.moveaxis(np.asarray(lab2, np.float64), -1, 0)
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    dh = h2p - h1p
    dh = np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh))
    dh = np.where(C1p * C2p == 0, 0, dh)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2))
    Lbp = (L1 + L2) / 2
    Cbp = (C1p + C2p) / 2
    hs = h1p + h2p
    hbp = np.where(np.abs(h1p - h2p) > 180, (hs + 360) / 2, hs / 2)
    hbp = np.where(C1p * C2p == 0, hs, hbp)
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dth = 30 * np.exp(-((hbp - 275) / 25) ** 2)
    Rc = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / np.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -np.sin(np.radians(2 * dth)) * Rc
    return np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def hsv_sat(srgb01):
    mx, mn = np.max(srgb01, -1), np.min(srgb01, -1)
    return np.where(mx > 0, (mx - mn) / np.where(mx > 0, mx, 1), 0)


def compare(srgb01, hexstr):
    """Report how a measured sRGB colour (0..1) reads against a target hex."""
    t = hex_rgb(hexstr)
    m = np.asarray(srgb01, np.float64)
    return dict(measured='#%02X%02X%02X' % tuple(np.round(np.clip(m, 0, 1) * 255).astype(int)),
                target=hexstr.upper(), dE00=float(de2000(lab(m), lab(t))),
                sat_ratio=float(hsv_sat(m) / max(hsv_sat(t), 1e-6)),
                L=float(lab(m)[0]), L_target=float(lab(t)[0]))


def best_scale(scene_lin_rgb, hexstr, exposure=-3.0, lo=0.05, hi=8.0, n=400):
    """The factor s that makes s * scene_lin_rgb read closest (dE00) to hexstr through PBR Neutral at `exposure`.
    Returns (s, report). Scan is log-spaced; light energy scales by the same s."""
    t = lab(hex_rgb(hexstr))
    ss = np.exp(np.linspace(np.log(lo), np.log(hi), n))
    cols = display(np.outer(ss, scene_lin_rgb), exposure)
    de = de2000(lab(cols), np.broadcast_to(t, cols.shape))
    i = int(np.argmin(de))
    return float(ss[i]), compare(cols[i], hexstr)
