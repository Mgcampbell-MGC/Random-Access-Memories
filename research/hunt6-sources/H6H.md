# H6H — source log: the kit desk's field failure (freight + corruption), tested at primary sources

Agent H6H, Hunt 6, 25 Sep 2026. Question: is the archive's "thin-field premium" partly a directed-tender
premium, what does freight on bulky kits really cost, and is there a repaired desk that survives both.
Working files: `scratchpad/hunt6/work/h6h/` (cache, scripts, extracted PDFs).

## A. Coari/AM — 34,8% of the archive's clearing pool, read document by document

- `https://pncp.gov.br/api/search/?q=coari%20enxoval&tipos_documento=edital` — Coari compra 2025/238 is
  indexed `Pregão - Presencial`, `data_publicacao_pncp` **2026-03-16**, `data_fim_vigencia` (proposal close)
  **2025-03-14**: published on PNCP **367 days after the session**. A PNCP art. 54 cron could never have seen it.
- `https://pncp.gov.br/api/pncp/v1/orgaos/04262432000121/compras/2025/238/itens?pagina=1&tamanhoPagina=100` —
  30 items = one 15-item kit × 2 lots: **12.960 kits** (Sem benefício) + **1.440 kits** (ME/EPP quota). Estimates:
  banheira R$63,11, macacão soft R$43,20, bolsa R$132,67, body+bermuda R$71,34, cueiro R$44,06.
- `.../compras/2025/238/itens/7205911/resultados` — VITORIA REGIA CONFECCAO, banheira **R$62,70**,
  `percentualDesconto` **0,6496%**, `dataResultado` 2026-03-16 (insertion date, not the real award date).
- `https://pncp.gov.br/pncp-api/v1/orgaos/04262432000121/compras/2025/238/arquivos/3` (despacho de homologação,
  PDF, 5 pp.) — "PREGÃO PRESENCIAL Nº 010/2025-CCC"; lot 1 VITÓRIA RÉGIA (CNPJ 27.698.768/0001-37) 12.960 kits,
  **"VALOR UNITARIO DO KIT R$ 675,37"**; lot 2 OLIVEIRA CONFECÇÃO E SERVIÇOS DE IMPRESSÃO (04.896.372/0001-07)
  1.440 kits at **R$676,00**. Every one of 15 items awarded at 99,3–100,0% of its estimate (toalhas umedecidas
  and luva/gorro exactly at estimate). Brand column lists a bath towel as "PAMPERS / NACIONAL" (odd, not proof).
- `.../2025/238/arquivos/4` (ARP 21/2025, 13 pp.) — signed **25 Mar 2025** by the SEMAS secretary; validity 12
  months; winner address Manaus/AM.
- `.../2025/238/arquivos/1` (zip → EDITAL-PREGÃO-PRESENCIAL-010.pdf, 94 pp.) — session **14/03/2025 08:30 at the
  Coari city hall** (river town, no road to Manaus); invokes "art. 17, §§ 2º e 5º" with no stated reason for the
  presencial form; **MENOR PREÇO POR LOTE**; copies to be authenticated by cartório or the commission "em até 2
  (dois) dias úteis antes"; atestado must prove "pelo menos 10% das quantidades" (= 1.440 kits of prior
  delivery); adesões allowed up to "o dobro do quantitativo de cada item registrado".
