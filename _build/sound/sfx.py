#!/usr/bin/env python
"""HOLOFOTE · sfx.py — builds the foley / SFX library and the sonic identity from licensed real recordings
(see fetch_sources.py) plus code synthesis. Output: 04_FILMES/som/{sfx,identidade}/*.wav (48 kHz, 24-bit) and
04_FILMES/som/sfx_manifest.json (sync points measured from the files, loudness, sources).

    /home/user/venvs/web/bin/python -I sfx.py            # everything
    /home/user/venvs/web/bin/python -I sfx.py clac tosse # only some builders
"""
from __future__ import annotations

import glob, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dsp  # noqa: E402
from dsp import SR, db  # noqa: E402

KIT = os.path.abspath(os.path.join(HERE, "..", ".."))
SOM = os.path.join(KIT, "04_FILMES", "som")
F = os.path.join(HERE, "_fontes")
TMP = os.path.join(HERE, "_tmp")
FPS = 24.0
FRAME = 1.0 / FPS


def src(rel: str) -> np.ndarray:
    return dsp.read(os.path.join(F, rel))


K_UI = "kenney_ui/x/Audio/"
K_RPG = "kenney_rpg/x/Audio/"
K_IMP = "kenney_impact/x/Audio/"
K_CAS = "kenney_casino/x/Audio/"


def first_onset(x: np.ndarray, thresh_db: float = -30.0) -> float:
    """Time of the first sample whose envelope rises within `thresh_db` of the file peak (s)."""
    m = np.abs(dsp.mono(x))
    pk = m.max()
    i = int(np.argmax(m > pk * db(thresh_db)))
    return i / SR


def align(x: np.ndarray, at: float, thresh_db: float = None) -> np.ndarray:
    """Shift x so its transient lands at `at` seconds — measured the way onsets.py measures it (HF rise),
    or, if thresh_db is given, at the first sample within thresh_db of the peak."""
    o = first_onset(x, thresh_db) if thresh_db is not None else hf_onset(x) / SR
    d = int(round((at - o) * SR))
    if d >= 0:
        return np.concatenate([np.zeros((d,) + x.shape[1:]), x], axis=0)
    return x[-d:]


def hf_onset(x: np.ndarray) -> int:
    """Sample index of an isolated event's onset, by the same rule as onsets.py (1,5 kHz high-pass, causal
    1,5 ms peak-hold, first sample of the rise reaching 25 % of the peak)."""
    from scipy.ndimage import maximum_filter1d
    h = np.abs(dsp.hp(dsp.mono(x), 1500, 2))
    kh = int(0.0015 * SR)
    e = maximum_filter1d(h, size=kh, origin=(kh - 1) // 2)
    ip = int(np.argmax(e))
    i = ip
    while i > 0 and e[i - 1] >= 0.25 * e[ip]:
        i -= 1
    return i


def gate_pre(x: np.ndarray, at: float, ramp: float = 0.002) -> np.ndarray:
    """Silence everything before `at` - ramp (removes a source's noise floor from the pre-roll)."""
    y = x.copy()
    i1 = max(0, int((at - 0.0005) * SR)); i0 = max(0, i1 - int(ramp * SR))
    g = np.ones(len(y)); g[:i0] = 0; g[i0:i1] = np.linspace(0, 1, i1 - i0)
    return y * (g[:, None] if y.ndim == 2 else g)


def pan(x: np.ndarray, p: float) -> np.ndarray:
    """Equal-power pan of a mono/stereo signal, p in [-1, 1]."""
    m = dsp.mono(x)
    a = (p + 1) * np.pi / 4
    return np.stack([m * np.cos(a), m * np.sin(a)], axis=1)


def noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


# ============================================================================================ builders
REG: dict = {}


def builder(fid, name, kind, sync_desc):
    def deco(fn):
        REG[fn.__name__] = dict(fn=fn, id=fid, name=name, kind=kind, sync=sync_desc)
        return fn
    return deco


def _filament(n_warm: int, total: float, seed: int, level_db: float = -22.0):
    """Lamp filament warm-up: a 120 Hz mains buzz (Brazil runs at 60 Hz) whose level and brightness rise over
    n_warm samples, then settle to a faint hum that dies away. Returns mono."""
    N = int(total * SR)
    t = np.arange(N) / SR
    # buzz: rich harmonics of 120 Hz with a little jitter, like a dimmer pack / transformer
    rng = np.random.default_rng(seed)
    ph = 2 * np.pi * 120 * t + 0.02 * np.cumsum(rng.standard_normal(N)) / SR * 50
    buzz = sum((0.9 ** k) * np.sin(k * ph + rng.uniform(0, 6.28)) for k in range(1, 26))
    buzz += 0.15 * dsp.hp(rng.standard_normal(N), 2000) * (np.sin(ph) > 0.6)  # arcing grit on the peaks
    # brightness rises with the warm-up: crossfade a dark and a bright version
    dark = dsp.lp(buzz, 400, 2)
    bright = dsp.lp(buzz, 5000, 2)
    w = np.clip(t / (n_warm / SR), 0, 1)
    sig = dark * (1 - w) + bright * w
    env = np.where(t < n_warm / SR, (t / (n_warm / SR)) ** 1.5,
                   0.35 + 0.65 * np.exp(-(t - n_warm / SR) / 0.05))
    env *= np.exp(-np.maximum(t - n_warm / SR, 0) / 0.30)
    env *= np.clip((total - t) / (0.45 * total), 0, 1) ** 2  # always dies to zero before the file ends
    sig = sig * env
    return sig / (np.abs(sig).max() + 1e-12) * db(level_db)


@builder("HLF-SFX-01", "clac", "one-shot",
         "transiente do interruptor (o quadro em que a luz ACENDE começa 2 quadros = 83 ms depois)")
def clac():
    """CLAC: a theatre lamp switching on, with a 2-frame (83 ms) filament warm-up after the switch."""
    return _clac(0.020, 1.6)


def _clac(pre: float, T: float):
    out = np.zeros((int(T * SR), 2))
    sw = src("oga_lightswitch/x/light_switch_turn_on.mp3")       # real wall switch, close-miked
    latch = dsp.pitch(src(K_RPG + "metalLatch.ogg"), -4)          # real metal latch, pitched down for mass
    dsp.place(out, align(sw, pre), 0, 0)
    dsp.place(out, align(latch, pre + 0.002), 0, -7)
    # body: the thunk of a heavy stage switch / contactor
    n = int(0.12 * SR); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (70 + 60 * np.exp(-t / 0.01)) * t) * np.exp(-t / 0.028)
    dsp.place(out, thump, pre, -9)
    # 2-frame warm-up: buzz rising from the click to full at +83 ms
    warm = int(2 * FRAME * SR)
    fil = _filament(warm, 1.2, seed=11, level_db=-14)
    dsp.place(out, fil, pre + 0.004, 0)
    # the light lands: a soft low 'whoomph' of air + the housing's thermal 'tink'
    n = int(0.09 * SR); t = np.arange(n) / SR
    wh = dsp.bp(noise(n, 12), 90, 700, 2) * np.sin(np.pi * np.clip(t / 0.09, 0, 1)) ** 2
    dsp.place(out, wh / np.abs(wh).max(), pre + warm / SR - 0.03, -15)
    n = int(0.25 * SR); t = np.arange(n) / SR
    tink = (np.sin(2 * np.pi * 2870 * t) + 0.5 * np.sin(2 * np.pi * 4410 * t + 1)) * np.exp(-t / 0.05)
    dsp.place(out, tink / 1.5, pre + warm / SR, -30)
    # the hall: a big empty theatre answers
    ir = dsp.hall_ir(1.7, 0.03, seed=21)
    out = dsp.convolve(out, ir, wet=0.22, dry=1.0)[:int(T * SR)]
    return dsp.fade(gate_pre(out, pre), 0, 0.25)


