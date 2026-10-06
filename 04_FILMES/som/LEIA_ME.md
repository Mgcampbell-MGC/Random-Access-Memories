# HOLOFOTE · som

Biblioteca de efeitos, identidade sonora, música e o som dos filmes. **Tudo em WAV 48 kHz / 24 bits, estéreo.**
Licenças e origem de cada som: `CREDITOS.md`.

## Como refazer tudo

```
bash _build/sound/construir.sh
```

Baixa as fontes e confere o SHA-256 → gera as vozes do público (TTS local) → música → efeitos e identidade →
filmes → PNGs de verificação. Leva de 4 a 6 minutos. **O resultado sai idêntico, bit a bit, a cada execução**
(todo sorteio tem semente fixa).

## Volume (normalização)

- **Efeitos (`sfx/`):** cada um com pico de loudness momentâneo de **−20 LUFS-M** e **true peak ≤ −1 dBTP**.
  Quando o pico não deixa, o ganho baixa (sem limitador, para não amassar o ataque). Por isso palmas e estalos
  ficam entre −21 e −26 LUFS-M.
- **Identidade, música e filmes:** **−14 LUFS integrado, ≤ −1 dBTP** (pyloudnorm, ITU-R BS.1770-4, com
  limitador true-peak).
- Os efeitos são material de biblioteca, não estão no volume final de uso. Exemplo: o tom de sala entra uns
  28–30 dB abaixo. Os ganhos usados de fato estão nos `*_cues.json` dos filmes.

## Ponto de sincronia

Em cada efeito, **o transiente cai num lugar conhecido**. Em geral é 0,020 s depois do início do arquivo; nos sinos
e nas palmas em série, é 0,000 s. O valor medido de cada arquivo está em `manifesto_sfx.json`
(`onsets_medidos_s`). Para pôr um efeito num quadro, use `"sync": "onset"` no `mix.py`: o **transiente** cai no
quadro, não o começo do arquivo.

## Arquivos

### `sfx/` — biblioteca

| Arquivo | O que é |
|---|---|
| `HLF-SFX-01_clac.wav` | CLAC: o refletor de teatro acende. Interruptor real + filamento que esquenta em 2 quadros (83 ms). |
| `HLF-SFX-02_clac_off.wav` | CLAC-off: blackout. O zumbido do refletor morre no clique (clique em 0,060 s). |
| `HLF-SFX-03_murmurio_teatro_loop.wav` | Murmúrio do público antes do show. Loop de 16 s sem emenda. |
| `HLF-SFX-04_rugido_estadio_0s8.wav` | Estádio explodindo, 0,8 s. Começa cheio e corta seco. |
| `HLF-SFX-05_aplauso_estadio_distante.wav` | Aplauso de estádio que cresce de longe. Pico de ~5 s até o fim (9 s). |
| `HLF-SFX-06a/b/c_palma_1/2/3.wav` | Uma palma de uma pessoa só, sala pequena e seca. Três palmas reais diferentes. |
| `HLF-SFX-06d_palmas_tres_0s3.wav` | Três palmas a 0,0 · 0,3 · 0,6 s (espaçamento da vinheta). |
| `HLF-SFX-06e_palmas_tres_10q.wav` | Três palmas a cada 10 quadros (0 · 0,417 · 0,833 s): F15 f312, F06A f100, F06B f120. |
| `HLF-SFX-06f_palmas_quatro_auditorio.wav` | Quatro palmas lentas no auditório vazio, com reverberação (Ad 1, gesto 6–9 s). |
| `HLF-SFX-07_fosforo_fsst.wav` | Fósforo: risca (0,020 s), acende, chia. |
| `HLF-SFX-08_crepitar_pavio_loop.wav` | Crepitar do pavio de madeira, o aplauso baixinho da marca. Loop de 12 s sem emenda. |
| `HLF-SFX-09_sino_teatro.wav` | Um golpe do sino do teatro, em si♭, golpe em 0,000 s. |
| `HLF-SFX-09a/b/c_sinal_1/2/3…wav` | 1, 2 ou 3 sinos em f0 / f8 / f16 a 24 fps (F06C 07.05, 08.05, 09.05). |
| `HLF-SFX-10_tosse_plateia.wav` | Uma tosse na plateia, algumas fileiras atrás, no silêncio. |
| `HLF-SFX-11_elevador_hidraulico_1s.wav` | O elevador do palco: motor, bomba, fluido. 1,0 s. |
| `HLF-SFX-12_ima_case.wav` | O CASE fechando: ar, papelão, o clac dos ímãs (contato em 0,050 s). |
| `HLF-SFX-13_pulseira_fecho.wav` | A PULSEIRA: a fita passa e o fecho trava (clique em 0,200 s). |
| `HLF-SFX-14_selo_papel_rrrip.wav` | O selo rasgando: *rrrr…ip*. Começa em 0,020 s; o *ip* final em 0,300 s. |
| `HLF-SFX-15_tom_de_sala_loop.wav` | Tom de sala pequena. Loop de 12 s; use bem baixo. |

