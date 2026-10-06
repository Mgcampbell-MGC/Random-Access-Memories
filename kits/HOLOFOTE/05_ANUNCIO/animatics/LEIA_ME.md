# HOLOFOTE · O ANÚNCIO · animatics (previs)

Os 8 mestres do anúncio (plataforma §F) em **previs**: manequins cinza no auditório 3D (A ESCOLA) no lugar das
pessoas, com o tempo exato do roteiro, a VO temporária, as legendas, a credencial, os títulos, o som e o **bloco
9–15 s de verdade** (o KV-45 aceso do diretor). **Não é o anúncio filmado:** as tomadas de H01 e H02 ainda serão
geradas pela Sol e entram no lugar dos manequins. Nenhuma placa de IA (decisão da dona, 6 out 2026).

## Arquivos

| Arquivo | O que é |
|---|---|
| `HLF-AD-<corte>_<conceito>_animatic_som.mp4` | O mestre com som. 15,0 s, 1080 × 1920, 24 fps, H.264 BT.709, AAC. |
| `HLF-AD-<corte>_<conceito>_animatic_mudo.mp4` | O mesmo quadro a quadro, sem trilha. Toda fala já tem legenda nos dois. |
| `HLF-AD-<corte>_<conceito>_animatic_folha.png` | Folha de contato: quadros em 0,5 / 2,5 / 4,5 / 7,5 / 10 / 14 s, tirados do MP4 entregue. |
| `animatic_tempos.json` | Todos os tempos usados: VO, páginas de legenda, chaves medidas no som, loudness. |

Cortes: **1A 1B 1C** (O PIOR SHOW) · **2A 2B** (PRIMEIRO SINAL) · **3A 3B 3C** (FÃ DE CARTEIRINHA).
Fidelidade do rótulo no bloco 9–15 s: `06_PRODUCAO/fidelidade/ANUNCIO_animatics_KV.json`.

## Linha do tempo (igual nos 8)

- **0,0–6,0 s:** manequim falando (sentado na beira do palco; no anúncio 2, de pé no centro do palco com as mãos
  para trás), credencial em y 560–620, legendas sincronizadas palavra a palavra na faixa y 1000–1240 (palavra
  ativa em amarelo). Gancho com VO a partir de 0,10 s (2B: 0,40 s, "um tempo de silêncio"); corpo a partir de 2,05 s.
- **6,0–9,0 s:** o gesto (corte seco em 6,0) e o título do gesto (Locutor, y 760–860).
  Anúncio 1: quatro palmas, mãos juntas exatamente nos quadros dos transientes medidos (151, 167, 184, 200).
  Anúncio 2: o telefone para cima, balançando (5 posições), no segundo sinal (6,0 s).
  Anúncio 3: coração com os dedos → dedo apontando, que chega no quadro da caixa (180 = 7,5 s).
- **9,0–15,0 s:** KV-45 aceso (render do diretor, nunca refeito aqui), empurrão 100 → 103 % em torno do centro do
  quadro, tipo do KV por código (título, *holofote nela.*, linha de segurança). A legenda da VO (y 300–330) só existe
  no anúncio 2 (*terceiro sinal.*): em 1A–1C (*Sua vez.*) e 3A–3C (*holofote nela.*) a fala já está escrita na tela
  e a legenda sai (decisão do diretor, 6 out 2026). Anúncio 2: preto nos quadros 216–219 (terceiro sinal em 9,0 s) e
  o CLAC acende no quadro 220.

## Enquadramento que as tomadas de pessoas precisam respeitar (medido no previs)

- **Fala (0–6 s):** topo da cabeça abaixo de y 640 (a credencial ocupa y 560–620 a partir de x 120) e queixo acima
  de y 990 (a legenda cobre o peito).
- **Gesto, anúncio 1:** plano médio fechado; queixo acima de y 750 e as mãos batendo palmas abaixo de y 865. O
  título cruza o peito entre os dois.
- **Gesto, anúncio 2:** plano aberto; telefone e cabeça acima de y 750; o título cruza o peito.
- **Gesto, anúncio 3:** câmera girada ~18° para o dedo ler; coração e dedo acima de y 750, o título cruza a
  barriga. Entre o queixo e o coração há só ~10 cm: não cabe um título de 100 px ali.

