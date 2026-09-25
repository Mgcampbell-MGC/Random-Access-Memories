# LA1 — source log (Hunt 6, lead arbitrage via paid ads, energy first) — 25 Sep 2026

Fetched with curl (browser UA) unless marked. Local copies are in `work/la1/`. "Snippet" means a search-result summary only, NOT read at source.

## Energy: dates, law, state counter
- https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D13097.htm — Decreto 13.097 of 12/08/2026, art. 1: low-voltage (<2,3 kV) consumers may choose their supplier from **25 Nov 2027 (industrial and commercial)** and **25 Nov 2028 (everyone else)**. Art. 2: they must be represented by an agente varejista. Art. 3: 90-day notice. Art. 9 §1–2: ANEEL may provide for sharing of distributor-held personal data "de forma não discriminatória, com amplo e isonômico acesso aos interessados", only with prior consent or another LGPD basis. **Art. 10: CCEE "deverá disponibilizar plataforma centralizada que permita a comparação de ofertas"**. Its sole paragraph: CCEE tells all varejistas about consumers on supplier-of-last-resort.
- https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15269.htm — Lei 15.269 of 24/11/2025 (DOU 25/11/2025). Lei 9.074 art. 15 §17 says "até 24 meses" for industrial/commercial and "até 36" for the rest, and requires a "produto padrão e… preço de referência".
- https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm — Lei 14.300 art. 27: the Fio B share on energy compensated by non-grandfathered GD is 60% from 2026, 75% from 2027 and 90% from 2028. The art. 17 rule applies from 2029.
- DD3's output (out/DD3.json) covers ACL commissions, Cemig SINERGIA (R$7/MWh × months at signing), the BDGD pool, Clarke/UC Livre and the Ecom terms. I did not re-derive any of it.

## Energy: who pays for leads, meetings and activations
- https://afiliados.leadenergy.com.br/ plus the terms PDF https://afiliados.leadenergy.com.br/termo_adesao.pdf (read in full). Lead Energy SA pays a **bonificação of 0,5% of the indicated bill, capped at R$300 per client, for a "Cliente Elegível"** (simulation plus a valid meeting). Commissions are R$4→7/MWh by tier. It pays R$1.200 per multi-UC management client and R$1.800 per large-client UC. Payment follows invoice liquidation, "cerca de 60 dias desde a emissão da nota fiscal". The terms also say:
  - cl. 3.4: the affiliate warrants consent;
  - cl. 3.7: leads from "campanhas internas" are void;
  - cl. 3.8: the buyer's records prevail;
  - cl. 3.9: no "listas não autorizadas";
  - cls. 5.3–5.4: the buyer can re-cut commissions and claw them back.
  The site says it "possui uma inteligência capaz de ler o pdf original de uma conta de luz".
- https://publica.cnpj.ws/cnpj/38422829000155 — LEAD ENERGY SA, São Paulo, capital R$3.529.705,76, porte Demais, opened 11/09/2020.
- https://despertaenergia.com/blog/parcerias-energia-solar — the payer's own blog, 29/10/2025. Commission options: one-off up to 60% of the client's monthly consumption value (40% in one payment, or up to 60% in up to 3x), or 3,5% of every paid invoice "por prazo indefinido", or a mix. Paid after the client's 1st invoice is paid. Clients need a bill ≥R$300 and must be in a served region. The first partner to register a CPF/CNPJ gets the client. No fee and no minimums.
- https://www.neoenergia.com/web/produtos-e-solucoes/parceiro-neoenergia — "comissões por cada contrato fechado". Amount not published. PJ only, bills ≥R$5.000.
- https://sunne.com.br/blog/parceria-em-energia-por-assinatura/ — "indique, a Sunne fecha e você ganha". No number published.
- https://comparesolar.com.br/seja-parceiro/ — **"Pré-lançamento"**. Sells leads to GD operators: shared R$35–75 (sent to 3–5 suppliers), exclusive R$70–150. Prepaid credits, unused credits returned. Automatic 24h refund if a lead fails any of 4 machine-checked criteria (CEP, bill value, WhatsApp, distributor). Consent log is shipped with each lead. Claims 100% organic Google traffic. "Ticket médio do consumidor R$ 1.106/mês".
- https://publica.cnpj.ws/cnpj/26704902000100 — CompareSolar = PERFORMANCE DIGITAL SERVICOS EM COMUNICACAO LTDA, EPP, Fortaleza, capital R$100.000.
- https://www.portalsolar.com.br/mercado-livre-de-energia — the ACL form asks for bill upload ("Anexe uma ou mais contas de Luz"). https://www.portalsolar.com.br/leads.html has no price.
- https://gdash.io/blog/como-escalar-a-carteira-de-clientes-de-energia-por-assinatura/ — SaaS for GD gestoras/cooperatives: self-service simulation and digital adhesion. Also: "inadimplência em torno de 5% pode comprometer… a margem".
- work/dd3/sebrae.txt (fetched by DD3) — Solarien recruits partners on recurring commission.
- https://afiliados.leadenergy.com.br/ — "Em breve, mais de 90 milhões de consumidores… padarias, supermercados… salões de beleza… mais de R$500,00 por mês". This is the incumbent's own low-voltage positioning.

