"""Write 02_PRODUTO/LEIA_ME.md from what is actually on disk: one line per file, plain Portuguese.

    /home/user/venvs/web/bin/python _build/pack/leia_me.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(os.path.dirname(os.path.dirname(HERE)), '02_PRODUTO')

FAIXA = {'1': 'CAMARIM', '2': 'AO VIVO', '3': 'MAIS UM!', '4': 'ACÚSTICO'}

CT = r'(HLF-0\d-200|HLF-02-080|HLF-REF-0\d)'


def ct(code):
    """(name for the line, carton size) for a carton code."""
    if code == 'HLF-02-080':
        return 'HLF-02-080 (O INGRESSO SINGLE, AO VIVO)', '74 × 74 × 76'
    m = re.fullmatch(r'HLF-REF-0(\d)', code)
    if m:
        return f'{code} (refil NOVA TEMPORADA, {FAIXA[m[1]]})', '74 × 74 × 82'
    m = re.fullmatch(r'HLF-0(\d)-200', code)
    return f'{code} ({FAIXA[m[1]]})', '96 × 96 × 98'


RULES = [
    # rotulos
    (r'HLF-02-080_ROTULO_wrap\.png', 'O SINGLE: mestre do rótulo 7288 × 1960 px (182,2 mm × zona 14–63 mm, 40 px/mm), só tinta, fundo transparente.'),
    (r'HLF-02-080_ROTULO_wrap\.svg', 'O SINGLE: o mesmo rótulo em vetor, em milímetros reais.'),
    (r'HLF-02-080_ROTULO_wrap_preview\.png', 'O SINGLE: prévia chapada do rótulo sobre o amarelo do copo.'),
    (r'HLF-02-080_ROTULO_wrap_ERRO-PLANTADO\.png', 'O SINGLE: cópia com erro plantado (E de MÃE espelhado) para testar a ferramenta de fidelidade.'),
    (r'HLF-02-080_label_copy\.json', 'O SINGLE: todos os textos, medidas e o hash do mestre.'),
    (r'(HLF-0\d)_ROTULO_wrap\.png', lambda m: f'{m[1]}: mestre do rótulo 9552 × 2560 px (40 px/mm), só tinta, fundo transparente.'),
    (r'(HLF-0\d)_ROTULO_wrap\.svg', lambda m: f'{m[1]}: o mesmo rótulo em vetor, em milímetros reais.'),
    (r'(HLF-0\d)_ROTULO_wrap_preview\.png', lambda m: f'{m[1]}: prévia chapada do rótulo sobre a cor do copo.'),
    (r'(HLF-0\d)_ROTULO_wrap_ERRO-PLANTADO\.png', lambda m: f'{m[1]}: cópia com erro plantado para testar a fidelidade.'),
    (r'(HLF-0\d)_label_copy\.json', lambda m: f'{m[1]}: todos os textos, medidas, desvios e o hash do mestre.'),
    (r'(HLF-CASE-0\d_[A-Z-]+)_ROTULO_wrap\.png', lambda m: f'{m[1]}: mestre do rótulo personalizado (9552 × 2560 px).'),
    (r'(HLF-CASE-0\d_[A-Z-]+)_ROTULO_wrap\.svg', lambda m: f'{m[1]}: o mesmo rótulo personalizado em vetor.'),
    (r'(HLF-CASE-0\d_[A-Z-]+)_ROTULO_wrap_preview\.png', lambda m: f'{m[1]}: prévia do rótulo personalizado sobre a cor do copo.'),
    (r'(HLF-CASE-0\d_[A-Z-]+)_ROTULO_wrap_ERRO-PLANTADO\.png', lambda m: f'{m[1]}: cópia com erro plantado para testar a fidelidade.'),
    (r'(HLF-CASE-0\d_[A-Z-]+)_label_copy\.json', lambda m: f'{m[1]}: textos, dados do pedido (fictícios) e medidas.'),
    # tampa
    (r'HLF-TAMPA-(\d\d)_topo\.png', lambda m: f'Tampa Ø{m[1]}: arte completa da impressão UV (fita gaffer + sombra + tintas), transparente fora do disco. É o arquivo que o 3D aplica.'),
    (r'HLF-TAMPA-(\d\d)_fita\.png', lambda m: f'Tampa Ø{m[1]}: só a fita gaffer amarela com textura de tecido e a sombra da ponta levantada.'),
    (r'HLF-TAMPA-(\d\d)_tinta\.png', lambda m: f'Tampa Ø{m[1]}: só as tintas ("ela fica aqui." preto e "a tampa vira palco." amarelo).'),
    (r'HLF-TAMPA-(\d\d)_tinta\.svg', lambda m: f'Tampa Ø{m[1]}: as duas tintas em vetor, em mm.'),
    (r'HLF-TAMPA-(\d\d)_trama_altura\.png', lambda m: f'Tampa Ø{m[1]}: mapa de altura 16 bits da trama da fita (para o relevo no 3D).'),
    (r'HLF-TAMPA-(\d\d)_preview\.png', lambda m: f'Tampa Ø{m[1]}: prévia sobre o disco preto.'),
    (r'HLF-TAMPA-(\d\d)\.json', lambda m: f'Tampa Ø{m[1]}: geometria das fitas, ponta levantada e posição dos textos, em mm.'),
    # base
    (r'HLF-BASE-(\d+)_PRECISAVA_altura16\.png', lambda m: f'Fundo do copo {m[1]} g: relevo "PRECISAVA." como mapa de altura 16 bits (branco = 0,4 mm), lido com o copo virado.'),
    (r'HLF-BASE-(\d+)_PRECISAVA\.svg', lambda m: f'Fundo do copo {m[1]} g: o relevo em vetor.'),
    (r'HLF-BASE-(\d+)_ETIQUETA-LOTE_PAPEL-ACUSTICO\.png', lambda m: f'Etiqueta de lote {m[1]} g em tinta papel (para o ACÚSTICO), transparente.'),
    (r'HLF-BASE-(\d+)_ETIQUETA-LOTE_PAPEL-ACUSTICO\.svg', lambda m: f'Etiqueta de lote {m[1]} g em tinta papel, vetor.'),
    (r'HLF-BASE-(\d+)_ETIQUETA-LOTE\.png', lambda m: f'Etiqueta de lote {m[1]} g em tinta preta, transparente (PP transparente fosco).'),
    (r'HLF-BASE-(\d+)_ETIQUETA-LOTE\.svg', lambda m: f'Etiqueta de lote {m[1]} g em tinta preta, vetor.'),
    (r'HLF-BASE-(\d+)_preview_por-baixo\.png', lambda m: f'Fundo do copo {m[1]} g visto por baixo, luz rasante, com a etiqueta no lugar (só para revisão).'),
    (r'HLF-BASE\.json', 'Medidas do relevo e das etiquetas, e a orientação de leitura.'),
    # case
    (r'CASE_ATLAS_(tampa|base)_foil\.png', lambda m: f'O CASE, {m[1]}: máscara do hot-foil prata no layout do atlas (branco = foil).'),
    (r'CASE_ATLAS_(tampa|base)_altura16\.png', lambda m: f'O CASE, {m[1]}: mapa de altura 16 bits (granulado tolex, foil achatado, cantoneiras abauladas).'),
    (r'CASE_ATLAS_tampa_espelho\.png', 'O CASE, tampa: máscara do espelho (branco = acrílico espelhado).'),
    (r'CASE_ABA_hasp\.png', 'O CASE: a aba do fecho (52 × 16 mm) com a fenda e "acesso restrito", recorte em alfa.'),
    (r'CASE_ABA_hasp\.svg', 'O CASE: a aba do fecho em vetor.'),
    (r'CASE_(tampa_\w+|base_\w+)\.png', lambda m: f'O CASE: painel {m[1].replace("_", " ")} (comum a todas as unidades), 10 px/mm.'),
    (r'CASE_(tampa_\w+|base_\w+)\.svg', lambda m: f'O CASE: painel {m[1].replace("_", " ")} em vetor (tintas, foil e faca em camadas).'),
    (r'(HLF-CASE-0\d)_ATLAS_tampa\.png', lambda m: f'{m[1]}: atlas 4 × 3 da tampa (130 × 130 × 30) para candle_lib.box().'),
    (r'(HLF-CASE-0\d)_ATLAS_base\.png', lambda m: f'{m[1]}: atlas 4 × 3 da base (130 × 130 × 102), case fechado (aba desenhada na frente).'),
    (r'(HLF-CASE-0\d)_PREVIEW_planificado\.jpg', lambda m: f'{m[1]}: prévia sombreada das duas caixas abertas em cruz (só revisão).'),
    (r'(HLF-CASE-0\d)_case\.json', lambda m: f'{m[1]}: textos, medidas, contrato do atlas e posição da aba.'),
    (r'(HLF-CASE-0\d)_(tampa_topo|base_frente|base_tras)\.png', lambda m: f'{m[1]}: painel {m[2].replace("_", " ")} personalizado, 10 px/mm.'),
    (r'(HLF-CASE-0\d)_(tampa_topo|base_frente|base_tras)\.svg', lambda m: f'{m[1]}: painel {m[2].replace("_", " ")} em vetor.'),
    # cartucho (O INGRESSO 96 x 96 x 98, O INGRESSO SINGLE 74 x 74 x 76, refil NOVA TEMPORADA 74 x 74 x 82)
    (CT + r'_CARTUCHO_ATLAS\.png', lambda m: f'{ct(m[1])[0]}: atlas 4 × 3 do cartucho {ct(m[1])[1]} para candle_lib.box().'),
    (CT + r'_CARTUCHO_planificado_preview\.jpg', lambda m: f'{ct(m[1])[0]}: folha planificada com a faca por cima (revisão).'),
    (CT + r'_CARTUCHO_planificado\.png', lambda m: f'{ct(m[1])[0]}: folha de impressão planificada, 10 px/mm, sangria de 3 mm.'),
    (CT + r'_CARTUCHO_([a-z0-9-]+)\.png', lambda m: f'{ct(m[1])[0]}: painel {m[2]}, 20 px/mm.'),
    (CT + r'_CARTUCHO_([a-z0-9-]+)\.svg', lambda m: f'{ct(m[1])[0]}: painel {m[2]} em vetor.'),
    (CT + r'_cartucho\.json', lambda m: f'{ct(m[1])[0]}: textos, medidas e desvios de cada painel.'),
    # refil
    (r'HLF-REF-0(\d)_TAMPA-PEEL\.png', lambda m: f'Refil NOVA TEMPORADA {FAIXA[m[1]]}: tampa peel Ø66 com aba, cor da faixa + tinta, recorte em alfa, 40 px/mm.'),
    (r'HLF-REF-0(\d)_TAMPA-PEEL_tinta\.png', lambda m: f'Refil {FAIXA[m[1]]}: só a tinta da tampa peel.'),
    (r'HLF-REF-0(\d)_TAMPA-PEEL\.svg', lambda m: f'Refil {FAIXA[m[1]]}: tampa peel em vetor, com a faca.'),
    (r'HLF-REF_CAPSULA_faixa-laser\.png', 'Cápsula do refil: faixa de LOTE · FAB · VAL gravada a laser (213,6 × 10 mm), transparente.'),
    (r'HLF-REF_CAPSULA_faixa-laser_preview\.png', 'Cápsula do refil: prévia da gravação sobre o alumínio preto.'),
    (r'HLF-REF_refil\.json', 'Refil: textos e medidas das tampas e da faixa.'),
    # setlist
    (r'SETLIST_lado-(\d)\.png', lambda m: f'A SETLIST, lado {m[1]}: arte de impressão 105 × 400 mm a 20 px/mm.'),
    (r'SETLIST_lado-(\d)\.svg', lambda m: f'A SETLIST, lado {m[1]}: vetor com as tintas preto e amarelo em camadas.'),
    (r'SETLIST_lado-(\d)_preto\.png', lambda m: f'A SETLIST, lado {m[1]}: separação da tinta preta (transparente).'),
    (r'SETLIST_lado-(\d)_amarelo\.png', lambda m: f'A SETLIST, lado {m[1]}: separação da tinta amarela (transparente).'),
    (r'SETLIST_picote_lado-1\.png', 'A SETLIST: máscara de picotes (branco) e dobras (cinza), lado 1.'),
    (r'SETLIST_preview_aberto\.jpg', 'A SETLIST: prévia dos dois lados abertos, com papel, dobras e picotes.'),
    (r'SETLIST\.json', 'A SETLIST: textos, posições e as notas de diagramação.'),
    # pulseira
    (r'PULSEIRA_padrao\.png', 'A PULSEIRA: desenho do jacquard 15 × 350 mm a 20 px/mm (preto + amarelo), duas repetições inteiras.'),
    (r'PULSEIRA_padrao\.svg', 'A PULSEIRA: o desenho do jacquard em vetor.'),
    (r'PULSEIRA_tecido\.png', 'A PULSEIRA: render do tecido (fios de trama, sarja preta, ourela).'),
    (r'PULSEIRA_tecido_altura16\.png', 'A PULSEIRA: mapa de altura 16 bits do tecido.'),
    (r'PULSEIRA_SELO_faixa\.png', 'Selo de papel 60 × 15 mm: a tira inteira como é impressa (só por fora), 20 px/mm; TOPO "pode / rasgar.", BAIXO "o que se guarda é a pulseira.".'),
    (r'PULSEIRA_SELO_faixa\.svg', 'Selo de papel: a tira inteira em vetor, em mm.'),
    (r'PULSEIRA_SELO_face-(topo|baixo)\.png', lambda m: f'Selo de papel: a face {m[1]} (15 × 16 mm) como aparece montada no maço, só revisão.'),
    (r'PULSEIRA\.json', 'A PULSEIRA: medidas, fonte e repetições.'),
    # facas
    (r'FACA_COPO-200_zona-impressao\.svg', 'Copo 200 g desenrolado: zona de impressão, painéis, lacunas e emenda.'),
    (r'FACA_COPO-080_zona-impressao\.svg', 'Copo 80 g (O SINGLE) desenrolado: zona de impressão, painéis, lacunas e emenda.'),
    (r'FACA_CARTUCHO_96x96x98\.svg', 'Faca do cartucho O INGRESSO (corte, vinco, sangria).'),
    (r'FACA_CARTUCHO_74x74x76\.svg', 'Faca do cartucho O INGRESSO SINGLE (corte, vinco, sangria).'),
    (r'FACA_CARTUCHO_74x74x82\.svg', 'Faca do cartucho do refil NOVA TEMPORADA (corte, vinco, sangria).'),
    (r'FACA_CASE_base-130x130x102\.svg', 'Faca do forro da base do case, fenda do fecho e inserto de EVA.'),
    (r'FACA_CASE_tampa-130x130x30\.svg', 'Faca do forro da tampa do case e da aba do fecho.'),
    (r'FACA_SETLIST_105x400\.svg', 'Faca da setlist: dobras e picotes.'),
    (r'FACA_PULSEIRA_selo-60x15\.svg', 'Faca do selo de papel da pulseira, com o mapa dos painéis ao longo da tira (vincos, TOPO, BAIXO, colagem).'),
    (r'FACA_ETIQUETA-LOTE_(\d+x\d+)\.svg', lambda m: f'Faca da etiqueta de lote {m[1]} mm.'),
    (r'FACA_TAMPA_(\d\d)\.svg', lambda m: f'Desenho da tampa Ø{m[1]}: área útil, aba, anel de vedação e as fitas.'),
]

INTRO = """# 02_PRODUTO · LEIA-ME

