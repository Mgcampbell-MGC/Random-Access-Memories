"""Every consumer-facing string on the HOLOFOTE pack, copied character for character from
00_estrategia/CREATIVE_PLATFORM.md (LOCKED). The art and the label_copy.json files both read from here, so a string
can only ever be wrong in one place."""

C = dict(preto='#121014', papel='#FFF8EC', amarelo='#FFE81A', rosa='#FF4FA0', laranja='#FF6A1A',
         violeta='#8424F5', luz='#FFE9C4', cera='#F3E9D6', croma='#0047BB')

# §B.1 / §B.2 / §C.2 per SKU
SKUS = {
    '01': dict(sku='HLF-01-200', faixa='01', show='CAMARIM', wdth=106, descriptor='pó de arroz e batom',
               coating='rosa', ink='preto',
               inci=['ALPHA-ISOMETHYL IONONE', 'COUMARIN'], pt=['alfa-isometil ionona', 'cumarina']),
    '02': dict(sku='HLF-02-200', faixa='02', show='AO VIVO', wdth=125, descriptor='rosas no palco, luz quente',
               coating='amarelo', ink='preto',
               inci=['LIMONENE', 'LINALOOL', 'CITRONELLOL', 'GERANIOL'],
               pt=['limoneno', 'linalol', 'citronelol', 'geraniol']),
    '03': dict(sku='HLF-03-200', faixa='03', show='MAIS UM!', wdth=111, descriptor='laranja, cacau e mais um pouco',
               coating='laranja', ink='preto',
               inci=['LIMONENE', 'LINALOOL', 'COUMARIN'], pt=['limoneno', 'linalol', 'cumarina']),
    '04': dict(sku='HLF-04-200', faixa='04', show='ACÚSTICO', wdth=102, descriptor='voz e violão, luz baixa',
               coating='violeta', ink='papel',
               inci=['LIMONENE', 'LINALOOL'], pt=['limoneno', 'linalol']),
}

# §C.2 front panel
L1_LEFT = 'HOLOFOTE APRESENTA'
L1_RIGHT = 'A TURNÊ · 2027'
L4_LEFT = 'DOMINGO · 09.05'
L4_RIGHT_PREFIX = 'abertura: '
OPENING_DEFAULT = 'você'
L6_LEFT = 'vela aromática'
L6_RIGHT_CAPS = 'PESO LÍQUIDO '
L6_RIGHT_FIG = '200 g'
NET_WEIGHT = '200 g'

# §C.3 back panel
B1 = 'ELA ESTEVE EM TODAS.'
B2_LEFT = 'TURNÊ \u201cVOCÊ\u201d'   # director's decision 6 Oct 2026 (platform: «VOCÊ»); see B2_FIX
B2_RIGHT = 'DESDE O PRIMEIRO DIA'
ESTREIA_RETAIL = 'ESTREIA · O DIA EM QUE VOCÊ NASCEU'
ESTREIA_STATUS = 'QUEM FEZ O SHOW FOI ELA'
TOUR = [  # lines 2..8 (line 1 is ESTREIA)
    ('PREZINHO, DIA DAS MÃES', 'PRIMEIRA FILA'),   # director's decision 6 Oct 2026; see TOUR_FIX
    ('FESTA JUNINA', 'O BIGODE FOI ELA'),
    ('FEIRA DE CIÊNCIAS', 'O VULCÃO TAMBÉM'),
    ('PRONTO-SOCORRO, 3H', 'SEM INGRESSO. ENTROU.'),
    ('FORMATURA', 'DE PÉ (COM O DEDO NA LENTE)'),
    ('PRIMEIRO APÊ', '4 VIAGENS DE CARRO'),
    ('09.05.2027', 'A ATRAÇÃO É ELA'),
]
# director's decisions after the copy/compliance review (6 Oct 2026); every file that prints them records them
TOUR_FIX = dict(kind="director's decision", platform='PRÉZINHO, DIA DAS MÃES', used='PREZINHO, DIA DAS MÃES',
                reason='spelling: Lei 5.765/1971 dropped the accent in -zinho derivatives (pé → pezinho, '
                       'pré → prezinho)')
B2_FIX = dict(kind="director's decision", platform='TURNÊ «VOCÊ»', used='TURNÊ \u201cVOCÊ\u201d',
              reason='guillemets are not Brazilian usage: curly double quotes')
