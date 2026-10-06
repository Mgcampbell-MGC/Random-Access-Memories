"""O ANÚNCIO previs animatics: 8 masters x (with sound, silent), 15,0 s, 1080 x 1920, 24 fps (platform §F, §D.10).

    /home/user/venvs/web/bin/python animatic.py [ETAPA ...] [--cortes 1A,2A]
    ETAPAs, in order (default: all):  vo  camadas  som  quadros  folhas  fidelidade

Inputs (all regenerable):
  _tmp_animatic/vo/          temp VO, from  /home/user/venvs/kokoro/bin/python vo.py _tmp_animatic/vo
  _tmp_animatic/plates/      grey-mannequin previs plates, from  _build/shots/blender.sh animatic_previs.py
  02_PRODUTO/renders/KV-45_aceso_16bit.png  the director's KV-45 plate (never re-rendered here)
  _build/shots/aov/KV-45_aceso/0001.exr     its label AOVs (for the fidelity check)
Outputs:
  05_ANUNCIO/animatics/HLF-AD-<cut>_<conceito>_animatic_som.mp4 / _mudo.mp4   (encoded ONLY by tools/codificar.py)
  05_ANUNCIO/animatics/HLF-AD-<cut>_<conceito>_animatic_folha.png             contact sheet, decoded from the MP4
  05_ANUNCIO/animatics/animatic_tempos.json                                   every timing actually used
  06_PRODUCAO/fidelidade/ANUNCIO_animatics_KV.json                           per-frame label fidelity, 9–15 s

Timeline (platform §F): 0,0–2,0 hook · 2,0–6,0 body (the talk plate, tag, word-synced captions) · 6,0–9,0 gesture
plate + gesture title · 9,0–15,0 KV-45 lit, push 100 -> 103 % about the frame centre, KV type (headline, lockup,
safety line) and the VO caption at y 300–330 — dropped where the VO line IS the headline or the lockup (1A–1C,
3A–3C; director, 6 Oct 2026). Ad 2: black 4 frames, then the CLAC to lit (frame 220).
The cut to the KV, the claps, the second bell and the snare are keyed to onsets MEASURED on the final mix.
No disclosure plate (founder override, 6 Oct 2026). Silent master = the same picture with no audio track: every
spoken line is already captioned in both.
"""
import glob, json, math, os, shutil, subprocess, sys
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..'))
KIT = os.path.abspath(os.path.join(B, '..'))
sys.path.insert(0, os.path.join(B, 'brand'))
sys.path.insert(0, os.path.join(B, 'kv'))
sys.path.insert(0, os.path.join(B, 'tools'))
sys.path.insert(0, HERE)
import legendas as LG  # noqa: E402

PY = '/home/user/venvs/web/bin/python'
TTS = '/home/user/venvs/kokoro/bin/python'
TMP = os.path.join(HERE, '_tmp_animatic')
VO = os.path.join(TMP, 'vo')
PLATES = os.path.join(TMP, 'plates')
LAY = os.path.join(TMP, 'camadas')
SOM = os.path.join(TMP, 'som')
OUT = os.path.join(KIT, '05_ANUNCIO', 'animatics')
FIDDIR = os.path.join(KIT, '06_PRODUCAO', 'fidelidade')
KV16 = os.path.join(KIT, '02_PRODUTO', 'renders', 'KV-45_aceso_16bit.png')
KV_AOV = os.path.join(B, 'shots', 'aov', 'KV-45_aceso', '0001.exr')
MASTER = os.path.join(KIT, '02_PRODUTO', 'rotulos', 'HLF-02_ROTULO_wrap.png')
SFXROOT = os.path.join(KIT, '04_FILMES', 'som')

FPS, N, W, H = 24, 360, 1080, 1920
KV0 = 216                                  # 9,0 s
PUSH = (1.00, 1.03)
PIVOT_KV = (539.5, 959.5)                  # frame centre (pixel-centre coordinates)
R = json.load(open(os.path.join(HERE, 'roteiros.json')))['cortes']
SLUG = {'1': 'O-PIOR-SHOW', '2': 'PRIMEIRO-SINAL', '3': 'FA-DE-CARTEIRINHA'}

# VO placement: hook 0,10 s (2B 0,40 s: "a beat of silence, then she speaks"), body 2,05 s, KV line 9,25 s.
STARTS = {'gancho': 0.10, 'corpo': 2.05, 'kv_vo': 9.25}
STARTS_CUT = {'2B': {'gancho': 0.40}}
VO_LUFS = -16.0                            # each line; the bed is ducked 8 dB under it (sound team: "baixe a cama ~8 dB")

# Previs plates and their head pixel (1080 space; animatic_previs.SHOTS). Talk push: about the head.
HEAD = {'SIT': (540, 815), 'USHER': (540, 795)}


def talk_plate(cut):
    r = R[cut]
    return ('USHER_H01' if cut[0] == '2' else 'SIT_' + r['apresentador'])


def gesture_plates(cut):
    p = R[cut]['apresentador']
    return {'1': 'CLAP_' + p, '2': 'PHONE_H01', '3': 'HEART_' + p}[cut[0]]


LOCKUP = 'holofote nela.'