@builder("HLF-SFX-02", "clac_off", "one-shot", "transiente do interruptor (o BLACKOUT é neste quadro)")
def clac_off():
    """CLAC-off: the spot cut to black. The hum is already running and dies on the click."""
    pre = 0.060
    T = 1.2
    out = np.zeros((int(T * SR), 2))
    # the running hum before the cut (60 ms) that stops dead on the switch
    hum = _filament(int(0.001 * SR), 0.8, seed=13, level_db=-26)
    hum = dsp.stereo(hum[:int(pre * SR) + 40])
    hum = dsp.fade(hum, 0.03, 0.002)
    dsp.place(out, hum, 0, 0)
    sw = src("oga_lightswitch/x/light_switch_turn_off.mp3")
    latch = dsp.pitch(src(K_RPG + "metalLatch.ogg"), -6)
    dsp.place(out, align(sw, pre), 0, 0)
    dsp.place(out, align(latch, pre + 0.001), 0, -6)
    n = int(0.12 * SR); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (62 + 50 * np.exp(-t / 0.01)) * t) * np.exp(-t / 0.035)
    dsp.place(out, thump, pre, -8)
    # filament cooling: a tiny tick 40 ms later
    n = int(0.08 * SR); t = np.arange(n) / SR
    tick = np.sin(2 * np.pi * 3300 * t) * np.exp(-t / 0.012)
    dsp.place(out, tick, pre + 0.045, -36)
    ir = dsp.hall_ir(1.7, 0.03, seed=22)
    out = dsp.convolve(out, ir, wet=0.2, dry=1.0)[:int(T * SR)]
    return dsp.fade(out, 0, 0.3)


# -------------------------------------------------------------------------------------------- circular helpers

def circ_place(dst: np.ndarray, src_: np.ndarray, t: float, gain_db: float = 0.0):
    """Add src into dst at t, wrapping around the end (for seamless loops)."""
    src_ = dsp.stereo(src_) * db(gain_db)
    L = len(dst)
    i = int(round(t * SR)) % L
    n = len(src_)
    while n > 0:
        k = min(n, L - i)
        dst[i:i + k] += src_[len(src_) - n:len(src_) - n + k]
        n -= k
        i = 0
    return dst


def circ_conv(x: np.ndarray, ir: np.ndarray, wet: float, dry: float = 1.0) -> np.ndarray:
    """Circular convolution: the reverb tail of the end of a loop wraps onto its start, so the loop is seamless."""
    L = len(x)
    reps = int(np.ceil(len(ir) / L)) + 1
    tiled = np.vstack([x] * (reps + 1))
    y = dsp.convolve(tiled, ir, wet=wet, dry=dry)
    return y[reps * L:(reps + 1) * L]


def circ_filter(x: np.ndarray, fn) -> np.ndarray:
    """Apply an IIR filter `fn` to a loop without a seam (run over two periods, keep the second)."""
    y = fn(np.vstack([x, x]))
    return y[len(x):]


def walla_files(kind):
    return sorted(glob.glob(os.path.join(TMP, "walla", f"{kind}_*.wav")))


def stadium_ir(seed=31):
    """Open bowl: a long dark tail plus two slap-back echoes off the far stands."""
    ir = dsp.hall_ir(2.4, 0.035, seed=seed, hf_damp=2.8, lf_boost=1.25)
    for dt, g in ((0.19, 0.35), (0.33, 0.22), (0.52, 0.12)):
        k = int(dt * SR)
        sl = dsp.lp(ir[:len(ir) - k] * 1.0, 2500, 2)
        ir[k:] += sl * g
    return ir / np.abs(ir).max()


# -------------------------------------------------------------------------------------------- crowd

@builder("HLF-SFX-03", "murmurio_teatro_loop", "loop 16 s",
         "loop sem emenda: o fim encosta no começo; sem ponto de sincronia")