### `identidade/`

| Arquivo | O que é |
|---|---|
| `HLF-ID-01_vinheta_ovacao_de_uma_pessoa_so_2s0.wav` | **A vinheta, *a ovação de uma pessoa só* (2,0 s).** CLAC em 0,000 → estádio de 0,100 a 0,900 → corte seco → três palmas numa sala pequena em 1,100 / 1,400 / 1,700 (medidos: 1,1005 / 1,4005 / 1,7000). |
| `HLF-ID-02_crepitar_para_aplauso_morph.wav` | **O pavio vira aplauso.** 0,0–0,5 s só o pavio; 0,5–2,0 s a fusão (1,5 s); 2,0–5,0 s o aplauso distante crescendo. Debaixo do crossfade, os estalos ficam mais rápidos e viram palmas. |

### `musica/`

| Arquivo | O que é |
|---|---|
| `HLF-MUS-01_fanfarra_120bpm_20s_mix.wav` | **FANFARRA HOLOFOTE**: fanfarra escolar, 120 BPM, 20 s, 10 compassos. Composição nossa. Masterizada. |
| `…_stem_caixas.wav` · `…_stem_bumbos.wav` · `…_stem_pratos.wav` | Stems: caixa + tarol, bumbo + surdo, pratos. |
| `…_stem_tambores.wav` | Os três stems somados. Os stems estão 5–6 dB abaixo do mix, para a soma não clipar (o valor exato está no JSON). |
| `HLF-MUS-01_pontos_de_edicao.json` | Compassos, pontos de corte (a cada 2,0 s = 48 quadros), golpes principais, trecho que faz loop (4–16 s). |
| `pecas/HLF-MUS-02_caixa_acento.wav` · `_bumbo.wav` · `_caixa_bumbo_juntos.wav` | Golpes avulsos para quadros fixos (F15 f44/f60/f84/f108; Ad 3: a caixa no dedo apontando). |
| `pecas/HLF-MUS-02_rufo_entrada_2s_pp_cresc.wav` | O rufo de entrada sozinho, 2 s, de pp a f. |

**Sem metais.** O roteiro pedia metais em si♭. Metais sintetizados não passam no padrão do estúdio sem um ouvido
humano, e nenhum de nós ouve. Um stem experimental sai com `musica.py --metais` em `_build/sound/_tmp/`, só para
alguém avaliar. **Não está aqui e não está no mix.**

**Estrutura:** c.1–2 rufo de entrada (pp→f) · c.3–8 marcha (bumbo nos tempos 1 e 3, surdo no 2 e no 4, caixa nas
semicolcheias, tarol no contratempo, pratos) · c.8 virada · c.9 breque (4 golpes juntos) · c.10 golpe final no
tempo 2 (18,5 s), soando até 20,0 s. Um tempo = 12 quadros; um compasso = 48 quadros.

### `filmes/` — o som de cada filme, pronto e já sincronizado

| Arquivo | Filme |
|---|---|
| `HLF-F15_A_ENTRADA_som.wav` | F15, 15 s, segue a tabela da plataforma quadro a quadro |
| `HLF-F06A_CLAC_som.wav` | F06A, 6 s. O aplauso corta seco no corte de imagem (f96); palmas em f100/110/120. |
| `HLF-F06B_O_PIOR_SHOW_som.wav` | F06B, 6 s. A marcha cai com um tempo por palavra (f0, f12, f24…); tosse no PIOR (f48). |
| `HLF-F06C_SINAL_07-05/08-05/09-05_som.wav` | F06C, as três datas: 1/2/3 sinos, CLAC em f72, depois a plateia (07 e 08) ou o pavio virando aplauso (09). |
| `HLF-AD_KV_9a15s_ads1e3_som.wav` | Cama dos 9–15 s dos anúncios 1 e 3 (t = 0 é 9,0 s no anúncio): CLAC → pavio → aplauso → palmas às 13,0 s. |
| `HLF-AD_KV_9a15s_ad2_sino_som.wav` | O mesmo para o anúncio 2: terceiro sinal às 9,0 s, 4 quadros de preto, CLAC… |
| `*_cues.json` | A lista de cues que gerou cada filme. Edite e rode o `mix.py`. |
| `*_som.json` | Loudness, cada cue, os quadros-chave e **os onsets medidos na mixagem final**. |

**Quadros-chave medidos:** todos caem a ±0,11 quadro do previsto.

Nos anúncios, a VO entra 6 dB acima da cama. Ao juntar, baixe a cama uns 8 dB por baixo da fala.

