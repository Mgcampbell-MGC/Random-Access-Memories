# VER1: source log (O LANÇAMENTO plan verification), Hunt 6, 25 Sep 2026

Pages were fetched on 25 Sep 2026, either with curl (browser User-Agent) or, where marked, through the r.jina.ai reader, which returns the page text verbatim. Raw captures are in `work/ver1/`: `nnfull2/*.json` (99Freelas projects), `wk/*.md` (Workana), `orne/*.js`, `villo_*.html`, `bf/p*.json`, `hf/*`, `alt/*`, `pv/*`.

The FX rate is the PTAX venda for 24 Sep 2026, 5,1795, from https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo (fetched; 21–24 Sep series).

## 1. Buyer posts

### 99Freelas method
Project pages are reachable by ID through `https://www.99freelas.com.br/project/x-{id}`, which resolves regardless of slug.
- ID dates: 765000 is 2 Jul 2026 (first proposal); 775000 is 11 Aug; 784923 is 16 Sep; 786854 is 24 Sep.
- I enumerated IDs 763000–787500, covering 26 Jun to 25 Sep 2026. That gave 24.501 IDs and 17.077 live project pages.
- I fetched 6.727 of them in full, chosen by title regex (beauty, AI, video, image, product, campaign, art, design, visual and similar words).
- From each page I extracted the full `data-content` description, the "Data da publicação", Propostas, Orçamento, Valor Mínimo and "Freelancer vencedor".
- Budget field: 6.702 of 6.727 read "Orçamento: Aberto", with a platform minimum of R$30–100. Offers show as "Privado". **99Freelas never shows a buyer budget.**

### 99Freelas projects found
- https://www.99freelas.com.br/project/producao-de-videos-com-ia-para-e-commerce-e-marketplaces-768972 (18/07/2026 13:06)
  - Buyer words: "Tenho uma loja de dermocosméticos e produtos de estética… Vídeos de produtos criados com IA generativa… Mercado Livre, Shopee, TikTok Shop e Instagram Reels… Forneço fotos PNG dos produtos, logotipo e descrições técnicas. Início: teste pago com 2 vídeos."
  - Aberto, minimum R$50; 9 proposals; "Freelancer vencedor Claudia A."
  - **This is the plan's July buyer: a STORE, not a brand.**
- https://www.99freelas.com.br/project/criar-videos-e-imagens-para-3-produtos-na-shopee-773216 (04/08/2026)
  - Nail polish, 3 products: 6 AI ambient images per product plus AI clips.
  - The buyer asks for "os prompts e a indicação da ferramenta… para que possamos fazer pequenos ajustes no futuro".
  - 11 proposals; awarded to Adson J.
- https://www.99freelas.com.br/project/editor-para-vsl-estilo-tiktok-ugc-de-produto-de-beleza-784663 (15/09/2026): edit of a VSL for a lip product with an AI presenter. 2 proposals, no winner.

### Fidelity-clause briefs, all non-beauty
- https://www.99freelas.com.br/project/criacao-de-imagens-para-marketplace-776283 (14/08/2026) and …-de-brinquedos-educativos-776351 (15/08/2026, 55 proposals): "o produto deve permanecer totalmente fiel às fotos originais, sem alterar cores, formato, proporções…"
- https://www.99freelas.com.br/project/imagens-de-capa-e-carrossel-para-e-commerce-781340 (02/09/2026, 208 proposals): "a fidelidade ao produto físico deve ser 100%".
- https://www.99freelas.com.br/project/adaptacao-de-video-publicitario-com-ia-784613 (15/09/2026, winner Peter D): "preservar formato, proporções, acabamento…"
- https://www.99freelas.com.br/project/criar-imagens-realistas-de-moda-com-ia-771869 (29/07/2026, 36 proposals): "preservar fielmente o produto (cor, textura, detalhes e caimento)".
- https://www.99freelas.com.br/project/videos-com-ia-para-anuncios-do-mercado-livre-766504 (08/07/2026, winner Denis R.): "mantenham fidelidade ao produto real".
- **No beauty brief with packaging, logo, text, colours and geometry preservation was found, so the plan's "August 2026 brief" is UNVERIFIED.**

