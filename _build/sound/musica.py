#!/usr/bin/env python
"""HOLOFOTE · musica.py — 'FANFARRA HOLOFOTE', an original school-fanfarra drumline at 120 BPM (20 s = 10 bars of 4/4).

Composed and synthesised entirely in code for SOL Estúdio (the studio owns it; no sample of any recording, no melody,
no quoted rhythm signature of any song). Drums are modal syntheses (membrane modes + stick + snare wires) with
round-robin variation and human timing, so no two hits are identical.

    /home/user/venvs/web/bin/python -I musica.py            # stems + mix + pieces + edit points
    /home/user/venvs/web/bin/python -I musica.py --metais   # ALSO renders the experimental brass stem into _tmp/
                                                             # (NOT delivered: see LEIA_ME.md)
Writes 04_FILMES/som/musica/.
"""
from __future__ import annotations

import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dsp  # noqa: E402
from dsp import SR, db  # noqa: E402

KIT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(KIT, "04_FILMES", "som", "musica")
TMP = os.path.join(HERE, "_tmp")
BPM = 120.0
BEAT = 60.0 / BPM          # 0,5 s
BAR = 4 * BEAT             # 2,0 s
BARS = 10
LEN = BARS * BAR           # 20 s
MEMBRANE = [1.0, 1.594, 2.136, 2.296, 2.653, 2.918, 3.156, 3.501]   # circular membrane mode ratios


# ============================================================================================ instruments

def snare(vel=1.0, rng=None, tune=1.0, kind="caixa", rim=False):
    """Marching snare (caixa): tight head modes with a pitch drop, stick crack, snare wires. Mono, ~0,45 s."""
    rng = rng or np.random.default_rng()
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f1 = (335.0 if kind == "caixa" else 245.0) * tune * (1 + rng.uniform(-0.012, 0.012))
    drop = 1 + 0.10 * vel * np.exp(-t / 0.006)                 # the head is stretched by the stroke
    head = np.zeros(n)
    pos = rng.uniform(0.0, 1.0)                                # where the stick lands changes which modes speak
    for k, r in enumerate(MEMBRANE):
        dec = (0.045 if kind == "caixa" else 0.07) / (1 + 0.35 * k)
        a = (1.0, 0.7, 0.55, 0.4, 0.3, 0.22, 0.15, 0.1)[k] * (1 + 0.6 * vel * (k > 2))
        a *= 0.45 + 1.1 * abs(np.sin(np.pi * (k + 1) * (0.15 + 0.3 * pos)))
        ph = 2 * np.pi * np.cumsum(f1 * r * drop) / SR + rng.uniform(0, 6.28)
        head += a * np.sin(ph) * np.exp(-t / dec)
    head /= np.abs(head).max()
    # stick: a 1,5 ms crack, brighter when harder
    k = int(0.0025 * SR)
    stick = rng.standard_normal(k) * np.exp(-np.arange(k) / (0.0006 * SR))
    stick = dsp.bp(np.pad(stick, (0, 64)), 1800, 9000 if vel > 0.5 else 6000, 2)[:k + 64]
    # wires: noise, gated by the head's motion, decaying
    wires = rng.standard_normal(n)
    wires = dsp.bp(wires, 2200, 9500, 2) + 0.4 * dsp.bp(wires, 900, 2200, 2)
    wd = (0.048 if kind == "caixa" else 0.075) * (0.8 + 0.4 * vel)
    wires *= np.exp(-t / wd) * (1 - np.exp(-t / 0.0015))
    wires /= np.abs(wires).max()
    y = head * (0.75 if kind == "caixa" else 1.0) + wires * (0.85 + 0.3 * vel) * (1.0 if kind == "caixa" else 0.6)
    y[:len(stick)] += stick / (np.abs(stick).max() + 1e-12) * (0.5 + 0.9 * vel)
    if rim:                                                   # rimshot: a hard 'ping' of the hoop
        ping = np.sin(2 * np.pi * 920 * t) * np.exp(-t / 0.02) + 0.5 * np.sin(2 * np.pi * 1730 * t) * np.exp(-t / 0.012)
        y += ping * 0.55
    y = dsp.lp(y, 4500 + 9000 * vel, 1)                         # softer strokes are darker
    return y / np.abs(y).max() * vel


