#!/usr/bin/env python
"""HOLOFOTE · filmes.py — the films' sound, as cue lists written from the platform's frame tables (§E.4, §F.2),
rendered with mix.py. Writes 04_FILMES/som/filmes/<ID>_cues.json, <ID>_som.wav and <ID>_som.json.

    /home/user/venvs/web/bin/python -I filmes.py            # all
    /home/user/venvs/web/bin/python -I filmes.py F15 F06B   # some

Every keyed transient (CLAC, hits, cough, claps, bells) uses "sync": "onset", so the TRANSIENT lands on the frame,
and each render reports the onset measured on the final mix against its frame (±1 frame = OK). The picture team
snaps the type slams to those measured times (platform §E.5: "data, not decoration").
"""
from __future__ import annotations

import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mix as MX  # noqa: E402
import dsp  # noqa: E402
import onsets as ON  # noqa: E402

OUT = os.path.join(MX.SOM, "filmes")
FPS = 24.0
MUS = "musica/HLF-MUS-01_fanfarra_120bpm_20s_mix.wav"
PEC = "musica/pecas/HLF-MUS-02_"
S = "sfx/HLF-SFX-"
MORPH = "identidade/HLF-ID-02_crepitar_para_aplauso_morph.wav"


def f2s(f):
    return f / FPS


def F15():
    """A ENTRADA — 15 s, 360 frames."""
    c = [
        dict(label="fanfarra: rufo pp, corte seco f132", file=MUS, frame=0, dur_s=f2s(132), fade_out=0.015, gain_db=-6),
        dict(label="CLAC f12", file=S + "01_clac.wav", frame=12, sync="onset", gain_db=2),
        dict(label="murmúrio sobe f12", file=S + "03_murmurio_teatro_loop.wav", frame=12, dur_s=f2s(132 - 12),
             fade_in=1.0, fade_out=0.12, gain_db=-8),
        dict(label="caixa f44", file=PEC + "caixa_acento.wav", frame=44, sync="onset", gain_db=1),
        dict(label="bumbo f60", file=PEC + "bumbo.wav", frame=60, sync="onset", gain_db=0),
        dict(label="caixa f84", file=PEC + "caixa_acento.wav", frame=84, sync="onset", gain_db=1),
        dict(label="caixa f108", file=PEC + "caixa_acento.wav", frame=108, sync="onset", gain_db=1),
        dict(label="ar da casa (silêncio) f132", file=S + "15_tom_de_sala_loop.wav", frame=132, dur_s=f2s(168 - 132),
             fade_in=0.05, fade_out=0.3, gain_db=-30),
        dict(label="tosse f150", file=S + "10_tosse_plateia.wav", frame=150, sync="onset", gain_db=-3),
        dict(label="elevador desce f168", file=S + "11_elevador_hidraulico_1s.wav", frame=168, dur_s=0.36,
             fade_out=0.08, gain_db=-6),
        dict(label="elevador sobe f177", file=S + "11_elevador_hidraulico_1s.wav", frame=177, dur_s=1.0,
             fade_out=0.06, gain_db=-6),
        dict(label="plateia cresce f168→f204", file=S + "03_murmurio_teatro_loop.wav", frame=168, trim_in_s=4.0,
             dur_s=f2s(204 - 168), fade_in=1.2, fade_out=0.02, gain_db=-5),
        dict(label="CLAC-off f204 (BLACKOUT)", file=S + "02_clac_off.wav", frame=204, sync="onset", gain_db=2),
        dict(label="fósforo fsst f206", file=S + "07_fosforo_fsst.wav", frame=206, sync="onset", gain_db=-2),
        dict(label="pavio → aplauso (morph) f210", file=MORPH, frame=210, dur_s=f2s(312 - 210), fade_out=0.004,
             gain_db=-4),
        dict(label="CLAC f222", file=S + "01_clac.wav", frame=222, sync="onset", gain_db=2),
        dict(label="aplauso cresce f222→f312", file=S + "05_aplauso_estadio_distante.wav", frame=222, trim_in_s=2.5,
             dur_s=f2s(312 - 222), fade_in=1.5, fade_out=0.004, gain_db=2),
        dict(label="palmas f312/322/332", file=S + "06e_palmas_tres_10q.wav", frame=312, sync="onset", gain_db=2),
        dict(label="tom de sala f312→f348", file=S + "15_tom_de_sala_loop.wav", frame=312, dur_s=f2s(348 - 312),
             fade_in=0.004, fade_out=0.25, gain_db=-28),
    ]
    keys = [12, 44, 60, 84, 108, 150, 204, 206, 222, 312, 322, 332]
    return dict(duracao_s=15.0, fps=FPS, cues=c), keys