def murmurio_teatro_loop():
    """Pre-show murmur: ~60 own-synthesised PT-BR voices (walla_tts.py) at random seats of a hall, smeared below
    intelligibility, with seat creaks and the house's air. Circular, so it loops without a seam."""
    rng = np.random.default_rng(303)
    L = 16.0
    out = np.zeros((int(L * SR), 2))
    talks = [dsp.read(f) for f in walla_files("talk")]
    for i in range(64):
        v = talks[rng.integers(len(talks))]
        v = dsp.pitch(v, rng.uniform(-2.2, 2.0))
        far = rng.uniform(0, 1)                       # 0 = row in front of us, 1 = back of the house
        v = dsp.bp(dsp.mono(v), 140, 5200 - 2800 * far, 2)
        v = dsp.peak_eq(v, 2600, -5, 0.8)              # take the consonants down: no word survives
        v = dsp.fade(v, 0.08, 0.15)
        circ_place(out, pan(v, rng.uniform(-0.85, 0.85)), rng.uniform(0, L), rng.uniform(-9, -1) - 6 * far)
    # seats: a few creaks of wooden/plastic theatre seats
    for i in range(7):
        c = src(K_RPG + f"creak{rng.integers(1, 4)}.ogg")
        c = dsp.lp(dsp.pitch(c, rng.uniform(-7, -3)), 2500, 2)
        circ_place(out, pan(c, rng.uniform(-0.9, 0.9)), rng.uniform(0, L), rng.uniform(-30, -24))
    # slow breathing of the crowd level (periodic in L, so it loops)
    t = np.arange(len(out)) / SR
    breath = 1 + 0.12 * np.sin(2 * np.pi * t * 3 / L + 0.4) + 0.08 * np.sin(2 * np.pi * t * 7 / L + 2.1)
    out *= breath[:, None]
    out = circ_conv(out, dsp.hall_ir(1.6, 0.03, seed=33), wet=0.85, dry=0.55)
    # the house: air handling, very low
    n = len(out)
    air = np.stack([dsp.brown(n, np.random.default_rng(34)), dsp.brown(n, np.random.default_rng(35))], 1)
    out += circ_filter(air, lambda z: dsp.lp(dsp.hp(z, 35, 2), 300, 2)) * db(-34) * np.abs(out).max()
    out = circ_filter(out, lambda z: dsp.lp(dsp.hp(z, 90, 2), 6500, 2))
    return dsp.match_tilt(out, {125: -9, 250: -2, 500: 0, 1000: -4, 2000: -11, 4000: -19, 8000: -30}, loop=True)


def _cheer_bank(rng, n_voices, dur, rise_st=1.2):
    """n_voices sustained TTS cheers, pitch-varied, each with a rising contour (a crowd lifting its voice)."""
    cheers = [dsp.mono(dsp.read(f)) for f in walla_files("cheer")]
    out = np.zeros((int(dur * SR), 2))
    for i in range(n_voices):
        c = cheers[rng.integers(len(cheers))]
        st = rng.uniform(0.5, 7.0)                       # shouting raises the voice
        c = dsp.pitch(c, st)
        # rising contour: speed the second half up slightly (varispeed in two halves, crossfaded)
        h = len(c) // 2
        a = c[:h]
        b = dsp.pitch(c[h:], rise_st * rng.uniform(0.3, 1.0))
        c = np.concatenate([a, b])
        c = dsp.fade(c, rng.uniform(0.01, 0.06), 0.12)
        c = dsp.shelf(dsp.bp(c, 220, 7000, 2), 1800, 5, high=True)
        t0 = rng.uniform(-0.5, dur * 0.3)
        seg_ = c[int(max(0, -t0) * SR):]
        dsp.place(out, pan(seg_, rng.uniform(-0.95, 0.95)), max(0, t0), rng.uniform(-10, 0))
    return out


