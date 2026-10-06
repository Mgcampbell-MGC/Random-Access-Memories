"""HOLOFOTE · peças finais: o tipo, posto por código, sobre os renders limpos (plataforma §E.1–§E.2, §D.10).

    /home/user/venvs/web/bin/python _build/shots/pecas_finais.py [KV01 KV45 C C03C07 PORTAO LIVRO]

KV01   KV-01 9:16 · 4:5 · 1:1 · 16:9: a camada de tipo de _build/kv/kv.html (tipo_kv.job) sobre KV-01_<fmt>_limpo.png
KV45   KV-45 aceso/apagado × (SUA VEZ. · A ATRAÇÃO É ELA. · sem título) sobre os planos do diretor
C      C01 C02 C04 C05 (1:1 e 9:16) C06 C08 C10: tipo_c.html (motor da marca) sobre os renders limpos
C03C07 as miniaturas da vela em C03 e C07 (recorte do KV-45_aceso do diretor, sem alegação de fidelidade §D.7.5)
PORTAO o portão de legibilidade da chama (§D.6) no KV-01 9:16 final
LIVRO  os renders nas caixas RENDER das pranchas do livro da marca (01_MARCA/placeholders.json)
Nenhuma placa de IA (decisão da dona, 6 out 2026). Nenhum pixel gerado; nenhuma edição por IA depois da composição.
"""
import json, os, sys, subprocess
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..'))
KIT = os.path.abspath(os.path.join(B, '..'))
sys.path.insert(0, os.path.join(B, 'brand'))
sys.path.insert(0, os.path.join(B, 'kv'))
from render import renderizar  # noqa: E402
import tipo_kv  # noqa: E402

RENDERS = os.path.join(KIT, '02_PRODUTO', 'renders')
LAN = os.path.join(KIT, '03_LANCAMENTO')
CACHE = os.path.join(HERE, 'cache', 'tipo')
HTML = os.path.join(HERE, 'tipo_c.html')
os.makedirs(CACHE, exist_ok=True)


def compor(plate, camada, out):
    p = Image.open(plate).convert('RGBA')
    c = Image.open(camada).convert('RGBA')
    assert p.size == c.size, (plate, p.size, c.size)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.alpha_composite(p, c).convert('RGB').save(out)
    print('  ', os.path.relpath(out, KIT))
    return out


def qa(nome, r):
    ruins = [q for q in r.get('qa', []) if abs(q.get('erro', 0) or 0) > 0.5]
    if ruins or r.get('console'):
        print('  QA', nome, ruins, r.get('console'))


# ------------------------------------------------------------------------------------------------ KV-01 / KV-45
def kv01():
    jobs = [tipo_kv.job(f, os.path.join(CACHE, 'KV-01_%s_tipo.png' % f)) for f in ('9x16', '4x5', '1x1', '16x9')]
    res = renderizar(jobs, verbose=False)
    for f, j, r in zip(('9x16', '4x5', '1x1', '16x9'), jobs, res):
        qa('KV-01 ' + f, r)
        compor(os.path.join(RENDERS, 'KV-01_%s_limpo.png' % f), j['saida'], os.path.join(LAN, 'KV', 'KV-01_%s.png' % f))


KV45_TITULOS = (('SUA VEZ.', 'SUA-VEZ'), ('A ATRAÇÃO É ELA.', 'A-ATRACAO-E-ELA'), (None, 'sem-titulo'))


def kv45():
    jobs = [tipo_kv.job('kv45', os.path.join(CACHE, 'KV-45_tipo_%s.png' % tag), dict(headline=hl)) for hl, tag in KV45_TITULOS]
    res = renderizar(jobs, verbose=False)
    for (hl, tag), j, r in zip(KV45_TITULOS, jobs, res):
        qa('KV-45 ' + tag, r)
        for estado in ('aceso', 'apagado'):
            compor(os.path.join(RENDERS, 'KV-45_%s.png' % estado), j['saida'],
                   os.path.join(LAN, 'KV', 'KV-45_%s_%s.png' % (estado, tag)))


# ------------------------------------------------------------------------------------------------ série C
def X(t, cap, cor='papel', **kw):            # o Locutor (Expanded One)
    return dict(t=t, f='X', cap=cap, cor=cor, lsEm=kw.pop('lsEm', -0.01), **kw)


def C(t, cap, cor='papel', **kw):            # a Produção (Condensed One)
    return dict(t=t, f='C', cap=cap, cor=cor, lsEm=kw.pop('lsEm', 0.0), **kw)


