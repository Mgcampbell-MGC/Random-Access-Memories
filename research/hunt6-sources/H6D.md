# H6D — source log (production fidelity, hours, cost, replacement cost, treadmill, backlash) — 25 Sep 2026

One line per source: what it said. PRIMARY = the party's own page/doc/statute/dataset or an academic paper; SECONDARY = press, practitioner or tool-vendor blog; VENDOR CLAIM = marketing assertion. Local copies in `work/h6d/`.

## Fidelity — evidence
- https://www.photoroom.com/blog/top-editing-image-models-maintain-product-details-only-28-of-the-time — PRIMARY (vendor benchmark, 6 Jul 2026): 850 products (clothing, footwear, bags, jewelry, accessories), 4 models at 2K, >=3 of 10 annotators, one flag = fail, 30 s minimum review. Pass: Nano Banana 2 29,0% · Nano Banana Pro 28,2% · GPT Image 2 Medium 27,2% · FLUX.2 Klein 9B 16,8%; + Photoroom Fidelity Layer 38,2%. "Logo and text distortion was the most common failure, affecting 20.1% of all base-model generations." Soft goods, not cosmetic bottles.
- https://www.photoroom.com/blog/fidelity-gap-ai-product-photography — PRIMARY (31 Jul 2026): repeats 29%; "37% of enterprise leaders" (Photoroom B2B survey, Mar 2026) name inaccurate visuals their top AI-imaging concern.
- https://arxiv.org/abs/2606.19103 (PDF grepped) — PRIMARY (17 Jun 2026) ProductConsistency: 870-edit benchmark incl. 140 Personal Care; labels 5-12 words; summed per-image CER Nano Banana 1,1868 · GPT-Image-1 High 0,3315 · Flux.1 Kontext-dev 0,1490; closed models "not sufficient for consistent product fidelity"; limitation: curved/stylized text "remain challenging"; RL fine-tune ~5x CER cut.
- https://arxiv.org/abs/2604.24023 (PDF grepped) — PRIMARY (ServImage, MBZUAI): 1.070 paid crowdsourced design tasks, product median US$139; Gemini-Banana-Pro task acceptance 70,50%, deliverable 79,88%, 83,4% of product-category value.
- https://arxiv.org/abs/2609.04151 (PDF grepped) — PRIMARY (Phota Labs, faces): GPT-Image-2 identity similarity ~0,71 -> 0,56 and NB2 ~0,70 -> 0,49 as face scale shrinks; worse under iterative edits.
- https://masonry.so/blog/best-ai-video-model-for-product-ads — SECONDARY (3 Jun / 16 Aug 2026): serum bottle, Kling O3 Pro "Dense side copy was invented as the bottle turned"; Veo 3.1 and Seedance 2.0 invented coffee/steam on a mug; one candidate per model, "not a statistically powered benchmark".
- https://kling.ai/quickstart/klingai-video-3-model-user-guide — VENDOR CLAIM (6 Feb 2026): Kling 3.0 "can automatically identify text content in uploaded images (such as signs, captions, or logos) and maintain text consistency, avoiding issues such as text displacement or blurring".
- https://www.prnewswire.com/news-releases/kling-ai-launches-3-0-model-ushering-in-an-era-where-everyone-can-be-a-director-302679944.html — PRIMARY (Kling AI release, 5 Feb 2026): Kling 3.0 series launch; "Better preservation of text in imagery".
- mcp Higgsfield get_workflow_instructions product-photoshoot + references/refinement-pass.md — PRIMARY (vendor recipe, pulled 25 Sep 2026): model locked to nano_banana_pro 2K; "Warped text — label letters mangled or AI-fictional" listed as a common defect; max 3 generations per final output; fix = regeneration; "Do not claim tiny text or full-resolution sharpness is verified from a thumbnail."
- mcp Higgsfield get_workflow_instructions brand-asset-creation — PRIMARY (vendor recipe): "Never redraw an uploaded logo when it can be placed or composited exactly"; mockups use GPT Image 2 as a second stage to apply text with locked placement.
- https://higgsfield.ai/blog/new-marketing-studio-higgsfield — PRIMARY (18 Aug 2026): 1.500+ one-click templates; only Posters are editable, "Other categories get regenerated instead of edited"; 8 s 720p 47,62 credits (US$2,38), 15 s 720p 89,2 (US$4,46), Product Shot 2K 1,5 (US$0,075), Posters 2K 7,5 (US$0,38); target users include brand owners "without a creative team or agency budget" and agencies.
- https://www.adobe.com/products/photoshop/harmonize-image-blender.html — PRIMARY: Harmonize blends "in seconds"; "adjusts the subject's lighting, shadows, colors, and reflections in a click"; "Your added element will be recreated" (it regenerates the object — label must be re-overlaid).
- https://primores.org/wiki/marketing/ai-product-video-fidelity/ — SECONDARY (Jun 2026): real product composited, first/last-frame keyframes, 3-5 s clips, 2-3 seeds per segment; limits "on-product text under motion, and any occlusion".
- https://domoai.app/blog/ai-product-videos-without-warping-the-product — SECONDARY (23 Aug 2026): composite product as locked still; 4-6 takes per segment; check frames 1, 5-10, last.
- https://www.yahoo.com/entertainment/articles/chaotic-kalshi-ad-during-nba-173937071.html — SECONDARY (Business Insider, 13 Jun 2025): Kalshi ad "300 to 400 generations to get 15 usable clips", two days, US$2.000.
- https://www.thewrap.com/coca-cola-ai-christmas-ad-2025/ — SECONDARY (3 Nov 2025): 70.000+ clips, 5 AI specialists, 30 days.
- https://www.nvidia.com/en-us/case-studies/unilever/ — SECONDARY (vendor case study): Unilever digital twins contain "all product variants, sizes, labels, language versions"; 2x faster, 50% lower imagery cost. (unilever.com press release: HTTP 403.)
- https://blog.google/innovation-and-ai/products/nano-banana-pro/ — PRIMARY (20 Nov 2025): NB Pro launch; in Gemini app, Google Ads, Slides, Vids; SynthID on all; visible watermark on free and AI Pro tier images, removed for Ultra and AI Studio.