def bass(vel=1.0, rng=None, f0=72.0, dec=0.32, kind="bumbo"):
    """Marching bass (bumbo) / surdo: felt mallet thud, low mode with a pitch drop, shell modes."""
    rng = rng or np.random.default_rng()
    n = int((dec * 7.0) * SR)
    t = np.arange(n) / SR
    f = f0 * (1 + rng.uniform(-0.01, 0.01)) * (1 + 0.35 * vel * np.exp(-t / 0.018))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / dec)
    for r, a, d in ((1.594, 0.45, 0.4), (2.136, 0.32, 0.3), (2.296, 0.22, 0.25), (2.653, 0.15, 0.2), (2.918, 0.1, 0.18)):
        y += a * np.sin(r * ph + rng.uniform(0, 6.28)) * np.exp(-t / (dec * d))
    k = int(0.012 * SR)
    mallet = dsp.lp(rng.standard_normal(k + 64), 1400 if kind == "bumbo" else 900, 2)[:k] * np.exp(-np.arange(k) / (0.003 * SR))
    y[:k] += mallet / (np.abs(mallet).max() + 1e-12) * (0.35 + 0.4 * vel)
    skin = dsp.bp(rng.standard_normal(n), 150, 900, 2) * np.exp(-t / 0.035)
    y += skin / np.abs(skin).max() * 0.3
    return y / np.abs(y).max() * vel


