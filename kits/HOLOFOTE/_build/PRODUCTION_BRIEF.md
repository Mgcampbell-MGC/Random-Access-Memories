# HOLOFOTE — production brief (read this, then the platform)

**The source of truth is `../00_estrategia/CREATIVE_PLATFORM.md` (LOCKED).** Build exactly what it specifies: exact
Portuguese strings (accents, case, full stops), sizes, colours, fonts and layouts. This brief adds only the
founder's overrides, the file conventions and the tools. If this brief and the platform disagree, **this brief's
overrides win**; otherwise the platform wins.

## Founder overrides (6 Oct 2026) — these beat the platform

1. **No disclosure plates on any piece.** Delete every *"imagem ilustrativa criada com IA"*, *"render 3D
   ilustrativo · marca fictícia"* and *"… · publicidade"* plate from KVs, campaign images, films and ads. The founder:
   *"dont label the AD"*. Keep the y-band they occupied free (nothing else moves into it unless the layout needs it).
   *(The legal/lot copy printed ON the pack — "PROTÓTIPO FICTÍCIO · NÃO COMERCIALIZAR", "(FICTÍCIO)" tags in the
   manifesto, the fictional CNPJ — stays: it is pack design, not an AI label.)*
2. **No testimonial lines, ever** (CONAR applies to AI content). Presenters speak to *você* about *ela*.
3. Quality bar: **Wieden+Kennedy / Droga5 for the idea, Collins for the brand system.** "No AI slop." Every piece
   must survive a senior designer's eye at 100% zoom: optical kerning, filled measures, no orphan words, no
   misaligned baselines, real paper texture where the system says *O LAMBE*.

## Where things live

```
kits/HOLOFOTE/
  00_estrategia/          platform, research, concepts, judges (read-only)
  01_MARCA/               logo/ (done: SVG wordmarks + O FOCO), palette, type, system boards, devices, stickers
  02_PRODUTO/             label masters, dielines, packshots, chroma stand-ins
  03_LANCAMENTO/          KV, C-, B-, D-, STK-, L-series finals
  04_FILMES/              F15, F06A/B/C, S01 (with and without sound)
  05_ANUNCIO/             casting, scripts, prompts, previs animatics
  06_PRODUCAO/            machine files, fidelity reports
  07_KIT_COMPLETO/        zip + packet
  _build/                 code, fonts, tokens, intermediate files (commit sources, not caches)
    fonts/                OFFICIAL Google Fonts files (see below)
    tokens.css            colours + @font-face + voice classes
    logo.py               wordmark generator
    tools/html2png.py     HTML → PNG at an exact pixel size (Chromium)
    blender/candle_lib.py parametric candle studio (Cycles); render_scene.py JSON driver
```

## Fonts — use ONLY these files

`_build/fonts/SpecialGothicExpandedOne-Regular.ttf` · `SpecialGothicCondensedOne-Regular.ttf` ·
`SpecialGothic-VF.ttf` (axes wght 400–700, wdth 75–125) · `ShantellSans-VF.ttf` (wght 300–800, INFM, BNCE, SPAC).
**Never** download fonts through the Google Fonts CSS API with an old user agent: those files are subsets that drop
glyphs (HarfBuzz returned .notdef for every letter). Licences: OFL (copies in `fonts/`).

## Tools

- **Python:** `/home/user/venvs/web/bin/python` has Playwright, Pillow, numpy, OpenCV, uharfbuzz, fontTools.
  Blender: `/home/user/venvs/blender/bin/python` (bpy 4.5 LTS, Cycles CPU + OIDN). TTS: `/home/user/venvs/kokoro/bin/python`
  (`kokoro_onnx`, model files in `/home/user/maes_build/tts/`, voices `pf_dora` female PT-BR, `pm_alex` male PT-BR).
- **HTML → PNG:** `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers /home/user/venvs/web/bin/python _build/tools/html2png.py page.html out.png 1080x1350 [--transparent]`.
  Chromium is `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. Fonts load from `_build/fonts` via `tokens.css`
  (link it with a relative path or `file://` absolute path).
