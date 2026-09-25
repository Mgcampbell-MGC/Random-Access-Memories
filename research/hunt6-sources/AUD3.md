# AUD3: source log (arithmetic, units, price reality). Hunt 6, 25 Sep 2026

One line per source: what it said. Local copies and scripts are in `work/aud3/`: `calc.py` (bar, units, pools, treadmill), `hours.py` (hours by maturity), `build.py` (JSON), `fabrica.txt`, `lcp123.htm`.

## Fetched today (primary)
- https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo (18–25 Sep 2026): PTAX venda 24 Sep 2026 = 5,1795 (the latest published). This confirms H6D's rate. H6B used the archive's 5,2037 instead.
- https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm, Anexo III (LC 155/2016 wording): 6,00% up to R$180k; 11,20% less R$9.360 for R$180–360k.
- Same page, Anexo V: 15,50% up to R$180k; 18,00% less R$4.500 for R$180–360k.
- Same page, art. 18 §5-B XV: "produções cinematográficas, audiovisuais, artísticas e culturais… artes visuais…" go to Anexo III. §5-I VI covers "design" and X covers "jornalismo e publicidade" (Anexo V). §5-J moves those to Anexo III if payroll is at least 28% of revenue. §24 counts "retiradas de pró-labore" as payroll.
- https://www.planalto.gov.br/ccivil_03/leis/l8212cons.htm: art. 21 sets the contribuinte individual rate at 20%. Art. 30 §4 lets the worker deduct 45% of the company's contribution, capped at 9% of the salary-de-contribuição. The result is the 11% used here (derived; not checked against the IN RFB).
- https://www.planalto.gov.br/ccivil_03/leis/2003/l10.666.htm: art. 4 makes the company withhold the contribuinte individual's contribution from pay.
- https://www.estudiofabrica.com.br/servicos-e-precos/ (read in full). This is an apparel/e-commerce studio working in the "centro expandido da cidade de São Paulo". Its prices:
  - AI lines: lookbook with AI R$35 per up to 3 images; lookbook + basic video (2 takes, up to 11 s) R$80 per look; lookbook + video with pose variation (up to 15 s) R$120 per look; AI persona R$53; "Imagem Conceito/Campanha/Redes sociais" R$53 per image; 15–20 s video R$260; "(Direcionamento criativo definido pelo cliente…)".
  - Its AI caveat: "A geração sempre será focada na peça principal, não garantindo fidelidade às demais peças". **This refers to complementary GARMENTS, not labels.**
  - Traditional lines: "Produção de Conteúdo" R$1.250 per period (studio, scenery, lighting, treatment of up to 50 images or 5 edited videos; no model or makeup); external shoot R$1.600 for a half day of 40 images and R$2.500 for a full day of 80 images; lookbook R$1.250 per half day of 40 looks, hair and makeup included, model fee not included; white-background still R$18–25 per image; studio rental R$530 half day / R$850 full day; "Montagem de kits" R$53–80.
- https://jobformodel.com/public_jobs: 13 live jobs today, none from a beauty brand. Buyer-posted model diárias include: snack brand social videos R$2.500 (2-year usage); accessories brand R$1.200 (RJ) / R$1.500 (SP); Ferrero Rocher campaign photos (R$2.500 per H6B); a trade-fair show R$700/day.
- https://www.99freelas.com.br/projects?q=cosmeticos (also searched: cosméticos, skincare, "fotos produto cosméticos", "vídeo cosméticos", "campanha cosméticos", shampoo, "lançamento produto"): 12 distinct projects.
- https://www.99freelas.com.br/project/producao-de-video-institucional-para-marca-de-cosmeticos-784923: "Orçamento: Aberto… Valor Mínimo: R$ 50,00", 18 proposals.
- https://www.99freelas.com.br/project/social-media-para-marca-de-beleza-e-subscription-box-780472: "Aberto", minimum R$60, 29 proposals.
- https://www.99freelas.com.br/project/criacao-de-logotipo-e-identidade-visual-para-marca-de-cosmeticos-786124: "Aberto", minimum R$50, 59 proposals. On 99Freelas the buyer budget is not disclosed, so these pages give no price evidence either way.
- https://www.contweb.com.br/planos-mensais: online accounting for Simples Nacional "a partir de R$ 99,99 / mês"; MEI R$49,00; Lucro Presumido R$149,99.

