"""Arquivos de máquina do kit HOLOFOTE, gerados dos arquivos ENTREGUES (nunca escritos à mão).

    /home/user/venvs/web/bin/python _build/pacote/maquina.py

Grava em 06_PRODUCAO/:
  MACHINE_BRIEF.json      marca, regras, produtos (do label_copy.json de cada mestre), peças com arquivo e verificação
  CENAS.csv               uma linha por peça: formato, descrição e texto exatos (do pacote), arquivo, render, rótulo
  AUDIO_CUE_SHEET.csv     todo cue de todo filme e anúncio (dos *_cues.json e *_som.json da equipe de som)
  CORTES_6S.csv           os cortes de 6 s (F06A, F06B, F06C ×3) com quadros e loudness medidos
  TEXTOS_SOCIAL.txt       legenda de post, data e texto alternativo de cada peça orgânica
  STATUS_ENTREGA.txt      o que existe, o que falta, e por quê (do preencher.py)
e na raiz do kit: INVENTARIO_ARQUIVOS.json (todo arquivo entregue, tamanho e SHA-256).
"""
import csv, glob, hashlib, html, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
PROD = os.path.join(KIT, '06_PRODUCAO')
MODELO = os.path.join(HERE, 'HOLOFOTE_PACKET_modelo.html')
sys.path.insert(0, HERE)
import preencher as P  # noqa: E402


def rel(p):
    return os.path.relpath(p, KIT) if p else None


def ids_do_pacote():
    """ID -> {formato, descricao, texto} from the packet's own Portuguese tables (one source of truth)."""
    s = open(MODELO, encoding='utf-8').read()
    out = {}
    for t in re.findall(r'<table.*?</table>', s, re.S):
        hdr = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<th[^>]*>(.*?)</th>', t, re.S)]
        for r in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
            cells = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', c))).strip()
                     for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
            m = re.match(r'^(KV-0\d|C\d\d|B0\d|L0\d|D0\d|S01|STK|P0\d)\b', cells[0]) if cells else None
            if not m:
                continue
            key = m.group(1)
            d = out.setdefault(key, {'nome': cells[0]})
            if hdr[:2] == ['ID', 'Formato'] and len(cells) >= 4:
                d.update(nome=cells[0], formato=cells[1], descricao=cells[2], texto=cells[3], faz=cells[4] if len(cells) > 4 else None)
            elif hdr[:2] == ['ID', 'Cena'] and len(cells) >= 2:
                d.update(nome=cells[0], descricao=cells[1])
            elif hdr[:2] == ['Cartão', 'Data'] and len(cells) >= 4:
                d.update(nome='%s · BOLETIM' % cells[0], data=cells[1], cor=cells[2], texto=cells[3], formato='1:1 + 9:16')
    out.setdefault('KV-01', {}).update(nome='KV-01 · MÃE AO VIVO', formato='9:16 · 4:5 · 1:1 · 16:9',
        descricao='O PALCO: a vela AO VIVO acesa sobre o X de fita, sob um spot duro, com a escalação MÃE AO VIVO em tipo por código.',
        texto='MÃE AO VIVO · DOMINGO · 09.05 · abertura: você · holofote nela.')
    out.setdefault('KV-45', {}).update(nome='KV-45 · quadro de produto', formato='9:16 (aceso e apagado; com e sem título)',
        descricao='A vela a 85 mm, rótulo inteiro legível, acesa e apagada: o quadro de produto dos anúncios e filmes.',
        texto='SUA VEZ. · A ATRAÇÃO É ELA. · holofote nela. · nunca deixe a vela acesa sem supervisão.')
    return out


def arquivo_da_peca(pid):
    pads = {'KV-01': ['03_LANCAMENTO/KV/KV-01_*.png'], 'STK': ['03_LANCAMENTO/STK/STK-0*.webp'],
            'S01': ['04_FILMES/S01_*_som.mp4']}
    pp = pads.get(pid, ['03_LANCAMENTO/*/%s_*.png' % pid, '03_LANCAMENTO/*/%s_*.webp' % pid, '02_PRODUTO/renders/%s_*.png' % pid])
    fs = []
    for p in pp:
        fs += [f for f in sorted(glob.glob(os.path.join(KIT, p))) if '_16bit' not in f and '_alpha' not in f and 'limpo' not in f]
    return fs