- **Type fitting:** "every line fills its measure" — solve it in the page with JS before the screenshot: measure with
  `getBoundingClientRect()` / canvas and adjust `font-size`, `letter-spacing` or `font-variation-settings: 'wdth'`
  until the line is within ±0,5 px of the measure. Use `font-feature-settings: 'tnum','lnum'` for figures.
- **Look at your output.** Open every PNG you produce with the Read tool and check it like a senior designer before
  you report it. A file that exists is not a file that is right.
- **CPU:** the machine has 4 cores shared by everyone. Blender test renders at ≤540 px and ≤32 samples unless you are
  making a final. Never run more than one Blender process at a time yourself.

## Conventions

- Filenames: `UPPERCASE_ID_descricao.png` (e.g. `KV-01_9x16.png`, `HLF-02_ROTULO_wrap.png`). PNG for masters, JPG
  (quality 92) only for previews.
- Colours: exact hexes from `tokens.css`. sRGB. No colour profiles other than sRGB.
- Every generator script is committed next to its output's family in `_build/` (e.g. `_build/pack/`,
  `_build/brand/`), runnable end to end with one command, and writes into the numbered folders.
- Write a short `LEIA_ME.md` (Portuguese, plain) in each numbered folder you fill: what each file is, in one line.

## The label wrap master (shared contract between the 2D and 3D teams)

- **One PNG per SKU / personalised unit: `9552 × 2560 px` = the full 360° circumference (238,8 mm) × the print zone
  (18,0–82,0 mm above the base), at exactly 40 px/mm.** Transparent background; ink pixels only, in the ink colour
  (PRETO-PALCO on amarelo/rosa/laranja, PAPEL-CARTAZ on violeta).
- **x = 0 is the centre of the LEFT side gap; the FRONT panel is centred at x = 2388 (arc 72,0 mm = 2880 px →
  x 948–3828); the BACK panel is centred at x = 7164 (x 5724–8604).** The side gaps stay empty.
- **y = 0 is 82,0 mm above the base; y = 2560 is 18,0 mm above the base.** Convert a platform baseline `b` mm to
  pixels as `y = (82,0 − b) × 40`.
- Also export a flat preview per master with the coating colour behind the ink (`…_wrap_preview.png`) and a
  `label_copy.json` with every string used (the platform §C.10 fields).

## Director's decisions after measurement (6 Oct 2026) — these amend the platform