## Resultados medidos (6 out 2026, KV-45 das 09:05)

- **Arquivos:** 8 × com som + 8 × mudo, 15,000 s, 360 quadros, 1080 × 1920, 24 fps, H.264 marcado BT.709 (codificar.py).
  O mudo é o mesmo quadro a quadro (conferido: os 144 quadros do KV decodificados são idênticos ao com som).
- **Som entregue (AAC decodificado):** −14,10 a −14,16 LUFS integrado; pico real −1,20 a −1,36 dBTP.
- **Sincronia:** palmas nos quadros 151/167/184/200, segundo sinal 144, caixa 180, CLAC 216 (anúncio 2: sino 216,
  CLAC 220), todos medidos na mixagem final (desvio 0,00 quadro).
- **Rótulo no bloco 9–15 s: REPROVADO pela barra de filme** (`06_PRODUCAO/fidelidade/ANUNCIO_animatics_KV.json`).
  Em todo quadro: 5º percentil ≥ 0,96, erro plantado pego, matiz −1,42°, saturação 0,998. Mas o pior bloco cai
  abaixo de 0,80 em 63 dos 144 quadros (mínimo 0,60). O bloco que falha é sempre o fio sob *DOMINGO · 09.05* onde
  ele entra na borda esquerda do copo (x ≈ 240, y ≈ 1330–1390), com só 2–6 % de tinta, que o render quase não
  resolve. Não é o animatic que estraga: o quadro 216 é a placa intacta (só codificada) e já dá 0,799; e a própria
  placa do diretor, sem empurrão nem codificação, cai abaixo de 0,80 em 19 de 64 posições da grade de blocos
  (mínimo 0,41). A placa passa na posição (0, 0) por sorte de grade; qualquer empurrão ou codificação a encontra.
  **A decisão é do diretor** (regra de blocos de fio no verificador, ou a placa); o animatic se refaz com um comando.

## Como refazer

```
TTS=/home/user/venvs/kokoro/bin/python; PY=/home/user/venvs/web/bin/python
cd _build/anuncio
$TTS vo.py _tmp_animatic/vo                                            # VO temporária
for s in SIT_H01 SIT_H02 USHER_H01 CLAP_H01 CLAP_H02 PHONE_H01 HEART_H01 HEART_H02; do
  ../shots/blender.sh animatic_previs.py -- $s --samples 32 --pct 50; done   # placas do previs (540 × 960)
$PY animatic.py camadas som quadros folhas fidelidade audio               # camadas, mix, MP4, folhas, fidelidade, som entregue
```

**Quando o KV-45 for refeito** (placa e AOV novos, tipo do KV talvez em outra altura): rode só
`$PY animatic.py camadas quadros folhas fidelidade audio`. O bloco 9–15 s é recomposto da placa, do `kv.html` e do AOV;
a legenda da VO acompanha a linha de base do título.

`animatic_previs.py -- --medir` imprime onde cabeça, mãos e telefone caem em pixels, sem renderizar.
Os intermediários ficam em `_build/anuncio/_tmp_animatic/` (fora do git).

## O que é provisório

- **A VO** é Kokoro local (pf_dora / pm_alex). Será trocada por voz sintética licenciada; depois disso, rode
  `animatic.py som quadros folhas fidelidade audio` de novo (as legendas são realinhadas na hora).
- **Os manequins** marcam lugar, pose e tempo. Rosto, roupa e luz finais vêm das tomadas geradas.
- **Ninguém ouviu o som.** Foi conferido por números: −14 LUFS integrado; o WAV sai a ≤ −1,6 dBTP para que o AAC
  do MP4, decodificado, fique ≤ −1 dBTP (a −1,0 dBTP no WAV, o AAC passou para −0,72); transientes no quadro.
- **Texto corrigido pelo diretor (6 out 2026):** *Prezinho.* / *DIA DAS MÃES · PREZINHO* sem acento (Lei 5.765/1971);
  *holofote nela.* sempre em caixa baixa, inclusive como fala no roteiro.
