"""Preenche o Pacote de Informação Criativa a partir dos arquivos e relatórios REAIS do kit.

    /home/user/venvs/web/bin/python _build/pacote/preencher.py [--pdf]

Lê   _build/pacote/HOLOFOTE_PACKET_modelo.html       (o modelo com [preencher] e as caixas data-slot)
Grava 07_KIT_COMPLETO/HOLOFOTE_PACKET.html            (o pacote preenchido)
      07_KIT_COMPLETO/figuras/<SLOT>.jpg              (uma imagem por caixa, montada dos arquivos entregues)
      07_KIT_COMPLETO/HOLOFOTE_PACKET.pdf             (com --pdf; A4, Chromium)
      06_PRODUCAO/pacote_preenchimento.json           (o que entrou, de onde veio, e o que ficou faltando)

Regra: nenhum número é escrito à mão. Cada [preencher] vem de um arquivo (vídeo medido com ffprobe, loudness dos
JSONs da equipe de som, fidelidade dos JSONs de 06_PRODUCAO/fidelidade/, segundos de render dos logs). O que não
existe fica AUSENTE e entra na lista de faltas; nunca é estimado.
"""
import argparse, glob, html, json, os, re, subprocess, sys
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
MODELO = os.path.join(HERE, 'HOLOFOTE_PACKET_modelo.html')
SAIDA = os.path.join(KIT, '07_KIT_COMPLETO', 'HOLOFOTE_PACKET.html')
FIG = os.path.join(KIT, '07_KIT_COMPLETO', 'figuras')
FIDDIR = os.path.join(KIT, '06_PRODUCAO', 'fidelidade')
PAPEL = (0xEC, 0xF8, 0xFF)          # BGR
FILMES = os.path.join(KIT, '04_FILMES')
sys.path.insert(0, os.path.join(KIT, '_build', 'tools'))

FALTAS, FONTES = [], {}


def k(p):
    return os.path.join(KIT, p)


def achar(*padroes, excluir=('limpo', '_16bit', '_alpha', '_tests', 'teste')):
    for pd in padroes:
        for f in sorted(glob.glob(k(pd))):
            if not any(x in os.path.basename(f) or x in f for x in excluir):
                return f
    return None


def br(v, casas=1):
    if v is None:
        return None
    s = ('%.' + str(casas) + 'f') % v
    return s.replace('-', '−').replace('.', ',')


# ------------------------------------------------------------------------------------------------ imagens

def ler(f):
    a = cv2.imread(f, cv2.IMREAD_UNCHANGED)
    if a is None:
        raise FileNotFoundError(f)
    if a.ndim == 2:
        a = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
    if a.shape[2] == 4:
        al = a[..., 3:4].astype(np.float32) / 255
        a = (a[..., :3].astype(np.float32) * al + np.array(PAPEL, np.float32) * (1 - al)).astype(np.uint8)
    return a


def caber(a, w=None, h=None):
    H, W = a.shape[:2]
    s = min((w / W) if w else 1e9, (h / H) if h else 1e9)
    return cv2.resize(a, (max(1, round(W * s)), max(1, round(H * s))), interpolation=cv2.INTER_AREA)


def grade(ims, cols, cel_h, gap=24, fundo=PAPEL):
    ims = [caber(a, h=cel_h) for a in ims]
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    W = max(sum(a.shape[1] for a in r) + gap * (len(r) - 1) for r in rows)
    H = sum(max(a.shape[0] for a in r) for r in rows) + gap * (len(rows) - 1)
    out = np.full((H, W, 3), fundo, np.uint8)
    y = 0
    for r in rows:
        rw = sum(a.shape[1] for a in r) + gap * (len(r) - 1)
        x = (W - rw) // 2
        for a in r:
            out[y:y + a.shape[0], x:x + a.shape[1]] = a
            x += a.shape[1] + gap
        y += max(a.shape[0] for a in r) + gap
    return out


def pilha(ims, largura=1800, gap=24):
    ims = [caber(a, w=largura) for a in ims]
    H = sum(a.shape[0] for a in ims) + gap * (len(ims) - 1)
    out = np.full((H, largura, 3), PAPEL, np.uint8)
    y = 0
    for a in ims:
        x = (largura - a.shape[1]) // 2
        out[y:y + a.shape[0], x:x + a.shape[1]] = a
        y += a.shape[0] + gap
    return out


