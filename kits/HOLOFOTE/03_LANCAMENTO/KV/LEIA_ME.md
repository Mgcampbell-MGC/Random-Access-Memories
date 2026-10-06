# 03_LANCAMENTO/KV · MÃE AO VIVO (§E.1)

Peças finais com tipo. O tipo é posto por código sobre o render limpo (nenhum pixel gerado, nenhuma edição por IA depois
da composição, nenhuma placa de IA — decisão da dona, 6 out 2026). Os renders limpos estão em `02_PRODUTO/renders/`.

| Arquivo | O que é |
|---|---|
| `KV-01_9x16.png` | KV-01 orgânico 1080 × 1920: a vela AO VIVO acesa no X, sozinha no spot; o lineup em cima (HOLOFOTE APRESENTA · A TURNÊ · 2027 / MÃE / AO VIVO / DOMINGO · 09.05 · abertura: você), a linha de segurança e "holofote nela." |
| `KV-01_4x5.png` | O mesmo KV no feed 1080 × 1350, câmera própria (copo 351 px, topo em y 677), tipo reposto na medida 140–940. |
| `KV-01_1x1.png` | O mesmo KV 1080 × 1080 (copo 260 px, topo em y 590), tipo reposto na medida 180–900. |
| `KV-01_16x9.png` | Herói do site 1920 × 1080: lineup à esquerda (160–1000), vela à direita (copo 410 px, centro x 1420). |
| `KV-45_aceso_SUA-VEZ.png` | KV-45 (o quadro de produto dos 9–15 s): vela acesa, título SUA VEZ., "holofote nela." e a linha de segurança. |
| `KV-45_aceso_A-ATRACAO-E-ELA.png` | O mesmo, com o título A ATRAÇÃO É ELA. |
| `KV-45_aceso_sem-titulo.png` | O mesmo, só com "holofote nela." e a linha de segurança. |
| `KV-45_apagado_*.png` | As mesmas três versões sobre o plano com a vela apagada. |

Como refazer: `_build/shots/blender.sh _build/shots/campanha.py -- KV01_9x16 KV01_4x5 KV01_1x1 KV01_16x9` (renders) e
`/home/user/venvs/web/bin/python _build/shots/pecas_finais.py KV01 KV45 PORTAO` (tipo + portão da chama).

Notas:
- O tipo do KV-01 é a camada exata do diretor (`_build/kv/kv.html`). A linha de segurança *nunca deixe a vela acesa sem
  supervisão.* foi acrescentada como camada própria (a plataforma §D.8.6 pede essa linha em todo post com vela acesa e
  a camada do KV não a tinha), no chão escuro entre a poça e a assinatura, fora da poça.
- Portão de legibilidade da chama (§D.6) refeito no KV-01 9:16 final: ver `06_PRODUCAO/fidelidade/KV-01_9x16_portao-chama.json`.
- Fidelidade do rótulo de cada render: `06_PRODUCAO/fidelidade/KV-01_<formato>_limpo.json` e `KV-45_*.json`.
- KV-45: os seis arquivos foram montados sobre os planos finais do diretor (`KV-45_apagado` das 10:53 e `KV-45_aceso`
  das 11:50, já com a chama final). Os dois planos são renderizados a 2× e reduzidos 2 × 2; o relatório de
  verificação é o do render 2× (`KV-45_aceso.json`: pior ladrilho 0,934, p5 0,962, matiz −1,29°, saturação 0,999,
  controle plantado pego) e o 1× fica como `KV-45_*_1x_informativo.json`. As versões apagadas também levam a linha de
  segurança, como as acesas (a mesma camada de tipo nas seis).
- Chama: todos os KV-01 acesos foram refeitos com a chama final do diretor (holofote.py, terceira passada, 6 out:
  corpo luminoso, azul só na borda da base, pavio carbonizado mais escuro).