def kv_caption(cut):
    """Director, 6 Oct 2026 (compliance review): the 9–15 s VO caption never duplicates type already on screen in
    another case. When the VO line IS the headline or the lockup, the caption is dropped: the KV type already carries
    the words for silent viewers. 1A–1C 'Sua vez.' = SUA VEZ.; 3A–3C 'holofote nela.' = the lockup; 2A–2B keep it."""
    norm = lambda x: ' '.join(x.lower().split())
    v = norm(R[cut]['kv_vo'])
    return v not in (norm(R[cut]['headline']), norm(LOCKUP))


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def talk_scale(cut, t):
    """0–6 s camera: Ad 1 a near-locked 1,5 % creep (the small shrug), Ad 2 locked off (absolute composure),
    Ad 3 the slow lean toward the lens as a 6 % eased push over the body (2–6 s)."""
    c = cut[0]
    if c == '1':
        return 1.0 + 0.015 * t / 6.0
    if c == '3':
        return 1.0 + 0.06 * ease((t - 2.0) / 4.0)
    return 1.0


def kv_scale(f):
    return PUSH[0] + (PUSH[1] - PUSH[0]) * (f - KV0) / (N - 1 - KV0)


def kv_affine(f):
    s = kv_scale(f)
    cx, cy = PIVOT_KV
    return np.array([[s, 0, cx * (1 - s)], [0, s, cy * (1 - s)]], np.float64)


def cuts_from_args(a):
    if '--cortes' in a:
        return a[a.index('--cortes') + 1].split(',')
    return list(R)


# ================================================================================================ 1. timings
def tempos(cuts):
    """Word timings and caption pages, aligned on the temp VO with legendas.py's own aligner, at this file's starts."""
    vt = json.load(open(os.path.join(VO, 'vo_tempos.json')))
    res = {}
    for cut in cuts:
        r = R[cut]
        allw = {}
        for part, t0 in STARTS.items():
            t0 = STARTS_CUT.get(cut, {}).get(part, t0)
            x, sr = LG.read(os.path.join(VO, f'{cut}_{part}.wav'))
            ws = LG.align(r[part], x, sr)
            for w in ws:
                w['t0'] = round(w['t0'] + t0, 3)
                w['t1'] = round(w['t1'] + t0, 3)
            pgs = LG.pages(ws)
            for pg in pgs:
                n = sum(len(l) for l in pg['linhas'])
                pg['cps'] = round(n / max(pg['t1'] - pg['t0'], 1e-3), 1)        # over the spoken words only
            v = vt[f'{cut}_{part}']
            allw[part] = dict(inicio_audio_s=t0, palavras=ws, paginas=pgs, fala_s=[ws[0]['t0'], ws[-1]['t1']],
                              arquivo_s=v['duracao_s'], velocidade_tts=v['velocidade'],
                              janela_s={'gancho': [0.0, 2.0], 'corpo': [2.0, 6.0], 'kv_vo': [9.0, 15.0]}[part])
        # reading rate over the time each page is actually on screen (a page holds until the next starts; the body's
        # last page to 6,0 s; the KV caption for its display window)
        seq = [pg for part in ('gancho', 'corpo') for pg in allw[part]['paginas']]
        for i, pg in enumerate(seq):
            end = seq[i + 1]['t0'] if i + 1 < len(seq) else 6.0
            pg['cps_leitura'] = round(sum(len(l) for l in pg['linhas']) / max(end - pg['t0'], 1e-3), 1)
        kv = allw['kv_vo']['paginas'][0]
        kv['cps_leitura'] = round(sum(len(l) for l in kv['linhas']) / max(kv['t1'] + 0.75 - kv['t0'], 1.5), 1)
        res[cut] = allw
    return res


# ================================================================================================ 2. overlay layers
def camadas(cuts, T):
    from render import renderizar
    import tipo_kv
    os.makedirs(LAY, exist_ok=True)
    html = os.path.join(HERE, 'camadas.html')
    jobs, index = [], {}

    def add(key, dados, path=None, html_=html):
        p = path or os.path.join(LAY, key + '.png')
        index[key] = p
        jobs.append(dict(html=html_, saida=p, w=W, h=H, dados=dados, transparente=True))
    for cut in cuts:
        r = R[cut]
        add('tag_' + cut, dict(modo='tag', t=r['tag']))
        add('gesto_' + cut, dict(modo='gesto', t=r['gesto']))
        for part in ('gancho', 'corpo'):
            for pi, pg in enumerate(T[cut][part]['paginas']):
                for k in range(len(pg['palavras'])):
                    add(f'leg_{cut}_{part}_{pi}_{k}', dict(modo='legenda', linhas=pg['linhas'], ativa=k))
        if kv_caption(cut):
            pg = T[cut]['kv_vo']['paginas'][0]
            add('kvleg_' + cut, dict(modo='kvlegenda', linhas=pg['linhas']))
        if cut[0] == '2':
            add('abertura', dict(modo='abertura', t='abertura: você'))
        hl = r['headline']
        j = tipo_kv.job('kv45', os.path.join(LAY, 'kvtipo_%s.png' % hl.replace(' ', '_').replace('.', '')),
                        dict(headline=hl))
        index['kvtipo_' + cut] = j['saida']
        jobs.append(j)
    # dedupe identical jobs (same output path)
    seen, uniq = set(), []
    for j in jobs:
        if j['saida'] not in seen:
            seen.add(j['saida'])
            uniq.append(j)
    out = renderizar(uniq, verbose=False)
    qa = {os.path.basename(j['saida']): o for j, o in zip(uniq, out)}
    bad = {k: v['console'] for k, v in qa.items() if v['console']}
    if bad:
        raise RuntimeError('console errors: %s' % bad)
    json.dump(dict(index=index, info={k: v.get('info') for k, v in qa.items()},
                   qa_kv={k: v.get('qa') for k, v in qa.items() if k.startswith('kvtipo')}),
              open(os.path.join(LAY, 'index.json'), 'w'), ensure_ascii=False, indent=1)
    print('camadas:', len(uniq), 'PNGs')


