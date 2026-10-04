---
name: o-lancamento
description: Produção do O LANÇAMENTO, campanhas para marcas de beleza com a embalagem verdadeira. Leva cenas ao tamanho de entrega (recortar.py), aplica a embalagem da marca sobre cenas geradas com uma embalagem azul (compor.py), confere cada imagem e cada quadro de filme contra a arte aprovada (relatorio_fidelidade.py), e escreve as frases aprovadas ao lado da embalagem (texto.py) e monta filmes simples já em BT.709 (filme.py). Use sempre que a Sol pedir para compor, aplicar a embalagem, conferir, montar ou exportar filme, ou preparar uma entrega.
---

# O LANÇAMENTO — produção

## A regra (nunca quebre)

A IA faz tudo, menos o rótulo.

- A embalagem da marca só aparece de dois jeitos:
  - aplicada por `compor.py` sobre uma embalagem azul;
  - ou como camada própria, intacta, no editor de vídeo.
- **Nunca** use a foto, o PDF, o logo ou o recorte da marca como referência para gerar imagem ou vídeo.
- Nunca peça a um gerador para "desenhar o produto".
- Toda cena gerada leva a embalagem em azul chapado. Use sempre este texto no prompt:
  `the whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare`
- Nenhum texto da marca é gerado. Frases, selos e nome entram como camada de texto. Use só o que está na Ficha de
  Alegações assinada, palavra por palavra.
- Nunca edite, retoque, harmonize ou "melhore" a camada da embalagem. Ajuste o cenário à embalagem, nunca o contrário.
- **Depois de aplicada a embalagem, nenhuma edição por IA na peça** (Design View, editar imagem, upscale por IA,
  remover objeto): esses recursos redesenham a imagem inteira, inclusive o rótulo. Texto e ajustes só por código
  (Pillow) ou Photoshop. Para mudar uma peça pronta, mude a cena e aplique a embalagem de novo.
- Uma peça REPROVADA nunca é entregue.

## Onde rodar

1. **No computador da Sol (Manus Desktop, "My Computer")**, se a pasta `O LANCAMENTO` estiver autorizada.
   - Use as ferramentas de `O LANCAMENTO/_ferramentas/`.
   - Se essa pasta não existir, copie para lá os arquivos de `scripts/` deste Skill.
2. **No sandbox do Manus**, se não houver computador conectado. Use `scripts/` deste Skill.

Antes do primeiro uso em cada lugar:

```
python3 -c "import cv2, numpy, imageio_ffmpeg, PIL" || python3 -m pip install opencv-python-headless numpy imageio-ffmpeg pillow
```

- No Windows, o comando pode ser `python` ou `py` em vez de `python3`.
- Se o `pip` falhar, diga à Sol exatamente qual foi o erro.
- **Autoteste** (quando a Sol pedir, ou depois de instalar): `python3 autoteste.py` na pasta das ferramentas. Tem de
  terminar em `AUTOTESTE: 11/11 OK`. Mostre a tela inteira.
- Não tente outro método de composição.

## Pastas de cada cliente

```
O LANCAMENTO/clientes/<marca>_<produto>/
  00_recebido/   EMBALAGEM.png (recorte com fundo transparente), arte em PDF, fichas, briefing
  01_mundos/     as 3 propostas de mundo
  02_cenas/      cenas geradas com a embalagem azul
  03_pecas/      peças com a embalagem aplicada
  04_filme/      filmes e quadros
  05_entrega/    só o que foi APROVADO, mais relatorio.json
```

## 1. Tamanho certo, antes de compor

Leve cada cena ao tamanho final **antes** de aplicar a embalagem. Assim a embalagem nunca é redimensionada depois.

| Cena | Gere em | Depois rode |
|---|---|---|
| Key visual (vale também para o filme) | 9:16, o maior tamanho possível | `python3 recortar.py CENA.png CENA_9x16.png 1080x1920` |
| 6 imagens de campanha | 4:5 | `python3 recortar.py CENA.png CENA_4x5.png 1080x1350` |
| 3 imagens de loja | 1:1 | `python3 recortar.py CENA.png CENA_1x1.png 1200x1200` |

- No key visual, a embalagem fica **no centro, ocupando de 45% a 50% da altura**. Com mais de 50%, ela não cabe nos
  recortes. Com menos de 45%, a letra miúda borra no movimento do filme e a conferência reprova, com razão.
- Depois de compor o key visual 9:16, tire os outros formatos dele:

```
python3 recortar.py 03_pecas/KV_9x16.png 03_pecas/KV_4x5.png 1080x1350
python3 recortar.py 03_pecas/KV_9x16.png 03_pecas/KV_1x1.png 1080x1080
```

- Esses dois só recortam, sem redimensionar. As máscaras vão junto.
- Se aparecer `AVISO: a peça foi redimensionada`, confira a peça de novo.

## 2. Aplicar a embalagem

`00_recebido/EMBALAGEM.png` só pode vir do arquivo listado na Ficha do Produto assinada. Se a marca mandar uma arte
nova, pare e peça à Sol uma ficha nova. A conferência não enxerga uma única letra parecida trocada em letra miúda. Por
isso o arquivo certo é garantido na origem.

```
python3 compor.py 02_cenas/CENA.png 00_recebido/EMBALAGEM.png 03_pecas/PECA.png
```

