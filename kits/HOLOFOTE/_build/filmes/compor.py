"""HOLOFOTE · the films: composes every frame from the plates, the 3D frames, the flame crops and the type layers,
writes PNG frames, checks the label on every frame where it is visible, and encodes each film twice (with the sound
team's mix and silent) with the studio encoder (tools/codificar.py, BT.709 converted and tagged, 24 fps).

    /home/user/venvs/web/bin/python _build/filmes/compor.py [F15 F06A F06B F06C_07-05 F06C_08-05 F06C_09-05]
        [--so-quadros] [--sem-video] [--manter]

Inputs (made first): _render/ (f15_3d.py through the render lock), 02_PRODUTO/renders/KV-45_aceso|apagado_16bit.png
and their AOVs (the director's), 04_FILMES/som/filmes/*_som.wav (the sound team's).
Outputs: 04_FILMES/<FILM>_som.mp4 and <FILM>_mudo.mp4 · 06_PRODUCAO/fidelidade/<FILM>.json (+ FILM_PLAN.json,
EDIT_DECISION_LIST.csv via plano.py) · contact sheets in _quadros/<FILM>/ (deleted with the frames unless --manter).
"""
import os, sys, json, time, hashlib, subprocess, shutil
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'brand'))
import comum as C          # noqa: E402
import plano as P          # noqa: E402
import ritmo as R          # noqa: E402
import lambe               # noqa: E402
from render import renderizar   # noqa: E402

PAGINA = os.path.join(HERE, 'tipo_filme.html')
BOX = (430, 450, 650, 670)            # = f15_3d.crop_box()
PENA = 20


