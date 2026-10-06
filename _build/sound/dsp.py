"""HOLOFOTE · dsp.py — shared audio helpers for the sound team (48 kHz, float64 internally).

Everything here is deterministic: every random process takes an explicit seed, so a rebuild is bit-identical.
"""
from __future__ import annotations

import os
import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000


# ----------------------------------------------------------------------------------------------- I/O

def read(path: str, sr: int = SR) -> np.ndarray:
    """Read any libsndfile/ffmpeg-decodable file as float64 (N, ch) resampled to `sr`."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".mp3":
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as d:
            tmp = os.path.join(d, "x.wav")
            subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", path, tmp], check=True)
            x, r = sf.read(tmp, always_2d=True, dtype="float64")
    else:
        x, r = sf.read(path, always_2d=True, dtype="float64")
    if r != sr:
        g = np.gcd(int(r), int(sr))
        x = signal.resample_poly(x, sr // g, r // g, axis=0)
    return x


def write(path: str, x: np.ndarray, sr: int = SR) -> None:
    """Write 24-bit PCM WAV. Mono input is written as stereo (dual mono) so the library is uniform."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = x[:, None]
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    sf.write(path, np.clip(x, -1.0, 1.0), sr, subtype="PCM_24")


def mono(x: np.ndarray) -> np.ndarray:
    return x.mean(axis=1) if x.ndim == 2 else x


def stereo(x: np.ndarray) -> np.ndarray:
    if x.ndim == 1:
        return np.stack([x, x], axis=1)
    if x.shape[1] == 1:
        return np.repeat(x, 2, axis=1)
    return x


def seg(x: np.ndarray, t0: float, t1: float, sr: int = SR) -> np.ndarray:
    return x[int(round(t0 * sr)):int(round(t1 * sr))].copy()


def silence(sec: float, ch: int = 2, sr: int = SR) -> np.ndarray:
    return np.zeros((int(round(sec * sr)), ch))


def place(dst: np.ndarray, src: np.ndarray, t: float, gain_db: float = 0.0, sr: int = SR) -> np.ndarray:
    """Add `src` into `dst` starting at time t (s). Extends nothing: src is clipped to dst length."""
    src = stereo(src) if dst.ndim == 2 else mono(src)
    i = int(round(t * sr))
    if i >= len(dst):
        return dst
    j0 = max(0, -i)
    n = min(len(src) - j0, len(dst) - max(i, 0))
    if n > 0:
        dst[max(i, 0):max(i, 0) + n] += src[j0:j0 + n] * db(gain_db)
    return dst


def db(v: float) -> float:
    return 10.0 ** (v / 20.0)


def todb(v: float) -> float:
    return 20.0 * np.log10(max(abs(v), 1e-12))


# ----------------------------------------------------------------------------------------------- envelopes

def fade(x: np.ndarray, fin: float = 0.0, fout: float = 0.0, sr: int = SR, shape: str = "cos") -> np.ndarray:
    x = x.copy()
    n = len(x)
    for dur, rev in ((fin, False), (fout, True)):
        k = min(int(round(dur * sr)), n)
        if k <= 0:
            continue
        r = np.linspace(0.0, 1.0, k)
        w = np.sin(r * np.pi / 2) ** 2 if shape == "cos" else r
        if rev:
            w = w[::-1]
            x[n - k:] *= w[:, None] if x.ndim == 2 else w
        else:
            x[:k] *= w[:, None] if x.ndim == 2 else w
    return x


def env_points(n: int, pts, sr: int = SR) -> np.ndarray:
    """Piecewise-linear gain envelope from [(t, gain_db), ...]."""
    t = np.arange(n) / sr
    ts = [p[0] for p in pts]
    gs = [db(p[1]) for p in pts]
    return np.interp(t, ts, gs)


def apply_env(x: np.ndarray, e: np.ndarray) -> np.ndarray:
    return x * (e[:, None] if x.ndim == 2 else e)


# ----------------------------------------------------------------------------------------------- filters

def _sos(kind: str, f, order: int = 2, sr: int = SR):
    return signal.butter(order, f, btype=kind, fs=sr, output="sos")


