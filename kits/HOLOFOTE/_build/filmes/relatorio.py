"""HOLOFOTE · FILM_PLAN.json: the plan and the record of the films in one file (06_PRODUCAO/FILM_PLAN.json).

    /home/user/venvs/web/bin/python _build/filmes/relatorio.py

Per film: frames, duration, the shots (= EDIT_DECISION_LIST.csv), every type string with its frames, the sound file and
its loudness (the sound team's measurement), the slam/onset sync table, the label-fidelity summary
(06_PRODUCAO/fidelidade/<FILM>.json) and the deliverables with their probed streams. Plus the 3D render log.
"""
import os, sys, json, glob, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import comum as C      # noqa: E402
import plano as P      # noqa: E402

DESVIOS = [
    'No disclosure plate on any frame (founder override, 6 Oct 2026): the platform\'s "render 3D ilustrativo · marca fictícia" plate is not burnt in; its band y 276–312 stays empty.',
    'Display lines fill their measure (rule 2) by size, so their caps land within 3 px of the frame tables: A ATRAÇÃO É ELA. cap 53,96 (table 51), O MENOR HOLOFOTE DO BRASIL. 53,55 (56), PRA MAIOR ATRAÇÃO. 79,29 (80), holofote nela. 72,77 (70), F06C titles 101–103 (105: at 105 they overflow the 800 px measure by 12–30 px).',
    'The poster squash (wdth 75 -> 128 -> 125) is set on the Special Gothic wdth axis for Locutor lines (MÃE, AO VIVO, A ATRAÇÃO É ELA., the F06B woodtype); wdth 128 is above the axis and Condensed One has no wdth axis, so those use a horizontal scale (overshoot 102,4 %; Condensed slams 60 -> 84 -> 102,4 -> 100 %). The 128 overshoot frame of a full-measure line is ~10 px wider than the measure for one frame.',
    'CLAC filament warm-ups (2 frames) are 2D relights of the rendered plates in SCENE-LINEAR light (exact inverse of Khronos PBR Neutral), the spot at 10 % / 2.000 K then 55 % / 2.700 K over the flame light; not extra 3D renders.',
    'Flame flicker on the lit KV-45: a 24-frame BORDER/CROP 3D loop of the flame region (the box is the flame object projected at the KV-45 camera at 110 % scale + 36 px; _render/chama_*/box.json), composited with a 20 px feather; the flame\'s light on everything outside the crop follows the flicker through the blackout plate (lit = spot + flame, and the blackout plate is the flame\'s light alone), scaled in scene-linear. Every KV-45 frame we render (crops, blackout) is built by the director\'s own shots/kv45.py build(), with only the flicker state and the blackout injected.',
    'F15 f204–209 is pure black (the candle is unlit when the spot cuts; the match strike at f206 is sound only, per the table).',
    'F06A end card uses the F15 end-card setting (holofote nela. filling 800 at baseline 410 + safety line at 508); the F06A table names the lines but not their layout.',
    'F06A headline A ATRAÇÃO É ELA. sits at baseline 410 (not the slot\'s 442) so abertura: você at baseline 470 clears its descender (Ç) by ~20 px.',
    'F06C KV-45 state: MÃE AO VIVO fills the headline slot (MÃE in amarelo), DOMINGO · 09.05 (the dotted date, compliance review) and holofote nela. share baseline 496 as an L/R split, safety at 530 on the lit 09.05 only. The table names the strings, not their layout.',
    'F06C sub-line (Shantell, the Fã) at x-height 36 px, centred, baseline 900; the table gives only its baseline.',
    'Push centre: x 540, 90 px below the top of the print (read from the KV-45 label AOV, so it follows any re-framing): the dolly expands about the label\'s upper half and the flame tip stays clear of the type zone.',
    'Crane frames f160–175 (no candle) rendered at 50 % and Lanczos-upscaled; f176–203 at 100 % with label AOVs; 48 samples + OIDN (adaptive 0,02), the director\'s light-path trims.',
]


def sonda(p):
    try:
        out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                              'stream=codec_name,width,height,r_frame_rate,nb_frames,pix_fmt,color_space,color_primaries,color_transfer,duration,sample_rate,channels',
                              '-of', 'json', p], capture_output=True, text=True).stdout
        return json.loads(out)['streams']
    except Exception as e:
        return str(e)


