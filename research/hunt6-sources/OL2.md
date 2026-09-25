# OL2 — Is R$2.990 (and R$490 / R$690 / R$6.900) a price an established Brazilian indie hair/skin brand actually pays?

**Verdict: PARTLY CLOSED.**

- **The seller side now supports R$2.990.**
  - A verifiable traditional São Paulo launch shoot costs **R$6.878–13.255** with a model and a product film.
  - Stills with a model cost **≈R$3.378**.
  - R$2.990 is **23–43% of the with-film bill** and equals the minimum of the one AI studio that sells campaign days (Make Move, R$3.000).
- **The buyer side still has not been observed at that price.**
  - Every buyer-set number found today is small:
    - UGC video: R$100–250 (Creatify) and from R$169 (Noovid);
    - freelance boards: <US$500 (VER1).
  - The best buyer-side support is indirect. Small brands that do shoot pay R$1.200–2.500 for the **model alone**.
- Price and restructure as below, then let the 20 calls decide (bars at the end).

All fetches were made 25 Sep 2026 with curl (browser user agent, the proxy CA bundle). Raw captures are in
`work/OL2/`. USD uses PTAX 5,1795, as in `O_LANCAMENTO.md`.

---

## 1. São Paulo still / packshot photography: what is published

**Finding: premium São Paulo still studios do not publish prices.** Ten were checked (six fetched, four unreachable):

- **Did not publish:**
  - Estúdio Tasso;
  - Fotografia Still;
  - IWD (`fotografiaproduto.com.br`);
  - FotoCommerce;
  - Picx Filmes;
  - Fifitong.
- **Unreachable:** Studio Petrangelo (502), Estúdio Zarez (502), Bianca Machado (TLS error) and Frame In Focus (404).

This is the legibility–margin law again: the tier that would anchor R$2.990 quotes privately.

The two statements closest to a number:

- **Fotografia Still (SP, "desde 2009"):** *"Fatura de serviços still até R$ 1k à vista na entrega do serviço. Para valores superiores o serviço pode ser parcelado em até 3 vezes"*
  - https://www.fotografiastill.com.br/serv
  - The payment terms put a typical still job at around R$1.000.
- **IWD:** *"cobramos por foto finalizada"*, with no number.
  - https://fotografiaproduto.com.br/fotografia-still-preco/

**Sellers that DO publish a number** (11 in total; 6 in São Paulo state):