# ================================================================================================ 3. sound
def loudness(path):
    sys.path.insert(0, os.path.join(B, 'sound'))
    import dsp
    import pyloudnorm as pyln
    x = dsp.stereo(dsp.read(path))
    return pyln.Meter(48000).integrated_loudness(x)


def som(cuts, T):
    os.makedirs(SOM, exist_ok=True)
    rep = {}
    for cut in cuts:
        c = cut[0]
        t = T[cut]
        cues = [dict(label='tom de sala (auditório) 0–9 s', file='sfx/HLF-SFX-15_tom_de_sala_loop.wav', start_s=0.0,
                     dur_s=9.0, loop=True, gain_db=-26, fade_in=0.08, fade_out=0.01)]
        for part in ('gancho', 'corpo', 'kv_vo'):
            p = os.path.join(VO, f'{cut}_{part}.wav')
            cues.append(dict(label='VO ' + part, file=p, start_s=t[part]['inicio_audio_s'],
                             gain_db=round(VO_LUFS - loudness(p), 2)))
        if c == '1':
            cues.append(dict(label='quatro palmas no auditório (1ª em f151)', file='sfx/HLF-SFX-06f_palmas_quatro_auditorio.wav',
                             frame=151, sync='onset', gain_db=6))
            bed = 'filmes/HLF-AD_KV_9a15s_ads1e3_som.wav'
        elif c == '2':
            if cut == '2A':
                cues.append(dict(label='primeiro sinal sob a palavra (f0)', file='sfx/HLF-SFX-09_sino_teatro.wav',
                                 frame=0, sync='onset', gain_db=1, dur_s=3.4, fade_out=1.2))
            cues.append(dict(label='segundo sinal 6,0 s (f144)', file='sfx/HLF-SFX-09_sino_teatro.wav', frame=144,
                             sync='onset', gain_db=4, dur_s=2.95, fade_out=0.8))
            bed = 'filmes/HLF-AD_KV_9a15s_ad2_sino_som.wav'
        else:
            cues.append(dict(label='caixa no apontar (f180)', file='musica/pecas/HLF-MUS-02_caixa_acento.wav',
                             frame=180, sync='onset', gain_db=4))
            bed = 'filmes/HLF-AD_KV_9a15s_ads1e3_som.wav'
        v0, v1 = t['kv_vo']['fala_s']
        d0, d1 = v0 - 9.0, v1 - 9.0
        cues.append(dict(label='cama KV 9–15 s (equipe de som), abaixada 8 dB sob a VO', file=bed, start_s=9.0, gain_db=0,
                         envelope=[[0, 0], [round(d0 - 0.07, 3), 0], [round(d0 - 0.01, 3), -8], [round(d1 + 0.05, 3), -8],
                                   [round(d1 + 0.30, 3), 0], [6.0, 0]]))
        spec = dict(duracao_s=15.0, fps=FPS, alvo_lufs=-14, teto_dbtp=-1, cues=cues)
        cj = os.path.join(SOM, cut + '_cues.json')
        json.dump(spec, open(cj, 'w'), ensure_ascii=False, indent=1)
        wav = os.path.join(SOM, cut + '.wav')
        r = subprocess.run([PY, '-I', os.path.join(B, 'sound', 'mix.py'), cj, wav], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(r.stderr[-1500:])
        print(r.stdout.strip())
        rep[cut] = json.load(open(os.path.join(SOM, cut + '.json')))
    return rep


def onset_near(rep, t, tol=0.09):
    ons = [o['t_s'] for o in rep['onsets_medidos']]
    if not ons:
        return None
    k = int(np.argmin([abs(o - t) for o in ons]))
    return ons[k] if abs(ons[k] - t) <= tol else None


# ================================================================================================ 4. frames
def load_rgba(path):
    a = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if a is None:
        raise FileNotFoundError(path)
    al = a[..., 3]
    ys, xs = np.where(al > 0)
    if not len(ys):
        return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgb = a[y0:y1, x0:x1, :3].astype(np.float32) / 255.0
    alpha = a[y0:y1, x0:x1, 3:4].astype(np.float32) / 255.0
    return (y0, y1, x0, x1, rgb, alpha)


def over(img, lay):
    if lay is None:
        return
    y0, y1, x0, x1, rgb, a = lay
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + rgb * a


class Plates:
    def __init__(self):
        self.c = {}

    def get(self, name):
        if name not in self.c:
            p = os.path.join(PLATES, name + '.png')
            a = cv2.imread(p, cv2.IMREAD_UNCHANGED)
            if a is None:
                raise FileNotFoundError(p)
            self.c[name] = (a.astype(np.float32) / (65535.0 if a.dtype == np.uint16 else 255.0))[..., :3]
        return self.c[name]


def warp_plate(src, s=1.0, pivot=(540, 960)):
    """One resample: upscale the half-res previs plate to 1080 x 1920 and push by s about pivot."""
    h, w = src.shape[:2]
    k = W / w
    off = (k - 1) / 2.0                    # pixel-centre alignment of a k x upscale
    px, py = pivot
    M = np.array([[k * s, 0, s * off + px * (1 - s)], [0, k * s, s * off + py * (1 - s)]], np.float64)
    return cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)


