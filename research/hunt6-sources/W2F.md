# W2F — source log. Lens: what a launching Brazilian cosmetic brand needs in the ~79 days between ANVISA notification and shelf (Hunt 6, wave 2, 25 Sep 2026)

Fetched 25 Sep 2026 with curl (browser user agent) unless marked. Working files are in `hunt6/work/w2f/` (raw pages, `calc.py`, `calc_out.txt`, `confere_parsed.json`, `cr_ads/`). The ANVISA and AFE files are H6A's copies in `hunt6/work/`; nothing was downloaded twice.

**Answer in one line.** The one launch need that is not bundled by the factory, not sold self-serve by the tool vendor, and paid for today at a published price is **SELL-IN**: getting the product onto shelves. Brands say so in their own postings: they pay **10–15% commission on invoiced sales** to representatives. Every other need in the lens died.

## A. The launch need the factories leave to the brand (re-read of AUD2's saved pages, `work/aud2/pages/`)
- https://amoscosmeticos.com.br/terceirizacao-de-cosmeticos-marca-propria/ : "A fábrica terceirista cuida da parte técnica e produtiva. A marca contratante foca em posicionamento, **vendas, distribuição**, comunicação e relacionamento com o cliente."
- https://www.mzcosmeticos.com.br/informacoes/terceirizacao-de-cosmeticos : "mantendo o foco do contratante em branding, **distribuição** e relacionamento com o mercado."
- https://behub.com.br/terceirizacao-cosmeticos (AUD2) : "O contratante foca exclusivamente em marca, marketing e **vendas**."
- https://www.florus.com.br/ (AUD2 copy) : lists "Formação do Canal de Vendas" and partner "Traders" among its services. This is advice and referral; it does not take orders.
- https://stoaindustria.com/ (AUD2 copy) : "assessoria comercial, criação de marca…"; its services page reads "Assessoria Comercial e Tributária". Advice only.
- https://frosinicosmeticos.com.br/ (AUD2 copy) : "Consultoria comercial — Nosso time comercial está disponível para aconselhar e direcionar você". Advice only.
- ⇒ Of the factories read, **none takes orders or places product with a store or distributor.** Three sell commercial advice. Veneza-made (Alther) and SDK-made (Glam Professional) brands are recruiting their own reps and distributors (section D).

## B. The paid incumbent for outsourced sell-in
- https://behub.com.br/market-sales : "Market Sales — Terceirização de Área Comercial B2B". **"R$ 4.900 /mês fixo + 28% royalties sobre vendas"** for "2 vendedores dedicados", up to 30 leads a day. Its own in-house comparison assumes "Comissão de 5% sobre vendas (prática de mercado B2B)". Its table puts the cost at 52,5% of sales at R$20k/month of sales and 32,9% at R$100k. **Seller asking price.**
- https://behub.com.br/salao-parceiro : a salon own-brand programme (R$1.497; kit R$149,90). Not relevant to sell-in.
- https://behub.com.br/distribuicao : distribution of raw materials and packaging to brands, not sell-in.