- **Beauty view transform: `Khronos PBR Neutral`, look `None`, exposure ≈ −3,0** (not AgX). Measured on the HLF-02
  hero at one camera: AgX "Medium High Contrast" kept the hue (−1,3°) but halved the coating's saturation (chroma ÷
  lightness at 0,50 of the hex's): the amarelo read mustard (`#BEA845` against `#FFE81A`). Khronos PBR Neutral: hue
  −0,4°, saturation ratio 0,87. Standard view (the platform's colour-check transform) measures the same as Khronos.
- **The product is `_build/blender/holofote.py`** (`copo()`, `tampa()`, `use_size('200'|'080')`): glass, coating with
  the 1 mm clear lip, matte print shell UV-mapped to the wrap master, black capsule, wax with memory ring, wood wick,
  volume flame (wide and low; colour ramp tuned 1.750–2.700 K by eye because 1.400–1.900 K rendered salmon-pink under
  Khronos; the flame's point light stays 1.900 K), the lid in `on` or `stage` pose. Nobody else edits it.
- **Label fidelity on 3D renders: `_build/tools/fidelidade_uv.py`.** The print material writes AOVs (`label_uv`,
  `label_ink`, `label_mask`; `holofote.enable_label_aovs(exr_dir)`); the tool rebuilds the label in screen space from
  the master and compares tile by tile, with a planted error that must be caught. Calibration on the hero view:
  exact render worst tile 0,90–0,97 / 5th pct 0,98; planted error 0,17–0,19 (caught); a render whose label really said
  *MÃF* 0,025 (fail); AgX render fails on saturation (0,49 < 0,75).
  **Glyph-corner rule, 6 Oct 2026:** a tile counts only if ≥ 2 % of it is ink and ≥ 2 % paper. KV-45's one tile under
  0,80 (0,758) held 2 px of ink, the tip of a *v*, beside a shading band. With the rule: KV-45 worst 0,926 / p5 0,968,
  planted error −0,14 (caught); calibration exact still 0,90 / 0,98; the *MÃF* render still fails at 0,025. The verdict
  holds from 2 % to 10 %. Skipped tiles are counted in every report (`corner_tiles_skipped`, `corner_tiles_worst`).
- **Flame-legibility gate (§D.6), run 6 Oct 2026 — the swap is recorded.** KV-01 9:16 at the platform camera (50 mm,
  220 mm high, −6°, glass 384 px), downscaled to 108 × 192, flame isolated as lit − unlit: the **16 × 12 mm** wood-wick
  flame showed its warm core on **3 px (FAIL, bar ≥ 9)**; the **double-ply wood wick with a 14 × 18 mm flame** showed
  **10 px (PASS)**. `holofote.copo()` now defaults to `wick='double'`; pass `wick='single'` only for close-ups.
- **Brand decisions, 6 Oct 2026 (brand team's open questions):** (1) the wordmark is **9,03 × cap** at the advance
  width (8,90 at the ink); the platform's 9,273 is superseded by the font file. (2) **§D.1 wins over §D.3**: amarelo
  never touches laranja, so on laranja the lit O is preto, as on amarelo. (3) Width-axis values solved at the ink
  edge stand (CAMARIM 104, MAIS UM! 110, ACÚSTICO 100). (4) C07 follows its §E.2 row (PIX is its largest word).
  (5) `01_MARCA/cartazes/3d/` (albedo + height maps for the 3D wall) is regenerable and stays out of git.

- **S01 · DIGITANDO, 6 Oct 2026 (director).** Built in 2D by `_build/filmes/s01/s01.py` (Shantell on O MURO papel;
  the line never reflows, each line shows a prefix of itself). **It runs 10,83 s, not 6 s:** the platform's own counts
  (12 f per word, 18 f hold on the half-typed *d*, 2 f per deleted letter, 12 f per word) sum to 202 f = 8,4 s before
  the sign-off, and the rhythm is the joke. *domingo tô aí.* wraps to two lines (877 px on one line > the 800 px safe
  box). The sign-off lands on HLF-ID-01's first clap (measured 0,013 f off). Keys: Kenney UI clicks, CC0 (credited).

- **Copy and compliance review, 6 Oct 2026 — director's decisions (amend the platform):**
  1. **PREZINHO**, not *PRÉZINHO* (Lei 5.765/1971 dropped the accent in -zinho derivatives). Glass backs, posters,
     C09, ads 1B/1C, packet.
  2. **TURNÊ “VOCÊ”** with Brazilian curly quotes, not guillemets.
  3. **Refill safety:** *Retire o selo antes de usar. Encaixe a cápsula no copo HOLOFOTE limpo e frio.* on the carton;
     *Retire o selo antes de acender.* on every peel lid; refill disposal symbols papel · metal; HOLOFOTE on the main
     panel. **Case underside:** *O copo é seu. O resto, separe: papel, plástico e metal.*
  4. **Use line, every pack:** *Use a vela sempre dentro do copo. Apoie o copo sobre a tampa virada ou sobre
     superfície plana, firme e resistente ao calor.* (the old line read as three alternatives).
  5. **Planted-error masters live in `02_PRODUTO/rotulos/_controle/`**, never beside print masters.
  6. **C03/C07 thumbnails are composited AFTER O LAMBE.** The lambe pass re-inks and misregisters what it touches; it
     garbled the label. **C03:** 24 px above *DE PÉ* so the acute clears *APLAUDIU*.
  7. **Body text is ragged-right** in the brand book. Fill-the-measure is the display rule, not the body rule. No
     one-letter word at a line end; no single-word last line.
  8. **Dates are always DOMINGO · 09.05.** VO captions never duplicate on-screen type: drop *Sua vez.* /
     *holofote nela.* captions in 9–15 s.
  9. **Every lit-candle post carries** *Nunca deixe a vela acesa sem supervisão.* in its caption (§D.8.6).
  10. **S01 uses the 9:16 organic safe box** (x 140–940; sign-off centred at 540).