## Energy: ANEEL GD register (downloaded, computed)
- https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/cd29f6eb-e08d-4db7-b6fb-ed6e3b682d27/download/empreendimento-geracao-distribuida.parquet — 106 MB, 4.656.839 rows, data up to 31/08/2026.
  - "Compartilhada" (shared generation): 22.670 plants and 2.213.543 beneficiary UCs.
  - **By state: MG 1.920.197 (86,7%), PR 92.484, SC 51.002, SP 38.756.** The ELETROPAULO (Enel SP) concession has 341.
  - PJ owners: 396 CNPJ roots with ≥100 beneficiary UCs hold 98,7% of the total. 179 roots have ≥500 and 121 have ≥1.000. Present in MG: 124 with ≥500 and 86 with ≥1.000.
  - **The Cemig SIM consortia hold 590.238 UCs (27,2%).**
  - Plants with ≥20 UCs by cadastral-update year: 2023 982, 2024 956, 2025 605, 2026 (Jan–Aug) 92. This year is a proxy for connection date (UNVERIFIED as such).
  - Named operators: Bulbe 140.920 UCs (MG), Órigo 39.196, Desperta 41 plants/734 UCs, Sunne 18 plants/665 UCs, Lemon 4 plants/414 UCs. Many operators manage consortia held under other names.
  - Top 60 owners saved to out/LA1_gd_owners_top60.csv.
- work/dd3/ucmt_pj.csv (ANEEL BDGD, fetched by DD3). MG Grupo A PJ units with coffee CNAE 0134: 616 active, 474 captive with no GD, median 13 MWh/month. MG rural-class PJ Grupo A: 3.645 active and 2.856 captive with no GD, median 18 MWh. This is an enumerable universe, so it suits DD3's calls and not ads.

## Other verticals — prices
- https://salyd.com.br/ — observed live marketplace listings of exclusive health-plan leads. Examples: R$9,51 (Hapvida, Porangatu GO, CNPJ 3–5 vidas, 4 days old), R$12,40, R$14,80, R$11,20. Tiers: Start R$9–15, Piloto Automático R$10–22, PRO R$13 average from 300 leads/month. "Reposição Automática/Garantida".
- https://venda.doutorleads.com/Pacote-de-leads-para-vender-planos-de-sa%C3%BAde-PF-e-PME — R$1.449/60, R$2.760/120 and R$13.125/600 regional health leads, each with a buy button.
- https://www.bancadeleads.com.br/leads-plano-de-saude.html — prepaid credits. No price visible.
- https://blog.getninjas.com.br/como-funcionam-as-moedas-do-getninjas/ — 500 moedas for R$69,90, packs up to 4.800. Each request can be unlocked by up to 3 providers.
- https://www.getninjas.com.br/central-de-ajuda/profissional/pagamento/o-que-sao-moedas — coins expire after 3 months. GetNinjas LTDA, CNPJ 55.744.877/0001-89.
- https://solartask.com.br/ — rooftop solar comparator, free: "8.000+ empresas instaladoras · 5.000+ cidades · Até 3 propostas por pedido".
- meusite.solar (R$99/month incl. free Solar Task listing) and web.solarideal.com.br (R$49,90/month unlimited leads): snippet only, connection reset. UNVERIFIED.
- https://www.loja.marketingparaconsorcio.com.br/100-leads-de-consorcio-mailing-nacional (WebFetch) — a consórcio "mailing" of 100 contacts in Excel. Product unavailable, no price.
- https://wesow.com.br/quanto-custa-terceirizar-a-prospeccao-b2b/ — outsourced SDR at R$3–15k/month; the market does 15–25 meetings/month per SDR (vendor). The nav lists "Agendamento de reuniões qualificadas para empresa de energia"; that page returned 403.
- https://portal.cfm.org.br/images/PDF/cem2019.pdf — Código de Ética Médica. Art. 59 forbids "remuneração ou vantagens por paciente encaminhado ou recebido". Art. 58 forbids "exercício mercantilista". Art. 72 forbids ties with financing/consórcio firms.

