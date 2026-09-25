# W2A — CONSENT lens — source log (25 Sep 2026)

Fetched with curl (browser UA) unless marked SEARCH-SNIPPET (a search-result summary, SECONDARY, not a fetched page). Raw files: work/w2a/.

## Voice consent marketplaces (ElevenLabs — vendor's own docs and API)
- https://elevenlabs.io/docs/eleven-creative/voices/voice-library — "The Voice Library is a marketplace where our community can share Professional Voice Clones and earn rewards when others use them. Currently, only Professional Voice Clones can be shared. Instant Voice Clones and voices created with Voice Design are not shareable."
- https://elevenlabs.io/docs/eleven-creative/voices/payouts — Payouts go through Stripe Connect; the "Supported countries" list runs Argentina, Australia … Mexico … Peru … Portugal … Uruguay, Vietnam. BRAZIL IS ABSENT (string count 0 on the whole page). US withholding at 30% applies to US-customer usage only when no treaty is claimed. Minimum payout usually US$10.
- https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning — "Can I create a Professional Voice Clone of someone else's voice? No. You can only create a Professional Voice Clone of your own voice. Even with their consent, you cannot clone someone else's voice." ⇒ no agent or label can hold a talent's PVC.
- https://elevenlabs.io/blog/22-million-earned-by-voice-creators-on-elevenlabs — "$11 million" by Nov 2025, "over $22 million" six months later; "10,400+ creators earning" (vendor's own figure; average ≈US$2.115 per creator over the life of the programme). Voices in 32 languages.
- https://elevenlabs.io/blog/monetize-your-voice-with-elevenlabs-voice-library-and-create-passive-income — "The base rate is $0.03 per 1,000 characters"; HQ or rare voices "up to $0.20 per 1,000 characters"; Creator plan US$22/month needed to make a PVC; at least 30 minutes of audio.
- https://api.elevenlabs.io/v1/shared-voices?language=pt&page_size=3&sort=usage_character_count_1y — unauthenticated API (max 3 voices, filters return 401): total_count 6.057 Portuguese voices; top 3 by 12-month usage all pt-BR: "Keren" 4.281.259.807 characters, "Matheus" 958.720.799, "Amandoca" 743.241.884. At the blog's base rate Keren alone ≈US$128k/yr (the payout formula actually applied is UNVERIFIED).
- Same endpoint, other languages (top voice, 12-mo characters): es 13,1 bn (8.162 voices) · en 20,5 bn (10.865) · hi 8,4 bn (6.853) · de 7,0 bn (6.673) · fr 3,9 bn (4.057) · it 1,8 bn (5.271) · ja 0,8 bn (592). PT-BR demand is real, the head is ~1/3 of Spanish.
- https://elevenlabs.io/iconic-marketplace + SEARCH-SNIPPET (musically.com, radioworld, variety) — Iconic Marketplace launched 11 Nov 2025: 28 celebrity/estate voices, rights partner CMG Worldwide; brands request, rights-holder approves; no published price.

## Likeness / twin consent marketplaces
- https://www.modelmanagement.com/digital-twins/ — "Browse 100,000+ pre-consented AI twins … API integration for platforms"; "Every twin we license is a real, ID-verified person with documented, timestamped consent"; models withdraw consent any time. Site languages EN/ES/DE/FR/IT (no Portuguese).
- https://www.modelmanagement.com/digital-twins-for-models/ — models "set your own price range for licensing your digital twin"; brand sends booking request with usage and payment.
- https://getdigitaltwin.ai/ — "Lease pricing is flat at $99/twin/month across every tier"; plans Silver US$99/mo, Gold US$299/mo, Diamond US$599/mo; members "recorded a 20-second consenting take". Seller asking, with buy buttons.
- https://www.pixelz.com/digital-twins/ — Pixelz sells "Digital Twins … hyper-realistic, AI-generated digital models created from" real people for e-commerce content.
- https://www.heygen.com/pricing — Free plan US$0 includes "500+ Stock Video Avatars" and "1 Custom Video Avatar"; Creator US$29/mo adds Voice Cloning; Business US$149/mo.
- SEARCH-SNIPPET https://www.synthesia.io/post/introducing-synthesia-talent-experience-program-for-exceptional-actors (+ Slashdot/TechCrunch) — stock-avatar actors license likeness 3 years for a flat fee (one report ~US$5.000); US$1M equity pool for popular actors. SECONDARY.
- SEARCH-SNIPPET https://movie.io/ — "AI talent agency", actors keep 95%, platform 5%. SECONDARY.
- https://www.lotiai.com/ — "Likeness Protection for Everyone — Track your face and voice across the internet, for free." Free monitoring + takedowns; paid tiers for public figures.
- https://vendedores.mercadolivre.com.br/nota/editor-de-fotos-uma-ferramenta-para-melhorar-seus-anuncios — Mercado Livre's own seller tool "gera fotos profissionais com inteligência artificial a partir da sua foto de capa. Assim, não é necessário passar por uma sessão de fotos".
- SEARCH-SNIPPET (CNN Brasil, fashionunited.com.br) — H&M 30 digital twins, models own the twin; Dafiti Black Friday 2025 "Modo Absurdo" with Vitória Strada's digital twin by agency House of Rabbits (portal.saladanoticia.com.br returned 403). SECONDARY.
- https://papagaioai.com/ — sells cloned voices of "Neymar, Galvão, Faustão, Silvio Santos, Datena" and "+50 vozes" from R$19, "+50.000 gerações" — unauthorised-looking supply of famous Brazilian voices at consumer prices.

