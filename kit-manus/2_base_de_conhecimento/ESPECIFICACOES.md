# O que sai de cada pedido

## Os produtos

| Produto | Preço | O que entra | Prazo |
|---|---|---|---|
| **VITRINE** | R$ 490 por produto | 6 imagens, 2 com o produto na mão ou em uso · imagem principal de fundo branco · formatos 1:1, 4:5 e 9:16 · relatório | 48 horas |
| **O LANÇAMENTO** | R$ 2.990 por lançamento | Produto principal + até 2 de apoio na cena · key visual · 6 imagens de campanha · filme de 15 s · 2 cortes de 6 s · 3 peças de loja · relatório | 5 a 7 dias úteis |
| **EXTENSÃO** | R$ 690 por produto | Novo produto no mundo que já é da marca · 6 imagens · kit de marketplace | 48 horas |
| **A LINHA** | R$ 4.900 | Até 3 produtos no mesmo mundo de campanha | — |
| **TEMPORADA** | R$ 9.900 | 4 lançamentos pagos antecipadamente | — |
| **PRÉVIA** | grátis | O produto mais vendido da marca na mão, feito da foto pública dele, com autorização. Marca d'água *"PRÉVIA — uso interno, não publicar"*. Apagar em 30 dias se não virar pedido | — |

- **Uma rodada de ajustes por pedido.** Correção de embalagem não conta como rodada.
- **O filme não gira o produto em 3D.**

## O LANÇAMENTO: as 13 peças

| # | Peça | Formato | Nome do arquivo |
|---|---|---|---|
| 1 | Key visual | 4:5, 1080×1350 | `<marca>_01_key_visual.png` |
| 1b | Key visual, recortes | 1:1 1080×1080 e 9:16 1080×1920 | `<marca>_01_key_visual_1x1.png`, `_9x16.png` |
| 2–7 | 6 imagens de campanha | 4:5, 1080×1350 | `<marca>_02_….png` a `<marca>_07_….png` |
| 8 | Loja: fundo branco | 1:1, 1200×1200 | `<marca>_loja_1_fundo_branco.png` |
| 9 | Loja: em uso | 1:1, 1200×1200 | `<marca>_loja_2_em_uso.png` |
| 10 | Loja: rotina | 1:1, 1200×1200 | `<marca>_loja_3_rotina.png` |
| 11 | Filme | 9:16, 1080×1920, 30 fps, 15 s | `<marca>_filme_15s_9x16.mp4` |
| 12 | Corte | 9:16, 1080×1920, 30 fps, 6 s | `<marca>_corte_6s_9x16.mp4` |
| 13 | Corte | 1:1, 1080×1080, 30 fps, 6 s | `<marca>_corte_6s_1x1.mp4` |
| — | Relatório de fidelidade | JSON + uma linha por peça | `relatorio.json` |

## As 6 imagens de campanha: uma sugestão de roteiro

Use as seis e varie dentro do mundo escolhido.

1. **Ritual:** o produto em uso, mãos e pele, sem rosto inteiro.
2. **Na mão:** a mão segurando a embalagem de frente, rótulo visível e parado.
3. **Prateleira:** o produto em pé num ambiente do mundo (banheiro, penteadeira, mala).
4. **Mesa:** o produto deitado ou em pé com elementos do mundo (toalha, água, folhas).
5. **Mood:** a cena do mundo com o produto pequeno no quadro.
6. **Detalhe:** textura do produto (creme, gota, espuma) ao lado da embalagem.

## O filme de 15 s, em quatro tempos

| Tempo | O que acontece | Texto (só da Ficha de Alegações) |
|---|---|---|
| 0–3 s | O mundo: chuva, luz, cabelo, sem produto | Nenhum |
| 3–8 s | O key visual entra, câmera aproxima devagar | Uma palavra curta, por exemplo *NOVO* |
| 8–12 s | A frase principal ao lado da embalagem, nunca por cima | A frase aprovada |
| 12–15 s | Cartão final: nome do produto e data | *EM BREVE · 01·11*, ou a data da marca |

- **Trilha:** criada por IA para uso comercial. Nunca música de biblioteca com licença por assinatura.
- **Cortes de 6 s:** os tempos 3 a 8 e 12 a 15, sem a abertura.

## A Ficha do Produto traz

- Nome exato do produto, como é vendido.
- Tipo de embalagem: tubo, pump, pote, conta-gotas ou vidro.
- Cores da marca, em HEX.
- Tolerância de cor. Se a ficha não disser, use 2.

## Nova embalagem

Para cada tipo novo (pump, pote, conta-gotas, vidro), antes do primeiro cliente desse tipo:

1. Faça três peças exatas com a embalagem.
2. Confira que todas saem APROVADAS com o erro plantado detectado.

A conferência foi calibrada num tubo.
