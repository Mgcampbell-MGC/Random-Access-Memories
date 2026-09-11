# FIELDTAG → BRAZIL — 11 Sep 2026. A government-only, zero-inventory reseller, transposed and measured

**The founder supplied FIELDTAG GOV — a US blueprint for a government-only thermal-media reseller (zero
inventory, blind drop-ship from trade-only converters, AI-operated bid/fulfil/invoice loop, 15–30 recurring
contracts, US$50k/month wall target) — and asked: take the best parts, does it work in Brazil, any niche.**
This file answers with the Brazilian state's own purchase records, the statutes, and two named one-person
operators already running the model. Every number below was fetched today by me.

---

## 1. The verdict in one paragraph

**The model transposes, and Brazil is a BETTER host than the US on every rail FIELDTAG has to buy:** the
opportunity feed, the incumbent/price database, the vendor registry and the auto-notification are all free and
statutory; small-value items are reserved by law to micro and small companies; the auction platform ships its
own bid robot; and — three days ago — a federal decree brought into force a government e-commerce catalogue
(**Sicx**) whose supplier reputation score starts at zero for everyone. **Two one-person Brazilian suppliers
already run FIELDTAG's exact niche at R$365k and R$1,78M a year of shipped revenue.** What does NOT transpose is
the US$50k/month wall: at her working capital the honest target is the archive's own bar, and the binding
constraint is cash timing, not demand or automation.

## 2. What FIELDTAG owns that Brazil gives away

| FIELDTAG has to build or buy | Brazil supplies, free, by statute |
|---|---|
| SAM.gov opportunities API + a paid state/local aggregator | **PNCP API** (all levels of government) and `dadosabertos.compras.gov.br` (federal) — open, no key |
| Incumbent rail (who won, at what price) — reconstructed from awards | **Painel de preços**: every homologated line with unit price, quantity, buyer and **the winning supplier's name and CNPJ** |
| Vendor lists so buyers send RFQs | **SICAF** registration → **IN SEGES/ME 67/2021 art. 7: every dispensa is "encaminhado automaticamente aos fornecedores registrados… por mensagem eletrônica"** (verified verbatim) |
| Small-business set-asides with a nonmanufacturer rule to navigate | **LC 123 art. 48 I: items up to R$80.000 are EXCLUSIVE to ME/EPP ("deverá")**; art. 44: an ME/EPP within 10% (5% in pregão) may beat the best price. **No nonmanufacturer rule exists.** |
| Standing price quotations / BPAs | **Sicx — Decreto 13.106/2026, in force 8 Sep 2026**: permanent supplier credentialing via SICAF, offers per locality with tiered prices, **automated ranking with a mandate to "mitigar a concentração de mercado"**, reputation scores for suppliers AND buyers (payment delays count against the buyer), definitive receipt ≤10 days, **payment released on definitive receipt** |
| A bid-bot vendor | **Compras.gov.br's own automatic bidding — IN 73/2022 art. 19** (confidential minimum value, automatic cover bids); third-party robots (Effecti, WaveCode) are lawful |
| Dispensa threshold | **R$65.492,11 per contratação for goods/services in 2026** (Decreto 12.807/2025) |

## 3. The oracle — what the state actually buys from one-person suppliers

- **8.395 homologated lines won by *Empresário Individual* suppliers in 12 days (1–12 Jun 2026), all Brazil ≈
  250.000 a year.** Sampled 3.000: median R$932/line, p75 R$3.895, p90 R$14.949. What they sell (read from
  PNCP): welding electrodes and brush-cutter parts (J. J. Vitalli, 104 lines in 12 days), medicines, school
  food (flour, cheese, eggs), tractor parts and brake shoes, humidity reference standards, coffee and milk,
  stationery. **Goods resale by tiny suppliers is the dominant shape of Brazilian small-value procurement.**
