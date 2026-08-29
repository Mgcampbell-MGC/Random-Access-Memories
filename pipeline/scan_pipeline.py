#!/usr/bin/env python3
"""
SCAN KEEPSAKE PIPELINE — deterministic ultrasound -> print-ready art.

The commercial question this exists to answer: can a MACHINE turn a typical clinic
ultrasound printout into something worth $150+, with no human judgment per unit?

The two stages that make this not a catalogue item (Shutterfly/Etsy cannot do either):

  STAGE 2  REDACT   Clinic ultrasounds have burned-in PHI - mother's name, DOB, hospital,
                    machine settings - rendered as bright text over the black surround.
                    Every keepsake made from a real scan MUST remove it. This is both the
                    privacy requirement and the hardest automatable step.
  STAGE 4  ISOLATE  Separate subject from ultrasound speckle. Speckle is multiplicative
                    noise, not Gaussian, so ordinary denoising smears the subject.

Everything is deterministic: same input -> same output, no model, no per-unit choices.
Run:  python3 scan_pipeline.py <image> [--out DIR] [--name "..."] [--date "..."]
"""
import sys, os, json, time, argparse, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from scipy import ndimage

DPI = 300
PALETTES = {
    # (shadow, mid, highlight) - warm neutral, deliberately not medical grey
    "warm":  ((28, 22, 20), (150, 118, 98), (250, 243, 236)),
    "mono":  ((18, 18, 20), (128, 128, 132), (248, 248, 250)),
    "blush": ((32, 20, 26), (168, 116, 118), (252, 240, 238)),
}

def _stage(log, name, t0):
    log.append({"stage": name, "ms": round((time.time() - t0) * 1000)})
    return time.time()