Tudo aqui foi gerado por código em `_build/pack/` (um comando refaz tudo:
`/home/user/venvs/web/bin/python _build/pack/tudo.py`). Cores exatas da plataforma, sRGB.
`renders/` é das equipes de 3D e não está nesta lista.

"""

SECTIONS = [('rotulos', 'Rótulos do copo'), ('tampa', 'Tampa-palco'), ('base', 'Fundo do copo e etiqueta de lote'),
            ('case', 'O CASE'), ('cartucho', 'Cartuchos: O INGRESSO, O INGRESSO SINGLE e refil NOVA TEMPORADA'), ('refil', 'Refil NOVA TEMPORADA'),
            ('setlist', 'A SETLIST'), ('pulseira', 'A PULSEIRA'), ('facas', 'Facas e desenhos técnicos')]


def describe(name):
    for pat, d in RULES:
        m = re.fullmatch(pat, name)
        if m:
            return d(m) if callable(d) else d
    return None


def main():
    out = [INTRO]
    missing = []
    for folder, title in SECTIONS:
        p = os.path.join(PROD, folder)
        if not os.path.isdir(p):
            continue
        out.append(f'## {folder}/ · {title}\n')
        for f in sorted(os.listdir(p)):
            if f.startswith('.') or f == 'LEIA_ME.md':
                continue
            d = describe(f)
            if d is None:
                missing.append(f'{folder}/{f}')
                d = '(sem descrição)'
            out.append(f'- `{f}` — {d}')
        out.append('')
    with open(os.path.join(PROD, 'LEIA_ME.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))
    if missing:
        print('NO DESCRIPTION:', missing)
    print('LEIA_ME.md written')


if __name__ == '__main__':
    main()
