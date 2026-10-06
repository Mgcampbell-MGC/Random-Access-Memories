# 01_MARCA · HOLOFOTE

Tudo aqui sai de código em `_build/brand/`. Fonte da verdade: `00_estrategia/CREATIVE_PLATFORM.md` §A, §D, §E.
Python: `/home/user/venvs/web/bin/python`. Os comandos abaixo rodam da raiz do kit (`kits/HOLOFOTE/`).

## O que tem em cada pasta

| Pasta / arquivo | O que é |
|---|---|
| `logo/*.svg` | Wordmarks e O FOCO, gerados por `_build/logo.py`. No papel, no amarelo e no laranja o O aceso é PRETO (`preto-sobre-papel`, `preto_transparente` = o mono). O FOCO num quadrado 1200 × 1200 centrado pela área: disco d, vão 1,2 d, poça 3,2 d × 0,5 d (revisão do CCO, 6 out 2026). |
| `logo/png/` | Os mesmos SVGs em PNG (logo 2400 px de largura, O FOCO 1200 × 1200), fundo transparente onde o SVG é transparente. |
| `marca/A-MARCA_X_s927.*`, `A-MARCA_X_s4.*` | A MARCA, o X de fita gaffer: PNG 2048 transparente, versão sobre preto, SVG vetorial e JSON com a geometria das tiras. |
| `marca/A-TIRA_s31.*` | Uma fita só (o pedaço da tampa, "ela fica aqui."), mesmos formatos. |
| `lambe/LAMBE_<LxA>_s<n>_*.png` | O LAMBE em camadas soltas: `grao`, `rugas`, `borda` (alfa rasgado), `altura16` (16 bits). Tamanhos 1080×1080, 1080×1350, 1080×1920, 2000×3000. |
| `cartazes/` | Os 12 cartazes da parede (2000 × 3000) com O LAMBE, mais `3d/` (albedo + altura) e `cartazes.json`. Ver `cartazes/PRONTO.txt`. |
| `livro/LIVRO-01…16_*.png` | O livro da marca, 16 pranchas 1920 × 1080. |
| `placeholders.json` | Onde entram os renders nas pranchas: `"arquivo.png"` ou `"arquivo.png::ID"` → `[x, y, w, h]` em px. |

## Os geradores (para os outros times reaproveitarem)

### A MARCA · o X de fita gaffer · `_build/brand/marca.py`
Duas tiras a ±45°, 3,75 : 1, pontas rasgadas à mão, trama, uma ponta descolando, sombra. Tudo pela semente.
```
python _build/brand/marca.py --png saida.png --svg saida.svg --tamanho 2048 --semente 927
python _build/brand/marca.py --png fita.png --uma --angulo -7 --semente 31      # uma fita só
```
Opções: `--razao 3.75`, `--fios 40`, `--cor amarelo`, `--fundo transparente|preto|papel|<hex>`, `--sem-sombra`.
O JSON ao lado dá centro, ângulo, comprimento e largura de cada tira (para escrever ao longo da fita).
Uma por quadro.

### O LAMBE · papel colado na parede · `_build/brand/lambe.py`
Separa as tintas da arte chapada, tira cada chapa de registro (1–2 px) com uma batida fantasma de 1–2 px na preta, dá
falha de tinta, grão de papel, rugas de cola (vincos, vincos direcionais, bolhas pequenas), marcas de pincel e borda
rasgada com o miolo do papel em fibra (6–12 px). `folga_tinta=40` mantém todo rasgo de borda a ≥ 40 px dos glifos. A semente muda tudo; use uma por peça.
```
python _build/brand/lambe.py aplicar arte_chapada.png saida.png --papel amarelo --semente 7 \
       [--rasgo 0.3] [--rugas 1.0] [--registro 2] [--sem-borda] [--albedo alb.png] [--altura alt.png]
python _build/brand/lambe.py overlays 1080x1350 --semente 7 --pasta 01_MARCA/lambe/
```
`--papel` é a cor do papel (amarelo, rosa, laranja, violeta, papel, preto). Pixels que não são mistura de duas cores
da paleta (uma foto, um render) não perdem a cor: só ganham o papel e as rugas por cima.
Em Python também: `lambe.aplicar(img, papel, semente, idade=0.6)` (cartaz antigo, desbotado),
`lambe.buraco(...)`, `lambe.rasgo_linha(...)` e `lambe.rasgado(topo, antigo, ...)` (cartaz rasgado sobre o antigo).

**Receita de composição com as camadas soltas** (quando não dá para rodar o `aplicar`, ex.: no editor de vídeo):
1. Arte chapada embaixo, nas cores exatas.
2. Deslocar a chapa preta 1–2 px numa direção qualquer (o fora de registro). Só a preta.
3. `…_grao.png` por cima em **sobreposição (overlay)** a 100 %. Cinza 50 % é neutro.
4. `…_rugas.png` por cima em **luz suave (soft light)** a 100 %.
5. `…_borda.png` como **máscara de alfa** da peça (borda rasgada). Em peça sangrada, pular.
6. No 3D: `…_altura16.png` em deslocamento (amplitude total ~0,6 mm, midlevel 0,5) e nada das etapas 3–4,
   porque a luz da cena faz as rugas.

