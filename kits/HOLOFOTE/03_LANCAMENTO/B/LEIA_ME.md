# 03_LANCAMENTO/B · BOLETIM DA TURNÊ (§E.2 B01–B08)

Oito cartões lambe das 06:03, de 2 a 9 de maio, cada um na cor da faixa do dia, em dois formatos.

| Arquivo | O que é |
|---|---|
| `B0n_BOLETIM_DDMM_1x1.png` | Post 1080 × 1080 (caixa segura x 180–900, y 80–1000). |
| `B0n_BOLETIM_DDMM_9x16.png` | Status / story 1080 × 1920 (caixa segura x 140–940, y 270–1500; base livre de tipo). |

B01 02.05 amarelo · B02 03.05 rosa · B03 04.05 laranja · B04 05.05 violeta · B05 06.05 amarelo · B06 07.05 rosa ·
B07 08.05 laranja · B08 09.05 amarelo. A linha da assinatura fica 16 px acima do fim da caixa segura (o wordmark e
o registro de O LAMBE não passam de y 1000 / 1500). A linha do dia é a do §E.2, palavra por palavra; só a quebra de linha foi
escolhida. B06–B08 levam os três sinais (o sino do dia cheio). Tudo gráfico, nenhum render.
Refazer: `python _build/brand/lancamento.py B` (template: `peca.html`, receita `boletim`; papel: `lambe.py`).