| # | Seller (location) | Published price | Exact quote | URL |
|---|---|---|---|---|
| 1 | Estúdio Fábrica (São Paulo, centro expandido) | Still on white R$25→18/image. Content-production period R$1.250 (up to 50 treated images or 5 edited videos, **no model, no make-up**). External shoot: half-day 40 images R$1.600, full day 80 images R$2.500. Studio hire R$530 / R$850 | *"01 a 49 imagens: R$ 25,00 por imagem… 100 imagens ou mais: R$ 18,00"*; *"Investimento: R$ 1.250,00 por período… Incluso tratamento de até 50 imagens por período ou 5 vídeos editados… Não inclui modelo e não inclui maquiagem."*; *"Meia diária – 40 imagens: R$ 1.600,00… Diária – 80 imagens: R$ 2.500,00"* | https://www.estudiofabrica.com.br/servicos-e-precos/ |
| 2 | fotografiadeprodutos.com.br (SP, (11) 95737-0613) | Small products: R$25 per unit (3 photos); tiers R$13 / 11 / 9 / 7 per photo (minimum 80–120 photos). Clothing R$70–150 per piece | *"VALORES PADRÃO R$ 25,00 por unidade… 03 FOTOGRAFIAS por unidade"*; *"R$ 7,00 POR FOTOGRAFIA QUANTIDADE MÍNIMA 120"* | http://www.fotografiadeprodutos.com.br/fotografia-de-produtos-tabela-de-preco.html |
| 3 | **Estúdio Magotte** (SP region, (11) 4118-4416; sells to artisanal cosmetic brands) | "Fotografia de produtos": **10 photos R$600 · 20 R$1.080 · 50 R$2.000**. Models and scenes, 10 working days, 3 adjustments. The product image filename is `freepik__coloque-a-img1-segurando-o-frasco…`, i.e. AI-made | Variants in page JSON: `"option0":"10 fotos"… "price_short":"R$1.080,00"… "option0":"20 fotos"`, `"R$2.000,00"… "50 fotos"`. Copy: *"Fotos Humanizadas… Fotos Ambientadas… o prazo de entrega do material é de até 10 dias úteis… até 3 ajustes sem custo"*. Its MOCKUP service states: *"Não garantimos emabalagens idênticas na criação dos mockups."* | https://www.estudiomagotte.com.br/produtos/ensaio-fotografico-digital-5hh4x/ ; https://www.estudiomagotte.com.br/produtos/mockup/ |
| 4 | Agência Wys (Sorocaba-SP) | 10 photos from R$300; 20 from R$500; R$20–80 per photo; R$80–150 with art direction | *"10 fotos: a partir de R$300"*, *"20 fotos: a partir de R$500"*, *"com direção de arte… R$80 a R$150 por foto"* (FAQ on the seller's own page) | https://agenciawys.com.br/fotografia-de-produto-preco/ |
| 5 | Armais Publicidade (Americana-SP; apparel) | 500-photo e-commerce pack from R$1.700 | *"Pacote fotográfico para e-commerce A partir de R$1.700,00"* | https://www.armaispublicidade.com/product-page/pacote-fotogr%C3%A1fico-para-e-commerce-500-fotos |
| 6 | Matheus Dacosta (photographer's own table; city UNVERIFIED) | Studio photo up to 8 h R$900 / 1.000 / 1.200, royalty-free | *"Foto estúdio Até 8h R$ 900,00 R$ 1000,00 R$ 1200,00"*; *"Todas as imagens são Royalty Free"* | https://matheusdacosta.art.br/tabela-de-precos-para-fotografia |
| 7 | Destaquei (Curitiba, bookable online) | Photographer from R$1.690; videomaker from R$2.890; overtime R$350/h | *"a partir de R$ 1.690"*, *"a partir de R$ 2.890"*, *"R$ 350/hora"* | https://destaquei.com.br/contratar-online/ |
| 8 | Estúdio Bala (Rua Fidalga 407, Vila Madalena, SP), studio hire | Studio I R$572 (4 h) / R$754 (8 h); Studio II R$800 / R$1.200; weekend up to R$1.450 | price list on page | https://estudiobala.com.br/locacao/ |
| 9 | Phoco Studio, studio hire | Day R$700; R$100/h, 3 h minimum | *"1 Diária: 08:00h as 17:00h – Valor R$ 700,00; b) Por hora, R$100,00 a hora ( Mínimo de 3 horas )"* | https://phocostudio.com.br/locacao-estudio/ |
| 10 | GetNinjas (platform editorial) | Product photos "a partir de R$10 a foto"; fashion R$900–1.000 | *"Fotografia de produtos (e-commerce): A partir de R$ 10 a foto"* | https://www.getninjas.com.br/eventos/fotografia/preco/fotografo-comercial |
| 11 | Cronoshare (aggregator, SECONDARY) | 8-hour day R$1.000–1.600 | *"uma diária completa de 8h por R$ 1.000 a R$ 1.600"* | https://www.cronoshare.com.br/quanto-custa/fotografia-produto |

**Reading.**

- A packshot is a **R$7–25** item.
- A styled or ambient image is **R$53–150**, whether AI (Fábrica, Magotte) or human art-directed (Wys).
- A studio **day** is **R$850–2.500**, before any model or make-up.

**VITRINE's 6 stills at R$490 (≈R$82 per image) sits inside the styled-image band:**

- 6 × R$53–60 AI = R$318–360;
- 6 × R$80–150 human = R$480–900.

---

## 2. Product video / launch film

| Seller | Published price | Exact quote | URL |
|---|---|---|---|
| Destaquei (Curitiba) | Product video from R$3.500. Package for 1–10 products R$8.000–25.000. Advertising film from ~R$10.000 | *"Vídeo de produto a partir de R$ 3.500"*; *"o investimento em vídeo de produto varia em média de R$8.000 a R$25.000 para um pacote de 1 a 10 produtos"*; *"Vídeos publicitários partem de cerca de R$ 10.000"* | https://destaquei.com.br/calculadora-de-orcamento/ ; https://destaquei.com.br/videos/video-produto/ |
| Matilde Filmes (city UNVERIFIED) | Product video from R$7 mil. Short social videos, one-off from R$4 mil | *"Vídeos de Produtos ➡️A vitrine do século XXI… 💰 Valor: a partir de R$ 7 mil"*; *"pacote de vídeos mensais a partir de R$ 6 mil / avulsos a partir de R$ 4 mil"* | https://www.matildefilmes.com.br/produtoras-de-videos-como-escolher-com-precos-e-exemplos/ |
| Lou Studios (guide on its own site) | "Produtora Básica" R$3.000–12.000 | *"Produtora Básica — R$ 3.000 a R$ 12.000 Indicada para vídeos simples de até 1 minuto"* | https://www.loustudios.com.br/post/quanto-custa-uma-produtora-de-v%C3%ADdeo-guia-de-pre%C3%A7os-2026-no-brasil |
| Estúdio Fábrica | Social/stop-motion video R$160 each (no model); AI video 15–20 s R$260 | *"Social Básico/Stop Motion: R$ 160,00 por vídeo"*; *"Produção de vídeo de até 15 a 20 seg: R$ 260,00"* | https://www.estudiofabrica.com.br/servicos-e-precos/ |
| Villo (AI) | Video R$50 per ≤10 s | *"R$ 50,00 Por apenas / por vídeo *Conteúdos de até 10 segundos"* (VER1 capture) | https://www.villo.ia.br/precos |

**Reading.** A produced product film starts at **R$3.500–7.000**. An AI or social clip costs **R$50–260**.
O LANÇAMENTO's 15 s film sits between the two. Its value rests on the label staying exact, not on production scale.

---

## 3. What a model / lifestyle image replaces: model, make-up, studio

| Component | Price | Exact quote | URL | Status |
|---|---|---|---|---|
| Model day, small accessories brand, SP (posted by the brand's photographer) | **R$1.500 per day**, 2 years of image rights (R$1.200 in RJ) | *"Bruto: R$ 1.500,00 por diária… Photoshoot para marca de acessórios masculino, bijuterias. Fotos e vídeos curtos serão publicados na rede social da marca e site… 2 anos de direito de imagem"* | https://jobformodel.com/public_jobs/29961f9f-b9b2-4988-a8d8-88e50fb1fae2 | verified (live listing) |
| Model day, Ferrero Rocher campaign, SP | **R$2.500 per day**, 2 years | *"Fotos para a campanha de Final de Ano Ferrero Rocher… R$ 2.500,00 por diária… 2 anos de direito de imagem"* | https://jobformodel.com/public_jobs | verified |
| Actor floors, SP audiovisual **and advertising**, 2026/27 (SATED-SP × SIAESP CCT, signed, in force 1 Jan 2026) | Internet video: protagonist **R$600/day**, supporting R$300. TV/streaming protagonist **R$1.438,14** | *"PRODUÇÃO DE CONTEÚDO AUDIOVISUAL e PUBLICITÁRIA"*; *"VÍDEOS/INTERNET PROTAGONISTA R$ 600,00"*; *"TELEVISÃO/STREAMING… PROTAGONISTA R$ 1.438,14"* | https://satedsp.org.br/wp-content/uploads/2025/12/CCT-SATED-SP-E-SIAESP-2026-2027.pdf | verified. Floors, not market rates. The draft AI clause in the 2024 pauta is **not** in the signed text |
| Make-up artist / hairdresser day (SINDCINE minimums 2022/23, reproduced by a trade site) | **R$627,52/day each** | *"CABELEIREIRO DIÁRIA 627,52 · MAQUIADOR DIÁRIA 627,52"* | https://filmmakers.pro.br/tabela-22-23-de-precos-minimos-de-prestacao-de-servicos-para-filmes-publicitarios/ | SECONDARY and stale. The current table is not on sindcine.com.br. SINDCINE's own notice says CADE found *"ausência de mecanismos de coerção para impor as tabelas"* (https://www.sindcine.com.br/Pagina/10/Tabelas) |
| Director of photography (same table) | R$2.509,98/day | *"DIRETOR DE FOTOGRAFIA DIÁRIA 2509,98"* | same | SECONDARY, stale |
| Studio hire | R$530–1.450 | see §1, rows 1, 8, 9 | — | verified |

### The minimal traditional launch bill in São Paulo

Built only from the published numbers above.

| | Low | High |
|---|---|---|
| Studio + photographer + treated images | R$1.250 (Fábrica, one 4 h period) | R$2.500 (Fábrica, full day, 80 images) |
| Model (brand-side posted) | R$1.500 | R$2.500 |
| Make-up (+ hair) | R$627,52 | R$1.255,04 |
| **Stills-with-model subtotal** | **R$3.377,52** | **R$6.255,04** |
| Product film | R$3.500 (Destaquei) | R$7.000 (Matilde) |
| **Launch with film** | **R$6.877,52** | **R$13.255,04** |

**R$2.990 = 43,5% of the low with-film bill, 22,6% of the high one, and 88,5% of stills-with-model alone.**

---

## 4. Buyer-side money

Everything found today, plus the record:

| What | Amount | Exact quote | URL | Status |
|---|---|---|---|---|
| Freelance-board beauty visual briefs | all <US$500 per project (<R$2.590) | see VER1 | `O_LANCAMENTO.md` Part B / `research/hunt6-sources/VER1.md` | verified by VER1 |
| Brands set their own UGC budget (Creatify marketplace) | **R$100–250 per video** | *"você define seu próprio orçamento para cada projeto, com preços geralmente variando entre R$100 e R$250 por vídeo"* | https://creatify.com.br/ | platform statement about buyer budgets |
| UGC for beauty brands (Noovid) | **from R$169/video**; "+5.000 marcas" | *"Vídeos UGC produzidos por criadores reais, a partir de R$169. Sem agência, sem contrato, sem mensalidade"*; *"Marcas +5.000 marcas usando a Noovid"* | https://noovid.com/pt-br/marcas/ugc-para-marcas-de-beleza | verified (seller page; brand count is the seller's claim) |
| Small brand's shoot: model alone | R$1.500 (SP) / R$1.200 (RJ) per day | §3 row 1 | jobformodel | verified |
| Hair brand, Beauty Fair show-room models | R$200/day | *"URGENTE - Beauty Fair… Bruto: R$ 200,00 por diária"* | https://jobformodel.com/public_jobs/7fa81cd8-0aa1-424a-b1b6-33c2a29f4ca8 | verified. Old listing (date pattern fits 2021); not launch visuals |
| Funded digital-native scale (not the ICP) | Creamy: R$1 bi cumulative revenue | Headline: *"Como irmãos de 23 e 28 anos e um dermatologista criaram marca de skincare que já faturou R$ 1 bilhão"* (Exame, 25 Aug 2025) | https://exame.com/negocios/como-irmaos-de-23-e-28-anos-e-um-dermatologista-criaram-marca-de-skincare-que-ja-faturou-r-1-bilhao/ | press-reported |

**Not found:** any Brazilian beauty brand publicly stating what a launch's visuals cost, or a brief or RFP with a budget ≥R$2.500. Trade-press searches returned only celebrity budgets, e.g. Boca Rosa's R$1,2 M campaign (Exame). That is not the ICP. **UNVERIFIED stays UNVERIFIED.**

**Note on the gap:**

- R$2.990 = US$577. The top freelance-board bucket is US$250–500.
- So the list price is **1,15× the ceiling of the best observed brief, not 8×**.
- It is 8–11× Orne's full set (≈R$280–360, VER1).

---

## 5. Sizing the buyer: 13 indie hair/skin brands measured

**Method:**

- Prices were read from each store's own catalogue API: Shopify `products.json` (full catalogue) and VTEX `api/catalog_system/pub/products/search` (first 50–150).
- "Singles" excludes kit/duo/trio/rotina titles.
- ANVISA counts are notifications in the last 12 months from `TA_CONSULTA_COSMETICOS.CSV`:
  - notification date = DT_VENCIMENTO − 10 y;
  - brand matched by name in `NO_PRODUTO`;
  - they include re-filings (≥20,8–31,5%), so they are not launches.
- Porte and capital come from `publica.cnpj.ws/cnpj/{cnpj}`.
- **Revenue is UNVERIFIED** throughout. Porte only bounds it: EPP ≤ R$4,8 M/yr; "Demais" = not ME/EPP.

| Brand | Store | Products online | Median single-SKU price | Median images per product | Porte · capital (CNPJ) | ANVISA notif. 12 m |
|---|---|---|---|---|---|---|
| Sallve | Shopify | 205 | R$59,90 | 7 | Demais · R$133,6 M (32.124.385/0001-95, SP) | 15 |
| Simple Organic | Shopify | 141 | R$64,00 | 3 | Demais S.A. · R$43,7 M (24.692.452/0001-40, Florianópolis) | 0 (name match) |
| Creamy | VTEX | 50 sampled | R$99,99 (all) | n/a | UNVERIFIED; press R$1 bi cumulative | 60 |
| Principia | own | 10 pages sampled | serums R$59–69 | n/a | Demais · R$68,8 M (39.710.427/0011-90) | 38 |
| Hidrabene | Shopify | 79 | R$49,90 | 5 | UNVERIFIED | 67 |
| Kokeshi | Shopify | 143 | R$39,90 | 4 | UNVERIFIED | 20 |
| Rosa Selvagem | Shopify | 346 | R$49,90 | **1** | EPP · R$10 k (operator Dermaweb 65.722.831/0001-12, opened Mar 2026) | 27 |
| Nouê | Shopify | 212 | R$147,00 | 7 | Demais · R$100 k (57.791.110/0002-17, Guarulhos) | 36 |
| Dermare | Shopify | 114 | R$39,99 | **1** | EPP, Simples · R$10 k (58.229.554/0001-45, Jales-SP) | 4 |
| Feito Brasil | Shopify | 101 | R$179,00 | 5 | UNVERIFIED | 28 |
| Apse | Shopify | 448 (349 kits) | R$49,90 | 4 | Demais · R$50 k (48.290.289/0001-57, Serra-ES) | 1 (name match) |
| Bioextratus | VTEX | 150 sampled | R$51,90 (all) | n/a | UNVERIFIED | 1 (name match) |
| Negra Rosa | VTEX | 50 sampled | R$23,37 (all) | n/a | UNVERIFIED | 4 |

Also counted from ANVISA only (prices not parsed on their platforms):

- Amend 90;
- Aneethun 63;
- Widi Care 53;
- Lowell 34;
- Lola from Rio 34;
- Felps 31.

**What this says about R$2.990:**

- **The median single-SKU price of the 9 Shopify brands is R$49,90.**
  - R$2.990 is the retail revenue of ~60 units.
  - At an assumed 50% gross margin (**UNVERIFIED**), it is the margin on ~120 units.
  - A contract manufacturer's page puts test batches at *"lotes de 500 a 2.000 unidades"* (https://www.packforyou.com.br/blog/quanto-custa-criar-uma-marca-de-cosmeticos/, a vendor statement).
  - So the visuals are paid back by roughly 6–24% of one first batch. That is plausible for an EPP-or-larger brand. For an ME (≤R$360 k/yr), 4 launches a year at R$2.990 is ≥3,3% of revenue: heavy.
- **Brands launch LINES and KITS, not single products.**
  - ANVISA notifications run 15–90 a year for active indie brands.
  - Kits are 12–78% of catalogues (Apse 349/448, Rosa Selvagem 210/346, Kokeshi 60/143).
  - **Pricing R$2.990 per SKU would bill an active brand R$45–270 k a year. They will not buy that way.** The unit must be the launch moment.
- **Visual under-supply is measurable for free.** Dermare and Rosa Selvagem show a median of **1 image per product**. Sallve and Nouê show 7. That is a VITRINE prospect signal read from `products.json`.
- **The top of the sample is not the ICP.** Sallve, Creamy, Principia and Simple Organic have R$43–134 M of capital and agency budgets. The ICP is the EPP-to-low-"Demais" tier (Nouê, Apse, Kokeshi, Hidrabene, Feito Brasil, Dermare, Rosa Selvagem).

---

## 6. Repair: the price ladder

| Tier | Now | Recommendation | Why (anchors) |
|---|---|---|---|
| PRÉVIA | free | keep | Villo also gives a free test image; it is table stakes |
| **VITRINE** | R$490 | **keep; make it the first paid step, credited in full against O LANÇAMENTO within 30 days** | 6 × R$53–60 AI (Fábrica / Magotte) = R$318–360 **with no packaging guarantee**; 6 × R$80–150 human art-directed (Wys) = R$480–900. R$490 is inside the band, and it is the tier closest to observed buyer money |
| **O LANÇAMENTO** | R$2.990 | **keep as list price for the test; redefine the unit as ONE LAUNCH (hero SKU + up to 2 supporting SKUs shown in the world) and add 1 kit composite** | 43,5% of the minimal traditional launch-with-film bill (R$6.878); equal to Make Move's AI minimum (R$3.000, stills only); 1,15× the top freelance bucket. Kit composites are priced by Fábrica at R$53–80 per kit, and fidelity-by-construction composites real packshots natively |
| **A LINHA** | R$6.900 (3 SKUs) | **lower to R$4.900 for up to 3 SKUs** (or keep R$6.900 but for up to 6 SKUs) | Traditional cost is per DAY, not per SKU: Fábrica prices periods; Destaquei prices *"1 a 10 produtos"* together. R$6.900 is also inconsistent with her own ladder: LANÇAMENTO + 2 × EXTENSÃO = R$4.370 |
| EXTENSÃO | R$690 | keep (stills + commerce set; film cutdown +R$490 optional) | Fábrica extra images R$35 each, AI images R$53. R$690 for a label-checked 6-image set is defensible |
| TEMPORADA | R$9.900 (4 prepaid) | keep, offered only to repeat buyers | R$2.475 per launch; brands file 15–90 notifications a year, so 4 launches a year is realistic for the ICP |
| **Fallback, only if the test fails its bar** | — | **LANÇAMENTO ESSENCIAL R$1.490** (key visual + 6 images + commerce set, no film) + **FILME add-on R$990** | Sits over Magotte (R$1.080 for 20 AI photos) and Fábrica AI sets (≈R$1.030–1.150), with the guarantee as the wedge |
| **Gate by porte** | — | Offer LANÇAMENTO / LINHA to EPP and "Demais" CNPJs; offer ME brands VITRINE only | Porte is a free CNPJ field; affordability arithmetic in §5 |

Monthly arithmetic against the R$12.200–15.800 gross bar:

- O LANÇAMENTO only: 4,1–5,3 a month.
- 1 LANÇAMENTO + 1 LINHA (R$4.900) + 6 VITRINE + 4 EXTENSÃO: **R$13.590**.
- The current table's 2 LANÇAMENTO + 6 VITRINE + 4 EXTENSÃO: **R$11.680, below the bar**.
- Fallback (ESSENCIAL with a 40% film attach, average R$1.886): 6,5–8,4 a month.
- VITRINE alone: 25–32 a month. That is origination-forever and not a business at the bar.

---

## 7. The anchor sentences for calls (Portuguese, every figure sourced above)

**For a brand that has shot traditionally:**

> "Pra lançar com imagem de campanha do jeito tradicional em São Paulo, meio período de estúdio com as fotos
> tratadas sai R$1.250 — sem modelo e sem maquiagem —, a modelo sai R$1.500 a diária e um vídeo de produto começa
> em R$3.500. Passa de R$6 mil. O LANÇAMENTO entrega key visual, 6 imagens de campanha, filme de 15 segundos com 2
> cortes e 3 peças de e-commerce por R$2.990, em 5 a 7 dias úteis — e cada letra do rótulo sai idêntica à arte
> aprovada, ou refazemos sem custo."

*(R$1.250 = Fábrica, one period, no model/make-up. R$1.500 = jobformodel, a small brand's model day with 2 years of rights. R$3.500 = Destaquei's product-video floor. Sum R$6.250.)*

**For a brand that already uses AI, freelancers or UGC:**

> "Imagem de IA sai uns R$53 a R$60 a peça, mas ninguém garante o rótulo — os termos da Villo dizem que 'pequenas
> variações visuais, textuais ou compositivas podem ocorrer'. A VITRINE são 6 imagens com o rótulo conferido letra por
> letra e um relatório de fidelidade, por R$490, em 48 horas — e o valor abate integralmente do LANÇAMENTO se vocês
> fecharem em 30 dias."

**Do not** cite Fábrica's *"não garantindo fidelidade"* clause as a packaging disclaimer. It is about complementary garments in apparel lookbooks (AUD3 correction).

---

## 8. Bar for the call test (commit before the first call)

- **Sample:** 20 brands pre-qualified on:
  - porte EPP or "Demais" (CNPJ);
  - an own store;
  - ≥10 ANVISA notifications in 12 months;
  - median single-SKU price ≥R$40.
- **Question 1 (ask before any price is said):** *"Quanto vocês gastaram por fora nas imagens e no vídeo do último lançamento — fotógrafo, estúdio, modelo, freela, IA, UGC?"*
- **Log per call:** porte, the number stated, what they used, and launches a year.
- **KEEP R$2.990** if ≥6/20 state ≥R$2.500 **and**, within 30 days, either ≥2 buy O LANÇAMENTO or ≥4 buy VITRINE (with the credit).
- **DOWNSHIFT** to ESSENCIAL R$1.490 + FILME R$990 if fewer than 6/20 state ≥R$2.500 but ≥8/20 state ≥R$1.000. **Do not discount R$2.990 on the call; switch the product.**
- **STOP and re-plan** if ≥12/20 state <R$1.000. VITRINE alone needs 25–32 sales a month.

---

## 9. Residual risks

1. **No buyer was observed paying ≥R$2.500 per launch.** The hole is closed on the seller side only; the calls are the only instrument left.
2. **The traditional anchor only works on brands that shoot traditionally.** Many indie brands use phone, Canva, UGC (R$100–250) or an in-house designer. For them the relevant anchor is AI at R$53–60 an image, and R$2.990 looks expensive.
3. **The anchor inputs are partly apparel and partly stale.**
   - Fábrica is a fashion studio.
   - The make-up floor is SINDCINE 2022/23, reproduced by a third party, and CADE has said such tables cannot be imposed.
   - The cosmetics-specialist still studios that would anchor the premium end do not publish prices.
4. **The AI done-for-you tier is already in São Paulo** (Magotte R$1.080 for 20 images; Fábrica R$53 an image; Make Move R$3.000) and will get cheaper. The guarantee, the film and the claim lock are the only wedge.
5. **Revenue for the ICP is UNVERIFIED.** Porte bounds it. Two ICP brands (Dermare, Rosa Selvagem's operator) are EPPs with R$10 k of capital, opened in 2024 and 2026.