## Consent in Brazilian advertising (rules)
- https://www.conar.org.br/codigos → https://conar.wpenginepowered.com/wp-content/uploads/2026/08/Codigo_CONAR_2026.pdf (83 pp., downloaded, grepped) — Anexo Q: 3.b "Os modelos profissionais, os empregados do Anunciante ou das Agências de Propaganda não deverão se fazer passar por Consumidor comum"; 3.c consumer testimony "limitado à experiência pessoal com o produto"; 5.a "Todo Anunciante, ou sua Agência, estará obrigado a comprovar/demonstrar a veracidade do testemunhal, sempre que isto lhe for solicitado"; 6.a "deverá obter autorização escrita da testemunha antes de proceder à veiculação. Essa autorização poderá ser exigida pelos veículos." The strings "inteligência artificial"/"sintétic" appear 0 times in the 2026 code.
- SEARCH-SNIPPET (migalhas.com.br, smabr.com) — CONAR's new influencer guide (effective June 2026) says ads made with AI follow the same rules and expressly does NOT create an AI-disclosure duty. SECONDARY.
- https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465 (renderer API) — 16 CFR 465.2(b): unlawful to disseminate a consumer testimonial that misrepresents "That the reviewer or testimonialist exists" or "used or otherwise had experience with the product". Civil penalties per FTC press release (SEARCH-SNIPPET) up to US$51.744 per violation.
- https://dadosabertos.camara.leg.br/api/v2/proposicoes/2487262 — PL 2338/2023 (AI framework) status 2 Sep 2026: "Aguardando Parecer", regime de prioridade, bills still being attached. No Brazilian digital-replica statute in force.
- https://satedsp.org.br/wp-content/uploads/2025/12/CCT-SATED-SP-E-SIAESP-2026-2027.pdf — signed 24 Nov 2025; grep for "intelig", "sintét", "réplica", "avatar": 0 hits. No AI/digital-replica fee in the SP actors' CCT.

## Crowd consent prices (the floor)
- https://www.vintepila.com.br/servicos/publicidade/eu-vou-fazer-video-ugc-para-seu-produto-servico/ — observed gigs on the same page: "Comercial do seu Produto… R$ 40,00 · ★5,0 (167) · 390 vendidos"; "gravar seu vídeo… R$ 30,00 · ★5,0 (207) · 753 vendidos"; the listed UGC seller: video R$45, "Ads e Direito de imagem 3 meses R$ 30,00", 3 photos R$30. Observed buyer-side (sales counts).
- SEARCH-SNIPPET (influencerbrasil.com.br, airfluencers.com) — Brazilian UGC R$150–500 per video for beginners, +50–100% for paid-ads use. SECONDARY, seller-side advice.
- SEARCH-SNIPPET (diariodonordeste, ocorre.com, cybersecbrazil) — Brazilians paid for head-mounted chore videos for robot training, "R$ 30" per session reported, up to R$4 mil/month for heavy users. SECONDARY.
- https://www.opentrain.ai/jobs/language/pt/ — live posts: "Portuguese Audio Transcription Expert Hourly · $20–$36/hr" (19 Sep 2026); "Brazilian Portuguese Audio Transcript Editor … $10-$35 per hour"; 140 audio & speech roles. AI buyers hire Brazilians directly.
- SEARCH-SNIPPET (ziprecruiter, indeed, mediabistro) — PT-BR voice actors for AI training US$20–60/h, contractor basis. SECONDARY.