- IBGE SIDRA t.2612 `https://apisidra.ibge.gov.br/values/t/2612/n6/1301209/v/218/p/2022,2023,2024` — Coari births
  (mother's residence) **1.440 / 1.429 / 1.300**. ⇒ 14.400 kits registered = **11,1× a year of births**; ARP ceiling
  12.960×675,37 + 1.440×676,00 = **R$9.726.235**.
- `https://transparencia.coari.am.gov.br/download.php?file=...ata_de_registro_de_precos_29_2025.pdf` (read via
  WebFetch download) — ARP 29/2025, **Pregão Presencial 019/2025**, uniformes for the same SEMAS, same secretary,
  **same winner VITÓRIA RÉGIA**, signed 14 Apr 2025.
- `https://publica.cnpj.ws/cnpj/27698768000137` — VITORIA REGIA: EPP, Manaus, capital R$2.000.000, main CNAE
  "confecção sob medida", secondary CNAEs incl. tintas, material elétrico, hidráulico, papelaria, brinquedos.
  `https://publica.cnpj.ws/cnpj/04896372000107` — OLIVEIRA CONFECÇÃO E SERVIÇOS DE IMPRESSÃO: Presidente
  Figueiredo/AM; secondary CNAEs include **boat repair, sewage networks, earthworks, foundations, road works,
  building painting** — a generic "faz-tudo" object.
- **The natural experiment.** `https://pncp.gov.br/api/pncp/v1/orgaos/04262432000121/compras/2026/95/itens` +
  `/resultados` + `.../2026/95/arquivos/2` (homologação PE 47/2026, 3 Sep 2026) — same buyer, same object,
  **Pregão ELETRÔNICO**: 5.670 + 630 kits; lot 1 estimate R$8.102.033,10 → **R$4.808.160 (ratio 0,593)**, PONTO
  NORTE AMAZONIA LTDA (Manaus, 67 secondary CNAEs); ME lot 0,773, VITALOG LTDA (Urucará/AM, 94 secondary CNAEs).
  Same-spec items, presencial 2025 → eletrônico 2026: **banheira anatômica PP R$62,70 → R$25,00 (−60%) · macacão
  R$43,00 → R$25,00 (−42%) · kit cueiro 3 un R$43,95 → R$26,00 (−41%) · kit banho 3 pç R$31,96 → R$21,00 (−34%) ·
  toalhas umedecidas R$19,32 → R$15,50 · sabonete R$13,50 → R$13,00.** At Sol's verified costs the 2026 banheira
  is −19% (R$29,71 cost) and the macacão +22% (R$19,60).
- `.../compras/2026/59` — PE 032/2026, same kits, retified, no result ("Em andamento").
- SICONFI `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio=2026&nr_periodo=3&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2007&co_esfera=M&id_ente=1301209`
  — Coari restos a pagar processados: inscritos R$6.963.391,36, pagos R$4.462.227,05 ⇒ saldo **35,9%** — fails the
  archive's own ">0,30 reject" payment rule.
- MPAM (primary, institutional) `https://www.mpam.mp.br/noticias-portal/18206-em-coari-ministerio-publico-recomenda-adocao-de-pregao-eletronico-apos-apuracao-de-editais-presenciais`
  — 9 Apr 2025, recommendation **nº 2025/0000042102.02PROM_CIZ** to mayor Adail Pinheiro after a complaint about
  **"sete editais de licitação em 2024, todos na modalidade presencial, sem justificativas compatíveis"**.
- News (SECONDARY, not re-verified at TCE-AM): `https://fatoamazonico.com.br/tce-am-barra-licitacao-da-prefeitura-de-coari-por-indicios-de-manobra-para-restringir-concorrencia/`
  (27 May 2025: TCE-AM cautelar suspends Coari **Pregão Presencial 42/2025** for unjustified presencial form and
  non-publication of the full edital) · `https://portaltucuma.com.br/tce-am-denuncia-licitacoes-de-coari/`
  (1 Sep 2026: TCE-AM admits a representation of "direcionamento sistemático" on six 2026 Coari pregões
  eletrônicos 043, 046, 053, 057, 058, 063/2026; removal of two pregoeiros requested) ·
  `https://emtempo.com.br/390134/amazonas/ministerio-publico-recomenda-que-coari-abandone-o-papel-e-cumpra-lei-das-licitacoes/`.
- TCE-AM Diário Eletrônico ed. 3638, 18 Sep 2025 `https://doe.tceam.tc.br/wp-content/uploads/2025/09/Edicao-de-n%C2%B03638-de-18-de-setembro-de-2025.pdf`
  — embargos on the 2023 annual accounts of the **Fundo Municipal de Assistência Social de Coari** (the fund that
  buys the kits); representation against Câmara de Coari PE 003/2025. Outcome of the FMAS accounts: UNVERIFIED.
- CGU CEIS/CNEP bulk `https://portaldatransparencia.gov.br/download-de-dados/ceis/20260924` and `/cnep/20260924`
  (23.720 + 1.814 rows) — **none** of the four Coari kit winners is listed.

## B. The other named high-price buyers

- Arinos/MG (archive top-10 clearing, R$170.769): PNCP `18125120000180-1-000012/2025` — published **16 Oct 2025**,
  proposals closed **28 Apr 2025** (5,5 months late); 300 kits at R$569,23 vs est R$581,57 (**0,979**), RUY COMERCIO
  VARIEDADES, ME/EPP exclusive. Births 238 (2024).
- Maués/AM (fixture R$298): `04282869000127-1-000006/2026` — 1.265 kits at R$298,00 vs est R$300,53 (**0,992**),
  F. B. PEREIRA LTDA; births 1.059 (plausible 1,2×).
- Icatu/MA (0% paid per archive): `05296298000142-1-000038/2025` — eletrônico, 13 days' notice, 1.172 + 390 kits at
  R$296,84 vs R$395,78 (0,75), J E C DA COSTA NETO-ME; births **223** ⇒ **7,0×**.
- Serrano do Maranhão/MA: `01612626000111-1-000014/2026` — 300 kits R$555 vs R$731,65 (0,759), GLOBAL
  EMPREENDIMENTOS E ASSESSORIA; births 128 ⇒ 2,3×.
- Nhamundá/AM (0% paid per archive): `04283578000153-1-000022/2026` + ARP 013/2026 (`.../2026/22/arquivos/2`, signed
  19 Aug 2026) — 3.500 kits est R$604,57, registered at **R$320,00** to **A. P. GOMES LTDA, Rua Furtado Belém 27,
  Nhamundá** (the prefeitura is at Rua Furtado Belém 42); main CNAE hospital-materials wholesale + minimercado,
  opened Feb 2022 (`https://minhareceita.org/45419693000190`). Births **318** ⇒ **11,0×**.
- Taiobeiras/MG: `01172959000177-1-000007/2026` — bolsa maternidade **4.850** units (GPADOVANO) vs births 403 ⇒ 12×.
- São Paulo capital, Mãe Paulistana PE 90392/2025 — BRINK MOBIL's recurso published in the DOC
  (`https://diariooficial.prefeitura.sp.gov.br/md_epubli_visualizar.php?hgq9w...`): alleges award R$875,17/kit vs
  "valor médio de mercado" R$594,06 × 72.000 kits = "SUPERFATURAMENTO DE R$ 20.239.920,00", and that requests to
  view the process on 04/06, 15/08 and 16/09 were ignored. **A losing bidder's allegation — UNVERIFIED.** (BRINK
  MOBIL itself is in CEIS: impedimento by Uberlândia/MG 26/02/2025–26/02/2028.)