def cymbal(vel=1.0, rng=None, choke=None):
    """Pratos (hand crash pair): a dense inharmonic partial cloud + noise, highs dying first; `choke` in s."""
    rng = rng or np.random.default_rng()
    T = 3.2 if choke is None else choke + 0.08
    n = int(T * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    fr = np.exp(rng.uniform(np.log(420), np.log(16500), 700))
    for i in range(0, len(fr), 50):
        f = fr[i:i + 50][:, None]
        a = np.exp(-((np.log(f / 4500)) ** 2) / 1.6) * rng.uniform(0.3, 1.0, f.shape)
        d = 1.6 * (1200 / f) ** 0.45
        drift = 1 + 0.004 * np.exp(-t[None, :] / 0.3)           # modes sag slightly as the plate calms
        y += (a * np.sin(2 * np.pi * f * drift * t[None, :] + rng.uniform(0, 6.28, f.shape)) * np.exp(-t[None, :] / d)).sum(0)
    nz = dsp.hp(rng.standard_normal(n), 2500, 2) * np.exp(-t / 0.5)
    y = y / np.abs(y).max() + 0.9 * nz / np.abs(nz).max()
    y *= np.clip(t / 0.002, 0, 1)
    # the two plates' first contact: a short bright smear
    y[:int(0.01 * SR)] *= np.linspace(1.6, 1.0, int(0.01 * SR))
    if choke is not None:
        y *= np.clip((choke + 0.06 - t) / 0.06, 0, 1) ** 2
    y = dsp.hp(y, 350, 2)
    return y / np.abs(y).max() * vel


# ============================================================================================ score

class Score:
    """Hit list: (time s, instrument, velocity, extra)."""

    def __init__(self, seed=120):
        self.rng = np.random.default_rng(seed)
        self.hits = []

    def at(self, bar, beat, sub=0.0):  # bar 1-based, beat 1-based, sub in beats
        return (bar - 1) * BAR + (beat - 1 + sub) * BEAT

    def hit(self, t, inst, vel, **kw):
        j = {"caixa": 0.0025, "tarol": 0.003, "bumbo": 0.003, "surdo": 0.004, "pratos": 0.004}[inst]
        self.hits.append((max(0.0, t + self.rng.normal(0, j)), inst, float(np.clip(vel * (1 + self.rng.normal(0, 0.06)), 0.05, 1.0)), kw))

    def roll(self, t0, t1, inst, v0, v1, rate=22.0):
        """Open double-stroke roll: diddles, the second stroke of each pair a touch softer."""
        t = t0
        i = 0
        while t < t1:
            u = (t - t0) / max(t1 - t0, 1e-6)
            v = v0 + (v1 - v0) * u ** 1.6
            self.hit(t, inst, v * (0.88 if i % 2 else 1.0))
            t += 1.0 / rate
            i += 1


def compose(sc: Score):
    A = sc.at
    # bars 1-2 · RUFO DE ENTRADA: the snare roll rises from pp; bumbo answers on bar 2 beats 1 and 3
    sc.roll(A(1, 1), A(2, 4, 0.5), "caixa", 0.07, 0.95, rate=21.0)
    sc.roll(A(2, 1), A(2, 4, 0.5), "tarol", 0.15, 0.8, rate=17.0)
    for b in (1, 3):
        sc.hit(A(2, b), "bumbo", 0.6)
    sc.hit(A(2, 4, 0.5), "surdo", 0.85)
    # bars 3-8 · MARCHA: bumbo on 1 and 3 (with a pickup), surdo on 2 and 4, caixa backbeat + sixteenths
    for bar in range(3, 9):
        sc.hit(A(bar, 1), "bumbo", 1.0 if bar in (3, 5, 7) else 0.9)
        sc.hit(A(bar, 3), "bumbo", 0.85)
        sc.hit(A(bar, 3, 0.75), "bumbo", 0.55)
        for b in (2, 4):
            sc.hit(A(bar, b), "surdo", 0.8)
        # caixa: sixteenth grid with accents on 2 and 4, a ghosted texture between
        for b in range(1, 5):
            for s in range(4):
                if bar == 8 and b >= 3:
                    continue
                acc = (s == 0 and b in (2, 4))
                v = 0.95 if acc else (0.32 if s % 2 else 0.45)
                if (b, s) in ((1, 1), (3, 1)) and bar % 2:
                    continue          # breathe: drop two notes in odd bars
                sc.hit(A(bar, b, s / 4), "caixa", v, rim=acc and bar >= 5)
        # tarol: the off-beat 'chick' that makes it a fanfarra, not a rock beat
        for b in range(1, 5):
            sc.hit(A(bar, b, 0.5), "tarol", 0.5)
        # pratos: crash on the phrase starts, choke 'tchk' on 2 and 4 from bar 5
        if bar in (3, 5, 7):
            sc.hit(A(bar, 1), "pratos", 0.85)
        if bar >= 5:
            for b in (2, 4):
                sc.hit(A(bar, b), "pratos", 0.45, choke=0.11)
    # bar 8 beats 3-4 · VIRADA: sixteenth-note fill crescendo into bar 9
    for i in range(8):
        sc.hit(A(8, 3, i / 4), "caixa", 0.55 + 0.05 * i, rim=(i == 7))
        if i % 2 == 0:
            sc.hit(A(8, 3, i / 4), "tarol", 0.6 + 0.05 * i)
    # bar 9 · BREQUE: four unison hits, then silence on 4& for a breath
    for b in (1, 2, 3, 4):
        sc.hit(A(9, b), "caixa", 1.0, rim=True)
        sc.hit(A(9, b), "tarol", 0.9)
        sc.hit(A(9, b), "bumbo", 1.0)
        sc.hit(A(9, b), "surdo", 0.9)
        sc.hit(A(9, b), "pratos", 0.7 if b < 4 else 0.9, choke=(0.12 if b < 4 else None))
    # bar 10 · FINAL: a short roll into one big unison button on beat 2, ring out to 20,0 s
    sc.roll(A(9, 4, 0.25), A(10, 1, 0.95), "caixa", 0.4, 1.0, rate=22.0)
    sc.hit(A(10, 2), "caixa", 1.0, rim=True)
    sc.hit(A(10, 2), "tarol", 1.0)
    sc.hit(A(10, 2), "bumbo", 1.0)
    sc.hit(A(10, 2), "surdo", 1.0)
    sc.hit(A(10, 2), "pratos", 1.0)
    return sc


# ============================================================================================ render

def patio_ir():
    """An open school courtyard: walls on three sides, no roof — a few clear reflections and a short tail."""
    return dsp.room_ir(0.75, dims=(30.0, 22.0, 30.0), src=(12.0, 8.0, 1.3), mic=(15.0, 15.0, 1.7), absorb=0.55,
                       order=3, seed=1201, hf_damp=1.5)


STEMS = {"caixas": ("caixa", "tarol"), "bumbos": ("bumbo", "surdo"), "pratos": ("pratos",)}
PAN = {"caixa": -0.12, "tarol": 0.28, "bumbo": 0.0, "surdo": 0.15, "pratos": 0.0}
GAIN = {"caixa": -3.0, "tarol": -9.0, "bumbo": 0.0, "surdo": -4.0, "pratos": -13.0}


def tail_fade(y, ms=25.0):
    """Every voice ends on a short raised-cosine, so nothing is ever truncated mid-ring (no clicks)."""
    k = min(len(y), int(ms / 1000 * SR))
    y = y.copy()
    y[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)) ** 2
    return y


