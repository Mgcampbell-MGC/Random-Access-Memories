# Manus prompt: the O LANÇAMENTO website and portfolio

## Before you paste it

1. **Set up Sol's kit first** (`SETUP.md`): the `o-lancamento` Skill installed and Test 1 at 9/9.
2. **Create a SEPARATE Manus project** called **SITE O LANÇAMENTO**.
   - Don't use the production project. Its instruction says *"one step at a time, wait for Sol"*, which would stall
     the build.
   - Add the **o-lancamento** Skill to this project (Project → Skills → + Add).
3. **Attach these files to the first message:**
   - `oferta-o-lancamento.pdf`: the offer.
   - `CLIMATE-Rescue-O-Lancamento-Case-Study.pdf`: **art direction only**.
     - Its stills were never machine-checked, and two film frames smear the label.
     - If you still have the original Climate image and video files in your Manus account, attach them too.
   - `EMBALAGEM_climate.png`: the Climate packshot. Use the one the case study was made from if you have it.
   - **Do NOT attach the business-plan text.** It holds the prospect list with names, emails and phones. The website
     doesn't need it, and the prompt below carries everything it does need.
4. Paste everything between the two lines below.

---

You are the art director, producer, designer, copywriter and web developer for **O LANÇAMENTO**: a one-person studio
that makes launch campaigns for small Brazilian beauty brands. Build a **working website preview** and a
**three-case portfolio made with the studio's real production method**. Don't stop at a plan. Don't buy credits,
tools or a domain, and don't publish publicly without my written approval.

## The business, in one paragraph

A brand sends its product and label files. The studio delivers a complete launch campaign in one visual world:
- 1 key visual;
- 6 campaign images;
- 3 store images (white background, in use, routine);
- a 15 s vertical film;
- two 6 s cuts;
- a fidelity report.

**The difference is the label.** AI makes the scene, the hands, the light and the people, but never the label. Every
scene is generated with a flat chroma-blue stand-in where the product goes. The brand's real packshot is then
composited over the stand-in by code. Every image and every film frame is then machine-checked against the brand's
file. AI tools misspell labels when they draw them; this method never lets them draw one.

The `o-lancamento` Skill in this project does that work:
- `recortar.py`: exact sizes;
- `compor.py`: composite;
- `texto.py`: approved phrases beside the pack, never over it;
- `relatorio_fidelidade.py`: the check;
- `filme.py`: a simple film.

## The production rules (they apply to every portfolio piece)

1. **Generate every scene with the stand-in.** Put this in every prompt: *"the whole [bottle/tube/jar] including the
   cap in flat matte chroma blue, no text, no logo, no glare"*.
2. **Never give the packshot or the label art to an image or video model as a reference.**
3. **Apply the pack with `/o-lancamento`.** Before composing, bring each scene to its delivery size:
   - key visual 9:16 1080×1920, with the pack centred at 45–50% of the frame height (the 4:5 and 1:1 versions are crops
     of it);
   - campaign images 4:5 1080×1350;
   - store images 1:1 1200×1200.
4. **After the pack is in, no AI editing of the piece.** No Design View, edit-image, AI upscale or object removal:
   they redraw the whole picture, label included. Add text with `texto.py` or code. To change a finished piece,
   change the scene and composite again.
5. **Film.** Put the approved 9:16 key visual into the Video Editor as one image layer, with camera moves only. Add
   generated shots only where no label is visible. Then check every frame.
   - If the editor's export fails the check, make the film with `filme.py` instead.
   - 6 s cuts use half the camera move: `--zoom 0.04 --pan 0.02`.
6. **Only APROVADA pieces go on the site.** A piece that fails is regenerated, or left out and listed as missing.

## The three cases

Every case page says **"Caso demonstrativo · marca fictícia"**. No invented clients, testimonials, results or
approvals.

**How to make a fictional brand's packshot** (it becomes that case's "brand file", `EMBALAGEM.png`):
1. Generate a photoreal, front-facing, BLANK pack (no text, no logo) on a plain background.
2. Cut it out, removing the background only.
3. Design the label artwork **in code** (HTML/SVG or Pillow), with fonts that allow commercial use (Google Fonts, OFL).
4. Apply the label onto the pack's label area by code. A gentle cylindrical warp is fine.
5. Export a PNG with a transparent background, at least 1.000 px tall.

The label's text exists only as code, so it is exact by construction. Keep claims cosmetic and modest: no treatment,
cure, percentage, "clinically proven" or ingredient you didn't print on the label.