def F06A():
    """CLAC — 6 s, 144 frames."""
    c = [
        dict(label="CLAC f6", file=S + "01_clac.wav", frame=6, sync="onset", gain_db=2),
        dict(label="pavio f7", file=S + "08_crepitar_pavio_loop.wav", frame=7, dur_s=f2s(14 - 7), fade_in=0.04,
             fade_out=0.12, gain_db=-7),
        dict(label="pavio → aplauso (fusão começa f24), corta seco no corte de imagem f96", file=MORPH, frame=12,
             dur_s=f2s(96 - 12), fade_in=0.08,
             fade_out=0.004, gain_db=-4),
        dict(label="palmas f100/110/120", file=S + "06e_palmas_tres_10q.wav", frame=100, sync="onset", gain_db=2),
        dict(label="tom de sala f100→f144", file=S + "15_tom_de_sala_loop.wav", frame=100, dur_s=f2s(44),
             fade_in=0.004, fade_out=0.3, gain_db=-28),
    ]
    return dict(duracao_s=6.0, fps=FPS, cues=c), [6, 100, 110, 120]


def F06B():
    """O PIOR SHOW — 6 s, 144 frames. One word per beat: the march's downbeat lands on f0."""
    c = [
        dict(label="fanfarra (marcha, compasso 3) f0→f84", file=MUS, frame=0, trim_in_s=4.0, dur_s=f2s(84),
             fade_out=0.012, gain_db=-4,
             envelope=[[0.0, 0.0], [1.9, 0.0], [1.98, -7.0], [2.7, -7.0], [2.95, 0.0], [3.5, 0.0]]),
        dict(label="tosse no PIOR f48", file=S + "10_tosse_plateia.wav", frame=48, sync="onset", gain_db=1),
        dict(label="CLAC f84 (corte pro KV-45)", file=S + "01_clac.wav", frame=84, sync="onset", gain_db=2),
        dict(label="aplauso f84→f120", file=S + "05_aplauso_estadio_distante.wav", frame=84, trim_in_s=5.0,
             dur_s=f2s(36), fade_in=0.25, fade_out=0.004, gain_db=0),
        dict(label="palmas f120/130/140", file=S + "06e_palmas_tres_10q.wav", frame=120, sync="onset", gain_db=2),
        dict(label="tom de sala f120→", file=S + "15_tom_de_sala_loop.wav", frame=120, dur_s=f2s(24),
             fade_in=0.004, fade_out=0.25, gain_db=-28),
    ]
    return dict(duracao_s=6.0, fps=FPS, cues=c), [0, 12, 24, 36, 48, 60, 84, 120, 130, 140]


def F06C(n_bells: int):
    """SINAL — 6 s template; 1, 2 or 3 bells (07.05 / 08.05 / 09.05)."""
    bell = {1: "09a_sinal_1_sino.wav", 2: "09b_sinal_2_sinos.wav", 3: "09c_sinal_3_sinos.wav"}[n_bells]
    c = [
        dict(label=f"{n_bells} sino(s) f0/f8/f16", file=S + bell, frame=0, dur_s=f2s(72), fade_out=0.35, gain_db=0),
        dict(label="CLAC f72", file=S + "01_clac.wav", frame=72, sync="onset", gain_db=2),
    ]
    if n_bells < 3:   # unlit: the house is filling up
        c.append(dict(label="plateia chegando f74→", file=S + "03_murmurio_teatro_loop.wav", frame=74, dur_s=f2s(70),
                      fade_in=1.4, fade_out=0.3, gain_db=-13))
    else:             # 09.05: lit — the wick, and it turns into applause
        c.append(dict(label="pavio → aplauso f74→", file=MORPH, frame=74, dur_s=f2s(70), fade_in=0.04,
                      fade_out=0.3, gain_db=-4))
    keys = [0, 8, 16][:n_bells] + [72]
    return dict(duracao_s=6.0, fps=FPS, cues=c), keys