def voice(inst, vel, rng, kw):
    if inst == "caixa":
        y = snare(vel, rng, rim=kw.get("rim", False))
    elif inst == "tarol":
        y = snare(vel, rng, kind="tarol")
    elif inst == "bumbo":
        y = bass(vel, rng, f0=76.0, dec=0.17)
    elif inst == "surdo":
        y = bass(vel, rng, f0=56.0, dec=0.45, kind="surdo")
    elif inst == "pratos":
        y = cymbal(vel, rng, kw.get("choke"))
    else:
        raise ValueError(inst)
    return tail_fade(y)


def pan(x, p):
    a = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], axis=1)


def render(sc: Score, T=LEN + 0.0):
    rng = np.random.default_rng(1200)
    n = int(T * SR)
    stems = {k: np.zeros((n, 2)) for k in STEMS}
    for t, inst, vel, kw in sorted(sc.hits, key=lambda h: h[0]):
        y = voice(inst, vel, rng, kw)
        if inst == "pratos":                                   # the pair spreads wide
            y2 = np.stack([y, np.roll(y, int(0.0007 * SR))], 1)
            src_ = y2
        else:
            src_ = pan(y, PAN[inst])
        stem = next(k for k, v in STEMS.items() if inst in v)
        dsp.place(stems[stem], src_, t, GAIN[inst])
    # one shared space: the school courtyard
    ir = patio_ir()
    for k in stems:
        stems[k] = dsp.convolve(stems[k], ir, wet=0.2, dry=1.0)[:n]
        stems[k] = dsp.hp(stems[k], 35, 2)
    return stems


def pieces():
    """Single hits for picture-locked moments (F15 f44/f60/f84/f108, Ad 3 'one snare hit on the point')."""
    rng = np.random.default_rng(777)
    ir = patio_ir()

    def one(sig, T):
        x = np.zeros((int(T * SR), 2))
        dsp.place(x, sig, 0.0, 0)
        return dsp.fade(dsp.convolve(x, ir, wet=0.2)[:len(x)], 0, 0.15)

    out = {}
    out["caixa_acento"] = one(pan(tail_fade(snare(1.0, rng, rim=True)), -0.1), 1.2)
    out["bumbo"] = one(pan(tail_fade(bass(1.0, rng, f0=76.0, dec=0.17)), 0), 1.4)
    sn = pan(tail_fade(snare(1.0, rng, rim=True)), -0.1)
    bd = pan(tail_fade(bass(1.0, rng, 76.0, 0.17)), 0) * db(3)
    both = np.zeros((max(len(sn), len(bd)), 2))
    both[:len(sn)] += sn
    both[:len(bd)] += bd
    out["caixa_bumbo_juntos"] = one(both, 1.4)
    sc = Score(seed=55)
    sc.roll(0.0, 2.0, "caixa", 0.07, 0.95, rate=21.0)
    roll = np.zeros((int(2.6 * SR), 2))
    for t, inst, vel, kw in sc.hits:
        dsp.place(roll, pan(tail_fade(snare(vel, rng)), -0.1), t, 0)
    roll = dsp.convolve(roll, ir, wet=0.2)[:len(roll)]
    out["rufo_entrada_2s_pp_cresc"] = dsp.fade(roll, 0, 0.2)
    return out


