# OL1: Is the label-exact guarantee actually scarce? (25 Sep 2026)

**Hole:** O LANÇAMENTO's differentiator is "fidelity by construction": the real packshot is composited, so the label is pixel-exact. But many self-serve tools also keep the real product pixels and generate only the background. If they do, the guarantee is table stakes, not a moat.

**Verdict: PARTLY CLOSED.**

- **For stills of a product standing in a generated scene, label-exactness is table stakes and cannot be sold.**
  - At least 9 tools keep the product's own pixels and generate only the background, for free to about US$15 a month.
  - One of them, Google Product Studio, is free and live in Brazil.
- **What remains scarce is narrower:**
  - the real, untouched pack inside a human or in-use scene (hands, skin, water, fingers over the label);
  - the real pack moving inside a campaign world;
  - a whole launch set in one coherent look in 5–7 working days;
  - a written re-do guarantee plus a per-asset report sold to a small brand. Only Photoroom sells a fidelity guarantee, and only to enterprise food and fashion teams.
- **The true incumbent for label-exact motion is 3D CGI.**
  - A Brazilian studio (Criativoo) already sells "CGI + IA" hybrid label-exact visuals to indie cosmetics brands.
  - Pacdora sells self-serve label-exact 3D tube and bottle renders and MP4 videos for US$17–59 a month.

Pages were fetched with curl (browser user agent). Where marked *(reader)*, they came through the r.jina.ai reader because the direct curl was 403 or failed. Raw captures are in `work/ol1/`.

---

## 1. Self-serve tools: does the product keep its own pixels?

### A. Keeps the uploaded product's pixels; generates only the scene (stills)