### O CARTAZ · o cartaz lambe-lambe por dados · `_build/brand/cartaz.html`
HOLOFOTE APRESENTA / atração / show / data / abertura (+ a lista da turnê, opcional). Qualquer cor de faixa, qualquer
tamanho; toda linha enche a medida (§D.5 regra 2) medindo na tinta; a atração passa pela escada de encaixe do §C.10
(até recusar com "esse nome não cabe no cartaz. tenta um apelido?"); coração ♥ desenhado em vetor. Sai chapado;
O LAMBE entra depois.
```
python _build/brand/render.py _build/brand/cartaz.html saida.png 2000x3000 \
  '{"W":2000,"H":3000,"cor":"rosa","headliner":"DONA CIDA","show":"AO VIVO","abertura":"você"}'
```
Campos: `W`, `H`, `cor`, `headliner`, `coracao` (true/false), `show` (padrão = o show da faixa), `data`, `abertura`,
`apresenta` ([esq, dir]), `turne` ({titulo, linhas:[[local, status]…]}), `rodape` ("assinatura" ou {esq, dir}),
`caixaY` ([y0, y1], a zona segura), `margem` ({x, t, b} em frações), `lamp` (cor do O aceso). Modo `itens` = pilha livre
de linhas (é como saem o C01 e os cartazes curtos; ver `cartazes.py`).
Os 12 cartazes da parede: `python _build/brand/cartazes.py` (ou `… cartazes.py 07 08` para alguns).

### O INGRESSO · `_build/brand/peca.html`, receita `ingresso`
O ingresso com canhoto, picote e meias-luas: INGRESSO · atração · show · SETOR: PRIMEIRA FILA · ASSENTO: O DE SEMPRE ·
DOMINGO 09.05 · ADMITE 1 · ATRAÇÃO · código de barras fictício. Sai em fundo transparente; `lancamento.py` faz o papel
cartão, o rasgo do picote e o canhoto solto (D02).
```
python _build/brand/render.py _build/brand/peca.html ingresso.png 1080x1350 \
  '{"receita":"ingresso","cor":"amarelo","headliner":"MAINHA"}' --transparente
```

### O BOLETIM · `_build/brand/peca.html`, receita `boletim`
O cartão das 06:03: BOLETIM DA TURNÊ · data · 06:03, o lineup, a linha do dia (a Produção, cada linha enchendo a
medida), os três sinais nos dias 7, 8 e 9, a assinatura. Formatos `1x1` e `9x16`.
```
python _build/brand/render.py _build/brand/peca.html b.png 1080x1080 \
  '{"receita":"boletim","formato":"1x1","cor":"rosa","data":"03.05","linhas":["bom dia. a atração já","confirmou presença. e você?"]}'
```
As quebras da linha do dia são escolhidas à mão para equilibrar os comprimentos; a frase não muda (o script confere).

### As outras receitas de `pecas.js`
`C03`, `C07`, `C09` (o gerador de cartaz em 9:16, `headliner`, `turne`, `abertura`), `D01` (a carteirinha: `headliner`,
`anos`, `cor`, `foto`), `stk` (`v` = nome da figurinha). Tudo roda por `lancamento.py`.

## Como refazer tudo
```
python _build/brand/metricas.py      # tabela de métricas dos glifos (só se as fontes mudarem)
python _build/brand/wordmark.py      # contornos do wordmark para os templates (só se o logo mudar)
python _build/brand/exportar.py      # marca/, lambe/, logo/png/
python _build/brand/cartazes.py      # cartazes/ (≈2 min, 2 processos)
python _build/brand/lancamento.py    # 03_LANCAMENTO/B, C, D, STK (≈2 min)
python _build/brand/livro.py         # livro/ + placeholders.json (depende dos três de cima)
```

## Observações honestas
- **Largura do logo.** O §D.3 diz "largura = 9,273 × versal". Com o arquivo oficial da Expanded One, tracking −10 e
  kerning ligado, a medida dá **8,90 × versal na tinta** e **9,03 × versal no avanço** (o `logo.py` já avisava). A
  prancha 05 mostra o valor medido. Os SVGs aprovados não foram tocados. **Precisa de decisão do ECD.**
- **Respiro.** Os SVGs aprovados usam a versal (710) como respiro; a prancha desenha a altura do O (734), como diz o
  §D.3. Diferença de 3 %.
- **Eixo wdth da linha 3.** Resolvido na tinta, o motor dá CAMARIM 104, MAIS UM! 110, ACÚSTICO 100; o §C.2 (medido no
  avanço) dá 106, 111, 102. A prancha 10 mostra os dois.
- **O aceso.** Decidido pelo diretor (6 out 2026, §D.1 vence §D.3): amarelo no preto, no rosa e no violeta; PRETO no
  amarelo, no laranja (amarelo nunca encosta no laranja) e no papel (amarelo sobre papel é par "Nunca", 1,18:1).
  Regra no código: `lampDe` em `pecas.js`, `lamp` em `cartaz.html`, `ways` em `_build/logo.py`.
- **O FOCO.** Redesenhado na revisão do CCO (6 out 2026): o desenho do §D.3 (vão 0,5 d, poça 2,4 × 0,8 d) lia como o
  ícone genérico de usuário a 16–32 px. Agora: vão 1,2 d, poça 3,2 d × 0,5 d, num quadrado centrado pela área com a
  tinta dentro de 84 % do raio (o recorte redondo do avatar nunca corta). A pulseira (time de embalagem) não mudou.
- **"Nunca deixe a vela acesa sem supervisão."** entra em C03 e C07 porque mostram a vela acesa (§D.8.6).
