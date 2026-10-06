"""HOLOFOTE · the edit, as data: one source of truth for compor.py, the EDL and FILM_PLAN.json (platform §E.4–§E.5).

Every film is a list of SHOTS (picture) and a function that returns the TYPE of each frame. Shots name their source
(a 3D render, a still plate, black, the lambe poster) and their MODE (hold, 2D push, 2D relight, flame crop, 3D frame).
Type is set by code on tipo_filme.html with the strings below, character for character from the platform frame tables.

    /home/user/venvs/web/bin/python _build/filmes/plano.py      -> 06_PRODUCAO/EDIT_DECISION_LIST.csv + FILM_PLAN.json

Slams are keyed to the sound team's MEASURED onsets (04_FILMES/som/filmes/*_som.json, `quadros_chave`): each slam's
first frame is the frame of the onset (rounded); plano.verificar_sincronia() reports the error, which must be ±1 frame.
"""
import os, json, math, csv
import comum as C

DUR = {'F15': 360, 'F06A': 144, 'F06B': 144, 'F06C_07-05': 144, 'F06C_08-05': 144, 'F06C_09-05': 144}
SOM = {'F15': 'HLF-F15_A_ENTRADA', 'F06A': 'HLF-F06A_CLAC', 'F06B': 'HLF-F06B_O_PIOR_SHOW',
       'F06C_07-05': 'HLF-F06C_SINAL_07-05', 'F06C_08-05': 'HLF-F06C_SINAL_08-05', 'F06C_09-05': 'HLF-F06C_SINAL_09-05'}
NOME = {'F15': 'F15_A-ENTRADA', 'F06A': 'F06A_CLAC', 'F06B': 'F06B_O-PIOR-SHOW',
        'F06C_07-05': 'F06C_SINAL_07-05', 'F06C_08-05': 'F06C_SINAL_08-05', 'F06C_09-05': 'F06C_SINAL_09-05'}

# ------------------------------------------------------------------------------------------------ motion constants
SQ_WDTH = [75, 104, 128]          # the poster squash, frames 0–2 of a slam; frame 3 is the final setting (wdth 125)
SQ_SX = [0.60, 0.84, 1.024]       # the same squash for the static Condensed One (horizontal scale; no wdth axis)
AQUEC = [(0.10, 2000.0), (0.55, 2700.0)]    # CLAC filament warm-up, 2 frames: (light gain, colour temperature)
PUSH_F15 = (222, 359, 0.04)       # 2D dolly push on the KV-45 plate: frames, amount
PUSH_F06A = (24, 95, 0.03)
PUSH_CENTRO = (540.0, 760.0)      # the push expands about the label's upper half: the flame keeps clear of the type


def ease_out(t, p=1.6):
    t = min(1.0, max(0.0, t))
    return 1.0 - (1.0 - t) ** p