def fid_da_peca(pid):
    rs = []
    for f in sorted(glob.glob(os.path.join(P.FIDDIR, '%s*.json' % pid))):
        try:
            r = json.load(open(f))
            r = r[0] if isinstance(r, list) else r
        except Exception:
            continue
        if 'resumo' in r:
            continue
        l = P.linha_fid(r)
        if l:
            rs.append('%s: pior %s · p5 %s · %s' % (os.path.splitext(os.path.basename(f))[0], l['PIOR'], l['P5'], l['RESULTADO']))
        elif r.get('thumbnail_sem_alegacao'):
            rs.append('%s: miniatura, sem alegação' % os.path.splitext(os.path.basename(f))[0])
    return rs


def segundos():
    seg = {}
    log = os.path.join(KIT, '_build', 'shots', 'campanha_log.jsonl')
    if os.path.exists(log):
        for ln in open(log):
            try:
                j = json.loads(ln)
            except Exception:
                continue
            if not j.get('teste'):
                seg[j['nome']] = (j.get('segundos'), j.get('samples'), j.get('res'))
    seg['KV-45_aceso'], seg['KV-45_apagado'] = (389.8, 128, [1080, 1920]), (309.2, 96, [1080, 1920])
    return seg


def cenas(ids):
    seg = segundos()
    linhas = []
    ordem = ['KV-01', 'KV-45'] + ['C%02d' % i for i in range(1, 11)] + ['B%02d' % i for i in range(1, 9)] + \
            ['L%02d' % i for i in range(1, 8)] + ['D01', 'D02', 'STK', 'S01', 'P01', 'P02', 'P03']
    for pid in ordem:
        d = ids.get(pid, {})
        fs = arquivo_da_peca(pid)
        rs = [(n, v) for n, v in seg.items() if n.startswith(pid)]
        linhas.append({
            'id': pid, 'peca': d.get('nome', pid), 'formato': d.get('formato', ''), 'data': d.get('data', ''),
            'descricao': d.get('descricao', ''), 'texto_exato': d.get('texto', ''),
            'origem': {'L': 'local (Blender + tipo por código)', 'G': 'precisa de pessoa gerada'}.get(d.get('faz'), 'local'),
            'arquivos': ' | '.join(rel(f) for f in fs) or 'AUSENTE',
            'render_s': ' | '.join('%s %.0f s (%s amostras)' % (n, v[0], v[1]) for n, v in rs if v[0]) or '',
            'rotulo': ' | '.join(fid_da_peca(pid)) or ('não se aplica' if pid in ('B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08',
                                                                                'D01', 'D02', 'STK', 'S01', 'C07', 'C09') else ''),
        })
    with open(os.path.join(PROD, 'CENAS.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)
    return linhas


def cues():
    rows = []
    for j in sorted(glob.glob(os.path.join(KIT, '04_FILMES', 'som', 'filmes', '*_som.json'))):
        J = json.load(open(j))
        filme = os.path.basename(j).replace('_som.json', '')
        cj = j.replace('_som.json', '_cues.json')
        cs = J.get('cues') or []
        if os.path.exists(cj):
            C = json.load(open(cj))
            cs = C if isinstance(C, list) else (C.get('cues') or cs)
        for c in cs:
            rows.append({'filme': filme, 'quadro': c.get('quadro'), 'inicio_s': c.get('inicio_s'), 'sincronia': c.get('sync'),
                         'som': c.get('label'), 'arquivo': c.get('arquivo'), 'lufs_i_mix': J.get('lufs_i'),
                         'true_peak_mix': J.get('true_peak_dbtp')})
        for q in J.get('quadros_chave', []):
            rows.append({'filme': filme, 'quadro': q.get('quadro'), 'inicio_s': q.get('onset_medido_s'), 'sincronia': 'ataque medido',
                         'som': 'desvio %s quadro · %s' % (q.get('desvio_quadros'), 'OK' if q.get('ok') else 'FORA'),
                         'arquivo': '', 'lufs_i_mix': J.get('lufs_i'), 'true_peak_mix': J.get('true_peak_dbtp')})
    if rows:
        with open(os.path.join(PROD, 'AUDIO_CUE_SHEET.csv'), 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    return rows


def cortes():
    rows = []
    for pd, nome in (('F06A', 'F06A · CLAC'), ('F06B', 'F06B · O PIOR SHOW'), ('F06C*07-05', 'F06C · SINAL 07.05'),
                     ('F06C*08-05', 'F06C · SINAL 08.05'), ('F06C*09-05', 'F06C · SINAL 09.05')):
        som = P.achar('04_FILMES/*%s*_som.mp4' % pd)
        mudo = P.achar('04_FILMES/*%s*_mudo.mp4' % pd)
        if not som:
            rows.append({'corte': nome, 'arquivo_som': 'AUSENTE', 'arquivo_mudo': rel(mudo) or 'AUSENTE'})
            continue
        dur, n = P.sonda(som)
        li, tp = P.loud(som)
        fs = sorted(glob.glob(os.path.join(P.FIDDIR, pd + '.json')))
        R = json.load(open(fs[0])).get('resumo', {}) if fs else {}
        rows.append({'corte': nome, 'arquivo_som': rel(som), 'arquivo_mudo': rel(mudo), 'duracao_s': round(dur, 3),
                     'quadros': n, 'lufs_i': li, 'true_peak_dbfs': tp,
                     'rotulo_pior_bloco': R.get('worst_tile_min'), 'quadros_com_rotulo': R.get('frames_label_visible'),
                     'quadros_reprovados': len(R.get('frames_fail') or []) if R else None})
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    with open(os.path.join(PROD, 'CORTES_6S.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    return rows


# Copy for the organic posts. Rules: the piece's own line leads; one product line; the signature in lower case; no
# testimonial, no memorial phrasing, no claim the label does not make; prices only where the platform sets them.
SOCIAL = [
    ('C01', '19.04 · ato 1 O MURO', 'MÃE AO VIVO. 09.05. INGRESSOS COM VOCÊ.\nA TURNÊ: quatro velas aromáticas, quatro faixas do show dela.\nholofote nela.',
     'Muro de reboco coberto de cartazes lambe-lambe amarelos, rosa, laranja e violeta escritos MÃE AO VIVO · 09.05, dois deles rasgados; num parapeito, quatro velas em copos coloridos, tampadas. Um dos cartazes diz MÃE AO VIVO. 09.05. INGRESSOS COM VOCÊ.'),
    ('C10', '22.04 · ato 1 O MURO', 'comenta como ela tá salva no seu celular. a gente bota no cartaz.\nholofote nela.',
     'Três velas em copos coloridos num parapeito, com nomes no rótulo: MÃE com coração, DONA CIDA e MAINHA.'),
    ('C09', '26.04 · ato 1 O MURO', 'faz o cartaz dela.\nholofote.exemplo/cartaz\nholofote nela.',
     'Cartaz lambe-lambe rosa escrito DONA CIDA AO VIVO, com seis momentos da turnê dela, e a chamada faz o cartaz dela.'),
    ('C02', '01.05 · ato 2 O PALCO', 'A vida toda guardando lugar na primeira fila.\nEsse ano, o palco é dela.\nholofote nela.\nNunca deixe a vela acesa sem supervisão.',
     'Vela acesa no palco de um auditório de escola vazio, vista de trás; ao fundo, oito cadeiras brancas e uma bolsa guardando a do meio.'),
    ('C03', '02.05 · ato 2 O PALCO', 'Ela aplaudiu de pé o seu pior show.\nSua vez.\nholofote nela.\nNunca deixe a vela acesa sem supervisão.',
     'Cartaz amarelo com letras pretas grandes: ELA APLAUDIU DE PÉ O SEU PIOR SHOW., com a anotação à mão (girassol, 2007); embaixo, um círculo com a vela acesa e os textos Sua vez., holofote nela. e nunca deixe a vela acesa sem supervisão.'),
    ('C04', '03.05 · ato 2 O PALCO', 'A discografia dela. (até agora.)\n1. camarim · 2. ao vivo · 3. mais um! · 4. acústico\nholofote nela.\nNunca deixe a vela acesa sem supervisão.',
     'Quatro velas acesas em fila num palco preto, cada uma sob seu próprio foco de luz branca; uma setlist colada no chão à frente.'),
    ('C05', '04.05 · ato 2 O PALCO', 'Mãe não tem camarim. Agora tem.\nO CASE · com o nome dela · R$179\nholofote nela.',
     'Case de turnê preto aberto, visto de cima, com espelho na tampa, a vela tampada na espuma, a setlist e uma pulseira de tecido preta com letras amarelas.'),
    ('C06', '05.05 · ato 2 O PALCO', 'O menor holofote do Brasil.\nPra maior atração.\nholofote nela.\nNunca deixe a vela acesa sem supervisão.',
     'Uma vela acesa no escuro total; só a chama ilumina o rótulo amarelo.'),
    ('C07', '06.05 · ato 2 O PALCO (só neste dia)', 'Pix não tem cheiro.\nMÃE AO VIVO · DOMINGO · 09.05\nholofote nela.\nNunca deixe a vela acesa sem supervisão.',
     'Cartaz lambe-lambe amarelo escrito PIX NÃO TEM CHEIRO. em letras pretas grandes; embaixo, a vela acesa em miniatura, MÃE AO VIVO, DOMINGO · 09.05, holofote nela. e nunca deixe a vela acesa sem supervisão.'),
    ('S01', '08.05 · ato 2 O PALCO (sugerida)', 'domingo tô aí.\nholofote nela.',
     'Vídeo: num papel creme, alguém digita “mãe, você foi a melhor plateia d…”, para, apaga letra por letra e digita “domingo tô aí.”; no fim, holofote nela.'),
    ('C08', '10.05 · ato 3 O BIS', 'O copo fica. A turnê continua.\nrefil 200 g · R$79\nholofote nela.',
     'Copo de vela limpo e vazio sobre um X de fita no palco, com a cápsula de refil preta ao lado e a tampa-selo levantada.'),
]


def social(ids):
    out = ['HOLOFOTE · TEXTOS DOS POSTS ORGÂNICOS · Dia das Mães 2027 (marca fictícia, caso demonstrativo)',
           'Regra: a linha da peça abre; uma linha de produto; a assinatura em minúsculas; em todo post com vela acesa, a linha de segurança (§D.8.6). Sem depoimento, sem luto, sem promessa que o rótulo não faz.',
           'Os BOLETINS (B01–B08) saem às 06:03, de 02 a 09.05, com a frase do dia como legenda e nada mais.',
           'Sem rótulo de IA nos anúncios (decisão da fundadora, 6 out 2026).',
           'Datas: os atos são os da plataforma (§E). Fixadas por ela: C07 (06.05), BOLETIM (02–09.05, 06:03), F06C (07, 08 e 09.05) e C08 (10.05). As outras datas são sugestão dentro do ato.', '']
    for pid, quando, legenda, alt in SOCIAL:
        fs = arquivo_da_peca(pid)
        out += ['%s · %s' % (ids.get(pid, {}).get('nome', pid), quando),
                'ARQUIVO: ' + (' | '.join(rel(f) for f in fs) or 'AUSENTE'),
                'LEGENDA:', legenda, 'TEXTO ALTERNATIVO: ' + alt, '']
    for i in range(1, 9):
        d = ids.get('B%02d' % i, {})
        fs = arquivo_da_peca('B%02d' % i)
        out += ['B%02d · BOLETIM · %s 06:03 · %s' % (i, d.get('data', ''), d.get('cor', '')),
                'ARQUIVO: ' + (' | '.join(rel(f) for f in fs) or 'AUSENTE'), 'LEGENDA:', d.get('texto', ''),
                'TEXTO ALTERNATIVO: Cartão lambe-lambe %s com MÃE AO VIVO · DOMINGO · 09.05, o horário 06:03 no canto e a frase: %s'
                % (d.get('cor', ''), d.get('texto', '')), '']
    open(os.path.join(PROD, 'TEXTOS_SOCIAL.txt'), 'w', encoding='utf-8').write('\n'.join(out))


def produtos():
    out = []
    for f in sorted(glob.glob(os.path.join(KIT, '02_PRODUTO', 'rotulos', '*_label_copy.json'))):
        j = json.load(open(f))
        out.append({k: j.get(k) for k in ('sku', 'faixa', 'headliner', 'show_name', 'descriptor', 'opening_act',
                                          'net_weight', 'front_lines', 'back_lines', 'warnings', 'master_hash')}
                   | {'mestre': rel(f.replace('_label_copy.json', '_ROTULO_wrap.png')), 'copy_json': rel(f)})
    return out


def brief(ids, cen):
    tok = {}
    for m in re.finditer(r'--(\w+):\s*(#[0-9A-Fa-f]{6});\s*/\*\s*(.*?)\s*\*/', open(os.path.join(KIT, '_build', 'tokens.css')).read()):
        tok[m.group(1)] = {'hex': m.group(2), 'uso': m.group(3)}
    filmes = []
    for f in sorted(glob.glob(os.path.join(KIT, '04_FILMES', '*_som.mp4'))):
        dur, n = P.sonda(f)
        filmes.append({'filme': os.path.basename(f).replace('_som.mp4', ''), 'com_som': rel(f),
                       'sem_som': rel(f.replace('_som.mp4', '_mudo.mp4')), 'duracao_s': round(dur, 3), 'quadros': n, 'fps': 24})
    ads = json.load(open(os.path.join(KIT, '05_ANUNCIO', 'CREATOR_ADS.json')))
    B = {
        'kit': 'HOLOFOTE · Dia das Mães 2027', 'natureza': 'caso demonstrativo do SOL Estúdio · marca, produto e pessoas fictícios',
        'leia_primeiro': ['00_LEIA_PRIMEIRO.txt', '06_PRODUCAO/COMECE_AQUI_PROXIMO_LLM.txt', '07_KIT_COMPLETO/HOLOFOTE_PACKET.html'],
        'plataforma': {'nome': 'MÃE AO VIVO', 'colecao': 'A TURNÊ', 'assinatura': 'holofote nela.',
                       'ideia': 'Ela foi a plateia de todos os seus shows. No Dia das Mães, a atração é ela.',
                       'fonte': '00_estrategia/CREATIVE_PLATFORM.md'},
        'cores': tok,
        'vozes': {'Locutor': 'Special Gothic Expanded One / SG 700, caixa-alta, tracking −10 a 0; toda linha enche a medida',
                  'Produção': 'Special Gothic Condensed One, caixa-alta +80 a +120 ou minúsculas a 0; algarismos tabulares',
                  'Fã': 'Shantell Sans 500, INFM 60, só minúsculas, até 6 palavras, uma por layout'},
        'regras_de_producao': [
            'A embalagem é exata por construção: o rótulo é o arquivo-mestre mapeado em UV no 3D, nunca desenhado por um gerador.',
            'Todo still com rótulo visível passa por _build/tools/fidelidade_uv.py: pior bloco ≥ 0,80, 5º percentil ≥ 0,95 (filmes ≥ 0,93), erro plantado tem de ser pego, cor ≤ 3,0° de matiz e saturação ≥ 0,75.',
            'Blocos com < 2 % de tinta ou de papel (canto de letra) não entram no veredito e são contados no relatório.',
            'Embalagem abaixo de 20 % da altura do quadro é miniatura: sai do mesmo mestre, sem alegação de fidelidade.',
            'Nenhuma edição por IA depois da composição. Tipo sempre por código (motor _build/brand/holofote.js).',
            'Segurança da chama (§D.8): vela acesa só sob observação de cena; nada de papel, tecido ou confete perto da chama.',
            'Sem rótulo de IA nos anúncios (fundadora, 6 out 2026). Sem depoimento, sem frase de luto, sem promessa que o rótulo não faz.',
            'Vídeo: quadros PNG codificados por _build/tools/codificar.py (BT.709 convertido e marcado). Som: −14 LUFS integrado, ≤ −1 dBTP.',
        ],
        'produtos': produtos(),
        'pecas': cen,
        'filmes': filmes,
        'anuncios': ads,
        'som': {'leia_me': '04_FILMES/som/LEIA_ME.md', 'creditos': '04_FILMES/som/CREDITOS.md',
                'manifesto': '04_FILMES/som/manifesto_sfx.json', 'cue_sheet': '06_PRODUCAO/AUDIO_CUE_SHEET.csv'},
        'fidelidade': '06_PRODUCAO/fidelidade/ (um JSON por peça; filmes com resumo e quadro a quadro)',
        'falta': 'ver 06_PRODUCAO/STATUS_ENTREGA.txt',
    }
    json.dump(B, open(os.path.join(PROD, 'MACHINE_BRIEF.json'), 'w'), ensure_ascii=False, indent=1)


def status_txt():
    st = P.status()
    rel_p = os.path.join(PROD, 'pacote_preenchimento.json')
    R = json.load(open(rel_p)) if os.path.exists(rel_p) else {}
    out = ['HOLOFOTE · STATUS DA ENTREGA · ' + st.pop('STATUS_DATA'), '',
           'Gerado por _build/pacote/maquina.py a partir das pastas. ENTREGUE = todos os arquivos esperados existem;',
           'PARCIAL = alguns; AUSENTE = nenhum. Nenhuma peça é "aprovada" aqui: aprovação é verificador real + olho humano.', '']
    nomes = {'STATUS_SISTEMA': 'Sistema e livro da marca', 'STATUS_LOGO': 'Logo, O FOCO, A MARCA', 'STATUS_CARTAZES': 'Cartazes (12)',
             'STATUS_ROTULOS': 'Rótulos-mestre', 'STATUS_PACKSHOTS': 'Embalagem e objetos', 'STATUS_KV': 'KV-01 e KV-45',
             'STATUS_C': 'Série C (C01–C10)', 'STATUS_B': 'BOLETIM (B01–B08)', 'STATUS_DIGITAL': 'D01, D02, figurinhas, S01',
             'STATUS_L': 'Loja (L01–L07)', 'STATUS_FILMES': 'Filmes', 'STATUS_SOM': 'Som', 'STATUS_ANIMATIC': 'O ANÚNCIO (animatics)',
             'STATUS_MAQUINA': 'Arquivos de máquina', 'STATUS_FIDELIDADE': 'Relatórios de fidelidade'}
    for k, v in st.items():
        out.append('%-28s %s' % (nomes.get(k, k), v))
    out += ['', 'NÃO PRODUZIDO DE PROPÓSITO',
            '• Pessoas (H01, H02, M01) e as peças P01–P03: precisam de créditos de geração e da aprovação escrita da dona.',
            '  Os anúncios estão em animatic com manequim cinza; os prompts estão em 05_ANUNCIO/.',
            '• O som foi medido (loudness, pico, sincronia), mas ainda não foi ouvido por uma pessoa. Ouvir antes de mostrar.']
    if R.get('faltas') or R.get('dados_ausentes'):
        out += ['', 'O PACOTE AINDA MOSTRA AUSENTE EM', '• figuras: ' + ', '.join(R.get('faltas', [])) if R.get('faltas') else '',
                '• dados: ' + ', '.join(R.get('dados_ausentes', [])) if R.get('dados_ausentes') else '']
    open(os.path.join(PROD, 'STATUS_ENTREGA.txt'), 'w', encoding='utf-8').write('\n'.join(x for x in out if x is not None) + '\n')


def inventario():
    itens = []
    for raiz in ('00_estrategia', '01_MARCA', '02_PRODUTO', '03_LANCAMENTO', '04_FILMES', '05_ANUNCIO', '06_PRODUCAO', '07_KIT_COMPLETO'):
        for dp, dn, fn in os.walk(os.path.join(KIT, raiz)):
            dn[:] = [d for d in dn if not d.startswith('_') or d in ('_sets_tests', '_objects_tests')]
            for f in sorted(fn):
                p = os.path.join(dp, f)
                h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
                itens.append({'arquivo': rel(p), 'bytes': os.path.getsize(p), 'sha256': h})
    json.dump({'kit': 'HOLOFOTE', 'arquivos': len(itens), 'bytes': sum(i['bytes'] for i in itens), 'itens': itens},
              open(os.path.join(KIT, 'INVENTARIO_ARQUIVOS.json'), 'w'), ensure_ascii=False, indent=1)
    return len(itens)


def main():
    ids = ids_do_pacote()
    cen = cenas(ids)
    nc = len(cues())
    co = cortes()
    social(ids)
    brief(ids, cen)
    status_txt()
    n = inventario()
    print('CENAS %d · cues %d · cortes %d · inventário %d arquivos' % (len(cen), nc, len(co), n))


if __name__ == '__main__':
    main()
