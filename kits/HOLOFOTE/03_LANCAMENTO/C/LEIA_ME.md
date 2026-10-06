# 03_LANCAMENTO/C · a série C (§E.2)

| Arquivo | O que é |
|---|---|
| `C01_O-MURO.png` | 4:5. A parede de lambe-lambe no flash duro, os cartazes da marca em grade 4 × 3 (dois rasgados até camadas antigas, uma gota de cola seca); no peitoril de concreto, as quatro velas apagadas e tampadas, 01–02–03–04. O título é o cartaz 12 colado na parede: MÃE AO VIVO. 09.05. INGRESSOS COM VOCÊ. (nenhum tipo por cima). |
| `C02_A-PRIMEIRA-FILA.png` | 4:5. Do palco de uma escola: o verso da vela MÃE ♥ acesa, com a linha ESTREIA · 03.08.2003 · 14:32; lá embaixo, a primeira fila de cadeiras brancas e uma bolsa guardando o lugar do meio. "A vida toda guardando lugar na primeira fila." / "Esse ano, o palco é dela." + linha de segurança e "holofote nela.". |
| `C03_O-PIOR-SHOW.png` | 9:16 (equipe de marca). ELA / APLAUDIU / DE PÉ / O SEU / PIOR / SHOW. em tipo de madeira, a nota da Fã "(girassol, 2007)", o círculo da vela acesa, "Sua vez." + "holofote nela." + linha de segurança. |
| `C04_A-DISCOGRAFIA.png` | 4:5. As quatro velas acesas em fila no palco preto, cada uma no seu foco branco; a setlist colada no chão 60 cm à frente, escrita à mão pela Fã: 1. camarim · 2. ao vivo · 3. mais um! · 4. acústico. "A DISCOGRAFIA DELA." / "(até agora.)" + "holofote nela." e a linha de segurança. |
| `C05_O-CASE_1x1.png` | 1:1. O CASE aberto visto a 70° de cima, no preto: o espelho mostra só o teto e uma lâmpada nua; na espuma, a AO VIVO tampada; a setlist saindo da fenda; a pulseira pela fechadura. "Mãe não tem camarim." / "Agora tem." + "O CASE · com o nome dela · R$179" e "holofote nela.". |
| `C05_O-CASE_9x16.png` | 9:16. A mesma cena com câmera e tipo próprios (nunca recortado do 1:1). |
| `C06_O-MENOR-HOLOFOTE.png` | 4:5. Blecaute: a vela acesa no escuro, a chama é a única luz. "O MENOR HOLOFOTE DO BRASIL." / "Pra maior atração." + linha de segurança e "holofote nela.". |
| `C07_PIX.png` | 9:16, só em 6 de maio (equipe de marca). PIX / NÃO TEM / CHEIRO., miniatura do KV, MÃE AO VIVO · DOMINGO 09.05. Sem marca Pix. |
| `C08_NOVA-TEMPORADA.png` | 4:5. O copo limpo e vazio no X, a cápsula de refil preta ao lado com a tampa de selar meio aberta. "O copo fica." / "A turnê continua." + "refil 200 g · R$79" e "holofote nela.". |
| `C09_O-CARTAZ-DELA_DONA-CIDA.png` | 9:16 (equipe de marca). Saída de exemplo do gerador: DONA CIDA AO VIVO em rosa. |
| `C10_SALVA-COMO.png` | 4:5. Reboco no flash, três copos personalizados apagados no peitoril: MÃE ♥ (amarelo), DONA CIDA (rosa), MAINHA (laranja). "comenta como ela tá salva no seu celular. a gente bota no cartaz." + "holofote nela." (O aceso em preto: amarelo nunca sobre fundo claro, §D.1). |
| `placeholders.json` | Caixas da miniatura da vela em C03 e C07 (equipe de marca). |

As peças de C01–C10 feitas em 3D têm o render limpo em `02_PRODUTO/renders/C0n_*_limpo.png`; o tipo é posto por código
(motor da marca: `_build/shots/tipo_c.html`, composto por `_build/shots/pecas_finais.py C`). Nenhuma placa de IA, nenhum
pixel gerado, nenhuma edição por IA depois da composição. Toda peça com vela acesa leva *nunca deixe a vela acesa sem
supervisão.* (§D.8.6), e nenhum tipo entra na poça de luz (regra 3).

Como refazer: `_build/shots/blender.sh _build/shots/campanha.py -- C01 C02 C04 C05_1x1 C05_9x16 C06 C08 C10` e depois
`/home/user/venvs/web/bin/python _build/shots/pecas_finais.py C`. C03, C07 e C09 saem de `_build/brand/lancamento.py`.

Notas de produção (6 out 2026):
- Todas as peças com vela acesa (C02, C04, C06) foram refeitas com a chama final do diretor (holofote.py, terceira
  passada).
- C06: a especificação não dá guinada ao copo; a −12° do KV, as primeiras letras de HOLOFOTE APRESENTA ficavam no
  limbo esquerdo, onde o albedo do revestimento cai (ladrilho 0,54 no passe de albedo). A −4° o painel fica de frente.
  No blecaute a chama é a única luz e o rótulo fica no contraluz dela; um disco de luz quente minúsculo (`rim_spill`,
  ligado só ao revestimento e à impressão por light linking, sem sombra, invisível à câmera e aos reflexos) devolve um
  pouco da luz da chama à frente do copo — a `flame_spill` da biblioteca não alcança o rótulo (N·L < 0). A
  verificação do rótulo é feita no passe de albedo e numa câmera idêntica em luz neutra (`C06_O-MENOR-HOLOFOTE_neutra`,
  não é peça).
- C08: o copo vazio vai a −6° (no KV é −12°): a −12° "rosas no palco" e "vela aromática" ficavam no limbo. O vidro é
  transparente à sombra do spot só para o próprio vidro: a casca da impressão não projeta sombra (senão cada letra
  desenha uma cópia deslocada de si mesma sob luz dura). Foco no rótulo, f/11.
- C10: enquadramento mais próximo (85 mm a 0,90 m, copos a 92 mm) para que cada copo tenha ~26 % da altura e o tipo
  pequeno de MÃE ♥ seja verificável. O copo amarelo reflete o rosa de DONA CIDA ao lado (efeito real do brilho do
  revestimento); renderizado a 2× e reduzido 2 × 2, verificação no render 2× (relatório de registro
  `C10_SALVA-COMO_limpo__<copo>.json`, 1× em `…_1x_informativo.json`).
- C01, C04 (e L06): os copos ocupam menos de 20 % da altura do quadro — miniaturas, sem alegação de fidelidade (§D.7.5);
  os relatórios existem e trazem `thumbnail_sem_alegacao: true`.
