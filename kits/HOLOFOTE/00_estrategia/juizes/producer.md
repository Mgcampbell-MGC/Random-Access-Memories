# Verdict: Head of Production + Compliance

**Brief judged:** can each concept be built under the studio's rules, will it look premium made with local
Blender renders and code-set type, and what are its brand-safety and legal risks?

**Studio rules checked:**
- the label is never generated;
- a chroma-blue stand-in in every generated scene, and no other blue in that frame;
- a photoreal Blender pack;
- code-set type, beside the pack and never on it;
- the presenter timing (0–6 s talk, 6–9 s gesture, 9–15 s key visual), and she never holds the pack;
- no testimonial lines;
- AI disclosure;
- the label's legal copy.

**What I read:**
- all five concept files in full;
- `research/label_rules.md` §0–§12;
- AVELUNE §12–13, for the compositing and checking method.

**Fonts measured myself** with fontTools on the files in `research/raw_*/fonts/` (scripts in
`judges/prodtools/`).

## Scores

| | Concept | Score | Single best thing | Single worst thing |
|---|---|---|---|---|
| **A** | **MÃENÊS** | **8** | **The label is the campaign, and the film can be checked today.** Every headline is pack copy set by code. The film keeps the pack still in each shot: only a global 2D move and a separately rendered flame pass. So every frame can be checked against its own same-angle master render with the existing checker, with no new tooling. It is the lowest-risk route to a finished, verified launch. | **Its premium level rests on type alone.** Fraunces plus candy glass on a paper cove can read as 2024 direct-to-consumer branding. And the presenter's "code writes on a blank whiteboard" gag assumes a generator will hold a locked camera, which they don't. |
| **B** | **pode.** | **4,5** | **The object is beautiful on its own.** Glossy porcelain, a gold rim line and a ribbed glass dome. In the film only the dome moves, and it carries no label. | **It names candles after other products** (*sabonete*, *perfume*, *bolo*), sets *vela aromática* at 2,4 mm under a 6 mm *sabonete*, and adds a sweet-dish dome in candy colours. That stacks a misleading-nature risk (RDC 907 art. 12 I) on a food-look risk (CDC arts. 8–10). |
| **C** | **cheguei** | **6,5** | **The most premium image per render hour.** One dark gloss glass, one flame, and the *fresta* glowing through subsurface wax. It also has the most careful label typography: it caught that Young Serif's default figures are oldstyle, and I confirmed the `lnum` lining figures at 750–762 units and the x-height ratio of 0,667, so its 110% "g" is right. | **It reads as a memorial by structure:** dark glass, a single flame, *mãe* and *"casa apagada"*. And it breaks its own label. L03 shows the lit 01:17 candle beside a paper electricity bill, while the pack says *"Acenda longe de… papéis"* (CONAR art. 33). |
| **D** | **sinal** | **4** | **The only label that can be checked in motion today.** The pot's front is flat, so the existing plane-fit checker verifies it in every frame, even under camera moves. | **The pack itself imitates WhatsApp's voice-note interface:** ▶, waveform, duration, a **1x** speed pill, and ✓✓ that change colour when "read". A real client's lawyer deletes that on day one. On top of it: a scam-themed ad spoken by an AI presenter, and a burn time made into the product name with a real-time countdown on an untested single-wick rectangular pool. |
| **E** | **HOLOFOTE** | **7,5** | **The most reliably premium key visual we can make locally:** one hard spot, a black lacquer floor, one object on a gaffer-tape X. It also has the tournament's best fire-safety discipline: the pack moves only while unlit, clearances are stated, and confetti is banned near a flame. | **Three production holes.** It puts a woven textile wristband on the candle body, a fire hazard by design. The P01 prompt dresses the mother in **"everyday blue jeans" in the same frame as the chroma-blue stand-in**. And the film depends on a real filmed match insert and an unbuilt label check, the two things this pipeline cannot deliver today. |

**Winner: A, MÃENÊS.** E is a close second if the creative judges need more spectacle; its three holes are fixable,
but each one costs time A doesn't need.

---

## Why A wins on this lens

1. **It can be built today, in full, by this pipeline.**
   - Opaque gloss glass is one cylinder with satin screen-print ink and a 0,05 mm decal shell.
   - The lid is a flat ceramic disc and the set is a paper cove under hard flash.
   - The film is kinetic type plus still packshots. The match strike is **sound only**, so no CG match has to look
     real. (C's match floats into frame with no hand, which is uncanny; E's needs real footage.)
   - No set piece risks the "CG interior" look: no cabinet (B), auditorium (E), inflatables (D) or hallway (C).
2. **Verification needs no new method.**
   - The CLAUDE.md rule says curved labels must be proven before they are sold, and four of the five concepts are
     cylinder wraps.
   - A's own design solves this. It renders **one master per camera view** and keeps the pack still within each
     shot, so each frame is compared like for like with a still render from the same angle.
   - Only **one** extra check is needed: each master view is unwrapped and compared with the flat artwork once,
     with a planted error.
   - E's turning, rising pack needs a per-frame check that has not been built yet.