### Workana method
Direct curl returns 403 (Cloudflare). I read listings through r.jina.ai with `X-Engine: browser` and `X-With-Links-Summary: true`. That covers 33 queries (1–3 pages each), giving 155 distinct open jobs. The listing shows budget, proposals and sometimes the client's country flag. Job pages were read through r.jina.ai for the publication date and text. Insight pages ("Dados dos concorrentes") return "Access Denied".

### Workana jobs found
- https://www.workana.com/pt/job/editor-de-videos-com-ia-para-reels-e-tiktok-personagem-consistente-para-perfumaria-premium: published 24 Sep 2026; USD 250–500; 12 proposals. Brief: 30 AI videos, "preservando a autenticidade dos produtos".
- https://www.workana.com/pt/job/editor-de-video-vertical-com-ia-para-tiktok-reels-de-marca-de-cosmeticos: 19 Aug 2026; USD 50–100; 15 proposals. Brief: AI video pilot of up to 2 min for a cosmetics brand.
- https://www.workana.com/pt/job/editor-de-video-para-campanha-de-marca-de-korean-beauty: 11 Sep 2026; USD 50–100; 19 proposals; Brasil. Brief: 30 s launch film re-edit for a new Brazilian K-beauty brand.
- https://www.workana.com/pt/job/editor-de-video-para-conteudo-de-beleza-e-cosmeticos-tiktok-reels: 19 Aug 2026; < USD 50; 6 proposals. Dudéa, a new beauty brand; paid test of 1–3 videos.
- https://www.workana.com/job/edicao-profissional-de-video-de-beleza-maquiagem-2-minutos-de-duracao-final: < USD 50; 2 proposals; BR.
- https://www.workana.com/job/editor-de-video-para-vsl-de-direct-response-nicho-skincare: < USD 50; 13 proposals; BR.
- https://www.workana.com/job/designer-para-desenvolvimento-de-identidade-visual-de-marca-de-cosmeticos: USD 100–250; 26 proposals; BR. This is branding.
- https://www.workana.com/job/desenvolvimento-de-identidade-visual-e-branding-para-nova-marca-de-cosmeticos-infantis: USD 500–1.000; 30 proposals. This is branding.
- https://www.workana.com/pt/job/creacion-de-video-para-marca-dermocosmetica-cosmetic-science: 06 Oct 2025, an Argentine (ANMAT) buyer. Budget not visible, and not Brazil.

### Search engines
Six or more WebSearch queries for the two briefs (Workana and 99Freelas site searches, the Portuguese phrases) returned nothing beyond the above.

## 2. Orne and Villo

### Orne
- https://studio.orne.ai/: an SPA whose HTML has no prices. JSON-LD reads "Plataforma de conteúdo visual com IA para moda", parent Orne.ai.
- The route `/tabeladepreco` ("Tabela de preços — Orne.Studio") is chunk https://studio.orne.ai/assets/Dx6k-TZz.js. Its price array per unit (base price, then floor):

  | Line | Base | Floor |
  |---|---|---|
  | Imagens Ambientadas | R$5,5 | R$3,9 |
  | Mais Poses | R$5,5 | R$3,9 |
  | Cena com Modelo — Imagem | R$6,9 | R$4,9 |
  | Social Media Creator | R$25 | R$18 |
  | Vídeo 360° | R$65 | R$55 |
  | Vídeo Ambientado (5 s) | R$85 | R$72 |
  | Cena com Modelo — Vídeo 5s Essencial | R$29,9 | R$24 |
  | Cena com Modelo — Vídeo 5s Premium | R$49,9 | R$42 |
  | Cena com Modelo — Vídeo 10s Premium | R$89 | R$75 |

  - "Iterações incluídas: 2"; "Desconto por volume: 200+ = -10%, 500+ = -20%, 1000+ = -35%"; "Orçamento válido por 15 dias".
  - Feature bullets include "Fidelidade total ao produto" and "Joia, calçado, roupa, acessório".