def hp(x, f, order=2, sr=SR):
    return signal.sosfilt(_sos("highpass", f, order, sr), x, axis=0)


def lp(x, f, order=2, sr=SR):
    return signal.sosfilt(_sos("lowpass", f, order, sr), x, axis=0)


def bp(x, f1, f2, order=2, sr=SR):
    return signal.sosfilt(_sos("bandpass", [f1, f2], order, sr), x, axis=0)


def peak_eq(x, f0, gain_db, q=1.0, sr=SR):
    """RBJ peaking EQ."""
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / sr
    al = np.sin(w0) / (2 * q)
    b = np.array([1 + al * A, -2 * np.cos(w0), 1 - al * A])
    a = np.array([1 + al / A, -2 * np.cos(w0), 1 - al / A])
    return signal.lfilter(b / a[0], a / a[0], x, axis=0)


def shelf(x, f0, gain_db, high=True, sr=SR):
    """RBJ shelving EQ (S = 1)."""
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / sr
    al = np.sin(w0) / 2 * np.sqrt(2)
    c = np.cos(w0)
    if high:
        b = [A * ((A + 1) + (A - 1) * c + 2 * np.sqrt(A) * al), -2 * A * ((A - 1) + (A + 1) * c),
             A * ((A + 1) + (A - 1) * c - 2 * np.sqrt(A) * al)]
        a = [(A + 1) - (A - 1) * c + 2 * np.sqrt(A) * al, 2 * ((A - 1) - (A + 1) * c),
             (A + 1) - (A - 1) * c - 2 * np.sqrt(A) * al]
    else:
        b = [A * ((A + 1) - (A - 1) * c + 2 * np.sqrt(A) * al), 2 * A * ((A - 1) - (A + 1) * c),
             A * ((A + 1) - (A - 1) * c - 2 * np.sqrt(A) * al)]
        a = [(A + 1) + (A - 1) * c + 2 * np.sqrt(A) * al, -2 * ((A - 1) + (A + 1) * c),
             (A + 1) + (A - 1) * c - 2 * np.sqrt(A) * al]
    b = np.array(b) / a[0]
    a = np.array(a) / a[0]
    return signal.lfilter(b, a, x, axis=0)


def resonator(x, f0, bw, sr=SR):
    """Two-pole resonator (constant peak gain ~1)."""
    r = np.exp(-np.pi * bw / sr)
    th = 2 * np.pi * f0 / sr
    a = [1, -2 * r * np.cos(th), r * r]
    b = [(1 - r * r) / 2, 0, -(1 - r * r) / 2]
    return signal.lfilter(b, a, x, axis=0)


def pitch(x: np.ndarray, semitones: float) -> np.ndarray:
    """Varispeed pitch shift (duration changes by the same ratio), like a tape speed change."""
    ratio = 2 ** (semitones / 12)
    up, down = _ratio(1 / ratio)
    return signal.resample_poly(x, up, down, axis=0)


def stretch_speed(x: np.ndarray, factor: float) -> np.ndarray:
    """Varispeed: factor > 1 makes it longer and lower."""
    up, down = _ratio(factor)
    return signal.resample_poly(x, up, down, axis=0)


def _ratio(r: float, maxden: int = 400):
    from fractions import Fraction
    f = Fraction(r).limit_denominator(maxden)
    return f.numerator, f.denominator


# ----------------------------------------------------------------------------------------------- noise

def pink(n: int, rng: np.random.Generator) -> np.ndarray:
    """Pink noise via spectral shaping (1/f power)."""
    w = rng.standard_normal(n)
    W = np.fft.rfft(w)
    f = np.arange(len(W))
    f[0] = 1
    W = W / np.sqrt(f)
    y = np.fft.irfft(W, n)
    return y / (np.abs(y).max() + 1e-12)


def brown(n: int, rng: np.random.Generator) -> np.ndarray:
    w = rng.standard_normal(n)
    W = np.fft.rfft(w)
    f = np.arange(len(W)).astype(float)
    f[0] = 1
    y = np.fft.irfft(W / f, n)
    return y / (np.abs(y).max() + 1e-12)


