"""SVG (mm) -> exact-size coverage masks via headless Chromium, and numpy compositing.

Why masks: every printed ink is rendered alone as black-on-transparent, its alpha channel is the coverage, and the
final file is composed in numpy with the exact hex from the platform. So a one-ink master is ink RGB everywhere and
coverage in alpha (no fringe colours from antialiasing against a background), and multi-ink pieces never blend
colours by accident.
"""
import os
import io
import json
import hashlib
import tempfile
import atexit

import numpy as np
from PIL import Image

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
TMP = tempfile.mkdtemp(prefix='holofote_pack_')

_pw = None
_browser = None


def _get_browser():
    global _pw, _browser
    if _browser is None:
        from playwright.sync_api import sync_playwright
        _pw = sync_playwright().start()
        _browser = _pw.chromium.launch(executable_path=CHROME,
                                       args=['--font-render-hinting=none', '--disable-lcd-text',
                                             '--force-color-profile=srgb'])
        atexit.register(_close)
    return _browser


def _close():
    global _pw, _browser
    try:
        if _browser:
            _browser.close()
        if _pw:
            _pw.stop()
    except Exception:
        pass
    _browser = None


class Doc:
    """An SVG page in mm. Elements are SVG snippets in mm coordinates (y down)."""

    def __init__(self, w_mm, h_mm, ppmm):
        self.w, self.h, self.ppmm = w_mm, h_mm, ppmm
        self.items = []
        self.defs = []

    @property
    def px(self):
        return int(round(self.w * self.ppmm)), int(round(self.h * self.ppmm))

    def add(self, s):
        self.items.append(s)

    def path(self, d, fill='#000', rule='nonzero', mask=None, opacity=None):
        if not d:
            return
        m = f' mask="url(#{mask})"' if mask else ''
        o = f' fill-opacity="{opacity}"' if opacity is not None else ''
        self.items.append(f'<path d="{d}" fill="{fill}" fill-rule="{rule}"{m}{o}/>')

    def rect(self, x, y, w, h, fill='#000', rx=0):
        self.items.append(f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" rx="{rx}" fill="{fill}"/>')

    def svg(self, standalone_units=False):
        W, H = self.px
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ''
        if standalone_units:  # a print-ready vector file in real mm
            head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" '
                    f'viewBox="0 0 {self.w} {self.h}">')
            return head + defs + ''.join(self.items) + '</svg>'
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {self.w} {self.h}" '
                f'shape-rendering="geometricPrecision">')
        return head + defs + ''.join(self.items) + '</svg>'


def rasterise(doc):
    """Return coverage (H, W) float32 0..1 of everything drawn in doc (draw in black)."""
    W, H = doc.px
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:transparent}'
            'svg{display:block}</style></head><body>' + doc.svg() + '</body></html>')
    p = os.path.join(TMP, 'r.html')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    b = _get_browser()
    pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
    pg.goto('file://' + p)
    pg.wait_for_load_state('load')
    png = pg.screenshot(omit_background=True, clip={'x': 0, 'y': 0, 'width': W, 'height': H}, type='png')
    pg.close()
    im = Image.open(io.BytesIO(png)).convert('RGBA')
    a = np.asarray(im)[:, :, 3].astype(np.float32) / 255.0
    assert a.shape == (H, W), (a.shape, W, H)
    return a


def hex2rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def ink_rgba(alpha, ink_hex):
    """A one-ink master: RGB = ink everywhere, A = coverage."""
    H, W = alpha.shape
    out = np.zeros((H, W, 4), np.uint8)
    out[:, :, :3] = hex2rgb(ink_hex).astype(np.uint8)
    out[:, :, 3] = np.clip(np.round(alpha * 255), 0, 255).astype(np.uint8)
    return out


def over(dst_rgb, alpha, color):
    """composite a flat colour with coverage alpha over an RGB float image (in place, returns it)"""
    c = hex2rgb(color) if isinstance(color, str) else color
    a = alpha[..., None]
    dst_rgb *= (1 - a)
    dst_rgb += a * c
    return dst_rgb


def flat(h, w, color):
    out = np.zeros((h, w, 3), np.float32)
    out[:] = hex2rgb(color)
    return out


def layers_rgba(h, w, layers):
    """Compose [(alpha, colour)] over transparent; returns uint8 RGBA (straight alpha)."""
    rgb_p = np.zeros((h, w, 3), np.float32)  # premultiplied
    a_acc = np.zeros((h, w), np.float32)
    for alpha, color in layers:
        c = hex2rgb(color) if isinstance(color, str) else np.asarray(color, np.float32)
        if c.ndim == 1:
            c = c[None, None, :]
        rgb_p = rgb_p * (1 - alpha[..., None]) + alpha[..., None] * c
        a_acc = a_acc * (1 - alpha) + alpha
    out = np.zeros((h, w, 4), np.uint8)
    safe = np.maximum(a_acc, 1e-6)[..., None]
    out[..., :3] = np.clip(np.round(rgb_p / safe), 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(np.round(a_acc * 255), 0, 255).astype(np.uint8)
    return out


def save_png(arr, path, bits16=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if bits16:
        Image.fromarray(arr.astype(np.uint16)).save(path)
    else:
        Image.fromarray(arr).save(path, optimize=False, compress_level=6)
    return path


def save_jpg(rgb, path, q=92):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(np.clip(np.round(rgb), 0, 255).astype(np.uint8)).save(path, quality=q, subsampling=0)
    return path


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path


def write_svg(doc, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(doc.svg(standalone_units=True))
    return path


def downscale(rgb_or_rgba, factor):
    im = Image.fromarray(rgb_or_rgba)
    return np.asarray(im.resize((im.width // factor, im.height // factor), Image.LANCZOS))
