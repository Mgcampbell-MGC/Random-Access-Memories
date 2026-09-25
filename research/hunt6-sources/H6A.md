# H6A — VBPH demand side: pool, launch cadence, trigger feed, current production mix
Agent H6A, Hunt 6, 25 Sep 2026. All fetches by curl from this session. Working files are in `hunt6/work/`.

## Source log (one line per URL: what it said)

### ANVISA: the trigger feed and the pool
- https://dados.anvisa.gov.br/dados/ : h5ai index of ANVISA open data. No "notified cosmetics" file at root. Petition-cycle files only (CICLO_ANALISE_PETICOES_COSMETICO.CSV, 41 MB).
- https://dados.anvisa.gov.br/dados/CONSULTAS/PRODUTOS/ : lists **TA_CONSULTA_COSMETICOS.CSV**, 227.527 KB, modified 2026-09-25 10:22.
- https://dados.anvisa.gov.br/dados/CONSULTAS/PRODUTOS/TA_CONSULTA_COSMETICOS.CSV : downloaded, HTTP 200, 227.527.719 bytes, latin-1, `;` separator, **1.201.421 rows**, **5.241 distinct holder CNPJs**.
  - Fields: NU_PROCESSO; NO_PRODUTO; NU_CNPJ_EMPRESA; NO_RAZAO_SOCIAL_EMPRESA; DT_VENCIMENTO; ST_SITUACAO_PRODUTO (S 1.007.036 / N 194.382); NU_REGISTRO; DS_TIPO_PETICAO (ISENTO DE REGISTRO 591.250 · Notificado 520.964 · DESCARTAVEL 5.043 · REGISTRO 2.278); ST_REGISTRADO; DT_ATUALIZACAO (all rows = 24/09/2026).
  - There is **no notification-date field and no category field.** For electronic notifications the date is DT_VENCIMENTO minus 10 years, to the second. Checked two ways: (1) against the year in NU_PROCESSO (25351.NNNNNN/**YYYY**-DV). For 2023–2026 processes the diagonal agrees on 58.868/59.268, 70.081/70.420, 99.848/100.549 and 81.148/81.148 rows. (2) Against RDC 907/2024 art. 41 §1 (below).
  - Newest record: 2026-09-23 23:51:42, in a file stamped 2026-09-25 10:22. **Publication lag is about 1,5 days.**
  - Daily volume in September 2026: 311–558 records per weekday, 8–33 per weekend day.
  - Hair/skin (keyword classifier on NO_PRODUTO; regexes in `work/classify.py`): 353.407 hair + 118.161 skin rows in total. **Last 12 months (24 Sep 2025 to 23 Sep 2026): 42.498 hair/skin records.** Of these, 41.037 are electronic "Notificado" records with a timestamp, about 3.400 a month. The other 1.461 (3,4%) are midnight-stamped legacy or renewal rows and must be excluded.
  - Re-notifications: **31,5%** (13.096 of 41.595) of the 12-month hair/skin rows repeat, token for token, the name of an earlier notification. They are manufacturer switches or re-filings, not launches. That figure is a lower bound.
- https://dados.anvisa.gov.br/dados/Documentacao_e_Dicionario_de_Dados_COSMETICOS.pdf : data dictionary (2020) for the *petition-cycle* dataset, not the product file. It confirms that updates are daily.
- https://dados.anvisa.gov.br/dados/CONSULTAS/EMPRESA_FISCALIZACAO_PRODUTO/TA_CONSULTA_FUNCIONAMENTO_EMPRESA_NACIONAL.CSV : AFE register, 313.620.860 bytes, 352.101 rows.
  - Cosmetic AFE ("Cosmético - 2"): 19.203 rows, **15.458 active, 15.451 distinct CNPJs**. **3.473 of them hold the "Fabricar" activity**, and 1.399 of those are in SP.
  - Fields include NO_FANTASIA, DS_HOMEPAGE and NU_SAC. Among the 584 fitting-band holders, a homepage is present for 106 (18%) and an SAC phone for 213 (36%).
- .../Documentacao_e_Dicionario_de_Dados_Certificado_AFE.pdf : AFE data dictionary (03/06/2025). Update frequency "diária".
- https://anvisalegis.datalegis.net/...numeroAto=00000752...valorAno=2022 : RDC 752/2022, "Revogada pela … RDC nº 907, de 19/09/2024".
- https://anvisalegis.datalegis.net/...numeroAto=00000907...valorAno=2024 : RDC 907/2024, "Vigente com Alterações".
  - Art. 3º II: "comunicação prévia: … informar à Anvisa a **intenção de comercialização** de um produto isento de registro por meio de notificação".
  - Art. 35: every group not listed in art. 34 is exempt from registration and "sujeitos ao procedimento de comunicação prévia".
  - Art. 37: titulares and/or fabricantes need AFE.
  - Art. 41 §1: maintenance is tied to a declaration "a cada 10 (dez) anos, contados a partir do dia da notificação". This is why DT_VENCIMENTO = notification + 10 years.
- https://consultas.anvisa.gov.br/api/consulta/... : HTTP 403. The per-product consult API is not usable from here. The open-data CSV is the rail.

### Pool: counts derived from the file (scripts in work/)
- Holders with at least one active hair/skin product: **3.803**. Holders that notified at least one new hair/skin product in 12 months: **1.616**.
- Holder bands by active hair/skin count: 1–4: 837 · 5–9: 466 · 10–29: 737 · 30–99: 825 · 100–299: 604 · 300–999: 297 · ≥1000: 37.
- Band 10–100 active **and** ≥2 new in 12 months: **584** CNPJs. 468 of them hold "Fabricar" AFE.
- Manual read of 30 random holders from that band (seed 7; 7 product names each). 7 are clear own-brand fits: Korban, Vitamédica, Madame Lis, Grazie, Caulí, Beautyderm, Aramath. 8 are partial (low-end mass or a small multi-brand owner). 4 are importers of foreign brands (Wabi, Sarol, EAP, ICD). 9 are contract manufacturers (terceiristas). 1 is a multinational (Weleda). 1 is misclassified (deodorant).
- Brand mining: a within-holder frequency vote over trailing and leading n-grams of NO_PRODUTO (`work/brandmine.py`).
  - 40-row precision check: ~35 of 40 keys are real brands, so **~85% precision**.
  - Brand keys with ≥4 / ≥6 / ≥10 new hair/skin notifications in 12 months: 2.886 / 1.667 / 796.
  - Of the ≥6 group, **1.209 (73%) are held by multi-brand holders** (≥10 brand keys, i.e. contract manufacturers). Only 205 are held by 1–3-brand holders.
- Contract-manufacturer concentration: **58 multi-brand holders with ≥100 new hair/skin notifications a year account for 30,1% of all 12-month hair/skin notifications**, and 185 holders with ≥50 account for 52,0%.
  - Largest: "+ BRIEFING AGENCIA DE PUBLICIDADE E REPRESENTACOES LTDA" (1.072 new, ~998 brand keys), Veneza (1.016), Império (614), SDK (485), TCI (447), Alfahair (390), HF (321).
- Own-notifying launchers (10–600 band, ≥6 new in 12 months, top brand key ≥50% of products): **262** CNPJs.

### publica.cnpj.ws (porte, capital, email, phone)
- 20 random fitting-band holders: https://publica.cnpj.ws/cnpj/{36345458000120, 11313496000170, 33759082000101, 07966295000102, 27799585000108, 10481819000171, 49526381000136, 10307523000139, 51490625000110, 25958628000125, 80851249000140, 20906653000141, 35758651000120, 29223262000105, 22087904000139, 57460618000151, 25086167000148, 32978628000152, 40941948000166, 12579559000105}.
  - Porte: ME 13, EPP 5, Demais 2.
  - Email present on 16/20. Only **12/20 reach the business itself**. 4 are accountants' addresses: escritoriomaster@gmail, cadastro@angolacontabilidade, contato@consultecauditoria, falecom@sernocontec.
  - Phone present on **19/20**.
  - Clear fits looked up: Korban EPP (capital R$100k) · Vitamédica ME (R$10k) · Madame Lis EPP (R$20k) · Grazie ME (R$10k) · Caulí/Natre ME (R$1,5k) · Beautyderm/RJR ME (R$10k).
- Established-brand holders:
  - 04696774000150 Kush (Truss) Demais
  - 03994975000170 Gram (Haskell) Demais, capital R$5M, contato@haskellcosmeticos.com.br
  - 05787174000160 Lobato (Lowell) EPP
  - 08040489000137 Bem Estar (Amend) Demais
  - 13366641000106 Nova Cedral (Inoar) Demais
  - 00152968000133 Suelym (Widi Care) "ME" with capital R$20,6M, so **the porte field is stale or self-declared**
  - 06025461000103 Condor (Nupill) EPP
  - 82914334000135 Dahuer (Hidrabene) Demais
  - 39299870000149 AVLFM (Adcos) Demais, capital R$17M
  - 40367856000114 CCD (Dermage) Demais
- 38 random own-notifying launchers (`work/cnpj_own40.txt`, results in `work/own40_result.json`).
  - Porte: **Demais 14 · EPP 10 · ME 14.**
  - 6 are multinationals, importers or group subsidiaries: Elizabeth Arden/Revlon, Galderma, Grupo Boticário's Vegan do Brasil (g_cscsocietario@grupoboticario.com.br), Quattror, TRL, Olita.
  - **Domestic EPP+Demais: 18/38 (47%).**
  - Email on 37/38, of which ~32 reach the business (the rest are accountants' addresses). Phone on 37/38, of which 2 are the placeholder 1199999999.

### Trade fair, association and CNAE rails
- https://beautyfair.com.br/expositores/ → CMS API https://cms.beautyfair.com.br/beautyfair/wp-json/custom/v1/node?path=expositores&paged={1..33} : **491 exhibitors (2026)**, each with tags and a link.
  - 236 are tagged Cabelos/Barber/Skincare/Proteção Solar. **226 of those 236 (96%) link an Instagram (129) or a website (97).**
  - Matched by name to ANVISA: 129 have hair/skin records, 113 had ≥1 new notification in 12 months and **80 had ≥6**. Median among the 113 is 12 new notifications a year.
  - The next edition is at Expo Center Norte, 4–7 Sep 2027 (ctaEvent field).
- https://www.hairbrasil.com.br/ redirects to hairbrasilshop.com.br. /expositores returns 404, and feirahairbrasil.com.br gives a 502 at the proxy. **Hair Brasil 2026 exhibitor list: NOT OBTAINED.**
- https://abihpec.org.br/empresas-associadas/?letra={#,A..Z} : **263 member companies**, including suppliers, multinationals and non-cosmetics firms (3M, Ajinomoto). 159 fuzzy-match an ANVISA hair/skin holder, and **100 of those have ≥6 new hair/skin notifications in 12 months**. The match is fuzzy and unaudited.
- CNAE 2063-1/00 and 4646-0/01 counts by porte: the Receita bulk file hosts (arquivos.receitafederal.gov.br, dadosabertos.rfb.gov.br) returned an empty reply or a connection reset. **NOT OBTAINED.** The ANVISA AFE counts above are used instead.
- https://www.packforyou.com.br/ and /servicos/ : a contract manufacturer (holder of 1.999 active hair/skin products). It sells "Full Service": "Criação da Marca · Desenvolvimento da Identidade Visual · Criação do Rótulo · **Publicidade** · Registros de produtos". Contract manufacturers already bundle creative for their private-label clients.

### Lead time to market (notification → first published on the brand's own store)
- https://sallve.com.br/products.json?limit=250 (Shopify, 205 products, created_at/published_at):
  - Máscara Renovadora Labial: notified 2026-03-10, published 2026-08-05, **148 d**.
  - Firmador Pró-Colágeno: notified 2026-01-07, published 2026-04-06, **89 d**.
  - Bastão Vitamina C: notified 2025-08-21, published 2026-01-09, **141 d**.
  - Sérum Antiolheiras: notified 2025-04-29, published 2025-08-05, **98 d**.
  - Also 8 or more Sallve notifications in 2025–26 are **re-notifications of products already on sale since 2022–24** (Limpador Enzimático, Hidratante Antiatrito, Bastão Antioleosidade, Protetor Toque Seco…). Sallve moved between four contract manufacturers: Cosmo, K&G, Weckerle and Lipson.
- https://www.dermage.com.br/api/catalog_system/pub/products/search?O=OrderByReleaseDateDESC (VTEX releaseDate):
  - Photoage Water Gold: notified 04-13, released 08-14 (**123 d**).
  - Hidracare loção/creme: 04-06 → 07-02 (**87 d**).
  - Clarité Mela Repair: 02-04 → 06-26 (**142 d**).
  - Bruma Lavanda: 04-02 → 05-12 (**40 d**).
  - Sonata: 03-19 → 04-24 (**36 d**).
  - Secatriz Salic: 01-28 → 02-13 (**16 d**).
  - Senskin and Body Glow: 2025-10-02 → 11-17 (**46 d** each).
  - Photoage Water Sport: 2025-07-21 → 10-06 (**77 d**).
  - Improve C 30: 2025-06-05 → 08-25 (**81 d**).
  - Exocare Cell Repair: 2025-03-13 → 07-22 (**131 d**).
- https://hidrabene.com.br/products.json (Shopify, 79 products):
  - Sérum GHK-Cu and Sérum PDRN: notified 2026-07-17, created 07-30, published 08-12 (**26 d** each).
  - Harmonizador: notified 07-01 → published 08-12 (**42 d**).
- **18 pairs across 3 brands: median ≈ 79 days, range 16–148 days.**

### Launch cadence (ANVISA dates; `work/cadence.json`)
- n=34 brands, of which 24 are established and 10 are small band-fit brands.
- New hair/skin notifications in 12 months: median **21** (IQR 11–37).
- Distinct notification days: median **10,5**.
- "Launch windows" (clusters split at >21-day gaps): median **3**, distribution {0:1, 1:4, 2:6, 3:7, 4:6, 5:2, 6:5, 7:3}.
  - Established brands: median **4**. Examples: Truss 4, Haskell 7, Inoar 6, Braé 7, Principia 7, Sallve 6, Nupill 6, Adcos 6, Dermage 5.
  - Small band-fit brands: median **2**. Korban 2, Vitamédica 1, Madame Lis 2, Grazie 3, Caulí 0, Beautyderm 3, Aramath 1, Lanuty 4, Zantor 1, Atos 3.
  - Windows are an upper bound on campaigns because re-notifications inflate them. Sallve's 6 windows contain about 2 real new launches.

### Current production mix (15 launches, brand-owned pages; images viewed in contact sheets `work/img/sheet1-3.jpg`)
- https://www.inoar.com.br/beleza-arabe-e-alta-performance-inoar-apresenta-as-linhas-latifah-e-baccarah-blue : Baccarah Blue, bottles in a rendered Arabian-night desert scene with no human. **CGI or likely AI** (visual judgement only).
- https://www.inoar.com.br/korea-repair-o-ritual-coreano-que-transforma-o-cuidado-dos-cabelos : Korea Repair, a styled product-only photo on a bathroom counter.
- https://www.felps.com.br/mascara-redutora-quiabo-xbtx-antifrizz-felps-professional-300g : Quiabo XBTX, white packshot front and back. Image filenames are dated 2025-08-05, so the 2026-06 notification was a re-notification.
- https://www.nupill.com.br/creme-antirrugas-nupill-nano-hyaluronic : Firmness Intensive, packshot or render with carton on white.
- https://loja.qodcosmetics.com/qod-pro-more-volume-shampoo-300ml : More Volume, packshot plus a typographic instructions card.
- https://sallve.com.br/products/mascara-renovadora-labial : **studio shoot with human models** (lips, face, hand holding the product) plus packshot.
- https://sallve.com.br/products/firmador-pro-colageno : **studio shoot with human model** (face, hand) plus texture swatch.
- https://www.dermage.com.br/photoage-water-gold/p : packshot plus **hand model** in studio.
- https://www.dermage.com.br/clarite-mela-repair/p : packshot plus **hand model**.
- https://www.dermage.com.br/hidracare-locao-hidratante-corporal/p : packshot plus **leg/hand with swatch**.
- https://hidrabene.com.br/products/hidrabene-serum-facial-shot-pdrn (and GHK-Cu, Harmonizador) : liquid-splash and droplet product scenes plus an East-Asian model holding the tube on grey. **Looks AI-generated** (visual judgement, UNVERIFIED).
- https://www.amend.com.br/ banner `.26.Agosto/full_lancamentosv4.png` ("Chegaram os lançamentos") : product-only 3D render on pedestals.
- https://www.amend.com.br/ banner `.26.Junho/fullSCIENCE.png` : product-only render.
- https://www.principiaskin.com/ slide `slide_desktop_CO_01.webp` ("Lançamento: Creme para Área dos Olhos CO-01") : product-only CGI scene.
- https://www.principiaskin.com/ slide `slide_desktop_protetor_solar_cores.webp` ("Lançamento: Protetor solar com cor PS-05, 7 cores") : product-only studio photo plus swatch.
- **Tally, 15 launches:**
  - Studio with human model: **5** (2 full-face, 3 hand/body-part only).
  - Product-only studio or 3D render: **8**.
  - Likely AI-generated: **2**.
  - UGC/influencer: **0 observed**, because Instagram was not readable.
  - Low-budget phone: **0**.

### Rails that failed
- https://www.instagram.com/api/v1/users/web_profile_info/?username=sallve : 401 "require_login". Instagram launch posts and Instagram contactability could not be measured.
- VTEX catalog API for Inoar, Nupill, Felps, Phállebeauty and QOD redirects to /sem-resultados-na-busca (these are Tray stores). Truss (trussprofessional.com.br) and Adcos return 403 (Akamai). Haskell and Lowell are SPAs with no images in the HTML.
- Domain-existence test for mined brands (brand.com.br) was discarded because generic tokens (gold, flor, web) resolve to unrelated domains. Too noisy to use.