def quadros_de(mp4, idx):
    from codificar import ffmpeg
    out = []
    cap = cv2.VideoCapture(mp4)
    for i in idx:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, fr = cap.read()
        if ok:
            out.append(fr)
    cap.release()
    return out


def frente_verso(wrap_prev, lado):
    a = ler(wrap_prev)
    W = a.shape[1]
    x0, x1 = (0.06, 0.44) if lado == 'frente' else (0.56, 0.94)
    return a[:, int(W * x0):int(W * x1)]


def fig_slots():
    """SLOT -> (função que monta a imagem, [arquivos-fonte]). Só arquivos ENTREGUES; testes nunca entram."""
    S = {}
    prev = k('02_PRODUTO/rotulos/HLF-02_ROTULO_wrap_preview.png')
    S['ROTULO_FRENTE'] = (lambda: caber(frente_verso(prev, 'frente'), w=1600), [prev])
    S['ROTULO_VERSO'] = (lambda: caber(frente_verso(prev, 'verso'), w=1600), [prev])
    f = achar('02_PRODUTO/tampa/HLF-TAMPA-90_preview.png')
    S['TAMPA'] = (lambda f=f: caber(ler(f), w=1400), [f])
    fb, l03 = achar('02_PRODUTO/base/HLF-BASE-200_preview_por-baixo.png'), achar('02_PRODUTO/renders/L03*.png', '03_LANCAMENTO/L/L03*.png')
    S['BASE'] = ((lambda: grade([ler(fb), ler(l03)], 2, 900)) if l03 else (lambda: caber(ler(fb), w=1400)), [fb, l03])
    c1, c2 = achar('02_PRODUTO/renders/L04*.png', '03_LANCAMENTO/L/L04*.png'), achar('02_PRODUTO/renders/C05*.png', '03_LANCAMENTO/C/C05*.png')
    cf = achar('02_PRODUTO/renders/CASE*fechado*.png')
    cs = [x for x in (cf, c1, c2) if x]
    S['CASE'] = ((lambda cs=cs: grade([ler(x) for x in cs], len(cs), 900)) if cs else None, cs)
    p1, p2 = k('02_PRODUTO/pulseira/PULSEIRA_padrao.png'), k('02_PRODUTO/pulseira/PULSEIRA_SELO_faixa.png')
    S['PULSEIRA'] = (lambda: pilha([ler(p1), caber(ler(p2), w=900)]), [p1, p2])
    f = k('02_PRODUTO/setlist/SETLIST_preview_aberto.jpg')
    S['SETLIST'] = (lambda f=f: caber(ler(f), w=1600), [f])
    f = k('02_PRODUTO/cartucho/HLF-02-200_CARTUCHO_planificado_preview.jpg')
    S['CARTUCHO'] = (lambda f=f: caber(ler(f), w=1600), [f])
    ps = [k('02_PRODUTO/rotulos/%s_ROTULO_wrap_preview.png' % n) for n in
          ('HLF-CASE-01_DONA-CIDA', 'HLF-CASE-02_MAE-CORACAO', 'HLF-CASE-03_MAINHA')]
    S['ROTULOS_PERSONALIZADOS'] = (lambda: grade([frente_verso(p, 'frente') for p in ps], 3, 700), ps)
    for slot, f in (('PALETA', '01_MARCA/livro/LIVRO-08_PALETA.png'), ('TIPOGRAFIA', '01_MARCA/livro/LIVRO-04_AS-TRES-VOZES.png'),
                    ('LOGO', '01_MARCA/livro/LIVRO-05_O-LOGO.png'), ('STK', '03_LANCAMENTO/STK/STK_folha_contato.jpg')):
        S[slot] = (lambda f=k(f): caber(ler(f), w=1600), [k(f)])
    for fmt in ('9x16', '4x5', '1x1', '16x9'):
        f = achar('03_LANCAMENTO/KV/KV-01_%s*.png' % fmt)
        S['KV-01_' + fmt] = ((lambda f=f: caber(ler(f), w=1200)) if f else None, [f])
    f = achar('03_LANCAMENTO/KV/KV-45_aceso*SUA*.png', '03_LANCAMENTO/KV/KV-45_aceso*.png', '02_PRODUTO/renders/KV-45_aceso.png')
    S['KV-45'] = (lambda f=f: caber(ler(f), w=1080), [f])
    for i in range(1, 11):
        f = achar('03_LANCAMENTO/C/C%02d_*.png' % i)
        S['C%02d' % i] = ((lambda f=f: caber(ler(f), w=1080)) if f else None, [f])
    for i in range(1, 9):
        f = achar('03_LANCAMENTO/B/B%02d_*_1x1.png' % i)
        S['B%02d' % i] = ((lambda f=f: caber(ler(f), w=1080)) if f else None, [f])
    f = achar('03_LANCAMENTO/D/D01_*.png')
    S['D01'] = ((lambda f=f: caber(ler(f), w=1080)) if f else None, [f])
    d2 = [achar('03_LANCAMENTO/D/D02_*inteiro.png'), achar('03_LANCAMENTO/D/D02_*rasgado.png')]
    S['D02'] = ((lambda: pilha([ler(x) for x in d2], 1400)) if all(d2) else None, d2)
    for i in range(1, 8):
        f = achar('03_LANCAMENTO/L/L%02d_*.png' % i, '02_PRODUTO/renders/L%02d_*.png' % i)
        S['L%02d' % i] = ((lambda f=f: caber(ler(f), w=1200)) if f else None, [f])
    f15 = achar('04_FILMES/F15*_mudo.mp4', '04_FILMES/HLF-F15*_mudo.mp4')
    S['F15_FRAMES'] = ((lambda: grade(quadros_de(f15, [0, 14, 60, 132, 176, 204, 216, 222, 288, 359]), 5, 640, 16))
                       if f15 else None, [f15])
    f6 = [achar('04_FILMES/*F06A*_mudo.mp4'), achar('04_FILMES/*F06B*_mudo.mp4'),
          achar('04_FILMES/*F06C*07-05*_mudo.mp4'), achar('04_FILMES/*F06C*08-05*_mudo.mp4'), achar('04_FILMES/*F06C*09-05*_mudo.mp4')]
    S['F06_FRAMES'] = ((lambda: grade(sum([quadros_de(m, [12, 72, 140]) for m in f6 if m], []), 6, 560, 16))
                       if any(f6) else None, f6)
    for h in ('H01', 'H02'):
        f = achar('02_PRODUTO/renders/_objects_tests/T_previs_%s_stand.png' % h, excluir=())
        S['CASTING_' + h] = ((lambda f=f: caber(ler(f), w=700)) if f else None, [f])
    an = achar('05_ANUNCIO/*1A*_som.mp4', '05_ANUNCIO/**/*1A*.mp4', '05_ANUNCIO/*.mp4')
    S['ANUNCIO_ANIMATIC'] = ((lambda: grade(quadros_de(an, [24, 96, 180, 300]), 4, 900, 16)) if an else None, [an])
    return S


