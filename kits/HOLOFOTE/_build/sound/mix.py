#!/usr/bin/env python
"""HOLOFOTE · mix.py — render a JSON cue list to a stereo 48 kHz / 24-bit WAV at −14 LUFS integrated, ≤ −1 dBTP.

Cue list: either a plain list of cues, or an object {"duracao_s": 15.0, "alvo_lufs": -14, "teto_dbtp": -1,
"fps": 24, "cues": [...]}. Each cue:

    {"file": "sfx/HLF-SFX-01_clac.wav",   # relative to the JSON's folder, else to 04_FILMES/som/, or absolute
     "start_s": 0.5,                     # where the cue lands on the timeline (see "sync")
     "gain_db": 0.0,
     "fade_in": 0.0, "fade_out": 0.0,    # seconds (raised-cosine)
     # optional:
     "frame": 12,                        # instead of start_s: a frame number at "fps"
     "sync": "onset",                    # "start" (default): the file's first sample lands on start_s;
                                         # "onset": the file's main transient (the strongest onset in its
                                         # first 250 ms, measured by onsets.py) lands on start_s
     "trim_in_s": 0.0,                   # skip this much of the file's beginning
     "dur_s": null,                      # keep only this much (after trim_in); the cut gets fade_out
     "loop": false,                      # repeat the file to fill dur_s (for the *_loop.wav beds)
     "pan": 0.0,                         # -1 .. 1 (equal-power, applied to the downmixed source)
     "envelope": [[0.0, 0.0], [1.0, -6.0]],   # gain points (s from cue start, dB), linear between points
     "label": "CLAC f12"}

Loudness: pyloudnorm (ITU-R BS.1770-4 integrated, gated) and a 4x-oversampled look-ahead true-peak limiter.
Writes <out>.wav and <out>.json (loudness, every cue's anchor, the onsets measured on the final mix).

    /home/user/venvs/web/bin/python -I mix.py cues.json out.wav [--duracao 15] [--sem-normalizar]
"""
from __future__ import annotations

import argparse, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dsp  # noqa: E402
from dsp import SR, db  # noqa: E402
import onsets as ON  # noqa: E402

SOM = os.path.abspath(os.path.join(HERE, "..", "..", "04_FILMES", "som"))


def resolve(path: str, base: str) -> str:
    for p in (path, os.path.join(base, path), os.path.join(SOM, path)):
        if os.path.exists(p):
            return os.path.abspath(p)
    raise FileNotFoundError(path)


def render(spec, base: str, dur: float | None = None, normalise: bool = True):
    if isinstance(spec, list):
        spec = {"cues": spec}
    fps = float(spec.get("fps", 24.0))
    cues = spec["cues"]
    target = float(spec.get("alvo_lufs", -14.0))
    ceiling = float(spec.get("teto_dbtp", -1.0))
    placed = []
    for c in cues:
        path = resolve(c["file"], base)
        x = dsp.stereo(dsp.read(path))
        x = x[int(round(float(c.get("trim_in_s", 0.0)) * SR)):]
        if c.get("loop") and c.get("dur_s"):
            need = int(round(float(c["dur_s"]) * SR))
            reps = int(np.ceil(need / max(1, len(x))))
            x = np.vstack([x] * max(1, reps))
        if c.get("dur_s") is not None:
            x = x[:int(round(float(c["dur_s"]) * SR))]
        start = float(c["frame"]) / fps if "frame" in c else float(c.get("start_s", 0.0))
        anchor = 0.0
        if c.get("sync", "start") == "onset":
            tmp = os.path.join(HERE, "_tmp", "_onset_probe.wav")
            dsp.write(tmp, x)
            on = ON.onsets(tmp, detail=True)
            early = [o for o in on if o[0] <= 0.25] or on[:1]
            anchor = max(early, key=lambda o: o[1])[0] if early else 0.0   # the strongest transient in the first 250 ms
        if "pan" in c:
            m = dsp.mono(x)
            a = (float(c["pan"]) + 1) * np.pi / 4
            x = np.stack([m * np.cos(a), m * np.sin(a)], axis=1)
        if c.get("envelope"):
            pts = sorted((float(t), float(g)) for t, g in c["envelope"])
            t = np.arange(len(x)) / SR
            x = x * np.interp(t, [p[0] for p in pts], [db(p[1]) for p in pts])[:, None]
        x = dsp.fade(x, float(c.get("fade_in", 0.0)), float(c.get("fade_out", 0.0)))
        placed.append((start - anchor, x * db(float(c.get("gain_db", 0.0))), c, start, anchor, path))
    end = max((t + len(x) / SR for t, x, *_ in placed), default=0.0)
    T = float(dur if dur is not None else spec.get("duracao_s", end))
    out = np.zeros((int(round(T * SR)), 2))
    for t, x, c, start, anchor, path in placed:
        dsp.place(out, x, t, 0.0)
    info = {}
    if normalise:
        out, info = dsp.norm_mix(out, target, ceiling)
    return out, info, placed, fps


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cues")
    ap.add_argument("out")
    ap.add_argument("--duracao", type=float, help="total length in s (default: the JSON's duracao_s, else the last cue)")
    ap.add_argument("--sem-normalizar", action="store_true", help="skip loudness normalisation (raw sum)")
    a = ap.parse_args()
    spec = json.load(open(a.cues))
    base = os.path.dirname(os.path.abspath(a.cues))
    out, info, placed, fps = render(spec, base, a.duracao, not a.sem_normalizar)
    dsp.write(a.out, out)
    measured = ON.onsets(a.out)
    rep = dict(arquivo=os.path.basename(a.out), duracao_s=round(len(out) / SR, 4), fps=fps, **info,
               normalizacao="−14 LUFS integrado (pyloudnorm, BS.1770-4), ≤ −1 dBTP (limitador true-peak 4x)",
               cues=[], onsets_medidos=[dict(t_s=round(t, 4), quadro=round(t * fps, 2)) for t in measured])
    ms = np.array(measured) if measured else np.array([np.inf])
    for t, x, c, start, anchor, path in placed:
        row = dict(label=c.get("label", os.path.basename(path)), arquivo=os.path.relpath(path, SOM),
                   inicio_s=round(start, 4), quadro=round(start * fps, 2), sync=c.get("sync", "start"))
        if c.get("sync") == "onset":
            k = int(np.argmin(np.abs(ms - start)))
            row["onset_medido_na_mix_s"] = round(float(ms[k]), 4)
            row["desvio_quadros"] = round(float((ms[k] - start) * fps), 3)
        rep["cues"].append(row)
    json.dump(rep, open(os.path.splitext(a.out)[0] + ".json", "w"), indent=2, ensure_ascii=False)
    print(f"{a.out}: {rep['duracao_s']} s  {info.get('lufs_i', 'n/a')} LUFS  {info.get('true_peak_dbtp', 'n/a')} dBTP")
    for r in rep["cues"]:
        if "desvio_quadros" in r:
            flag = "OK" if abs(r["desvio_quadros"]) <= 1.0 else "VERIFICAR"
            print(f"  {r['label']:34s} alvo f{r['quadro']:7.2f}  medido {r['onset_medido_na_mix_s']:.4f} s  "
                  f"(Δ {r['desvio_quadros']:+.2f} f) {flag}")


if __name__ == "__main__":
    main()
