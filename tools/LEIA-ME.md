# Ferramentas do O LANÇAMENTO — como usar

Três comandos. Rodam no seu computador; **nenhum envia arquivo da marca para a internet.**

**Uma vez só, para instalar:** Python 3 e, no terminal:

```
pip install opencv-python numpy imageio-ffmpeg
```

## O caminho de uma peça

**1. Gere o cenário com a embalagem em branco (no Higgsfield).**
- No prompt, nunca escreva nome de marca, de produto nem alegação.
- Peça sempre: *"the whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare"*. A embalagem
  inteira, tampa incluída, num azul chapado, sem brilho. Se a tampa vier branca, gere de novo.
- Mesmo ângulo da imagem-mestra da marca (de frente, se a mestra é de frente).
- **Nunca suba a foto, o PDF ou o logo da marca no Higgsfield nem em nenhum outro serviço de IA.**

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

**3. Acabamento no Photoshop, à mão:** sombra de contato, borda, cor da tampa. **Ajuste o cenário à embalagem,
nunca a embalagem ao cenário.** Não use Preenchimento Generativo, Gerar Plano de Fundo nem Harmonizar na camada da
embalagem.

**4. Filme de 15 segundos:**

```
python3 filme.py PECA.png FILME.mp4 --formato 9:16 --trilha musica.mp3
```

- Formatos: `9:16`, `4:5`, `1:1`, `16:9`.
- Cortes de 6 s: `--segundos 6`.
- Com mão na embalagem, a paralaxe desliga sozinha.
- O filme não gira o produto em 3D.

**5. Confira TUDO antes de entregar:**

```
python3 relatorio_fidelidade.py EMBALAGEM.png PECA.png FILME.mp4 --json relatorio.json
```

- **APROVADA** ou **REPROVADA** por peça.
- Em toda imagem, a ferramenta planta um erro de teste numa cópia e confere se o encontra (`control_caught: true`).
  Se não encontrar, a peça sai REPROVADA: um controle que não pode falhar não prova nada.
- Filmes são conferidos **quadro a quadro**. Não use `--every` maior que 1 numa entrega.
- **Uma peça REPROVADA nunca é entregue.** Gere o cenário de novo ou refaça o encaixe.

## Antes do primeiro cliente de um tipo novo de embalagem
Pump, pote, conta-gotas ou vidro: monte três peças exatas e confira que todas saem APROVADAS com o controle
detectado. Os limites foram calibrados num tubo (ver `O_LANCAMENTO_AIRTIGHT.md` §4).