# ---------- STAGE 1: INGEST ----------
def ingest(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("L")     # strips EXIF orientation + metadata
    a = np.asarray(im).astype(np.float32) / 255.0
    return a

# ---------- STAGE 2: REDACT burned-in PHI ----------
def redact_overlay(a):
    """Burned-in text is near-max-intensity, thin, high-gradient, and sits on the dark
    surround outside the scan sector. Detect by intensity + local structure, then inpaint
    from the surround rather than blurring (blurring leaves a legible ghost)."""
    h, w = a.shape
    bright = a > 0.88
    # text strokes are thin: opening with a disk larger than stroke width removes them,
    # so (bright AND NOT opened) isolates thin bright structures
    opened = ndimage.grey_opening(a, size=(9, 9))
    thin = bright & ((a - opened) > 0.15)
    # anatomy is a large connected mass; text is many small components
    lab, n = ndimage.label(thin)
    mask = np.zeros_like(thin)
    if n:
        sizes = ndimage.sum(thin, lab, range(1, n + 1))
        for i, s in enumerate(sizes, start=1):
            if s < 0.004 * h * w:          # small => overlay glyph, not anatomy
                mask |= (lab == i)
    mask = ndimage.binary_dilation(mask, iterations=3)
    out = a.copy()
    if mask.any():
        # inpaint with the local dark surround value
        bg = ndimage.median_filter(a, size=25)
        out[mask] = bg[mask]
    return out, float(mask.mean())

# ---------- STAGE 3: DESPECKLE ----------
def despeckle(a):
    """Ultrasound speckle is multiplicative. Work in log space so it becomes additive,
    median-filter, then return. Preserves edges far better than Gaussian on this data."""
    eps = 1e-3
    log = np.log(a + eps)
    med = ndimage.median_filter(log, size=3)
    sm = ndimage.uniform_filter(med, size=2)
    return np.clip(np.exp(sm) - eps, 0, 1)

# ---------- STAGE 4: ISOLATE subject ----------
def isolate(a):
    """Two input classes, and they need opposite treatment:

      SECTOR  a 2D scan: bright fan on a large near-black surround. Cut the fan out.
      FULL    a 3D/4D render: fills the frame, no surround. Cutting it out destroys it -
              the correct move is a soft vignette, not a mask.

    Deciding by measuring the dark fraction rather than assuming. Getting this wrong was
    the first real bug the build exposed: a 3D render was treated as SECTOR and the
    'largest bright component' turned out to be a random blob."""
    dark_frac = float((a < 0.06).mean())
    if dark_frac < 0.18:                       # FULL-FRAME
        h, w = a.shape
        yy, xx = np.mgrid[0:h, 0:w]
        r = np.sqrt(((yy - h / 2) / (h / 2)) ** 2 + ((xx - w / 2) / (w / 2)) ** 2)
        vig = np.clip(1.0 - np.clip((r - 0.72) / 0.55, 0, 1), 0, 1)
        return vig.astype(np.float32), "full-frame"
    t = np.percentile(a[a > 0.02], 62)         # SECTOR
    m = a > t
    m = ndimage.binary_closing(m, structure=np.ones((7, 7)))
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        m = (lab == (int(np.argmax(sizes)) + 1))
    return np.clip(ndimage.gaussian_filter(m.astype(np.float32), sigma=9), 0, 1), "sector"

# ---------- STAGE 5: TONE MAP ----------
def tonemap(a, alpha, palette="warm"):
    lo, mid, hi = [np.array(c, dtype=np.float32) for c in PALETTES[palette]]
    v = a.copy()
    inside = alpha > 0.05
    if inside.any():
        p1, p99 = np.percentile(v[inside], 1), np.percentile(v[inside], 99)
        if p99 > p1:
            v = np.clip((v - p1) / (p99 - p1), 0, 1)
    v = np.power(v, 0.85)
    t = v[..., None]
    ramp = np.where(t < 0.5, lo + (mid - lo) * (t / 0.5), mid + (hi - mid) * ((t - 0.5) / 0.5))
    bg = np.array(PALETTES[palette][2], dtype=np.float32) * 0.985
    a3 = alpha[..., None]
    comp = ramp * a3 + bg * (1 - a3)
    return np.clip(comp, 0, 255).astype(np.uint8)

# ---------- STAGE 6: COMPOSE ----------
def _font(sz, bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif%s.ttf" % ("-Bold" if bold else ""),
              "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def compose(art, name, date, weeks, size_in=(12, 16), palette="warm"):
    W, H = int(size_in[0] * DPI), int(size_in[1] * DPI)
    bgc = tuple(int(c * 0.985) for c in PALETTES[palette][2])
    canvas = Image.new("RGB", (W, H), bgc)
    m = int(1.15 * DPI)
    box_w, box_h = W - 2 * m, int(H * 0.635)
    im = Image.fromarray(art)
    src_w, src_h = im.size
    scale = min(box_w / src_w, box_h / src_h)          # fills the box, up OR down
    im = im.resize((max(1, int(src_w * scale)), max(1, int(src_h * scale))), Image.LANCZOS)
    eff_dpi = round(DPI / scale) if scale > 0 else 0   # honest effective resolution
    canvas.paste(im, (m + (box_w - im.width) // 2, m + (box_h - im.height) // 2))
    d = ImageDraw.Draw(canvas)
    ink = PALETTES[palette][0]
    y = m + box_h + int(0.55 * DPI)
    d.line([(W // 2 - 120, y), (W // 2 + 120, y)], fill=ink, width=3)
    y += int(0.42 * DPI)
    for txt, sz, bold, gap in [(name.upper(), 108, True, 0.44), (date, 62, False, 0.26),
                               (weeks, 54, False, 0)]:
        if not txt:
            continue
        f = _font(sz, bold)
        w = d.textbbox((0, 0), txt, font=f)[2]
        d.text(((W - w) // 2, y), txt, font=f, fill=ink)
        y += int(gap * DPI) + sz
    return canvas, eff_dpi

# ---------- DRIVER ----------
def run(path, outdir, name, date, weeks, palette="warm"):
    log, t0 = [], time.time()
    start = t0
    a = ingest(path);                       t0 = _stage(log, "1 ingest", t0)
    a, frac = redact_overlay(a);            t0 = _stage(log, "2 redact", t0)
    a = despeckle(a);                       t0 = _stage(log, "3 despeckle", t0)
    alpha, mode = isolate(a);               t0 = _stage(log, "4 isolate", t0)
    art = tonemap(a, alpha, palette);       t0 = _stage(log, "5 tonemap", t0)
    canvas, eff_dpi = compose(art, name, date, weeks, palette=palette); t0 = _stage(log, "6 compose", t0)
    os.makedirs(outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(outdir, f"{base}__{palette}.jpg")
    canvas.save(out, "JPEG", quality=94, dpi=(DPI, DPI))
    _stage(log, "7 export", t0)
    total = round((time.time() - start) * 1000)
    sh, sw = a.shape
    gate = ("PASS >=200dpi" if eff_dpi >= 200 else
            "MARGINAL 150-200dpi" if eff_dpi >= 150 else "FAIL <150dpi at this size")
    return {"input": path, "output": out, "source_px": f"{sw}x{sh}", "input_class": mode,
            "px": f"{canvas.width}x{canvas.height}", "effective_dpi": eff_dpi,
            "resolution_gate": gate,
            "max_good_print_in": f"{sw/200:.1f}x{sh/200:.1f} at 200dpi",
            "redacted_area_pct": round(frac * 100, 3), "total_ms": total, "stages": log}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image"); ap.add_argument("--out", default="pipeline/out")
    ap.add_argument("--name", default="BABY"); ap.add_argument("--date", default="")
    ap.add_argument("--weeks", default=""); ap.add_argument("--palette", default="warm")
    A = ap.parse_args()
    print(json.dumps(run(A.image, A.out, A.name, A.date, A.weeks, A.palette), indent=2))
