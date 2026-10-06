# 03_LANCAMENTO/D · D01 A CARTEIRINHA, D02 O INGRESSO (§E.2)

| Arquivo | O que é |
|---|---|
| `D01_A-CARTEIRINHA_9x16.png` | Story 9:16: o cartão de fã-clube dos anos 80, plastificado (faixa de brilho de borda dura), cantos redondos, janela de foto. FÃ-CLUBE OFICIAL · MÃE · SÓCIO Nº 0001 · Membro desde: hoje · Atraso: 22 anos · Validade: vitalícia · Benefício: acesso total (sempre teve). |
| `D02_O-INGRESSO_inteiro.png` | E-ticket 1080 × 1350 antes da entrega: canhoto preso. |
| `D02_O-INGRESSO_rasgado.png` | O mesmo depois da entrega: o picote abriu e o canhoto caiu. |
| `placeholders.json` | Caixa da foto em D01 (4:5, cantos 16 px). |

São geradores: `peca.html` receitas `D01` (`headliner`, `anos`, `cor`, `foto`) e `ingresso` (`headliner`, `cor`).
Refazer: `python _build/brand/lancamento.py D`.