## Data-licensing money (buyer side)
- https://www.sec.gov/Archives/edgar/data/1549346/000154934626000008/sstk-20251231.htm — Shutterstock FY2025 10-K: "Data, Distribution, and Services" revenue US$203.264k (2025), 175.251k (2024), 137.323k (2023); "increased demand for access to our metadata for machine learning and generative artificial intelligence model training". PRIMARY, buyer-side aggregate.
- https://defined.ai/partnership-programs (redirect from /partnerships/data-partner) — data-partner programme: licensing "driven by marketplace demand", terms "aligned with and approved by the partner", data must be consented and commercialisable; vendor's own marketing figures "319% YoY growth in dataset sales · $600K+ Average partner revenue · $1M+ Revenue for 5+ partners"; also "Apply as an AI Service Supplier — project-based jobs". Vendor marketing, not a price.
- SEARCH-SNIPPET — "Only 30% of partners are approved for the marketplace" (Defined.ai). SECONDARY.
- https://unidata.pro/datasets/facial-skin-condition-image-dataset/ — the request form's budget options start at "$5,000 – $25,000" then $25–50k, $50–100k, $100k+. Vendor form, not a price.
- SEARCH-SNIPPET https://datarade.ai/search/products/face-datasets (403 on fetch) — "Nexdata face datasets start at $10,000 per purchase; Unidata … start at $30,000". SECONDARY/UNVERIFIED.
- SEARCH-SNIPPET https://arxiv.org/pdf/2608.30688 — "UFPR-PEs: A Brazilian Face Recognition Benchmark with Self-Declared Race/Color Labels" (academic, Aug 2026) — free Brazilian face data exists for benchmarking.
- https://www.troveo.ai/resources/sell-data-to-ai-companies — non-exclusive licences "can generate revenue from multiple buyers over time"; value from "uniqueness, history, and context".
- https://defined.ai/datasets — marketplace is JS-rendered; no prices in server HTML (nothing usable).

## Swatch / real-skin anchors
- https://www.squareshot.com/services (from /pricing) — US studio publishes "BEAUTY (Swatches)" as a service category; "Hand model image = 3 credits"; credits US$45–60 (Launch US$1.500/mo = 25 credits at US$60; Scale US$4.500/mo = 100 at US$45) ⇒ ≈US$135–180 per hand-model image; model shoot day US$5.950 incl. 1 model + "6 months usage rights". Seller asking, US.
- SEARCH-SNIPPET https://www.tiktok.com/@bocarosabeauty/video/7428700533755628805 — Boca Rosa Beauty posts a swatch of the "7 tons mais escuros" of Stick Pele made by influencer @estojodabeleza — brands get shade swatches from influencers (PR, unpaid or paid UNVERIFIED).
- SEARCH-SNIPPET https://www.refinery29.com/en-us/2018/08/207334/makeup-swatch-photoshop-dark-skin-controversy — brands accused of photoshopping foundation swatches on dark skin (why shade truth is contested).
- work/TA_CONSULTA_COSMETICOS.CSV (ANVISA daily file, downloaded by wave 1; notification date = DT_VENCIMENTO − 10 years; window 25 Sep 2025–24 Sep 2026, 116.207 rows): name-regex counts — lip (batom/gloss/lip tint) 3.374 notifications, 423 holders; base/corretivo/foundation 782, 150 holders; sombra/blush/iluminador/contorno 3.086, 376 holders; "ESMALTE" 385, 103 holders (many are removers/driers). Several top holders are importers of coded generic lines (e.g., "BATOM CREMOSO BN8517 | SOLLIS TRADING LTDA").

## Dead ends (recorded so nobody repeats them)
- https://www.conar.org.br/codigo/codigo.php 403; old PDF paths 404 — use conar.wpenginepowered.com PDF above.
- https://help.elevenlabs.io/… 403; shared-voices API filters (gender, age, locale, use_cases, category, search, accent) all 401 when not logged in; pagination (page=) 401.
- https://docs.stripe.com/connect/cross-border-payouts (via WebFetch) — self-serve cross-border payouts only between US/UK/EEA/CA/CH platforms; "Stripe doesn't support self-serve cross-border payouts to countries outside the listed regions." (ElevenLabs' list is longer — it evidently uses another arrangement — but still excludes Brazil.)
- https://jobformodel.com/job_examples — model-booking categories (e-commerce, campanha, "Direito de imagem de 1 ano", "Diária de 8h") but cachê values are JS-rendered; no number captured.
- Arcads/HeyGen/Creatify/Synthesia "become an actor" URLs guessed — all 404.
- https://datarade.ai 403; https://proxifai.me connection reset.