## Ad platforms
- https://ads.tiktok.com/help/article/about-daily-budgets?lang=en — the campaign daily budget must exceed US$50 and the ad-group daily budget must exceed US$20.
- https://ads.tiktok.com/help/article/budget-and-bidding-faq?lang=en — same minimums, US$50 and US$20.
- https://ads.tiktok.com/help/article/lead-generation-objective?lang=en — recommends 3–5 ad groups, each with a daily budget at least 10× the expected CPA. Instant form or own website.
- https://ads.tiktok.com/help/article/lead-generation-faq?lang=en — the paid Lead Generation objective is "Full GA". Leads are available for 90 days.
- https://ads.tiktok.com/help/article/explaining-privacy-practices-to-lead-generation-ads-users?lang=en (Feb 2025) — a privacy policy is required. Sharing with "commercial partners" must be disclosed.
- https://ads.tiktok.com/i18n/official/policy/lead-gen-terms — JS-rendered, not readable. According to a search snippet, the third-party clause limits use and sharing "on behalf of that third party". UNVERIFIED.
- https://ads.tiktok.com/help/article/tiktok-ads-policy-other-products-and-services?lang=en — no energy, utility or solar restriction. The only "energy" match is energy drinks. Legal services and accounting are restricted in Brazil.
- https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content?lang=en — no exaggerated results and no absolute terms. Price and discount must match the landing page and its T&C. **AIGC must be labelled; undisclosed AIGC is rejected.**
- https://ads.tiktok.com/business/en/inspiration/small-business-stepful-uses-lead-generation-to-reach-prospects, …/qatch-lead-acquisition-case-study, …/invisalign-smile-quiz-lead-generation — US CPL case studies (snippet). Platform marketing.
- https://www.reformatributaria.com/wp-content/uploads/2025/09/Comunicado-oficial-Meta.pdf — Meta's letter to customers. From 01/01/2026 it passes on PIS/Cofins 9,25% and ISS 2,9%, about +12,15%. Prepaid R$1.000 buys R$878,50 of delivery. Applies to clients billed by Facebook Serviços Online do Brasil Ltda.
- facebook.com/business/help/203183363050448 (minimum budgets) and facebook.com/legal/leadgen_tos (Lead Ads Terms) — HTTP 400 or JS-only. UNVERIFIED.
- CPL benchmarks: all vendor or agency, via snippets. UNVERIFIED.
  - babitonhela.com: R$8–35 native, R$15–80 LP.
  - altavance.media: R$8–25 local.
  - LinkedIn agency post: 265 solar contacts at R$9.
  - givanildo.com.br: health R$3–15.
  - telescopiomarketingdigital: móveis planejados R$15–80.

## LGPD, telemarketing
- https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (decoded cp1252) — the provisions relied on:
  - art. 7 I and **art. 7 §5** ("consentimento específico… para esse fim" before sharing with other controllers);
  - art. 8 §4 (generic authorisations are null);
  - art. 9 V and §1;
  - art. 18 VII;
  - art. 52 II (fine up to 2% of revenue, capped at R$50M per infraction).
- https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_legitimo_interesse.pdf/@@display-file/file — ANPD legitimate-interest guide (Feb 2024). One of its legitimate-expectation factors is whether the data were "obtidos por meio de compartilhamento realizado por terceiros".
- https://www.privacidade.unicamp.br/2023/07/18/anpd-aplica-a-primeira-multa-por-descumprimento-a-lgpd/ — mirror of ANPD's news, which returned 401. **ANPD's first sanction went to Telekall Infoservice, a microempresa offering a WhatsApp contact list of voters: R$14.400 (2% cap per infraction) for art. 7, plus a warning for art. 41.**
- https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-aplica-a-primeira-multa-por-descumprimento-a-lgpd — HTTP 401 ("Conteúdo Restrito").
- https://www.gov.br/anpd/… (news) — not readable.
- https://www.gov.br/anpd/… (Telekall) — not readable.
- https://www.gov.br/anatel/pt-br/regulado/numeracao/telemarketing-ativo-prefixo-0303 (modified 28/08/2026) — **0303 is optional since Acórdão 201 of 14/08/2025**. Call authentication is mandatory only above 500.000 calls/month. "Não Me Perturbe" covers telecom and consignado only.

## Disputes
- THE_COROA_KILL.md (in the repo) — GetNinjas seller-side complaint quotes. Not re-fetched.
- https://www.reclameaqui.com.br/… — 403 Cloudflare, both with curl and WebFetch. The search result title "Prometem leads qualificados para energia solar e não entregam — DIGITAL MEDIA" was seen; the body is UNVERIFIED.

## Unreachable / blocked this session
solarlead.eco.br (DNS), leadssolar.com.br, meusite.solar, web.solarideal.com.br, leadsmoveisplanejados.com.br (connection reset), clienteja.com (502), reclameaqui.com.br (Cloudflare), facebook.com legal/help pages (JS), TikTok lead-gen terms (JS), wesow energy page (403).

## Arithmetic
Computed in Python. The script and figures are in work/la1/build_json.py; the inline calculations are recorded in this session.
- Target: net R$10.400–12.950 + R$1.000 stack. Tax 8% on gross (UNVERIFIED annex). Media × 1,1215 (Meta tax).
- Cost per verified lead = CPL × 1,1215 ÷ (bill-sent × eligible).
- Cost per activation = the verified-lead cost ÷ close rate.
- PTAX 5,2037 R$/US$, from CLAUDE.md.