## C. Commission rates. THE MARGIN LAW tested on cosmetics (brands' own postings = payer-published prices)
- https://www.confere.org.br/oportunidades.php : Conselho Federal dos Representantes Comerciais opportunity board, 170 live postings, parsed in `confere_parsed.json`.
  - **Êxodo Cosmética Avançada (Hactoon professional haircare), 16/09/2026:** "Comissão Progressiva e Atrativa: **Ganho base de 10% a 15%** + Bônus". It also states "Meta Média Estimada por Região no 1º Semestre: **R$ 15.000,00 a R$ 25.000,00/mês** · 2º Semestre: **R$ 25.000 a R$ 50.000/mês**". Requirements: "Registro ativo no CORE. Carteira de clientes ativa e consolidada… Estrutura de transporte própria".
  - Kosmetiquë Distribuidora (MG): "100% comissionada"; targets perfumarias, lojas de cosméticos and farmácias; "Plataforma B2B para realização e acompanhamento dos pedidos".
  - Trevo Distribuidora (Pink21 and 4Angels): "Comissão sobre vendas"; targets cosmetics shops, perfumarias, variety stores, distributors and wholesalers.
  - Kapeh: "introdução de produtos no mercado… Comissão atrativa".
  - Alther Health & Beauty: "Carteira ativa… CORE ativo… CNH".
  - Lokram: "visitas PDV 3–4x na semana".
  - Fleur Noire: "Comissionamento atrativo".
  - Cross-sector rates in the same board:
    - Goods: food 1–7%; auto parts 2,5%; hardware 3%; electrical 3%; furniture 3,25–4,5%; hospital 5%.
    - Software and services: 15–40%.
    - Cosmetics: **10–15%.**
  - Also on the board: Novare RH (auto parts) pays "**R$ 3.000,00 nos primeiros 3 meses + comissão de 2,5%**". This is a fixed launch fee paid to a rep, published by the payer, outside cosmetics.
- https://centraldosrepresentantes.com.br/ad_cat/cosmeticos/ (pages 1–5; 31 ads fetched in `cr_ads/`):
  - …/ad_listing/kah-noa-cosmeticos-busca-representantes-e-distribuidores/ : "**10% do valor líquido vendido** + bônus por meta batida – Auxílio combustível".
  - …/ad_listing/kb-distribuidora-karseell-busca-representante-comercial/ : "**Comissão de 10%** + bonificação"; requires a "Carteira ativa de clientes".
  - …/ad_listing/representante-comercial-autonomo-cosmeticos/ : "**Comissão: 10% sobre as vendas** · Bônus: 5% sobre a meta líquida"; capital and state of SP; "Carteira ativa de clientes (**exigência fundamental**)"; "Não oferecemos ajuda de custo".
  - …/ad_listing/vaga-para-representante-de-linha-cosmetica-capilar/ : "**comissionamento 10%** + bônus por meta"; channel is LOJAS.
  - …/ad_listing/sun-nails-brasil-procura-representantes/ : "**Comissao de 3%**" on salon cabins and nail motors. This is hardware, and it is the control case: a factory good returns to the 3% band.
  - …/ad_listing/distribuidora-dom-jose-busca-representantes-no-interior-de-sp/ : a distributor of Embelleze, Ruby Rose, Salon Line, Forever Liss, Davene and Alva. It wants "carteira acima de **50 clientes ativos e com R$ 70 mil mês**" plus "capacidade de visitação", and offers "Comissão… paga no faturamento… prazo 30/60/90 ao lojista, +10 marcas em uma única pasta". **Implied ≈R$1.400 per active client per month.**
  - …/ad_listing/cosmeticos-especiais-dermocosmeticos/ : "Pedido mínimo de **R$ 500,00**".
  - …/ad_listing/spa-pharma-cosmeticos-importados-de-israel-com-minerais-do-mar-morto/ : "Pedido Mínimo de **R$ 500** para Revenda".
  - …/ad_listing/cseros-cosmetics-busca-representantes-e-distribuidores-na-area-de-cosmeticos/ : opening order of 1 box of 12, then 5 boxes minimum.
  - …/ad_listing/distribuicao-em-saloes-de-beleza/ : distributor "Ganhos de 40% ou mais".
- https://portaldorepresentante.com.br/vagas-para-representantes/cosmeticosperfumaria/ : 5 live cosmetics postings.
  - …/29089-distribuicao-de-cosmeticos-profissional-/ (Pravda Cosmética, 15/09/2026): "Rentabilidade de até 100% · Região fechada com exclusividade · pagamento em até 10X".
  - …/52006-representante-pap-cosmeticos-e-perfumaria-/ (Pra Gente RH, 24/09/2026): "Remuneração: **PJ fixo + comissão**"; "Visitas comerciais porta a porta… Veículo próprio". The fixed amount is not published.
