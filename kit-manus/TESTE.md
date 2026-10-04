# O teste, antes do primeiro cliente

Dois testes, nesta ordem. Os limites estão escritos **antes** de rodar e não mudam depois.

---

## Teste 1 · A instalação funciona? (5 minutos, uma mensagem)

No projeto **O LANÇAMENTO**, crie uma tarefa nova e envie:

> /o-lancamento Rode o autoteste: `python3 autoteste.py` na pasta das ferramentas. Me mostre a tela inteira.

O autoteste usa um produto inventado, **ORVALHA**, e confere onze coisas sozinho:

| # | O que confere |
|---|---|
| 1 | As bibliotecas estão instaladas |
| 2 | A cena vai para 1080x1920 |
| 3 | A embalagem verdadeira é aplicada sobre a azul |
| 4 | Os recortes 4:5 e 1:1 saem no tamanho certo |
| 5 | O texto entra ao lado da embalagem sem tocar nela |
| 6 | As 3 peças exatas são APROVADAS, com o erro plantado detectado |
| 7 | O filme sai em 1080x1920, 30 fps, cor BT.709 |
| 8 | Todos os quadros do filme são APROVADOS |
| 9 | **Um filme com trecho sem embalagem não declarado é REPROVADO** |
| 10 | O mesmo filme, com o trecho declarado, é APROVADO |
| 11 | **Uma peça com o rótulo errado é REPROVADA** |

**Passa se aparecer `AUTOTESTE: 11/11 OK`.**
- Se não passar, mande a tela inteira para quem configurou o kit.
- Não comece o Teste 2 antes do 11/11.
- Os itens 9 e 11 são os mais importantes: uma conferência que não reprova nada não prova nada.
- O autoteste não prova mão sobre a embalagem, filme completo de cliente, outros formatos de embalagem nem a
  exportação do Manus. Isso é o Teste 2.

---

## Teste 2 · Três lançamentos de prática, cronometrados

O cliente é inventado: **ORVALHA, sérum capilar, frasco com pump**.
- Os arquivos estão em `O LANCAMENTO/clientes/orvalha_PRATICA/00_recebido`: embalagem, Ficha do Produto e Ficha de
  Alegações.
- Você faz o papel da marca: escolhe o mundo e aprova por escrito para você mesma.
- Siga o **GUIA_DA_SOL.md** da etapa 0 à 7. Na etapa 0, em vez da mensagem do guia, envie esta:

> Cliente de prática: ORVALHA, sérum capilar, pedido O LANÇAMENTO. A pasta já existe em
> clientes/orvalha_PRATICA. Crie as subpastas que faltam, preencha o BRIEFING.md a partir das duas fichas e me diga o
> que falta. Nesta prática, eu faço o papel da marca, e não há PDF do rótulo: a arte aprovada é o EMBALAGEM.png.

Faça três rodadas, cada uma num mundo diferente:
1. Depois da Chuva.
2. Banheiro de Manhã.
3. Um mundo à sua escolha.

A terceira mostra quanto você ganhou de prática.

### Os limites (escritos antes)

| | Limite | Se não passar |
|---|---|---|
| A | **Toda peça e todo filme APROVADOS, com o erro plantado detectado.** 100%, nas três rodadas | Não vende ainda. Anote qual peça e por quê |
| B | **Seu tempo, etapas 1 a 7: até 3 horas** por rodada | Anote onde o tempo foi. Isso decide o preço e quantos lançamentos cabem no mês |
| C | **O Video Editor exporta 1080x1920** e o filme exportado passa na conferência (rótulo **e** cor) | O filme passa a sair sempre pelo caminho simples. Anote o motivo |
| D | **As cenas geradas têm pelo menos 1080 pixels no lado menor** | Anote o tamanho que o Manus entrega |
| E | **Créditos anotados por etapa** (o Manus mostra os créditos de cada tarefa) | A estimativa é de 2.000 a 5.000 por lançamento |
| F | **Uma peça que você não teria vergonha de mostrar a uma marca de verdade**, por rodada | Anote o que faltou: luz, mão, sombra, cenário |

### A ficha de anotação (uma por rodada)

| Etapa | Seus minutos | Créditos | APROVADA? | O que aconteceu |
|---|---|---|---|---|
| 0 · Novo cliente | | | — | |
| 1 · Três mundos | | | | |
| 2 · Cenas | | | — | |
| 3 · Aplicar e conferir | | | | |
| 4 · Acabamento | | — | | |
| 5 · Texto | | | | |
| 6 · Filme e cortes | | | | |
| 7 · Entrega interna | | | — | |
| **Total** | | | | |

### Duas perguntas para anotar no fim

1. O que demorou mais do que deveria?
2. Você conseguiria fazer isso **quatro vezes por mês**, para marcas de verdade, por três anos?

---

## O que a conferência pega, e o que ela não pega

**Pega** (medido em 4 out 2026):
- rótulo redesenhado, borrado ou com letra inventada, como o *RESSCUE*;
- nome da marca trocado (*ORVAHLA*);
- letra faltando (*capilr*);
- número trocado numa embalagem grande (*30 ml* → *50 ml*);
- embalagem torta ou deformada;
- cor alterada.

**Não pega com segurança:** uma única letra parecida trocada numa letra miúda, como *secos* → *secas* ou um acento
faltando. O mesmo vale para o número quando a embalagem aparece pequena.

**Por isso a regra da etapa 0:**
- A embalagem só sai do arquivo listado na Ficha do Produto assinada.
- A marca aprova o key visual por escrito.

As letras vêm do arquivo da marca: a embalagem é redimensionada, girada e reiluminada por código, nunca redesenhada.
A conferência confirma que ela não foi redesenhada, deformada ou recolorida. Ela não prova que cada pixel é idêntico.