def ease_in_out(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def push(f, spec):
    f0, f1, amt = spec
    if f < f0:
        return 1.0
    return 1.0 + amt * ease_out((f - f0) / (f1 - f0))


def squash(f, f0, vf=True):
    i = f - f0
    if 0 <= i < 3:
        return {'wdth': SQ_WDTH[i]} if vf else {'sx': SQ_SX[i]}
    return None


def voo(f, f0, n, dist):
    """Fly-out upward over n frames from f0 (ease-in, accelerating): (dy, motion-blur length px). None = gone."""
    if f < f0:
        return 0.0, 0.0
    i = f - f0 + 1
    if i >= n:
        return None

    def y(k):
        return -dist * (k / n) ** 2.2
    v = y(i) - y(i - 1)
    return y(i), abs(v) * 0.5


def bnce(f, f0, f1):
    """Shantell bounce axis while a line draws on: ±20 (§D.2), 0 at rest."""
    if f < f0 or f >= f1:
        return 0
    return round(20 * math.sin(2 * math.pi * (f - f0) / 6.0))


# ------------------------------------------------------------------------------------------------ type helpers
def L(t, f, y, **k):
    d = dict(k='linha', id=k.pop('id', t), t=t, f=f, y=y)
    d.update(k)
    return d


SEG = dict(t='nunca deixe a vela acesa sem supervisão.', f='C', cap=22, lsEm=0.02, cor='papel', op=0.85, al='center')
LOCK_FILL = dict(t='holofote nela.', f='X', fill='tamanho', lsEm=-0.01, cor='papel')


def camada(*els):
    return {'camada': list(els)}


# ------------------------------------------------------------------------------------------------ F15 · A ENTRADA
F15_TIPO_INFO = """f0–11 DOMINGO · 09.05 (amarelo, Condensed One, cap 46, centred, cap centre y 600) · f14–17 A ATRAÇÃO É ELA. slams
(squash wdth 75→128→125), fills 800, baseline 391 · f36–43 flies out upward · KV-01 lineup: L1 f44, MÃE f60, AO VIVO
f84, DOMINGO · 09.05 f108 (slams), abertura: f132–143, você f144–155 (draw on, BNCE ±20) · lineup flies out from f156,
staggered 2 f per line · f212 O MENOR HOLOFOTE DO BRASIL. (hard cut, fills, baseline 396) · f222 PRA MAIOR ATRAÇÃO.
(fills, baseline 420) · f288 holofote nela. (fills, baseline 410) · f300 HOLOFOTE AO VIVO · vela aromática · 200 g
(cap 26, baseline 466) + nunca deixe a vela acesa sem supervisão. (cap 22, baseline 508)"""

LINEUP = [('L1E', 44, 156, False), ('L1D', 44, 156, False), ('MAE', 60, 158, True), ('SHOW', 84, 160, True),
          ('L4E', 108, 162, False), ('L4D', 132, 162, None)]
VOO_LINEUP = 6
VOO_ATR = 8


def tipo_F15(f, geom):
    """List of (camada, dy, blur) for F15 frame f. geom: ink boxes from a first layout pass (for fly-out distances)."""
    out = []
    if f <= 11:
        out.append((camada(L('DOMINGO · 09.05', 'C', 623, cap=46, lsEm=0.02, cor='amarelo', tnum=True, al='center')), 0, 0))
    if 14 <= f <= 43:
        v = voo(f, 36, VOO_ATR, geom['atr']['bot'] + 24)
        if v is not None:
            el = L('A ATRAÇÃO É ELA.', 'X', 391, id='atr', fill='tamanho', lsEm=-0.01, cor='papel', sq=squash(f, 14))
            out.append((camada(el), v[0], v[1]))
    # the KV-01 lineup, built piece by piece and flown out line by line
    grupos = {}
    for pid, t0, tv, vf in LINEUP:
        if f < t0:
            continue
        v = voo(f, tv, VOO_LINEUP, geom[pid]['bot'] + 24)
        if v is None:
            continue
        key = (round(v[0], 3), round(v[1], 3))
        g = grupos.setdefault(key, {'k': 'kv01', 'so': [], 'sq': {}, 'rv': {}, 'bnce': {}})
        g['so'].append(pid)
        if vf is not None:
            s = squash(f, t0, vf)
            if s:
                g['sq'][pid] = s
        else:
            # abertura: f132–143, você f144–155: the ink revealed left to right, a pen's pace
            ab = geom['L4D_ab']
            if f < 144:
                g['rv'][pid] = ab * (f - 131) / 12.0
            elif f < 156:
                g['rv'][pid] = ab + (1 - ab) * (f - 143) / 12.0
            g['bnce'][pid] = bnce(f, 132, 155)
    for key, g in grupos.items():
        out.append((camada(g), key[0], key[1]))
    if 212 <= f <= 221:
        out.append((camada(L('O MENOR HOLOFOTE DO BRASIL.', 'C', 396, fill='tamanho', lsEm=0.02, cor='papel')), 0, 0))
    if 222 <= f <= 287:
        out.append((camada(L('PRA MAIOR ATRAÇÃO.', 'C', 420, fill='tamanho', lsEm=0.02, cor='papel')), 0, 0))
    if f >= 288:
        els = [L(y=410, id='lock', **LOCK_FILL)]
        if f >= 300:
            els.append(L('HOLOFOTE AO VIVO · vela aromática · 200 g', 'C', 466, cap=26, lsEm=0.02, cor='papel', al='center',
                         tnum=True))
            els.append(L(y=508, id='seg', **SEG))
        out.append((camada(*els), 0, 0))
    return out


def fotos_F15():
    """Picture shots: (shot, first, last, source, mode, notes)."""
    return [
        ('F15-01', 0, 11, 'black', 'black', 'house dark; DOMINGO · 09.05 on black'),
        ('F15-02', 12, 13, 'render:_render/F15_camA_16bit.png', 'relight-2D warm-up', 'CLAC: the spot comes up 10 % at 2.000 K, 55 % at 2.700 K (scene-linear, exact PBR Neutral inverse)'),
        ('F15-03', 14, 161, 'render:_render/F15_camA_16bit.png', 'hold', 'cam A (KV-01 9:16 framing), the empty hard pool on the X (the crane eases in from f160: f160–161 move < 0,05 px)'),
        ('F15-04', 162, 175, 'render:_render/grua/f####_50.png', '3D frame 50 % + Lanczos 2x', 'crane + dolly A->B begins (ease in-out to f203); lift plate drops 100 mm f168–175; no candle in frame'),
        ('F15-05', 176, 203, 'render:_render/grua/f####_100.png', '3D frame 100 % + label AOV', 'the plate rises carrying the UNLIT candle, label to camera at yaw 12 deg, no rotation; locks flush and the camera settles at KV-45 on f203'),
        ('F15-06', 204, 209, 'black', 'black', 'BLACKOUT: the spot cuts in 1 frame (CLAC-off f204; fsst f206 is sound only)'),
        ('F15-07', 210, 221, 'render:_render/F15_blecaute_16bit.png + _render/chama_blecaute/c####.png', 'still + 2D relight (flame gain) + 3D flame crop', 'the wick catches f210–215 (scale 0,10 -> 1,0), then the flame alone in the black; label checked on the albedo pass'),
        ('F15-08', 222, 223, 'KV-45_aceso + F15_blecaute (+ crops)', 'relight-2D warm-up + 3D flame crop + 2D push', 'CLAC: the spot snaps back on: blackout + gain x (lit - blackout), scene-linear'),
        ('F15-09', 224, 359, 'KV-45_aceso_16bit.png + _render/chama_palco/c####.png', 'still + 3D flame crop loop + 2D push 0->4 %', 'the KV-45 end card; push f222–359 ease-out; flame flicker = 24-frame crop loop (±6 %, 2–4 Hz)'),
    ]


# ------------------------------------------------------------------------------------------------ F06A · CLAC
def tipo_F06A(f, geom):
    out = []
    if f <= 5:
        out.append((camada(L('09.05', 'C', 1002, cap=120, lsEm=0.02, cor='amarelo', tnum=True, al='center')), 0, 0))
    if 8 <= f <= 95:
        out.append((camada(L('A ATRAÇÃO É ELA.', 'X', 410, id='atr', fill='tamanho', capMax=110, lsEm=-0.01, cor='papel',
                             sq=squash(f, 8))), 0, 0))
    if 24 <= f <= 95:
        ab = geom['ab470']
        rv = ab * (f - 23) / 12.0 if f < 36 else (ab + (1 - ab) * (f - 35) / 12.0 if f < 48 else None)
        out.append((camada(L('abertura: você', 'S', 470, id='ab', x=18, cor='papel', al='right', ax=940, rv=rv,
                             bnce=bnce(f, 24, 47))), 0, 0))
    if f >= 96:
        out.append((camada(L(y=410, id='lock', **LOCK_FILL), L(y=508, id='seg', **SEG)), 0, 0))
    return out


def fotos_F06A():
    return [
        ('F06A-01', 0, 5, 'black', 'black', '09.05 on black'),
        ('F06A-02', 6, 7, 'KV-45_aceso + F15_blecaute (+ crops)', 'relight-2D warm-up + 3D flame crop', 'CLAC: the candle is already lit in the dark; the spot warms up over it'),
        ('F06A-03', 8, 23, 'KV-45_aceso_16bit.png + chama_palco', 'still + 3D flame crop loop', 'hold'),
        ('F06A-04', 24, 95, 'KV-45_aceso_16bit.png + chama_palco', 'still + 3D flame crop loop + 2D push 0->3 %', 'dolly push, ease-out'),
        ('F06A-05', 96, 143, 'KV-45_aceso_16bit.png + chama_palco', 'still + 3D flame crop loop, push held at 3 %', 'end card: holofote nela. + safety; claps f100/110/120'),
    ]


# ------------------------------------------------------------------------------------------------ F06B · O PIOR SHOW
PALAVRAS = [('ELA', 0), ('APLAUDIU', 12), ('DE PÉ', 24), ('O SEU', 36), ('PIOR', 48), ('SHOW.', 60)]


def tipo_F06B(f, geom):
    """F06B f0–83 is a poster (the type is part of the picture, it goes through O LAMBE); from f84 the KV-45 type zone."""
    if f <= 83:
        ver = [w for w, t in PALAVRAS if f >= t]
        sq = {}
        for w, t in PALAVRAS:
            s = squash(f, t)
            if s:
                sq[w] = s
        nota = 0.0 if f < 66 else min(1.0, (f - 65) / 12.0)
        seta = 0.0 if f < 78 else min(1.0, (f - 77) / 6.0)
        return [({'camada': [{'k': 'c03', 'y0': 370, 'ver': ver, 'sq': sq, 'nota': nota, 'seta': seta, 'bnce': bnce(f, 66, 77)}],
                  'fundo': 'amarelo'}, 0, 0)]
    return [(camada(L('SUA VEZ.', 'X', 442, id='hl', fill='tamanho', capMax=110, lsEm=-0.01, cor='papel'),
                    L('holofote nela.', 'X', 496, id='lk', cap=34, lsEm=-0.01, cor='papel', al='center'),
                    L(y=530, id='seg', **SEG)), 0, 0)]


def fotos_F06B():
    return [
        ('F06B-01', 0, 83, 'lambe:amarelo (C03 recipe, seed 303)', 'poster: flat type -> O LAMBE per frame', 'one word per beat (f0, 12, 24, 36, 48, 60), each fills the measure, poster squash; (girassol, 2007) + arrow draw on f66–83'),
        ('F06B-02', 84, 85, 'KV-45_aceso + F15_blecaute (+ crops)', 'relight-2D warm-up + 3D flame crop', 'hard cut; CLAC'),
        ('F06B-03', 86, 143, 'KV-45_aceso_16bit.png + chama_palco', 'still + 3D flame crop loop (hold)', 'SUA VEZ. + holofote nela. + safety; claps f120/130/140'),
    ]


# ------------------------------------------------------------------------------------------------ F06C · SINAL (template)
F06C = {
    '07-05': dict(sinos=1, titulo='PRIMEIRO SINAL.', sub='faltam 2 dias.', aceso=False),
    '08-05': dict(sinos=2, titulo='SEGUNDO SINAL.', sub='é amanhã.', aceso=False),
    '09-05': dict(sinos=3, titulo='TERCEIRO SINAL.', sub='é hoje.', aceso=True),
}


def tipo_F06C(data):
    v = F06C[data]

    def fn(f, geom):
        out = []
        if f <= 71:
            # title on the first bell (f0); Condensed One, papel, centred at y 760 (cap centre), fills the measure
            cap = geom['titulo']['cap']
            out.append((camada(L(v['titulo'], 'C', round(760 + cap / 2), id='titulo', fill='tamanho', lsEm=0.02, cor='papel')), 0, 0))
        if 24 <= f <= 71:
            rv = min(1.0, (f - 23) / 14.0)
            out.append((camada(L(v['sub'], 'S', 900, id='sub', x=36, cor='papel', al='center', rv=rv if rv < 1 else None,
                                 bnce=bnce(f, 24, 37))), 0, 0))
        if f >= 72:
            els = [L('MÃE AO VIVO', 'X', 442, id='mav', fill='tamanho', capMax=110, lsEm=-0.01, cor='papel',
                     trechos=[[0, 3, 'amarelo']]),
                   L('DOMINGO · 09.05', 'C', 496, id='dom', cap=34, lsEm=0.02, cor='amarelo', tnum=True, al='left', ax=140),
                   L('holofote nela.', 'X', 496, id='lk', cap=34, lsEm=-0.01, cor='papel', al='right', ax=940)]
            if v['aceso']:
                els.append(L(y=530, id='seg', **SEG))
            out.append((camada(*els), 0, 0))
        return out
    return fn


def fotos_F06C(data):
    v = F06C[data]
    st = 'KV-45_aceso' if v['aceso'] else 'KV-45_apagado'
    return [
        ('F06C-01', 0, 71, 'black', 'black', '%d bell(s) f0/8/16; %s on the first bell; %s draws on f24–37' % (v['sinos'], v['titulo'], v['sub'])),
        ('F06C-02', 72, 73, st + (' + F15_blecaute (+ crops)' if v['aceso'] else ''), 'relight-2D warm-up' + (' + 3D flame crop' if v['aceso'] else ''), 'CLAC f72'),
        ('F06C-03', 74, 143, st + '_16bit.png' + (' + chama_palco' if v['aceso'] else ''), 'still hold' + (' + 3D flame crop loop' if v['aceso'] else ''),
         'MÃE AO VIVO + DOMINGO · 09.05 + holofote nela.' + (' + safety' if v['aceso'] else '') + '; the stage is set'),
    ]


TIPO = {'F15': tipo_F15, 'F06A': tipo_F06A, 'F06B': tipo_F06B,
        'F06C_07-05': tipo_F06C('07-05'), 'F06C_08-05': tipo_F06C('08-05'), 'F06C_09-05': tipo_F06C('09-05')}
FOTOS = {'F15': fotos_F15, 'F06A': fotos_F06A, 'F06B': fotos_F06B,
         'F06C_07-05': lambda: fotos_F06C('07-05'), 'F06C_08-05': lambda: fotos_F06C('08-05'),
         'F06C_09-05': lambda: fotos_F06C('09-05')}

# picture/type events keyed to sound: (film, frame of the event, what, the sound key frame it is keyed to or None).
# Each keyed event is checked against the onset the sound team MEASURED in the final mix (±1 frame, §E.5).
SINCRONIA = [
    ('F15', 12, 'CLAC warm-up begins (cam A)', 12),
    ('F15', 14, 'A ATRAÇÃO É ELA. slams: the first full-light frame after the 2-frame warm-up (table f14–17)', None),
    ('F15', 44, 'L1 HOLOFOTE APRESENTA · A TURNÊ · 2027 slams (snare)', 44), ('F15', 60, 'MÃE slams (bass drum)', 60),
    ('F15', 84, 'AO VIVO slams (snare)', 84), ('F15', 108, 'DOMINGO · 09.05 slams (snare)', 108),
    ('F15', 150, 'você is drawing on through the cough', 150),
    ('F15', 204, 'BLACKOUT cut (CLAC-off)', 204), ('F15', 222, 'CLAC: the spot snaps back on; PRA MAIOR ATRAÇÃO. cut', 222),
    ('F15', 312, 'end card held under the three claps', 312),
    ('F06A', 6, 'CLAC warm-up begins', 6),
    ('F06A', 8, 'A ATRAÇÃO É ELA. slams: first full-light frame after the warm-up (table f8–11)', None),
    ('F06A', 100, 'end card (cut f96) under the first clap', 100),
    ('F06B', 0, 'ELA', 0), ('F06B', 12, 'APLAUDIU', 12), ('F06B', 24, 'DE PÉ', 24), ('F06B', 36, 'O SEU', 36),
    ('F06B', 48, 'PIOR (+ the cough)', 48), ('F06B', 60, 'SHOW.', 60), ('F06B', 84, 'hard cut to KV-45, CLAC warm-up', 84),
    ('F06C_07-05', 0, 'title on bell 1', 0), ('F06C_07-05', 72, 'CLAC warm-up -> KV-45 unlit', 72),
    ('F06C_08-05', 0, 'title on bell 1', 0), ('F06C_08-05', 72, 'CLAC warm-up -> KV-45 unlit', 72),
    ('F06C_09-05', 0, 'title on bell 1', 0), ('F06C_09-05', 72, 'CLAC warm-up -> KV-45 lit', 72),
]


def verificar_sincronia():
    """Each keyed picture/type event against the onset measured in the final mix: error = event frame - onset frame."""
    rows = []
    for film, fr, what, key in SINCRONIA:
        if key is None:
            rows.append(dict(film=film, frame=fr, what=what, keyed_to=None, ok=None))
            continue
        js = json.load(open(os.path.join(C.SOM, SOM[film] + '_som.json')))
        ks = {k['quadro']: k['onset_medido_s'] * 24 for k in js.get('quadros_chave', [])}
        ons = [o['t_s'] * 24 for o in js['onsets_medidos']]
        onset_f = ks.get(key, min(ons, key=lambda q: abs(q - key)))
        rows.append(dict(film=film, frame=fr, what=what, keyed_to=key, onset_frame=round(onset_f, 3),
                         error_frames=round(fr - onset_f, 3), ok=abs(fr - onset_f) <= 1.0))
    return rows


def escrever_edl():
    os.makedirs(C.PROD, exist_ok=True)
    p = os.path.join(C.PROD, 'EDIT_DECISION_LIST.csv')
    with open(p, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['film', 'shot', 'source', 'timeline_in', 'timeline_out', 'frames', 'mode', 'notes'])
        for film in DUR:
            for shot, a, b, src, mode, notes in FOTOS[film]():
                w.writerow([NOME[film], shot, src, a, b, b - a + 1, mode, notes])
    return p


if __name__ == '__main__':
    print(escrever_edl())
    for r in verificar_sincronia():
        print(r)