3. **It is the cleanest on testimonials.**
   - The presenter *"never says 'eu' or 'minha mãe'"*, so a testimonial cannot happen.
   - C and E give the AI presenter a first-person life (*"Paguei minha primeira conta de luz"*, *"Eu mando
     'cheguei'"*). That is lawful as *licença publicitária*, but it sits closer to Anexo Q 3(b): a model must not
     pass as an ordinary consumer.
4. **It is the only concept that names its chroma conflict and fixes it.**
   - The brand ink is blue. A's rule: Caneta blue appears only in code-set type and rendered packs, the presenter
     wears pink, and the walls are cream.
   - B's world is cobalt and never addresses this. E dresses the mother in jeans next to the stand-in.
5. **It has the least legal exposure.**
   - **Name:** *Mãenês* is a coined word, the strongest kind of mark in the tournament (still unverified at INPI).
   - **Claims:** none.
   - **Trade dress:** no third-party look is borrowed. The messenger, the ballpoint pen and the competitor shelf are
     all generic by rule.
   - **Grief:** an opt-out is designed in, plus a quiet unadvertised *Beijos, mãe.* edition for people remembering a
     mother.
6. **It shows what the studio sells.**
   - The product is a label proven against the brand's own file. In A the label *is* the headline, the lid is the
     punchline and the base is the button.
   - So every frame of the sample advertises the studio's guarantee.

## Fixes A needs before anything is rendered (not optional)

1. **The whiteboard.** Don't rely on the generator holding a locked camera.
   - Either planar-track the board in the generated take,
   - or move the "lesson" to a code-set panel beside her, which needs no tracking.
   - Reject any take whose board drifts more than 2 px between frames.
2. **P01 contradicts itself.** The shot says Z01 *"sets the closed livro-caixa on a kitchen table"*, while the rule
   says *"stand-in on the table, not in hands"*.
   - The book box carries text, so it is a product. It must be a stand-in, already resting on the table, with no
     hand on it.
3. **The base.** The embossed ring *SABIA QUE VOCÊ IA VIRAR* and the required LOTE/FAB/VAL sticker both live on the
   base.
   - Specify the sticker at ≤Ø 36 mm, inside the 52 mm ring, over the monogram, so the joke stays readable.
   - Render the base macro both with and without the sticker.
4. **Net weight in Fraunces** (my measurement).
   - The default figures are lining (cap 1.400 units, 1.440 with overshoot). Good.
   - But x-height ÷ figure height is **0,675 at opsz 9, 0,682 at opsz 14, and 0,627 at opsz 144**.
   - **So set PESO LÍQUIDO only at opsz 9–14, and set the "g" at 105–110%.** At 4,0 mm figures, an unscaled "g" is
     2,70 mm, exactly on Inmetro's ⅔ line.
   - B's claimed 2,8 mm "g" is in fact 2,70 mm.
5. **Flame-lit shots.** In the "Luz acesa" shots (I-02 and Ad 2's end card) the flame is the key light. The beauty
   pass will legitimately shift the label's hue and fail the studio's ≤2,0 colour bar.
   - Verify letters and geometry on the Cycles *Diffuse Color* (albedo) pass, with a planted-error control.
   - Measure colour on a neutral-light render of the same view.
   - Never relax the bar.
6. **The *Já comeu?* glass is yellow and its scent is gourmand.**
   - No plates, cake, cutlery or crumbs in any frame.
   - Never render the wax in a colour that reads as *doce* or custard.
7. **Personalisation.**
   - Allow nicknames and first names; block the names of public figures, trademarks and profanity.
   - Use a fit ladder for a 28-character headword on the 77,5 mm panel. Two lines at most, then step the type size
     down. Above that, reject the order; never squeeze the text.
8. **Copy review, not production:** the lid *"nem você."* can read as back-talk to mum. The CCO should sign it off
   against the *zoeira com respeito* rule.

## Grafts onto A from the other concepts

1. **D → the warning written in mum's voice, then the formal block.**
   - Back panel, as a verbete: *"acendeu? fica de olho. longe da cortina. apaga antes de sair. — Tradução: nunca
     deixe a vela acesa sem supervisão."*
   - Then the full ATENÇÃO block from `label_rules.md` §11.2 exactly.
   - Compliance becomes copy in the brand's own language.
2. **B and D → put movement only on flat, text-bearing parts.**
   - Let the ceramic *tampa-bilhete* lift off and land in the film. That is B's *tlin*, as a ceramic *toc*.
   - The curved glass stays still.
   - A flat disc is verified by a plane fit (D's logic), so the lid's reply (*levei.*) can move with no new checker.
3. **C → verify on the albedo pass with a planted error**, for every frame where the flame is the key light (fix 5).
4. **C → C's figure check as standing rule.**
   - Measure figures and x-height on the actual font file before any legal line is set (fix 4).
   - C caught Young Serif's oldstyle default. The same check gives Fraunces's 0,627 at display sizes.
5. **C → treat *A FRASE DELA* the way C treats *A PRIMEIRA VEZ*.**
   - The variable fields are strings in `label_copy.json`.
   - Every personalised master goes through the fidelity tool with a planted error before printing.
   - That is the sample's best proof that the studio's label pipeline works.
6. **E → fire safety in every frame, written as rules.**
   - The pack moves only while unlit.
   - Each shot states its clearance: 30 cm from paper, fabric or a person.
   - A per-frame checklist runs before delivery.
   - The leaflet becomes a dictionary page in the brand's form: *"modo de uso (loc. mãenês)"*. That is E's
     setlist-as-instructions idea, in A's voice.
7. **E → claim discipline.**
   - Until each master view has passed its one-time unwrap check, the packet says only *"render 3D, textura do
     arquivo-mestre"*, never "verificado".
   - Keep E's split disclosure: *"render 3D ilustrativo"* on renders, *"imagem ilustrativa criada com IA"* on
     presenter frames.
8. **D → make the tilde voice-note waveform data, not decoration.**
   - Compute the bar heights of *A NOTA DE VOZ DE TILS* (7:12) from a real recording: the match-strike sonic logo.
9. **E → reset type for each format, never crop or scale it.** A already states this for the key visual; extend it
   to every carousel and story template.

## Other concepts: production and compliance notes

**B · pode.** Do not proceed as written.
- **Hardest key visual in the tournament.** The cabinet has a mirrored back, glass shelves, cut-glass props and a
  tinted ribbed dome. In Cycles that means caustics, fireflies and long noisy renders, and it is the scene most
  likely to look CG.
- **The tearing paper band** in Corte A needs a cloth or paper simulation we have not built.
- **The dome cannot be composited over a chroma stand-in.** The dome is transparent, so whatever sits behind it was
  hidden by the opaque blue stand-in, and that needs a clean background plate.
- **PL1 contradicts itself.** The stand-in includes the dome, but the composited pack is lit, and the candle may
  only be lit with the dome off.
- **The palette conflicts with the chroma stand-in.** The cobalt cabinet and the Lápis world are never reconciled
  with the "no other blue" rule.
- **The insight is unsourced** (B says so itself).

**C · cheguei**
- **Fix L03.** Show the candle unlit, or move the bill at least 30 cm away and out of the frame's reading of
  "beside".
- **The film's 3D match** strikes with no hand and floats into frame, which reads as uncanny. Use sound only (as in
  A) or a real insert.
- **Two features are presented as safety features but are untested:**
  - *"Tampa quando for dormir"*: snuffing with the lid, where the flame rises above the rim;
  - the *fresta* stop line.

  Neither may be stated as a safety function until a candle maker has tested it.
- **The light under the door in Ad 1** is drawn by code onto a generated plate, which needs tracking if the
  generated camera drifts.
- **Memorial test.** The concept commits to a bar of 0/10 on its memorial test. Run it before it is shown to anyone.

**D · sinal**
- **The key visual hangs a vinyl inflatable over an open flame.**
  - The bubble spans y 22–38% of the frame.
  - The flame tip sits at about y 34–36%: the pot's centre is at 52%, its height is 26% of the frame, the wax is
    15 mm below the rim, and the flame is about 22 mm tall.
  - So the flammable prop overlaps the flame in the picture. That is CONAR art. 33 at the level of the image, and a
    collision in the composition.
- **The inflatable UI props** are the look most likely to read as stock 3D illustration rather than craft.
- **The single cotton wick** in an 80 × 58 mm rectangular pool will probably tunnel at the corners, so *"áudio de 40
  horas"* is an untested performance claim built into the product name (CDC art. 37).
- **Ad 3 (the *"oi, mãe"* scam):** an AI presenter talking about a fraud that itself uses AI voices is a brand-safety
  risk I would not ship in a sample.
- **The flame mascot with eyes** reads as a children's motif. Route B forbids it outright (RDC 989 art. 29).

**E · HOLOFOTE**
- **Remove the jeans from P01.**
- **Move the wristband off the glass and into the box** (around the fan-club card).
- **The film's match:** either Sol films the insert, or it becomes sound only.
- **Build and prove the label-AOV check before the film's turn and rise are called verified.** E flags this
  honestly itself.
- **Two smaller problems:**
  - the warnings are set at 1,8 mm condensed caps on day-glo, curved glass, which may not meet the CDC's
    *"ostensiva"* test;
  - fluorescent coatings near heat need a fade test.
- **The ACÚSTICO blue glass is acceptable** only because every image of it is a render. **Never put the range into a
  generated scene.**
- **IP hygiene is good:**
  - no real artist or festival;
  - no *"mãe"* used as diva slang;
  - *Acústico MTV* styling avoided;
  - Lei Cidade Limpa respected.

## The rule that applies to every route

A rendered pack is "exact by construction" only for the file it was built from. The studio's guarantee covers that
file, not the render.

- **The one live risk is a wrong or outdated master file.** It is closed by process: the label comes only from the
  file named in the signed Ficha.
- **One extra check for cylinder wraps:**
  - each master view is unwrapped and compared with the flat artwork once, with a planted error;
  - every shot is then checked against its master view.
- No route claims "verified" before both checks have passed.
