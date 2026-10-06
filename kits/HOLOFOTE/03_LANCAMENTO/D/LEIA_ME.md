# 03_LANCAMENTO/D · D01 A CARTEIRINHA, D02 O INGRESSO (§E.2)

| Arquivo | O que é |
|---|---|
| `D01_A-CARTEIRINHA_9x16.png` | Story 9:16: o cartão de fã-clube dos anos 80, plastificado (faixa de brilho de borda dura), cantos redondos, faixa de cima #2A2730 (aparece no campo preto), janela de foto de amostra (retícula de meio-tom desenhada por código + a Fã: "(a foto dela aqui)" com cantoneira) que o gerador troca pela foto. FÃ-CLUBE OFICIAL · MÃE · SÓCIO Nº 0001 · Membro desde: hoje · Atraso: 22 anos · Validade: vitalícia · Benefício: acesso total (sempre teve). |
| `D02_O-INGRESSO_inteiro.png` | E-ticket 1080 × 1350 antes da entrega: canhoto preso. O ingresso sai a 94 % (medida 752) para a versão rasgada caber na caixa 4:5 (x 140–940, y 64–1286). |
| `D02_O-INGRESSO_rasgado.png` | O mesmo depois da entrega: o picote rasgou (rasgo de papel, com o miolo do cartão em fibra nas duas bordas) e o canhoto caiu. |
| `placeholders.json` | Caixa da foto em D01 (4:5, cantos 16 px), onde o gerador põe a foto enviada. |

São geradores: `peca.html` receitas `D01` (`headliner`, `anos`, `cor`, `foto`) e `ingresso` (`headliner`, `cor`).
Refazer: `python _build/brand/lancamento.py D`.
