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
PENA = 20


def caixa():
    """The flame crop box, written by f15_3d.py next to the crops (projected from the flame at the KV-45 camera)."""
    for k in ('palco', 'blecaute'):
        p = os.path.join(C.RENDER, 'chama_' + k, 'box.json')
        if os.path.exists(p):
            return tuple(json.load(open(p))['box'])
    raise FileNotFoundError('no flame crop box: render the crops first (f15_3d.py chama)')


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
    """Every plate, at the film's 1x (1080 x 1920) or at the KV-45 check scale 2x (2160 x 3840)."""
    def __init__(self):
        self.c = {}

    def get(self, k, fn):
        if k not in self.c:
            self.c[k] = fn()
        return self.c[k]

    def caminho(self, nome, q):
        if nome in ('L', 'U'):
            base = os.path.join(C.RENDERS, 'KV-45_%s' % ('aceso' if nome == 'L' else 'apagado'))
            p2 = base + '_2x_16bit.png'
            return p2 if (q == 2 and os.path.exists(p2)) else base + '_16bit.png'
        return {'camA': os.path.join(C.RENDER, 'F15_camA_16bit.png'),
                'B': os.path.join(C.RENDER, 'F15_blecaute_16bit.png')}[nome]

    def plate(self, nome, q=1):
        def fazer():
            im = C.ler(self.caminho(nome, q))
            w, h = C.W * q, C.H * q
            if im.shape[:2] == (h, w):
                return im
            interp = cv2.INTER_AREA if im.shape[0] > h else cv2.INTER_CUBIC
            return np.clip(cv2.resize(im, (w, h), interpolation=interp), 0, 1)
        return self.get((nome, q), fazer)

    def cena(self, nome, q=1):
        return self.get((nome, q, 'cena'), lambda: C.para_cena(self.plate(nome, q)))

    def crop(self, kind, n, q=1):
        p = os.path.join(C.RENDER, 'chama_' + kind, 'c%04d.png' % n)
        def fazer():
            c = C.ler(p)
            if q != 1:
                c = np.clip(cv2.resize(c, (c.shape[1] * q, c.shape[0] * q), interpolation=cv2.INTER_CUBIC), 0, 1)
            return C.para_cena(c)
        return self.get((p, q), fazer)

    def mask(self, kind='palco', q=1):
        """Where the crop replaces the plate: only where the FLAME changes. The union, over every crop of this kind,
        of |crop - (the 2D light model at that flicker state)| > 10 levels (plus the flame's own pixels), closed,
        dilated 14 px, feathered (sigma 6) and held to zero at the crop's own border. The plate keeps its own (2x
        supersampled) rim and wick everywhere else, so no seam can show on the rim highlights that cross the box."""
        def fazer():
            import glob
            x0, y0, x1, y1 = caixa()
            Ls, Bs = self.cena('L')[y0:y1, x0:x1], self.cena('B')[y0:y1, x0:x1]
            d = np.zeros((y1 - y0, x1 - x0), np.float32)
            for p in sorted(glob.glob(os.path.join(C.RENDER, 'chama_' + kind, 'c*.png'))):
                c = C.ler(p)
                n = int(os.path.basename(p)[1:5])
                # what the 2D model alone would give at this flicker state: the crop replaces only where it differs
                if kind == 'palco':
                    base = C.para_tela(Ls + (R.flicker(n)[0] - 1.0) * Bs)
                else:
                    base = C.para_tela(Bs * R.flame_state(n)[0])
                dd = np.abs(c - base).max(axis=-1)
                if kind == 'blecaute':
                    dd = np.maximum(dd, (c.max(axis=-1) > 0.35) * 1.0)    # the flame itself, at any ignition scale
                d = np.maximum(d, dd)
            m = (d > 10 / 255.0).astype(np.uint8)
            m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
            m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (29, 29)))
            m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 6)
            m = np.minimum(m, C.mascara_caixa(y1 - y0, x1 - x0, 12)[..., 0])
            if q != 1:
                m = cv2.resize(m, (m.shape[1] * q, m.shape[0] * q), interpolation=cv2.INTER_LINEAR)
            return m[..., None]
        return self.get(('mask', kind, q), fazer)