SEG = 'nunca deixe a vela acesa sem supervisão.'

# Each piece: its plate, its format and its type blocks (pilha boxes inside the §D.10 safe box, never inside a pool).
PECAS = {}


def def_pecas():
    P = PECAS
    # C02 · 4:5 · the type sits in the dark of the house, above the front row; the stage pool fills the bottom
    P['C02'] = dict(plate='C02_A-PRIMEIRA-FILA_limpo.png', out='C02_A-PRIMEIRA-FILA.png', W=1080, H=1350, blocos=[
        dict(x0=140, x1=940, y0=72, y1=420, itens=[
            dict(tipo='cheia', s=X('A vida toda guardando', 54)),
            dict(tipo='cheia', s=X('lugar na primeira fila.', 54), antes=14),
            dict(tipo='cheia', s=X('Esse ano, o palco é dela.', 54, cor='amarelo'), antes=34),
        ]),
        dict(x0=140, x1=940, y0=1206, y1=1286, itens=[
            dict(tipo='assinatura', cap=28, tinta='papel', lamp='amarelo'),
            dict(tipo='cheia', s=C(SEG, 18, op=0.85), antes=14),
        ]),
    ])
    # C04 · 4:5 · A DISCOGRAFIA / DELA. (ela, a maior palavra) · (até agora.) Produção; the setlist carries the Fã
    P['C04'] = dict(plate='C04_A-DISCOGRAFIA_limpo.png', out='C04_A-DISCOGRAFIA.png', W=1080, H=1350, blocos=[
        dict(x0=140, x1=940, y0=72, y1=400, itens=[
            dict(tipo='cheia', s=X('A DISCOGRAFIA', 60)),
            dict(tipo='cheia', s=X('DELA.', 200), antes=18),
            dict(tipo='dividida', esq=C(SEG, 18, op=0.85), dir=C('(até agora.)', 30), antes=22),
        ]),
        dict(x0=140, x1=940, y0=1240, y1=1286, itens=[
            dict(tipo='assinatura', cap=28, tinta='papel', lamp='amarelo'),
        ]),
    ])
    # C05 · 1:1 and 9:16 · unlit (the copo is in the foam, lid on): no safety line needed
    P['C05_1x1'] = dict(plate='C05_O-CASE_1x1_limpo.png', out='C05_O-CASE_1x1.png', W=1080, H=1080, blocos=[
        dict(x0=180, x1=900, y0=80, y1=232, itens=[
            dict(tipo='cheia', s=X('Mãe não tem camarim.', 48)),
            dict(tipo='cheia', s=X('Agora tem.', 48, cor='amarelo'), antes=12),
        ]),
        dict(x0=180, x1=900, y0=948, y1=1000, itens=[
            dict(tipo='dividida', esq=C('O CASE · com o nome dela · R$179', 26, lsEm=0.04, tnum=True),
                 dir=dict(t='holofote nela.', f='X', cap=24, cor='papel', lsEm=-0.01)),
        ]),
    ])
    P['C05_9x16'] = dict(plate='C05_O-CASE_9x16_limpo.png', out='C05_O-CASE_9x16.png', W=1080, H=1920, blocos=[
        dict(x0=140, x1=940, y0=278, y1=500, itens=[
            dict(tipo='cheia', s=X('Mãe não tem', 80)),
            dict(tipo='cheia', s=X('camarim.', 80), antes=14),
            dict(tipo='cheia', s=X('Agora tem.', 80, cor='amarelo'), antes=14),
        ]),
        dict(x0=140, x1=940, y0=1400, y1=1500, itens=[
            dict(tipo='cheia', s=C('O CASE · com o nome dela · R$179', 34, lsEm=0.04, tnum=True)),
            dict(tipo='assinatura', cap=30, tinta='papel', lamp='amarelo', antes=24),
        ]),
    ])
    # C06 · 4:5 · blackout: the flame is the only light; type in the dark above and below
    P['C06'] = dict(plate='C06_O-MENOR-HOLOFOTE_limpo.png', out='C06_O-MENOR-HOLOFOTE.png', W=1080, H=1350, blocos=[
        dict(x0=140, x1=940, y0=72, y1=400, itens=[
            dict(tipo='cheia', s=X('O MENOR', 120)),
            dict(tipo='cheia', s=X('HOLOFOTE', 120), antes=14),
            dict(tipo='cheia', s=X('DO BRASIL.', 120), antes=14),
        ]),
        dict(x0=140, x1=940, y0=1160, y1=1286, itens=[
            dict(tipo='cheia', s=X('Pra maior atração.', 52, cor='amarelo')),
            dict(tipo='assinatura', cap=26, tinta='papel', lamp='amarelo', antes=24),
            dict(tipo='cheia', s=C(SEG, 18, op=0.85), antes=12),
        ]),
    ])
    # C08 · 4:5 · unlit
    P['C08'] = dict(plate='C08_NOVA-TEMPORADA_limpo.png', out='C08_NOVA-TEMPORADA.png', W=1080, H=1350, blocos=[
        dict(x0=140, x1=940, y0=72, y1=380, itens=[
            dict(tipo='cheia', s=X('O copo fica.', 90)),
            dict(tipo='cheia', s=X('A turnê continua.', 90, cor='amarelo'), antes=16),
        ]),
        dict(x0=140, x1=940, y0=1220, y1=1286, itens=[
            dict(tipo='dividida', esq=C('refil 200 g · R$79', 30, lsEm=0.02, tnum=True),
                 dir=dict(t='holofote nela.', f='X', cap=26, cor='papel', lsEm=-0.01)),
        ]),
    ])
    # C10 · 4:5 · O MURO, preto on plaster; unlit
    P['C10'] = dict(plate='C10_SALVA-COMO_limpo.png', out='C10_SALVA-COMO.png', W=1080, H=1350, blocos=[
        dict(x0=140, x1=940, y0=72, y1=560, itens=[
            dict(tipo='cheia', s=X('comenta como ela', 60, cor='preto')),
            dict(tipo='cheia', s=X('tá salva no seu celular.', 60, cor='preto'), antes=16),
            dict(tipo='cheia', s=X('a gente bota no cartaz.', 60, cor='preto'), antes=16),
        ]),
        dict(x0=140, x1=940, y0=1240, y1=1286, itens=[
            dict(tipo='assinatura', cap=28, tinta='preto', lamp='amarelo'),
        ]),
    ])