- Other chunks (`orne/*.js`) contain a "Cosméticos & Beleza" prompt preset: "The EXACT cosmetic from the reference image — 100% identical: packaging form, label content, typography, color…"
- They also contain a per-model cost table (Freepik API endpoints) with costBrl values:
  - Images: Seedream V4 0,17, Flux Pro 1.1 0,23, Imagen 3 0,26, HyperFlux 0,85.
  - Video, per second: Pixverse V5 0,21, Kling 2.5 Pro 0,37, Kling 3 Pro 0,89, Runway 4.5 1,06.
- https://orne.ai/: the parent's B2B AI agents, e.g. "SDR Autônomo… R$ 1.490 a R$ 4.900/mês".

### Villo
- villo.ai is Villo, a Swedish AI property-video company, **not the plan's Villo**. villo.com.br gives a proxy 502.
- https://www.villo.ia.br/precos (Wix):
  - Teste Grátis: 1 image.
  - START R$19,90 per pacote: 1 product, 3 variations.
  - IMPULSO R$59,90: up to 5 × 3, plus models.
  - ESCALA R$99,90: up to 10 × 3.
  - Social media R$250 / 350 / 600 per pacote (≤10 / 15 / 30 posts a month).
  - Video R$50 per video ≤10 s.
  - Campaigns: "Falar com consultor".
- https://www.villo.ia.br/: "ganhe Grátis uma imagem teste do seu produto"; traditional shoot "R$ 1.200 a R$ 4.000 por sessão" (the firm's own marketing claim).
- https://www.villo.ia.br/termos-condicoes:
  - "pequenas variações visuais, textuais ou compositivas podem ocorrer entre versões"
  - "obrigação de meio"
  - liability limited "ao valor efetivamente pago"
- The footer names Luque Partners Ltda, CNPJ 18.681.190/0001-15.

## 3. Beauty Fair
- https://beautyfair.com.br/expositores/ returns 200. Data comes from https://cms.beautyfair.com.br/beautyfair/wp-json/custom/v1/node?path=expositores&paged=1…33 (all 33 fetched).
- Block title: "Descubra quais foram as marcas que marcaram presença em 2026". Pagination: total_items 491, total_pages 33. I counted 491 distinct ids.
- ctaEvent: Expo Center Norte, "4 a 7 setembro 2027".
- Tags: Cabelos 161, Skincare 109, Maquiagem 104, Perfume 99, Cosméticos 77, Unhas 73, Acessórios 57, Estética 56, Cílios 48, Equipamentos 43, Higiene 43, Barber 40, Sobrancelhas 40, Móveis 25, Podologia 24, Depilação 22, Micropigmentação 21, Proteção Solar 17, Ferramentas 14, Embalagem 12, Suplementos 9, Mídia 6, Gestão 5, Sindicato 4, Transportadora 4, Tesouras 1.
- Hair or skin (Cabelos, Skincare or Proteção Solar): 229; 236 with Barber added. Of the 229, 34 also carry a supplier tag.
- Record fields: id, title, url, thumbnail, categories, link. The 33 pages contain 0 email strings and 0 tel or WhatsApp links. Links among the 229: Instagram 125, website 95, none 9.

## 4. Preview test
- ANVISA file: `work/TA_CONSULTA_COSMETICOS.CSV`, downloaded today from https://dados.anvisa.gov.br/dados/CONSULTAS/PRODUTOS/TA_CONSULTA_COSMETICOS.CSV.
  - Filter: hair/skin keywords, DT_VENCIMENTO 2036-07-27 to 2036-09-25 (notified 2026-07-27 to 2026-09-23). Result: 4.929 rows, 792 holders.
  - 1.026 rows (20,8%) have an identical normalised product name under another process number (dated earlier, or undated with situação N). That share is a lower bound on re-notifications.
