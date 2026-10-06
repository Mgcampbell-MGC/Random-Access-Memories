"""O LANÇAMENTO · peças gráficas: B01–B08 (BOLETIM), C03 · C07 · C09, D01 · D02, STK ×8 (plataforma §E.2).

Uma linha gera tudo, do zero (arte chapada no Chromium → O LAMBE / papel em Python → 03_LANCAMENTO/):
    /home/user/venvs/web/bin/python _build/brand/lancamento.py              (tudo)
    /home/user/venvs/web/bin/python _build/brand/lancamento.py B C           (só as famílias B e C)
Encaixar a vela renderizada nas miniaturas de C03/C07 (o render entra DEPOIS de O LAMBE, intocado: o passe de papel
reentinta e desregistra tudo o que toca, e o rótulo tem de continuar sendo o pixel do mestre):
    ... lancamento.py C --vela-c03 render_vela.png --vela-c07 render_kv.png
Saídas e espaços reservados: 03_LANCAMENTO/{B,C,D,STK}/ + 03_LANCAMENTO/C/placeholders.json.
"""
import json, math, os, sys, time
import numpy as np
import cv2
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import lambe, marca, ruido  # noqa: E402
from render import renderizar  # noqa: E402

KIT = os.path.dirname(os.path.dirname(AQUI))
L = os.path.join(KIT, '03_LANCAMENTO')
CACHE = os.path.join(AQUI, 'cache', 'lancamento')
PECA = os.path.join(AQUI, 'peca.html')

# §E.2: BOLETIM DA TURNÊ — data, cor da faixa, a linha do dia (exata) e as quebras escolhidas (comprimentos equilibrados)
BOLETIM = [
    ('B01', '02.05', 'amarelo', 'bom dia. faltam 7 dias pro show. pode encaminhar.', ['bom dia. faltam 7 dias', 'pro show. pode encaminhar.']),
    ('B02', '03.05', 'rosa', 'bom dia. a atração já confirmou presença. e você?', ['bom dia. a atração já', 'confirmou presença. e você?']),
    ('B03', '04.05', 'laranja', 'bom dia. leva um casaquinho. e um ingresso.', ['bom dia. leva um', 'casaquinho. e um ingresso.']),
    ('B04', '05.05', 'violeta', 'bom dia. ingressos com os filhos. (os filhos sabem quem são.)', ['bom dia. ingressos com os filhos.', '(os filhos sabem quem são.)']),
    ('B05', '06.05', 'amarelo', 'bom dia. faltam 3 dias. vou contar até três.', ['bom dia. faltam 3 dias.', 'vou contar até três.']),
    ('B06', '07.05', 'rosa', 'bom dia. primeiro sinal.', ['bom dia. primeiro sinal.']),
    ('B07', '08.05', 'laranja', 'bom dia. segundo sinal. visualizou? então.', ['bom dia. segundo sinal.', 'visualizou? então.']),
    ('B08', '09.05', 'amarelo', 'bom dia. terceiro sinal. o show é hoje.', ['bom dia. terceiro sinal.', 'o show é hoje.']),
]
TURNE_C09 = [['ESTREIA · 21.11.1999 · 06:40', 'QUEM FEZ O SHOW FOI ELA'], ['PREZINHO, DIA DAS MÃES', 'PRIMEIRA FILA'],
             ['FESTA JUNINA', 'O BIGODE FOI ELA'], ['PRONTO-SOCORRO, 3H', 'SEM INGRESSO. ENTROU.'],
             ['FORMATURA', 'DE PÉ (COM O DEDO NA LENTE)'], ['09.05.2027', 'A ATRAÇÃO É ELA']]
STK = [('STK-01', 'ACESSO-TOTAL'), ('STK-02', 'MAIS-UM'), ('STK-03', 'ABERTURA-VOCE'), ('STK-04', 'NAO-PRECISAVA'),
       ('STK-05', 'PRECISAVA'), ('STK-06', 'EQUIPE-TECNICA'), ('STK-07', 'TERCEIRO-SINAL'), ('STK-08', 'ELA-FICA-AQUI')]