def whistle(f0: float, dur: float, seed: int, glide: bool = True) -> np.ndarray:
    """A fan's finger whistle: a near-sine with breath, a 6 Hz wobble and (optionally) the rising 'fiu' glide."""
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (1 + (0.18 * (1 - np.exp(-t / 0.07)) - 0.18 if glide else 0.0)) * (1 + 0.012 * np.sin(2 * np.pi * 6.1 * t))
    f *= 1 + 0.004 * np.cumsum(rng.standard_normal(n)) / np.sqrt(n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.08 * np.sin(2 * ph + 0.5)
    br = dsp.resonator(rng.standard_normal(n), f0, 400) * 0.6
    y = y + br / (np.abs(br).max() + 1e-9) * 0.25
    e = np.clip(t / 0.035, 0, 1) * np.clip((dur - t) / 0.12, 0, 1) * (0.85 + 0.15 * np.sin(2 * np.pi * 2.3 * t + rng.uniform(0, 6)))
    return y * e / np.abs(y).max()


@builder("HLF-SFX-04", "rugido_estadio_0s8", "one-shot 0,8 s",
         "começa cheio no 1º sample (0,000 s) e corta seco em 0,800 s")
def rugido_estadio_0s8():
    return _roar(0.8)


def _roar(dur):
    rng = np.random.default_rng(404)
    T = dur + 0.6
    out = np.zeros((int(T * SR), 2))
    out += _cheer_bank(rng, 110, T) * 1.0
    crowd = src("oga_crowdshout/crowd_shouting_0.ogg")
    for i, (off, st) in enumerate(((2.0, -1.5), (7.5, 0.0), (13.0, 1.2), (19.5, -0.6), (23.0, 2.0))):
        c = dsp.pitch(dsp.seg(crowd, off, off + T + 0.5), st)[:len(out)]
        dsp.place(out, c[:, ::(1 if i % 2 else -1)], 0, -3)
    app = src("oga_applause/applause-clapping-church-crowd-immersive.wav")
    dsp.place(out, dsp.seg(app, 18.0, 18.0 + T), 0, -9)
    dsp.place(out, dsp.seg(app, 26.0, 26.0 + T)[:, ::-1], 0, -11)
    n = len(out)
    rngn = np.random.default_rng(405)
    rum = dsp.lp(np.stack([dsp.brown(n, rngn), dsp.brown(n, rngn)], 1), 110, 2)
    out += rum / np.abs(rum).max() * np.abs(out).max() * db(-22)
    # the bowl: start the space already 'full' by pre-rolling 0.4 s of material through it, then cut
    pre = 0.4
    padded = np.vstack([out[::-1][:int(pre * SR)], out])          # mirrored pre-roll so the tail is established
    y = dsp.convolve(padded, stadium_ir(), wet=0.6, dry=0.85)[int(pre * SR):int(pre * SR) + len(out)]
    # the people nearest the mic: a few raised voices and the Brazilian stadium whistle, almost dry
    near = _cheer_bank(np.random.default_rng(406), 7, T)
    y += near * db(-2)
    for k, (t0, f0) in enumerate(((0.05, 2450.0), (0.22, 3150.0), (0.41, 2780.0), (0.0, 3500.0))):
        w_ = whistle(f0, 0.9, seed=410 + k, glide=(k % 2 == 0))
        dsp.place(y, pan(w_, (-0.6, 0.5, -0.2, 0.75)[k]), t0, (-13, -15, -14, -18)[k])
    y = dsp.match_tilt(y, {125: -13, 250: -5, 500: 0, 1000: -2, 2000: -8, 4000: -14, 8000: -24, 16000: -36})
    y = y[:int(dur * SR)]
    # eruption: full within 12 ms, a 6% swell over the first 150 ms, hard cut at the end (3 ms)
    t = np.arange(len(y)) / SR
    e = np.clip(t / 0.012, 0, 1) * (0.94 + 0.06 * np.clip(t / 0.15, 0, 1))
    y = y * e[:, None]
    return dsp.fade(y, 0, 0.003)


@builder("HLF-SFX-05", "aplauso_estadio_distante", "one-shot 9 s",
         "cresce de longe a partir de 0 s; pico estável de ~5,0 s até o fim (corte seco no editor)")
def aplauso_estadio_distante():
    rng = np.random.default_rng(505)
    T = 9.0
    n = int(T * SR)
    out = np.zeros((n, 2))
    app = src("oga_applause/applause-clapping-church-crowd-immersive.wav")
    # layer A: the recording's own natural start (a hall breaking into applause)
    dsp.place(out, dsp.seg(app, 0.0, T), 0, 0)
    # layers B-D: more of the same crowd, shifted in time and pitch, so it reads as thousands
    for off, st, g in ((12.0, -1.0, -1), (21.5, 0.8, -2), (29.0, -2.0, -3)):
        layer = dsp.pitch(dsp.seg(app, off, off + T + 0.5), st)[:n]
        dsp.place(out, layer[:, ::-1] if st > 0 else layer, 0, g)
    cheers = _cheer_bank(rng, 70, T, rise_st=2.0)
    dsp.place(out, cheers, 0, -8)
    # swell: from far to near-full over 5 s
    e = dsp.env_points(n, [(0, -26), (1.0, -18), (3.0, -7), (5.0, 0), (T, 0.5)])
    out = dsp.apply_env(out, e)
    # distance: the highs go first, then the bowl
    out = dsp.lp(out, 3200, 2)
    out = dsp.convolve(out, stadium_ir(seed=51), wet=1.0, dry=0.45)[:n]
    out = dsp.hp(out, 70, 2)
    return dsp.fade(out, 0.05, 0.08)


# -------------------------------------------------------------------------------------------- one pair of hands

CLAP_SRC = "oga_welldone/Well_Done_CCBY3.flac"
CLAP_ONSETS = (3.432, 1.089, 2.235, 0.064)  # the four cleanest single claps in the take (30-42 dB over the room)


def single_clap(k: int) -> np.ndarray:
    """One real clap, gated tight to drop the source room and the other people, onset at sample 0."""
    x = dsp.mono(src(CLAP_SRC))
    o = CLAP_ONSETS[k]
    c = x[int((o - 0.004) * SR):int((o + 0.11) * SR)]
    # snap to the real transient, measured the way onsets.py measures it (HF rise to 25 %), 0,5 ms of lead
    c = dsp.hp(c, 140, 2)
    i = hf_onset(c)
    c = c[max(0, i - int(0.0005 * SR)):]
    c = c / np.abs(c).max()
    t = np.arange(len(c)) / SR
    g = np.clip(1 - (t - 0.045) / 0.05, 0, 1) ** 2      # gate: keep the clap body, close by 95 ms
    return c * g


def small_room_ir():
    return dsp.room_ir(0.30, dims=(3.6, 3.0, 2.6), src=(1.5, 1.4, 1.3), mic=(2.4, 1.9, 1.4), absorb=0.55,
                       order=6, seed=61, hf_damp=1.6)


def claps_at(times, gains_db, T, room="small", seed=0):
    out = np.zeros((int(T * SR), 2))
    order = [0, 1, 2, 3]
    for j, (t, g) in enumerate(zip(times, gains_db)):
        c = single_clap(order[j % 3])
        dsp.place(out, pan(c, 0.04 * (-1) ** j), t, g)
    if room == "small":
        out = dsp.convolve(out, small_room_ir(), wet=0.32, dry=1.0)[:len(out)]
    else:
        ir = dsp.hall_ir(1.5, 0.02, seed=62 + seed, hf_damp=2.0)
        out = dsp.convolve(dsp.lp(out, 7000, 1), ir, wet=0.75, dry=0.8)[:len(out)]
    return dsp.fade(out, 0, 0.06)


@builder("HLF-SFX-06a", "palma_1", "one-shot", "transiente da palma em 0,020 s")
def palma_1():
    return claps_at([0.02], [0], 0.6)


@builder("HLF-SFX-06b", "palma_2", "one-shot", "transiente da palma em 0,020 s")
def palma_2():
    out = np.zeros((int(0.6 * SR), 2))
    c = single_clap(1)
    dsp.place(out, c, 0.02, 0)
    return dsp.fade(dsp.convolve(out, small_room_ir(), wet=0.32)[:len(out)], 0, 0.06)


@builder("HLF-SFX-06c", "palma_3", "one-shot", "transiente da palma em 0,020 s")
def palma_3():
    out = np.zeros((int(0.6 * SR), 2))
    c = single_clap(2)
    dsp.place(out, c, 0.02, 0)
    return dsp.fade(dsp.convolve(out, small_room_ir(), wet=0.32)[:len(out)], 0, 0.06)


@builder("HLF-SFX-06d", "palmas_tres_0s3", "one-shot",
         "palmas em 0,000 / 0,300 / 0,600 s (o espaçamento da vinheta)")
def palmas_tres_0s3():
    return claps_at([0.0, 0.3, 0.6], [0, -0.3, -2.0], 1.1)


@builder("HLF-SFX-06e", "palmas_tres_10q", "one-shot",
         "palmas nos quadros 0 / 10 / 20 a 24 fps (0,000 / 0,417 / 0,833 s): F15 f312/322/332, F06A f100/110/120")
def palmas_tres_10q():
    return claps_at([0.0, 10 * FRAME, 20 * FRAME], [0, -0.3, -2.0], 1.35)


@builder("HLF-SFX-06f", "palmas_quatro_auditorio", "one-shot",
         "quatro palmas lentas no auditório vazio, em 0,00 / 0,68 / 1,36 / 2,04 s (Ad 1, gesto 6–9 s)")
def palmas_quatro_auditorio():
    return claps_at([0.0, 0.68, 1.36, 2.04], [0, -0.8, -0.3, -0.5], 3.4, room="hall")


# -------------------------------------------------------------------------------------------- fire

@builder("HLF-SFX-07", "fosforo_fsst", "one-shot", "início do risco (a cabeça do fósforo raspa) em 0,020 s")
def fosforo_fsst():
    """Match strike: the head scraping the striker, the flare, a short burning hiss."""
    T = 1.1
    out = np.zeros((int(T * SR), 2))
    ign = dsp.mono(src("oga_ignition/ignition.flac"))
    # the recording is a real matchstick sped up by its author: slow it back by 1,25x for a natural flare
    ign = dsp.stretch_speed(ign, 1.25)
    # scrape: the first, grainy part of the strike, sharpened
    scr = dsp.hp(ign[int(0.30 * SR):int(0.40 * SR)], 1800, 2)
    ts = np.arange(len(scr)) / SR
    scr = scr / np.abs(scr).max() * np.clip(ts / 0.001, 0, 1) * (0.55 + 0.45 * np.exp(-ts / 0.02)) \
        * np.clip((ts[-1] - ts) / 0.03, 0, 1)                       # the head bites the striker: 'tch', then rasp
    dsp.place(out, scr, 0.020, -2)
    knife = dsp.hp(dsp.mono(src(K_RPG + "knifeSlice.ogg")), 2500, 2)
    dsp.place(out, align(knife, 0.020), 0, -8)
    # flare: the body of the ignition, fast attack, decaying hiss
    fl = dsp.hp(ign[int(0.45 * SR):int(1.10 * SR)], 260, 2)
    fl = fl / np.abs(fl).max()
    t = np.arange(len(fl)) / SR
    fl = fl * (np.clip(t / 0.012, 0, 1) * np.exp(-t / 0.20)) * np.clip((t[-1] - t) / 0.25, 0, 1) ** 2
    dsp.place(out, fl, 0.065, -1)
    # the small low 'puff' of the phosphorus catching
    n = int(0.12 * SR); t = np.arange(n) / SR
    wh = dsp.bp(noise(n, 71), 150, 600, 2) * np.sin(np.pi * np.clip(t / 0.12, 0, 1))
    dsp.place(out, wh / np.abs(wh).max(), 0.06, -20)
    out = dsp.convolve(out, small_room_ir(), wet=0.12)[:len(out)]
    return dsp.fade(gate_pre(out, 0.020), 0, 0.15)


def _crackle_grains():
    """Real crackle grains: transients from the two CC0 fire recordings, high-passed (a wood wick has no roar)."""
    import librosa
    grains = []
    for rel, hpf in (("oga_fire1/fire-1.wav", 600), ("oga_fireplace/fire.wav", 500)):
        x = dsp.mono(src(rel))
        x = dsp.hp(x, hpf, 4)
        on = librosa.onset.onset_detect(y=x.astype(np.float32), sr=SR, units="samples", hop_length=256,
                                        backtrack=True, delta=0.08)
        for o in on:
            g = x[max(0, o - 48):o + int(0.05 * SR)]
            if len(g) < 200:
                continue
            pk = np.abs(g).max()
            bg = np.sqrt(np.mean(x[max(0, o - 4800):max(1, o - 480)] ** 2)) + 1e-9
            if pk / bg > 6:
                t = np.arange(len(g)) / SR
                grains.append((pk / bg, g / pk * np.exp(-np.maximum(t - 0.004, 0) / 0.012)))
    grains.sort(key=lambda z: -z[0])
    return [g for _, g in grains[:60]]


def _crackle_loop(L: float, seed: int, rate: float = 7.0, pop_every: float = 2.3):
    rng = np.random.default_rng(seed)
    n = int(L * SR)
    out = np.zeros((n, 2))
    # bed: the real fireplace, high-passed hard: what is left is the fine fizz of a small flame
    fp = src("oga_fireplace/fire.wav")
    bed = dsp.hp(dsp.seg(fp, 3.0, 3.0 + L + 0.6), 900, 4)
    xf = int(0.6 * SR)
    loop = bed[:n].copy()
    w = np.linspace(0, 1, xf)[:, None]
    loop[:xf] = bed[n:n + xf] * (1 - w) + bed[:xf] * w   # crossfade the overhang onto the start
    out += loop / np.abs(loop).max() * db(-12)
    grains = _crackle_grains()
    t = 0.0
    while t < L:
        t += rng.exponential(1.0 / rate)
        g = grains[rng.integers(len(grains))]
        g = dsp.pitch(g, rng.uniform(-2, 3))
        gain = -24 + 18 * rng.random() ** 2.5                     # mostly small, sometimes bigger
        circ_place(out, pan(g, rng.uniform(-0.25, 0.25)), t, gain)
    t = 0.0
    while t < L:                                                   # the occasional real pop
        t += rng.uniform(0.6, 1.4) * pop_every
        g = grains[rng.integers(min(12, len(grains)))]
        circ_place(out, pan(g, rng.uniform(-0.2, 0.2)), t, rng.uniform(-3, 0))
    # micro-crackle: very short ticks, the 'paper' texture of a wood wick
    t = 0.0
    while t < L:
        t += rng.exponential(1 / 22.0)
        k = int(rng.uniform(0.0004, 0.0018) * SR)
        tick = dsp.hp(rng.standard_normal(k + 64), 3000, 2)[64:] * np.hanning(k)
        circ_place(out, pan(tick, rng.uniform(-0.3, 0.3)), t, -30 + 10 * rng.random() ** 3)
    out = circ_conv(out, small_room_ir(), wet=0.10)
    return out


@builder("HLF-SFX-08", "crepitar_pavio_loop", "loop 12 s", "loop sem emenda; sem ponto de sincronia")
def crepitar_pavio_loop():
    return _crackle_loop(12.0, seed=808)


# -------------------------------------------------------------------------------------------- bells

BB6 = 1864.655  # B♭6 — the bell sits in the fanfarra's key


def bell_strike(f0=BB6 / 2, T=3.4, vel=1.0, seed=0, detune_cents=0.0):
    """Struck bell by modal synthesis (Risset's bell partials), tuned so the strong 2,0 partial is B♭6.
    A real metallic strike (Kenney impactBell, high-passed) gives the attack its 'tink'."""
    rng = np.random.default_rng(900 + seed)
    f0 = f0 * 2 ** (detune_cents / 1200)
    n = int(T * SR)
    t = np.arange(n) / SR
    ratios = [0.56, 0.56, 0.92, 0.92, 1.19, 1.70, 2.00, 2.74, 3.00, 3.76, 4.07]
    offs = [0, 1.0, 0, 1.7, 0, 0, 0, 0, 0, 0, 0]
    amps = [1.0, 0.67, 1.0, 1.8, 2.67, 1.67, 1.46, 1.33, 1.33, 1.0, 1.33]
    durs = [1.0, 0.9, 0.65, 0.55, 0.325, 0.35, 0.25, 0.2, 0.15, 0.1, 0.075]
    y = np.zeros(n)
    for r, o, a, d in zip(ratios, offs, amps, durs):
        f = r * f0 + o
        if f > SR / 2.2:
            continue
        y += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 2 * np.pi)) * np.exp(-t / (d * T / 4.6))
    y *= np.clip(t / 0.0015, 0, 1) * np.clip((T - t) / 0.6, 0, 1) ** 2   # never truncated mid-ring
    y /= np.abs(y).max()
    strike = dsp.hp(dsp.mono(src(K_IMP + "impactBell_heavy_002.ogg")), 2500, 2)
    strike = strike[int(first_onset(strike) * SR):][:int(0.03 * SR)]
    strike = strike / np.abs(strike).max() * np.exp(-np.arange(len(strike)) / SR / 0.006)
    y[:len(strike)] += strike * 0.35
    return y * vel