- Random 15 (seed 20260925): 3 exact, all re-notifications; 3 sibling-only; 9 none. Sources per row are in the JSON. Main pages:
  - caaspshop.com.br and superfumaria.com.br: Derma Fine.
  - walmart.com: Keune After Color.
  - avlon.com: Affirm.
  - mundodavaidade.com.br: Yoyo Maquiamor Mask Stick Vit C, the sibling.
  - estorilcosmeticos.com.br/carrinho/le-botanique-olive/: 2 em 1 Olive, the sibling.
  - eaebrazil.com.br/products.json: 160 products; Condicionador and Máscara Macadâmia & Mel exist, the shampoo does not.
  - nassdermocosmetique.com.br: "A loja está temporariamente fora de serviço".
  - veromarcosmeticos.com.br, beauline.com.br and loovycare.com.br: private-label factories.
- ICP 6:
  - Adcos Stick FPS 80 Peach: belezanaweb.com.br. The same product was notified in 2019 as "…STICK FPS UVB 80 PEACH".
  - Natura Faces máscara: natura.com.br NATBRA-67647.
  - Neutrogena Hydro Boost Water Gel FPS 25: neutrogena.com.
  - Wella Ultimate Hydra: only Ultimate Repair and Smooth appear.
  - Widi Care Juba: widicare.com.br/produto/juba-shampoo/.
  - Alia Beauty PDRN: no match.
- CNPJ lookups: publica.cnpj.ws for 16 holders, stored in `work/ver1/cnpj/`.
- Blocked:
  - instagram.com through r.jina.ai: "AbuseAlleviationError… Anonymous access to domain www.instagram.com blocked".
  - lista.mercadolivre.com.br: redirects to account verification.
  - adcos.com.br VTEX API and natura.com.br search: 403 / Cloudflare.
  - aliabeauty.com.br, sancare.com.br and several guessed domains: proxy 502 or no DNS.

## 5. Training terms
- Higgsfield Terms of Use, https://higgsfield.ai/terms-of-use-agreement (the /terms and /terms-of-service paths 404). "Last updated: July 26, 2026".
  - §4.4: "Your Content, Inputs, and Outputs may be used by Company to train… Different terms apply to enterprise and business customers who use the Service under an Enterprise Agreement… Company does not use the customer's content to train… You can stop this going forward by deleting Your Content or your Account".
  - §4.2: the user warrants rights in the content.
  - §16.5(c)(iii): content already trained on cannot be removed.
- Higgsfield Privacy Policy, https://higgsfield.ai/privacy-policy (effective Aug 27, 2026):
  - §2.3: Inputs and Outputs are used "to train and improve our (and our affiliates') AI models".
  - §4: data is shared with "third-party AI model and compute providers".
- https://higgsfield.ai/enterprise:
  - "Higgsfield Enterprise never trains models on your data… contractual no-train guarantee… built for unreleased products, embargoed campaigns, and confidential client material."
  - "credit-based pricing on annual contracts with monthly payments, sized to your team's seats"; Contact Sales.
- https://higgsfield.ai/team-plan: no no-training statement.
- Adobe General Terms, https://www.adobe.com/legal/terms.html (through r.jina.ai; direct curl got an empty reply or HTTP/2 error). "Published October 3, 2025": "We will not use your Local or Cloud Content to train generative AI models except for Content you choose to submit to the Adobe Stock marketplace".
- https://www.adobe.com/ai/overview/firefly/gen-ai-approach.html (through r.jina.ai): "User data and content within our applications are not, and will not be, used to train generative AI models—whether those models are from Adobe or its partners."
- Gemini API terms, https://ai.google.dev/gemini-api/terms (through r.jina.ai; direct fetch loops on OAuth):
  - Paid Services: "Google doesn't use your prompts (including… files such as images…) or responses to improve our products".
  - Unpaid Services: "Do not submit sensitive, confidential, or personal information".