- https://pravdacosmetica.com.br/distribuidor-cosmeticos : unreachable (HTTP 000 by curl, 503 by WebFetch). A search snippet reads "representação = 10% commission; distribuidor compra com 45–50% de desconto, rentabilidade 82–100%". **UNVERIFIED (snippet only).**
- https://olenkastore.com.br/ : distributor recruitment. "Você está disposto a investir no mínimo **R$15 mil**?" and "R$15.000,00 para áreas pequenas"; "área de atendimento exclusiva".
- https://portal.tjpr.jus.br/jurisprudencia/j/1865020/ (archive, THE MARGIN LAW) : industrial rate of 3–6%.
- ⇒ **Result: the MARGIN LAW holds, since the rate follows the principal's margin. Its arithmetic kill does not carry over to cosmetics.** At the current bar (gross R$12,3–17,0k a month):
  - at 10–15%, she needs **R$1,0–2,0M a year of paid sales**;
  - at 3–6%, she would need R$2,5–6,8M.
  - Note: the archive's "R$12,5–25M" was computed at the old US$10k target.

## D. The ANVISA feed and the rep market are the same brands (computed from H6A's `TA_CONSULTA_COSMETICOS.CSV`)
- 12 brands were seen recruiting reps or distributors on CONFERE, Central dos Representantes or Portal do Representante.
  - 11 appear in the ANVISA file; 10 notified hair or skin products in the last 12 months:
    - Êxodo/Hactoon: 41, newest 23/09/2026.
    - 4Angels: 20.
    - Pink21: 17.
    - Kah Noa: 9.
    - Olenka: 9.
    - Kapeh: 6.
    - Alther: 4, **made by VENEZA**.
    - Glam Professional: 4, **made by SDK**.
    - Pravda: 1.
    - Lokram and Fleur Noire: 0 in the last 12 months.
    - Dvien: absent from the file.
  - **The brands that are launching are the brands hiring sell-in, including brands made by the two largest "full-service" factories.**
- Debut brands: brand keys whose first-ever electronic notification falls in the last 12 months.
  - ≥1 notification: 3.676. ≥3: 1.820. **≥4: 1.270.** ≥6: 678. ≥10: 294.
  - Of the 1.270, 182 are own-notifying (holder has ≤3 brand keys); the rest are made by contract manufacturers.
  - Monthly debuts with ≥4 notifications ran 58–104 from Dec 2025 to Aug 2026.
  - A 25-key sample includes noise keys (DESODORANTE, CANETA, SAO, HOTEL, GIRLS…), so ≈75–90% precision gives **≈900–1.100 debut lines a year (≈75–90 a month).** The key extraction is H6A's (≈85% precision).

## E. The store and distributor pools (primary government data)
- https://servicodados.ibge.gov.br/api/v3/agregados/6450/… (IBGE CEMPRE, 2021, the last year of the series):
  - CNAE 47.72-5 cosmetics retail: **37.074 local units**, 147.258 people. By state: SP **11.710**, MG 2.989, PR 2.887, RJ 2.660, BA 2.150.
  - CNAE 46.46-0 cosmetics wholesale: **6.649 units** (SP 2.176).
  - CNAE 20.63-1 manufacturing: 2.365 units.
  - Excludes MEI; includes franchise stores.
- `work/AFE_NAC.CSV` (ANVISA AFE register, H6A copy): 15.458 active cosmetic AFEs.
  - 6.009 CNPJs hold "Distribuir" without fabricar or importar. 2.722 of them also hold a medicines AFE, which marks them as pharma distributors.
  - **2.173 hold only cosmetics/saneantes AFE**; 768 of those have cosmetic words in their name. SP 614, MG 354, PR 225.
  - SAC phone is present on 424 and homepage on 285, so phones must come from publica.cnpj.ws.
  - Caveat: brand owners that outsource manufacturing also hold "Distribuir", so this is an upper bound on real distributors.