def bells(times, T=3.6, seed=0):
    out = np.zeros((int(T * SR), 2))
    vels = [1.0, 0.92, 0.97]
    for j, t in enumerate(times):
        b = bell_strike(vel=vels[j % 3], seed=seed + j, detune_cents=(-2, 1.5, -0.5)[j % 3])
        dsp.place(out, pan(b, 0.1), t, 0)
    out = dsp.convolve(out, dsp.hall_ir(1.9, 0.03, seed=91), wet=0.35, dry=1.0)[:len(out)]
    return dsp.fade(out, 0, 0.4)


@builder("HLF-SFX-09", "sino_teatro", "one-shot", "golpe do sino em 0,000 s")
def sino_teatro():
    return bells([0.0])


@builder("HLF-SFX-09a", "sinal_1_sino", "one-shot (F06C 07.05)", "sino em f0 (0,000 s)")
def sinal_1_sino():
    return bells([0.0], seed=10)


@builder("HLF-SFX-09b", "sinal_2_sinos", "one-shot (F06C 08.05)", "sinos em f0 e f8 (0,000 / 0,333 s)")
def sinal_2_sinos():
    return bells([0.0, 8 * FRAME], seed=10)


@builder("HLF-SFX-09c", "sinal_3_sinos", "one-shot (F06C 09.05)", "sinos em f0, f8 e f16 (0,000 / 0,333 / 0,667 s)")
def sinal_3_sinos():
    return bells([0.0, 8 * FRAME, 16 * FRAME], seed=10)