ATENCAO = 'ATENÇÃO'
WARNINGS = [  # the five printed lines, bullets included, continuation indented
    '• Nunca deixe a vela acesa sem supervisão.',
    '• Mantenha fora do alcance de crianças e animais.',
    '• Acenda longe de cortinas, tecidos, papéis e correntes de ar,',
    '  sobre superfície firme e resistente ao calor.',
    '• O copo esquenta: não toque nem mova a vela acesa.',
]
B_FULL = 'Advertências completas e modo de uso: ver embalagem externa.'
B_ODOR = 'ODORIZANTE DE AMBIENTE · Perfuma o ambiente com aroma agradável.'

# §C.4 base
PRECISAVA = 'PRECISAVA.'
LOT = 'HLF0927'
FAB = '03/2027'
VAL = '03/2029'
STICKER = ['LOTE HLF0927 · FAB 03/2027 · VAL 03/2029', 'INDÚSTRIA BRASILEIRA', 'PROTÓTIPO FICTÍCIO · NÃO COMERCIALIZAR']

# §C.5 lid
LID_TAPE = 'ela fica aqui.'
LID_BRIM = 'a tampa vira palco.'

# §C.6 wristband
BAND = 'ACESSO TOTAL · ATRAÇÃO · 09.05.27 · HOLOFOTE ·'
SEAL_FRONT = 'pode rasgar.'
SEAL_BACK = 'o que se guarda é a pulseira.'

# §C.7 O CASE
CASE_NO = 'CASE Nº 09.05'
CASE_CAMARIM = 'CAMARIM 1 · '  # + headliner
CASE_LID_FRONT = 'acesso restrito'
CASE_FRONT_SHOW = 'HOLOFOTE · '  # + show name
CASE_FRAGIL = 'FRÁGIL · ESTE LADO PRA CIMA ↑'
CASE_UNDER = 'O copo é seu.'   # director's decisions rounds 2–3 (the disposal block says the rest), see CASE_UNDER_FIX
CASE_BINS = ['papel', 'plástico', 'vidro', 'metal']
CASE_MIRROR = 'olha a atração.'
RIDER_HEAD = 'RIDER DA ATRAÇÃO · TURNÊ DIA DAS MÃES 2027'
RIDER = [
    ('camarim', 'o sofá dela'),
    ('exigências', 'nenhuma (ela vai dizer)'),
    ('bis', 'obrigatório'),
    ('água', 'ela vai perguntar se você bebeu'),
    ('som', 'ela canta junto. deixa.'),
    ('luz', 'uma vela. o menor holofote do brasil.'),
    ('equipe técnica', 'você'),
]
BARCODE = 'CÓDIGO DE BARRAS FICTÍCIO'


def manifesto(faixa, ver='case'):
    s = SKUS[faixa]
    inci = ', '.join(['HYDROGENATED COCONUT OIL', 'HYDROGENATED SOYBEAN OIL', 'PARFUM'] + s['inci']) + '.'
    pt = ', '.join(['óleo de coco hidrogenado', 'óleo de soja hidrogenado', 'fragrância'] + s['pt']) + '.'
    last_ver = ('Modo de uso e advertências completas: ver lateral e SETLIST no interior.' if ver == 'case'
                else 'Modo de uso e advertências completas: ver lateral.')
    return [
        'MANIFESTO DE CARGA · TURNÊ DIA DAS MÃES 2027',
        f'CONTEÚDO: HOLOFOTE {s["show"]} — vela aromática · ODORIZANTE DE AMBIENTE',
        'PESO LÍQUIDO 200 g',
        'COMPOSIÇÃO / INGREDIENTS (INCI): ' + inci,
        'Ingredientes (português): ' + pt + ' Pavio de madeira. Cápsula de alumínio.',
        '(Alérgenos da fragrância declarados na composição acima.)',   # no regulation number: RDC 1.029/2026 is UNVERIFIED
        'Fabricado e distribuído por: PALCO PEQUENO INDÚSTRIA DE VELAS LTDA. (EMPRESA FICTÍCIA)',
        'CNPJ 00.000.000/0001-00 (FICTÍCIO)',
        'Rua do Palco, 0 — Bairro Fictício — São Paulo/SP — CEP 00000-000 (ENDEREÇO FICTÍCIO)',
        'AFE Anvisa nº 0.00000-0 · Processo Anvisa nº 25351.000000/0000-00 (FICTÍCIOS)',
        'SAC 0800 000 0000 · sac@holofote.exemplo · holofote.exemplo (FICTÍCIOS)',
        'INDÚSTRIA BRASILEIRA',
        'LOTE: ver base do copo · FAB 03/2027 · VAL 03/2029 (FICTÍCIOS)',
        last_ver,
        'PROTÓTIPO FICTÍCIO · DADOS FICTÍCIOS · NÃO COMERCIALIZAR',
    ]