## C. Population measurements (PNCP, this agent's harvest)

- Tender list: `https://pncp.gov.br/api/search/?q={12 kit queries}&tipos_documento=edital&tam_pagina=500`, filtered to
  newborn-kit objects → **2.751 compras** (2021–2026). See `kit_compras.json`, `nb_compras.json`.
- Line data: `/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{seq}/itens` + `/itens/{n}/resultados` for the compras with
  results published since 1 Jan 2025 (see section D of the JSON for the sample actually harvested — PNCP latency was
  bimodal 0,5 s / 15 s all afternoon, so the harvest is partial and says so).
- Winner registry: `https://minhareceita.org/{cnpj}` (UF, CNAE, capital, secondary-CNAE count; email not used).
- Births: `https://apisidra.ibge.gov.br/values/t/2612/n6/{codes}/v/218/p/2024`; IBGE codes from
  `https://servicodados.ibge.gov.br/api/v1/localidades/municipios`.


### C.1 Results (sample: 2.518 award lines, 572 of 1.100 kit editais with results since Jan 2025; full metrics in `out/H6H_metrics.json`)

- award ÷ estimate, median (share of lines ≥0,98): on-time pregão eletrônico **0,64 (11,4%)** · late-posted eletrônico
  0,58 (9,1%) · **presencial 0,994 (53,1%, n=32)** · dispensa 0,97 (45,9%).