- https://www.ebccosmeticos.com.br/ : a distributor, CNPJ 01.505.662/0001-86, SP. Channels listed: "**Televendas · WhatsApp · Representante Comercial**", "Exclusivo para CNPJs". **Stores do buy by phone and WhatsApp.**
- https://officialdistribuidora.com.br/ : "atende perfumarias, lojas de cosméticos, quiosques… todos com CNPJ"; "Atende **mais de 20 mil lojistas** e revendedores com **mais de 80 marcas** em pronta-entrega" (verified in the fetched page; imported perfumes and cosmetics; Goiânia/GO).
- https://www.bimdistribuidora.com.br/ : a distributor. "Mais de 40 representantes" appears in a search snippet only, not in the fetched HTML: **UNVERIFIED**.
- https://polyser.com.br/ : distributor order portal; "Seja Nosso Representante".
- https://www.zaxapp.com.br/cosmeticos-atacado : "+1000 Fornecedores" of B2B wholesale (Brás and Bom Retiro, mostly apparel). A partial self-serve route to lojistas.
- Store-side contactability (phone share of 4772 CNPJs) **NOT MEASURED**. Receita bulk hosts gave connection reset or closed tunnel (arquivos.receitafederal.gov.br, dadosabertos.rfb.gov.br). api.casadosdados.com.br is Cloudflare-blocked.

## F. The statute that makes commission verifiable by file (C4-compatible)
- https://www.planalto.gov.br/ccivil_03/leis/l4886.htm (Lei 4.886/65):
  - **Art. 32 §1º**: "O pagamento das comissões deverá ser efetuado até o dia 15 do mês subseqüente ao da liquidação da fatura, **acompanhada das respectivas cópias das notas fiscais**."
  - Art. 32: the commission is due "quando do pagamento dos pedidos".
  - **Art. 31**: exclusive zone, "**ou quando este for omisso**", gives the rep commission on business "ainda que diretamente pelo representado". It can be contracted away (archive: THE ANTI-DISINTERMEDIATION STATUTE).
  - Art. 27(j) indemnity on termination.
- LC 123 art. 18 §5-I **VII** (`work/aud3/lcp123.htm`): "representação comercial e demais atividades de intermediação" falls in **Anexo V**. With fator R ≥28% it moves to Anexo III (§5-J).
  - All-in rate computed at RBT12 R$150–200k: **9,1–9,6%** (Anexo III + 11% INSS on 28% pró-labore) or **15,5–15,75%** (Anexo V).
- https://www.core-sp.org.br/noticias/anuidade-2026 : fees are not in the HTML. **CORE fee UNVERIFIED.**
  - Brands ask for "CORE ativo" as a market gate. STJ REsp 1.678.551 (archive) says it is not a legal gate.