def colar(base, crop, m, q=1):
    x0, y0, x1, y1 = [v * q for v in caixa()]
    out = base.copy()
    out[y0:y1, x0:x1] = base[y0:y1, x0:x1] * (1 - m) + crop * m
    return out


def kv_aceso_cena(F, i, q=1):
    """KV-45 lit with the flame in flicker state i (scene-linear): the flame's light on everything is the blackout
    plate's light (the flame is the only source there), scaled by the flicker; the flame itself is the 3D crop."""
    s, _ = R.flicker(i)
    sc = F.cena('L', q) + (s - 1.0) * F.cena('B', q)
    return colar(sc, F.crop('palco', i % 24, q), F.mask('palco', q), q)


def blecaute_cena(F, f):
    """F15 blackout: the flame the only light. Everything it lights scales with it (point light, floor bounce, label
    wash were all rendered proportional to the flame's gain); the flame itself is the 3D crop of that frame."""
    s, _ = R.flame_state(f)
    return colar(F.cena('B') * s, F.crop('blecaute', f), F.mask('blecaute'))


def blecaute_idx_cena(F, i, q=1):
    """The blackout scene at flicker index i (rendered as F15 frames 216 + i)."""
    s, _ = R.flicker(i)
    return colar(F.cena('B', q) * s, F.crop('blecaute', 216 + (i % 24), q), F.mask('blecaute', q), q)


def aquec(sc_luz, k, kelvin, sc_fixo=None):
    """CLAC filament warm-up: the spot's light at gain k and colour `kelvin` (balanced 3.300 K, as the spot is
    recorded), over whatever does not come from the spot (the flame)."""
    t = C.tinta_quente(kelvin)
    out = sc_luz * (k * t)[None, None, :]
    return out + sc_fixo if sc_fixo is not None else out


class Verificador:
    """The label check, run INLINE on the 2x picture of every KV-45-derived frame (the director's rule, 6 Oct: the
    official verification is at 2x; the delivered frame is that 2x picture area-averaged to 1080). Identical label
    regions (holds) reuse the previous result; every frame gets a row."""
    def __init__(self):
        import fidelidade_filmes as FF
        self.FF = FF
        m = cv2.imread(C.MASTER, cv2.IMREAD_UNCHANGED)
        self.alpha = m[..., 3].astype(np.float32) / 255.0
        self.aov = {}
        self.ultimo = (None, None)

    def __call__(self, img2, aov_path, s, centro2, cor):
        FF = self.FF
        if aov_path not in self.aov:
            self.aov = {aov_path: FF.ler_aov(aov_path, nativo=True)}
        aov = self.aov[aov_path]
        M = None if abs(s - 1) < 1e-9 else C.empurrar_M(s, centro2)
        bgr = (np.clip(img2, 0, 1) * 255 + 0.5).astype(np.uint8)[..., ::-1].copy()
        a = FF.transformar(aov, M)
        ys, xs = np.nonzero(a['mask'] > 0.02)
        chave = hashlib.sha1(bgr[ys.min():ys.max() + 1, xs.min():xs.max() + 1].tobytes()).hexdigest() + str(cor)
        if chave == self.ultimo[0]:
            return dict(self.ultimo[1], reused_identical_label_region=True)
        r = FF.checar(self.alpha, a, bgr, coat=FF.COAT if cor else None)
        r['scale'] = '2x (%dx%d), then area-averaged to 1080 for delivery' % (bgr.shape[1], bgr.shape[0])
        r['method'] = ('label AOV 2x, 2D push x%.4f applied to the AOV' % s) if M is not None else 'label AOV 2x'
        self.ultimo = (chave, r)
        return r


VERIF = None


def aquec_aceso(F, i, q, k, kel):
    bi = blecaute_idx_cena(F, i, q)
    return aquec(kv_aceso_cena(F, i, q) - bi, k, kel, bi)