- Gross at Sol's published SP cost by award÷estimate band: <0,6 **−21,8%** · 0,6–0,8 +15,1% · 0,8–0,98 +20,9% · ≥0,98 **+35,3%**.
- Component value clearing ≥50% gross: R$7.482.720 in sample (R$5.378.376 ex-Coari). **89,9% won by an in-state firm,
  7,1% by SP firms**; 49,9% in presencial/late/no-discount lines (30,3% ex-Coari); **only 5,3% (7,4% ex-Coari) clean AND
  won from outside the buyer's state.**
- Winner location, components: local 0,809 of estimate, +18,3% gross at her cost · out-of-state **0,625, −6,2%** · SP firms
  selling out of state 0,537, −11,1%. MG lines won from outside: +12,8% (n=80). Near region (S/SE/CO) out-of-state −4,9%;
  N/NE −8,5%.
- Kits by quantity band, local vs out-of-state winner: <300 kits 0,86 (R$250) vs **0,611 (R$178,85)** · 300–1.000 0,706 vs 0,518.
- Out-of-state-won component gross at cost ×1,0 / ×0,70 / ×0,55: **−6,2% / +25,7% / +41,6%** (fralda de pano +40,8% at ×1,0,
  manta +31,5%; banheira −18,1%, macacão −16,0%, toalha −11,9%, body −104%).
- Generalist winners (≥40 secondary CNAEs): 110 of 400; 31,1% of clearing value vs 24,2% of the rest; gross when they win
  +29,3% vs +11,8% for specialists (<10 CNAEs).
- Kits registered ÷ births 2024: median 0,89 · p90 2,92 · 16,2% of editais >2× · 3,2% >5×.
- CEIS/CNEP: 27 of 400 winners listed (6,8%), 1,5% of value.

## D. Freight

- Correios official calculator `https://www2.correios.com.br/sistemas/precosPrazos/prazos.cfm` (POST, balcão retail
  prices, 25 Sep 2026, origin 01310-100 São Paulo). Kit box **76×48×23 cm** (Plasútil 21 L bathtub envelope) at 5 kg
  and at 14 kg gives the **same price** (cubic weight governs). PAC service price + R$11,19 "manuseio especial
  (dimensão superior a 70 cm)": **SP capital R$85,29 · Belo Horizonte R$110,79 · Montes Claros R$177,29 · Fortaleza
  R$141,59 · Teresina R$172,19 · São Luís R$172,19 · Icatu R$172,19 (14–18 d.u.) · Manaus R$172,19 (20 d.u.) · Maués
  R$306,99 · Coari R$306,99 (26–30 d.u.)**. SEDEX São Luís R$442,60. Mochila-only kit 45×32×24 cm 4 kg: PAC
  BH R$50,50 · Fortaleza R$65,90 · São Luís/Teresina/Icatu R$81,70 · Coari R$153,60. Dense textile box 40×30×25 cm
  10 kg: PAC BH R$65,60 · Fortaleza R$86,00 · São Luís/Teresina R$106,20 · Montes Claros R$109,70.
