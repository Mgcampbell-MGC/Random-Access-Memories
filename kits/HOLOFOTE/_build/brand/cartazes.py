"""O MURO · os 12 cartazes lambe-lambe da parede (plataforma §E.2 C01, §D.4 O CARTAZ + O LAMBE).

Uma linha de comando gera tudo, do zero:
    /home/user/venvs/web/bin/python _build/brand/cartazes.py            (todos)
    /home/user/venvs/web/bin/python _build/brand/cartazes.py 01 07      (só alguns)

O que sai em 01_MARCA/cartazes/ (2000 × 3000 px, sRGB):
    CARTAZ-NN_<nome>.png            RGBA 'assado': O LAMBE completo (rugas sombreadas, grão, registro, borda rasgada).
                                    Para 2D, pranchas, e para o 3D se não for usar deslocamento.
    3d/CARTAZ-NN_<nome>_albedo.png  RGBA sem o sombreado das rugas (o 3D faz a luz).
    3d/CARTAZ-NN_<nome>_altura.png  mapa de altura 16 bits das rugas da colagem (normalizado 0–1) para deslocamento.
    cartazes.json                   o que é cada cartaz, semente, cores, onde estão os rasgos.
    CARTAZES_contato.jpg            folha de contato (prévia).
Os cartazes chapados (antes do LAMBE) ficam em _build/brand/cache/ (não versionar).
"""
import json, math, os, sys, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import lambe, ruido  # noqa: E402

KIT = os.path.dirname(os.path.dirname(AQUI))
SAIDA = os.path.join(KIT, '01_MARCA', 'cartazes')
CACHE = os.path.join(AQUI, 'cache', 'cartazes')
W, H = 2000, 3000

# A lista da turnê do verso do copo (§C.3), com a linha ESTREIA de varejo
TURNE = dict(titulo='ELA ESTEVE EM TODAS.', linhas=[
    ['ESTREIA · O DIA EM QUE VOCÊ NASCEU', 'QUEM FEZ O SHOW FOI ELA'],
    ['PREZINHO, DIA DAS MÃES', 'PRIMEIRA FILA'], ['FESTA JUNINA', 'O BIGODE FOI ELA'],
    ['FEIRA DE CIÊNCIAS', 'O VULCÃO TAMBÉM'], ['PRONTO-SOCORRO, 3H', 'SEM INGRESSO. ENTROU.'],
    ['FORMATURA', 'DE PÉ (COM O DEDO NA LENTE)'], ['PRIMEIRO APÊ', '4 VIAGENS DE CARRO'],
    ['09.05.2027', 'A ATRAÇÃO É ELA']])


def lineup(cor, show=None):
    """O CARTAZ completo: lineup + a lista da turnê + assinatura."""
    d = dict(W=W, H=H, cor=cor, modo='cartaz', turne=TURNE)
    if show:
        d['show'] = show
    return d


def teaser(cor):
    """O CARTAZ curto: lineup + a data gigante. MÃE continua a maior palavra (cap 199 u contra 09.05 a ~151 u)."""
    return dict(W=W, H=H, cor=cor, modo='itens', itens=[
        dict(tipo='dividida', esq=dict(t='HOLOFOTE APRESENTA', f='C', cap=30, lsEm=0.08),
             dir=dict(t='A TURNÊ · 2027', f='C', cap=30, lsEm=0.08, tnum=True)),
        dict(tipo='headliner', nome='MÃE', capRef=199, antes=34, flex=1),
        dict(tipo='cheia', s=dict(t='AO VIVO', f='V', wght=700, cap=112), modo='wdth', antes=22),
        dict(tipo='regua', antes=44, flex=2),
        dict(tipo='cheia', s=dict(t='09.05', f='X', cap=150, lsEm=-0.01, tnum=True), modo='tamanho', antes=44, flex=0.6),
        dict(tipo='dividida', antes=34, esq=dict(t='DOMINGO', f='C', cap=46, lsEm=0.02),
             dir=dict(t='abertura: você', f='S', x=18)),
        dict(tipo='espaco', flex=1.4),
        dict(tipo='assinatura', cap=30, antes=44),
    ])