def kv45_frame(F, tela_fn, s, lit, cor):
    """Build a KV-45-derived picture at 2x (if the director's 2x plate exists), check its label there, deliver the
    area-average at 1x. tela_fn(q) -> display picture at scale q."""
    global VERIF
    q = 2 if os.path.exists(F.caminho('L' if lit else 'U', 2)) and F.caminho('L' if lit else 'U', 2).endswith('_2x_16bit.png') else 1
    cx, cy = C.centro_push()
    img = C.empurrar(tela_fn(q), s, (cx * q, cy * q))
    nome = 'KV-45_aceso' if lit else 'KV-45_apagado'
    man = dict(push=s, centro=[cx, cy], check='label')
    if q == 2:
        if VERIF is None:
            VERIF = Verificador()
        man['fid'] = VERIF(img, os.path.join(C.AOV_KV, nome + '_2x', '0001.exr'), s, (cx * 2, cy * 2), cor)
        img = cv2.resize(img, (C.W, C.H), interpolation=cv2.INTER_AREA)
    man['aov'] = os.path.join(C.AOV_KV, nome, '0001.exr')
    return img, man


def picture(film, f, F):
    """-> (RGB float display image at 1x, manifest dict for the label check)."""
    man = dict(aov=None, push=1.0, check='none')
    if film == 'F15':
        if f <= 11 or 204 <= f <= 209:
            return np.zeros((C.H, C.W, 3), np.float32), man
        if f in (12, 13):
            k, kel = P.AQUEC[f - 12]
            return C.para_tela(aquec(F.cena('camA'), k, kel)), man
        if f <= 161:
            # the crane starts at f160 with a smootherstep ease: f160–161 move < 0,05 px, so they ARE the cam A still
            return F.plate('camA'), man
        if f <= 203:
            full = f >= 176
            p = os.path.join(C.RENDER, 'grua', 'f%04d_%d.png' % (f, 100 if full else 50))
            im = C.ler(p)
            if not full:
                im = np.clip(cv2.resize(im, (C.W, C.H), interpolation=cv2.INTER_LANCZOS4), 0, 1)
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
            fn = lambda q: C.para_tela(aquec_aceso(F, i, q, k, kel))
        else:
            fn = lambda q: C.para_tela(kv_aceso_cena(F, i, q))
        return kv45_frame(F, fn, s, True, f not in (222, 223))
    if film in ('F06A', 'F06B') or film == 'F06C_09-05':
        lit_from = {'F06A': 6, 'F06B': 84, 'F06C_09-05': 72}[film]
        if f < lit_from:
            return np.zeros((C.H, C.W, 3), np.float32), man
        i = f % 24
        s = P.push(f, P.PUSH_F06A) if film == 'F06A' else 1.0
        warm = f in (lit_from, lit_from + 1)
        if warm:
            k, kel = P.AQUEC[f - lit_from]
            fn = lambda q: C.para_tela(aquec_aceso(F, i, q, k, kel))
        else:
            fn = lambda q: C.para_tela(kv_aceso_cena(F, i, q))
        return kv45_frame(F, fn, s, True, not warm)
    if film.startswith('F06C'):
        if f < 72:
            return np.zeros((C.H, C.W, 3), np.float32), man
        warm = f in (72, 73)
        if warm:
            k, kel = P.AQUEC[f - 72]
            fn = lambda q: C.para_tela(aquec(F.cena('U', q), k, kel))
        else:
            fn = lambda q: F.plate('U', q)
        return kv45_frame(F, fn, 1.0, False, not warm)
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


# frames every contact sheet adds to its every-6th grid: slams, warm-ups, cuts, the crane, the flame
EXTRA = {
    'F15': [12, 13, 14, 15, 16, 17, 44, 45, 46, 60, 61, 62, 84, 85, 86, 108, 109, 110, 133, 139, 145, 151, 155, 157,
            159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201,
            203, 205, 210, 211, 212, 213, 214, 215, 217, 219, 221, 222, 223, 225, 288, 300, 359],
    'F06A': [5, 6, 7, 8, 9, 10, 11, 25, 29, 33, 37, 41, 45, 96],
    'F06B': [1, 2, 3, 13, 14, 15, 49, 50, 51, 61, 62, 63, 67, 71, 75, 79, 81, 83, 84, 85, 86],
    'F06C_07-05': [8, 16, 25, 29, 33, 37, 72, 73, 74], 'F06C_08-05': [8, 16, 25, 29, 33, 37, 72, 73, 74],
    'F06C_09-05': [8, 16, 25, 29, 33, 37, 72, 73, 74],
}


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
        print(folha_contato(film, od, EXTRA.get(film, ())))
        if '--sem-video' not in a:
            print(codificar(film, od))
