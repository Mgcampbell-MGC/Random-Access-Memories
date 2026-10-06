# 02_PRODUTO/renders · os renders 3D limpos (sem tipo)

Tudo renderizado no Blender (Cycles), nada gerado. Cor: Khronos PBR Neutral, look None, exposição −3,0 (decisão do
diretor). Cada arquivo tem um mestre de 16 bits (`*_16bit.png`) e a cópia entregue de 8 bits sRGB. Os de loja
(`L0n_*_alpha.png`) são transparentes, com a sombra de contato; a foto final com o fundo papel está em `03_LANCAMENTO/L/`.
Cada render com rótulo visível tem o seu relatório de fidelidade em `06_PRODUCAO/fidelidade/<nome>.json`
(nas cenas com vários copos, um relatório por copo: `<nome>__<copo>.json`).

| Arquivo | O que é |
|---|---|
| `KV-45_aceso.png` · `KV-45_apagado.png` | KV-45 do diretor (quadro de produto dos 9–15 s), vela acesa e apagada. |
| `KV-01_9x16_limpo.png` | KV-01 9:16 sem tipo: AO VIVO acesa no X, guinada de 12° à esquerda, O PALCO. |
| `KV-01_4x5_limpo.png` · `KV-01_1x1_limpo.png` · `KV-01_16x9_limpo.png` | O mesmo KV, cada formato com a sua câmera (números da plataforma §E.1). |
| `KV-01_9x16_apagado_portao.png` | Referência apagada (50 %, 32 amostras) só para o portão da chama (§D.6); não é peça. |
| `C01_O-MURO_limpo.png` | C01: a parede de lambe-lambe com flash, as quatro velas apagadas e tampadas no peitoril (01–04). O título é o cartaz 12 na parede. |
| `C02_A-PRIMEIRA-FILA_limpo.png` | C02: do palco da escola, o verso da vela MÃE ♥ (ESTREIA · 03.08.2003 · 14:32) acesa; a primeira fila de cadeiras brancas e a bolsa guardando o lugar do meio. |
| `C04_A-DISCOGRAFIA_limpo.png` | C04: as quatro velas acesas em fila, cada uma no seu foco branco; a setlist colada no chão 60 cm à frente. |
| `C05_O-CASE_1x1_limpo.png` · `C05_O-CASE_9x16_limpo.png` | C05: O CASE aberto visto a 70° de cima no preto; o espelho mostra só o teto e uma lâmpada. |
| `C06_O-MENOR-HOLOFOTE_limpo.png` | C06: blecaute, a chama é a única luz. Verificação do rótulo no passe de albedo. |
| `C06_O-MENOR-HOLOFOTE_neutra.png` | A mesma câmera em luz neutra, só para medir a cor do revestimento (§D.7.3); não é peça. |
| `C08_NOVA-TEMPORADA_limpo.png` | C08: o copo limpo e vazio no X, a cápsula de refil ao lado com a tampa meio aberta. |
| `C10_SALVA-COMO_limpo.png` | C10: reboco no flash, os três copos personalizados apagados: MÃE ♥, DONA CIDA, MAINHA. |
| `L00_FRENTE_alpha.png` … `L07_NOVA-TEMPORADA_alpha.png` | As fotos de loja, transparentes (ver `03_LANCAMENTO/L/LEIA_ME.md`). |
| `_campanha_testes/` | Testes de enquadramento (50 %, 24 amostras). Não são peças. |
| `_sets_tests/` · `_objects_tests/` | Testes das equipes de cenários e objetos. |

Como refazer: `_build/shots/blender.sh _build/shots/campanha.py -- <PLANO …>` (lista dos planos no topo do arquivo).