def c01():
    """C01: 'MÃE AO VIVO. 09.05. INGRESSOS COM VOCÊ.' como mais um cartaz da parede, tipo de madeira empilhado."""
    return dict(W=W, H=H, cor='papel', modo='itens', itens=[
        dict(tipo='dividida', esq=dict(t='HOLOFOTE APRESENTA', f='C', cap=30, lsEm=0.08),
             dir=dict(t='A TURNÊ · 2027', f='C', cap=30, lsEm=0.08, tnum=True)),
        dict(tipo='headliner', nome='MÃE', capRef=199, antes=34, flex=1),
        dict(tipo='cheia', s=dict(t='AO VIVO.', f='V', wght=700, cap=176), modo='wdth', antes=34, flex=1),
        dict(tipo='cheia', s=dict(t='09.05.', f='V', wght=700, cap=176, tnum=True), modo='wdth', antes=34, flex=1),
        dict(tipo='regua', antes=40, flex=1),
        dict(tipo='cheia', s=dict(t='INGRESSOS COM VOCÊ.', f='V', wght=700, cap=60), modo='wdth', antes=40),
        dict(tipo='espaco', flex=1),
        dict(tipo='assinatura', cap=30, antes=44),
    ])


# id, nome, dados do cartaz chapado, parâmetros do LAMBE, composição
CARTAZES = [
    dict(id='01', nome='MAE-AO-VIVO_amarelo', papel='amarelo', dados=lineup('amarelo'), semente=101, rasgo=0.30),
    dict(id='02', nome='MAE-AO-VIVO_rosa', papel='rosa', dados=lineup('rosa', 'AO VIVO'), semente=102, rasgo=0.35),
    dict(id='03', nome='MAE-AO-VIVO_laranja', papel='laranja', dados=lineup('laranja', 'AO VIVO'), semente=103, rasgo=0.25),
    dict(id='04', nome='MAE-AO-VIVO_violeta', papel='violeta', dados=lineup('violeta', 'AO VIVO'), semente=104, rasgo=0.40),
    dict(id='05', nome='MAE-AO-VIVO-0905_amarelo', papel='amarelo', dados=teaser('amarelo'), semente=105, rasgo=0.30),
    dict(id='06', nome='MAE-AO-VIVO-0905_rosa', papel='rosa', dados=teaser('rosa'), semente=106, rasgo=0.35),
    # dois dos quatro rasgados até as camadas antigas
    dict(id='07', nome='MAE-AO-VIVO_rosa_RASGADO-sobre-MAIS-UM', papel='rosa', dados=lineup('rosa', 'AO VIVO'),
         semente=107, rasgo=0.45, antigo=dict(papel='laranja', dados=lineup('laranja', 'MAIS UM!'), semente=207, idade=0.55),
         furo='faixa'),
    dict(id='08', nome='MAE-AO-VIVO_laranja_RASGADO-sobre-CAMARIM', papel='laranja', dados=lineup('laranja', 'AO VIVO'),
         semente=108, rasgo=0.45, antigo=dict(papel='rosa', dados=lineup('rosa', 'CAMARIM'), semente=208, idade=0.6),
         furo='metade-de-baixo'),
    # as camadas antigas, soltas (para o 3D montar a parede em camadas)
    dict(id='09', nome='MAE-CAMARIM_rosa_ANTIGO', papel='rosa', dados=lineup('rosa', 'CAMARIM'), semente=209, rasgo=0.6, idade=0.6),
    dict(id='10', nome='MAE-MAIS-UM_laranja_ANTIGO', papel='laranja', dados=lineup('laranja', 'MAIS UM!'), semente=210, rasgo=0.6, idade=0.55),
    dict(id='11', nome='MAE-ACUSTICO_violeta_METADE', papel='violeta', dados=lineup('violeta', 'ACÚSTICO'), semente=211,
         rasgo=0.5, idade=0.65, furo='metade-direita'),
    dict(id='12', nome='C01_MAE-AO-VIVO-INGRESSOS-COM-VOCE_papel', papel='papel', dados=c01(), semente=112, rasgo=0.25),
]