# ----------------------------------------------------------------------------------------------- spaces

def room_ir(rt60: float, dims=(4.2, 3.4, 2.7), src=(1.3, 1.6, 1.4), mic=(2.6, 2.0, 1.5), absorb=0.45,
            order: int = 8, tail_lp: float = 7000.0, seed: int = 1, sr: int = SR, hf_damp: float = 1.8) -> np.ndarray:
    """Stereo room impulse response: image-source early reflections (shoebox) + a decorrelated diffuse tail.

    rt60   reverberation time (s) of the diffuse tail at mid frequencies
    hf_damp how much faster the highs decay (ratio), the main thing that makes a room sound 'real'
    """
    rng = np.random.default_rng(seed)
    c = 343.0
    L = int(sr * max(rt60 * 1.3, 0.12)) + 1
    ir = np.zeros((L, 2))
    ear = 0.09  # half head-width, gives a little stereo spread to early reflections
    refl = np.sqrt(1 - absorb)
    Lx, Ly, Lz = dims
    for ix in range(-order, order + 1):
        for iy in range(-order, order + 1):
            for iz in range(-order // 2, order // 2 + 1):
                n_ref = abs(ix) + abs(iy) + abs(iz)
                if n_ref > order:
                    continue
                px = (ix * Lx + (src[0] if ix % 2 == 0 else Lx - src[0]))
                py = (iy * Ly + (src[1] if iy % 2 == 0 else Ly - src[1]))
                pz = (iz * Lz + (src[2] if iz % 2 == 0 else Lz - src[2]))
                for ch, off in ((0, -ear), (1, ear)):
                    d = np.sqrt((px - mic[0]) ** 2 + (py - (mic[1] + off)) ** 2 + (pz - mic[2]) ** 2)
                    k = int(round(d / c * sr))
                    if k < L:
                        ir[k, ch] += (refl ** n_ref) / max(d, 0.3)
    # diffuse tail: noise decaying at rt60 (lows) and rt60/hf_damp (highs), starting after the early field
    t = np.arange(L) / sr
    d0 = np.sqrt(sum((np.array(src) - np.array(mic)) ** 2)) / c
    onset = d0 + 0.012
    for ch in range(2):
        nz = rng.standard_normal(L)
        lo = lp(nz, 1500, 2, sr) * np.exp(-6.91 * t / rt60)
        hi = hp(nz, 1500, 2, sr) * np.exp(-6.91 * t / (rt60 / hf_damp))
        tail = lp(lo + hi, tail_lp, 1, sr)
        ramp = np.clip((t - onset) / 0.02, 0, 1)
        ir[:, ch] += tail * ramp * 0.35 * (1.0 / max(d0 * c, 0.3))
    ir /= np.abs(ir).max()
    return ir


def hall_ir(rt60: float = 1.8, predelay: float = 0.025, width: float = 1.0, seed: int = 2, sr: int = SR,
            hf_damp: float = 2.2, lf_boost: float = 1.15) -> np.ndarray:
    """Large-space stereo IR (theatre / hall): sparse early reflections + dense frequency-dependent tail."""
    rng = np.random.default_rng(seed)
    L = int(sr * (rt60 * 1.4 + predelay))
    t = np.arange(L) / sr
    ir = np.zeros((L, 2))
    ir[0, :] = 1.0
    # early reflections, 6-80 ms after predelay
    for _ in range(28):
        tt = predelay + rng.uniform(0.004, 0.085)
        k = int(tt * sr)
        g = 0.55 * np.exp(-tt / 0.09) * rng.uniform(0.4, 1.0)
        ch = rng.integers(0, 2)
        ir[k, ch] += g
        ir[min(L - 1, k + int(rng.uniform(0, 0.003) * sr)), 1 - ch] += g * (1 - width * 0.5)
    for ch in range(2):
        nz = rng.standard_normal(L)
        bands = [(None, 250, rt60 * lf_boost), (250, 2000, rt60), (2000, 6000, rt60 / hf_damp),
                 (6000, None, rt60 / (hf_damp * 1.6))]
        tail = np.zeros(L)
        for f1, f2, r in bands:
            if f1 is None:
                b = lp(nz, f2, 2, sr)
            elif f2 is None:
                b = hp(nz, f1, 2, sr)
            else:
                b = bp(nz, f1, f2, 2, sr)
            tail += b * np.exp(-6.91 * t / r)
        ramp = np.clip((t - predelay - 0.01) / 0.06, 0, 1)
        ir[:, ch] += tail * ramp * 0.11
    return ir / np.abs(ir).max()


def convolve(x: np.ndarray, ir: np.ndarray, wet: float = 0.3, dry: float = 1.0, keep_len: bool = False) -> np.ndarray:
    """Stereo convolution with dry/wet. Mono x is spread to both IR channels."""
    x = stereo(x)
    y = np.zeros((len(x) + len(ir) - 1, 2))
    for ch in range(2):
        y[:, ch] = signal.fftconvolve(x[:, ch], ir[:, ch])
    # normalise wet to roughly the dry's RMS so the wet/dry knobs mean something
    rx = np.sqrt((x ** 2).mean()) + 1e-12
    ry = np.sqrt((y[:len(x)] ** 2).mean()) + 1e-12
    y *= (rx / ry)
    out = y * wet
    out[:len(x)] += x * dry
    return out[:len(x)] if keep_len else out


# ----------------------------------------------------------------------------------------------- loudness

# ITU-R BS.1770-4 K-weighting coefficients for 48 kHz
_K1 = (np.array([1.53512485958697, -2.69169618940638, 1.19839281085285]),
       np.array([1.0, -1.69065929318241, 0.73248077421585]))
_K2 = (np.array([1.0, -2.0, 1.0]), np.array([1.0, -1.99004745483398, 0.99007225036621]))


def kweight(x: np.ndarray) -> np.ndarray:
    y = signal.lfilter(*_K1, x, axis=0)
    return signal.lfilter(*_K2, y, axis=0)


def momentary_max(x: np.ndarray, sr: int = SR) -> float:
    """Maximum momentary loudness (400 ms window, 100 ms hop), LUFS. Valid for one-shots of any length."""
    x = stereo(x)
    y = kweight(x)
    w = int(0.4 * sr)
    if len(y) < w:
        y = np.vstack([y, np.zeros((w - len(y), 2))])
    p = np.cumsum(np.vstack([np.zeros((1, 2)), y ** 2]), axis=0)
    hop = int(0.1 * sr)
    idx = np.arange(0, len(y) - w + 1, max(1, hop // 4))
    ms = (p[idx + w] - p[idx]) / w
    z = ms.sum(axis=1)
    return float(-0.691 + 10 * np.log10(z.max() + 1e-15))


def integrated(x: np.ndarray, sr: int = SR) -> float:
    import pyloudnorm as pyln
    x = stereo(x)
    if len(x) < int(0.4 * sr):
        return float("nan")
    return float(pyln.Meter(sr).integrated_loudness(x))


def true_peak(x: np.ndarray) -> float:
    """dBTP with 4x oversampling (BS.1770 annex 2 style)."""
    up = signal.resample_poly(stereo(x), 4, 1, axis=0)
    return todb(np.abs(up).max())


def tp_limit(x: np.ndarray, ceiling_db: float = -1.0, release: float = 0.06, look: float = 0.0015,
             sr: int = SR) -> np.ndarray:
    """Look-ahead true-peak limiter. Detection on a 4x-oversampled signal, gain smoothed, linked stereo."""
    x = stereo(x)
    c = db(ceiling_db - 0.15)  # a small safety margin for the reconstruction filter
    up = signal.resample_poly(x, 4, 1, axis=0)
    pk = np.abs(up).max(axis=1).reshape(-1, 4).max(axis=1)[:len(x)]
    if len(pk) < len(x):
        pk = np.pad(pk, (0, len(x) - len(pk)))
    g = np.minimum(1.0, c / np.maximum(pk, 1e-12))
    la = int(look * sr)
    # look-ahead: take the minimum gain over the next `la` samples
    from scipy.ndimage import minimum_filter1d
    g = minimum_filter1d(g, size=2 * la + 1, origin=0)
    # smooth: instant attack (already looked ahead), exponential release
    a = np.exp(-1.0 / (release * sr))
    out = np.empty_like(g)
    s = 1.0
    for i in range(len(g)):  # simple loop; fine for <60 s at 48 kHz
        s = g[i] if g[i] < s else a * s + (1 - a) * g[i]
        out[i] = s
    # attack ramp: a short moving minimum + average so the gain change is not a step
    k = max(1, la)
    out = np.convolve(np.pad(out, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]
    return x * out[:, None]


def norm_sfx(x: np.ndarray, target_m: float = -20.0, tp_ceiling: float = -1.0):
    """Library normalisation: max momentary loudness -> target_m LUFS-M, then never above tp_ceiling dBTP
    (the gain is reduced, not limited, so transients stay intact). Returns (y, info)."""
    m0 = momentary_max(x)
    g = target_m - m0
    y = x * db(g)
    tp = true_peak(y)
    if tp > tp_ceiling:
        y = y * db(tp_ceiling - tp)
    info = dict(lufs_m_max=round(momentary_max(y), 2), true_peak_dbtp=round(true_peak(y), 2),
                lufs_i=(None if len(y) < 0.4 * SR else round(integrated(y), 2)))
    return y, info


def norm_mix(x: np.ndarray, target_i: float = -14.0, tp_ceiling: float = -1.0, iters: int = 12):
    """Programme normalisation: integrated loudness -> target_i LUFS, true peak <= tp_ceiling via the limiter."""
    y = stereo(x).copy()
    for _ in range(iters):
        li = integrated(y)
        y = y * db(target_i - li)
        if true_peak(y) > tp_ceiling:
            y = tp_limit(y, tp_ceiling)
        if abs(integrated(y) - target_i) < 0.05 and true_peak(y) <= tp_ceiling + 0.01:
            break
    return y, dict(lufs_i=round(integrated(y), 2), true_peak_dbtp=round(true_peak(y), 2))


# ----------------------------------------------------------------------------------------------- matching EQ

OCT = np.array([63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000], float)


def octave_levels(x: np.ndarray, sr: int = SR) -> np.ndarray:
    """Long-term octave-band levels (dB) of x at OCT centres."""
    f, p = signal.welch(mono(x), fs=sr, nperseg=8192)
    out = []
    for b in OCT:
        m = (f > b / np.sqrt(2)) & (f < b * np.sqrt(2))
        out.append(10 * np.log10(p[m].mean() + 1e-24))
    return np.array(out)


def match_tilt(x: np.ndarray, target: dict, loop: bool = False, limit: float = 18.0, sr: int = SR) -> np.ndarray:
    """Zero-phase matching EQ: reshape x's long-term spectrum toward `target` {octave_centre_Hz: dB relative}.
    Bands absent from `target` are left alone. Done in the FFT domain (circular when loop=True, padded otherwise)."""
    cur = octave_levels(x, sr)
    keys = sorted(target)
    ref_c = np.interp(np.log2(1000), np.log2(OCT), cur)
    corr = {}
    for k in keys:
        c = np.interp(np.log2(k), np.log2(OCT), cur) - ref_c
        corr[k] = float(np.clip(target[k] - c, -limit, limit))
    xs = stereo(x)
    n = len(xs) if loop else int(2 ** np.ceil(np.log2(len(xs) + sr)))
    F = np.fft.rfft(xs, n=n, axis=0)
    f = np.fft.rfftfreq(n, 1 / sr)
    lf = np.log2(np.maximum(f, 20.0))
    g_db = np.interp(lf, np.log2(keys), [corr[k] for k in keys])
    F *= (10 ** (g_db / 20))[:, None]
    y = np.fft.irfft(F, n=n, axis=0)[:len(xs)]
    # keep the overall level where it was (RMS)
    return y * (np.sqrt((xs ** 2).mean()) / (np.sqrt((y ** 2).mean()) + 1e-20))