def checar(nome, r):
    ruins = [q for q in r['qa'] if abs(q.get('erro', 0)) > 0.5]
    if ruins or r['console']:
        print('  QA', nome, ruins, r['console'])


def lamber(chapado, saida, papel, semente, **kw):
    img = lambe.ler(chapado)
    assado, _, _, _ = lambe.aplicar(img, papel, semente, borda=False, rasgo=0, **kw)
    lambe.salvar(assado[..., :3], saida)


def compor_miniatura(chapado, caixa, render_png, circulo):
    """Encaixa um render na caixa reservada (cobre, centralizado), recortado em círculo se for o caso."""
    base = Image.open(chapado).convert('RGB')
    x, y, w, h = caixa
    im = Image.open(render_png).convert('RGB')
    k = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    m = Image.new('L', (w * 4, h * 4), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(m)
    (d.ellipse if circulo else d.rectangle)((0, 0, w * 4 - 1, h * 4 - 1), fill=255)
    base.paste(im, (x, y), m.resize((w, h), Image.LANCZOS))
    base.save(chapado)


# ------------------------------------------------------------------ B
def fazer_B():
    os.makedirs(os.path.join(L, 'B'), exist_ok=True)
    jobs = []
    for bid, data, cor, linha, quebras in BOLETIM:
        assert ' '.join(quebras) == linha, bid       # a quebra nunca muda a frase
        for fmt, (w, h) in (('1x1', (1080, 1080)), ('9x16', (1080, 1920))):
            jobs.append(dict(html=PECA, saida=os.path.join(CACHE, f'{bid}_{fmt}_chapado.png'), w=w, h=h,
                             dados=dict(receita='boletim', formato=fmt, cor=cor, data=data, linhas=quebras,
                                        sinal={'B06': 1, 'B07': 2, 'B08': 3}.get(bid)),
                             meta=(bid, data, cor, fmt)))
    res = renderizar(jobs, verbose=False)
    for j, r in zip(jobs, res):
        bid, data, cor, fmt = j['meta']
        checar(bid + fmt, r)
        semente = 600 + int(bid[1:]) * 10 + (1 if fmt == '9x16' else 0)
        out = os.path.join(L, 'B', f"{bid}_BOLETIM_{data.replace('.', '')}_{fmt}.png")
        lamber(j['saida'], out, cor, semente, rugas=0.75, registro=1.6)
        print('  ', os.path.relpath(out, KIT))


# ------------------------------------------------------------------ C
def fazer_C(vela_c03=None, vela_c07=None):
    os.makedirs(os.path.join(L, 'C'), exist_ok=True)
    pecas = [('C03', 'C03_O-PIOR-SHOW', dict(receita='C03'), 'amarelo', 303, vela_c03),
             ('C07', 'C07_PIX', dict(receita='C07'), 'amarelo', 307, vela_c07),
             ('C09', 'C09_O-CARTAZ-DELA_DONA-CIDA', dict(receita='C09', cor='rosa', headliner='DONA CIDA', turne=TURNE_C09), 'rosa', 309, None)]
    jobs = [dict(html=PECA, saida=os.path.join(CACHE, f'{p[0]}_chapado.png'), w=1080, h=1920, dados=p[2]) for p in pecas]
    res = renderizar(jobs, verbose=False)
    ph = {}
    for p, j, r in zip(pecas, jobs, res):
        checar(p[0], r)
        nome = p[1] + '.png'
        out = os.path.join(L, 'C', nome)
        lamber(j['saida'], out, p[3], p[4], rugas=0.8, registro=1.8)
        # the render goes in AFTER O LAMBE: the lambe pass re-inks and misregisters everything it touches, and the
        # pack's label must stay the master's pixels (platform §0 rule 1; garbled thumbnails caught in review, 6 Oct)
        for q in r['placeholders']:
            ph[nome] = [round(q['x']), round(q['y']), round(q['w']), round(q['h'])]
            if p[5]:
                compor_miniatura(out, ph[nome], p[5], q['tipo'] == 'circulo')
        print('  ', os.path.relpath(out, KIT))
    json.dump(ph, open(os.path.join(L, 'C', 'placeholders.json'), 'w'), ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ D
def papel_cartao(rgba, cor, semente, rugas=0.22):
    """Textura de cartão (gramatura alta): grão, registro de 1,5 px, quase nenhuma ruga. Mantém o alfa."""
    a = rgba[..., 3:4].astype(np.float32) / 255
    fundo = np.array(lambe.rgb(cor), np.float32) * 255
    rgb = rgba[..., :3].astype(np.float32) * a + fundo * (1 - a)
    assado, _, _, _ = lambe.aplicar(rgb.astype(np.uint8), cor, semente, borda=False, rasgo=0, rugas=rugas, registro=1.2, tinta=0.5)
    return np.dstack([assado[..., :3], a[..., 0]])


def fazer_D():
    os.makedirs(os.path.join(L, 'D'), exist_ok=True)
    jobs = [dict(html=PECA, saida=os.path.join(CACHE, 'D01_chapado.png'), w=1080, h=1920, dados=dict(receita='D01')),
            dict(html=PECA, saida=os.path.join(CACHE, 'D02_ingresso.png'), w=1080, h=1350, dados=dict(receita='ingresso'),
                 transparente=True)]
    res = renderizar(jobs, verbose=False)
    for j, r in zip(jobs, res):
        checar(os.path.basename(j['saida']), r)
    # D01 — cartão plastificado: só grão de papel, sem rugas nem registro solto
    img = lambe.ler(jobs[0]['saida'])
    assado, _, _, _ = lambe.aplicar(img, 'preto', 401, borda=False, rasgo=0, rugas=0.0, registro=0.0, grao=0.8, tinta=0.0)
    lambe.salvar(assado[..., :3], os.path.join(L, 'D', 'D01_A-CARTEIRINHA_9x16.png'))
    ph = {'D01_A-CARTEIRINHA_9x16.png': [round(v) for v in (lambda q: (q['x'], q['y'], q['w'], q['h']))(res[0]['placeholders'][0])]}
    json.dump(ph, open(os.path.join(L, 'D', 'placeholders.json'), 'w'), ensure_ascii=False, indent=1)
    print('   03_LANCAMENTO/D/D01_A-CARTEIRINHA_9x16.png')
    # D02 — o ingresso: papel cartão + picote; versão inteira (antes da entrega) e rasgada (depois)
    g = res[1]['info']
    rgba = np.asarray(Image.open(jobs[1]['saida']).convert('RGBA'))
    tk = papel_cartao(rgba, g['cor'], 402)
    H, W = tk.shape[:2]
    preto = np.array(lambe.rgb('preto'), np.float32)
    fundo = np.empty((H, W, 3), np.float32)
    fundo[:] = preto
    fundo = fundo * (1 + 0.02 * lambe.grao_papel(H, W, ruido.rng(9))[..., None])     # palco: preto com grão, não chapado

    def sobre(base, cam):
        return base * (1 - cam[..., 3:4]) + cam[..., :3] * cam[..., 3:4]

    lambe.salvar(sobre(fundo, tk), os.path.join(L, 'D', 'D02_O-INGRESSO_inteiro.png'))
    # rasgado: o picote abre, o canhoto desce e gira (papel de verdade, fibra no rasgo)
    r = ruido.rng(4021)
    yp = g['yPicote']
    mant, franja = lambe.rasgo_linha(H, W, r, (g['x1'] + 40, yp), (g['x0'] - 40, yp), amp=0.0035)
    corpo = tk.copy()
    corpo[..., 3] *= mant
    canhoto = tk.copy()
    canhoto[..., 3] *= (1 - mant)
    branco = np.array([0.985, 0.975, 0.955], np.float32)
    for peca, fr in ((corpo, franja), (canhoto, None)):
        f = (franja if fr is not None else np.clip(cv2.dilate(franja, np.ones((3, 3), np.uint8)), 0, 1))[..., None] * 0.85
        peca[..., :3] = peca[..., :3] * (1 - f) + branco * f
    cx, cy = (g['x0'] + g['x1']) / 2, (yp + g['y1']) / 2
    M = cv2.getRotationMatrix2D((cx, cy), -3.2, 1.0)
    M[0, 2] += 14
    M[1, 2] += 54
    canhoto2 = cv2.warpAffine(canhoto, M, (W, H), flags=cv2.INTER_CUBIC, borderValue=(0, 0, 0, 0))
    lambe.salvar(sobre(sobre(fundo, corpo), canhoto2), os.path.join(L, 'D', 'D02_O-INGRESSO_rasgado.png'))
    print('   03_LANCAMENTO/D/D02_O-INGRESSO_inteiro.png · _rasgado.png')


# ------------------------------------------------------------------ STK
def borda_adesivo(rgba, esp=13, margem=16, S=512):
    """Borda branca de adesivo (papel-cartaz) em volta da arte: dilatação circular do alfa; depois cabe em S − 2·margem."""
    a = rgba[..., 3].astype(np.float32) / 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * esp + 1, 2 * esp + 1))
    pad = esp + 4
    a2 = np.pad(a, pad)
    rgb2 = np.pad(rgba[..., :3].astype(np.float32) / 255, ((pad, pad), (pad, pad), (0, 0)))
    dil = cv2.dilate((a2 > 0.5).astype(np.uint8), k).astype(np.float32)
    dil = cv2.GaussianBlur(dil, (0, 0), 0.8)
    branco = np.array(lambe.rgb('papel'), np.float32)
    rgb = branco * (1 - a2[..., None]) + rgb2 * a2[..., None]
    alfa = np.maximum(dil, a2)
    out = np.dstack([rgb, alfa])
    ys, xs = np.where(alfa > 0.01)
    out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = out.shape[:2]
    k2 = min(1.0, (S - 2 * margem) / max(h, w))
    im = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), 'RGBA')
    if k2 < 1:
        im = im.resize((round(w * k2), round(h * k2)), Image.LANCZOS)
    tela = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    tela.alpha_composite(im, ((S - im.width) // 2, (S - im.height) // 2))
    return tela


def fazer_STK():
    os.makedirs(os.path.join(L, 'STK'), exist_ok=True)
    tira = os.path.join(CACHE, 'tira512.png')
    img, meta, _ = marca.gerar(512, 31, uma=True, angulo=-7.0)
    marca.salvar_png(img, tira)
    jobs = [dict(html=PECA, saida=os.path.join(CACHE, f'{sid}_arte.png'), w=512, h=512, transparente=True,
                 dados=dict(receita='stk', v=v, tira='file://' + tira, angulo=-7.0, semente=int(sid[-1]) * 13))
            for sid, v in STK]
    res = renderizar(jobs, verbose=False)
    folha = Image.new('RGBA', (4 * 512, 2 * 512), (54, 52, 58, 255))
    for (sid, v), j, r in zip(STK, jobs, res):
        checar(sid, r)
        st = borda_adesivo(np.asarray(Image.open(j['saida']).convert('RGBA')))
        out = os.path.join(L, 'STK', f'{sid}_{v}.webp')
        st.save(out, 'WEBP', quality=88, method=6)
        kb = os.path.getsize(out) / 1024
        if kb > 100:
            st.save(out, 'WEBP', quality=72, method=6)
            kb = os.path.getsize(out) / 1024
        i = int(sid[-1]) - 1
        folha.alpha_composite(st, ((i % 4) * 512, (i // 4) * 512))
        print(f'   03_LANCAMENTO/STK/{sid}_{v}.webp  {kb:.0f} KB')
    folha.convert('RGB').save(os.path.join(L, 'STK', 'STK_folha_contato.jpg'), quality=90)


def main():
    a = sys.argv[1:]
    def opt(k):
        return a[a.index(k) + 1] if k in a else None
    fam = [x for x in a if x in ('B', 'C', 'D', 'STK')] or ['B', 'C', 'D', 'STK']
    os.makedirs(CACHE, exist_ok=True)
    t = time.time()
    if 'STK' in fam:
        print('STK'); fazer_STK()
    if 'D' in fam:
        print('D'); fazer_D()
    if 'C' in fam:
        print('C'); fazer_C(opt('--vela-c03'), opt('--vela-c07'))
    if 'B' in fam:
        print('B'); fazer_B()
    print(f'ok {time.time() - t:.0f}s')


if __name__ == '__main__':
    main()