def edit_points():
    labels = {1: "RUFO DE ENTRADA (caixa pp → f)", 2: "RUFO + bumbo nos tempos 1 e 3; surdo no 4e",
              3: "MARCHA A1 (pratos no 1)", 4: "MARCHA A2", 5: "MARCHA A3 (pratos; aro nos acentos)", 6: "MARCHA A4",
              7: "MARCHA A5 (pratos no 1)", 8: "MARCHA A6 + VIRADA nos tempos 3–4", 9: "BREQUE: 4 golpes em uníssono",
              10: "FINAL: rufo curto → golpe único no tempo 2 (18,5 s), soa até 20,0 s"}
    bars = [dict(compasso=b, inicio_s=round((b - 1) * BAR, 3), inicio_quadro_24fps=int(round((b - 1) * BAR * 24)),
                 rotulo=labels[b]) for b in range(1, BARS + 1)]
    return dict(
        titulo="FANFARRA HOLOFOTE (composição original, SOL Estúdio)", bpm=BPM, compasso="4/4", tempo_s=BEAT,
        compasso_s=BAR, duracao_s=LEN, fps=24, quadros_por_tempo=12, quadros_por_compasso=48,
        compassos=bars,
        pontos_de_corte_s=[round(b * BAR, 3) for b in range(BARS + 1)],
        pontos_de_corte_nota="Corte em qualquer início de compasso (a cada 2,0 s = 48 quadros). Cortes no tempo "
                             "(0,5 s = 12 quadros) também caem na grade; evite cortar no meio do rufo (0–4 s) sem fade.",
        loop_sem_emenda=dict(inicio_s=4.0, fim_s=16.0, nota="compassos 3–8 (MARCHA) repetem; corte em 4,0 e 16,0 s "
                                                           "com 10 ms de crossfade"),
        golpes_principais_s=dict(rufo_inicio=0.0, rufo_pico=3.75, marcha_inicio=4.0, virada=14.0, breque=[16.0, 16.5, 17.0, 17.5],
                                 golpe_final=18.5),
    )


def master(stems):
    for k in stems:                                             # the final crash rings out to 20,0 s, then silence
        stems[k] = dsp.fade(stems[k], 0, 0.9)
    mix = sum(stems.values())
    y, info = dsp.norm_mix(mix, -14.0, -1.0)
    # the gain the master applied, so stems can be delivered at the same level (they sum back to the mix)
    g = np.sqrt((y ** 2).mean() / ((mix ** 2).mean() + 1e-20))
    return y, info, g