def serie_c(quais=None):
    def_pecas()
    ks = [k for k in PECAS if not quais or k in quais]
    jobs = []
    for k in ks:
        p = PECAS[k]
        jobs.append(dict(html=HTML, saida=os.path.join(CACHE, k + '_tipo.png'), w=p['W'], h=p['H'], transparente=True,
                         dados=dict(W=p['W'], H=p['H'], blocos=p['blocos'])))
    res = renderizar(jobs, verbose=False)
    for k, j, r in zip(ks, jobs, res):
        qa(k, r)
        p = PECAS[k]
        plate = os.path.join(RENDERS, p['plate'])
        if os.path.exists(plate):
            compor(plate, j['saida'], os.path.join(LAN, 'C', p['out']))
        json.dump(r.get('info'), open(os.path.join(CACHE, k + '_tipo.json'), 'w'), ensure_ascii=False, indent=1)
    # C01: the headline IS the poster on the wall (§E.2: "set as one more poster on the wall"); no overlay
    c01 = os.path.join(RENDERS, 'C01_O-MURO_limpo.png')
    if os.path.exists(c01) and (not quais or 'C01' in quais):
        out = os.path.join(LAN, 'C', 'C01_O-MURO.png')
        Image.open(c01).convert('RGB').save(out)
        print('  ', os.path.relpath(out, KIT))


# ------------------------------------------------------------------------------------------------ C03 / C07
def c03c07():
    kv = os.path.join(RENDERS, 'KV-45_aceso.png')
    im = Image.open(kv).convert('RGB')
    W, H_ = im.size
    # C03: a Ø360 porthole on the lit candle (flame to label), square crop on the glass
    c03 = os.path.join(CACHE, 'C03_vela.png')
    im.crop((0, 470, 1080, 1550)).save(c03)
    # C07: a 4:5 KV thumbnail (the whole lit candle on its X)
    c07 = os.path.join(CACHE, 'C07_kv.png')
    y0 = 380
    im.crop((0, y0, 1080, y0 + 1350)).save(c07)
    subprocess.run(['/home/user/venvs/web/bin/python', os.path.join(B, 'brand', 'lancamento.py'), 'C', '--vela-c03', c03,
                    '--vela-c07', c07], check=True)


