# HOLOFOTE · som · créditos e licenças

Verificado em **6 out 2026**, na página de origem de cada arquivo. Todas as fontes gravadas são **CC0 1.0**
(domínio público): uso comercial livre, **sem obrigação de atribuição**. Listamos assim mesmo, por cortesia e para
rastrear a origem.

Cada arquivo é baixado e conferido por SHA-256 em `_build/sound/fetch_sources.py`. Nenhum arquivo baixado é
executado: os zips são abertos pelo Python e só o áudio é lido.

## 1 · Gravações reais usadas (CC0 1.0)

| Fonte | Autor | Página (licença lida nela) | O que usamos | Onde entra |
|---|---|---|---|---|
| Impact Sounds (pack) | Kenney (kenney.nl) | https://kenney.nl/assets/impact-sounds · "License: Creative Commons CC0" + `License.txt` no zip | `impactBell_heavy_002.ogg` (só o ataque metálico) | sinos |
| RPG Audio (pack) | Kenney | https://kenney.nl/assets/rpg-audio · CC0 + `License.txt` | `metalLatch.ogg`, `bookClose.ogg`, `cloth1.ogg`, `knifeSlice.ogg`, `creak1-3.ogg` | CLAC, CLAC-off, ímã do case, pulseira, fósforo, cadeiras do murmúrio |
| UI Audio (pack) | Kenney | https://kenney.nl/assets/ui-audio · CC0 + `License.txt` | `click2.ogg`, `click3.ogg`, `switch7.ogg` | pulseira, ímã do case |
| Casino Audio (pack) | Kenney | https://kenney.nl/assets/casino-audio · CC0 + `License.txt` | `cards-pack-open-1.ogg` (o rasgo) | selo de papel |
| Applause in a large hall or church | eXpl0it3r | https://opengameart.org/content/applause-in-a-large-hall-or-church · "License(s): CC0" | o aplauso inteiro (39 s) | aplauso distante, rugido, fusão |
| Well Done (palmas) | qubodup | https://opengameart.org/content/well-done · CC0 (*"Changed to CC0 on 2024-10-05"*; gravação própria) | 4 palmas isoladas (t = 0,064 · 1,089 · 2,235 · 3,432 s) | todas as palmas, vinheta, fusão |
| Crowd shouting/speaking ambience | StarNinjas | https://opengameart.org/content/crowd-shoutingspeaking-ambience · CC0 (gravação própria) | 5 trechos, transpostos | rugido do estádio |
| Old man cough | AntumDeluge | https://opengameart.org/content/old-man-cough · CC0 (gravação própria) | 2 tossidas (t = 2,93 e 3,37 s) | tosse da plateia |
| Fire crackling | AntumDeluge | https://opengameart.org/content/fire-crackling · CC0 | estalos isolados | crepitar do pavio, fusão |
| Fireplace sound loop | PagDev | https://opengameart.org/content/fireplace-sound-loop · CC0 | o chiado fino (passa-altas 900 Hz) + estalos | crepitar do pavio, fusão |
| Flare ignition | qubodup | https://opengameart.org/content/flare-ignition · CC0 (*"a matchstick ignition sound recording I made"*, acelerado pelo autor) | a ignição, desacelerada 1,25× | fósforo *fsst* |
| Light switch turn on and off | FunnyDude | https://opengameart.org/content/light-switch-turn-on-and-off-sfx-0 · CC0 | os dois cliques | CLAC, CLAC-off |
| Various paper sound effects | Luckius | https://opengameart.org/content/various-paper-sound-effects · CC0 (feitos pelo autor) | `Paper Ripped - 1.wav` | selo de papel |
| The Shop (amostras grátis) | LEGIT Audio | https://opengameart.org/content/the-shop · CC0 (*"CC0 only applies to the free sounds provided via www.opengameart.org"*) | `…drinks_fridge_drone.wav` | elevador hidráulico |

**URLs dos arquivos e SHA-256:** em `_build/sound/fetch_sources.py` (lista `SOURCES`).

**⚠ Procedência não verificada além da declaração do autor:** *Fireplace sound loop* (PagDev), *Light switch*
(FunnyDude) e *Applause in a large hall* (eXpl0it3r) declaram CC0 na página, mas não dizem como o som foi gravado.
Os outros dizem que é gravação própria. Se um cliente exigir cadeia de direitos documentada, troque esses três.

## 2 · Vozes feitas por nós (não são gravações de pessoas)

O murmúrio da plateia e os gritos do estádio usam frases e vogais sintetizadas localmente com **Kokoro-82M**
(pesos **Apache-2.0**, lido no cartão do modelo: https://huggingface.co/hexgrad/Kokoro-82M) via **kokoro-onnx**
(**MIT**, https://github.com/thewh1teagle/kokoro-onnx). As frases são falas comuns de saguão de teatro, escritas por
nós (`walla_tts.py`). Nenhuma voz imita uma pessoa real. Na mixagem ficam abaixo da inteligibilidade, de propósito.

## 3 · Música: composição original

**FANFARRA HOLOFOTE** (`HLF-MUS-01`), 120 BPM, 20 s. Composta e sintetizada inteiramente em código
(`_build/sound/musica.py`), **sem nenhuma amostra gravada**, **sem melodia** e sem citar ritmo, canto ou
assinatura de nenhuma música, torcida ou artista. **Obra da SOL Estúdio**, cedida conforme a regra do estúdio.

## 4 · Sínteses (100 % código)

Aquecimento do filamento e zumbido de 120 Hz do CLAC · corpo grave dos interruptores · sinos (síntese modal com as
parciais do sino de Risset, afinado em si♭) · apitos de torcida · tom de sala · micro-estalos do pavio · motor e
chiado do elevador · todas as salas e reverberações (respostas impulsivas calculadas, não gravadas).

## 5 · Fontes descartadas

- **BBC Sound Effects:** licença não comercial. Não usado.
- **Pixabay** e **Freesound:** bloqueados por desafio Cloudflare a partir desta máquina. Nada baixado.
- **Wikimedia Commons:** a API respondeu *429 Too Many Requests* em todas as tentativas. Nada baixado.