def chapados(lista):
    """Renderiza todos os cartazes chapados (e as camadas antigas) num só Chromium."""
    from render import renderizar
    jobs, chaves = [], []
    for c in lista:
        for k, d in (('', c['dados']), ('_antigo', (c.get('antigo') or {}).get('dados'))):
            if d is None:
                continue
            caminho = os.path.join(CACHE, f"CARTAZ-{c['id']}{k}_chapado.png")
            jobs.append(dict(html=os.path.join(AQUI, 'cartaz.html'), saida=caminho, w=W, h=H, dados=d))
            chaves.append((c['id'], k))
    res = renderizar(jobs)
    info = {}
    for (i, k), r in zip(chaves, res):
        info[i + k] = r['info']
        ruins = [q for q in r['qa'] if abs(q.get('erro', 0)) > 0.5]
        if ruins or r['console']:
            print('  QA', i + k, ruins, r['console'])
    return info


def linha(info, texto):
    for it in info['itens']:
        if it['t'] == texto:
            return it
    raise KeyError(texto)


def fazer(c, info):
    t0 = time.time()
    r = ruido.rng(c['semente'] * 7 + 1)
    img = lambe.ler(os.path.join(CACHE, f"CARTAZ-{c['id']}_chapado.png"))
    meta = dict(id=c['id'], nome=c['nome'], papel=c['papel'], semente=c['semente'], tamanho=[W, H])
    furo = c.get('furo')
    if c.get('antigo'):
        a = c['antigo']
        topo = lambe.aplicar(img, c['papel'], c['semente'], rasgo=c['rasgo'])[:3]
        ant_img = lambe.ler(os.path.join(CACHE, f"CARTAZ-{c['id']}_antigo_chapado.png"))
        antigo = lambe.aplicar(ant_img, a['papel'], a['semente'], idade=a['idade'], borda=False)[:3]
        show = linha(info[c['id']], c['dados'].get('show') or 'AO VIVO')
        ant_show = linha(info[c['id'] + '_antigo'], a['dados']['show'])
        cap = ant_show['top']
        if furo == 'faixa':
            # uma faixa arrancada na altura do nome do show: revela o show antigo inteiro
            cy = ant_show['baseline'] - cap * 0.45
            bur = [(W * 0.52, cy, W * 0.64, cap * 1.32, math.radians(-2.5))]
            assado, albedo, altura = lambe.rasgado(topo, antigo, r, buracos=bur, ilhas=0.0)
            meta['rasgo'] = dict(tipo='faixa', centro=[round(W * 0.52), round(cy)], raios=[round(W * 0.64), round(cap * 1.32)])
        else:
            # a metade de baixo do cartaz de cima saiu: sobra MÃE em cima, o show antigo embaixo
            y = (show['baseline'] - show['top'] + linha(info[c['id']], 'MÃE')['baseline']) / 2 - 8
            cortes = [((W + 60, y + 22), (-60, y - 18))]
            assado, albedo, altura = lambe.rasgado(topo, antigo, r, cortes=cortes, amp=0.017)
            meta['rasgo'] = dict(tipo='corte', linha=[[W + 60, round(y + 34)], [-60, round(y - 22)]])
        meta['camada_antiga'] = dict(papel=a['papel'], show=a['dados']['show'], semente=a['semente'], idade=a['idade'])
    else:
        assado, albedo, altura, _ = lambe.aplicar(img, c['papel'], c['semente'], rasgo=c['rasgo'], idade=c.get('idade', 0))
        if furo == 'metade-direita':
            # sobra meio ACÚSTICO: o lado direito foi arrancado (rasgo quase vertical, cortando a palavra)
            show = linha(info[c['id']], 'ACÚSTICO')
            xm = show['x0'] + (show['x1'] - show['x0']) * 0.56
            p0, p1 = (xm + 120, -60), (xm - 150, H + 60)
            mant, franja = lambe.rasgo_linha(H, W, r, p0, p1, amp=0.03)
            branco = np.array([0.985, 0.975, 0.955], np.float32)
            for arr in (assado, albedo):
                fr = (franja * mant)[..., None] * 0.9
                arr[..., :3] = arr[..., :3] * (1 - fr) + branco * fr
                arr[..., 3] *= mant
            meta['rasgo'] = dict(tipo='metade', linha=[[round(p0[0]), p0[1]], [round(p1[0]), p1[1]]])
        if c.get('idade'):
            meta['idade'] = c['idade']
    meta['rasgo_borda'] = c['rasgo']
    base = f"CARTAZ-{c['id']}_{c['nome']}"
    lambe.salvar(assado, os.path.join(SAIDA, base + '.png'))
    lambe.salvar(albedo, os.path.join(SAIDA, '3d', base + '_albedo.png'))
    lambe.salvar(altura, os.path.join(SAIDA, '3d', base + '_altura.png'))
    meta['arquivos'] = [base + '.png', '3d/' + base + '_albedo.png', '3d/' + base + '_altura.png']
    print(f'  {base}  {time.time() - t0:.1f}s', flush=True)
    return meta