# ================================================================================================ type layers
class Tipo:
    """Renders type layers (tipo_filme.html) once, cached by their JSON."""
    def __init__(self):
        os.makedirs(os.path.join(C.CACHE, 'tipo'), exist_ok=True)
        self.mem = {}

    def chave(self, dados):
        return hashlib.sha1(json.dumps(dados, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]

    def caminho(self, dados):
        return os.path.join(C.CACHE, 'tipo', self.chave(dados) + '.png')

    def preparar(self, lista):
        jobs, vistos = [], set()
        for d in lista:
            p = self.caminho(d)
            if os.path.exists(p) and os.path.exists(p[:-4] + '.json') or p in vistos:
                continue
            vistos.add(p)
            jobs.append(dict(html=PAGINA, saida=p, w=C.W, h=C.H, dados=d, transparente='fundo' not in d))
        if jobs:
            t = time.time()
            res = renderizar(jobs, verbose=False)
            for j, r in zip(jobs, res):
                if r['console']:
                    print('  console', r['console'])
                ruim = [q for q in r['qa'] if abs(q.get('erro', 0)) > 0.5]
                if ruim:
                    print('  QA medida > 0,5 px', ruim)
                json.dump(dict(info=r['info'], qa=r['qa']), open(j['saida'][:-4] + '.json', 'w'), ensure_ascii=False)
            print('  tipo: %d camadas em %.1f s' % (len(jobs), time.time() - t))

    def camada(self, dados):
        p = self.caminho(dados)
        if p not in self.mem:
            self.mem[p] = C.ler_rgba(p)
            if len(self.mem) > 160:
                self.mem.pop(next(iter(self.mem)))
        return self.mem[p]

    def info(self, dados):
        return json.load(open(self.caminho(dados)[:-4] + '.json'))


def geometria(tipo, film):
    """First layout pass: the final ink boxes, for fly-out distances and draw-on split points."""
    els = []
    if film == 'F15':
        els = [{'k': 'kv01'}, P.L('A ATRAÇÃO É ELA.', 'X', 391, id='atr', fill='tamanho', lsEm=-0.01, cor='papel'),
               P.L('abertura:', 'S', 832, id='ab_only', x=18, cor='papel', al='left', ax=140)]
    elif film == 'F06A':
        els = [P.L('abertura: você', 'S', 470, id='ab', x=18, cor='papel', al='right', ax=940),
               P.L('abertura:', 'S', 470, id='ab_only', x=18, cor='papel', al='left', ax=140)]
    elif film.startswith('F06C'):
        v = P.F06C[film.split('_')[1]]
        els = [P.L(v['titulo'], 'C', 800, id='titulo', fill='tamanho', lsEm=0.02, cor='papel')]
    else:
        return {}
    d = {'camada': els}
    tipo.preparar([d])
    g = tipo.info(d)['info']['geom']
    if film == 'F15':
        g['L4D_ab'] = min(1.0, (g['ab_only']['x1'] - g['ab_only']['x0'] + 4) / (g['L4D']['x1'] - g['L4D']['x0']))
    if film == 'F06A':
        g['ab470'] = min(1.0, (g['ab_only']['x1'] - g['ab_only']['x0'] + 4) / (g['ab']['x1'] - g['ab']['x0']))
    return g


# ================================================================================================ pictures
class Fontes:
    def __init__(self):
        self.c = {}

    def get(self, k, fn):
        if k not in self.c:
            self.c[k] = fn()
        return self.c[k]

    def plate(self, nome):
        paths = {'camA': os.path.join(C.RENDER, 'F15_camA_16bit.png'),
                 'L': os.path.join(C.RENDERS, 'KV-45_aceso_16bit.png'),
                 'U': os.path.join(C.RENDERS, 'KV-45_apagado_16bit.png'),
                 'B': os.path.join(C.RENDER, 'F15_blecaute_16bit.png')}
        return self.get(nome, lambda: C.ler(paths[nome]))

    def cena(self, nome):
        return self.get(nome + '_cena', lambda: C.para_cena(self.plate(nome)))

    def crop(self, kind, n):
        p = os.path.join(C.RENDER, 'chama_' + kind, 'c%04d.png' % n)
        return self.get(p, lambda: C.ler(p))

    def mask(self):
        x0, y0, x1, y1 = BOX
        return self.get('mask', lambda: C.mascara_caixa(y1 - y0, x1 - x0, PENA))


def colar(base, crop, m):
    x0, y0, x1, y1 = BOX
    out = base.copy()
    out[y0:y1, x0:x1] = base[y0:y1, x0:x1] * (1 - m) + crop * m
    return out


def kv_aceso_cena(F, i):
    """KV-45 lit with the flame in flicker state i (scene-linear): the flame's light on everything is the blackout
    plate's light (the flame is the only source there), scaled by the flicker; the flame itself is the 3D crop."""
    s, _ = R.flicker(i)
    sc = F.cena('L') + (s - 1.0) * F.cena('B')
    return colar(sc, C.para_cena(F.crop('palco', i % 24)), F.mask())


def blecaute_cena(F, f):
    """F15 blackout: the flame the only light. Everything it lights scales with it (point light, floor bounce, label
    wash were all rendered proportional to the flame's gain); the flame itself is the 3D crop of that frame."""
    s, _ = R.flame_state(f)
    sc = F.cena('B') * s
    return colar(sc, C.para_cena(F.crop('blecaute', f)), F.mask())


def blecaute_idx_cena(F, i):
    """The blackout scene at flicker index i (rendered as F15 frames 216 + i)."""
    f = 216 + (i % 24)
    s, _ = R.flicker(i)
    return colar(F.cena('B') * s, C.para_cena(F.crop('blecaute', f)), F.mask())


def aquec(sc_luz, k, kelvin, sc_fixo=None):
    """CLAC filament warm-up: the spot's light at gain k and colour `kelvin` (balanced 3.300 K, as the spot is
    recorded), over whatever does not come from the spot (the flame)."""
    t = C.tinta_quente(kelvin)
    out = sc_luz * (k * t)[None, None, :]
    return out + sc_fixo if sc_fixo is not None else out


def picture(film, f, F):
    """-> (RGB float display image, manifest dict for the label check)."""
    man = dict(aov=None, push=1.0, check='none')
    if film == 'F15':
        if f <= 11 or 204 <= f <= 209:
            return np.zeros((C.H, C.W, 3), np.float32), man
        if f in (12, 13):
            k, kel = P.AQUEC[f - 12]
            return C.para_tela(aquec(F.cena('camA'), k, kel)), man
        if f <= 159:
            return F.plate('camA'), man
        if f <= 203:
            full = f >= 176
            p = os.path.join(C.RENDER, 'grua', 'f%04d_%d.png' % (f, 100 if full else 50))
            im = C.ler(p)
            if not full:
                im = cv2.resize(im, (C.W, C.H), interpolation=cv2.INTER_LANCZOS4)
            else:
                man.update(aov=os.path.join(C.RENDER, 'grua_aov', '%04d.exr' % f), check='label')
            return im, man
        if f <= 221:
            man.update(aov=os.path.join(C.RENDER, 'blecaute_aov', '0001.exr'), check='albedo' if f >= 210 else 'none')
            return C.para_tela(blecaute_cena(F, f)), man
        i = (f - 216) % 24
        s = P.push(f, P.PUSH_F15)
        if f in (222, 223):
            k, kel = P.AQUEC[f - 222]
            bi = blecaute_idx_cena(F, i)
            sc = aquec(kv_aceso_cena(F, i) - bi, k, kel, bi)
        else:
            sc = kv_aceso_cena(F, i)
        img = C.empurrar(C.para_tela(sc), s, P.PUSH_CENTRO)
        man.update(aov=os.path.join(C.AOV_KV, 'KV-45_aceso', '0001.exr'), push=s, check='label')
        return img, man
    if film in ('F06A', 'F06B') or film == 'F06C_09-05':
        lit_from = {'F06A': 6, 'F06B': 84, 'F06C_09-05': 72}[film]
        if f < lit_from:
            return np.zeros((C.H, C.W, 3), np.float32), man
        i = f % 24
        s = P.push(f, P.PUSH_F06A) if film == 'F06A' else 1.0
        if f in (lit_from, lit_from + 1):
            k, kel = P.AQUEC[f - lit_from]
            bi = blecaute_idx_cena(F, i)
            sc = aquec(kv_aceso_cena(F, i) - bi, k, kel, bi)
        else:
            sc = kv_aceso_cena(F, i)
        img = C.empurrar(C.para_tela(sc), s, P.PUSH_CENTRO)
        man.update(aov=os.path.join(C.AOV_KV, 'KV-45_aceso', '0001.exr'), push=s, check='label')
        return img, man
    if film.startswith('F06C'):
        if f < 72:
            return np.zeros((C.H, C.W, 3), np.float32), man
        man.update(aov=os.path.join(C.AOV_KV, 'KV-45_apagado', '0001.exr'), check='label')
        if f in (72, 73):
            k, kel = P.AQUEC[f - 72]
            return C.para_tela(aquec(F.cena('U'), k, kel)), man
        return F.plate('U'), man
    raise ValueError(film)


# ================================================================================================ frames
def tipo_do_quadro(film, f, geom):
    return P.TIPO[film](f, geom)


def compor_filme(film, args):
    t0 = time.time()
    tipo = Tipo()
    F = Fontes()
    geom = geometria(tipo, film)
    n = P.DUR[film]
    # 1. every type layer this film needs, in one browser session
    plano_tipo = {f: tipo_do_quadro(film, f, geom) for f in range(n)}
    tipo.preparar([d for f in plano_tipo for d, _, _ in plano_tipo[f]])
    od = os.path.join(C.QUADROS, film)
    if os.path.isdir(od):
        shutil.rmtree(od)
    os.makedirs(od)
    manifest = {}
    lambe_mem = {}
    for f in range(n):
        camadas = plano_tipo[f]
        if film == 'F06B' and f <= 83:
            # the poster: flat type on amarelo -> O LAMBE (the C03 seed and settings: static paper, moving type)
            d = camadas[0][0]
            k = tipo.chave(d)
            if k not in lambe_mem:
                flat = (tipo.camada(d)[..., :3] * 255 + 0.5).astype(np.uint8)
                ass, _, _, _ = lambe.aplicar(flat, 'amarelo', 303, borda=False, rasgo=0, rugas=0.8, registro=1.8)
                lambe_mem = {k: ass[..., :3].astype(np.float32)}
            img = lambe_mem[k]
            man = dict(aov=None, push=1.0, check='none')
        else:
            img, man = picture(film, f, F)
            for d, dy, blur in camadas:
                img = C.sobre(img, tipo.camada(d), 0.0, dy, blur)
        C.salvar(os.path.join(od, 'q%04d.png' % f), img)
        manifest[f] = man
        if f % 24 == 0:
            print('  %s f%03d  %.1f s' % (film, f, time.time() - t0), flush=True)
    json.dump(manifest, open(os.path.join(od, 'manifest.json'), 'w'))
    print('%s: %d quadros em %.1f s' % (film, n, time.time() - t0))
    return od, manifest, geom


def folha_contato(film, od, extra=()):
    n = P.DUR[film]
    qs = sorted(set(list(range(0, n, 6)) + list(extra)))
    th = [cv2.resize(cv2.imread(os.path.join(od, 'q%04d.png' % q)), (180, 320), interpolation=cv2.INTER_AREA) for q in qs]
    cols = 12
    rows = (len(th) + cols - 1) // cols
    sheet = np.full((rows * 344, cols * 186, 3), 40, np.uint8)
    for i, (q, t) in enumerate(zip(qs, th)):
        r, c = divmod(i, cols)
        sheet[r * 344:r * 344 + 320, c * 186:c * 186 + 180] = t
        cv2.putText(sheet, 'f%d' % q, (c * 186 + 4, r * 344 + 337), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (230, 230, 230), 1)
    p = os.path.join(od, film + '_contato.jpg')
    cv2.imwrite(p, sheet, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return p


def codificar(film, od):
    nome = P.NOME[film]
    wav = os.path.join(C.SOM, P.SOM[film] + '_som.wav')
    enc = os.path.join(C.B, 'tools', 'codificar.py')
    out = {}
    for tag, extra in (('mudo', []), ('som', ['--trilha', wav])):
        mp4 = os.path.join(C.FILMES, '%s_%s.mp4' % (nome, tag))
        subprocess.run([C.WEB, enc, od, mp4, '--fps', '24'] + extra, check=True)
        out[tag] = mp4
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    films = [x for x in a if not x.startswith('--')] or list(P.DUR)
    for film in films:
        od, man, geom = compor_filme(film, a)
        print(folha_contato(film, od))
        if '--sem-video' not in a:
            print(codificar(film, od))