def loudness_mp4(p):
    """Integrated loudness and true peak of the muxed AAC (ffmpeg ebur128), to compare with the WAV."""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', p, '-filter_complex', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    i = re.findall(r'I:\s+(-?[\d.]+) LUFS', r)
    tp = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)
    return dict(lufs_i=float(i[-1]) if i else None, true_peak_dbfs=float(tp[-1]) if tp else None)


def tempos_3d():
    out = []
    for lg in sorted(glob.glob(os.path.join(C.RENDER, 'logs', '*.log'))):
        for ln in open(lg, errors='ignore'):
            if ln.startswith('TEMPO'):
                out.append(ln.strip())
    return out


def strings(film):
    geom_dummy = {'atr': {'bot': 400}, 'L1E': {'bot': 360}, 'L1D': {'bot': 360}, 'MAE': {'bot': 640}, 'SHOW': {'bot': 770},
                  'L4E': {'bot': 833}, 'L4D': {'bot': 833}, 'L4D_ab': 0.64, 'ab470': 0.65, 'titulo': {'cap': 102}}
    ev = {}
    for f in range(P.DUR[film]):
        for d, _, _ in P.TIPO[film](f, geom_dummy):
            for e in d['camada']:
                if e['k'] == 'linha':
                    ts = [e['t']]
                elif e['k'] == 'kv01':
                    names = {'L1E': 'HOLOFOTE APRESENTA', 'L1D': 'A TURNÊ · 2027', 'MAE': 'MÃE', 'SHOW': 'AO VIVO',
                             'L4E': 'DOMINGO · 09.05', 'L4D': 'abertura: você'}
                    ts = [names[x] for x in e['so']]
                elif e['k'] == 'c03':
                    ts = list(e['ver']) + (['(girassol, 2007)'] if e.get('nota') else [])
                else:
                    ts = []
                for t in ts:
                    a = ev.setdefault(t, [f, f])
                    a[1] = f
    return [dict(text=t, first=a[0], last=a[1]) for t, a in sorted(ev.items(), key=lambda x: x[1][0])]


def main():
    sinc = P.verificar_sincronia()
    plan = dict(kit='HOLOFOTE', made_with='_build/filmes (f15_3d.py, compor.py, fidelidade_filmes.py, plano.py, relatorio.py)',
                format=dict(w=C.W, h=C.H, fps=C.FPS, encoder='_build/tools/codificar.py --fps 24 (BT.709 converted and tagged, x264 CRF 14)'),
                films={}, deviations=DESVIOS, render_log_3d=tempos_3d())
    for film in P.DUR:
        nome = P.NOME[film]
        sj = json.load(open(os.path.join(C.SOM, P.SOM[film] + '_som.json')))
        fid = os.path.join(C.FID, nome + '.json')
        mp4 = {t: os.path.join(C.FILMES, '%s_%s.mp4' % (nome, t)) for t in ('som', 'mudo')}
        plan['films'][nome] = dict(
            frames=P.DUR[film], seconds=P.DUR[film] / C.FPS,
            deliverables={t: dict(path=os.path.relpath(p, C.KIT), exists=os.path.exists(p),
                                  streams=sonda(p) if os.path.exists(p) else None,
                                  loudness_muxed=loudness_mp4(p) if (t == 'som' and os.path.exists(p)) else None)
                          for t, p in mp4.items()},
            sound=dict(file=os.path.relpath(os.path.join(C.SOM, P.SOM[film] + '_som.wav'), C.KIT), lufs_i=sj['lufs_i'],
                       true_peak_dbtp=sj['true_peak_dbtp'], key_frames=sj.get('quadros_chave')),
            shots=[dict(shot=s, first=a, last=b, source=src, mode=m, notes=n) for s, a, b, src, m, n in P.FOTOS[film]()],
            type=strings(film),
            sync=[r for r in sinc if r['film'] == film],
            fidelity=json.load(open(fid))['resumo'] if os.path.exists(fid) else None)
    p = os.path.join(C.PROD, 'FILM_PLAN.json')
    json.dump(plan, open(p, 'w'), indent=1, ensure_ascii=False)
    print(p)


if __name__ == '__main__':
    main()