def contato(metas):
    """Folha de contato 4 × 3 sobre cinza-reboco, cada cartaz com sua borda rasgada."""
    th = 600
    tw = th * W // H
    gap = 40
    folha = Image.new('RGB', (4 * tw + 5 * gap, 3 * th + 4 * gap), (176, 172, 164))
    for i, m in enumerate(metas):
        im = Image.open(os.path.join(SAIDA, m['arquivos'][0])).convert('RGBA').resize((tw, th), Image.LANCZOS)
        x, y = gap + (i % 4) * (tw + gap), gap + (i // 4) * (th + gap)
        folha.paste(im, (x, y), im)
    folha.save(os.path.join(SAIDA, 'CARTAZES_contato.jpg'), quality=90)


def main():
    pedidos = [a for a in sys.argv[1:] if not a.startswith('-')]
    lista = [c for c in CARTAZES if not pedidos or c['id'] in pedidos]
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(os.path.join(SAIDA, '3d'), exist_ok=True)
    print('chapados…')
    info = chapados(lista)
    print('O LAMBE…')
    with ProcessPoolExecutor(max_workers=2) as ex:
        metas = list(ex.map(fazer, lista, [info] * len(lista)))
    # junta com o que já existia (rodada parcial)
    js = os.path.join(SAIDA, 'cartazes.json')
    antigos = {m['id']: m for m in json.load(open(js))['cartazes']} if os.path.exists(js) and pedidos else {}
    for m in metas:
        antigos[m['id']] = m
    todos = [antigos[k] for k in sorted(antigos)]
    json.dump(dict(fonte='_build/brand/cartazes.py', tamanho=[W, H],
                   nota='assado = 2D (rugas já sombreadas). 3d/ = albedo RGBA sem sombreado + altura 16 bits normalizada 0–1 (mín–máx da colagem; nas camadas rasgadas o papel antigo fica mais baixo). Deslocamento sugerido: 0,6 mm de amplitude total, midlevel 0,5. Alfa = borda rasgada.',
                   cartazes=todos), open(js, 'w'), ensure_ascii=False, indent=1)
    if len(todos) == len(CARTAZES):
        contato(todos)
    print('ok', len(metas))


if __name__ == '__main__':
    main()