- Correios limits (primary) `https://www2.correios.com.br/sistemas/precosprazos/Formato.cfm` — max 100 cm per side,
  C+L+A ≤ 200 cm. The 6.000 cubic factor and 10 kg threshold: SECONDARY (Melhor Envio/Frenet help pages); the
  5 kg vs 14 kg identical quote is consistent with it.
- Plasútil `https://www.plasutil.com.br/produtos/produto/013391-banheira-infantil-21-l-bichinhos` — "Dimensões (Comp
  x Larg x Alt): 76,0x47,7x22,4 cm", embalagem master 6. Envelope 0,081 m³.
- Infanti `https://infanti.com.br/products/banheira-fontana-duo` — "Dimensão de embalagem: 89,8 cm × 35,1 cm × 47,3 cm"
  (0,149 m³), product 5,15 kg.
- Observed LTL quotes, Alô Bebê VTEX checkout simulation (`POST https://www.alobebe.com.br/api/checkout/pub/orderForms/simulation?sc=1`,
  SKU 171154 Banheira Fontana Duo, 25 Sep 2026; the store's own contracted carriers, origin UNVERIFIED as SP):
  q=1 — Translovato BH R$109,60 · Montes Claros R$134,08; Farrapos Teresina R$134,48 · São Luís R$146,04 · Icatu
  R$172,11 · Fortaleza R$150,13; Translovato Manaus R$575,69 (30 d.u.). q=5 per unit — BH R$44,68 · Montes Claros
  R$57,51 · Teresina R$118,94 · São Luís R$129,46 · Icatu R$153,71 · Fortaleza R$123,64 · Manaus R$293,79. q=20 per
  unit — BH R$20,66 · Montes Claros R$27,16 · Manaus R$127,75; **all NE destinations "cannotBeDelivered" at q=20**
  (the carrier's route cap). Inflatable bathtub (small pack) PAC São Luís R$29,45.
- ANTT Resolução nº 6.084/2026 (Tabela A, carga lotação, carga geral) `https://anttlegis.antt.gov.br/action/ActionDatalegis.php?acao=abrirTextoAto&tipo=RES&numeroAto=00006084&seqAto=000&valorAno=2026&orgao=DG%2FANTT%2FMT&cod_modulo=623&cod_menu=9230`
  — CCD R$/km **3,9826 (2 eixos) · 5,0977 (3) · 6,6718 (5) · 7,3547 (6)**; CC **R$451,84 · 541,86 · 657,56 · 671,93**.
  Formula piso = d × CCD + CC (Res. 6.076/2026 art. 5 §1, same site, numeroAto=00006076). Tolls excluded
  (vale-pedágio separate — amount UNVERIFIED).
- Road distances from São Paulo, OSRM `https://router.project-osrm.org/route/v1/driving/...`: BH 584 km · Montes Claros
  984 · Arinos 1.135 · Taiobeiras 1.242 · Salvador 1.964 · Teresina 2.645 · Belém 2.866 · Icatu 2.974 · São Luís 2.985 ·
  Serrano do Maranhão 2.998 · Fortaleza 3.126.
- ANTT floor per truck (computed): SP→Icatu 2 eixos R$12.296 · 3 eixos R$15.702 · 6 eixos R$22.545; SP→Montes Claros
  R$4.371 / 5.558 / 7.909; SP→Fortaleza R$12.901 / 16.477 / 23.663.

## E. What did not work / not found
- No TCE-AM, TCE-MA, CGU or MP finding specifically on a **kit/enxoval** tender was found (searched: kit enxoval /
  kits maternidade / kit natalidade + fraude / superfaturamento / TCE / operação). The corruption evidence is
  circumstantial (process red flags + a documented pattern at the same buyer), not a ruling on the kit lot.
- Correios legacy webservice `ws.correios.com.br/calculador` → 503. Emilio.com.br, Suprimais (Nuvemshop) and the
  Pernambuco Agreste wholesalers publish no freight or price API usable without a session. Truck useful volumes
  (30 / 48 / 95 m³) are UNVERIFIED assumptions.
