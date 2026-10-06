# Codes research: the Gen Z visual and advertising language for a Brazilian Dia das Mães candle (2026–27)

Research date: 6 Oct 2026. Purpose: the visual and advertising codes a top agency would bring to a fictional Gen Z candle brand launching for **Dia das Mães, Sunday 9 May 2027**. It sits beside `culture.md` (the date, the audience, mum's vocabulary, the cringe list) and `category.md` (the candle shelf and prices). It does not repeat them; where they already answer a question, this file points there.

**Evidence rule.** Every number has a URL. A primary source is the platform's, standard-setter's or brand's own page; anything else is marked *secondary*. Where I state a craft opinion rather than a finding, it is labelled **studio rule** or **UNVERIFIED**.

**Raw captures** are in `research/raw_codes/`: the Google Fonts metadata (`gf_metadata.json`, fetched 6 Oct 2026), the font files and their descriptions (`fonts/`), TikTok's Portuguese trend report (`tt_whatsnext_ptbr.pdf/.txt`) and two TikTok safe-zone PDFs.

---

## 0. The twelve findings that matter most

1. **The platforms ask for the opposite of polish.** TikTok's own ad guidance: *"Adopt a DIY or not overly polished style"*, *"Introduce your content proposition in the first 3 seconds"*, *"Prioritize your hook in the first 6 seconds"*, and *"displaying 5-10 words per second when using text"* ([TikTok Ads Help, Creative best practices](https://ads.tiktok.com/help/article/creative-best-practices)). Canva's 2026 report (survey of 1.000 creators in the **US and Brazil**) calls the year **"Imperfect by Design"** ([Campaign Brief, 15 Dec 2025](https://campaignbrief.com/?p=305692), secondary). **So "Madison Avenue craft" here means craft that looks effortless, not craft that looks expensive.**
2. **The first three seconds carry about half the value.** Meta: *"up to 47% of the value in a video campaign was delivered in the first three seconds, while up to 74% of the value was delivered in the first ten"* ([Meta for Business](https://www.facebook.com/business/news/updated-features-for-video-ads)). The O ANÚNCIO rule keeps the product out until 9 s, **so the proposition must be carried in 0–3 s by type, caption and sound, never by the pack.**
3. **The tactile trend is literally a candle.** Pinterest Predicts 2026 names **"Gimme Gummy"** (*jelly blush* +130%, *jelly candy aesthetic* +100%) and **"Scent Stacking"** (*niche perfume collection* +500%, *scent layering* +75%) ([ppc.land summary of Pinterest Predicts, 9 Dec 2025](https://ppc.land/pinterest-unveils-21-consumer-trends-for-2026-advertising-campaigns/), secondary; Pinterest's own page not reachable). Adobe's 2026 list leads with *"Puffy, soft, and squishy textures"* ([Adobe Express](https://www.adobe.com/express/learn/blog/graphic-design-trends-2026)). **Translucent, subsurface-lit wax in Blender Cycles is the single most on-trend object we can render.**
4. **Handwriting is back, and Brazil has its own school hand on Google Fonts.** Pinterest's **"Pen Pals"** (*snail mail gifts* +110%, *cute stamps* +105%) and Canva's **"Notes App Chic"** (*"DIY and collage-inspired elements are up 90%"*) point the same way. **Playwrite BR** (TypeTogether, OFL) is built on the vertical cursive *"widely adopted"* in Brazilian schools ([google/fonts article](https://raw.githubusercontent.com/google/fonts/main/ofl/playwritebr/article/ARTICLE.en_us.html)). **It is mum's bilhete-na-geladeira hand, by construction, and almost nobody uses it** (popularity rank 1.989 on a scale that runs to 2.113 in Google's own metadata; only 70 families rank lower).
5. **TikTok's native caption face is now a free OFL font.** *"You may recognize this font as the default font used in millions of TikTok videos"* ([TikTok Sans on google/fonts](https://raw.githubusercontent.com/google/fonts/main/ofl/tiktoksans/article/ARTICLE.en_us.html)). Setting speech captions in TikTok Sans makes a studio ad read as a native post. **Verified: full Portuguese diacritics.**
6. **The two "current" fonts everyone reaches for are already default.** Bricolage Grotesque and Instrument Serif rank **53rd and 73rd in popularity of ~1.950 Google families**, alongside Fraunces (88th). They signal 2024–25 startup. **Use them as support at most; the hero face must be less common.**
7. **Three agency-made OFL fonts from 2025 cannot set Portuguese.** BBH Bartle and BBH Hegarty (Studio DRAMA, Dec 2025) contain **134 glyphs and none of ã õ ç á é í ó ú â ê ô à**, checked in the font files. **Banned.** Every other family recommended below was checked glyph by glyph.
8. **Sound is not optional on either platform.** TikTok: **88%** of users say *"sound is vital to the TikTok experience"* (Nielsen, Jul 2020); brand recall rises *"over 8x"* with *"distinctive brand sounds"* (Ipsos, 2020) ([TikTok Business blog](https://ads.tiktok.com/business/en-US/blog/evolution-of-sound-volume-1)). Meta: *"Over 75% of Reels views on Instagram are sound on"* ([Meta for Developers, Nov 2024](https://developers.facebook.com/blog/post/2024/11/07/unlock-the-power-of-reel-ads/)). **The brand needs a sonic mnemonic, and a candle owns one: the match strike.**
9. **The safe zone is the bottom third.** Meta: *"leaving at least 14% of the top, 35% of the bottom, and 6% on each side of your asset free from text, logos, or other important creative elements"* ([Meta Ads Guide, Reels video](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)). TikTok publishes no single number; its safe zone *"is determined by the dimension… ad caption length, and any additional formats used"* ([TikTok Ads Help](https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads)). **Studio box for 1080×1920: x 120–920, y 270–1240** (§6).
10. **Disclosure rules are now written down in Brazil and on TikTok.** CONAR's 2026 influencer guide covers *"avatares… inclusive os gerados por computação"* and asks for the identification *"de forma fixa e legível… em nítido contraste com o fundo, sem interferência de outros elementos em sobreposição"* ([CONAR Guia 2026](https://conar.wpenginepowered.com/wp-content/uploads/2026/05/260525_GUIA_INFLUENCIADORES_CONAR_v6.pdf)). TikTok rejects undisclosed AI content and accepts *"a clear disclaimer, caption, watermark, or sticker of your own"* ([TikTok ads policy, updated Apr 2026](https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content)). **The disclosure is a designed element of the frame, not small print.**
11. **Humour is the most-engaged motherhood register in Brazil.** Natura's agency cites Winnin IA: between Apr 2024 and Apr 2025, *"Beauty & Cosmetics"* and *"Humor"* were the most engaged themes associated with motherhood ([Propmark, 25 Apr 2025](https://propmark.com.br/anunciantes/natura-lanca-campanha-de-dia-das-maes-e-celebra-a-maternidade/)). **And the 2026 cautionary tale is AI itself:** Coca-Cola's AI remake of "Holidays Are Coming" was called *"creepy"* and *"soulless"* ([Adweek](https://www.adweek.com/creativity/how-coca-colas-ai-holiday-ad-went-from-praise-to-rage/)). Gen Z can smell slop.
12. **TikTok's Portuguese playbook gives the presenter grammar.** Its 2025 PT-BR report lists **"contato visual direto"** (*"filmado da perspectiva do observador… interagindo diretamente com o espectador"*), **"material de meme"**, **"palavras de afirmação"** and **"emoção humana"** (*"adição de olhos e lábios expressivos ao seu produto ou… um mascote"*) ([TikTok What's Next 2025, PT-BR PDF](https://ads.tiktok.com/business/library/Whats_Next_Report_Tendencias_pt_BR.pdf)). **The flame can be the character; the pack never has to move.**

---

## 1. Typography

### 1a. What the trend sources say (2026)

- **Adobe, 2026:** *"Oversized sans-serifs, bubbly and puffy letterforms, and wavy, distorted, bubble-like fonts"*, plus *"handwritten scripts and loopy cursives"* and *"hand-rendered and letterpress-inspired fonts"* ([Adobe Express](https://www.adobe.com/express/learn/blog/graphic-design-trends-2026)).
- **Canva, 2026:** the counter-trend **"Opt-Out Era"**: *"Searches for 'clean layout,' 'serif,' and 'simple branding' climbed 54%"* ([Campaign Brief](https://campaignbrief.com/?p=305692), secondary). So the year is split: **puffy display type on one side, a calm serif on the other.** A good system uses both.
- **Practitioner round-ups** list "funky curvy serifs", "cute and cosy fonts" and "chaotic scripts" as the 2026 moves ([Made Good Designs](https://madegooddesigns.com/web-typography-trends-2026/), secondary, vendor blog).

### 1b. Verified shortlist (all OFL, all on Google Fonts, all checked for Portuguese)

Method: each family's licence was read from its `METADATA.pb` in [github.com/google/fonts](https://github.com/google/fonts) (`license: "OFL"` for every row); the font file was downloaded and its character map checked for **ã õ ç á é í ó ú â ê ô à ü € ª º “ ” ‘ ’ – — …** (all present in every row). Date added, axes and the popularity rank (lower = more used; 1.950 families, ranks running 2–2.113) come from Google's own [metadata endpoint](https://fonts.google.com/metadata/fonts), fetched 6 Oct 2026.

| Family | Added | Popularity rank | Axes | Why it fits | Role |
|---|---|---|---|---|---|
| **Sour Gummy** | Nov 2024 | 1.053 | wdth, wght | Letters *"designed to look like they are made of bubbles"* ([article](https://raw.githubusercontent.com/google/fonts/main/ofl/sourgummy/article/ARTICLE.en_us.html)). The width axis lets the word **squash and spring** on a beat: Gimme Gummy in type. | Display, kinetic |
| **Bagel Fat One** | Jun 2023 | 995 | — | *"Very heavy/fat… inspired by bread, pastries and sweets"* (JAMO). Reads like a bentô-cake top. Full Latin despite being a Korean family. | Display headline, stickers |
| **DynaPuff** | May 2022 | 791 | wdth, wght | Designed for *"zomg's"*; OpenType that *"alternates the vertical position of the letters"* so *"noooooooooo waaaaaaay"* looks hand-drawn (Toshi Omagari, Jennifer Daniel). Texting energy without slang. | Chat-UI, stickers |
| **Fraunces** | Jul 2020 | 88 | **SOFT, WONK**, opsz, wght | *"The Softness axis controls the 'wetness' or 'inkiness'"* ([description](https://raw.githubusercontent.com/google/fonts/main/ofl/fraunces/DESCRIPTION.en_us.html)). **Animate SOFT 0→100 and the serif melts like wax.** Popular, but the motion use is not. | Wordmark candidate, film type |
| **Young Serif** | Sep 2023 | 648 (trending 134) | — | Heavy old-style; the rounded *b* and *f* add *"a tender and generous quality"*. The "Opt-Out Era" serif with warmth. | Calm serif, store copy |
| **Gloock** | Jan 2023 | 534 (trending 171) | — | High-contrast headline serif *"inspired by newspaper's headlines"* (Duarte Pinto). Deadpan announcements ("Comunicado oficial"). | Fake-serious headlines |
| **Playwrite BR** | May 2024 | 1.989 | wght | The Brazilian school vertical cursive; *"the replacement of… Palmer… with the vertical cursive approach"* (TypeTogether, Burian, Scaglione). **Mum's hand.** Connected cursive: 2–8 words only, never body copy. | Handwritten notes, gift tag |
| **Shantell Sans** | Jan 2023 | 717 | **BNCE**, INFM, SPAC, wght | Marker hand by artist Shantell Martin with Arrow Type; a **bounce** and an **informality** axis to animate. | Annotations, arrows, scribbles |
| **TikTok Sans** | 2025 | 660 | opsz, slnt, wdth, wght | *"The default font used in millions of TikTok videos"*; *"Optimized for high-DPI mobile UI typesetting"*. | **Speech captions** |
| **Doto** | Nov 2024 | 1.031 (trending 135) | ROND, wght | Dot-matrix on *"a 6x10 reference matrix"*. **The cupom fiscal and the thermal receipt printer.** | Receipt device, prices |
| **Special Gothic Expanded One** | Apr 2025 | 512 (family trending 53) | — | Wide grotesque *"created for… Special Group"* (an agency) as a *"reimagining of the raw tenacity"* of early Gothic type. Poster punch; lambe-lambe energy. | Poster/OOH headline |
| **Coiny** | Jun 2016 | 923 | — | *"Inspired by the vernacular designs seen around every big city… a rounded brush point"* (led by Marcelo Magalhães, who also drew Londrina). Brazilian *letreiro* warmth. | Shopfront-sign headline |
| **Comic Relief** | Apr 2025 | 377 | — | *"Metrically equivalent to the popular Comic Sans MS"*. **Only** for an affectionate parody of mum's *bom dia* image. | Parody only |

**Do not use as hero:** Bricolage Grotesque (rank 53), Instrument Serif (73), Fraunces as a static serif (88), Geist (101). They are fine as support. **Do not repeat the studio's previous kits:** AVELUNE and VOLTA used Cormorant Garamond + DM Sans; FAÍSCA used DM Sans (read in `ref/`). **Banned:** BBH Bartle, BBH Hegarty and BBH Bogle (no Portuguese accents); Honk (Indian truck-art lettering: wrong culture for a Brazilian mum).

### 1c. Three type systems to test (studio proposals)

| System | Headline | Support | Hand | Captions | Reads as |
|---|---|---|---|---|---|
| **A. Recado** | Bagel Fat One | Young Serif | Playwrite BR | TikTok Sans 800 | A fridge note from mum, set in a sweet shop |
| **B. Comunicado** | Gloock (deadpan) | Host Grotesk or Funnel Sans | Shantell Sans | TikTok Sans 800 | A very serious memo about something silly |
| **C. Derrete** | Fraunces variable (SOFT animated) | Sour Gummy for stickers | Playwrite BR | TikTok Sans 800 | The type itself melts and wobbles like wax |

### 1d. Technical notes for our pipeline

- **Variable axes in Blender:** set label and 3D type from **static instances**, cut with `fontTools.varLib.instancer` (fontTools 4.66 is installed). Whether Blender's text object reads variable axes was not tested here: **UNVERIFIED**, and instancing makes the question moot.
- **Kinetic type** (HyperFrames renders in Chrome): `font-variation-settings` is animatable, so the SOFT, wdth and BNCE ideas are free in the film.
- **Colour fonts (COLRv1)** such as Honk or Nabla need Chrome; Blender cannot render them. Not recommended anyway.
- **Label type** is set by code from the master file; none of this changes rule 1 (the generator never draws the pack).

---

## 2. Colour

### 2a. The sources

| Source | What it names | Note |
|---|---|---|
| **Pantone Colour of the Year 2026** | **11-4201 Cloud Dancer**, *"a billowy, balanced white"* (announced 4 Dec 2025) | [NBC News](https://www.nbcnews.com/pop-culture/pop-culture-news/pantone-names-2026-color-year-rcna247366), secondary. Hex **#F0EEE9** is a converter value ([hextoral](https://hextoral.com/hex-color/F0EEE9/pantone-fashion-home-interiors/), secondary); Pantone's own page not fetched. |
| **WGSN × Coloro Colour of the Year 2027** | **Luminous Blue, Coloro 125-28-38**, *"both mysterious and eccentric"* | [WGSN press release, 29 Apr 2025](https://www.wgsn.com/en/wgsn/press/press-releases/wgsn-and-coloro-reveal-colour-year-2027-luminous-blue-and-s-s-27-key). No hex published. |
| **WGSN S/S 27 key colours** | **Energy Orange 018-57-34 · Pop Pink 151-73-22** (*"joyful, uplifting and carefree"*) **· Meadowland Green 050-61-19 · Clay 014-60-13** | Same release. **Our launch is inside the S/S 27 window.** (May is autumn in São Paulo; global social palettes still flow.) |
| **Pinterest Predicts 2026** | **Cool Blue** (*frosted makeup* +150%) · **Gimme Gummy** · **Laced Up** (*lace doily* +105%) · **FunHaus** (*circus interior* +130%, *striped ceiling* +40%) · **Extra Celestial** (*opalescent* +115%) | [ppc.land](https://ppc.land/pinterest-unveils-21-consumer-trends-for-2026-advertising-campaigns/), secondary. Gen Z drives two-thirds of the list ([YPulse](https://www.ypulse.com/newsfeed/2025/12/10/gen-z-is-driving-two-thirds-of-pinterests-predicted-trends-for-2026/), secondary). |
| **Adobe 2026** | *"Bright, saturated color palettes"*; *"bold contrasts and vibrant color clashes"* | [Adobe Express](https://www.adobe.com/express/learn/blog/graphic-design-trends-2026) |
| **Brat green #8ACE00** | Charli XCX, *brat*, 7 Jun 2024 | [The Nightly](https://thenightly.com.au/politics/brat-green-aka-hex-8ace00-you-cant-escape-this-colour-thanks-to-charlie-xcx-c-15494520), secondary. **By May 2027 it is a 2024 reference. Avoid.** |
| **The Brazilian candle shelf** | 8 of 11 sampled Brazilian candles were clear or frosted glass; **none was an opaque saturated vessel; none carried big type** | `category.md` §0. **Colour is the open lane on the shelf.** |

**Hex values below are studio targets chosen by eye.** The Coloro codes are not convertible to sRGB without Coloro's own tools, so the "Luminous Blue" and "Pop Pink" hexes are **approximations, not official conversions**. Use a physical Coloro or Pantone guide before any print.

### 2b. Four palettes, with measured contrast

Contrast ratios computed with the WCAG 2.2 formula; the bar is **4.5:1 for normal text, 3:1 for large text** (*"at least 18 point or 14 point bold"*) ([W3C WCAG 2.2, SC 1.4.3](https://www.w3.org/TR/WCAG22/#contrast-minimum)).

**A. Recado na geladeira** (fridge note, BIC-blue ink)
- Post-it **#FFE45C** · paper **#FFF8E7** · caneta-azul ink **#1F3FBF** · tomato **#E8412C** · magnet black **#141414**
- Ink on post-it **6,55:1** · ink on paper **7,87:1** · black on post-it **14,48:1** · tomato on paper **3,80:1** (large type only)

**B. Bom dia, flor** (post-ironic WhatsApp *bom dia* image; see `culture.md` #8)
- Magenta **#E6007E** · sky **#6EC8FF** · glitter gold **#F2C230** · leaf **#2FA84F** · white
- White on magenta **4,50:1** (just passes) · black on sky **9,97:1** · white on leaf **3,07:1** (large only) · **gold on magenta 2,69:1: decoration only, never text**

**C. Gelatina** (Gimme Gummy × Pop Pink × Luminous Blue × Cloud Dancer)
- Pop pink **#FFB3CF** · hot pink **#FF6FAE** · cherry **#C8102E** · lapis (Luminous Blue approx.) **#2B3A9C** · butter **#FFE7A3** · Cloud Dancer **#F0EEE9**
- Cherry on Cloud Dancer **5,07:1** · lapis on pop pink **5,76:1** · Cloud Dancer on lapis **8,28:1** · lapis on butter **7,87:1** · **white on hot pink 2,58:1: fails; use #141414 (7,14:1)**

**D. Toalhinha de crochê** (Laced Up, grandmillennial, mum's living room)
- Doily cream **#F6EEDC** · lilac **#B9A3E3** · avocado-kitchen green **#6B7F2E** · terracotta clay **#B85C3E** · plum ink **#2A2230**
- Plum on doily **13,27:1** · plum on lilac **6,87:1** · doily on avocado **3,87:1** (large only) · terracotta on doily **3,92:1** (large only)

**Studio recommendation (opinion):** C or A. **C is the most rendered-object-friendly** (pink and cherry wax under subsurface light, a lapis seamless, a butter plinth) and the most distinct from a shelf of frosted glass. **A is the most Brazilian** (BIC blue is the ink of every bilhete) and the most ownable as a system. D is the strongest *mum's house* palette but drifts toward cosy and away from fun.

---

## 3. Graphic devices: evidence, execution, risk

Each device must work inside the studio rules: type by code, pack composited, no AI edit after compositing.

| Device | Evidence it is current | How we make it | Risk / rule |
|---|---|---|---|
| **Gummy / squishy 3D** | Pinterest "Gimme Gummy"; Adobe *"Puffy, soft, and squishy textures"*; Brisk revived claymation for Gen Z in 2024 with Doja Cat, noting the nostalgia window has moved to Y2K ([Marketing Dive](https://www.marketingdive.com/news/brisk-iced-tea-doja-cat-claymation-campaign-trail/727288/)) | Cycles: wax with subsurface scattering, slightly translucent; clay-like props (rounded primitives, bevel + fine noise bump for fingerprints); soft key light | Gloss and glow are the AI-slop tell; keep fingerprints, micro-dust and a wick that is not perfectly straight |
| **Notes-app / scrapbook** | Canva "Notes App Chic": *"lo-fi cut-and-paste… handwriting… layouts that appear unfinished"*, +90% ([Creative Bloq on Canva 2026](https://www.creativebloq.com/design/canvas-2026-trend-predictions-have-filled-me-with-hope), secondary) | Code-set Notes-style panels (system-neutral, our own type), masking-tape PNGs drawn in vector, Playwrite BR scribbles | Do not reproduce Apple's Notes UI exactly; make a generic "nota" with our colours |
| **Chat-UI parody** | DoorDash, *"The Real Moms of the Group Chat"* and an animated-memes spot for Mother's Day 2026 ([Marketing Dive](https://www.marketingdive.com/news/doordash-delivers-memes-reality-tv-moms-for-mothers-day-campaign/819175/)); Usaflex's WhatsApp voice notes for Dia das Mães 2026 ([Marcas pelo Mundo](https://marcaspelomundo.com.br/anunciantes/usaflex-cria-experiencia-com-audios-de-whatsapp-para-homenagear-maes/)); Brazilians send 4× more voice notes (`culture.md` #8) | A **generic** messenger: our bubble colours, our type (DynaPuff for mum, TikTok Sans for the child), ticks, *"digitando…"*, a voice-note waveform, a group called *"Família"*, a forwarded label | **WhatsApp's brand rules:** *"DON'T use the WhatsApp Brand Resources in a way that implies partnership, sponsorship, or endorsement"* and do not *"modify colors, design, or combine logos with other artwork"* ([Meta brand resources](https://www.meta.com/brand/resources/whatsapp/whatsapp-brand/)). No WhatsApp logo, name or exact green. |
| **Receipt / cupom fiscal** | Receiptify turned Spotify data into till receipts ([Yorkshire Post](https://www.yorkshirepost.co.uk/read-this/heres-how-people-are-making-receipts-of-their-top-spotify-tracks-2981151), secondary); Spotify Wrapped lineage (§7) | Doto or Geist Mono on a long thermal strip: *"1× casaquinho que você não levou… R$0,00"*, *"TOTAL: impagável"*. Render the strip in Blender (slight curl, thermal grey) or flat in code | **Never fake a Pix comprovante.** Pix is a BCB mark governed by a *Manual de Uso da Marca* (v1.6, Jun 2025, secondary: [Finsiders](https://finsidersbrasil.com.br/?p=354131)), and from 1 Mar 2027 the BCB bans *"propaganda, publicidade… ou quaisquer conteúdos não relacionados à transação"* in real Pix receipts ([Poder360, 3 Sep 2026](https://www.poder360.com.br/poder-economia/BC-proibe-propaganda-em-comprovantes-de-pagamento-do-pix/)). Say "Pix" in copy if needed; never draw its logo or receipt. |
| **Hand-drawn notes and stamps** | Pinterest "Pen Pals"; Adobe *"photos, doodles, stamps, and brush textures"* | Playwrite BR for mum's notes, Shantell Sans for the child's arrows; vector stamp borders and a postmark with the date **09.05.27** | Keep handwriting short; connected cursive drops legibility fast at caption size |
| **Stickers / figurinhas** | Brazilians send more WhatsApp stickers than any other country (Zuckerberg in São Paulo, via [Mobile Time](https://www.mobiletime.com.br/?p=579511), secondary) | Die-cut vector stickers with a white keyline and a soft drop shadow; also ship them as a real WhatsApp sticker pack (a gift-with-purchase that travels) | **Flork is someone else's character** (Flork of Cows, 2012, per [Canaltech](https://canaltech.com.br/internet/o-que-e-o-flork-meme-e-como-o-fantoche-foi-parar-em-bolos/)); draw our own Paint-style doodle, do not copy |
| **Product-as-character** | TikTok PT-BR: *"adição de olhos e lábios expressivos ao seu produto ou… um mascote"* | **The flame is the character.** Vector googly eyes or a tiny drawn face on the flame, added in code to the rendered still, never to a generated scene | The label stays untouched; the face sits on the flame or a sticker, never across the label |
| **Opalescent instead of Y2K chrome** | Pinterest "Extra Celestial" (*opalescent* +115%) and "Neo Deco" (*brass aesthetic* +35%) | Blender 4.2+ Principled BSDF **Thin Film** for a pearlescent lid or a soap-bubble badge (*"Thin Film simulates the effect of interference in a thin film"*; *"not yet supported by EEVEE"*; dielectric only at launch) ([Blender 4.2 Cycles notes](https://developer.blender.org/docs/release_notes/4.2/cycles/)) | Full chrome 3D type reads 2021–23; one iridescent accent, not a chrome world. **Render in Cycles, not EEVEE.** |
| **Lace / doily** | Pinterest "Laced Up" (*lace doily* +105%, *lace nails* +215%) | A vector crochet-doily pattern as the gift-box liner or a coaster under the candle in the set | Reads "grandma" fast; one element, used with a wink |
| **Stripes / FunHaus** | Pinterest "FunHaus" (*striped ceiling* +40%) | Awning-stripe seamless backdrop or box wrap (candy-shop) | Easy to over-do; pair with one calm serif |
| **São Paulo lambe-lambe** | Woodtype street posters now kept alive by Gráfica Fidalga in Vila Madalena ([Rico Lins](https://www.ricolins.com/en/?p=5616), secondary; [ESPM paper](https://dialogo.espm.br/revistadcec-rj/article/download/2026/2186/2299)) | Wide grotesque (Special Gothic Expanded One / Coiny), stacked lines, two flat colours, slight misregistration, as the OOH and carousel format | The fluorescent-ink look is **UNVERIFIED** as a Fidalga trait; treat as reference, and commission a real print later if the campaign grows |

---

## 4. The 15-second vertical ad

### 4a. What the platforms say

| Claim | Source |
|---|---|
| *"Introduce your content proposition in the first 3 seconds for better recall and awareness"*; *"Prioritize your hook in the first 6 seconds"* | [TikTok Ads Help](https://ads.tiktok.com/help/article/creative-best-practices) |
| *"Use captions or text overlays… We recommend displaying 5-10 words per second when using text"* | same |
| *"between 3-5 different creatives per ad group"* | same |
| *"up to 47% of the value… in the first three seconds… up to 74%… in the first ten"*; *"65% of people who watch the first three seconds… will watch for at least ten seconds and 45% continue watching for thirty"*; *"captioned video ads increase video view time by an average of 12%"* (Nielsen and Fors-Marsh research cited by Meta; undated) | [Meta for Business](https://www.facebook.com/business/news/updated-features-for-video-ads) |
| *"Over 75% of Reels views on Instagram are sound on"*; Reels ads gave *"14% higher average brand lift"* | [Meta for Developers](https://developers.facebook.com/blog/post/2024/11/07/unlock-the-power-of-reel-ads/) |
| 88% say sound is vital (Nielsen 2020); recall *"over 8x"* with distinctive brand sounds (Ipsos 2020) | [TikTok Business](https://ads.tiktok.com/business/en-US/blog/evolution-of-sound-volume-1) |
| Business accounts on TikTok use the **Commercial Music Library**, pre-cleared, TikTok placements only | [Soundstripe](https://www.soundstripe.com/blogs/tiktok-music-library-explained), secondary. **Studio rule already in force: use AI-made tracks assigned to Sol, so one track works on both platforms.** |

### 4b. The beat sheet (O ANÚNCIO, inside the fixed 0–6 / 6–9 / 9–15 structure)

| Time | What happens | Carries the proposition by |
|---|---|---|
| **0,0–0,3 s** | Open **mid-sentence, mid-gesture**. No logo sting, no fade from black, no "oi gente". | The first spoken word |
| **0,0–1,5 s** | **Hook**: spoken line ≤7 words + an on-screen text hook ≤6 words naming the **occasion and the tension** (e.g. *"dia das mães · 9/5"* + *"pix não tem cheiro"*). | Type and voice, never the pack |
| **1,5–6,0 s** | **The turn**: mum's own phrase quoted back with love (`culture.md` §4). Word-synced captions. Presenter looks into the lens (*contato visual direto*). | Caption + one brand-coloured sticker |
| **6,0–9,0 s** | **The beat**: a silent reaction or gesture; a sticker pops; **the sonic logo: match strike + flame "whoomp"**. | Sound |
| **9,0–15,0 s** | **Key visual**: composited pack, flame lit (3D render), name, one line, CTA (*"chega até 9 de maio"*), disclosure throughout. | The product, at last |
| **15,0 s** | **Loop seam (studio rule):** last frame rhymes with the first so a rewatch feels continuous. **UNVERIFIED** as a performance effect. | — |

**Three hook archetypes to write the 2–3 alternative openings (studio proposals, all in the child's voice, none a testimonial):**
1. **The quote:** text *"“chegou?” — sua mãe, desde sempre"*; presenter: *"Se a sua mãe ainda manda 'chegou?' toda vez que você sai… vem cá."*
2. **The tension:** text *"pix não tem cheiro."*; presenter: *"Dia das Mães tá chegando e você ia mandar um Pix. Respeito. Mas…"*
3. **The deadpan memo:** Gloock headline *"COMUNICADO OFICIAL"*; presenter: *"Atenção, filhos do Brasil. Isto é um comunicado."*

**Avoid** in hooks: first-person use or purchase (*"eu uso"*, *"comprei"*, *"minha mãe amou"*), results claims (*"acalma"*, *"relaxa"*), Gen Z slang as the joke (`culture.md` §6), and any joke whose target is mum's age, body or tech skills.

### 4c. The product film (kinetic type + 3D, no people)

- **Studio rule:** the same 0–3 s law applies: open on a moving word, not a slow push-in on a jar.
- Devices that suit a 15 s type-and-object film: the **melting serif** (Fraunces SOFT 0→100 as the flame is lit); **gummy squash** on the brand name (Sour Gummy wdth on the beat); a **receipt printing** in Doto; a **chat thread** typing out mum's phrases, answered by the candle lighting.
- Sound: match strike as the logo; wax "crackle" from a wood wick if the product has one (`category.md` §0 lists wood wicks as a category option).

---

## 5. Presenter tone in Brazilian Portuguese

**What the sources set:**
- **The register.** Humour is the most-engaged motherhood theme (Winnin IA via [Propmark](https://propmark.com.br/anunciantes/natura-lanca-campanha-de-dia-das-maes-e-celebra-a-maternidade/)); Natura's line is *"situações reconhecíveis ajudam a gerar conexão e senso de comunidade"*. 70% of Brazilian Gen Z approve of brands using memes, but forced slang turns *cringe* at once (`culture.md` §3).
- **The camera grammar.** TikTok PT-BR: *contato visual direto*, *material de meme* (*"criadores e marcas acrescentando as próprias adaptações dos memes do momento"*), *palavras de afirmação* ([PT-BR report](https://ads.tiktok.com/business/library/Whats_Next_Report_Tendencias_pt_BR.pdf)).
- **The legal frame.** CONAR treats virtual and computer-generated presenters as influencers and applies every rule, including testimonials, to AI content: the chain *"permanece[m] responsáveis"* and the ad must not contain *"simulações, endossos ou testemunhais"* that mislead ([CONAR Guia 2026](https://conar.wpenginepowered.com/wp-content/uploads/2026/05/260525_GUIA_INFLUENCIADORES_CONAR_v6.pdf)). It also says it creates no new AI-disclosure duty (see `label_rules.md` §9). **TikTok does**, so we disclose on every cut regardless.

**How she talks (studio rules, built on the above):**
1. **Deadpan, not hype.** No "influencer voice", no rising sing-song, no *"gente, vocês não vão acreditar"*. Dry, then warm. The punch lands on a pause.
2. **Speaks as the child, about mum, with love.** The joke is always on the child (the forgotten *casaquinho*, the unanswered *"chegou?"*), never on mum.
3. **Mum's vocabulary, not Gen Z slang.** Quote *"leva um casaquinho"*, *"já comeu?"*, *"me avisa quando chegar"*; allow *POV:* as a format at most (`culture.md` §4e).
4. **Lower-case captions, short lines, one punctuation mark.** The 2021 *cringe* list includes *"perfect grammar with capitalised sentences"* and *rsrsrs* (`culture.md` §3).
5. **Neutral São Paulo urban accent, natural pace.** Script 0–6 s to **≤100 characters (≈14–16 words)** so captions stay under 17 characters per second (§6).
6. **Never holds or describes using the product.** The product is a still at 9 s; she reacts *to* it at most.

---

## 6. Captions and safe zones (9:16)

### 6a. The safe zone

| Source | Top | Bottom | Left | Right |
|---|---|---|---|---|
| **Meta, Reels ads (primary)** | 14% (≈269 px at 1920) | 35% (≈672 px) | 6% (≈65 px) | 6% (≈65 px) |
| TikTok, per a German media agency's spec sheet (secondary) | 126 px | 352 px | 60 px | 120 px |
| TikTok, per AdKit, *"scaled from the labelled 720 × 1280 guide"* (secondary) | 240 px | 660 px | 120 px | 120 px, plus the action rail lower down |
| TikTok, per Affroom, *"conservative production baselines"* (secondary) | ~130 px | ~480 px | ~44–60 px | ~140 px |

Sources: [Meta Ads Guide](https://www.facebook.com/business/ads-guide/update/video/instagram-reels); crossvertise PDF (`raw_codes/tt_spec_de.pdf`, [link](https://www-cdn.crossvertise.com/production/docs/default-source/documents-onlinewerbung/spezifikationen-tiktok-ads.pdf)); [AdKit](https://adkit.so/tools/safe-zones/tiktok); [Affroom](https://affroom.com/blog/tiktok-safe-zone/). **The TikTok figures disagree because TikTok's safe zone moves with caption length and add-ons**; the official overlays are downloads inside TikTok Ads Help.

**Studio safe box for 1080×1920 (the strictest of the above, rounded):**
- **Keep everything that matters inside x 120–920 px, y 270–1240 px** (800 × 970 px): Meta's top and bottom, AdKit's left, and a 160 px right margin for TikTok's icon rail.
- **Speech captions:** baseline band **y ≈ 1000–1240**, centred on x ≈ 520 (the box centre, not the frame centre, because the right rail is wider).
- **When the pack occupies the lower half (9–15 s):** move captions to **y ≈ 300–520**.
- **Verify every master against TikTok's downloaded overlay and Meta's Safe Zone guardrail in Ads Manager before delivery.**

### 6b. Caption style

| Parameter | Value | Basis |
|---|---|---|
| Font | **TikTok Sans** 700–800 for speech; brand display face only for 1–3-word punch words | §1b |
| Size | **54–64 px** at 1080 width (studio rule) | Large-text contrast bar applies at ≥18 pt |
| Lines | **max 2**, usually 1 | Netflix PT-BR: *"Maximum two lines… usually… one line"* ([Netflix PT-BR style guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497-Portuguese-Brazil-Timed-Text-Style-Guide)) |
| Line length | **≤30 characters** (Netflix allows 42, but our safe width is 800 px at ~60 px type) | Netflix: *"42 characters per line"* |
| Reading speed | **≤17 characters per second** for speech | Netflix: *"Up to 17 characters per second"* (adults) |
| Text-only kinetic type | **5–10 words per second** at most | TikTok, §4a |
| Case and punctuation | lower-case or sentence case; one terminal mark; the single ellipsis character **…** | Netflix: *"Do not use more than one terminating punctuation mark"*, ellipsis *"U+2026"*; `culture.md` §3 |
| Contrast | white with a 6–8 px dark stroke, or a 70–85% plate; **≥4,5:1** | [WCAG 2.2 SC 1.4.3](https://www.w3.org/TR/WCAG22/#contrast-minimum) |
| Sync | word-level highlight in a brand colour (C: hot pink #FF6FAE with #141414 text, 7,14:1) | Studio rule; burned in, so no platform auto-caption is needed |

### 6c. The disclosure line

- **Text:** *"imagem ilustrativa criada com IA · publicidade"* (the studio's mandated wording plus CONAR's identification).
- **Position:** fixed for the whole video, inside the safe box, top-left (y ≈ 280–330), on a plate.
- **Size:** ≥34 px (studio rule).
- **Contrast:** ≥4,5:1.
- **Why it is designed, not hidden:** CONAR asks for *"de forma imediata e visível, preferivelmente na primeira tela"*, and in short videos *"fixa e legível… sem interferência de outros elementos em sobreposição"*. TikTok accepts *"a clear disclaimer, caption, watermark, or sticker of your own"* and also applies its own AIGC label.
- **Studio rule:** design it as a small branded tag (the sticker shape) so it reads as part of the system rather than a legal patch.

---

## 7. Ten reference campaigns that nailed Gen Z humour on a heritage occasion

| # | Campaign | Occasion | What it did | What we take | Link |
|---|---|---|---|---|---|
| 1 | **Liquid Death × Martha Stewart, "Dismembered Moments Luxury Candle"** | Halloween 2022 | A life-size black candle of a severed hand holding a can; US$58; launch film of Martha with a cleaver | **A candle can be the joke you actually buy.** Deadpan luxury-catalogue voice over an absurd object; heritage figure plus irreverent brand | [Apartment Therapy](https://www.apartmenttherapy.com/martha-stewart-liquid-death-candle-37142573) |
| 2 | **Duolingo, "Buttception"** | Super Bowl LVIII, Feb 2024 | A 5-second regional spot built on the community's own meme, synced with a push notification; 30M+ views | **Brevity and a community-born joke.** Five seconds is enough if the joke is already known | [Campaign](https://campaignlive.com/article/everything-know-duolingos-five-second-super-bowl-ad/1861011) |
| 3 | **Pop-Tarts Bowl, edible mascot** | College bowl season, 28 Dec 2023 | A giant smiling Pop-Tart, holding *"Dreams really do come true"*, lowered into a toaster and eaten | **Commit to the ritual parody; let a sincere sign sit over an absurd act** | [WUFT/NPR](https://www.wuft.org/2023-12-29/first-edible-mascot-in-sports-history-stars-in-the-pop-tarts-bowl) |
| 4 | **Spotify, "Thanks 2016, It's Been Weird"** | Year end, Nov 2016, 14 markets **incl. Brazil** | Billboards addressing users through their own data (*"Dear 3,749 people who streamed…"*) | **The affectionate roast in data form**; the ancestor of Wrapped and of every receipt meme | [The Drum](https://www.thedrum.com/news/spotify-celebrates-weird-2016-largest-ever-campaign-push); Brazil in the market list per [B&T](https://www.bandt.com.au/spotify-says-thanks-2016-weird-witty-home-ad-campaign/) |
| 5 | **Samsung, #MakeMomEpic** | Mother's Day, TikTok, markets **incl. Brazil** | Gen Z showed *"an everyday side of your mother"* to Missy Elliott's "Mommy"; 4,7M videos, 12,4B views | **Mum as "far from basic", shown by the child**; a branded sound is the format | [TikTok case study](https://ads.tiktok.com/business/ar/inspiration/samsung-galaxy-356) |
| 6 | **Tang × DAVID São Paulo** | Dia das Mães, Apr 2021 | Six 15 s films: *"Mães não vieram prontas para o TikTok. Mas será que o TikTok estava pronto para as mães?"* | **The exact 15 s Brazilian format; the twist makes the joke land on the platform, not on mum** | [Marcas pelo Mundo](https://marcaspelomundo.com.br/destaques/tang-faz-homenagem-ao-dia-das-maes-da-geracao-z/) |
| 7 | **Natura × NOS** | Dia das Mães, Apr 2025 | *"A maternidade é uma caixinha de surpresas. E se uma delas for um presente Natura?"* | **Recognisable everyday situations; humour backed by engagement data** | [Propmark](https://propmark.com.br/anunciantes/natura-lanca-campanha-de-dia-das-maes-e-celebra-a-maternidade/) |
| 8 | **DoorDash, "The Real Moms of the Group Chat" + "Memes"** | Mother's Day, May 2026 | Reality-TV parody of the mum group chat; a spot animating "This Is Fine" and Confused Math Lady | **The group chat is mum's stage.** We cannot license real memes, so we build our own chat | [Marketing Dive](https://www.marketingdive.com/news/doordash-delivers-memes-reality-tv-moms-for-mothers-day-campaign/819175/) |
| 9 | **Cadbury 5 Star × Ogilvy India, "uncles"** | Valentine's Day, Feb 2025 | Spent the week's budget paying older couples to take over the day, so youth would lose interest | **Generational inversion**: trends die when parents adopt them. The joke targets the occasion, not a person | [Campaign Brief Asia](https://campaignbriefasia.com/2025/02/04/cadbury-5star-and-ogilvy-india-team-up-with-uncles-to-end-valentines-day/) |
| 10 | **KFC × Enviro-Log, "11 Herbs & Spices Firelog"** | Christmas 2018 | A fried-chicken-scented fire log at Walmart; sold out within hours | **A scent can be a punchline and a sell-out limited drop** | [Newshub](https://www.newshub.co.nz/home/lifestyle/2018/12/kfc-sells-out-of-giant-firelog-that-smells-like-fried-chicken.html) |

**Two cautionary cases (what not to do):**
- **Coca-Cola, AI "Holidays Are Coming" (Nov 2024):** an AI remake of a 1995 classic. It first tested well, then was called *"creepy"*, *"ugly"* and soulless online ([Adweek](https://www.adweek.com/creativity/how-coca-colas-ai-holiday-ad-went-from-praise-to-rage/)). **AI made it look cheap on the one date where warmth is the product.**
- **Bumble, celibacy billboards (May 2024):** *"You know full well a vow of celibacy is not the answer"*. Pulled with an apology for mocking a choice its audience valued ([Fortune](https://fortune.com/2024/05/14/bumble-apologizes-celibacy-ad-women-angry-dating-apps)). **Punch at the occasion or at yourself, never at a choice the audience holds.**

---

## 8. The AI-slop tells to design out (studio rules)

These are craft rules, not measured findings. They extend the exclusions already used in the earlier kits (`ref/AVELUNE_packet.md` §4: *"fumaça, partículas ou reflexos que dupliquem o pote"*).

1. **No waxy over-smooth skin; no impossible hands; no glow halo** around the presenter.
2. **No floating particles, bokeh orbs, smoke wisps or lens flares** "for magic".
3. **No teal-and-orange "cinematic" grade.** One designed palette (§2), held across every asset.
4. **No perfect symmetry, perfect wick or perfect wax surface.** Real candles have a slight dome, a sink ring, a soot freckle on the second burn.
5. **No generic copy** (*"ilumine momentos especiais"*). Every line must sound like a person said it at a kitchen table.
6. **No text drawn by a generator, anywhere.** Rule 1 again: every letter is set by code.

---

## 9. Data notes and discrepancies

- **Natura "caixinha de surpresas" is dated 25 Apr 2025 by Propmark.** `culture.md` §2 lists it among 2026 campaigns; the brand may have run the line again in 2026. **Check before quoting a year.**
- **TikTok Sans** shows `dateAdded 2025-04-28` in Google's metadata API but `date_added 2025-07-09` in its `METADATA.pb`. Immaterial; "2025" is safe.
- **Pinterest Predicts 2026** figures come through ppc.land, YPulse and Axios (Axios returned 403); Pinterest's own page did not load. **Secondary.**
- **The TikTok safe-zone pixel values are all secondary** and disagree (§6a). The studio box uses the strictest value in each direction.
- **Meta's *"captions increased watch time by 25%"*** appears in some summaries and was **not** found on a Meta page; only the 12% figure is cited here.

---

## Sources fetched or read

**Platforms and standards (primary):**
- TikTok Ads Help, [creative best practices](https://ads.tiktok.com/help/article/creative-best-practices) · [in-feed ad specs](https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads) · [misleading and false content / AIGC](https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content) · [Evolution of Sound](https://ads.tiktok.com/business/en-US/blog/evolution-of-sound-volume-1) · [What's Next 2025 PT-BR](https://ads.tiktok.com/business/library/Whats_Next_Report_Tendencias_pt_BR.pdf) · [Samsung #MakeMomEpic case](https://ads.tiktok.com/business/ar/inspiration/samsung-galaxy-356)
- Meta: [Reels video ad guide](https://www.facebook.com/business/ads-guide/update/video/instagram-reels) · [video ad features](https://www.facebook.com/business/news/updated-features-for-video-ads) · [Reels ads blog](https://developers.facebook.com/blog/post/2024/11/07/unlock-the-power-of-reel-ads/) · [WhatsApp brand resources](https://www.meta.com/brand/resources/whatsapp/whatsapp-brand/)
- [Netflix PT-BR timed text style guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497-Portuguese-Brazil-Timed-Text-Style-Guide) · [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/#contrast-minimum) · [Blender 4.2 Cycles release notes](https://developer.blender.org/docs/release_notes/4.2/cycles/)
- Google Fonts [metadata](https://fonts.google.com/metadata/fonts) and [google/fonts repository](https://github.com/google/fonts) (licences, descriptions, font files)
- [CONAR Guia de Influenciadores 2026](https://conar.wpenginepowered.com/wp-content/uploads/2026/05/260525_GUIA_INFLUENCIADORES_CONAR_v6.pdf) (local copy `research/src/conar_guia2026.txt`)
- [WGSN × Coloro COTY 2027](https://www.wgsn.com/en/wgsn/press/press-releases/wgsn-and-coloro-reveal-colour-year-2027-luminous-blue-and-s-s-27-key) · [Adobe Express 2026 trends](https://www.adobe.com/express/learn/blog/graphic-design-trends-2026)

**Trade press and secondary:**
- Campaign Brief (Canva 2026); Creative Bloq (Canva Notes App Chic); ppc.land and YPulse (Pinterest Predicts 2026); NBC News (Pantone 2026); hextoral (Cloud Dancer hex)
- Marketing Dive (DoorDash 2026, Brisk 2024); Propmark (Natura 2025); Marcas pelo Mundo (Tang 2021, Usaflex 2026); Campaign (Duolingo 2024); The Drum (Spotify 2016); WUFT (Pop-Tarts 2023); Apartment Therapy (Liquid Death × Martha Stewart 2022); Campaign Brief Asia (Cadbury 5 Star 2025); Newshub (KFC firelog 2018); Adweek (Coca-Cola AI 2024); Fortune (Bumble 2024)
- Poder360 and Finsiders (Pix); Mobile Time (stickers); Canaltech (Flork); Yorkshire Post (Receiptify); The Nightly (brat green); Rico Lins and ESPM (lambe-lambe, Gráfica Fidalga); AdKit, Affroom and crossvertise (TikTok safe zones); B&T (Spotify markets); Soundstripe (TikTok Commercial Music Library); Made Good Designs (type trends)