# -------------------------------------------------------------------------------------------- the house

@builder("HLF-SFX-10", "tosse_plateia", "one-shot", "início da tosse em 0,020 s")
def tosse_plateia():
    """One audience cough, a few rows back, in the silence of a full house."""
    x = dsp.mono(src("oga_cough/old-man-cough.flac"))
    a = x[int(2.925 * SR):int(3.16 * SR)]
    b = x[int(3.365 * SR):int(3.60 * SR)]
    a = dsp.fade(a, 0.002, 0.04); b = dsp.fade(b, 0.002, 0.05)
    T = 2.4
    out = np.zeros(int(T * SR))
    dsp.place(out, align(a, 0.020, -24), 0, 0)
    dsp.place(out, align(b, 0.020 + 0.26, -24), 0, -5)
    out = dsp.lp(dsp.hp(out, 120, 2), 6000, 2)
    y = dsp.convolve(pan(out, -0.35), dsp.hall_ir(1.6, 0.03, seed=101), wet=0.7, dry=0.75)[:int(T * SR)]
    return dsp.fade(gate_pre(y, 0.020), 0, 0.3)


@builder("HLF-SFX-11", "elevador_hidraulico_1s", "one-shot 1,0 s", "o motor parte em 0,000 s")
def elevador_hidraulico_1s():
    """Stage lift: a real compressor drone pitched down + the pump motor's whine spinning up + fluid hiss."""
    T = 1.0
    n = int(T * SR)
    t = np.arange(n) / SR
    d = src("oga_shop/x/TheShopCollection_convenience_store_drinks_fridge_drone.wav")
    drone = dsp.pitch(dsp.seg(d, 2.0, 4.0), -5)[:n]
    drone = dsp.bp(drone, 45, 1200, 2)
    f = 150 + 70 * (1 - np.exp(-t / 0.12))                       # motor spin-up
    ph = 2 * np.pi * np.cumsum(f) / SR
    whine = sum((0.7 ** k) * np.sin(k * ph) for k in range(1, 9))
    whine *= 1 + 0.25 * np.sin(2 * np.pi * 27 * t)                 # pump pulsation
    hiss = dsp.bp(noise(n, 111), 900, 3500, 2)
    y = dsp.stereo(drone / np.abs(drone).max() * db(-4))
    y += pan(whine / np.abs(whine).max() * db(-10), 0.1)
    y += pan(hiss / np.abs(hiss).max() * db(-26), -0.1)
    e = np.clip(t / 0.06, 0, 1) * np.clip((T - t) / 0.12, 0, 1)
    y = dsp.apply_env(y, e)
    return dsp.convolve(y, dsp.hall_ir(1.6, 0.03, seed=112), wet=0.18)[:n]