# director's decisions after the copy/compliance review (6 Oct 2026), recorded in every JSON that prints them
DD = "director's decision"
MODO_FIX = dict(kind=DD, platform='Use a vela dentro do copo, sobre a tampa virada ou sobre superfície plana, firme e '
                'resistente ao calor.', used=None, reason='the old line read as if the candle could stand outside the '
                'glass: it is always used inside the glass, and the glass stands on the lid or a flat surface')
CASE_UNDER_FIX = dict(kind=DD, platform='O case é de papel. O copo é seu.', used=None,
                      reason='false as written: the case also has EVA, a PMMA mirror, magnets, a polyester band and a '
                             'plastic clasp. Round 3: "O resto, separe: papel, plástico e metal." dropped as redundant: '
                             'the disposal block (CASE · PAPEL, PLÁSTICO E METAL · SEPARE …) says it')
CT_TOP_FIX = dict(kind=DD, platform='ESTE LADO PRA CIMA ↑', used=None,
                  reason='an arrow is meaningless on a horizontal panel; the words stay')
ALERG_NOTE = '— exemplo; confirmar com o certificado do fornecedor da fragrância.'
ALERG_FIX = dict(kind=DD, platform='(Alérgenos de fragrância declarados conforme RDC Anvisa nº 1.029/2026 — exemplo; '
                 'confirmar com o certificado do fornecedor da fragrância.)',
                 used='(Alérgenos da fragrância declarados na composição acima.)',
                 reason='internal note removed from every printed panel; the regulation number is not printed because no '
                        'Anvisa RDC 1.029/2026 could be verified (search, 6 Oct 2026): an unverified citation never goes on pack',
                 note_kept_in_json=ALERG_NOTE)
INGREDIENT_BREAK = dict(kind=DD, reason='ingredient lists break only after a comma (or after the list\'s colon), never '
                        'inside a name: HYDROGENATED SOYBEAN OIL, alfa-isometil ionona stay whole')


# §C.8 SETLIST
SETLIST_P1 = ['SETLIST', 'DOMINGO · 09.05 · CAMARIM 1', '(ela abre. você acende.)']
RUN_OF_SHOW = [  # (number, step lines, who or None)
    ('1.', ['tira a pulseira do case e põe no pulso'], 'ela'),
    ('2.', ['abre o case'], 'ela'),
    ('3.', ['olha no espelho'], 'ela'),
    ('4.', ['tampa na mesa, X pra cima: isso é o palco'], 'você (equipe técnica)'),
    ('5.', ['vela em cima do X. mesa firme, longe de', 'cortina, papel e tecido'], 'você'),
    ('6.', ['tira a parte queimada do pavio. deixa uns 5 mm'], 'você'),
    ('7.', ['terceiro sinal: acende', 'primeira vez: deixa derreter até a borda (3 a 4 h).'], 'você'),
    ('8.', ['bis permitido. sessões de até 4 h. temporada de aprox. 40 h.'], None),
    ('9.', ['ninguém sai de perto da vela acesa. nem pra buscar o bolo.'], None),
    ('10.', ['pra apagar: abafador, nunca água. encerra quando restar 1 cm de cera.'], None),
]
SETLIST_BIS = 'BIS: não guarda pra visita. o show é hoje.'
P4_HEAD = 'BIS · 4 INGRESSOS'
TICKETS = [
    ('INGRESSO 01', '1 áudio de 7 minutos, ouvido até o fim.'),
    ('INGRESSO 02', 'avisar quando chegar. sem você pedir.'),
    ('INGRESSO 03', '1 domingo sem celular na mesa.'),
    ('INGRESSO 04', '______________________________'),
]
STUB = 'ADMITE 1 · ELA'
MODO_DE_USO = [
    'MODO DE USO',
    'Na primeira vez, deixe a cera derreter até a borda da cápsula (3 a 4 horas).',
    'Antes de cada uso, retire a parte queimada do pavio de madeira, deixando cerca de 5 mm.',
    'Não queime por mais de 4 horas seguidas. Deixe esfriar antes de acender de novo.',
    'Para apagar, use um abafador. Não use água.',
    'Encerre o uso quando restar cerca de 1 cm de cera no fundo.',
    'Use a vela sempre dentro do copo. Apoie o copo sobre a tampa virada ou sobre superfície plana, firme e '
    'resistente ao calor.',   # director's decision 6 Oct 2026, see MODO_FIX
]
ADVERTENCIAS = [
    'ADVERTÊNCIAS',
    'Produto destinado exclusivamente à odorização de ambientes. Não aplicar sobre a pele.',
    'Nunca deixe a vela acesa sem supervisão.',
    'Mantenha fora do alcance de crianças e animais.',
    'Mantenha a pelo menos 30 cm de cortinas, roupas de cama, livros e outros materiais inflamáveis.',
    'Use sobre superfície plana, firme e resistente ao calor. Mantenha o ambiente ventilado.',
    'Não mova a vela acesa ou com a cera ainda líquida. O copo e a cápsula ficam quentes durante e após o uso.',
    'Evite contato com os olhos e mucosas. Em caso de contato, lave com água em abundância.',
    'Não ingerir.',
]
DEPOIS = [
    'DEPOIS DA TEMPORADA',
    'A temporada acabou. O copo fica.',
    'Com tudo frio, retire a cápsula pela borda. Lave o copo com água morna e sabão.',
    'Nova temporada: encaixe uma cápsula de refil HOLOFOTE 200 g no copo limpo.',
    'Ou use o copo pra pincéis, canetas ou flores. Não use o copo para bebidas ou alimentos.',
    'Descarte a cápsula vazia na coleta de metais.',
]
TICKET_BACK = 'SETOR: PRIMEIRA FILA · ASSENTO: O DE SEMPRE · VALIDADE: VITALÍCIA · emitido por: você'
P1B_HEAD = 'REGRAS DA CASA · MODO DE USO'