# ------------------------------------------------------------------------------------------------ §D.6 flame gate
def portao():
    import cv2
    lit = cv2.imread(os.path.join(RENDERS, 'KV-01_9x16_limpo.png'))
    unl = cv2.imread(os.path.join(RENDERS, 'KV-01_9x16_apagado_portao.png'))
    a = cv2.resize(lit, (108, 192), interpolation=cv2.INTER_AREA).astype(np.float64)
    b = cv2.resize(unl, (108, 192), interpolation=cv2.INTER_AREA).astype(np.float64)
    d = a - b
    lum = 0.2126 * d[..., 2] + 0.7152 * d[..., 1] + 0.0722 * d[..., 0]
    core = (lum > 40) & (d[..., 2] > d[..., 0])
    n = int(core.sum())
    ys, xs = np.where(core)
    rep = dict(teste='§D.6 flame-legibility gate, KV-01 9:16 FINAL (campanha.py) at 108 × 192',
               metodo='INTER_AREA downscale of the delivered lit plate and of an unlit render of the same camera; '
                      'flame isolated as lit − unlit; warm-core pixel = luminance difference > 40/255 with R > B. '
                      'The same metric on the director\'s 6 Oct gate frames (single 16×12 / double 14×18) gives 3 / 12 '
                      '(recorded 3 / 10): same verdicts.',
               warm_core_px=n, barra=9, passa=bool(n >= 9),
               caixa=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if n else None)
    os.makedirs(os.path.join(KIT, '06_PRODUCAO', 'fidelidade'), exist_ok=True)
    json.dump(rep, open(os.path.join(KIT, '06_PRODUCAO', 'fidelidade', 'KV-01_9x16_portao-chama.json'), 'w'),
              ensure_ascii=False, indent=2)
    big = np.clip(np.repeat(np.repeat(np.dstack([lum] * 3), 4, 0), 4, 1) * 2, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(CACHE, 'portao_diff_x4.png'), big)
    print('PORTAO', json.dumps(rep, ensure_ascii=False))
    return rep


# ------------------------------------------------------------------------------------------------ brand book
LIVRO_RENDERS = {
    'LIVRO-02_A-IDEIA.png': os.path.join(LAN, 'KV', 'KV-01_9x16.png'),
    'LIVRO-12_AS-DUAS-LUZES.png::O-MURO': os.path.join(RENDERS, 'C01_O-MURO_limpo.png'),
    'LIVRO-12_AS-DUAS-LUZES.png::O-PALCO': os.path.join(RENDERS, 'KV-01_1x1_limpo.png'),
    'LIVRO-12_AS-DUAS-LUZES.png::LOJA': os.path.join(LAN, 'L', 'L01_FRENTE.png'),
    'LIVRO-16_SUA-VEZ.png': os.path.join(RENDERS, 'KV-45_aceso.png'),
}
LIVRO_FOCO = {'O-MURO': (0.5, 0.55), 'O-PALCO': (0.5, 0.62), 'LOJA': (0.5, 0.5)}


def cover(im, w, h, foco=(0.5, 0.5)):
    k = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x = int(round((im.width - w) * foco[0]))
    y = int(round((im.height - h) * foco[1]))
    return im.crop((x, y, x + w, y + h))


def livro():
    ph = json.load(open(os.path.join(KIT, '01_MARCA', 'placeholders.json')))
    feito = []
    for chave, (x, y, w, h) in ph.items():
        src = LIVRO_RENDERS.get(chave)
        if not src or not os.path.exists(src):
            print('  livro: sem render para', chave)
            continue
        nome = chave.split('::')[0]
        board = os.path.join(KIT, '01_MARCA', 'livro', nome)
        b = Image.open(board).convert('RGB')
        foco = LIVRO_FOCO.get(chave.split('::')[-1], (0.5, 0.5))
        b.paste(cover(Image.open(src).convert('RGB'), w, h, foco), (x, y))
        b.save(board)
        feito.append(chave)
        print('  livro', chave, '<-', os.path.relpath(src, KIT))
    return feito


if __name__ == '__main__':
    a = sys.argv[1:] or ['KV01', 'KV45', 'C', 'C03C07', 'PORTAO']
    if 'KV01' in a:
        kv01()
    if 'KV45' in a:
        kv45()
    if 'C' in a or any(x in ('C01', 'C02', 'C04', 'C05_1x1', 'C05_9x16', 'C06', 'C08', 'C10') for x in a):
        serie_c([x for x in a if x in ('C01', 'C02', 'C04', 'C05_1x1', 'C05_9x16', 'C06', 'C08', 'C10')] or None)
    if 'C03C07' in a:
        c03c07()
    if 'PORTAO' in a:
        portao()
    if 'LIVRO' in a:
        livro()
