# Ferramentas do O LANÇAMENTO — como usar

Poucos comandos. Rodam no seu computador; **nenhum envia arquivo da marca para a internet.**

**Uma vez só, para instalar:** Python 3 e, no terminal:

```
pip install opencv-python numpy imageio-ffmpeg pillow
```

Para confirmar que tudo funciona: `python3 autoteste.py` (cerca de 5 minutos; tem de terminar em `AUTOTESTE: 11/11 OK`).
O autoteste usa um produto inventado, ORVALHA, e inclui uma peça com rótulo errado que precisa ser REPROVADA.

Para o filme com animação (recomendado): Node.js 22 ou mais novo e FFmpeg, e depois:

```
npx hyperframes telemetry disable
npx hyperframes browser ensure
```

## O caminho de uma peça

**1. Gere o cenário com a embalagem em branco (no Higgsfield).**
- No prompt, nunca escreva nome de marca, de produto nem alegação.
- Peça sempre: *"the whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare"*. A embalagem
  inteira, tampa incluída, num azul chapado, sem brilho. Se a tampa vier branca, gere de novo.
- Mesmo ângulo da imagem-mestra da marca (de frente, se a mestra é de frente).
- **Nunca suba a foto, o PDF ou o logo da marca no Higgsfield nem em nenhum outro serviço de IA.**

**1b. Leve a cena ao tamanho final antes de aplicar a embalagem:**

```
python3 recortar.py CENA.png CENA_9x16.png 1080x1920
```

- Key visual em 9:16 (1080x1920), com a embalagem no centro ocupando 45% a 50% da altura. Dele saem os recortes:
  `python3 recortar.py PECA_9x16.png PECA_4x5.png 1080x1350` e `… PECA_1x1.png 1080x1080`, só recorte, sem
  redimensionar.
- Campanha 4:5 (1080x1350). Loja 1:1 (1200x1200).

**2. Aplique a embalagem verdadeira:**

```
python3 compor.py CENA.png EMBALAGEM.png PECA.png
```

- `EMBALAGEM.png` é o recorte da imagem-mestra, com fundo transparente, feito no Photoshop com *Remover plano de fundo*
  no modo **Dispositivo** (nunca Nuvem).
- Saem três arquivos: `PECA.png` (a peça), `PECA.hidden.png` (onde a mão cobre a embalagem) e `PECA.alpha.png`.
- Se o azul for outro tom, use `--matiz` (em graus: azul 210, verde 120).
- Se ficar pequena ou grande demais, use `--ajuste largura` ou `--ajuste altura`.
- Se nada estiver na frente da embalagem, use `--sem-oclusao`.

**2b. Texto, depois dos recortes, um formato por vez:**

```
python3 texto.py PECA_4x5.png PECA_4x5_texto.png --linhas "NOVO|Frase aprovada" --fonte fonte_da_marca.ttf
```

- Escolhe o maior espaço livre ao lado da embalagem.
- Prova que nenhum pixel da embalagem mudou; se mudou, não salva.
- Nunca ponha texto com um editor de imagem por IA: ele redesenha a imagem inteira, inclusive o rótulo.

**3. Acabamento no Photoshop, à mão:** sombra de contato, borda, cor da tampa. **Ajuste o cenário à embalagem,
nunca a embalagem ao cenário.** Não use Preenchimento Generativo, Gerar Plano de Fundo nem Harmonizar na camada da
embalagem.

**4. Filme (HyperFrames, recomendado):**

```
python3 filme_hyperframes.py PECA.png projeto --linhas "NOVO|Frase|aprovada" --final "EM BREVE|01 · 11"
cd projeto && npx hyperframes check . && npx hyperframes render . --format png-sequence -o ../quadros && cd ..
python3 codificar.py quadros FILME.mp4 --fps 30 --trilha musica.mp3 --segundos 8
```

- O texto vem **só** da Ficha de Alegações assinada. A ferramenta põe o texto ao lado ou acima/abaixo da embalagem,
  **nunca por cima dela**.
- O `check` do HyperFrames avisa se o texto está ilegível (contraste). Corrija antes de renderizar.
- **Nunca entregue o MP4 que o HyperFrames gera sozinho:** ele altera as cores no celular. Sempre `--format
  png-sequence` + `codificar.py`.
- **Nunca use `publish`, `cloud`, `lambda`, `cloudrun` nem `feedback --file-issue` em projeto de cliente:** esses
  comandos mandam o projeto para fora do seu computador.
- **Não deixe chave de IA (`GEMINI_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY`) configurada** no computador em que
  monta filmes de cliente; o comando `snapshot` mandaria os quadros para o Google.

**4b. Filme simples, sem instalar nada além do Python:**

```
python3 filme.py PECA.png FILME.mp4 --formato 9:16 --trilha musica.mp3
```

- Formatos: `9:16`, `4:5`, `1:1`, `16:9`. Cortes de 6 s: `--segundos 6`.
- Com mão na embalagem, a paralaxe desliga sozinha. Nenhum dos dois filmes gira o produto em 3D.

**5. Confira TUDO antes de entregar:**

```
python3 relatorio_fidelidade.py EMBALAGEM.png PECA.png FILME.mp4 --json relatorio.json
```

- **APROVADA** ou **REPROVADA** por peça.
- Em toda imagem, a ferramenta planta um erro de teste numa cópia e confere se o encontra (`control_caught: true`).
  Se não encontrar, a peça sai REPROVADA: um controle que não pode falhar não prova nada.
- Filmes são conferidos **quadro a quadro**. Não use `--every` maior que 1 numa entrega.
- A cor também é conferida: o desvio de tom da embalagem tem de ficar dentro da tolerância da Ficha
  (`--tolerancia-cor`, padrão 2).
- **Uma peça REPROVADA nunca é entregue.** Gere o cenário de novo ou refaça o encaixe.

## Antes do primeiro cliente de um tipo novo de embalagem
Pump, pote, conta-gotas ou vidro: monte três peças exatas e confira que todas saem APROVADAS com o controle
detectado. Os limites foram calibrados num tubo (ver `O_LANCAMENTO_AIRTIGHT.md` §4).