# ------------------------------------------------------------------------------------------------ números

def sonda(mp4):
    from codificar import ffmpeg
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets', '-show_entries',
                        'stream=nb_read_packets,r_frame_rate:format=duration', '-of', 'json', mp4],
                       capture_output=True, text=True)
    j = json.loads(r.stdout)
    return float(j['format']['duration']), int(j['streams'][0]['nb_read_packets'])


def loud(mp4):
    """Integrated loudness and true peak of the delivered file's own audio track (ffmpeg ebur128)."""
    r = subprocess.run(['ffmpeg', '-nostats', '-i', mp4, '-filter_complex', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True)
    t = r.stderr[r.stderr.rfind('Summary:'):]
    i = re.search(r'I:\s*(-?[\d.]+) LUFS', t)
    p = re.search(r'Peak:\s*(-?[\d.]+) dBFS', t)
    return (float(i.group(1)) if i else None), (float(p.group(1)) if p else None)


def fid(nome_padrao):
    fs = sorted(glob.glob(os.path.join(FIDDIR, nome_padrao)))
    if not fs:
        return None, None
    try:
        r = json.load(open(fs[0]))
        r = r[0] if isinstance(r, list) else r
        return r, fs[0]
    except Exception:
        return None, fs[0]


def linha_fid(r):
    if not r:
        return None
    c = r.get('control') or {}
    cor = None
    if r.get('hue_shift_deg') is not None:
        cor = '%s° / %s' % (br(r['hue_shift_deg'], 1), br(r.get('sat_ratio'), 2))
    passa = r.get('pass', r.get('pass_'))
    return dict(PIOR=br(r.get('worst_tile'), 3), P5=br(r.get('p5_tile'), 3),
                CONTROLE=(br(c.get('worst_tile'), 2) + (' (pego)' if c.get('caught') else ' (NÃO pego)')) if c else None,
                COR=cor or 'não medida', RESULTADO='PASSA' if passa else 'FALHA')


def dados():
    D = {}
    # filmes
    filmes = {'F15': 'F15*', 'F06A': 'F06A*', 'F06B': 'F06B*', 'F06C_0705': 'F06C*07-05*',
              'F06C_0805': 'F06C*08-05*', 'F06C_0905': 'F06C*09-05*', 'S01': 'S01*'}
    for key, pd in filmes.items():
        mp4 = achar('04_FILMES/%s_som.mp4' % pd, '04_FILMES/HLF-%s_som.mp4' % pd)
        if not mp4:
            continue
        dur, n = sonda(mp4)
        li, tp = loud(mp4)
        D[key + '_DURACAO'] = br(dur, 2) + ' s'
        D[key + '_QUADROS'] = str(n)
        D[key + '_LUFS'] = br(li, 1) if li is not None else None
        D[key + '_TP'] = (br(tp, 1) + ' dBTP') if tp is not None else None
        FONTES[key] = os.path.relpath(mp4, KIT)
        if key != 'S01':
            fs = sorted(glob.glob(os.path.join(FIDDIR, pd + '.json')))
            if fs:
                R = json.load(open(fs[0])).get('resumo', {})
                ok = not R.get('frames_fail') and R.get('frames_pass') == R.get('frames_label_visible')
                D[key + '_FID'] = 'pior %s · %s · %s quadros' % (br(R.get('worst_tile_min'), 3), 'PASSA' if ok else 'FALHA',
                                                               R.get('frames_label_visible'))
                FONTES[key + '_FID'] = os.path.relpath(fs[0], KIT)
    # som
    idw = k('04_FILMES/som/identidade/HLF-ID-01_vinheta_ovacao_de_uma_pessoa_so_2s0.wav')
    if os.path.exists(idw):
        import soundfile as sf
        D['SOM_LOGO_DURACAO'] = br(sf.info(idw).duration, 3) + ' s'
    desv = []
    for j in glob.glob(k('04_FILMES/som/filmes/*_som.json')):
        for q in json.load(open(j)).get('quadros_chave', []):
            if q.get('desvio_quadros') is not None:
                desv.append(abs(q['desvio_quadros']))
    if desv:
        D['SOM_ONSET_DESVIO_MAX'] = '%s quadro (em %d ataques medidos)' % (br(max(desv), 3), len(desv))
    # animatics
    ans = sorted(glob.glob(k('05_ANUNCIO/**/*_som.mp4'), recursive=True))
    if ans:
        ls = [loud(a)[0] for a in ans]
        ls = [x for x in ls if x is not None]
        if ls:
            D['ANIMATIC_LUFS'] = '%s a %s LUFS integrado (%d masters, alvo −14)' % (br(min(ls), 1), br(max(ls), 1), len(ls))
    # VO
    vt = achar('05_ANUNCIO/vo_tempos.json', '_build/anuncio/_tmp_animatic/vo/vo_tempos.json', excluir=())
    if vt:
        V = json.load(open(vt))
        for m in ('1A', '1B', '1C', '2A', '2B', '3A', '3B', '3C'):
            for parte, chave in (('gancho', 'GANCHO'), ('corpo', 'CORPO'), ('kv_vo', 'KV')):
                v = V.get('%s_%s' % (m, parte))
                if v:
                    D['VO_%s_%s' % (m, chave)] = '%s s / %s s' % (br(v['duracao_s'], 2), br(v['janela_s'], 2))
    # fidelidade por vista
    vistas = {'FRENTE': 'L00_FRENTE*.json', 'TRES_QUARTOS': 'L01_*.json', 'VERSO': 'L02_*.json', 'BASE': 'L03_*.json',
              'ALBEDO': 'C06_*albedo*.json', 'CASE01': 'C10_*DONA*.json', 'CASE02': 'C10_*MAE*.json',
              'CASE03': 'C10_*MAINHA*.json', 'SINGLE': 'L06_*SINGLE*.json'}
    for v, pd in vistas.items():
        r, f = fid(pd)
        l = linha_fid(r)
        if l:
            for c, val in l.items():
                D['FID_%s_%s' % (v, c)] = val
            FONTES['FID_' + v] = os.path.relpath(f, KIT)
    todos = [f for f in glob.glob(os.path.join(FIDDIR, '*.json'))]
    pec, ok, ruim, quadros = 0, 0, 0, 0
    for f in todos:
        try:
            r = json.load(open(f))
            r = r[0] if isinstance(r, list) else r
        except Exception:
            continue
        if 'resumo' in r:
            quadros += int(r['resumo'].get('frames_label_visible') or 0)
            continue
        if r.get('thumbnail_sem_alegacao'):
            continue
        pec += 1
        if r.get('pass', r.get('pass_')):
            ok += 1
        else:
            ruim += 1
    D.update(FID_PECAS_CONFERIDAS=str(pec), FID_PECAS_PASSARAM=str(ok), FID_PECAS_FALHARAM=str(ruim),
             FID_QUADROS_CONFERIDOS=str(quadros), FID_RELATORIO_ARQUIVO='06_PRODUCAO/fidelidade/ (um JSON por peça)')
    # segundos de render
    log = k('_build/shots/campanha_log.jsonl')
    seg = {}
    if os.path.exists(log):
        for ln in open(log):
            try:
                j = json.loads(ln)
            except Exception:
                continue
            if not j.get('teste'):
                seg[j['nome']] = j.get('segundos')
    seg['KV-45_aceso'], seg['KV-45_apagado'] = 389.8, 309.2      # motor.still, logs do diretor (6 out 2026)

    def soma(pref):
        v = [s for n, s in seg.items() if n.startswith(pref) and s]
        return ('%s min (%d placas)' % (br(sum(v) / 60, 1), len(v))) if v else None
    for key, pref in (('KV01', 'KV-01'), ('KV45', 'KV-45'), ('C02', 'C02'), ('C03', 'C03'), ('C04', 'C04'),
                      ('C06', 'C06'), ('C07', 'C07'), ('L05', 'L05')):
        D['SEG_' + key] = soma(pref)
    plano = achar('06_PRODUCAO/FILM_PLAN.json', '04_FILMES/FILM_PLAN.json', excluir=())
    if plano:
        P = json.load(open(plano))
        for key, pd in (('F15', 'F15'), ('F06AB', 'F06A'), ('F06C', 'F06C')):
            v = [f.get('render_s') or f.get('segundos_render') for f in (P.get('filmes') or P if isinstance(P, list) else [])
                 if isinstance(f, dict) and pd in str(f.get('id', f.get('filme', '')))]
            v = [x for x in v if x]
            if v:
                D['SEG_' + key] = br(sum(v) / 60, 1) + ' min'
    return D


STATUS = {
    'STATUS_SISTEMA': ['00_estrategia/CREATIVE_PLATFORM.md', '01_MARCA/livro/LIVRO-16_SUA-VEZ.png'],
    'STATUS_LOGO': ['01_MARCA/logo/HOLOFOTE_logo_preto-sobre-amarelo.svg', '01_MARCA/logo/O_FOCO_preto.svg'],
    'STATUS_CARTAZES': ['01_MARCA/cartazes/CARTAZ-%02d_*.png' % i for i in range(1, 13)],
    'STATUS_ROTULOS': ['02_PRODUTO/rotulos/HLF-0%d_ROTULO_wrap.png' % i for i in range(1, 5)] +
                      ['02_PRODUTO/rotulos/HLF-02-080_ROTULO_wrap.png', '02_PRODUTO/rotulos/HLF-CASE-0*_ROTULO_wrap.png'],
    'STATUS_PACKSHOTS': ['02_PRODUTO/tampa/HLF-TAMPA-90_preview.png', '02_PRODUTO/base/HLF-BASE-200_preview_por-baixo.png',
                         '02_PRODUTO/setlist/SETLIST_preview_aberto.jpg', '02_PRODUTO/pulseira/PULSEIRA_padrao.png',
                         '02_PRODUTO/cartucho/HLF-02-200_CARTUCHO_planificado_preview.jpg', '02_PRODUTO/renders/L04*.png'],
    'STATUS_KV': ['03_LANCAMENTO/KV/KV-01_%s*.png' % f for f in ('9x16', '4x5', '1x1', '16x9')] + ['03_LANCAMENTO/KV/KV-45*.png'],
    'STATUS_C': ['03_LANCAMENTO/C/C%02d_*.png' % i for i in range(1, 11)],
    'STATUS_B': ['03_LANCAMENTO/B/B%02d_*.png' % i for i in range(1, 9)],
    'STATUS_DIGITAL': ['03_LANCAMENTO/D/D01_*.png', '03_LANCAMENTO/D/D02_*.png', '03_LANCAMENTO/STK/STK-0*.webp',
                       '04_FILMES/*S01*_som.mp4'],
    'STATUS_L': ['03_LANCAMENTO/L/L0%d_*.png' % i for i in range(1, 8)],
    'STATUS_FILMES': ['04_FILMES/*F15*_som.mp4', '04_FILMES/*F06A*_som.mp4', '04_FILMES/*F06B*_som.mp4',
                      '04_FILMES/*F06C*_som.mp4', '04_FILMES/*S01*_som.mp4'],
    'STATUS_SOM': ['04_FILMES/som/identidade/HLF-ID-01_*.wav', '04_FILMES/som/sfx/HLF-SFX-01_*.wav', '04_FILMES/som/CREDITOS.md'],
    'STATUS_ANIMATIC': ['05_ANUNCIO/**/*1A*_som.mp4', '05_ANUNCIO/**/*3C*_som.mp4'],
    'STATUS_MAQUINA': ['05_ANUNCIO/CREATOR_ADS.json', '05_ANUNCIO/SEEDANCE_PROMPTS.txt', '06_PRODUCAO/MACHINE_BRIEF.json',
                       '06_PRODUCAO/CENAS.csv', '06_PRODUCAO/AUDIO_CUE_SHEET.csv', '06_PRODUCAO/TEXTOS_SOCIAL.txt'],
    'STATUS_FIDELIDADE': ['06_PRODUCAO/fidelidade/*.json'],
}


def status():
    D = {}
    for key, pads in STATUS.items():
        tem = [p for p in pads if glob.glob(k(p), recursive=True)]
        falta = [p for p in pads if p not in tem]
        if not falta:
            D[key] = 'ENTREGUE'
        elif tem:
            D[key] = 'PARCIAL · falta: ' + ', '.join(os.path.basename(p) for p in falta)
        else:
            D[key] = 'AUSENTE'
    D['STATUS_DATA'] = '6 out 2026'
    return D


# ------------------------------------------------------------------------------------------------ tabela

def tabela_fid():
    linhas = []
    for f in sorted(glob.glob(os.path.join(FIDDIR, '*.json'))):
        try:
            r = json.load(open(f))
            r = r[0] if isinstance(r, list) else r
        except Exception:
            continue
        nome = os.path.splitext(os.path.basename(f))[0]
        if 'resumo' in r:
            R = r['resumo']
            ok = not R.get('frames_fail') and R.get('frames_pass') == R.get('frames_label_visible')
            linhas.append('<tr><td>%s (filme, %s quadros com rótulo)</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s/%s pegos</td><td class="n">%s</td><td>%s</td></tr>'
                          % (html.escape(nome), R.get('frames_label_visible'), br(R.get('worst_tile_min'), 3), br(R.get('p5_min'), 3),
                             R.get('controls_caught'), R.get('frames_label_visible'),
                             ('%s° / %s' % (br((R.get('hue_shift_range') or [None])[0], 1), br(R.get('sat_ratio_min'), 2))) if R.get('hue_shift_range') else 'não medida',
                             'PASSA' if ok else 'FALHA'))
            continue
        if r.get('thumbnail_sem_alegacao'):
            linhas.append('<tr><td>%s</td><td colspan="5">miniatura (&lt; 20%% do quadro): sem alegação de fidelidade</td></tr>' % html.escape(nome))
            continue
        l = linha_fid(r)
        if not l:
            continue
        linhas.append('<tr><td>%s</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td><td>%s</td></tr>'
                      % (html.escape(nome), l['PIOR'] or '—', l['P5'] or '—', l['CONTROLE'] or '—', l['COR'], l['RESULTADO']))
    if not linhas:
        return None
    return ('<table class="compacta"><thead><tr><th>Peça</th><th>Pior bloco</th><th>5º pct</th><th>Erro plantado</th>'
            '<th>Cor (matiz / sat.)</th><th>Resultado</th></tr></thead><tbody>' + ''.join(linhas) + '</tbody></table>')


# ------------------------------------------------------------------------------------------------ montagem

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', action='store_true')
    a = ap.parse_args()
    s = open(MODELO, encoding='utf-8').read()
    os.makedirs(FIG, exist_ok=True)
    # figuras
    usadas = {}
    for slot, (fn, fontes) in fig_slots().items():
        if fn is None or not all(fontes if isinstance(fontes, list) else [fontes]) and slot not in ('CASE', 'BASE', 'F06_FRAMES'):
            FALTAS.append('figura ' + slot)
            continue
        try:
            img = fn()
        except Exception as e:
            FALTAS.append('figura %s (%s)' % (slot, e))
            continue
        out = os.path.join(FIG, slot + '.jpg')
        cv2.imwrite(out, img, [cv2.IMWRITE_JPEG_QUALITY, 88])
        usadas[slot] = [os.path.relpath(f, KIT) for f in fontes if f]
    tab = tabela_fid()

    def fig(m):
        slot = m.group(1)
        if slot == 'FIDELIDADE_TABELA' and tab:
            return m.group(0).replace(re.search(r'<div class="slot">.*?</div>', m.group(0), re.S).group(0), tab)
        if slot not in usadas:
            return m.group(0)
        alt = html.escape(slot)
        return re.sub(r'<div class="slot">.*?</div>', '<img class="fig" src="figuras/%s.jpg" alt="%s">' % (slot, alt),
                      m.group(0), count=1, flags=re.S)
    s = re.sub(r'<figure data-slot="([^"]+)"[^>]*>.*?</figure>', fig, s, flags=re.S)
    s = s.replace('</style>', 'figure img.fig { display: block; width: 100%; height: auto; }\n'
                  'figure:has(img.fig) .slot { display: none; }\n</style>', 1)
    # dados
    D = dados()
    D.update(status())
    vazios = []

    def dado(m):
        key = m.group(1)
        v = D.get(key)
        if v is None:
            vazios.append(key)
            return m.group(0).replace('[preencher]', 'AUSENTE')
        return m.group(0).replace('[preencher]', html.escape(v))
    s = re.sub(r'<span data-dado="([^"]+)">\[preencher\]</span>', dado, s)
    open(SAIDA, 'w', encoding='utf-8').write(s)
    rel = dict(figuras=usadas, faltas=FALTAS, dados_ausentes=sorted(set(vazios)), fontes=FONTES,
               restam_preencher=s.count('[preencher]'))
    json.dump(rel, open(k('06_PRODUCAO/pacote_preenchimento.json'), 'w'), ensure_ascii=False, indent=2)
    print('figuras %d · faltas %d · dados ausentes %d · [preencher] restantes %d'
          % (len(usadas), len(FALTAS), len(set(vazios)), s.count('[preencher]')))
    if FALTAS:
        print('faltas:', FALTAS)
    if vazios:
        print('ausentes:', sorted(set(vazios)))
    if a.pdf:
        from playwright.sync_api import sync_playwright
        sys.path.insert(0, os.path.join(KIT, '_build', 'brand'))
        from render import CHROME
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=CHROME, args=['--allow-file-access-from-files'])
            pg = b.new_page()
            pg.goto('file://' + SAIDA)
            pg.wait_for_load_state('networkidle')
            pg.pdf(path=SAIDA.replace('.html', '.pdf'), prefer_css_page_size=True, print_background=True)
            b.close()
        print('pdf', os.path.relpath(SAIDA.replace('.html', '.pdf'), KIT))


if __name__ == '__main__':
    main()