## Release cadence (treadmill)
- https://blog.google/products/gemini/updated-image-editing-model/ — PRIMARY: Nano Banana (Gemini image editing upgrade), 26 Aug 2025.
- https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/ — PRIMARY: Nano Banana 2, 26 Feb 2026.
- https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/ — PRIMARY: Nano Banana 2 Lite, 30 Jun 2026.
- https://en.wikipedia.org/wiki/GPT_Image — SECONDARY (openai.com returned 403): GPT Image 1 25 Mar 2025; gpt-image-2 21 Apr 2026; GPT Image 2.5 8 Sep 2026.
- https://seed.bytedance.com/en/blog/seedance-2-0-official-launch — PRIMARY: Seedance 2.0, 2026-02-12, "higher usability rate", commercial advertising named as a use case.
- https://seed.bytedance.com/en/seedance2_5 — fetched; model page, no launch date found (Seedance 2.5 date UNVERIFIED).

## Stack prices (BRL)
- https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/ (CotacaoDolarPeriodo 15-25 Sep 2026) — PRIMARY: PTAX venda 24 Sep 2026 = 5,1795.
- https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/decreto/d12499.htm — PRIMARY: IOF 3,5% on card purchases of goods/services abroad.
- HIGGSFIELD_FACTS.md (MCP show_plans_and_credits) — PRIMARY: PLUS US$49/mo 1.000 credits; ULTRA US$129 3.000; top-up 18 credits/US$ => R$262,68 / R$691,54 incl. IOF.
- https://www.adobe.com/br/products/photoshop/plans.html and https://www.adobe.com/br/creativecloud/plans.html — PRIMARY (via WebFetch; curl blocked): Photoshop R$65,00/mês annual billed monthly; Photography plan R$55,00; CC Pro R$99,00 promo / R$214,00 regular.
- https://apps.apple.com/br/app/capcut-editor-de-v%C3%ADdeo/id1500855883 — PRIMARY observed listing: CapCut Pro Monthly R$65,90; Standard R$32,90.
- https://apps.apple.com/br/app/canva-design-foto-e-v%C3%ADdeo/id897446215 — PRIMARY observed listing: Canva Pro Mensal R$34,90-35,00; Anual R$289,90.
- https://apps.apple.com/br/app/chatgpt/id6448311069 — PRIMARY observed listing: ChatGPT Plus R$99,90; Go R$39,90.
- https://apps.apple.com/br/app/google-one/id1451784328 — PRIMARY observed listing: 200 GB R$14,99/mês; Google AI Plus (2 TB) R$49,99.
- https://frame.io/pricing — PRIMARY: Free US$0 (2 members, 2 GB); Pro US$15 per member per month + tax; Team US$25.
- https://workspace.google.com/intl/pt-BR/pricing.html — PRIMARY page but prices rendered by JS (not extractable); https://manualdousuario.net/google-workspace-gemini-ia-aumento/ — SECONDARY (20 Jan 2025): Business Starter R$35 -> R$40,90.