## G. Other lens needs, each tested and killed
- https://www.gs1br.org/tabela-de-valores : GS1 Brasil sells barcodes directly and self-serve: "taxa de inscrição (**R$ 683,00** para a maioria das categorias) + metade do valor da anuidade". It warns about "revendedores terceiros que vendem códigos avulsos". → DEAD (a cheap direct counter).
- https://www.123marcas.com.br/ : trademark registration "Investimento: **R$ 462**", with "Busca por marcas similares" included. https://123marcas.com.br/produto/busca-de-marca : "Cuidado com buscas gratuitas que visam apenas a venda", i.e. free searches are the category's lead magnet. INPI fees: 2026 table at gov.br returned 404 by curl. Secondary sources say R$440 per class for ME/EPP: **UNVERIFIED**. → DEAD (free front door; trademark-seat domain already exhausted).
- https://abihpec.org.br/comunicado/abihpec-e-beautycare-brazil-lancam-manuais-de-regulamentacao-tecnica-para-exportacao/ : export regulatory manuals are "material de livre consulta… todo o conteúdo em português". → DEAD (free front door).
- https://abihpec.org.br/release/empresas-participantes-do-beautycare-brazil-registram-us-3634-milhoes-em-exportacoes-no-ano-de-2025/ : 162 Apex-supported firms, US$363,4M FOB; Argentina US$69,87M, Mexico 63,59, Colombia 48,79.
- https://abihpec.org.br/release/beautycare-brazil-apoia-projeto-comprador-organizado-pela-beauty-fair-2026/ (search result) : free buyer programme for foreign buyers.
- https://gpcgateway.com/regulatory-regions/paraguay/news-detail/… (search snippet, secondary) : Paraguay Decree 2942 requires a locally registered company as the registrant. → The registration is held by the importer (COMPELLED-BUT-CREDENTIALLED).
- https://escalada.com.py/en/regulatory-affairs-paraguay/ : tunnel closed. Not read.
- https://www.belezanaweb.com.br/marketplace : HTTP 403.
- https://plugg.to/exigencia-marketplace-beleza-na-web/ (search snippet, secondary) : "precisa de um Hub de Integração". Marketplace onboarding goes through self-serve hubs. Operating the brand's seller account would be standing access (C4). → DEAD.
- Pharmacy-chain listing fees ("taxa de cadastro", "verba de enxoval"): no primary source found in one search. **UNVERIFIED.** Retail media needs the SKU to be listed first. → not a launch-window service for a debut brand.
- https://glam.com.br/loja/marcas and InfoMoney on Glambox (search) : brands supply samples; brand-side fee not published. Glambox owns the channel. → DEAD for her.
- Outsourced SAC/cosmetovigilance for launches: RDC 894/2024 art. 46 §1º forbids outsourcing cosmetovigilance to an autonomous third party (archive-verified in CLAUDE.md, not re-fetched). → DEAD.
- https://portalradar.com.br/… and https://revistabusiness.com.br/2026/09/18/… (search snippets, secondary) : Beauty Fair 2026 had ~500 exhibitors, ~2.000 brands, 200k visits; "22,35%" of visitors were retailers, distributors or reps. It is the annual brand↔distributor meeting point, and it costs a booth.

## H. Rails that failed
- Receita bulk CNPJ hosts: reset or tunnel closed.
- casadosdados: Cloudflare.
- glamprofessional.com.br: proxy connect_rejected.
- pravdacosmetica.com.br and vnzconsult.com.br: no response.
- INPI fee PDF: 404.
- escalada.com.py: tunnel closed.
- belezanaweb: 403.
- TLS was never bypassed. Etsy and Faire were not attempted.

## I. Arithmetic (`calc.py` → `calc_out.txt`; PTAX 5,1795 on 24 Sep 2026, per AUD3)
- **Gross needed:** R$12.334 to 17.033 a month.
  - Low end: net R$10.400, stack R$750, 9,6% tax.
  - High end: net R$12.950, stack R$1.400, 15,75% tax.
- **Paid sales needed:**
  - at 10%: R$123–170k a month (R$1,48–2,04M a year);
  - at 12%: R$103–142k;
  - at 15%: R$82–114k.
- **Active stores needed at 10%** (Dom José implies R$1.400; R$600–900 is UNVERIFIED for unknown debut lines):
  - 88–122 stores at R$1.400 per store per month;
  - 137–189 at R$900;
  - 206–284 at R$600.
- **C1 scenarios:**
  - Month 12, pessimistic: net US$88.
  - Month 12, base: net US$786.
  - Month 18, base: net US$2.078 at 83,8 h.
- **C2 scenarios:**
  - Month 12: net US$297.
  - Month 18: net US$1.083 at 45,5 h.
  - Pairs needed for the bar: 51–71 at 3% × R$8k, or 31–43 at 5%.
