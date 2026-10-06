# HOLOFOTE · filmes

Os quatro filmes da plataforma (§E.4), 1080 × 1920, 24 quadros por segundo. **Cada filme sai duas vezes: com som e
mudo.** O mudo é a mesma imagem, sem áudio: todo o texto do filme já está na tela.

| Arquivo | O que é |
|---|---|
| `F15_A-ENTRADA_som.mp4` · `_mudo.mp4` | *A ENTRADA*, 15 s (360 quadros). O palco vazio, a escalação, o elevador traz a vela apagada, blecaute, a chama, o refletor volta, o cartão final. |
| `F06A_CLAC_som.mp4` · `_mudo.mp4` | *CLAC*, 6 s (144 quadros). O produto aceso, *A ATRAÇÃO É ELA.*, *abertura: você*, cartão final. |
| `F06B_O-PIOR-SHOW_som.mp4` · `_mudo.mp4` | *O PIOR SHOW*, 6 s. O cartaz amarelo palavra por palavra, *(girassol, 2007)*, corte para o produto com *SUA VEZ.* |
| `F06C_SINAL_07-05_som.mp4` · `_mudo.mp4` | *SINAL*, 7 de maio: *PRIMEIRO SINAL.* / *faltam 2 dias.*, a vela apagada. |
| `F06C_SINAL_08-05_som.mp4` · `_mudo.mp4` | *SINAL*, 8 de maio: *SEGUNDO SINAL.* / *é amanhã.*, a vela apagada. |
| `F06C_SINAL_09-05_som.mp4` · `_mudo.mp4` | *SINAL*, 9 de maio: *TERCEIRO SINAL.* / *é hoje.*, a vela acesa e a linha de segurança. |
| `som/` | O som de cada filme (equipe de som), já sincronizado; ver `som/LEIA_ME.md`. |

**Sem placa de "render 3D ilustrativo"** em nenhum quadro (decisão da dona, 6 out 2026). Só cortes secos, nunca fusão.
A embalagem nunca gira e só se move apagada (no elevador do F15).

**Codificação:** só pelo `_build/tools/codificar.py --fps 24` (cores convertidas E marcadas em BT.709). O som é o WAV
da equipe de som em AAC; a loudness medida está em `06_PRODUCAO/FILM_PLAN.json`.

**Como refazer** (de `kits/HOLOFOTE`):

```
_build/shots/blender.sh _build/filmes/f15_3d.py -- camA | blecaute | chama palco 0-23 | chama blecaute 210-223,228,229 | grua F0 F1 [--pct 50]
/home/user/venvs/web/bin/python _build/filmes/compor.py [F15 F06A F06B F06C_07-05 F06C_08-05 F06C_09-05]
/home/user/venvs/web/bin/python _build/filmes/fidelidade_filmes.py [mesmos nomes]
/home/user/venvs/web/bin/python _build/filmes/plano.py ; /home/user/venvs/web/bin/python _build/filmes/relatorio.py
```

O plano de montagem (`06_PRODUCAO/EDIT_DECISION_LIST.csv`), o registro completo (`06_PRODUCAO/FILM_PLAN.json`) e a
verificação do rótulo quadro a quadro (`06_PRODUCAO/fidelidade/<FILME>.json`) ficam em `06_PRODUCAO/`.