# §C.9 carton O INGRESSO
CT_FRONT = dict(ingresso='INGRESSO', platform='MÃE AO VIVO', date='DOMINGO · 09.05', setor='SETOR: PRIMEIRA FILA',
                stub='ADMITE 1 · ATRAÇÃO')
CT_SIDE2 = ['holofote nela.', 'ela vai dizer "não precisava". é a sua deixa.']
CT_TOP = 'ESTE LADO PRA CIMA'   # director's decision 6 Oct 2026 (platform: '… ↑'), see CT_TOP_FIX

# §C.9 refill
REF_LID = ['NOVA TEMPORADA', 'PESO LÍQUIDO 200 g', 'vela aromática · refil', 'Use dentro do copo HOLOFOTE.']
REF_BAND = 'LOTE HLF0927 · FAB 03/2027 · VAL 03/2029'

TAGLINE = 'holofote nela.'

# the director's-decision records carry the string actually printed
MODO_FIX['used'] = MODO_DE_USO[-1]
CASE_UNDER_FIX['used'] = CASE_UNDER
CT_TOP_FIX['used'] = CT_TOP

# ---------------------------------------------------------------------------------------------------------------------
# Round 3, director's decisions after the CCO visual review (6 Oct 2026)
# 1. disposal: code-set Produção caps lines in the brand voice replace the clip-art bin pictograms
DISPOSAL_CT = ['CARTUCHO · PAPEL · RECICLE', 'COPO · VIDRO · FICA', 'CÁPSULA · ALUMÍNIO · RECICLE']
DISPOSAL_REF = ['CARTUCHO · PAPEL · RECICLE', 'CÁPSULA · ALUMÍNIO · RECICLE']      # a refill has no glass
DISPOSAL_CASE = ['CASE · PAPEL, PLÁSTICO E METAL · SEPARE', 'COPO · VIDRO · FICA', 'CÁPSULA · ALUMÍNIO · RECICLE']
DISPOSAL_FIX = dict(kind=DD, platform='disposal pictograms (generic bins) + material names',
                    reason='clip-art bins replaced by code-set Condensed One caps lines in the brand voice, one per '
                           'material; "O copo fica" is the brand\'s own idea, so the disposal block says it')
# 3. the Locutor (Expanded / wght 700 display) is set in CAPITALS everywhere except the lockup "holofote nela."
LOCUTOR_CAPS = dict(kind=DD, reason='Locutor lines are capitals everywhere except the lockup "holofote nela."; lower '
                                    'case only in Shantell (the Fã) or Condensed One at 0 tracking (the Produção)')
BODY_PRODUCAO = dict(kind=DD, platform='body text in Special Gothic wght 400 (sentence case)',
                     used='Special Gothic Condensed One, sentence case, tracking 0 (the Produção)',
                     reason='lower case is allowed only in Shantell or Condensed One at 0 tracking')
ADMITE_BACK = 'ADMITE 1'      # round 3: the ticket backs on the setlist read as tickets