- O comando gera `PECA.png`, `PECA.hidden.png` (onde a mão cobre) e `PECA.alpha.png`.
- Se nada estiver na frente da embalagem, use `--sem-oclusao`.
- Se a embalagem ficar pequena ou grande, use `--ajuste largura` ou `--ajuste altura`. Para um ajuste fino, use
  `--escala 0.97`.
- Se o azul for outro tom, use `--matiz` (azul 210, verde 120).
- Se a tampa da cena vier branca ou o azul tiver brilho, **gere a cena de novo**. Não corrija na mão.

## 3. Texto (depois dos recortes, um formato por vez)

```
python3 texto.py 03_pecas/KV_4x5.png 03_pecas/KV_4x5_texto.png --linhas "NOVO|Frase aprovada" --fonte 00_recebido/fonte.ttf
```

- Sempre **depois** de tirar os recortes. Um texto posto no 9:16 é cortado fora no 4:5 e no 1:1.
- A primeira linha sai menor (chamada). As outras são a frase, copiada da Ficha de Alegações.
- A ferramenta escolhe o maior espaço livre acima, abaixo ou ao lado da embalagem. Depois prova que nenhum pixel da
  embalagem mudou; se mudou, não salva.
- Se disser que não há espaço, gere a cena com mais espaço em volta do produto. Não diminua a embalagem.
- Sem `--fonte`, usa uma fonte neutra. Prefira a fonte da marca.
- Peças de loja com fundo branco normalmente vão sem texto.

## 4. Conferir (toda peça, sempre)

```
python3 relatorio_fidelidade.py 00_recebido/EMBALAGEM.png 03_pecas/*.png 04_filme/*.mp4 --json 05_entrega/relatorio.json
```

Responda à Sol com uma tabela, uma linha por peça:

| Peça | Resultado | Pior bloco (mín. 0,80) | Erro plantado detectado | Cor (máx. 2,0) | Escondido pela mão |
|---|---|---|---|---|---|

- No JSON, os campos são: `pass`, `worst_tile`, `control_caught`, `color_drift` (no filme, `max_color_drift`) e
  `hidden_share`.
- Em filmes, confira **todos** os quadros. Nunca use `--every` maior que 1 nem `--sem-controle` numa entrega.

### Se der REPROVADA

| O que aparece | Causa provável | O que fazer |
|---|---|---|
| `found: false` | Embalagem não localizada | Ângulo da cena diferente do recorte. Gere a cena de frente, como a imagem-mestra |
| `worst_tile` baixo num só ponto | Borda, reflexo ou dedo mal recortado | Veja a peça; se for borda, refaça `compor.py` com `--escala` |
| `control_caught: false` | A conferência não ficou sensível nessa peça | A Sol precisa olhar. Não entregue |
| `color_drift` acima de 2 | Cor alterada | Imagem: não mexa na camada da embalagem. Filme: refaça pelo caminho simples (`filme.py`) |
| `hidden_share` acima de 0,35 | Mão cobre demais | Gere a cena com a mão mais baixa |
| Filme: `worst_tile` ≥ 0,80 e `control_caught: true`, mas `worst_p5_tile` abaixo de 0,93 | Um quadro ficou macio no movimento, não é letra errada | Refaça com movimento mais calmo (`--zoom 0.04 --pan 0.02`) e confira de novo. **Nunca baixe o limite** |

## 5. Filme

**Caminho principal: o Video Editor do Manus Studio.**
- O key visual aprovado (`KV_9x16.png`, já com a embalagem e já APROVADA) entra inteiro como camada de imagem.
  Só mova, escale e anime a opacidade dele. Nada de efeito, filtro ou IA sobre essa camada.
- Planos gerados entram só se não mostrarem rótulo legível (chuva, cabelo, rua, mão sem produto).
- Exporte, depois rode a conferência no MP4, todos os quadros, declarando onde a embalagem aparece:
  `--com-embalagem 3-15` (segundos). Quadro dentro desse trecho sem rótulo encontrado reprova o filme.

**Caminho simples, sem editor:**

```
python3 filme.py 03_pecas/KV_9x16_texto.png 04_filme/FILME_15s_9x16.mp4 --formato 9:16 --segundos 15 --fps 30 --trilha trilha.mp3
python3 filme.py 03_pecas/KV_9x16_texto.png 04_filme/CORTE_6s_9x16.mp4 --formato 9:16 --segundos 6 --fps 30 --zoom 0.04 --pan 0.02
python3 filme.py 03_pecas/KV_1x1_texto.png 04_filme/CORTE_6s_1x1.mp4 --formato 1:1 --segundos 6 --fps 30 --zoom 0.04 --pan 0.02
```

- No caminho simples, o texto já vem na imagem (etapa 3): use o 9:16 com texto para o filme e o corte vertical, e o
  1:1 com texto para o corte quadrado.

**Se um filme do Video Editor reprovar** (rótulo ou cor), não tente consertar o arquivo exportado. Monte o mesmo
plano pelo caminho simples e confira de novo.

## 6. Entrega

- Só entra em `05_entrega/` o que saiu APROVADA, com `relatorio.json`.
- Nomes: `<marca>_01_key_visual.png` (e `_1x1`, `_9x16`), `<marca>_02_….png` … `<marca>_07_….png`, `<marca>_loja_1_fundo_branco.png`,
  `<marca>_filme_15s_9x16.mp4`, `<marca>_corte_6s_9x16.mp4`, `<marca>_corte_6s_1x1.mp4`.
- Ao final, mostre à Sol os 12 itens da lista de conferência da base de conhecimento. Deixe cada um em branco para
  ela marcar. Não marque por ela.