- **FIELDTAG's own niche, federal painel, Sep 2025–Aug 2026, ten CATMAT lines:** R$52,3M/year; 4.733 lines;
  dispensa segment 1.129 lines ≈ R$5,2M. Etiqueta adesiva R$11,3M (1.500 lines, 634 buyers) · pulseira de
  identificação R$15,0M · papel bobinado R$4,9M · ribbon R$4,0M (504 lines, 336 buyers) · bobina papel
  impressora R$3,4M · papel térmico R$2,8M · etiqueta personalizada R$3,3M · bobina senha R$2,3M · fita
  impressora R$1,3M. Person-named winners 7–19% of lines. Biggest buyers: **EBSERH hospitals, the Army, the
  Navy, state health secretariats.**
- **Two named one-person operators, sized from PNCP results (12 months):**
  - **P H P DE FREITAS RODRIGUES** (CNPJ 38.261.300/0001-05, ME, *Empresário Individual*): **196 lines,
    R$1.782.432, median R$4.189/line, max R$158.700**, five-plus states. #1 winner of etiqueta adesiva (66) and
    etiqueta auto-adesiva (52). Sells a 110×74 wax ribbon to UNESP at R$24,15 and 2.000 thermal rolls to
    EBSERH at R$4,70.
  - **ALMIR GUERIERI** (CNPJ 22.400.151/0001-70, ME, *Empresário Individual*): **104 lines, R$365.194, median
    R$1.790/line**, 52 of 104 in São Paulo. #1 federal ribbon seller (54 lines); in the top five of five of the
    ten thermal-media lines. Sells ribbon at R$7,67–14,20.
  - **Both win almost entirely by PREGÃO (68/76 and 126/129 lines), not dispensa** — the volume is in the
    electronic auctions, which the platform's own robot bids in.
- **Margin, measured against retail:** government pays a **median R$11,84** for a 110×74 ribbon (p25 R$6,70,
  p75 R$30,00; n=128) against **Kalunga retail R$20,50 per 4-pack ≈ R$5,12/unit**; thermal roll 80×40
  government R$4,70 (P H P to EBSERH) against Kalunga R$3,99–4,79 retail per roll in a 10-box. **Wholesale sits
  below retail, so the observed spread is 30–70% gross on ribbons and thin on plain rolls — FIELDTAG's 15–18%
  is conservative for the specified-item lines and optimistic for commodity paper.**

## 4. Run the archive's screens on it

| Screen | Result |
|---|---|
| `THE MACHINE TEST` (revealed) | **Passes all three limbs**: the unit is made by the converter and shipped by them; the buyer verifies by receipt against a spec they wrote; a purchase order is not a relationship. |
| G2 buyer pushed to her | **Yes, by statute** — art. 7 emails; Sicx ranking; LC 123 exclusivity. |
| `THE CATALOGUE SCISSORS` | **Fires, and it is the price mechanism, not a kill**: these are catalogue items, so margin is price discipline plus a specified SKU the generalists misprice (p25–p75 spread of 4,5× on one ribbon). |
| `THE FREE FRONT DOOR` | **The manufacturers do not serve this**: of the top winners, converters (Bobmax, Inlabel, MNX) appear, but so do individuals — the small-lot, multi-address, multi-state fulfilment is exactly what a factory will not do for R$1.790. |
| `THE REPLACEMENT-COST CEILING` | Real. No moat beyond reputation, records and terms — FIELDTAG's own "partial moat" admission. **Sicx converts the reputation half into a measured, ranked asset that starts at zero for everyone on 8 Sep 2026 — a CLOCK-START, the only level moment the archive recognises.** |
| `INVOICE, DON'T CHECKOUT` | Government pays by bank transfer against a nota fiscal. No card. |
| Tax | Simples Nacional Anexo I (commerce): **4% of gross up to R$180k/yr, 7,3% to R$360k** (LC 123 Anexo I, current table). ICMS-ST may load some purchases — UNVERIFIED for paper products by state. |
| C2 / expert veto | No face, no name on the product, no claim. A CNPJ and a SICAF record. |
| `THE ONBOARDING LAW` | SICAF registration is written; portals are written; the Sicx credentialing is electronic. |
| **C5 — the one that binds** | **Working capital.** The state pays after *recebimento definitivo* (≤10 days on Sicx, in practice 10–45 days after delivery elsewhere; municipalities later). A new ME gets no supplier credit. **With R$15.600 she can carry ~R$10–12k of goods in flight — i.e. R$10–12k/month of shipped revenue at first, ≈ R$1.500–3.000 of gross margin.** Growth is capped by cash, not by demand. |
| `THE STEADY-STATE KILL` | Does not apply — per-order, no subscription base to decay. |
| C9 hours | Per order: read the notice, price, bid (robot), issue the supplier PO, emit the NF-e, track, invoice, collect. Automatable to ~20–30 min/order; Almir's 104 lines/year ≈ 9/month ≈ 3–5 h/month once templated. **Fits.** |