def AD_KV(with_bell: bool):
    """The shared 9–15 s KV block of the ads, as a 6,0 s bed to lay at 9,0 s (t=0 here = 9,0 s in the ad).
    Ads 1 and 3: CLAC at 9,0 → crackle → applause → three claps at 13,0.
    Ad 2: the THIRD BELL at 9,0, 4 frames of black, then CLAC → applause → three claps."""
    c = []
    clac_f = 0
    if with_bell:
        c.append(dict(label="terceiro sinal 9,0 s", file=S + "09_sino_teatro.wav", frame=0, sync="onset",
                      dur_s=3.0, fade_out=0.6, gain_db=-2))
        clac_f = 4
    c += [
        dict(label=f"CLAC +{clac_f} f", file=S + "01_clac.wav", frame=clac_f, sync="onset", gain_db=2),
        dict(label="pavio → aplauso", file=MORPH, frame=clac_f + 1, dur_s=4.0 - f2s(clac_f + 1), fade_in=0.03,
             fade_out=0.004, gain_db=-4),
        dict(label="palmas 13,0 s (f96 do bloco)", file=S + "06e_palmas_tres_10q.wav", frame=96, sync="onset",
             gain_db=2),
        dict(label="tom de sala", file=S + "15_tom_de_sala_loop.wav", frame=96, dur_s=2.0, fade_in=0.004,
             fade_out=0.3, gain_db=-28),
    ]
    keys = ([0] if with_bell else []) + [clac_f, 96, 106, 116]
    return dict(duracao_s=6.0, fps=FPS, cues=c), keys


JOBS = {
    "F15": ("HLF-F15_A_ENTRADA", F15),
    "F06A": ("HLF-F06A_CLAC", F06A),
    "F06B": ("HLF-F06B_O_PIOR_SHOW", F06B),
    "F06C_0705": ("HLF-F06C_SINAL_07-05", lambda: F06C(1)),
    "F06C_0805": ("HLF-F06C_SINAL_08-05", lambda: F06C(2)),
    "F06C_0905": ("HLF-F06C_SINAL_09-05", lambda: F06C(3)),
    "AD_KV_1_3": ("HLF-AD_KV_9a15s_ads1e3", lambda: AD_KV(False)),
    "AD_KV_2": ("HLF-AD_KV_9a15s_ad2_sino", lambda: AD_KV(True)),
}


def main(names=None):
    os.makedirs(OUT, exist_ok=True)
    for key, (fid, fn) in JOBS.items():
        if names and key not in names:
            continue
        spec, keys = fn()
        cj = os.path.join(OUT, f"{fid}_cues.json")
        json.dump(spec, open(cj, "w"), indent=2, ensure_ascii=False)
        wav = os.path.join(OUT, f"{fid}_som.wav")
        y, info, placed, fps = MX.render(spec, OUT)
        dsp.write(wav, y)
        ms = ON.onsets(wav)
        rep = dict(arquivo=os.path.basename(wav), duracao_s=round(len(y) / dsp.SR, 3), fps=fps, **info,
                   normalizacao="−14 LUFS integrado, ≤ −1 dBTP", cues=[], quadros_chave=[])
        for t, x, c, start, anchor, path in placed:
            row = dict(label=c.get("label"), arquivo=os.path.relpath(path, MX.SOM), quadro=round(start * fps, 2),
                       inicio_s=round(start, 4), sync=c.get("sync", "start"))
            rep["cues"].append(row)
        bad = 0
        for k in keys:
            t = k / fps
            near = min(ms, key=lambda v: abs(v - t)) if ms else float("inf")
            d = (near - t) * fps
            ok = abs(d) <= 1.0
            bad += not ok
            rep["quadros_chave"].append(dict(quadro=k, onset_medido_s=round(near, 4), desvio_quadros=round(d, 3),
                                             ok=ok))
        rep["onsets_medidos"] = [dict(t_s=round(v, 4), quadro=round(v * fps, 2)) for v in ms]
        json.dump(rep, open(os.path.join(OUT, f"{fid}_som.json"), "w"), indent=2, ensure_ascii=False)
        dev = " ".join(f"f{q['quadro']}:{q['desvio_quadros']:+.2f}" for q in rep["quadros_chave"])
        print(f"{fid:30s} {info['lufs_i']:6.2f} LUFS {info['true_peak_dbtp']:6.2f} dBTP  "
              f"{'OK' if not bad else f'{bad} FORA'}  {dev}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