### `manifesto_sfx.json` e `verificacao/`

- `manifesto_sfx.json`: duração, loudness, true peak, ponto de sincronia e onsets medidos de cada efeito.
- `verificacao/VER-0*.png`: forma de onda, onsets (linhas azuis) e espectrograma de cada arquivo. Nos filmes, também
  a curva de loudness.

## As ferramentas (`_build/sound/`)

### `mix.py`: mixa uma lista de cues

```
/home/user/venvs/web/bin/python -I _build/sound/mix.py cues.json saida.wav
```

O `cues.json` é uma lista, ou `{"duracao_s": 15, "cues": [...]}`. Cada cue:

```
{"file": "sfx/HLF-SFX-01_clac.wav", "start_s": 0.5, "gain_db": 0, "fade_in": 0, "fade_out": 0}
```

Campos opcionais:

- `"frame": 12` no lugar de `start_s`;
- `"sync": "onset"`: o transiente principal do arquivo cai em `start_s`;
- `"trim_in_s"`, `"dur_s"`, `"loop": true` (para os `_loop.wav`);
- `"pan"` (−1 a 1);
- `"envelope": [[s, dB], …]` (para abaixar a música sob uma fala, por exemplo).

Os caminhos podem ser relativos ao JSON ou a `04_FILMES/som/`.

**Saída:** WAV estéreo 48 kHz a **−14 LUFS integrado, ≤ −1 dBTP**, e um `.json` ao lado com o desvio, em
quadros, de cada cue com `sync`. A loudness é medida com **pyloudnorm** (BS.1770-4), não com aproximação RMS.

### `onsets.py`: onde estão os transientes

```
/home/user/venvs/web/bin/python -I _build/sound/onsets.py arquivo.wav            # tabela: segundos, quadro, nível
/home/user/venvs/web/bin/python -I _build/sound/onsets.py arquivo.wav --json saida.json
/home/user/venvs/web/bin/python -I _build/sound/onsets.py mix.wav --snap 204 206  # confere ±1 quadro
```

Primeiro o **librosa** acha cada evento. Depois cada um é refinado até a **amostra**, onde o agudo (acima de
1,5 kHz) sobe 25 % do caminho entre o fundo e o pico. Assim um golpe de sino em cima do sino anterior, ainda
tocando, cai no lugar certo. Em sinos e palmas, a precisão medida foi de 1 ms.

**Para a equipe de imagem:** encaixe cada *slam* de tipo no onset medido na mixagem final (plataforma §E.5).

### Outros

| Arquivo | O que faz |
|---|---|
| `sfx.py` | Gera os efeitos e a identidade |
| `musica.py` | Gera a música |
| `filmes.py` | Escreve os cues e mixa os filmes |
| `walla_tts.py` | Gera as vozes do público |
| `fetch_sources.py` | Baixa as fontes |
| `dsp.py` | Filtros, salas, loudness, limitador |
| `analisar.py` | Números + PNG de qualquer áudio |
| `verificacao.py` | Gera os PNGs |

Nada disso vai para o git: `_build/sound/_fontes/` (fontes baixadas) e `_build/sound/_tmp/` (vozes e
rascunhos).

## O que é gravado, o que é sintetizado, e quão convincente deve soar

Ninguém da equipe ouviu estes arquivos: foram conferidos por números e por imagem. **Antes de aprovar, alguém
precisa ouvir.**

- **Real (gravação CC0, tratada):** as palmas, a tosse, o aplauso, o fósforo, o clique dos interruptores, o rasgo
  do papel, o crepitar (chiado e estalos de lareira de verdade), os cliques da pulseira e do ímã. **Devem convencer.**
- **Misto:**
  - **CLAC:** clique real + corpo e filamento sintetizados. Deve convencer.
  - **Rugido do estádio:** público real + ~110 vozes TTS + apitos sintetizados. É o mais arriscado: pode soar como
    "muita gente gritando *ê*" em vez de estádio. Com 0,8 s e o corte seco, provavelmente passa.
  - **Murmúrio:** 64 frases TTS espalhadas pelo teatro. Pode soar artificial de perto. É uma cama baixa.
  - **Elevador:** compressor real + motor sintetizado.
- **Sintético:**
  - **Sinos:** síntese modal. Sinos sintetizados costumam soar bem.
  - **Tom de sala:** indistinguível de um real nesse volume.
  - **Fanfarra:** caixa, bumbo, surdo e pratos modelados. Os **pratos** são o ponto fraco provável: podem soar
    metálicos demais. Ficam baixos no mix.

**Não verificado:**

- se alguma palavra das vozes TTS ou da gravação de multidão aparece inteligível;
- se os pratos soam baratos;
- se a fanfarra soa como uma fanfarra escolar brasileira, e não como bateria eletrônica.
