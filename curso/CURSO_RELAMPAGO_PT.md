# Curso relâmpago: IA para campanhas de lançamento de beleza

Para a Sol · conferido em 4 de outubro de 2026 · existe uma versão em inglês na mesma pasta.

## Como usar este curso

São uns 90 minutos: 35 de leitura e 55 de vídeo. No fim, você vai saber como esse mundo inteiro funciona, quem faz o quê, onde a IA ainda erra, e por que o seu estúdio faz uma coisa diferente de todo mundo. Faça de uma vez, nesta ordem.

1. **O mapa** (5 min): os tipos de ferramenta e como se encaixam.
2. **Modelos de imagem, modelos de vídeo, plataformas** (15 min): quem é bom em quê, em outubro de 2026.
3. **Por que o rótulo quebra** (5 min): o problema em que o negócio inteiro se apoia.
4. **Prompt** (5 min): o vocabulário de fotógrafo, em forma de prompt.
5. **Um lançamento, passo a passo, e as regras no Brasil** (5 min).
6. **Os sete vídeos principais** (55 min), com o que observar em cada um.
7. **O autoteste** no fim. Acertou oito de dez, está pronta.

Você já segue o Miko ([@MikoxAI](https://www.youtube.com/@MikoxAI)). Ele é bom, mas é a ponta do iceberg: mostra uma ferramenta por vez, e quase sempre deixa a IA desenhar o produto. Este curso mostra o mapa inteiro.

Esse mundo muda todo mês. Cada seção de modelos traz a data em que foi conferida; qualquer coisa com mais de três meses precisa ser conferida de novo.

## O mapa

Uma campanha com IA usa quatro tipos de ferramenta: modelos de imagem, modelos de vídeo, as plataformas que dão acesso a eles e as ferramentas de acabamento. O seu estúdio acrescenta uma coisa que ninguém mais faz: a embalagem verdadeira da marca nunca passa por um modelo.

| Etapa | O que entra | O que sai |
| --- | --- | --- |
| 1. Modelos de imagem (Nano Banana, GPT Image, Seedream, FLUX, Midjourney) | Só o briefing | Cenas com uma embalagem azul chapada no lugar do produto |
| 2. Modelos de vídeo (Seedance, Kling, Veo, Gemini Omni, MiniMax H3) | O briefing, ou uma imagem pronta | Planos sem rótulo legível: chuva, cabelo, mãos, rua |
| 3. Plataformas (Manus, Higgsfield, Flow, Krea) | A sua conta | Acesso aos modelos acima, numa tela só |
| 4. O seu método: aplicar a embalagem verdadeira por código | O arquivo da embalagem, direto da marca | Cada peça com o rótulo exato |
| 5. O seu método: conferir cada peça e cada quadro de filme | Cada peça pronta | Aprovada ou reprovada, num relatório |
| 6. Acabamento e entrega | As peças aprovadas | Sombras, som, arquivos em todos os formatos, o relatório |

**A embalagem da marca nunca entra nas etapas 1 a 3.** Essa regra é o negócio.

## Modelos de imagem

A família Nano Banana, do Google, é o padrão para foto de produto e de campanha em outubro de 2026, e todo modelo sério agora anuncia "texto melhor". Mesmo assim, vários fabricantes admitem na própria documentação que texto pequeno ou elementos de marca ainda podem sair errados. Conferido em 4 out. 2026.

| Modelo | Quem faz | Versão atual | Bom para | O ponto fraco que o próprio fabricante admite |
| --- | --- | --- | --- | --- |
| [Nano Banana 2](https://ai.google.dev/gemini-api/docs/image-generation) | Google | 26 fev. 2026 | O padrão do app Gemini. 4K, "texto confiável", mantém até 4 pessoas e 10 objetos iguais entre imagens. O português está entre as melhores línguas dele. | O Google recomenda gerar o texto primeiro e depois a imagem; toda imagem leva uma marca d'água invisível (SynthID) |
| [Nano Banana Pro](https://ai.google.dev/gemini-api/docs/image-generation) | Google | nov. 2025 | "Consistência de marca", até 14 imagens de referência. É o motor do Design View do Manus. | O mesmo conselho sobre texto |
| [GPT Image 2.5](https://developers.openai.com/api/docs/guides/image-generation) | OpenAI | set. 2026 | Edição precisa com máscara, várias referências, fundo transparente, até 4K. | "Ainda pode ter dificuldade com texto em posição precisa" e com "elementos de marca" |
| [Seedream 5.0 Pro](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro) | ByteDance | 8 jul. 2026 | Muito texto, edição por laço, separa a imagem em camadas, pele realista. | "Pode melhorar em texto mais fino" |
| [FLUX 3 Image](https://bfl.ai/models/flux-3-image) | Black Forest Labs | anunciado em 23 jul. 2026 | 2K e 4K nativos, 10 referências, composição desenhando caixas, licença comercial. | Data de lançamento não publicada |
| [Midjourney V8.2](https://updates.midjourney.com/version-8-2/) | Midjourney | 24 jul. 2026 | O "visual" e o clima mais fortes. Texto funciona melhor "entre aspas"; `--raw` para resultado fotográfico. | "Ainda trabalhando na estética padrão da V8" |
| [Ideogram 4.5](https://docs.ideogram.ai/) | Ideogram | 4.5 | Feito para texto em imagem: separa o texto em camadas, fundo transparente, redimensiona anúncios. | — |
| [Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) | Alibaba (aberto) | 14 set. 2026 | Modelo aberto e gratuito; fundo transparente; mantém pessoas e produtos iguais. | — |
| [Recraft V4.1](https://www.recraft.ai/docs) | Recraft | V4.1 | Vetor (SVG editável) e um modo "Utility", chapado e de frente, para mockups. | — |

**O que isso significa para você.** Use o Nano Banana (dentro do Manus ou do Gemini) para cenas, mundos e mãos, sempre com a embalagem azul. "Texto melhor" é um avanço real para uma manchete; não é garantia para a lista de ingredientes de uma marca em letra de 2 mm, e os próprios fabricantes dizem isso.

## Modelos de vídeo

Em outubro de 2026 os líderes são o Seedance 2.5 e o Kling, com o Veo do Google e o novo Gemini Omni logo atrás; o Sora acabou. Todo fabricante admite um ponto fraco, e para vários deles é texto ou detalhe de objeto, que é exatamente o problema do rótulo. Conferido na página de cada fabricante em 4 out. 2026.

| Modelo | Quem faz | Versão atual | Bom para | O ponto fraco que o próprio fabricante admite |
| --- | --- | --- | --- | --- |
| [Seedance 2.5](https://ai.byteplus.com/en/activity/seedance2-5) | ByteDance | 2.5, 31 jul. 2026 | Até 30 s num plano só, áudio próprio, até 30 imagens de referência, edição por minutagem, 1080p. Roda dentro do Video Editor do Manus. | Na 2.0: "precisão do texto"; na 2.5: movimento complexo e várias pessoas interagindo |
| [Kling](https://www.klingai.com/blog/kling-4-vs-3) | Kuaishou | 3.0 hoje; a 4.0 "lança oficialmente em outubro" | 3.0: 3 a 15 s, até 4K nativo, áudio, quadro inicial e final, 7 referências. 4.0: 30 s, 10 quadros-chave, HDR de 10 bits, e passa a ter português. | A 3.0 é SDR de 8 bits e o português não está entre as línguas principais |
| [Veo 3.1](https://ai.google.dev/gemini-api/docs/veo) | Google DeepMind | 3.1 (out. 2025; 9:16 e 4K em jan. 2026) | Planos de 4 a 8 s, 3 imagens de referência, quadro inicial e final, estende até 141 s, sempre com áudio. No Flow e no Gemini. | Só a fala em inglês é "totalmente suportada"; as outras línguas "não foram avaliadas" |
| [Gemini Omni Flash](https://ai.google.dev/gemini-api/docs/video) | Google | 19 mai. 2026 | O Google agora diz: *"use o Gemini Omni Flash como modelo padrão para gerar vídeo"*. Edita conversando, estende até 40 s. | 720p nativo (1080p e 4K são ampliados); manter o mesmo personagem quando a cena muda |
| [MiniMax H3](https://www.minimax.io/blog/minimax-h3) | MiniMax (antiga Hailuo) | 31 jul. 2026 | Até 15 s em 2K, áudio estéreo, quadro inicial e final. Também está no Video Editor do Manus. | "O detalhe visual ainda pode melhorar em alguns casos" |
| [Runway Gen-4.5 e Aleph 2.0](https://runwayml.com/changelog) | Runway | Gen-4.5 dez. 2025; Aleph 2.0 mai. 2026 | 2 a 10 s, entrega em HDR e ProRes; o Aleph edita um vídeo que já existe. | Objetos somem: "uma xícara desaparece depois de ser encoberta" |
| [Wan 3.0](https://www.alibabacloud.com/help/en/model-studio/wan3-0-video) | Alibaba | 3.0 (só por API); a versão aberta para na 2.2 | Até 30 s em 1080p, quadro inicial e final. | Data de lançamento não publicada |

**Acabaram ou são menores:** a OpenAI desligou a API do Sora 2 em 24 set. 2026, sem substituto ([aviso da OpenAI](https://developers.openai.com/api/docs/deprecations)); tutorial antigo de Sora virou história. Luma Ray3.2, Pika 2.5, Grok Imagine Video 1.5, FLUX 3 Video e o vídeo do Midjourney (5 s, 720p) existem; você não precisa deles.

**O que isso significa para você.** O seu modelo do dia a dia é o Seedance, porque é o que está dentro do Video Editor do Manus. Vídeo gerado só entra em plano sem rótulo legível: chuva, cabelo, mão sem o produto, rua. Os planos com rótulo são as suas imagens prontas, com um movimento de câmera por cima.

## Plataformas, acabamento e som

Uma plataforma dá acesso a vários modelos numa tela só e acrescenta predefinições; o modelo por baixo costuma ser o mesmo que todo mundo usa. Por isso duas ferramentas "diferentes" podem dar o mesmo visual. O seu estúdio é o Manus; vale conhecer as outras porque os seus clientes e concorrentes usam.

| Plataforma | O que é | Vale saber |
| --- | --- | --- |
| [Manus 2.0](https://manus.im/blog/introducing-manus-2-0) | Um agente de IA que planeja e executa o trabalho; a 2.0 saiu em 28 set. 2026 | O [Video Editor](https://manus.im/blog/introducing-video-editor) tem linha do tempo em camadas (*"você não recebe um MP4 achatado"*), feito para anúncios de produto de 30 a 60 s. Modelos do Video Editor: Seedance 2.5, 2.0, 2.0 Fast e MiniMax H3; o Canvas acrescenta o Veo 3.1 ([ajuda](https://help.manus.im/en/articles/11711172-what-can-manus-video-generation-feature-do)). O [Design View](https://manus.im/docs/features/design-view) roda no Nano Banana Pro. |
| [Higgsfield](https://higgsfield.ai/marketing-studio) | Revende uns 120 modelos, mais os próprios | Soul 2.0 para UGC e moda realistas; Marketing Studio para anúncio de produto num clique (4 a 30 s, até 6 imagens do produto). Muitos criadores do YouTube são patrocinados por ela. |
| [Google Flow](https://flow.google.com/) | O estúdio de vídeo do Google | Veo 3.1 com Ingredients, Frames to Video, Extend e Insert; o Omni Flash está chegando. |
| [Krea](https://www.krea.ai/) | Estúdio com vários modelos | O Krea 2 próprio, mais Seedance, Nano Banana, Veo, Kling e outros; um ampliador que leva a imagem a tamanhos muito grandes. |
| [Magnific](https://docs.freepik.com/llms.txt) | A plataforma da Freepik, agora com o nome Magnific | Mystic, Kling, Seedance, e os ampliadores mais conhecidos (Precision e Creative). |
| [Runway](https://docs.dev.runwayml.com/guides/models/) | Modelos próprios, e agora revende também | Seedance, GPT Image, Nano Banana, Seedream e os ampliadores Magnific numa conta só. |
| [Adobe Firefly](https://www.adobe.com/products/firefly.html) | Modelos da Adobe e de parceiros | Fica ao lado do Photoshop, que você usa no acabamento à mão. |

**Acabamento.** No Photoshop você faz a sombra de contato e acerta bordas, só no cenário. [Topaz](https://www.topazlabs.com/gigapixel) e Magnific ampliam imagem e vídeo. **Um ampliador de IA redesenha o detalhe, rótulo incluído**: amplie a cena antes de aplicar a embalagem, nunca a peça pronta.

**Som.** O [ElevenLabs](https://elevenlabs.io/) v4 (28 set. 2026) faz vozes em mais de 90 línguas, inclusive português; a música dele não vale para cinema, TV e games. O [Suno](https://help.suno.com/en/articles/2416769) v6 faz músicas: no plano pago, a música é sua e você pode usar comercialmente; a música do plano grátis pertence ao Suno. Para trabalho de cliente, só música com direito comercial seu.

## Por que a IA erra o rótulo, e o método que resolve

Todo modelo de imagem e de vídeo redesenha o produto do zero, e por isso o texto pequeno do rótulo sai errado. É esse fato que sustenta o negócio inteiro.

**Por que acontece.** Um gerador não copia o seu arquivo. Ele pinta uma imagem nova, parecida com o que viu. As formas grandes sobrevivem; as letras pequenas são adivinhadas. Quanto menor o texto e quanto mais o produto se mexe, pior fica.

**O que nós medimos:**

- **O anúncio de teste da Climate Rescue (28 set. 2026):** o plano principal mostra *RESSCUE* em todos os quadros. O rótulo tinha só duas palavras, e o gerador ainda acrescentou uma letra, justo no plano que o cliente lê.
- **Um tubo real, campeão de vendas (25 set. 2026):** as duas opções de anúncio do próprio Higgsfield erraram nomes de ingredientes, uma com 2 erros e a outra com 4.
- **O estudo de caso da Climate (1 out. 2026):** as imagens paradas estavam certas, mas em dois quadros do filme o rótulo borra até ficar ilegível. É no movimento que o rótulo morre.

**O que os próprios fabricantes admitem.** O Manus diz que o primeiro corte de vídeo fica *"80 a 90% pronto"* e manda você *"arrastar a sua própria foto do produto"* para consertar. A central de ajuda da Riverflow diz que *"texto pequeno ainda é um dos detalhes mais difíceis de preservar"*, e vende conserto de rótulo feito à mão, por imagem.

**A solução: a IA nunca desenha o rótulo.**

1. Gere a cena com uma **embalagem azul chapada** no lugar do produto. No prompt, sempre: *"the whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare"* (troque *bottle* por *tube* ou *jar* conforme o produto).
2. Aplique o **arquivo verdadeiro da embalagem** sobre a azul, **por código** (`compor.py`). Ela é redimensionada, inclinada e reiluminada, nunca redesenhada.
3. **Confira** cada imagem e cada quadro de filme contra o arquivo da marca (`relatorio_fidelidade.py`). A conferência pega rótulo redesenhado, borrado, deformado ou com cor alterada.
4. **Olhe cada rótulo você mesma, com zoom de 100%.** A conferência pode deixar passar uma única letra parecida em letra miúda (*secos* virando *secas*), por isso uma pessoa sempre olha.

**Duas regras que mantêm tudo seguro.** Depois que a embalagem verdadeira entrou, nenhuma edição por IA naquela peça: "editar imagem", Design View e ampliador redesenham tudo, rótulo incluído. E num filme, só se gera plano sem rótulo legível; os planos com a embalagem usam a imagem pronta como uma camada, com a câmera se movendo por cima.

## Prompt para beleza e produto

Um bom prompt parece uma anotação de fotógrafo: o quê, onde, luz, lente, clima e o que não pode aparecer. Os seus anos de passarela e de set são uma vantagem enorme aqui: você já sabe como se ilumina um set e como um corpo segura um produto.

**Escreva o prompt em inglês, por enquanto.** Vários modelos foram treinados principalmente em inglês (o Kling 3.0 nem tem o português entre as línguas principais), o vocabulário técnico de luz e lente é em inglês, e a frase da embalagem azul está em inglês. As palavras abaixo vão em inglês, com o significado ao lado.

**As seis partes de todo prompt, nesta ordem:**

1. **Assunto:** o produto (como embalagem azul) e, se houver, a mão ou a pessoa.
2. **Cenário:** superfície, objetos, lugar (*wet stone ledge* = beirada de pedra molhada; *travertine counter* = bancada de travertino; *sea foam* = espuma do mar).
3. **Luz:** fonte e direção (*soft window light from the left* = luz suave de janela pela esquerda; *golden hour backlight* = contraluz de fim de tarde).
4. **Câmera:** lente, distância, ângulo (*85mm, eye level, front-facing* = 85 mm, altura dos olhos, de frente).
5. **Clima e paleta:** três ou quatro palavras (*calm, mineral green, warm* = calmo, verde mineral, quente).
6. **Restrições:** *no text anywhere in the image, no logo, no glare* (nenhum texto na imagem, sem logo, sem reflexo), mais a frase da embalagem azul.

**A lista de planos de beleza, e como cada um costuma ser feito:**

| Plano | O que mostra | Lente | Luz |
| --- | --- | --- | --- |
| Hero / key visual | O produto sozinho, a imagem principal da campanha | 85–100 mm | Fonte grande e suave de um lado, um leve contorno atrás |
| Na mão | Uma mão segurando a embalagem em pé, rótulo para a câmera | 85 mm | Suave, uniforme, favorável à pele |
| Em uso | Textura na pele ou no cabelo, a embalagem ao lado | 100 mm macro | Luz principal suave, um pouco de brilho na textura |
| Flat lay | Produto e objetos vistos de cima | 35–50 mm | Uniforme, sem sombra ou com uma sombra suave |
| Lifestyle / clima | O produto pequeno num lugar que parece real | 35 mm | Natural: janela, fim de tarde, dia nublado |
| Detalhe | Tampa, gota, swatch, condensação | 100 mm macro | Luz dura, para bordas nítidas |

**Palavras que mudam o resultado:**

- **Luz:** *softbox*, *beauty dish* (refletor de beleza), *window light* (luz de janela), *overcast* (nublado), *golden hour* (fim de tarde), *backlight* (contraluz), *rim light* (luz de contorno), *hard sun with crisp shadows* (sol duro, sombras marcadas), *gobo shadow* (sombra recortada, como folhas ou persiana).
- **Materiais:** *frosted glass* (vidro fosco), *amber glass* (vidro âmbar), *matte*, *satin*, *glossy* (brilhante), *metallic cap* (tampa metalizada), *condensation droplets* (gotas de condensação).
- **Pele real:** *visible skin texture, natural pores, no retouched plastic skin* (textura de pele visível, poros naturais, sem pele de plástico retocada). Pele gerada sai lisa demais por padrão.
- **Mãos:** pose simples; dedos abaixo do meio do rótulo; embalagem em pé e de frente. Depois do texto, mão é onde os geradores mais erram.

**Vídeo: um movimento por plano.** Os planos costumam ter de 5 a 10 segundos; dê a cada um um movimento de câmera e uma ação.

- **Push-in:** a câmera se aproxima devagar do produto. O movimento premium mais seguro.
- **Dolly ou truck:** a câmera desliza de lado, passando pela cena.
- **Orbit (arco):** a câmera gira em volta do produto. Evite com rótulo legível: a embalagem vira e o texto quebra.
- **Tilt, rack focus, handheld:** tilt sobe ou desce; rack focus passa o foco da frente para o fundo; handheld dá um leve tremor humano, bom para UGC.
- **Quadro inicial e final:** você dá ao modelo a primeira e a última imagem, e ele preenche o movimento entre as duas. É o maior controle que existe.

**Exemplo, key visual (com a embalagem azul):**

> A tall bottle standing on a wet stone ledge by a rain-streaked window, city lights blurred behind, soft overcast light from the left, cool blue-grey and mineral green palette, fine water droplets on the stone, 85mm lens, eye level, front-facing, the whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare, no text anywhere in the image.

*Tradução: um frasco alto em pé numa beirada de pedra molhada, ao lado de uma janela com chuva escorrendo, luzes da cidade desfocadas ao fundo, luz suave de dia nublado pela esquerda, paleta azul-acinzentada e verde mineral, gotinhas de água na pedra, lente 85 mm, altura dos olhos, de frente, o frasco inteiro, tampa incluída, em azul chroma fosco e chapado, sem texto, sem logo, sem reflexo, nenhum texto na imagem.*

## Um lançamento, do briefing à entrega

Um O LANÇAMENTO completo tem nove etapas e leva umas 4 a 4,5 horas do seu tempo, espalhadas por 5 a 7 dias úteis (é uma estimativa até as suas primeiras práticas cronometradas). A maior parte do calendário é espera pela marca.

1. **Briefing e arquivos.** A marca manda a foto do produto, a arte do rótulo, a ficha do produto e a lista de frases que ela aprova. Nada começa sem isso.
2. **Três mundos visuais.** Você propõe três direções (por exemplo *Depois da Chuva*, *Banheiro de Manhã*, *Estúdio de Cor Chapada*), cada uma já com a embalagem verdadeira aplicada. A marca escolhe uma, por escrito.
3. **Cenas com a embalagem azul.** O key visual em 9:16, seis imagens de campanha em 4:5, três imagens de loja em 1:1. Duas ou três opções de cada; você escolhe.
4. **Aplicar a embalagem verdadeira e conferir.** O script põe o arquivo da marca sobre a azul; a conferência aprova ou reprova cada peça.
5. **Acabamento à mão.** Sombra de contato, bordas e reflexos, só no cenário, nunca na embalagem.
6. **Texto.** As frases aprovadas entram ao lado da embalagem, por código, nunca por cima dela.
7. **Filme.** O key visual aprovado vira um filme vertical de 15 s: um movimento lento de câmera, um plano de abertura sem produto (chuva, cabelo, rua), as frases, música feita por IA. Mais dois cortes de 6 s. Todos os quadros são conferidos.
8. **Aprovação e uma rodada de ajustes.** A marca aprova por escrito. Um ajuste se faz mudando a cena, nunca editando a peça pronta.
9. **Entrega.** Os arquivos em todos os formatos, o relatório da conferência, e a licença e a cessão de direitos.

**O que você vende é o conjunto inteiro, num mundo visual só, com o rótulo provado contra o arquivo da própria marca.** Uma imagem solta é barata; um lançamento coerente, com garantia, não é.

## As regras no Brasil

Hoje nenhuma lei brasileira obriga a colocar "IA" num anúncio, mas as plataformas obrigam, e quatro regras decidem o que você pode fazer e vender. As leis estão mudando: confira estas regras a cada três meses.

**Aviso de IA.**

- O projeto de lei da IA, o [PL 2338/2023](https://dadosabertos.camara.leg.br/api/v2/proposicoes/2487262), ainda estava *"Aguardando Parecer"* na Câmara em 2 set. 2026. Não é lei.
- Os [códigos do CONAR](https://www.conar.org.br/codigos?section=codigo) aplicam as regras normais de publicidade aos anúncios feitos com IA. O CONAR já suspendeu um anúncio que usava um deepfake de um apresentador de TV conhecido.
- O [TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-ai-generated-content) exige aviso em pessoas e cenas realistas feitas com IA. A [Meta](https://transparency.meta.com/governance/tracking-impact/labeling-ai-content/) coloca "Informações de IA" a partir das marcas de origem do arquivo.
- **A sua prática:** a nota de entrega diz à marca para ligar o aviso de IA da plataforma. Onde aparecer uma pessoa criada por IA, vai um pequeno *"imagem ilustrativa criada com IA"*.

**De quem são as imagens.** A lei brasileira de direito autoral ([Lei 9.610, art. 11](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm)) diz que o autor é uma pessoa física, e o que é feito só por IA pode não ter proteção. Por isso você nunca escreve "as imagens são suas". Você vende uma **licença exclusiva**, uma **cessão por escrito dos direitos que você tiver** e a **sua promessa de nunca reutilizar** o trabalho.

**Alegação é responsabilidade da marca.** Só entram as frases da lista assinada pela marca, palavra por palavra. Palavras como *trata, cura, previne, clinicamente comprovado, %, em X dias, aprovado pela Anvisa, natural, vegano* só aparecem se estiverem no rótulo ou se a marca tiver a prova.

**Nunca faça:**

- antes e depois, ou qualquer sequência que sugira um resultado;
- promessa de tratamento ou cura; jaleco, clínica, estetoscópio;
- uma pessoa criada por IA dando depoimento ou avaliação;
- um rosto parecido com alguém real, famoso ou não;
- um ingrediente que não está no rótulo;
- nada voltado para criança.

**Guarde o registro.** Para cada pessoa criada por IA, salve o prompt e a data em que foi gerada. Se um dia alguém perguntar, você mostra que ela foi inventada.

## Os vídeos

Sete vídeos principais, 55 minutos, nesta ordem: cinco brasileiros e dois curtos em inglês. Para os em inglês, ligue a legenda: ⚙ (Configurações) → Legendas → Traduzir automaticamente → Português. Todos os links foram conferidos no YouTube em 4 out. 2026.

Antes de assistir, saiba duas coisas. A maioria dos criadores vende curso ou é patrocinada por uma ferramenta (vários pelo Higgsfield): trate o veredito deles como propaganda. E **nenhum deles aplica a embalagem verdadeira**: todos deixam a IA desenhar o produto. Repare no rótulo em cada vídeo; é ali que você vai ver o problema que o seu estúdio resolve.

**Os principais, em ordem (55 min):**

| # | Vídeo | Canal | Duração | Por que ver, e o que observar |
| --- | --- | --- | --- | --- |
| 1 | [Como fotografar produtos com apenas uma fonte de luz](https://www.youtube.com/watch?v=n3GIailBjFc) | AvMakers | 3:42 | Foto de produto de verdade, sem IA: como uma luz só modela uma embalagem. É isso que o prompt tem que descrever. |
| 2 | [TUTORIAL NANO BANANA: COMO FAZER CRIATIVOS QUE CONVERTEM PARA O META ADS](https://www.youtube.com/watch?v=UlDfDtsZPiw) | Adriano Gianini | 15:52 | O Nano Banana na prática, para anúncio. Observe onde o texto e o produto saem tortos. |
| 3 | [Keeping product text consistent with Nano Banana Pro and Kling 3.0 Omni](https://www.youtube.com/watch?v=XLHTLJhzDyQ) | Magnific (em inglês) | 6:08 | O problema do rótulo, contado por quem faz a ferramenta: que ajuste mantém o texto e onde ele ainda falha. |
| 4 | [27 Camera Moves Cinematográficos para IA – Guia Completo de Prompts](https://www.youtube.com/watch?v=UlogLFs3MWo) | Brizen AI | 13:58 | O dicionário de movimentos de câmera, com o nome de cada um em inglês para o prompt. |
| 5 | [Como Criar Vídeos para Divulgar Seu Produto com IA (Passo a Passo)](https://www.youtube.com/watch?v=V3teEPLM3tQ) | Darlan Evandro | 11:18 | Um vídeo de produto do começo ao fim. Repare nos quadros em que o rótulo se mexe. |
| 6 | [Introducing Manus Video Editor](https://www.youtube.com/watch?v=OSaWc0sBspA) | Manus AI (em inglês) | 0:53 | A demonstração oficial do editor onde você vai finalizar os filmes. |
| 7 | [Imagens geradas por IA em anúncios de comida podem violar o Código de Defesa do Consumidor](https://www.youtube.com/watch?v=cbYBTraJEFI) | Jornalismo TV Cultura | 2:58 | Por que um anúncio de IA que engana vira problema legal no Brasil. Vale igual para beleza. |

**Se quiser ir mais fundo, por assunto:**

| Assunto | Vídeo | Canal | Duração |
| --- | --- | --- | --- |
| Visão geral das IAs de vídeo | [TOP MELHORES IA PARA CRIAR VÍDEOS COM PROMPTS (ATUALIZADO)](https://www.youtube.com/watch?v=BfQhrY9Y4qg) | Preguiça Artificial | 15:59 |
| Qual IA usar para começar | [QUAL A MELHOR IA PRA QUEM ESTÁ COMEÇANDO EM 2026?](https://www.youtube.com/watch?v=n4sj3kb_3NQ) | Kaique Editor | 14:51 |
| Seedance 2.5 a fundo | [Testei o Dreamina Seedance 2.5 ao MÁXIMO: 3D, prompts complexos e 30s em um clipe](https://www.youtube.com/watch?v=ThtrD0VnCtQ) | Willian IA (patrocinado) | 28:33 |
| Prompt de vídeo | [a MELHOR FORMA possível para Criar PROMPT para Vídeo!](https://www.youtube.com/watch?v=ArAQLaurvXs) | Willian IA | 12:37 |
| Veo 3.1 e Flow | [Curso GRÁTIS de VEO 3.1: Crie Anúncios Realistas com o novo Flow](https://www.youtube.com/watch?v=EUzpW4YIM3s) | Marco Lang | 25:44 |
| Kling 3.0 do zero | [Como Usar a KLING AI 3.0 (Atualizado)](https://www.youtube.com/watch?v=A62npSHlTwI) | Mico Prompt | 12:44 |
| Foto de produto com Nano Banana | [Use IA para Criar Fotos de Produtos e Vender Mais no Ecommerce ou redes sociais](https://www.youtube.com/watch?v=OtlnOiS8Oz4) | Descomplicando Sites | 10:50 |
| Comercial cinematográfico | [Crie uma COMERCIAL CINEMATOGRÁFICO para um Produto com IA](https://www.youtube.com/watch?v=1duX0RpTJq4) | Matheus Delalibera | 11:45 |
| UGC com IA | [Como fazer criativos UGC com IA que geram um ROAS de 4,7x](https://www.youtube.com/watch?v=08zYIwpdZFc) | Henrique Oliveira | 17:10 |
| Higgsfield, curso | [Curso de Higgsfield AI Grátis (INICIANTE AO AVANÇADO 2026)](https://www.youtube.com/watch?v=X9PZQ2wyePw) | Preguiça Artificial | 34:42 |
| Higgsfield, anúncios | [Essa IA transforma imagens em vídeos de anúncios profissionais](https://www.youtube.com/watch?v=2hYO9aNHRA8) | Alex Henrique | 10:55 |
| Manus do zero | [Curso Básico de Manus AI 2026 - Agente de IA do Zero](https://www.youtube.com/watch?v=ZYQgz1eodFE) | Hashtag Treinamentos | 35:11 |
| Manus para marketing | [Essa IA da Meta Cria Conteúdo e Otimiza Seus Anúncios Sozinha (Manus 2026)](https://www.youtube.com/watch?v=lQgoPBrrdE0) | Filipe Detrey | 21:58 |
| O que mudou no Manus 2.0 | [Manus 2.0 agora é totalmente autônomo…](https://www.youtube.com/watch?v=DGekgJaXe-s) | AI Revolution em Português | 14:58 |
| Produto que reflete (vidro, metal) | [COMO FOTOGRAFAR PRODUTOS REFLEXIVOS ???](https://www.youtube.com/watch?v=iKAIK4TF5Zw) | Estúdio Mafe | 15:49 |
| Foto still para e-commerce | [COMO Fazer FOTOGRAFIA STILL para E-COMMERCE](https://www.youtube.com/watch?v=d7TZVhJCcBQ) | Kiiro Cine Fotografia | 16:09 |
| CONAR e publicidade | [Direito Publicitário, Conar e os desafios da publicidade contemporânea](https://www.youtube.com/watch?v=sLKzigKix4Y) | Daniel Law | 21:31 |

**Em inglês, com legenda automática, os melhores:**

| Assunto | Vídeo | Canal | Duração |
| --- | --- | --- | --- |
| Uma sessão real de skincare, luz por luz | [Lighting & Styling Breakdown for Skincare Product Shoot](https://www.youtube.com/watch?v=WM78JenzGAc) | Amanda Campeanu | 6:22 |
| A mesma fotógrafa, em prompts | [Nano Banana AI prompts for beauty brands](https://www.youtube.com/watch?v=VFXeOdQEMCs) | Amanda Campeanu | 6:06 |
| Kling 4.0 contra Seedance 2.5 (aos 8:47, um teste de rótulo num frasco de cosmético) | [Kling 4.0 vs Seedance 2.5 — Best AI Video Generator in 2026?](https://www.youtube.com/watch?v=YH1LLoBPx0Y) | Dom the AI Tutor | 9:47 |
| Seedance em anúncio de produto (patrocinado) | [I Tested Seedance 2.5 for Product Ads](https://www.youtube.com/watch?v=y6Zw5WFs62k) | Thomas Lundström | 8:42 |
| Onde a IA de produto falha | [Why Your AI Product Images Are Failing](https://www.youtube.com/watch?v=R7Eml0ttQtg) | Escapism | 25:43 |
| Miko: realismo com Nano Banana Pro | [Hyper-Realistic AI Images with Nano Banana Pro](https://www.youtube.com/watch?v=_D-7SamsJdY) | Miko | 10:23 |
| Miko: anúncio UGC | [How to Make Viral AI UGC Ads in 2026](https://www.youtube.com/watch?v=x_TAoTi3ras) | Miko | 15:28 |
| Miko: UGC com Seedance 2.5 | [Seedance 2.5 Just Changed AI UGC Ads (Full Breakdown)](https://www.youtube.com/watch?v=5jKsG3wTDrI) | Miko | 12:42 |

**Canais brasileiros para seguir, além do Miko:**

- [Marco Lang](https://www.youtube.com/@MarcoLang) (31,1 mil inscritos): Veo, Flow e anúncios realistas, passo a passo.
- [Preguiça Artificial](https://www.youtube.com/@preguicaartificial) (284 mil): o panorama das ferramentas novas, rápido e atualizado.
- [Willian IA](https://www.youtube.com/@willian.design) (108 mil): testes a fundo de modelos de vídeo e de prompt.
- [Matheus Delalibera](https://www.youtube.com/@MatheusDelalibera) (10,7 mil): comercial cinematográfico de produto com IA.
- [Estúdio Mafe](https://www.youtube.com/@FOTOGRAFIADEALIMENTOSEPRODUTOS) (17,7 mil): fotografia de produto de verdade, sem IA. Ensina a luz que você vai descrever nos prompts.

## Glossário

As palavras que esse mundo usa sem explicar, com o termo em inglês que você vai ouvir nos canais de fora.

| Termo | O que é | Em inglês |
| --- | --- | --- |
| Modelo | O motor de IA em si (Seedance, Veo, Nano Banana). As plataformas dão acesso a vários. | model |
| Plataforma | Um site ou app que dá acesso a vários modelos, com predefinições (Higgsfield, Manus, Freepik). | platform |
| Prompt | A instrução escrita. | prompt |
| Texto para imagem / vídeo | Imagem ou plano feito só a partir de palavras. | text-to-image / text-to-video |
| Imagem para vídeo | Um plano que começa de uma imagem que você dá. O principal jeito de controlar um filme. | image-to-video |
| Imagem de referência | Uma imagem que o modelo tem que seguir (um rosto, um estilo, um produto). | reference image |
| Quadro inicial e final | A primeira e a última imagem de um plano; o modelo preenche o movimento entre elas. | start and end frame |
| Inpainting / expandir | Repintar uma parte da imagem / estender a imagem além das bordas. | inpainting / outpainting |
| Ampliar | Deixar a imagem ou o vídeo maior e mais nítido. Ampliador de IA redesenha o detalhe, rótulo incluído. | upscale |
| Consistência | Manter o mesmo rosto, produto ou estilo em várias imagens. | consistency |
| Seed (semente) | O número aleatório por trás de um resultado. Mesma seed + mesmo prompt = resultado parecido. | seed |
| Proporção | O formato do quadro: 9:16 vertical, 4:5 feed, 1:1 quadrado, 16:9 horizontal. | aspect ratio |
| Créditos | A moeda que a maioria das plataformas cobra; vídeo gasta muito mais que imagem. | credits |
| Packshot / foto still | Foto limpa só do produto, normalmente no fundo branco. | packshot |
| Key visual (KV) | A imagem principal da campanha; tudo o mais segue o mundo dela. | key visual |
| Embalagem azul (chroma) | Um objeto azul (ou verde) chapado no lugar do produto, para a embalagem verdadeira ser aplicada por cima. | chroma stand-in |
| Composição / aplicar | Colocar uma imagem sobre outra por código ou Photoshop, sem redesenhar. | composite |
| UGC | "Conteúdo feito pelo usuário": o anúncio estilo selfie em que uma pessoa segura o produto e fala. | UGC |
| Sincronia labial | Fazer a boca de um rosto acompanhar uma voz. | lip-sync |
| Planos de apoio | Planos sem fala: chuva, cabelo, rua, mãos. | B-roll |
| Corte | Uma versão mais curta do filme para anúncio (6 s, 15 s). | cut / cutdown |
| BT.709 | O padrão de cor que o celular espera. Um arquivo marcado errado mostra as cores da embalagem deslocadas. | BT.709 |
| Proveniência (C2PA) | Marcas escondidas no arquivo dizendo que ele foi feito com IA; a Meta lê essas marcas. | provenance |

## Autoteste: dez perguntas

Se você responder oito sem olhar, já sabe mais do que a maioria das pessoas que vende conteúdo de IA no Brasil.

1. Por que os modelos de IA erram o rótulo, e por que é pior em vídeo?
2. O que é a embalagem azul, e quais palavras exatas vão no prompt?
3. Depois que a embalagem verdadeira foi aplicada, por que "editar imagem" é proibido naquela peça?
4. Qual a diferença entre um modelo e uma plataforma? Dê dois exemplos de cada.
5. Qual movimento de câmera é o mais seguro para um filme de produto premium, e qual quebra o rótulo?
6. O que "imagem para vídeo" com quadro inicial e final deixa você controlar?
7. O que a conferência do rótulo pega, e o que ela pode deixar passar?
8. Por que você nunca escreve "as imagens são suas" num contrato?
9. Cite quatro coisas que você nunca faz para uma marca de beleza.
10. A marca manda um rótulo novo depois da aprovação. O que acontece?

**Respostas.**

1. Eles repintam o produto em vez de copiar, e as letras pequenas são adivinhadas; no vídeo, ele é repintado em cada quadro.
2. Um produto azul chapado no lugar do verdadeiro. *"The whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare."*
3. Essas ferramentas repintam a peça inteira, rótulo incluído.
4. O modelo é o motor (Seedance, Veo, Nano Banana, Kling); a plataforma dá acesso a vários (Higgsfield, Manus, Freepik).
5. O push-in lento é o mais seguro; o orbit vira a embalagem e quebra o texto.
6. Onde o plano começa e termina; o modelo só inventa o movimento entre os dois.
7. Pega rótulo redesenhado, borrado, deformado ou com cor alterada. Pode deixar passar uma única letra parecida em letra miúda, por isso você sempre olha com zoom de 100%.
8. A lei diz que o autor é uma pessoa física e o que é feito por IA pode não ter proteção; você vende licença exclusiva, cessão de direitos e a promessa de não reutilizar.
9. Antes e depois; promessa de tratamento ou cura; pessoa criada por IA dando depoimento; rosto parecido com alguém real (também: jaleco, ingrediente fora do rótulo, anúncio para criança).
10. A marca assina uma ficha do produto nova, com o arquivo novo, e a embalagem é aplicada de novo a partir desse arquivo.