## 5. The Brazilian version, built

**A SICAF-registered ME (not MEI — the R$81k MEI ceiling is below the bar) that sells a narrow catalogue of
specified consumables to federal buyers in São Paulo state first, by pregão and dispensa, drop-shipped from
two converters, and that registers on Sicx on the day its first edital de credenciamento opens.**

- **Niche selection is data, not taste.** The painel gives, for every CATMAT line: the annual volume, the
  dispensa share, the buyer names, the winners and their prices. Pick lines where (a) person-named suppliers
  already win ≥10% of lines, (b) the p75/p25 unit-price spread exceeds 2× (mispriced specs), (c) buyers are
  federal (pay on time) and concentrated (EBSERH, Army, universities), (d) the item is dry, light and
  non-perishable. Thermal media passes all four; so do several of the individuals' niches above (welding
  consumables, machine parts, lab reference standards). **Run the same four filters on any PDM in an afternoon.**
- **The Golden Passport transposes as-is**: one record per CATMAT item — exact spec, printer, converter SKU,
  backup, price ladder, freight by UF, last three homologated prices from the painel.
- **Distribution is the state's job**: SICAF lines of supply → art. 7 emails; pregão alerts from PNCP; Sicx
  offers per locality once live.
- **The machine**: PNCP/painel pull → passport match → cost → bid via the platform's own robot (IN 73/2022 art.
  19) → PO to converter → NF-e → delivery evidence → cobrança. She reviews exceptions.
- **Arithmetic at her cash**: month 1–6, R$10–15k/month shipped at 20–30% gross on specified lines ⇒
  **R$2.000–4.500/month gross margin** — below the bar. The bar (R$12.300–15.400 gross domestic; here margin,
  not revenue, is what she keeps, so ≈ **R$50–75k/month shipped at 20–25%**) needs **R$40–60k of goods in
  flight**, i.e. supplier terms (net 30 from a converter after a clean history) or R$40k of capital. **Almir
  runs at R$30k/month shipped; P H P at R$148k/month.** She lands between them in year two only if a converter
  extends credit.

## 6. Kills that did NOT fire, and one that must be watched

- **Speech:** none. Everything is written, including disputes (portal).
- **Expert veto / C2:** none.
- **Platform ToS:** the government platforms are the ones inviting the robot.
- **⚠ Sicx timing:** rules in force 8 Sep 2026; **platform, complementary norms and the first editais de
  credenciamento are not yet published** (Effecti, Mattos Filho, Conjur, all 25–28 Aug 2026). The clock has
  started for the *law*, not yet for the *catalogue*. Build on the existing rail now; be credentialed on day one.
- **⚠ Payment reality:** Lei 14.133 art. 141 orders payments chronologically and lets ME/EPP/MEI be prioritised
  only on a showing of risk of discontinuity. Federal bodies (EBSERH, Army, universities) are the ones to sell
  to; municipal receivables are the ones to refuse until there is a cushion.

## 7. What this changes in the archive

- **`S2 IS CLOSED` was written about a *pessoa física* reselling FOREIGN goods with PIS/COFINS on gross and US
  sales tax on cost.** A Brazilian ME reselling DOMESTIC goods to the Brazilian state under Simples is a
  different animal: 4–7,3% on gross, no import, no card, no foreign insurance. **S2 reopens for ONE cell —
  domestic goods, public buyer, Simples entity — and the two named operators are the proof.**
- **The dispensa oracle is now a standing tool**: any candidate that sells a GOOD to the state can be sized,
  priced and benchmarked against named competitors in thirty minutes from `dadosabertos.compras.gov.br`.