## Replacement cost / scarcity
- https://t31158996.p.clickup-attachments.com/t31158996/ca3aa2b8-79d8-4bde-9c72-16be858767af/Tabela-guia-salarial-2026-robert-half-mundo-do-marketing.pdf (linked from https://guia-salarial.mundodomarketing.com.br/) — PRIMARY (Robert Half Guia Salarial 2026 table): São Paulo, Analista de marketing digital (P/M) p25/p50/p75 R$6.050/9.000/11.000; Coordenador(a) de marketing digital (P/M) R$11.000/13.000/16.000; salary only.
- https://www.roberthalf.com/br/pt/insights/guia-salarial/vendas-marketing — PRIMARY page, shows only executive ranges in HTML.
- https://www.salario.com.br/profissao/analista-de-marketing-cbo-142335/sao-paulo-sp/ — fetched; served a paywalled illustrative landing page (figures not usable).
- https://br.indeed.com/career/analista-de-marketing/salaries/S%C3%A3o-Paulo--SP — HTTP 403.
- https://www.99freelas.com.br/freelancers?q=midjourney | ?q=kling | ?q=nano+banana | ?q=higgsfield — PRIMARY observed counts (25 Sep 2026): 233 / 62 / 23 / 12 freelancers (national). Multi-word queries return inflated OR-matches (e.g. 5.115, 77.647) — not used.
- https://www.99freelas.com.br/freelancers?q=higgsfield — PRIMARY: 10 listed profiles, mostly 0 completed projects, several registered 2025-2026 ("AI Creator... Kling, Seedance, Higgsfield do briefing à peça", joined 07/07/2026).
- https://www.99freelas.com.br/projects?q=kling | ?q=higgsfield | ?q=video+ia+produto — PRIMARY: AI-video projects drawing 12-31 proposals each.
- https://www.workana.com/... and https://www.fiverr.com/search/gigs?query=ai%20product%20photography — HTTP 403.
- https://www.fotografiadeprodutos.com.br/ — observed (search snippet only, not fetched): "FOTOGRAFIA DE PRODUTOS R$ 7,00 POR FOTOGRAFIA" (São Paulo e-commerce packshots) — UNVERIFIED.

## Backlash / rules
- https://www.prnewswire.com/news-releases/dove-marks-20-years-of-real-beauty-with-a-renewed-commitment-to-real-and-pledge-to-never-use-ai-to-represent-real-women-in-its-advertising-302111130.html — PRIMARY (9 Apr 2024): Dove pledges never to use AI to represent real women; scope = people, not products.
- https://news.designrush.com/no-ai-disclaimers-brands-consumer-trust-2026 — SECONDARY: Aerie (Oct 2025) "never to use AI-generated bodies or people"; Cadbury, LEGO, Polaroid, Almond Breeze 'no AI' campaigns.
- https://www.cnn.com/2025/07/31/style/vogue-ai-models-guess-campaign — SECONDARY (search result, not fetched): Guess AI models in Vogue Aug 2025, backlash.
- https://www.meioemensagem.com.br/comunicacao/ia-avanca-mas-consumidor-ainda-prefere-criacao-humana — SECONDARY (14 Jul 2025) citing Ipsos AI Monitor 2025 Brazil (21 Mar-4 Apr 2025, ~1.000 urban adults, ±3,5 pp): 62% prefer human-made ad campaigns vs 22% AI; 38% trust AI for ad images/videos; 35% trust companies more when AI enhances product images.
- https://www.cartacapital.com.br/do-micro-ao-macro/inteligencia-artificial-influencia-compras-brasileiros/ — checked: does NOT contain the 62% figure (Branddi survey, Jan 2026, n=500) — the 62% is Ipsos, not Branddi.
- https://acontecendoaqui.com.br/marketing/ia-divide-marcas-e-consumidores/ — checked: UK/US Censuswide survey only, no Brazil data.
- https://nielseniq.com/global/en/news-center/2024/niq-research-uncovers-hidden-consumer-attitudes-toward-ai-generated-ads/ — PRIMARY (12 Dec 2024): >2.000 participants, ~150 EEG; AI ads identified, "annoying, boring, confusing", weaker memory activation.
- https://conar.wpenginepowered.com/wp-content/uploads/2026/05/260525_GUIA_INFLUENCIADORES_CONAR_v6.pdf (linked from https://www.conar.org.br/) — PRIMARY (PDF grepped) §1.3.1: CBAP applies to AI content; "Anunciantes, Agências e demais partes da cadeia" remain responsible; no "apresentação visual... simulações" that mislead on "atributos, desempenho"; footnote 6: guide does not create disclosure duties.
- https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content — PRIMARY: significantly AI-generated content must carry the AIGC label or clear disclaimer or "your ad will be rejected or restricted"; "Removing or modifying backgrounds" listed as an insignificant AI edit.
- https://www.kasznarleonardos.com/conar-arquiva-representacao-contra-campanha-publicitaria-da-volkswagen-que-recriou-imagem-da-cantora-elis-regina/ — SECONDARY (search result): CONAR archived the VW/Elis Regina AI case (2023) with a motion to monitor AI in ads.
- https://www.cnnbrasil.com.br/tecnologia/por-que-2026-pode-ser-o-ano-do-marketing-anti-ia/ — SECONDARY (17 Dec 2025): 'anti-AI marketing' thesis; no Brazilian data.

## Not used / blocked
- https://ir.kuaishou.com/... (Access Denied), https://openai.com/index/introducing-chatgpt-images-2-0/ (403), https://www.unilever.com/... (403), https://docs.photoroom.com/image-editing-api-plus-plan/ai-backgrounds (no statement on subject pixels).
- No Higgsfield credits were spent (founder account 7,88 credits left for the R$0 test).