def gesture_key(cut, f, claps):
    """Which gesture plate key shows on frame f (6,0–9,0 s), keyed to the measured onsets."""
    c = cut[0]
    if c == '1':
        # hands meet ON each measured clap onset frame and stay 2 frames; one in-between before and after
        for cf in claps:
            if cf <= f <= cf + 1:
                return 'B'
            if f == cf - 1 or f == cf + 2:
                return 'M'
        return 'A'
    if c == '2':
        # a slow sway, ~2,4 s per cycle, stepped through five rendered roll keys
        ang = 3.2 * math.sin(2 * math.pi * (f - 144) / (2.4 * FPS))
        keys = [('L2', -3.2), ('L1', -1.6), ('C', 0.0), ('R1', 1.6), ('R2', 3.2)]
        return min(keys, key=lambda kv: abs(kv[1] - ang))[0]
    # Ad 3: finger-heart, the turn, the point landing ON the snare onset frame
    sn = claps[0]
    if f >= sn:
        return 'B'
    if f >= sn - 3:
        return 'M'
    return 'A'


def caption_key(cut, T, t):
    """(layer key) of the caption page on screen at time t (0–6 s), or None. A page holds until the next page starts;
    the hook's last page holds to the body's first word, the body's last page to 6,0 s."""
    pages = []
    for part in ('gancho', 'corpo'):
        for pi, pg in enumerate(T[cut][part]['paginas']):
            pages.append((part, pi, pg))
    cur = None
    for i, (part, pi, pg) in enumerate(pages):
        end = pages[i + 1][2]['t0'] if i + 1 < len(pages) else 6.0
        if pg['t0'] <= t < end:
            cur = (part, pi, pg)
    if cur is None:
        return None
    part, pi, pg = cur
    k = 0
    for j, w in enumerate(pg['palavras']):
        if w['t0'] <= t:
            k = j
    return f'leg_{cut}_{part}_{pi}_{k}'


class Composer:
    """Every frame of one cut, composed from the plates, the overlay layers and the KV-45, keyed to the measured mix."""
    _layers, _plates, _kv = {}, Plates(), None

    def __init__(self, cut, T, rep):
        self.cut, self.T, self.c = cut, T, cut[0]
        self.idx = json.load(open(os.path.join(LAY, 'index.json')))['index']
        if Composer._kv is None:
            kvp = cv2.imread(KV16, cv2.IMREAD_UNCHANGED)
            if kvp is None or kvp.shape[:2] != (H, W):
                raise SystemExit('KV-45 plate missing or not 1080 x 1920: ' + KV16)
            Composer._kv = kvp.astype(np.float32) / (65535.0 if kvp.dtype == np.uint16 else 255.0)
        c = self.c
        # --- keys from the measured mix
        lit = 220 if c == '2' else KV0
        clac = onset_near(rep, lit / FPS)
        if clac is not None:
            lit = int(round(clac * FPS))
        if c == '1':
            nominal = [151 + o * FPS for o in (0.0, 0.6803, 1.3595, 2.04)]
            claps = [int(round((onset_near(rep, x / FPS) or x / FPS) * FPS)) for x in nominal]
        elif c == '3':
            claps = [int(round((onset_near(rep, 180 / FPS) or 180 / FPS) * FPS))]
        else:
            claps = []
        kvleg = T[cut]['kv_vo']['paginas'][0]
        self.kvleg_on = (kvleg['t0'], max(kvleg['t1'] + 0.75, kvleg['t0'] + 1.5)) if kv_caption(cut) else None
        self.ab_on = T[cut]['corpo']['paginas'][-1]['palavras'][-1]['t0'] if c == '2' else None
        self.lit, self.claps, self.clac = lit, claps, clac
        self.tp = talk_plate(cut)
        self.pivot = HEAD['USHER' if self.tp.startswith('USHER') else 'SIT']
        self.kv_f, self.kv_img = None, None

    def log(self):
        return dict(kv_aceso_quadro=self.lit, clac_medido_s=self.clac, palmas_ou_caixa_quadros=self.claps,
                    legenda_kv_s=[round(x, 3) for x in self.kvleg_on] if self.kvleg_on else
                    'sem legenda: a fala é o título ou a assinatura já na tela (diretor, 6 out 2026)', abertura_s=self.ab_on,
                    placas=dict(fala=self.tp, gesto=gesture_plates(self.cut)))

    def L(self, key):
        if key not in Composer._layers:
            Composer._layers[key] = load_rgba(self.idx[key])
        return Composer._layers[key]

    def frame(self, f):
        cut, T, t = self.cut, self.T, f / FPS
        if f < 144:
            img = warp_plate(self._plates.get(self.tp), talk_scale(cut, t), self.pivot)
            over(img, self.L('tag_' + cut))
            ck = caption_key(cut, T, t)
            if ck:
                over(img, self.L(ck))
            if self.ab_on is not None and t >= self.ab_on:
                over(img, self.L('abertura'))
        elif f < KV0:
            g = gesture_plates(cut) + '_' + gesture_key(cut, f, self.claps)
            img = warp_plate(self._plates.get(g), 1.0)
            over(img, self.L('gesto_' + cut))
        elif f < self.lit:
            img = np.zeros((H, W, 3), np.float32)      # Ad 2: the blackout between the third bell and the CLAC
        else:
            if self.kv_f != f:
                self.kv_f = f
                self.kv_img = cv2.warpAffine(Composer._kv, kv_affine(f), (W, H), flags=cv2.INTER_LANCZOS4,
                                             borderMode=cv2.BORDER_REFLECT)
            img = self.kv_img.copy()
            over(img, self.L('kvtipo_' + cut))
            if self.kvleg_on and self.kvleg_on[0] <= t < self.kvleg_on[1]:
                over(img, self.L('kvleg_' + cut))
        return (np.clip(img, 0, 1) * 255.0 + 0.5).astype(np.uint8)       # BGR (plates and layers read by OpenCV)