## Blocked or not usable (today)
- https://www.workana.com/pt/jobs?... returned 403 (Cloudflare) directly, via the r.jina.ai reader, and via WebFetch. The Workana budgets quoted come from H6B's earlier read.
- https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=10840123 returned an HTML session stub, so no TJSP case with a campaign contract value was read.
- The Sebraetec price-table PDFs (sebrae.com.br …/PI/…Tabela de preços atualizada junho 2024.pdf and …/ES/…Tabela de Preços 4.0 – PST V6.pdf) served a portal HTML shell. That leaves UNVERIFIED a possible CHEAP COUNTER: Sebrae subsidises 70% of design and marketing services for small firms.
- https://business.adobe.com/products/firefly-business/firefly-creative-production/production-workflows.html returned HTTP 503 / a stream error. The "3D digital-twin product fidelity" claim comes only from a search-result summary (SECONDARY).
- The contabilizei.com.br price pages returned 404, agilize.com.br/planos 404, and contabilivre 403.

## Web searches (no primary price evidence found)
- "campanha feita com IA marca de cosméticos brasileira custo produção reais 2026": no case study with a value.
- "quanto custa ensaio fotográfico campanha marca de cosméticos preço…": only studios that quote on request.
- "casting campanha marca de cosméticos cachê R$…": no fees published.
- "TJSP apelação cobrança contrato produção fotos… cosméticos": no readable value.
- "marca de cabelos… 'investimento de R$'…": no values.
- "Sebraetec fotografia de produto valor tabela…": the tables are not reachable.
- "fotos com IA para marcas de cosméticos preço…": only a Cronoshare aggregate (20–30 photos for R$400–1.500), which is SECONDARY and a public marketplace.

## Inputs taken from other agents (their sources; not re-fetched unless listed above)
- H6A (ANVISA TA_CONSULTA_COSMETICOS.CSV, publica.cnpj.ws, Beauty Fair, ABIHPEC): about 300 brands (range 225–425), 1–4 campaign-sized launches per brand per year, and a production mix from n=15 (5 model shoots / 8 product-only or 3D / 2 likely AI). The 79-day lead time is from 18 pairs across 3 brands.
- H6B (Make Move script.js, animaistudio.com.br, destaquei.com.br, Sinapro 2025 PDF, VintePila, Fiverr, Workana): prices of AI studios, traditional producers and marketplaces. Two figures are H6B's own computations: the ANIMAI HERO-equivalent (R$1.400–2.900) and the traditional build (R$9.900–17.000).
- H6C (LC 123, SC COSIT 466/2017, 145/2023): CNAE split and the Anexo III vs V question. The UNVERIFIED classification of AI-only film is moot under the fator-r route.
- H6D (Photoroom benchmark, Higgsfield recipes, App Store / Adobe / Frame.io price pages, Robert Half 2026): hours per HERO (14–28 at the start, 9–15 after campaign 15, 6–9 re-specced); non-generation stack R$387,11 per month; Higgsfield PLUS R$262,68 and ULTRA R$691,54 including IOF; in-house replacement cost R$500–1.350.
- H6F (Revendi, ABEVD, BR Catálogos, Fábrica): CICLO pool of 20 brands × 9 revistas × R$4.500 = R$810k. DeMillus is the only brand whose cadence (9 revistas) was verified. The claimed workload is 15–20 h per pack.

## Arithmetic (reproduced in work/aud3/calc.py and hours.py)
- **Net target:** 2.000–2.500 × 5,1795 = R$10.359–12.949 per month.
- **Gross needed:** (net + fixed stack R$750–1.379) ÷ (1 − 9,08–9,35%) = R$12.218–15.806 per month.
- **Units per month:** HERO 2,07–2,68 · KIT at R$2.500 4,89–6,32 · at R$3.000 4,07–5,27 · at R$3.500 3,49–4,52 · REVISTA 2,72–3,51.
- **Mix A** (1 HERO + 2,5 KIT at R$3.000 = R$13.400 gross) nets R$10.768–11.434, i.e. US$2.079–2.207.
- **Fábrica-rate equivalents:** HERO R$1.030–1.150 · KIT R$578–631 · REVISTA R$1.740–2.090 at the lookbook rate or R$4.220–5.810 at the campaign rate.
- **Lean traditional with a model:** R$4.150–7.050. R$5.900 is 84–142% of that.
- **Pools and required share** (required revenue R$146,6–189,7k):
  - HERO: 4,1–5,4% as the plan implies · 12,6–16,2% at P=33% central · 33,5–43,3% at P=33% low.
  - KIT: 8,1–10,5% as the plan implies · 24,7–31,9% at P=33% central.
  - REVISTA: 18,1–23,4% with 20 brands · 25,9–39,0% with the 12–14 beauty-only brands.
- **Treadmill:** at R$2.000 per set she needs 6,1–7,9 sets a month; at R$1.500, 8,1–10,5.