**Case 1: CLIMATE Rescue, "Depois da Chuva".** A hair-finishing stick in a Brazilian city after rain: wet stone,
mineral green, warm light.
- **Remake** the case with the method, using the attached case study as the art reference and `EMBALAGEM_climate.png`
  as the brand file.
- Say on the page that this is a new production of an earlier concept.
- Don't present the PDF's pieces as checked work.

**Case 2: premium facial skincare, your own fictional brand.** For example a facial oil or serum in glass with a
dropper or pump.
- Sculptural studio light, tactile glass and stone, a muted rose or warm monochrome palette, quiet premium type.
- It must look nothing like Case 1.

**Case 3: a different use, your own fictional brand.** For example a lip or body product.
- Graphic urban daylight or bold chromatic retail.
- Show it in hand in real life.
- Add one extra image extending the world to a second SKU (*EXTENSÃO*).

**Each case contains:**
- the concept (3–4 lines);
- the key visual;
- the 6 campaign images, at least 2 of them in hand or in use;
- the 15 s film and two 6 s cuts, playable;
- the 3 store images;
- **the real fidelity report**, rendered from `relatorio.json` as a readable table: piece · result · worst tile ·
  planted error caught · colour.

**Before composing the hands:** a hand may cover part of the pack, but never the main words.
- For hand shots, keep the fingers below the middle of the label.
- The check reports what share of the label was covered.

## The website (Brazilian Portuguese, mobile first)

**Pages:**
1. **Início.** Headline *"Você manda o produto. Nós entregamos a campanha."*, then:
   - what arrives, in one line per deliverable;
   - the label promise, in buyer language;
   - the three cases;
   - how it works, in 4 steps;
   - a call to action.
2. **Trabalhos:** the three case pages.
3. **O serviço:** O LANÇAMENTO as the main package, with exactly what's inside.
   - Also mention VITRINE, EXTENSÃO and PRÉVIA in one line each.
   - **Show no prices.** The CTA is *"Peça a proposta"*. Prices go in the proposal; they are still being tested.
   - Mark the price lines as an owner decision in the checklist.
4. **Como funciona:**
   - files and approved phrases;
   - three worlds to choose from;
   - key-visual approval;
   - production;
   - the check;
   - delivery with the report.
   - Also say in plain words what the check does, and what it doesn't: it confirms the label wasn't redrawn,
     distorted or recoloured; it isn't a regulatory opinion; and the brand approves its own claims and the key
     visual in writing.
5. **Sobre:** a solo studio with an exact method. **No founder photo, no personal name, no team.** The studio is the
   brand.
6. **Contato:** WhatsApp and e-mail links marked `[INSERIR]`. No form.

**Copy and legal:**
- Use the label guarantee from the offer PDF, flagged `[REVISÃO DA DONA]`.
- Footer:
  - *"Imagens e filmes criados por computador, com pessoas e cenários de IA; não são fotografias."*
  - On each case: *"Caso demonstrativo · marca fictícia"*.
- Mark images with a synthetic person: *"imagem ilustrativa criada com IA"*.

**Design:**
- An editorial beauty studio, not a SaaS page.
- Warm off-white with deep green or charcoal; expressive serif headings; disciplined grid; generous space.
- Each case can carry its own palette.
- Motion restrained, honouring reduced-motion.
- Real alt text on every image.

**Leave out:**
- "AI" as the headline;
- any fake browser domain;
- the business plan's costs, contacts, scripts or tax notes;
- anything about tools, credits or subscriptions.

## Work in two phases

**Phase 1:** the site plus Cases 1 and 2.
- Then **stop** and send me:
  - the preview link;
  - every piece with its check result;
  - what is finished, what is missing and why;
  - the credits Phase 1 used.
- Wait for my "segue".

**Phase 2:** Case 3, then the final checks:
- every page at 375 px and 1440 px wide;
- links, video playback and reduced motion;
- every image has alt text;
- no failed piece published.

**Hand-off:**
- the preview link;
- the asset folders per case, each with its `relatorio.json`;
- a short edit guide;
- a **pre-publication checklist** for me:
  - studio name and contact;
  - rights to show each case;
  - prices on or off;
  - guarantee wording;
  - turnaround wording;
  - domain;
  - go-live.

If a tool can't do something this prompt needs, say so plainly. Don't substitute something that looks similar and call
it done.
