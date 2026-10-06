# 03_LANCAMENTO/C · C03, C07, C09 (§E.2)

| Arquivo | O que é |
|---|---|
| `C03_O-PIOR-SHOW.png` | 9:16. ELA / APLAUDIU / DE PÉ / O SEU / PIOR / SHOW. em tipo de madeira, a nota da Fã "(girassol, 2007)" com seta, o círculo Ø 360 da vela acesa com fio preto de 6 px, "SUA VEZ." + "holofote nela." + linha de segurança. Os vãos da pilha são iguais (o de DE PÉ só tem o ar do agudo: ≥ 6 px limpos depois de O LAMBE). |
| `C07_PIX.png` | 9:16, só em 6 de maio. PIX / NÃO TEM / CHEIRO., miniatura do KV com fio preto de 6 px, MÃE AO VIVO · DOMINGO 09.05, linha de segurança e assinatura. Sem marca Pix. |
| `C09_O-CARTAZ-DELA_DONA-CIDA.png` | 9:16. Saída de exemplo do gerador: DONA CIDA AO VIVO em rosa (escada passo 4), seis datas da turnê; "faz o cartaz dela." é a anotação da Fã com seta até o nome; "holofote.exemplo/cartaz" em Produção pequena com um fio até o fim da medida. |
| `placeholders.json` | Caixa `[x, y, w, h]` da miniatura da vela em C03 (círculo) e C07 (retângulo 4:5). |

As miniaturas não têm alegação de fidelidade (§D.7.5). Para pôr o render no lugar com o mesmo papel:
`python _build/brand/lancamento.py C` usa `_build/brand/cache/vela_c03.png` e `vela_c07.png` (recortes do KV-45 aceso);
`… C --vela-c03 vela.png --vela-c07 kv.png` troca os arquivos. O render entra DEPOIS de O LAMBE, intocado, e o fio
preto de 6 px é desenhado depois do render.