@builder("HLF-SFX-12", "ima_case", "one-shot", "contato da tampa com os ímãs em 0,050 s")
def ima_case():
    """O CASE closing: the lid's air cushion, board on board, and the magnets' small hard snap."""
    T = 0.7
    out = np.zeros((int(T * SR), 2))
    n = int(0.05 * SR); t = np.arange(n) / SR
    air = dsp.bp(noise(n, 121), 200, 1500, 2) * (t / 0.05) ** 2
    dsp.place(out, air / np.abs(air).max(), 0.0, -20)
    book = src(K_RPG + "bookClose.ogg")
    dsp.place(out, align(dsp.pitch(book, 2), 0.050), 0, 0)
    snap = dsp.hp(dsp.mono(src(K_UI + "click3.ogg")), 1500, 2)
    dsp.place(out, align(snap, 0.0505), 0, -9)
    out = dsp.convolve(out, small_room_ir(), wet=0.18)[:len(out)]
    return dsp.fade(out, 0.002, 0.1)


@builder("HLF-SFX-13", "pulseira_fecho", "one-shot", "o clique final do fecho em 0,200 s")
def pulseira_fecho():
    """A PULSEIRA: the woven band pulled through the bead, then the one-way clasp clicks shut."""
    T = 0.6
    out = np.zeros((int(T * SR), 2))
    cl = dsp.hp(dsp.mono(src(K_RPG + "cloth1.ogg")), 1200, 2)
    cl = cl[:int(0.17 * SR)]
    cl = dsp.fade(cl / np.abs(cl).max(), 0.02, 0.05)
    dsp.place(out, cl, 0.02, -14)
    c1 = dsp.hp(dsp.mono(src(K_UI + "switch7.ogg")), 1000, 2)
    c2 = dsp.hp(dsp.mono(src(K_UI + "click2.ogg")), 1000, 2)
    c2 = c2[:hf_onset(c2) + int(0.025 * SR)]
    c2 = dsp.fade(c2, 0, 0.008)                                   # keep the press, drop the mouse's release
    dsp.place(out, align(c1, 0.178), 0, -10)
    dsp.place(out, align(c2, 0.200), 0, 0)
    out = dsp.convolve(out, small_room_ir(), wet=0.12)[:len(out)]
    return dsp.fade(out, 0.002, 0.08)


@builder("HLF-SFX-14", "selo_papel_rrrip", "one-shot", "início do rasgo em 0,020 s")
def selo_papel_rrrip():
    """The paper seal torn open: a real paper rip extended by a real wrapper tear."""
    T = 0.9
    out = np.zeros((int(T * SR), 2))
    rng = np.random.default_rng(1414)
    rip = dsp.mono(src("oga_paper/x/WAV/Paper Ripped - 1.wav"))
    rip = dsp.seg(rip, 0.27, 0.40)                              # the 130 ms of real tearing in the take
    tear = dsp.mono(src(K_CAS + "cards-pack-open-1.ogg"))
    tear = dsp.seg(tear, 0.37, 0.47)
    # the seal lets go: one sharp first tear (real), then the fibres keep parting for ~300 ms — overlapping
    # 18-35 ms grains of the real rip, accelerating then easing off, so it reads as ONE continuous 'rrrip'
    tt = 0.020
    first = True
    while tt < 0.30:
        u = (tt - 0.020) / 0.28
        L_ = int(rng.uniform(0.018, 0.035) * SR)
        i0 = rng.integers(0, len(rip) - L_)
        g = dsp.pitch(rip[i0:i0 + L_] * np.hanning(L_), rng.uniform(-1.5, 1.5) - 2 * u)
        if first:
            g = g[hf_onset(g):]                                  # the very first grain starts ON the sync point
            first = False
        dsp.place(out, pan(g, rng.uniform(-0.15, 0.15)), tt, -7 + 6 * np.sin(np.pi / 2 * min(1, u * 1.6)) + rng.uniform(-2, 1))
        tt += L_ / SR * rng.uniform(0.35, 0.6)
    # '…ip': the last fibres let go
    dsp.place(out, align(dsp.fade(tear, 0.001, 0.03), 0.300), 0, -5)
    out = dsp.hp(out, 150, 2)
    out = dsp.convolve(out, small_room_ir(), wet=0.14)[:len(out)]
    return dsp.fade(gate_pre(out, 0.020), 0, 0.12)


@builder("HLF-SFX-15", "tom_de_sala_loop", "loop 12 s", "loop sem emenda; use bem baixo (ver ganho sugerido)")
def tom_de_sala_loop():
    """Small-room tone: periodic shaped noise (an FFT-domain spectrum, so it loops perfectly) + faint mains hum."""
    L = 12.0
    n = int(L * SR)
    rng = np.random.default_rng(1515)
    f = np.fft.rfftfreq(n, 1 / SR)
    mag = np.ones_like(f)
    ff = np.maximum(f, 1.0)
    mag *= 1 / np.sqrt(ff / 100.0) ** 1.0                              # pinkish
    mag *= 1 / (1 + (ff / 3500.0) ** 4)                                # air absorbs the top
    mag *= 1 / (1 + (25.0 / ff) ** 6)                                  # nothing below 25 Hz
    mag *= 1 + 1.2 * np.exp(-((np.log2(ff / 140.0)) ** 2) / 0.5)        # a soft ventilation rumble
    out = np.zeros((n, 2))
    for ch in range(2):
        ph = rng.uniform(0, 2 * np.pi, len(f))
        y = np.fft.irfft(mag * np.exp(1j * ph), n)
        out[:, ch] = y / np.abs(y).max()
    t = np.arange(n) / SR
    hum = 0.012 * np.sin(2 * np.pi * 60 * t) + 0.008 * np.sin(2 * np.pi * 120 * t + 1) \
        + 0.003 * np.sin(2 * np.pi * 180 * t + 2)                       # 60 Hz mains (Brazil), whole cycles in 12 s
    out += hum[:, None]
    out = circ_conv(out, small_room_ir(), wet=0.4)
    return out