Sources fetched today: `planalto.gov.br` (Lei 14.133 arts. 4, 75, 141; Decreto 12.807/2025 anexo; Lei
15.266/2025; Decreto 13.106/2026 arts. 2–33; LC 123 arts. 44–48, Anexo I), `gov.br/compras` (IN 67/2021 art.
7), `dadosabertos.compras.gov.br` (modulo-pesquisa-preco, modulo-contratacoes, modulo-material),
`pncp.gov.br/api`, `kalunga.com.br`, plus Effecti/Mattos Filho/Conjur notes on Sicx status (secondary).

---

## 8. "Factoring takes care of this" — measured, 11 Sep 2026

**Half right, and the half that is right is bigger than the founder's version of it.** The federal government
runs the factoring itself: **AntecipaGov** (`antecipagov.comprasnet.gov.br`, MGI/SEGES), free to the supplier,
banks and fintechs credentialed by edital (Edital 7/2025, Nov 2025), **IN 82/2025 extended it to state and
municipal suppliers** (secondary: gov.br/compras news). Mechanics from the portal's own help page:

- **What is anticipated:** *"contratos ou empenho(s) com força de contrato"* — an active contract or an
  empenho with force of contract; the portal tracks *valores liquidados* (delivered, NF issued) and *a liquidar*.
- **Ceiling:** *"O valor da operação de crédito não poderá exceder a 70% do saldo a receber atualizado."*
- **Repayment:** the UASG pays the bank directly into a blocked linked account (*Termo de Vinculação de
  Domicílio Bancário*). The supplier never touches the money — which is why a NEW company qualifies: the
  bank's counterparty is the federal treasury, not her balance sheet.
- **Cost:** platform fee charged to the institution 0,17–0,42% of the operation (Edital 485/MGI); interest set by
  each institution's proposal — **UNVERIFIED band; private public-receivable factors quote ~1,5–4%/month**.
- **⚠ Speed, from the same page:** UASG review **10 business days** → bank proposals **15** → selection **5** →
  formalisation **20** → bank-account registration **2**. **Up to ~52 business days for a first operation.** It
  is built for CONTRACTS WITH BALANCES (a 12-month ata de registro de preços, a term supply), not for a R$1.790
  dispensa line paid in 30 days.

### What factoring does and does not move — the cycle arithmetic

Monthly shipped capacity ≈ capital in flight × 30 ÷ cycle days (pay converter → cash back).

| Configuration | Cycle days | Capacity on R$12k in flight | Gross margin at 25% |
|---|---|---|---|
| Prepay converter, federal buyer pays day 40–50 | ~45 | ≈ R$8.000/month | ≈ R$2.000 |
| + factoring of the attested NF (advance ~day 15–20) | ~18 | ≈ R$20.000/month | ≈ R$5.000 − ~2% factoring |
| + converter net-30 (after 2–3 clean orders) **and** factoring | ≤ 0 | **capital-free — bounded by supplier credit line, not by her cash** | the whole margin |
| Almir's observed level | — | R$30.000/month shipped | — |
| The bar (≈R$50–60k shipped at 20–25%) | — | needs ≈R$40–60k in flight **or** supplier terms | — |

⇒ **Factoring closes the POST-delivery leg (the state's 30–45 days) and roughly doubles-to-triples capacity. It
does nothing for the PRE-delivery leg — the converter must still be paid before the state has anything to
attest — and that leg is closed only by supplier credit.** The sequence that makes the business capital-free
is therefore: (1) first orders prepaid inside R$12k, small and federal; (2) factor the attested NFs from order
one; (3) convert two or three clean deliveries into net-30 from the converter; (4) move onto term contracts
(atas de registro de preços) where AntecipaGov's 70%-of-balance line finally fits its own timeline. **The
founder's instinct is right on direction; the mechanism that actually removes the cap is the converter's
credit, and factoring is what earns it.**

⚠ **And run the margin test before the cost:** 2–4% a month of revenue is a rounding error on a specified
ribbon at 30–70% gross and fatal on commodity thermal paper at ~8%. Factor the specified lines; never the
commodity ones.