def quadros(cuts, T, SR_):
    os.makedirs(OUT, exist_ok=True)
    log = {}
    for cut in cuts:
        C = Composer(cut, T, SR_[cut])
        log[cut] = C.log()
        fdir = os.path.join(TMP, 'quadros', cut)
        shutil.rmtree(fdir, ignore_errors=True)
        os.makedirs(fdir)
        for f in range(N):
            cv2.imwrite(os.path.join(fdir, 'f%04d.png' % f), C.frame(f), [cv2.IMWRITE_PNG_COMPRESSION, 1])
        name = 'HLF-AD-%s_%s_animatic' % (cut, SLUG[cut[0]])
        enc = os.path.join(B, 'tools', 'codificar.py')
        mp_som = os.path.join(OUT, name + '_som.mp4')
        mp_mudo = os.path.join(OUT, name + '_mudo.mp4')
        subprocess.run([PY, enc, fdir, mp_som, '--fps', str(FPS), '--trilha', os.path.join(SOM, cut + '.wav')], check=True)
        subprocess.run([PY, enc, fdir, mp_mudo, '--fps', str(FPS)], check=True)
        log[cut]['arquivos'] = [os.path.relpath(mp_som, KIT), os.path.relpath(mp_mudo, KIT)]
        shutil.rmtree(fdir, ignore_errors=True)
        print('quadros', cut, '->', os.path.basename(mp_som), os.path.basename(mp_mudo), flush=True)
    return log


def prova(cuts, T, SR_, frames):
    """Proof sheet of chosen frames straight from the compositor (before encoding)."""
    for cut in cuts:
        C = Composer(cut, T, SR_[cut])
        ims = [cv2.resize(C.frame(f), (270, 480), interpolation=cv2.INTER_AREA) for f in frames]
        row = np.hstack(ims)
        cv2.imwrite(os.path.join(TMP, 'teste', 'prova_%s.png' % cut), row)


# ================================================================================================ 5. contact sheets
def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


class Stream:
    """Decode the delivered MP4 frame by frame through a pipe (BT.709 limited range -> full-range RGB, the way a phone
    shows it), from frame `start` on. Holding a whole 1080 x 1920 master in memory would take 2,2 GB."""
    def __init__(self, mp4, start=0):
        vf = 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24'
        if start:
            vf = "select='gte(n,%d)'," % start + vf
        self.p = subprocess.Popen([ffmpeg(), '-loglevel', 'error', '-i', mp4, '-vf', vf, '-vsync', '0', '-f', 'rawvideo',
                                   '-'], stdout=subprocess.PIPE)
        self.n = W * H * 3

    def next(self):
        b = self.p.stdout.read(self.n)
        if len(b) < self.n:
            return None
        return np.frombuffer(b, np.uint8).reshape(H, W, 3)

    def close(self):
        self.p.stdout.close()
        self.p.wait()


def decode(mp4, frames):
    s = Stream(mp4)
    out, f, want = {}, 0, set(frames)
    while want:
        fr = s.next()
        if fr is None:
            break
        if f in want:
            out[f] = fr.copy()
            want.discard(f)
        f += 1
    s.close()
    return out