| Tool | Exact sentence (vendor's own page) | Price (vendor's own page) | Video? | Guarantee / proof? |
|---|---|---|---|---|
| **Photoroom** AI Backgrounds | *"Photoroom needs a source image to use as a starting point. It will remove the background from the source image so that it's ready for a new AI background."* ([help](https://help.photoroom.com/en/articles/6741465-how-to-use-ai-backgrounds)). ⚠ Its AI Relight changes the subject's lighting: *"correct lighting issues… by re-lighting the input image"* ([docs](https://docs.photoroom.com/image-editing-api-plus-plan/ai-relight)). | Pro US$12,99/mo (US$89,99/yr), 1.000 exports, 4.000 AI Background generations. Max US$34,99. Ultra US$99 (JSON-LD on [pricing](https://www.photoroom.com/pricing)). API: *"each API call is priced at $0.10"* ([docs](https://docs.photoroom.com/image-editing-api-plus-plan/pricing)). | Max and Ultra only: *"Up to 50 generations"* / *"Up to 150"* ⇒ ~US$0,66–0,70 per video. The video is generative, see B. | Enterprise only, see §3 |
| **Pebblely** | *"The AI creates backgrounds based on your uploaded images and adds shadows and reflections accordingly."* ([FAQ](https://pebblely.com/faq/)) | Lite US$9 = 30 images (US$0,30 each). Basic US$19 = 200 (US$0,095). Pro US$39 = 500 (US$0,078) ([pricing](https://pebblely.com/pricing/)) | No | *"we are not able to offer refunds"* ([FAQ](https://pebblely.com/faq/)) |
| **Claid.ai** | *"Every texture, label, and fine detail preserved."* ([home](https://claid.ai/)). *"Automatically isolate the product before generation… prepare a clean product cutout."* ([generate-background](https://claid.ai/api-products/generate-background)). ⚠ *"We automatically adjust product quality and light"* | Essentials US$15/mo (US$108/yr). Pro US$49/mo (US$420/yr), from the public plans endpoint the pricing page calls: `api.claid.ai/v1-internal/billing/plans`. AI Photoshoot costs 4 credits: 125 or 500 images a month ⇒ US$0,10–0,12 each ([pricing](https://claid.ai/pricing)) | *"AI Video Max generations (60 credits for 5s)"*: 8 or 33 a month ⇒ ~US$1,48 per 5 s. Generative. | None found |
| **Mokker** | *"Upload a product photo. Mokker will remove the background with AI"* ([home](https://mokker.ai/)). The site also says *"Mokker is joining forces with soona."* | Starter US$13/mo = 500 photos (US$0,026). Team US$29/user, unlimited ([pricing](https://mokker.ai/pricing)) | No (it links to UGC creators) | None found |
| **Pixelcut** Product Studio | *"Product Studio treats your uploaded product as the fixed part of the image, so the shape, label text, and colors stay true to the original."* ([AI product photography](https://www.pixelcut.ai/ai-product-photography)). The same page claims an On Model format. | Pro US$10/mo (US$8 yearly), 600 credits. Business US$30 (US$24), 3.600 credits ([pricing](https://www.pixelcut.ai/pricing)) | AI video generator, generative (*"Nano Banana Pro and Sora 2"*, [home](https://www.pixelcut.ai/)) | None found |
| **Canva** BG Generator | Steps: select photo → BG Generator → Generate. *"Select the Sun icon to choose between additional options such as Balanced relight or Maximum relight."* *"Generated results may sometimes have light direction, color, or style that doesn't match the image."* *"You can generate backgrounds for 200 images every 24 hours."* ([help](https://www.canva.com/help/bg-generator/), reader) | Canva Pro R$34,90/mo (App Store BR, per H6D). Direct canva.com pricing 403: **UNVERIFIED** here | n/a | None found |
| **Adobe Photoshop** Generate Background | *"Select Remove background in the Contextual Task Bar… Select Generate background"*. *"generated content that matches the lighting, shadows, and perspective of the subject"* ([helpx](https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/replace-background-with-generate-background.html), reader). ⚠ Harmonize: *"Your added element will be recreated"* (H6D, [adobe.com](https://www.adobe.com/products/photoshop/harmonize-image-blender.html)). | Photoshop R$65/mo (H6D, adobe.com/br) | Firefly video is generative | IP indemnity only, enterprise, see §3 |
| **Google** Product Studio (Merchant Center) | *"a suite of free, AI-powered tools"*. *"Describe the scene in which you want your product placed in."* *"The services may sometimes provide inaccurate or offensive content"* ([help](https://support.google.com/merchants/answer/13708167?hl=en)). Pixel preservation is implied by the flow, not stated. | **Free.** **Brazil is live:** *"its existing presence in Australia, Austria, Belgium, Brazil…"* ([help](https://support.google.com/merchants/answer/15717899?hl=en)) | *"only available to US merchants"* | None |
| **Amazon Ads** image generator | *"Reference the product as already-present in the product image"* ([guide](https://advertising.amazon.com/library/guides/how-to-use-ai-image-generators), reader). Pixel preservation **UNVERIFIED**. | *"at no additional cost"* ([aboutamazon](https://www.aboutamazon.com/news/innovation-at-amazon/amazon-ads-ai-powered-image-generator)). Brazil availability **UNVERIFIED** | n/a | None |
| **Pacdora** (3D mockup, maps the real artwork) | *"it only takes a few minutes to upload your design… you can download your design as a 4K image or a high-quality MP4 video."* Library counts: *"Cosmetic Bottle 402 · Cosmetic Jar 190 · Cosmetic Tube 185"* ([tube mockups](https://www.pacdora.com/mockups/tube-mockups), reader). *"video exports that showcase your design from every angle"* ([mockups](https://www.pacdora.com/mockups), reader) | Pro US$17/seat/mo (*"Billed $199 annually"*, *"For personal use only"*). Business US$59/seat/mo (*"Billed $708 annually"*, *"Commercial use and resale license"*, *"Maximum export of 2K rendered videos"*) ([pricing](https://www.pacdora.com/pricing), reader) | **Yes: label-exact 3D rotation**, template shapes only | Refund only if exported fewer than 3 times |

### B. Regenerates the product (the label is redrawn by a model)

- **Photoroom Product Staging:** *"combines OpenAI's GPT-Image-1 model"* ([page](https://www.photoroom.com/tools/product-staging)).
  - Photoroom's video generator promises only *"designed to help keep the original product recognisable"* ([page](https://www.photoroom.com/tools/video-generator)). Recognisable is not exact.
  - Photoroom's own benchmark: best base model **29,0%** full-fidelity pass. *"Logo and text distortion… affecting 20.1% of all base-model generations"* ([blog](https://www.photoroom.com/blog/top-editing-image-models-maintain-product-details-only-28-of-the-time)).
- **Flair.ai:** custom models trained on the product, plus repair tools.
  - *"Can I fix product distortion or proportion issues? Yes. Use the "Regenerate Product" option"*; *"The Fix Logo & Text option is now available again"* ([FAQ](https://flair.ai/resources/faq)).
  - Pro+ US$26/mo = 80 images, 3 videos. Scale US$38 = 150 images, 5 videos ([pricing](https://flair.ai/pricing)) ⇒ US$0,25–0,33 per image.
- **Higgsfield** Marketing Studio and the product-photoshoot recipe: they regenerate the product with Nano Banana Pro.
  - The vendor's own recipe says *"Do not claim tiny text… is verified"* (HIGGSFIELD_FACTS).
  - ⚠ But its brand-asset recipe says *"Never redraw an uploaded logo when it can be placed or composited exactly"* (H6D). The vendor already teaches compositing.
- **Orne:** feature bullet *"Fidelidade total ao produto"*.
  - Its cosmetics preset is a prompt to the generator: *"The EXACT cosmetic from the reference image — 100% identical"*.
  - *"Iterações incluídas: 2"* (VER1, `studio.orne.ai/assets/Dx6k-TZz.js`).
  - Prices R$5,50–6,90 per image; videos R$29,90–89.
- **Villo** terms: *"pequenas variações visuais, textuais ou compositivas podem ocorrer entre versões"*; *"obrigação de meio"* ([terms](https://www.villo.ia.br/termos-condicoes)). R$19,90 = 3 images; R$50 per video ≤10 s (VER1).
- **PhotoGen** (BR): *"Nosso pipeline proprietário baseado em Flux"*. R$25 / R$37/mo / R$87/mo ([home](https://photogen.com.br/)).
- **Milano AI** (BR, fashion): photo-to-campaign plus avatars ([home](https://www.milano-ai.com/pt-BR)).
- **Estúdio Fábrica:** *"Geração de Lookbook com IA: R$ 35,00 por até 3 imagens"* ([page](https://www.estudiofabrica.com.br/servicos-e-precos/)).
- **Make Move:** *"Total de fotos 65 · Valor total R$ 3.000"* ([page](https://make-move-studio-fotos-ia-para-marcas.netlify.app/)).
- **Booth.ai:** `booth.ai` redirects to `atom.com/name/Booth.ai`, a domain-sale page. Treated as defunct (an inference).

### Count

- **Stills, main scene mode.** Of 12 label-exact routes found, 10 are self-serve tools (Photoroom, Pebblely, Claid, Mokker, Pixelcut, Canva, Adobe, Google, Amazon, Pacdora). The other 2 are CGI services (Criativoo, WekArts). **10 products regenerate** (Photoroom Staging, Flair, Higgsfield, Orne, Villo, PhotoGen, Milano, Fábrica AI, Make Move, Adobe Harmonize).
  - Of the 10 preserving self-serve tools, **2 say it in words** (Pixelcut, Claid).
  - **6 show it by their architecture:** cut out the product, then generate the background (Photoroom, Pebblely, Mokker, Canva, Adobe, Pacdora).
  - **2 only imply it** (Google, Amazon).
- **Motion.** Every AI image-to-video tool regenerates frames (Photoroom, Claid, Pixelcut, Flair, Higgsfield, Orne, Villo, Milano). Label-exact motion exists only in 3D: Pacdora self-serve, plus CGI studios.
- **Relight caveat.** Photoroom Relight, Canva Balanced/Maximum relight and Claid's auto light all alter the product's tone, but not its letters.

## 2. Brazilian CGI / 3D packshot studios: the true incumbent for label-exact premium and rotating films

- **Criativoo** ([home](https://www.criativoo.com.br/)) is the closest analogue to O LANÇAMENTO's method, already on the market.
  - *"ambientação híbrida de produto (CGI + IA)"*.
  - *"O rótulo técnico permanece 100% nítido e protegido contra qualquer distorção visual."*
  - *"Produzimos comerciais em vídeo de 15 a 60 segundos utilizando as embalagens modeladas em 3D"*.
  - It builds the model *"a partir do PDF técnico ou de 3 fotos simples de celular"* ([We Sis](https://www.criativoo.com.br/portfolio/mockup-digital-3d-cosmeticos-we-sis/)).
  - Its clients include the indie cosmetics brands Nanda Cosméticos, We Sis and Biosante.
  - **It works before the physical product exists.**
  - **No published price.**
- **WekArts** ([product page](https://wekarts.com.br/product/embalagem-3d-para-produtos/)) is the only published CGI price found.
  - *"Pacote Essencial… 2590 · Embalagem 3D · Rotulo Pronto para Impressão · 2 Renders"*.
  - *"Pacote Corporativo 3990 · 4 Renders · Vídeo Motion de 20 Segundos"*.
  - *"As prévias estarão disponíveis de 20 a 40 dias úteis"*.
- **Lou Studios** published a market estimate (its own blog, 16 Jul 2026, so SECONDARY) ([post](https://www.loustudios.com.br/post/quanto-custa-produzir-um-v%C3%ADdeo-de-anima%C3%A7%C3%A3o-3d-para-produtos)):
  - *"Animação 3D Básica R$ 3.000 a R$ 12.000"*;
  - *"Intermediária R$ 15.000 a R$ 45.000"*;
  - *"Premium R$ 50.000 a R$ 150.000+"*.
- **Sidney Marcelo Studio 3D** (*"Cosméticos e Perfumaria em 3D"*) and **Digital Feeling** publish no prices.
- ⇒ Label-exact motion and rotation cost **R$3.990 and 20–40 working days** at the one published studio, or **US$59/month self-serve** at Pacdora for template shapes. O LANÇAMENTO's R$2.990 in 5–7 days sits in a real price and speed gap. **But it cannot do a full rotation:** its product motion is camera moves over locked stills, or a turn of 15° or less.

## 3. Does anyone sell a per-asset fidelity report or a re-do guarantee for label errors?

- **Photoroom Enterprise Guarantee** ([page](https://www.photoroom.com/enterprise/guarantee)) is the only one found.
  - *"Our proprietary fidelity model checks every output against your agreed criteria, then we rework any that miss."*
  - *"built for Enterprise teams running visual production at scale in food or fashion"*.
  - *"Pricing, contract minimums, and vertical eligibility are set with your account team."*
  - Launched 1 Sep 2026: *"available to food and fashion teams as a yearly-contract"* ([blog](https://www.photoroom.com/blog/enterprise-guarantee-pay-for-pass)).
  - It counts *"Wrong color"* as a miss.
  - Its companion Visual QA says *"Only generations with 100% fidelity make it through"* ([page](https://www.photoroom.com/enterprise/visual-qa)).
- **Adobe Firefly IP indemnity** covers infringement, not fidelity, and is enterprise-only.
  - *"if you have purchased the appropriate entitlement (which will require a new contracting event)"* ([FAQ PDF](https://www.adobe.com/content/dam/dx/us/en/products/sensei/sensei-genai/firefly-enterprise/Firefly_Legal_FAQs_Enterprise_Customers.pdf), reader).
  - It excludes *"(A) any modification of a Firefly Output… (B) any combination of a Firefly Output with any other material"* ([PSLT PDF](https://www.adobe.com/content/dam/cc/en/legal/terms/enterprise/pdfs/PSLT-AdobeFireflySupplementalCoverage_2024v1.pdf), reader). **A composite would not be covered.**
- **Small-business tools and Brazilian studios offer nothing comparable:**
  - Pebblely: no refunds;
  - Villo: disclaims textual variation;
  - Orne: 2 iterations;
  - Claid, Pixelcut, Mokker, Flair, Criativoo, WekArts: no guarantee text found.
- ⇒ **A written, per-asset re-do guarantee plus report for a small Brazilian brand is scarce (verified absent in ~15 vendors; not exhaustive).** Photoroom proves the idea sells, and it could move down-market.

## 4. The repair: what is actually scarce, and the wording that stays true

**What is NOT scarce, and must stop being the headline:**

- "Sua embalagem aparece exatamente como na arte aprovada" on stills of a product standing in a scene.
  - Google does this free in Brazil.
  - Pebblely does it for US$9; Mokker for US$13; Pixelcut for US$10; Photoroom for US$12,99.
- VITRINE as written (6 scene stills + white background + 1:1/4:5/9:16 + a report, R$490) is exactly what these tools sell.
- The method itself is public.
  - Lamina: *"generate the setting, lighting, composition, and lifestyle context; keep verified product pixels or approved packaging artwork anywhere the SKU has to stay literal"* ([blog](https://uselamina.ai/blog/benchmark-can-ai-product-photography-generate-ecommerce-ready-images-without-changing-logos-labe), SECONDARY).
  - Higgsfield's own brand-asset recipe composites logos.

**What IS scarce, from the evidence above:**

1. **The real pack inside a human or in-use scene:** a hand holding the tube with fingers over the label, product on skin, in water, with refraction.
   - Cutout tools only stand the product on a surface.
   - Regenerating tools reach hands but redraw the label: 29% pass at best, and text is the top failure.
   - ⚠ Pixelcut claims its On Model format keeps the product fixed. That claim is **UNVERIFIED**, and it is the one test that could erase this gap.
2. **The real pack in motion inside a campaign world.**
   - Every AI video tool regenerates frames.
   - The 3D route is exact but slow (R$3.990, 20–40 working days) or template-bound (Pacdora).
3. **Speed and coherence:** a whole launch set in one world in 5–7 working days, plus a world kept on file for the next SKU.
4. **Accountability sold to a small brand:** a written re-do guarantee and a per-asset report. Only Photoroom does it, for enterprise food and fashion.
5. **Confidentiality:** Higgsfield trains on inputs; the composite route means unreleased art never reaches a generator.

**Proposed differentiator (sheet wording):**

> *"Fotos com o produto em uso e um filme em movimento — a IA cria as mãos, a pele, o cenário e a luz; a sua embalagem nunca passa por ela. Campanha completa, num só universo visual, em 5 a 7 dias úteis."*

**Proposed guarantee, true against every competitor above:**

> *"Garantia de embalagem: em nenhuma foto e em nenhum quadro do filme a IA inventa, troca ou deforma uma letra, o logo ou a forma da sua embalagem, e a cor fica dentro da tolerância aprovada na ficha. Se alguma peça falhar, refazemos sem custo em até 2 dias úteis. (Partes da embalagem podem ficar escondidas pela mão, pelo ângulo ou pelo foco, conforme o key visual aprovado — escondidas, nunca alteradas.)"*

**Proposed report line:**

> *"Cada peça sai com um relatório que compara a embalagem, pixel a pixel (no filme, quadro a quadro), com a imagem-mestre aprovada por você; os textos legíveis na peça são conferidos com o seu PDF."*

**Proposed confidentiality line:**

> *"Sua arte e suas fotos nunca são enviadas a um gerador de imagens nem a nenhum serviço online de IA: o trabalho com a embalagem é feito no nosso computador."*

- Operating rule behind it: Photoshop Select Subject / Remove Background runs on **Device**. *"By default, Photoshop uses Device processing"* ([helpx](https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/improved-select-subject-and-remove-background-results.html), reader); never switch it to Cloud.
- Never use Generate Background, Harmonize or Generative Fill on the pack layer.
- Higgsfield only ever sees the blank placeholder.

## 5. Claims on the current offer sheet that are false or weak

1. **"Sua embalagem aparece exatamente como na arte aprovada, em todas as peças."**
   - **Weak:** it is table stakes for stills.
   - **Partly false:**
     - the source is usually a *photo* of the physical pack, not the art;
     - hands and angles hide parts of the label;
     - integration grading shifts colour.
2. **"Todo caractere da embalagem idêntico à arte aprovada."**
   - True only for characters that are visible and not occluded, and only if the master is the art or an accurate photo of it.
   - Replace with "nenhuma letra inventada, trocada ou deformada".
3. **"Cada peça sai com um relatório que confere o rótulo contra o seu PDF."** and the sample line **"Lista de ativos OK"**: overclaim.
   - OCR cannot read an ingredient list at campaign scale.
   - The check is against the master image; the PDF check covers legible text only.
4. **Sample report "Cor da embalagem OK"** collides with integration grading, which is what makes a composite look shot rather than pasted.
   - Define a colour tolerance (for example a ΔE bound agreed on the ficha; the exact value is **UNVERIFIED** and to be set by test).
   - Otherwise the guarantee fails on the thing that makes the work good.
5. **"Sua arte não entra em nenhuma IA antes do lançamento."** Literally false if any AI segmentation, even local, or relight touches the pack.
   - Use the precise wording in §4.
   - If Pacdora is adopted, uploads go to its cloud. Its terms contain no training clause either way: **UNVERIFIED**.
6. **VITRINE R$490 sold on fidelity:** replicable for US$0–15.
   - Keep it only if it includes ≥2 in-use/in-hand shots and is sold on "same world as your launch".
   - Otherwise treat it as an add-on to O LANÇAMENTO, not a stand-alone product.
7. **"Filme de 15 s"** must not imply a rotating product.
   - Say "movimento de câmera e luz sobre a sua embalagem"; a full rotation is not included.
   - CGI studios and Pacdora do rotation exactly.

## 6. Design changes (summary)

1. Move the differentiator from "label-exact" to **"label-exact where others break it: in hands, in motion, in one world, in 5–7 days, with a written re-do guarantee."**
2. **Make the PRÉVIA an in-hand or in-use shot, never product-on-surface.** Pebblely, Google and Villo already give the latter away free.
3. **Master-image sourcing for pre-launch SKUs.** 0 of 15 new SKUs had a public photo (VER1), so the brand may have only the PDF.
   - (a) Ask for a phone photo of a physical sample; or
   - (b) render a label-exact master from the PDF in **Pacdora Business (US$59/mo, commercial and resale licence)** when a template matches the pack shape. That makes "idêntico à arte" literally true; or
   - (c) commission a one-off 3D model and keep it as part of the world on file.
   - Test Pacdora's shape match and transparent-background export first (both **UNVERIFIED**).
4. **Optional 360° insert** via Pacdora for template shapes, only after that test. Otherwise state "sem giro completo".
5. Rewrite the guarantee, report and confidentiality lines as in §4.
6. Define the colour tolerance and occlusion rules on the ficha the client signs.
7. **R$0 test before the first call:** run the same bestseller tube through Pixelcut Product Studio On Model and Photoroom's free tiers (the founder, on her own account).
   - If either keeps the label exact with a hand over it, in-hand scarcity falls.
   - What would remain: motion in a world, coherence, speed, the guarantee and the service.

## 7. Residual risks

- **No technology moat.**
  - The composite method is published, and Higgsfield's own recipe composites logos.
  - Criativoo already sells CGI + IA label-exact to Brazilian indie cosmetics (price unknown).
  - Any brand designer with Pacdora and Pixelcut can approach it.
  - The position is price, speed and service between self-serve (R$0–300) and CGI (R$3.990 in 20–40 days), not a moat.
- Pixelcut's "fixed product" claim may extend to on-model shots (**UNVERIFIED**).
- Photoroom may push its guarantee down-market. It is 3 weeks old and lists beauty as an industry.
- This repair does not touch the separate price-evidence problem: buyer posts were under US$500.

## Numbers (per image / video / month)

| Tool | Price (month) | Per image | Per video |
|---|---|---|---|
| Photoroom Pro | US$12,99/mo (US$89,99/yr) | ~US$0,013 per export | n/a |
| Photoroom Max | US$34,99/mo | n/a | ~US$0,70 |
| Photoroom Ultra | US$99/mo | n/a | ~US$0,66 |
| Photoroom API | n/a | US$0,10 per call | n/a |
| Pebblely | US$9 / 19 / 39 per mo | US$0,30 / 0,095 / 0,078 | no video |
| Claid Essentials | US$15/mo | US$0,12 | ~US$1,48 per 5 s (Pro) |
| Claid Pro | US$49/mo | US$0,098 | ~US$1,48 per 5 s |
| Flair Pro+ / Scale | US$26 / 38 per mo | US$0,33 / 0,25 | 3 / 5 videos a month |
| Mokker | US$13/mo | US$0,026 | n/a |
| Pixelcut | Pro US$10/mo · Business US$30/mo | n/a | n/a |
| Canva Pro | R$34,90/mo | n/a | n/a |
| Photoshop | R$65/mo | n/a | n/a |
| Google Product Studio | free | free | video US-only |
| Amazon Ads image generator | free | free | n/a |
| Higgsfield | PLUS US$49/mo | Product Shot 2K US$0,075 | 15 s US$4,46 (H6D) |
| Pacdora | Pro US$17/mo · Business US$59/mo | n/a | MP4 up to 2K |
| Orne | n/a | R$5,50–6,90 | R$29,90–89 |
| Villo | n/a | R$6,63 (R$19,90 = 3 variations) | R$50 per video ≤10 s |
| Fábrica AI | n/a | R$35 per 3 images | n/a |
| Make Move | R$3.000 per 65 photos | ~R$46 | n/a |
| PhotoGen | R$25 / 37 / 87 | n/a | n/a |

**CGI studios:**

- WekArts: R$2.590 (3D pack, label artwork, 2 renders); R$3.990 (4 renders + 20 s motion); 20–40 working days.
- Lou Studios market estimate: R$3.000–12.000 basic, R$15.000–45.000 intermediate, R$50.000–150.000+ premium.
- Criativoo: price on request.

**Counts:**

- Stills preserve: 12 routes (10 self-serve + 2 CGI).
- Stills regenerate: 10.
- Label-exact motion: 3D only (1 self-serve tool plus ≥3 studios).
- Fidelity guarantees for small businesses: 0. Enterprise: 1 (Photoroom).
