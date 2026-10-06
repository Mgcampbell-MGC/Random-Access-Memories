"""Writes the ad's machine files (platform §F) into 05_ANUNCIO/: CREATOR_ADS.json, CREATOR_PROMPTS.txt,
SEEDANCE_PROMPTS.txt, PROMPTS_MODELO.json and MODEL_SHEET.json. Same file names as the studio's other kits.

    /home/user/venvs/web/bin/python maquina.py
Strings come from roteiros.json (exact PT from the platform) and the casting text below (platform §F.1/§F.5).
Founder override 6 Oct 2026: NO disclosure plate burned into any ad.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(KIT, '05_ANUNCIO')

H01 = ("Fictional Brazilian adult woman about 25: deep brown skin with visible texture and a few small dark marks on the "
       "cheekbones, bleached platinum buzz cut grown out to about two centimetres with dark roots, strong straight brows, "
       "a small scar through the outer end of the left eyebrow, slightly crooked lower teeth, thin gold wire-rim oval "
       "glasses, smudged black eyeliner, bare skin. A chunky cream hand-knitted cardigan, slightly too big, uneven "
       "stitches, one button missing, over a washed-black crew T-shirt with no print; a plain black woven fabric "
       "festival wristband with a yellow stripe and no lettering; short yellow nail polish chipped at the tips; a single "
       "silver ear cuff on the left ear.")
H02 = ("Fictional Brazilian adult man about 23: light brown skin, black hair in a low fade with a curly top, a thin "
       "patchy moustache he is clearly trying to grow, an expressive mouth, one dimple. His mother's old faded black "
       "nylon bum bag worn crossbody with no logo, an oversized heather-grey crew sweatshirt with no print, the same "
       "plain black woven festival wristband with a yellow stripe and no lettering, a thin silver chain.")
SET = ("Empty Brazilian school auditorium at dusk; behind, a faded pink non-woven fabric backdrop decorated with paper "
       "flowers and paper hearts, absolutely no letters or words; below, rows of white plastic monobloc chairs; "
       "fluorescent tubes off; one warm theatrical spotlight from front-left.")
COMMON_NO = ("Real skin texture, natural asymmetry, believable hands. No product, candle, jar, bottle, label, text, logo, "
             "confetti, smoke, particles, lens flare, glow halo, no blue or purple objects.")
TALK = ("One continuous six-second vertical shot. {who} {set} Camera locked "
        "at eye level, 50 mm perspective, medium shot. She looks straight into the lens, deadpan, and speaks naturally in "
        "Brazilian Portuguese with small, dry eyebrow movement and one small shrug; no big smile until the very end. "
        "{action} {no} 9:16.")
GESTURE = {
    '1': ("she slides off the stage edge, stands, and begins a slow, deadpan clap toward the camera, four claps, face "
          "neutral, then the faintest smile."),
    '2': ("standing centre stage, she raises a phone high with its flashlight on, the back of the phone toward the camera "
          "and mostly hidden in her palm, screen never visible, and sways it slowly side to side, eyes closed for one "
          "second."),
    '3': ("seated on the stage edge, she makes a small finger-heart toward the camera, then turns it into an index finger "
          "pointing at the lens, one eyebrow raised."),
}
HOOK_ACTION = {
    '1A': 'She sits on the edge of a low wooden stage, legs dangling, already mid-look into the lens.',
    '1B': 'She sits on the edge of a low wooden stage, legs dangling, already mid-look into the lens; one eyebrow up.',
    '1C': 'She sits on the edge of a low wooden stage, legs dangling, already mid-look into the lens.',
    '2A': 'She stands centre stage, hands behind her back, like a theatre usher.',
    '2B': 'She stands centre stage, hands behind her back; a beat of silence, then she speaks.',
    '3A': 'She sits on the edge of a low wooden stage, looking at camera like a disappointed tour manager; a slow lean toward the lens.',
    '3B': 'She sits on the edge of a low wooden stage, looking at camera like a disappointed tour manager; a slow lean toward the lens.',
    '3C': 'She sits on the edge of a low wooden stage, looking at camera like a disappointed tour manager; a slow lean toward the lens.',
}
SOUND = {
    '1': {'0-6': 'room tone', '6-9': 'four claps in the empty hall (reverb)',
          '9-15': 'CLAC at 9,0; crackle -> applause; three claps at 13,0'},
    '2': {'0-6': 'one theatre bell under the hook (2A)', '6-9': 'the second bell at 6,0',
          '9-15': 'black 4 f; the third bell at 9,0; CLAC; applause; three claps'},
    '3': {'0-6': 'room tone', '6-9': 'one snare hit on the point', '9-15': 'CLAC -> applause -> three claps'},
}
SLUG = {'1': 'O-PIOR-SHOW', '2': 'PRIMEIRO-SINAL', '3': 'FA-DE-CARTEIRINHA'}
# Framing the previs proved against the ad's fixed type (animatic_previs.py, 1080 x 1920 space). The people layer
# must match it, or the type lands on a face or a hand.
ENQUADRAMENTO = {
    'fala_0_6': ('Rosto entre y 640 e y 990: o topo da cabeça abaixo da credencial (y 560–620, a partir de x 120) e o '
                 'queixo acima da faixa de legendas (y 1000–1240), que cai sobre o peito.'),
    '1': ('Gesto 6–9 s: plano médio fechado; queixo acima de y 750 e as mãos batendo palmas abaixo de y 865; o título '
          'E ELA APLAUDIU DE PÉ. (y 760–860) cruza o peito entre os dois.'),
    '2': ('Gesto 6–9 s: plano mais aberto; o telefone e a cabeça acima de y 750; o título LANTERNA PRA CIMA. '
          '(y 760–860) cruza o peito.'),
    '3': ('Gesto 6–9 s: câmera com ~18° de giro para o dedo ler; o rosto, o coração com os dedos e o dedo apontando '
          'acima de y 750; o título JÁ FOI FÃ DELA? (y 760–860) cruza a barriga. Entre o queixo e o coração há só ~10 cm: '
          'não cabe o título ali.'),
}
REJECT = ["any generated letter (backdrop, clothing, wristband, phone)", "the face changes between talk and gesture takes",
          "extra or fused fingers", "any flame or candle in a presenter scene", "an influencer smile on the hook",
          "waxy skin", "any blue or violet object in a frame with a stand-in", "a recognisable real person or celebrity likeness"]


def who(p):
    w = H01 if p == 'H01' else H02
    return w if p == 'H01' else w


def talk_prompt(p, action):
    t = TALK.format(who=who(p), set=SET, no=COMMON_NO, action=action)
    if p == 'H01':
        return t
    return t.replace('She ', 'He ').replace(' she ', ' he ').replace(' her ', ' his ')


def main():
    os.makedirs(OUT, exist_ok=True)
    R = json.load(open(os.path.join(HERE, 'roteiros.json')))['cortes']
    ads = []
    for cut, r in R.items():
        c = cut[0]
        g = 'She ' + GESTURE[c][4:] if GESTURE[c].startswith('she ') else GESTURE[c]
        g = g[0].upper() + g[1:]
        ads.append({
            'id': cut, 'conceito': r['conceito'], 'apresentador': r['apresentador'],
            'status': ('ANIMATIC PRODUZIDO (previs com manequim, VO temporária) — tomadas de pessoas a gerar. Rótulo do '
                       'bloco 9–15 s NÃO verificado no filme: o verificador reprova blocos de fio de 2–6 % de tinta na '
                       'borda esquerda do copo (ver 06_PRODUCAO/fidelidade/ANUNCIO_animatics_KV.json).'),
            'duracao_s': 15,
            'janelas_s': {'gancho': [0, 2], 'corpo': [2, 6], 'gesto': [6, 9], 'kv': [9, 15]},
            'falado_pt': {'gancho': r['gancho'], 'corpo': r['corpo'], 'kv_vo': r['kv_vo']},
            'na_tela_pt': {'tag_gancho': r['tag'], 'titulo_gesto': r['gesto'], 'headline_kv': r['headline'],
                           'assinatura': 'holofote nela.', 'seguranca': 'nunca deixe a vela acesa sem supervisão.'},
            'som': SOUND[c],
            'prompt_tomada_fala_en': talk_prompt(r['apresentador'], HOOK_ACTION[cut]),
            'prompt_tomada_gesto_en': talk_prompt(r['apresentador'], g).replace(
                'and speaks naturally in Brazilian Portuguese with small, dry eyebrow movement and one small shrug; no big '
                'smile until the very end.', 'silent, no speech.').replace('six-second', 'four-second'),
            'kv_9_15': 'KV-45 aprovado como UMA camada de imagem, empurrão 100 → 103 %; tipo por código na zona y 334–534; '
                       'legenda só da fala de VO em y 300–330. Nunca enviar o KV a um gerador.',
            'audio': 'Voz sintética licenciada em PT-BR, sem imitar ninguém; a VO temporária do animatic é local e '
                     'será substituída. Se o lip-sync falhar, 0–6 s viram VO sobre tomada sem fala, com legendas.',
            'rejeitar_se': REJECT,
            'animatic': {k: '05_ANUNCIO/animatics/HLF-AD-%s_%s_%s' % (cut, SLUG[c], v)
                         for k, v in (('com_som', 'animatic_som.mp4'), ('mudo', 'animatic_mudo.mp4'),
                                      ('folha_de_contato', 'animatic_folha.png'))},
            'enquadramento_pessoas': {'fala_0_6': ENQUADRAMENTO['fala_0_6'], 'gesto_6_9': ENQUADRAMENTO[c]},
            'divulgacao': 'Nenhuma placa de IA na peça (decisão da dona, 6 out 2026). As regras de upload da plataforma '
                          'são outra coisa e devem ser conferidas na hora de publicar.',
        })
    json.dump(ads, open(os.path.join(OUT, 'CREATOR_ADS.json'), 'w'), ensure_ascii=False, indent=1)

    lines = ['HOLOFOTE · O ANÚNCIO · PROMPTS DAS TOMADAS (EN para o gerador; PT nas notas)',
             'Regra: pessoas e cenário SEM produto, SEM vela, SEM letra. O produto entra só no bloco 9–15 s, por código.', '']
    for a in ads:
        lines += [f"=== {a['id']} · {a['conceito']} · {a['apresentador']} ===",
                  f"FALA 0–6 s (PT): {a['falado_pt']['gancho']} / {a['falado_pt']['corpo']}",
                  'TOMADA DE FALA (6 s):', a['prompt_tomada_fala_en'], '',
                  'TOMADA DE GESTO (4 s, usar 3 s):', a['prompt_tomada_gesto_en'], '']
    open(os.path.join(OUT, 'CREATOR_PROMPTS.txt'), 'w').write('\n'.join(lines))

    # generator-ready blocks, one per take, deduplicated (hooks of the same presenter share the gesture take)
    seen, sd = set(), ['SEEDANCE / MANUS · blocos prontos (um por tomada). Copie o bloco inteiro. Sem produto, sem letra.', '']
    for a in ads:
        for kind, key in (('FALA', 'prompt_tomada_fala_en'), ('GESTO', 'prompt_tomada_gesto_en')):
            if a[key] in seen:
                continue
            seen.add(a[key])
            sd += [f"[{a['id']} · {kind}]", a[key], '']
    open(os.path.join(OUT, 'SEEDANCE_PROMPTS.txt'), 'w').write('\n'.join(sd))

    models = {
        'H01': {'nome': 'a fã atrasada', 'idade': 25, 'cortes': ['1A', '1B', '2A', '2B', '3A', '3B'],
                'descricao_en': H01, 'energia': 'Deadpan. Seca e sem pressa; as sobrancelhas trabalham; o calor só aparece na última palavra falada. Nunca tom de influencer, nunca "gente", nunca suspiro.',
                'voz': 'Sintética licenciada, média-grave, paulistana neutra, ~15 caracteres/s; leve sorriso só na última fala. Não imita ninguém.',
                'nunca': 'Nunca diz "eu" sobre um evento de vida, nunca alega ter mãe própria na fala, nunca é cliente.'},
        'H02': {'nome': 'o fã atrasado', 'idade': 23, 'cortes': ['1C', '3C'], 'descricao_en': H02,
                'energia': 'Deadpan, meio tempo mais lento que H01; envergonhado da própria sinceridade.',
                'voz': 'Sintética licenciada, média, paulistana, ~15 caracteres/s.', 'nunca': 'As mesmas regras de fala de H01.'},
        'M01': {'nome': 'a atração', 'idade': 54, 'pecas': ['P01', 'P03'],
                'descricao_en': ('Fictional Brazilian woman about 54: warm medium-brown skin, laugh lines, slight '
                                 'asymmetry; a short tousled dark cut with natural grey at the temples; red-framed '
                                 'reading glasses pushed up on her head; red lipstick; small gold hoops.')},
    }
    portrait = ('Casting reference, photographic, natural light, 4:5. {who} Neutral warm-grey seamless background. '
                '{no} Three frames: (1) head-and-shoulders, straight to camera, deadpan; (2) three-quarter, the same '
                'expression; (3) full-length standing, arms relaxed. Identity identical across the three.')
    prompts = {k: {'retrato_referencia_en': portrait.format(who=v['descricao_en'], no=COMMON_NO)} for k, v in models.items()}
    prompts['M01']['P01_en'] = (
        'Press-photo portrait in hard on-camera flash in her own living room. ' + models['M01']['descricao_en'] +
        ' A black tuxedo blazer with satin lapels over a plain white cotton T-shirt, grey jersey house trousers and plain '
        'black rubber flip-flops. Caught mid-laugh, one hand half covering her mouth, the other raised palm-out as if '
        'saying "para com isso". A beige fabric sofa, two potted plants, a wall clock and a blurred family photo. On a low '
        'wooden coffee table 70 cm in front of her, at 50% across and 70% down the frame, about 13% of frame height: the '
        'whole candle glass including its lid in flat matte chroma blue, no text, no logo, no glare. No other blue object. '
        '4:5.')
    prompts['M01']['P03_en'] = (
        'A real bulb-framed dressing-room mirror with lit bulbs. ' + models['M01']['descricao_en'] +
        ' Putting on red lipstick, smiling at herself in the mirror. No product, no candle, no text, no logo. 4:5.')
    prompts['H01']['P02_en'] = ('Filmed from a stage under one spotlight: ' + H01 + ' alone in the front row of white '
                                'monobloc chairs in the dim empty school auditorium, standing, clapping. No product, no '
                                'text, no logo. 9:16.')
    json.dump(prompts, open(os.path.join(OUT, 'PROMPTS_MODELO.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump({'modelos': models, 'rejeitar_se': REJECT,
               'status': 'Elenco especificado; imagens de pessoas NÃO geradas neste kit (sem créditos aprovados). '
                         'O animatic usa manequins cinza com as silhuetas do elenco.'},
              open(os.path.join(OUT, 'MODEL_SHEET.json'), 'w'), ensure_ascii=False, indent=1)
    print('wrote', len(ads), 'ads →', OUT)


if __name__ == '__main__':
    main()