def folhas(cuts, T):
    from PIL import Image, ImageDraw, ImageFont
    fonts = os.path.join(B, 'fonts')
    fC = lambda s: ImageFont.truetype(os.path.join(fonts, 'SpecialGothicCondensedOne-Regular.ttf'), s)
    times = [0.5, 2.5, 4.5, 7.5, 10.0, 14.0]
    tw, th, g, top = 400, 711, 24, 236
    for cut in cuts:
        c = cut[0]
        r = R[cut]
        name = 'HLF-AD-%s_%s_animatic' % (cut, SLUG[c])
        v = decode(os.path.join(OUT, name + '_som.mp4'), [int(round(ts * FPS)) for ts in times])
        Wd = 3 * tw + 4 * g
        Hd = top + 2 * (th + 46) + g
        sheet = Image.new('RGB', (Wd, Hd), (0x12, 0x10, 0x14))
        d = ImageDraw.Draw(sheet)
        papel, cinza = (0xFF, 0xF8, 0xEC), (0xB8, 0xB0, 0xA8)
        d.text((g, 20), f'HOLOFOTE · O ANÚNCIO · {cut} · {r["conceito"]} · {r["apresentador"]} · ANIMATIC (PREVIS)',
               font=fC(38), fill=(0xFF, 0xE8, 0x1A))
        d.text((g, 74), f'0–2 s  “{r["gancho"]}”   ·   credencial: {r["tag"]}', font=fC(24), fill=papel)
        d.text((g, 106), f'2–6 s  “{r["corpo"]}”', font=fC(24), fill=papel)
        d.text((g, 138), f'6–9 s  título: {r["gesto"]}   ·   9–15 s  VO “{r["kv_vo"]}” · título do KV: {r["headline"]}'
               + ('' if kv_caption(cut) else '  (sem legenda: a fala já está na tela)'), font=fC(24), fill=papel)
        d.text((g, 178), 'manequim cinza no lugar das tomadas de pessoas · VO temporária (Kokoro) · 9–15 s = KV-45 real · '
               'quadros tirados do MP4 entregue', font=fC(21), fill=cinza)
        for i, ts in enumerate(times):
            f = int(round(ts * FPS))
            im = Image.fromarray(v[f]).resize((tw, th), Image.LANCZOS)
            x = g + (i % 3) * (tw + g)
            y = top + (i // 3) * (th + 46)
            sheet.paste(im, (x, y))
            d.text((x, y + th + 8), f'{ts:.1f} s · quadro {f}'.replace('.', ','), font=fC(26), fill=(0xFF, 0xF8, 0xEC))
        p = os.path.join(OUT, name + '_folha.png')
        sheet.save(p)
        print('folha', p)


# ================================================================================================ 6. fidelity
def _aov_raw(path):
    import OpenEXR
    ch = OpenEXR.File(path).parts[0].channels

    def get(name):
        for k, v in ch.items():
            if k == name or k.startswith(name + '.') or k.split('.')[0] == name:
                return v.pixels
        raise KeyError(name)
    uv = get('label_uv')[..., :2].astype(np.float32)
    ink = get('label_ink')
    mask = get('label_mask')
    ink = ink[..., 0] if ink.ndim == 3 else ink
    mask = mask[..., 0] if mask.ndim == 3 else mask
    return uv, ink.astype(np.float32), mask.astype(np.float32)


def aov_at(raw, f):
    """The KV's label AOVs moved by the SAME affine as the picture on frame f. The EXR channels are pixel-filtered
    (premultiplied by coverage), so they are warped as stored and load_aov's own division by the mask applies."""
    uv, ink, mask = raw
    M = kv_affine(f)
    wa = lambda a: cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return np.dstack([wa(uv[..., 0]), wa(uv[..., 1])]), wa(ink), wa(mask)


def write_exr(path, uv, ink, mask):
    import OpenEXR
    z = np.zeros_like(mask)
    ch = {'label_uv': np.dstack([uv[..., 0], uv[..., 1], z, mask]).astype(np.float32),
          'label_ink.V': ink.astype(np.float32), 'label_mask.V': mask.astype(np.float32)}
    OpenEXR.File({'compression': OpenEXR.ZIP_COMPRESSION, 'type': OpenEXR.scanlineimage}, ch).write(path)


def fidelidade(cuts):
    """Every KV frame (9–15 s) of every master, decoded from the delivered MP4, against the master label.

    Method: fidelidade_uv.py's own functions and bars. For frame f the AOV is transformed by the frame's push
    (aov_at); the reference and the planted-error reference depend only on f, so they are built once per frame and
    scored against all eight masters (check() would rebuild them eight times). The stock CLI is run unmodified on
    two frames as a cross-check of this path (scale 1,000 with the untouched EXR; scale 1,030 with a written EXR)."""
    import fidelidade_uv as F
    m = cv2.imread(MASTER, cv2.IMREAD_UNCHANGED)
    alpha = m[..., 3].astype(np.float32) / 255.0
    raw = _aov_raw(KV_AOV)
    vids = {}
    for cut in cuts:
        name = 'HLF-AD-%s_%s_animatic' % (cut, SLUG[cut[0]])
        vids[cut] = os.path.join(OUT, name + '_som.mp4')
    # stream every master's KV frames (and its silent twin, which must carry the identical picture) in lockstep
    st = {cut: Stream(vids[cut], KV0) for cut in cuts}
    mu = {cut: Stream(vids[cut].replace('_som.mp4', '_mudo.mp4'), KV0) for cut in cuts}
    same = {cut: True for cut in cuts}
    keep = {cut: {} for cut in cuts}           # the two CLI cross-check frames
    coat = F.hex_lab('#FFE81A')
    h_ref = float(F.hue_deg(coat[None, :])[0])
    s_ref = np.hypot(coat[1] - 128, coat[2] - 128) / max(coat[0], 1)
    rows = {cut: [] for cut in cuts}
    for f in range(KV0, N):
        uvr, inkr, maskr = aov_at(raw, f)
        mk = np.clip(maskr, 1e-6, None)
        uv = uvr / mk[..., None]
        mask = maskr
        valid = mask > 0.98
        ys, xs = np.where(mask > 0)
        y0, y1, x0, x1 = max(ys.min() - 8, 0), min(ys.max() + 9, H), max(xs.min() - 8, 0), min(xs.max() + 9, W)
        E = np.zeros((H, W), np.float32)
        E[y0:y1, x0:x1] = F.sample_master(alpha, uv[y0:y1, x0:x1])
        alt, box = F.plant_error(alpha, uv, mask)
        E2 = np.zeros((H, W), np.float32)
        E2[y0:y1, x0:x1] = F.sample_master(alt, uv[y0:y1, x0:x1])
        agree = float(np.corrcoef(E[valid], (inkr / mk)[valid])[0, 1])
        ref = ((1.0 - E) * 255.0).astype(np.float32)
        ref2 = ((1.0 - E2) * 255.0).astype(np.float32)
        bare = valid & (E < 0.02)
        bare = cv2.erode(bare.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        for cut in cuts:
            rgb = st[cut].next()
            twin = mu[cut].next()
            if twin is None or not np.array_equal(rgb, twin):
                same[cut] = False
            if f in (KV0 + 4, N - 1) or (f == KV0 and cut[0] != '2'):
                keep[cut][f] = rgb.copy()
            lit = 220 if cut[0] == '2' else KV0
            if f < lit:
                rows[cut].append(dict(quadro=f, preto=True, media_rgb=round(float(rgb.mean()), 2)))
                continue
            bgr = rgb[..., ::-1]
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
            sk = []
            s = np.array([v for _, _, v in F.score(gray, ref, valid, E, sk)])
            s2 = np.array([v for _, _, v in F.score(gray, ref2, valid, E2)])
            lab = cv2.cvtColor(np.ascontiguousarray(bgr), cv2.COLOR_BGR2LAB).astype(np.float32)
            bb = bare & (lab[..., 0] > 40) & (lab[..., 0] < 250)
            hd = (F.hue_deg(lab[bb]) - h_ref + 180) % 360 - 180
            px = lab[bb]
            sat = float(np.median(np.hypot(px[:, 1] - 128, px[:, 2] - 128) / np.maximum(px[:, 0], 1)) / s_ref)
            rows[cut].append(dict(quadro=f, escala=round(kv_scale(f), 5), tiles=int(len(s)), cantos_pulados=len(sk),
                                  cantos_worst=round(min(v for _, _, v in sk), 3) if sk else None,
                                  worst=round(float(s.min()), 3),
                                  p5=round(float(np.percentile(s, 5)), 3), controle_worst=round(float(s2.min()), 3),
                                  controle_pego=bool(s2.min() < F.MIN_TILE_PASS), uv_agreement=round(agree, 4),
                                  hue_shift_deg=round(float(np.median(hd)), 2), sat_ratio=round(sat, 3)))
        if f % 24 == 0:
            print('fidelidade quadro', f, {c: rows[c][-1].get('worst') for c in cuts}, flush=True)
    for cut in cuts:
        st[cut].close()
        mu[cut].close()
    summary = {}
    for cut in cuts:
        rr = [x for x in rows[cut] if not x.get('preto')]
        w = min(x['worst'] for x in rr)
        p5 = min(x['p5'] for x in rr)
        ctl = all(x['controle_pego'] for x in rr)
        hue = max(abs(x['hue_shift_deg']) for x in rr)
        sat = min(x['sat_ratio'] for x in rr)
        ok = (w >= F.MIN_TILE_PASS and p5 >= F.P5_FILM and ctl and hue <= F.MAX_HUE_SHIFT and sat >= F.MIN_SAT_RATIO)
        summary[cut] = dict(quadros_com_rotulo=len(rr), quadros_pretos=len(rows[cut]) - len(rr), pior_tile_min=w,
                            p5_min=p5, controle_pego_em_todos=ctl, controle_worst_max=max(x['controle_worst'] for x in rr),
                            hue_shift_max_deg=hue, sat_ratio_min=sat, mudo_identico_ao_som=same[cut], passa=bool(ok))
    # cross-check with the stock CLI on two frames of the first cut
    cut = cuts[0]
    tmpd = os.path.join(TMP, 'fid_cli')
    os.makedirs(tmpd, exist_ok=True)
    cli = {}
    for f in (KV0 + (4 if cut[0] == '2' else 0), N - 1):
        png = os.path.join(tmpd, f'{cut}_f{f}.png')
        cv2.imwrite(png, keep[cut][f][..., ::-1])
        if abs(kv_scale(f) - 1.0) < 1e-9:
            exr = KV_AOV
        else:
            exr = os.path.join(tmpd, f'aov_f{f}.exr')
            write_exr(exr, *aov_at(raw, f))
        r = subprocess.run([PY, os.path.join(B, 'tools', 'fidelidade_uv.py'), '--master', MASTER, '--aov', exr, '--asset', png,
                            '--coat', '#FFE81A', '--film'], capture_output=True, text=True)
        cli[f'{cut}_f{f}'] = json.loads(r.stdout)[0]
        mine = rows[cut][f - KV0]
        cli[f'{cut}_f{f}']['este_caminho'] = {k: mine[k] for k in ('worst', 'p5', 'controle_worst', 'hue_shift_deg', 'sat_ratio')}
    rep = dict(ferramenta='_build/tools/fidelidade_uv.py (funções e barras dela), via _build/anuncio/animatic.py fidelidade',
               metodo=('Cada quadro 9–15 s de cada mestre, DECODIFICADO do MP4 entregue (BT.709 -> RGB). O AOV do KV-45 '
                       '(_build/shots/aov/KV-45_aceso/0001.exr) é transformado pela MESMA afim do empurrão daquele quadro '
                       '(escala 1,000 -> 1,030 em torno do centro do quadro; canais pré-multiplicados pela cobertura, '
                       'interpolação linear) e a referência é reconstruída do mestre nessa geometria. Erro plantado em '
                       'todo quadro. Barras de filme: pior bloco >= 0,80, p5 >= 0,93, controle pego.'),
               master=os.path.relpath(MASTER, KIT), aov=os.path.relpath(KV_AOV, KIT), kv=os.path.relpath(KV16, KIT),
               barras=dict(pior_tile=F.MIN_TILE_PASS, p5_filme=F.P5_FILM, hue_max_deg=F.MAX_HUE_SHIFT, sat_min=F.MIN_SAT_RATIO),
               resumo=summary, conferencia_cli=cli, quadros=rows)
    os.makedirs(FIDDIR, exist_ok=True)
    p = os.path.join(FIDDIR, 'ANUNCIO_animatics_KV.json')
    json.dump(rep, open(p, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: {kk: v[kk] for kk in ('worst_tile', 'p5_tile', 'pass')} | {'este_caminho': v['este_caminho']}
                      for k, v in cli.items()}, indent=1, ensure_ascii=False))
    return rep


# ================================================================================================ main
def main():
    a = sys.argv[1:]
    etapas = [x for x in a if x in ('vo', 'camadas', 'som', 'prova', 'quadros', 'folhas', 'fidelidade')] or \
        ['vo', 'camadas', 'som', 'quadros', 'folhas', 'fidelidade']
    cuts = cuts_from_args(a)
    os.makedirs(TMP, exist_ok=True)
    if 'vo' in etapas:
        subprocess.run([TTS, os.path.join(HERE, 'vo.py'), VO], check=True)
    T = tempos(cuts)
    tj = os.path.join(TMP, 'tempos.json')
    old = json.load(open(tj)) if os.path.exists(tj) else {}
    old.update(T)
    json.dump(old, open(tj, 'w'), ensure_ascii=False, indent=1)
    if 'camadas' in etapas:
        camadas(cuts, T)
    SR_ = {}
    if 'som' in etapas:
        SR_ = som(cuts, T)
    else:
        SR_ = {c: json.load(open(os.path.join(SOM, c + '.json'))) for c in cuts}
    if 'prova' in etapas:
        fr = [int(x) for x in a[a.index('--quadros') + 1].split(',')] if '--quadros' in a else [12, 60, 108, 160, 216, 300]
        prova(cuts, T, SR_, fr)
    if 'quadros' in etapas:
        log = quadros(cuts, T, SR_)
        lj = os.path.join(OUT, 'animatic_tempos.json')
        old = json.load(open(lj)) if os.path.exists(lj) else {}
        for cut in cuts:
            old[cut] = dict(chaves=log[cut], vo={p: {k: T[cut][p][k] for k in ('inicio_audio_s', 'fala_s', 'arquivo_s',
                                                                                'velocidade_tts', 'janela_s')}
                                                 for p in ('gancho', 'corpo', 'kv_vo')},
                            legendas={p: [dict(linhas=pg['linhas'], t0=pg['t0'], t1=pg['t1'], cps_fala=pg['cps'],
                                               cps_leitura=pg['cps_leitura'])
                                          for pg in T[cut][p]['paginas']] for p in ('gancho', 'corpo', 'kv_vo')},
                            som=dict(lufs_i=SR_[cut].get('lufs_i'), true_peak_dbtp=SR_[cut].get('true_peak_dbtp'),
                                     cues=SR_[cut].get('cues')))
        json.dump(dict(sorted(old.items())), open(lj, 'w'), ensure_ascii=False, indent=1)
    if 'folhas' in etapas:
        folhas(cuts, T)
    if 'fidelidade' in etapas:
        fidelidade(cuts)


if __name__ == '__main__':
    main()