# -------------------------------------------------------------------------------------------- the sonic identity

IDENT: dict = {}


def ident(fid, name, sync):
    def deco(fn):
        IDENT[fn.__name__] = dict(fn=fn, id=fid, name=name, sync=sync)
        return fn
    return deco


@ident("HLF-ID-01", "vinheta_ovacao_de_uma_pessoa_so_2s0",
       "CLAC 0,000 · estádio 0,100–0,900 (corte seco) · palmas 1,100 / 1,400 / 1,700 · fim 2,000")
def vinheta():
    T = 2.0
    out = np.zeros((int(T * SR), 2))
    # 0,0 s: CLAC (switch transient on the very first sample)
    r = _roar(0.8)
    rp = np.abs(r).max()
    c = _clac(0.0, 0.9)
    dsp.place(out, c * (rp / np.abs(c).max()) * db(-1), 0.0, 0)      # the CLAC hits as hard as the stadium peaks
    # 0,1-0,9 s: the stadium
    dsp.place(out, r, 0.100, 0)
    # hard cut at 0,9: everything (roar, clac tail, hall) stops dead
    k = int(0.900 * SR)
    out[k:] = 0
    out[k - int(0.003 * SR):k] *= np.linspace(1, 0, int(0.003 * SR))[:, None]
    # small dry room from the cut: its tone, very low, and one pair of hands
    rt = tom_de_sala_loop()[:len(out) - k]
    rt = rt / np.abs(rt).max() * rp * db(-50)
    out[k:] += dsp.fade(rt, 0.004, 0.1)
    cl = claps_at([0.0, 0.3, 0.6], [0, -0.3, -2.0], 0.9)
    # one pair of hands, close and dry: its peaks as high as the stadium's, its loudness far smaller
    dsp.place(out, cl * (rp / np.abs(cl).max()) * db(-1), 1.100, 0)
    return dsp.fade(out, 0, 0.04)


@ident("HLF-ID-02", "crepitar_para_aplauso_morph",
       "0,0–0,5 só o pavio · 0,5–2,0 a fusão (1,5 s) · 2,0–5,0 o aplauso distante crescendo")
def morph():
    """The candle applauds her: the wick's crackle turns into distant applause over 1,5 s. Underneath a plain
    equal-power crossfade, a bridge of grains whose rate rises and whose timbre slides from crackle to clap."""
    T = 5.0
    n = int(T * SR)
    t = np.arange(n) / SR
    x0, x1 = 0.5, 2.0
    m = np.clip((t - x0) / (x1 - x0), 0, 1)
    crack = _crackle_loop(T, seed=2020)[:n]
    crack = crack / np.sqrt(np.mean(crack ** 2)) * db(-3)
    app = aplauso_estadio_distante()
    app = app[int(2.4 * SR):int(2.4 * SR) + n]                       # start where the swell is already moving
    app = app / np.sqrt(np.mean(app[int(1.5 * SR):] ** 2))
    a_env = dsp.env_points(n, [(0, -6), (x1, 0), (T, 3)])
    out = crack * np.cos(m * np.pi / 2)[:, None] + app * (np.sin(m * np.pi / 2) * a_env)[:, None]
    # the bridge: crackle grains becoming claps
    rng = np.random.default_rng(2021)
    grains = _crackle_grains()
    claps = [single_clap(k) for k in range(4)]
    tt = x0
    while tt < x1 + 0.2:
        mm = float(np.clip((tt - x0) / (x1 - x0), 0, 1))
        rate = 8 + 46 * mm ** 1.5
        tt += rng.exponential(1 / rate)
        g = grains[rng.integers(len(grains))]
        c = dsp.lp(claps[rng.integers(4)], 4500 - 2000 * mm, 2)
        L_ = max(len(g), len(c))
        ev = np.zeros(L_)
        ev[:len(g)] += g * (1 - mm)
        ev[:len(c)] += c * mm * 0.8
        dsp.place(out, pan(ev, rng.uniform(-0.6 * mm - 0.15, 0.6 * mm + 0.15)), tt,
                  -3 - 14 * mm - 6 * rng.random())
    return dsp.fade(out, 0.01, 0.1)


# ============================================================================================ runner

def run(names=None):
    os.makedirs(os.path.join(SOM, "sfx"), exist_ok=True)
    os.makedirs(os.path.join(SOM, "identidade"), exist_ok=True)
    man_path = os.path.join(SOM, "manifesto_sfx.json")
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    import onsets as ON
    jobs = [(k, r, "sfx") for k, r in REG.items()] + [(k, r, "identidade") for k, r in IDENT.items()]
    for key, r, folder in jobs:
        if names and key not in names:
            continue
        x = r["fn"]()
        if folder == "sfx":
            y, info = dsp.norm_sfx(x, target_m=-20.0, tp_ceiling=-1.0)
            norm = "max momentary −20 LUFS-M, ≤ −1 dBTP (ganho reduzido, sem limitador)"
        else:
            y, info = dsp.norm_mix(x, target_i=-14.0, tp_ceiling=-1.0)
            norm = "−14 LUFS integrado, ≤ −1 dBTP (limitador true-peak)"
        fn = f"{r['id']}_{r['name']}.wav"
        path = os.path.join(SOM, folder, fn)
        dsp.write(path, y)
        on = [round(v, 4) for v in ON.onsets(path)]
        print(f"{fn:52s} {len(y)/SR:6.3f}s  M {info['lufs_m_max'] if 'lufs_m_max' in info else info['lufs_i']:6.1f}"
              f"  TP {info['true_peak_dbtp']:5.1f}  onsets {on[:8]}", flush=True)
        man[f"{folder}/{fn}"] = dict(id=r["id"], tipo=r.get("kind", "identidade"), duracao_s=round(len(y) / SR, 4),
                                     sincronia=r["sync"], onsets_medidos_s=on[:40], normalizacao=norm, **info)
    json.dump(dict(sorted(man.items())), open(man_path, "w"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    run(sys.argv[1:] or None)