def brass_experimental(sc_times):
    """EXPERIMENTAL B♭ brass stabs (additive brass: brightness tied to loudness, lip scoop, breath).
    Not delivered — a synthesised section rarely survives a senior ear. Rendered to _tmp/ for a human to judge."""
    rng = np.random.default_rng(42)
    n = int(LEN * SR)
    out = np.zeros((n, 2))
    # B♭ major: trumpets D5 F5 B♭5, trombones B♭2 F3 D4
    notes = [587.33, 698.46, 932.33, 116.54, 174.61, 293.66]
    for t0, dur in sc_times:
        for f in notes:
            for player in range(2):
                m = int((dur + 0.25) * SR)
                t = np.arange(m) / SR
                cents = rng.normal(0, 6)
                scoop = -0.03 * np.exp(-t / 0.03)
                fr = f * 2 ** ((cents / 1200) + scoop)
                ph = 2 * np.pi * np.cumsum(fr) / SR
                env = np.clip(t / 0.03, 0, 1) * np.where(t < dur, 1.0, np.exp(-(t - dur) / 0.06))
                env *= (1 - 0.25 * np.clip((t - 0.04) / 0.1, 0, 1))
                y = np.zeros(m)
                for k in range(1, 16):
                    if k * f > 9000:
                        break
                    y += (env ** (0.8 + 0.25 * k)) * np.sin(k * ph) / k ** 0.7
                y += 0.03 * dsp.bp(rng.standard_normal(m), 1500, 5000, 2) * np.exp(-t / 0.05)
                dsp.place(out, pan(y / np.abs(y).max(), rng.uniform(-0.5, 0.5)), t0 + rng.normal(0, 0.01), -14)
    ir = patio_ir()
    return dsp.convolve(out, ir, wet=0.3)[:n]


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "pecas"), exist_ok=True)
    sc = compose(Score())
    stems = render(sc)
    y, info, g = master(stems)
    dsp.write(os.path.join(OUT, "HLF-MUS-01_fanfarra_120bpm_20s_mix.wav"), y)
    rep = {"mix": info}
    # stems keep their balance and get one common offset so their SUM peaks at -1 dBTP (no clipping)
    tamb = sum(stems.values()) * g
    off = min(0.0, -1.0 - dsp.true_peak(tamb))
    for k, s in stems.items():
        p = os.path.join(OUT, f"HLF-MUS-01_fanfarra_120bpm_20s_stem_{k}.wav")
        dsp.write(p, s * g * db(off))
        rep[f"stem_{k}"] = dict(true_peak_dbtp=round(dsp.true_peak(s * g * db(off)), 2))
    dsp.write(os.path.join(OUT, "HLF-MUS-01_fanfarra_120bpm_20s_stem_tambores.wav"), tamb * db(off))
    rep["stem_tambores"] = dict(true_peak_dbtp=round(dsp.true_peak(tamb * db(off)), 2),
                                nota="soma dos stems caixas+bumbos+pratos")
    rep["stems_offset_db"] = round(off, 2)
    rep["stems_nota"] = (f"Os stems estão {off:+.1f} dB em relação ao mix (headroom: a soma não clipa). "
                         f"Soma dos stems {(-off):+.1f} dB → limitador true-peak = mix.")
    for k, v in pieces().items():
        yy, inf = dsp.norm_sfx(v, -20.0, -1.0)
        dsp.write(os.path.join(OUT, "pecas", f"HLF-MUS-02_{k}.wav"), yy)
        rep[f"pecas/{k}"] = inf
    ep = edit_points()
    ep["loudness"] = rep
    ep["metais"] = ("NÃO ENTREGUES. Metais sintetizados não passam no padrão do estúdio sem um ouvido humano; "
                    "o stem experimental sai só com --metais em _build/sound/_tmp/ para avaliação.")
    json.dump(ep, open(os.path.join(OUT, "HLF-MUS-01_pontos_de_edicao.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(rep, indent=1, ensure_ascii=False))
    if "--metais" in sys.argv:
        A = Score().at
        b = brass_experimental([(A(3, 1), 0.18), (A(5, 1), 0.18), (A(7, 1), 0.18), (A(9, 1), 0.12), (A(9, 2), 0.12),
                                (A(9, 3), 0.12), (A(9, 4), 0.12), (A(10, 2), 0.9)])
        dsp.write(os.path.join(TMP, "EXPERIMENTAL_metais_Bb_NAO_APROVADO.wav"), b * g)
        dsp.write(os.path.join(TMP, "EXPERIMENTAL_mix_com_metais_NAO_APROVADO.wav"),
                  dsp.norm_mix(sum(stems.values()) + b, -14.0, -1.0)[0])
        print("metais experimentais em _tmp/ (não entregues)")


if __name__ == "__main__":
    main()
