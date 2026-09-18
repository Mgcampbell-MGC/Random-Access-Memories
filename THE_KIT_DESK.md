# THE KIT DESK — the ground-up rebuild, 18 September 2026

**Supersedes `THE_KIT_REMEASUREMENT.md` (same day, earlier) and the kit sections of
`THE_ACOLHE_ASSESSMENT.md` and `THE_KIT_BUSINESS_BUILD.md`. Everything below is re-measured under the
corrected method, and three of my own numbers from this morning are corrected in it.**

---

## 0. The business in six sentences

She registers a São Paulo **ME on Simples Anexo I**, free on five procurement platforms. A cron reads
`Lei 14.133 art. 54` publications on PNCP every morning — the statute compels every município in Brazil to
publish what it is about to buy, before it buys it — and filters ~4 newborn-kit tenders a working day down
to the ones she can win at a margin. She buys the components from São Paulo wholesalers in the Brás, either
drop-shipped under *venda à ordem* or assembled into kits, and ships to the município's own address.
The state pays 20–30 working days after attesting the delivery. **She never originates a single unit of
demand: the buyer is legally obliged to announce itself, and the next order arrives whether or not she
does anything.** The whole company is a parser, a supplier account, and a bank balance.

**Target: R$360.000 of billings, ~52% gross, ≈R$146.000 net ≈ US$2.340/month — about 21 won editais a year,
which is 2,1% of the 979 published.** The stretch case, with a supplier account, is R$664.000 and
US$4.750/month.

---

## 1. Why this candidate and not the other 130

It is the only candidate in this archive that passes all four of the founder's own revealed screens at once:

| screen | how it was learned | kit desk |
|---|---|---|
| **THE MACHINE TEST** — a machine makes the unit, the buyer verifies without trusting her, no relationship to hold | REVEALED (she picked 3 of 10) | a parser makes the bid; the state judges on `Menor preço` against a written spec; the contract ends on delivery |
| **ORIGINATION ONCE VS FOREVER** — after the first yes, does demand arrive by itself? | REVEALED (she cut 3 of 6) | `art. 54` publishes every tender in the country, free, forever |
| **C1** — no daily phone-sales operation | stated | 96,4% of kit lines are judged on price alone; the disputa is a robot auction |
| **C2/C3/C4** — faceless, no employees, no credentials held | stated | she is a CNPJ in a bid file; suppliers and carriers are vendors, not contractors |

And it is the only one where **distribution is a statute**. This archive's own summary of seventeen S3
candidates: *"not one died on economics — all died on distribution."*

---

## 2. The market, measured

Twelve months to 18 Sep 2026, PNCP award records, **deduplicated (432 shadow rows dropped), with the Mato
Grosso school-uniform programme excluded** (4.052 rows / R$155,7M that a keyword harvest sweeps in — see
`DEDUPLICATE, AND CHECK YOU HARVESTED ONE PROGRAMME`):

| | |
|---|---|
| homologated value | **R$57.201.985** *(independent earlier count: R$59,1M — 3% apart)* |
| editais | **1.012** — 979 municipal · 6 estadual · 3 consórcio · **0 federal** |
| distinct buying municípios | **699** |
| publication rate | **~4,0 kit editais per working day** |
| median homologated per edital | **R$31.080** |
| median notice before close | **10 working days**, 98,1% ≥5, 0 under 3 |
| judged on `Menor preço` | **96,4%** of lines |
| award ÷ estimate | **median 0,75–0,80 in every band** *(p10 0,37 · p25 0,52 · p75 0,99)* |

⚠ **Three deflations that belong with that number and are not negotiable:** most of it is **SRP**, so
`valorTotalHomologado` is a *registered ceiling, not a sale* (the contract rail shows R$54,2M actually
contracted); some large state programmes are **not on PNCP at all** (Paraná's *Nascer Bem*, and the R$18,98M
*Kit Maternidade Mãe Gaúcha* has a contract but no matching edital); and 25% of kit tenders are invisible to
a title search, reachable only by descending to `/itens`.

---

## 3. THE FINDING — the biggest pocket in the market had never been priced

`THE_KIT_REMEASUREMENT.md`, written this morning, measured **component families only** and concluded the
market failed its bar by 2,2×. It never priced the **assembled kit**, and the assembled kit is
**R$11.110.510 — 19,4% of the market — at a median of R$288,00 a kit.**

**And the reason it matters is who wins it:**

| band | value | ME/EPP share by value | "Demais" share | winners | median winner-year |
|---|---|---|---|---|---|
| **assembled kits R$80–600** | R$11.110.510 | **75,1%** | **15,7%** | 91 | **R$60.520** |
| three "live" components | R$5.048.731 | 60,8% | 27,8% | 245 | R$6.760 |
| **body + macacão** | R$11.147.227 | 18,5% | **74,9%** | 150 | R$5.228 |

> ### ★ THE ARCHIVE HAD POINTED HER AT THE GIANTS' BAND AND IGNORED THE SMALL-FIRM BAND.
> **BRINK MOBIL** (capital social R$32.018.254 — the same firm that dominates office supplies) takes
> **R$5,66M of the R$11,1M** body-and-macacão band by itself, with GPADOVANO taking R$1,35M. Those are the
> two families this archive spent the morning measuring and declaring loss-making. **They are loss-making
> because a R$32M-capital manufacturer bids them direct.** Meanwhile the band where three quarters of the
> money goes to ME and EPP firms — the band an ME can actually contest — had no cost basis at all.

### 3.1 Why a bundle clears where its own components do not

**The kit price is set by the bundle; the component medians do not apply inside it.** A body costs R$15,32
in São Paulo and the state's standalone body line medians R$12,66 — **−21%, dead.** Inside a 17-item kit
awarded at R$359,05, that same body is one of seventeen lines and is absorbed. This is the single most
useful structural fact found today, and it is the inverse of `THE CATALOGUE SCISSORS`: the bundle is the
escape, because nobody publishes a price for *"17 specified baby items in one bag."*

### 3.2 The BOM, priced

**Itaquaquecetuba/SP, PE 447/2025, 17 items, estimated R$476,05, won by CONDAFE at R$359,05** (−24,6%).
Full spec pulled from `pncp.gov.br/api/pncp/v1/orgaos/46316600000164/compras/2025/447/itens`.

**Verified at `emilio.com.br` (CONFECCOES EMILIO LTDA, 50.191.584/0001-06, Brás/SP, published CNPJ prices,
no login) — 6 of 17 lines:**

| item | cost | source |
|---|---|---|
| banheira lisa ≥20 L | R$29,71 | Banheira Infantil 24L #BM2123 Monte Libano |
| cobertor infantil | R$12,18 | Manta Baby #88.04.0003 Sul Brasil |
| pagão | R$19,60 | Emilio macacão/conjunto |
| body manga longa | R$15,32 | Emilio body |
| pano de boca | R$8,47 | Pano de Boca Pinte e Borde #580856 Bublim |
| toalha de banho | R$17,47 | Toalha Fralda Muito Mimo #53-35 Minasrey *(cheapest of 13)* |
| **subtotal, 6 of 17** | **R$102,75** | |

**UNVERIFIED — 11 of 17, estimated as a band, not measured: R$66,60–127,00.** The largest and worst of them:
**the mochila, which Emilio does not stock at all** — the single most expensive line in the kit has no
verified São Paulo price anywhere in this archive.

| | BOM | gross at R$359,05 |
|---|---|---|
| best case | R$169,35 | **+52,8%** |
| worst case | R$229,75 | **+36,0%** |
| needed for 50% | ≤R$179,53 | |

⇒ **An assembled kit is +36% to +53% at the published São Paulo retail tier, and clears 50% at a
30% supplier discount — not the 45% the component families need.** The cliff this morning's Step 0 found
between 30% and 45% is a property of components, not of the business.

---

## 4. The corrected component table

Spec-controlled on **material, size, capacity and brand grade**, pieces-normalised, lot-total rows dropped,
`MIL`/`CENTO` handled, 12 months, against verified São Paulo costs:

| family | n | 12-mo value | median/piece | cost | gross | clears ≥50% |
|---|---|---|---|---|---|---|
| **FRALDA PANO** | 105 | R$525.524 | R$12,20 | R$2,452 | **+79,9%** | R$430.356 |
| **MANTA** *(named manta only)* | 139 | R$910.918 | R$20,05 | R$12,18 | **+39,3%** | R$418.330 |
| TOALHA BANHO | 193 | R$2.012.761 | R$21,00 | R$17,47 | +16,8% | R$179.723 |
| **BANHEIRA** *(conforming cost)* | 259 | R$3.572.825 | R$29,70 | R$29,71 | **−0,0%** | R$1.005.721 |
| COBERTOR *(named cobertor)* | 26 | R$190.286 | R$19,92 | R$21,47 | −7,8% | R$0 |
| MACACÃO/PAGÃO | 261 | R$6.824.022 | R$19,50 | R$19,60 | −0,5% | R$972.001 |
| BODY | 235 | R$4.186.297 | R$12,66 | R$15,32 | −21,0% | *see §4.2* |

### 4.1 ⚠ CORRECTION TO MY OWN STEP 0, SAME DAY — the banheira cost was a non-conforming bathtub

Step 0 priced banheira at **R$22,90** and reported **+22,9% at the median and +49,9% in the large band**.
That item is a **Banheira Sensitive Feminino 17,2 L #13357 (Plasutil)** — the cheapest of 24 on the page and
**the smallest**. Spec-controlled on stated capacity:

| capacity stated | n | value | median award | gross @R$22,90 | gross @R$29,71 |
|---|---|---|---|---|---|
| <20 L | **1** | R$1.670 | R$33,40 | +31,4% | +11,0% |
| **20–25 L** | **115** | **R$1.038.317** | R$26,19 | +12,6% | **−13,4%** |
| 26+ L | 15 | R$98.200 | R$40,85 | +43,9% | +27,3% |
| none stated | 128 | R$2.434.638 | R$33,61 | +31,9% | +11,6% |

**The 17,2 L bathtub conforms to exactly ONE line in the country.** At the cheapest *conforming* cost
(R$29,71, 24 L) the largest capacity-specified band is **−13,4%**. ⇒ **BANHEIRA IS NOT A LIVE FAMILY.**
*(`A PDM IS NOT A PRODUCT` firing on my own kit numbers, twelve hours after I wrote the law. Step 0 applied
the lot-total filter and the piece normaliser and did NOT apply spec control — it was half-corrected.)*

### 4.2 ⚠ AND BODY'S "R$1,08M CLEARING 50%" WAS A CLASSIFICATION ERROR, ALSO MINE

Of the 15 body lines clearing 50%, the two largest — **R$594.368 and R$384.120, both Taiobeiras/MG** — are
*"CONJUNTO BODY + BERMUDA"* and *"CONJUNTO BODY + CALÇA"*: **two-piece sets**, swept into BODY by a `\bBODY`
regex. Their cost basis is two garments, not one. Genuine single-body lines clearing 50% total ≈R$77k, not
R$1,08M. **Fixed by excluding `CONJUNTO|\+\s*(BERMUDA|CALÇA|SHORT)` from the BODY family.**

---

## 5. ⚠⚠ THE CONCENTRATION — and it is the most important caveat in this document

After every correction, the pool clearing ≥50% gross at the published tier is **R$4.380.049** across
**147 municípios**. But:

| município | clearing value | share |
|---|---|---|
| **Coari/AM** | **R$1.522.728** | **34,8%** |
| Aracaju/SE | R$200.000 | 4,6% |
| Piumhi/MG | R$194.962 | 4,5% |
| Arinos/MG | R$170.769 | 3,9% |
| Serrano do Maranhão/MA | R$166.500 | 3,8% |
| | **top 10 = 63,4%** | |

**ONE MUNICÍPIO IS A THIRD OF THE ENTIRE CLEARING POOL** — two lines from one tender: a banheira anatômica
at **R$62,70** against a R$29,71 cost, and a macacão de soft at **R$43,00** against R$19,60, 12.960 units
each. That is `THE CLEARING PRICE IS SET BY WHO BOTHERED TO BID` in its most extreme observed form, and it
means **this morning's UF table — which crowned Amazonas at a 40,9% median — was crowning one buyer.**

⇒ **Every number in this document is also reported ex-Coari. Plan on the ex-Coari figure; treat a Coari
repeat as upside.**

---

## 6. The arithmetic that decides everything

### 6.1 The pool, and the share she must take

| supplier account | pool clearing ≥50% | ex-Coari | share for R$360k | share for R$664k *(ex-Coari)* |
|---|---|---|---|---|
| **none (published tier)** | R$4,38M–8,28M | **R$2,86M–6,76M** | 4,3–8,2% | **23,2%** |
| 20% | R$6,97M–12,04M | R$5,45M–10,52M | 3,0–5,2% | **12,2%** |
| 30% | R$11,44M–13,94M | R$9,52M–12,03M | 2,6–3,1% | **7,0%** |
| 45% | R$16,74M–18,12M | R$14,82M–16,21M | 2,0–2,2% | **4,5%** |

`THE MARKET-MULTIPLE RULE` permits a greenfield entrant 15–25%, exceptionally 30–40%.

> ### ⇒ THE BAR IS CLEARED AT THE PUBLISHED TIER, WITH NO SUPPLIER ACCOUNT AT ALL, ON THE WORST-CASE BOM,
> ### EXCLUDING COARI: 8,2% share for R$360k of billings. The stretch case (US$4.750/month) needs 23,2%
> ### — the top edge of the band — and a 20% account brings it to 12,2%, comfortable.

**This is the finding that reverses Step 0's verdict.** Step 0 said the market failed by 2,2× and cleared
only at a 45% discount. It said that because it measured the 19% of the market where ME/EPPs win at zero
and priced a bathtub that conforms to one line in Brazil.

### 6.2 The balance sheet — how many lots she can hold at once

One median municipal kit edital is **R$31.080**; the cycle order → deliver → ateste → paid is ≈45 days.

| | COGS/lot | float | supplier terms | cash held/lot | **concurrent lots** | lots/yr | billings/yr |
|---|---|---|---|---|---|---|---|
| 48% gross | R$16.162 | R$15.600 | **none** | R$16.162 | **1,0** | 7,8 | R$243.000 |
| 52% gross | R$14.918 | R$15.600 | none | R$14.918 | 1,0 | 8,5 | R$263.611 |
| 52% gross | R$14.918 | R$15.600 | **28d** | R$5.636 | **2,8** | 22,5 | **R$697.794** |
| 52% gross | R$14.918 | +R$20k credit | none | R$14.918 | 2,4 | 19,4 | R$601.574 |

**With her own R$15.600 and no supplier terms she can hold exactly ONE median edital at a time**, capping
her at ~R$263k of billings whatever the win rate. **28-day terms buy more concurrent capacity (2,8) than
R$20.000 of borrowed money (2,4), and cost nothing.** FGI PEAC — the only Brazilian instrument whose
published eligibility a company with no history passes (BNDES FAQ Q4/Q11: no minimum revenue, no minimum
time in business, guarantees waived) — is worth **R$15–20k once and no more**; above ~R$35k of float,
capital stops binding and win count binds. Cost at the only published unsecured anchor (BizCapital CET
2,91–6,60% a.m.): **R$8.218–23.064/yr on R$20.000**. No FGI PEAC agent publishes a rate — **UNVERIFIED**.

### 6.3 Wins and hours

| avg won line | wins/yr | wins/mo | at 5% win rate | h/month |
|---|---|---|---|---|
| R$6.000 | 111 | 9,2 | 2.213 bids | **138 — OVER the 87 h ceiling** |
| **R$31.080** | **21** | **1,8** | 427 bids | **36 — comfortable** |
| R$58.475 | 11 | 0,9 | 227 bids | 21 |

**Lot size is the risk control on a win rate nobody can measure.** PNCP publishes only the winner —
`/propostas`, `/lances`, `/classificacao`, `/fornecedores`, `/participantes` all 404 — so the win rate is
structurally unknowable in advance. At the kit lot size it stops mattering: even 5% fits in her hours.

**21 won editais is 2,1% of the 979 published.** Both measured multi-UF operators already exceed it:
**CONDAFE 44 editais/yr (R$6.135.997, São Paulo EPP, 15 UFs)** and **AMA COMERCIO 38 editais / 16 UFs**.

---

## 7. Who she is competing with — named, not assumed

**The seat is not vacant and the pitch must never say it is.** ~36 firms operate multi-state.
**92,2% of 451 winners are single-UF by headcount, while the 7,8% multi-UF firms take 33,6% of the value.**

| firm | CNPJ | porte | reach | 12-mo |
|---|---|---|---|---|
| **CONDAFE COMERCIO DE ROUPAS** | 10.430.444/0001-10 | EPP, São Paulo/SP | 15 UFs, 36 municípios, 44 editais | **R$6.135.997** — and R$2,44M of the assembled band alone |
| AMA COMERCIO E SERVICOS | — | EPP | 16 UFs, 38 editais | — |
| DEBECHE + HIGI TEX | — | ME | 14 and 9 UFs — **same operation** (both publish `roberto.daud@uol.com.br`) | — |
| J.J.A. ENXOVAIS | — | ME, registered **17 Jan 2024** | MG, MS, PR, SP | — |

**The model is PROVEN, NOT VACANT** — which is a better fact than white space, because the playbook is
observable. CONDAFE is a São Paulo EPP shipping to 15 states: **exactly the arbitrage below.** And a
**two-year-old ME is already winning in four states**, which is the proof a new entrant can enter.

**And 78,5% of winners win exactly ONE edital a year**, median winner-year R$22.474 — a long tail of
one-shot local firms with a small professional head. The target sits inside the head, below CONDAFE.

---

## 8. The arbitrage: buy in São Paulo, never sell there

| UF | clearing value | share |
|---|---|---|
| **AM** | R$1.528.403 | 34,9% ⚠ *almost entirely Coari* |
| **MG** | R$631.960 | 14,4% |
| **MA** | R$443.073 | 10,1% |
| MT | R$261.807 | 6,0% |
| SE | R$234.043 | 5,3% |
| PE | R$221.112 | 5,0% |
| SP | R$199.747 | 4,6% |
| CE | R$139.337 | 3,2% |

**BID: MG · MA · PE · SE · CE · BA · PA · RN, and AM opportunistically.
DE-PRIORITISE: SP, ES, MT, MS.** São Paulo has the most kit lines in the country and the worst margins —
she buys there and must not sell there, which is precisely what CONDAFE does.

⚠ **The gradient is a COMPETITION gradient, not a cost one, and this file once overstated it ~5×** (it
recorded Bahia at +111% to +557%; measured cleanly on a spec-controlled commodity, BA is **−8,4%**).
**Bid thin fields, not far ones.**

**The supply side genuinely is São Paulo-only, and it is arithmetic:** `LC 123 art. 13 §1 XIII (h)` charges
a Simples optante the internal-minus-interstate difference — SP internal 18% vs interstate-into-SP 12% =
**~6 points**. An out-of-state supplier must beat a São Paulo one by more than 6%. *(And ICMS-ST on
papelaria in SP was revoked 1 Jul 2026 by Portaria SRE-09/26; the textile/puericultura position needs the
accountant's confirmation — see §12.)*

---

## 9. The parser IS the business — eleven admission rules

There is no pricing skill that rescues a lot she should not have entered. Each rule below has a measured
price tag.

1. **REJECT every `LOTE ÚNICO`.** Per-item municipal lines clear at 97–100% of estimate; lote único lines
   clear at **36–63%**, and two awarded pencils below the wholesale floor. Detect with `^\s*LOTE`. Costs 15%
   of the funnel, saves 100% of the losses.
2. **REJECT any atestado clause carrying a NUMBER** (a percentage or quantity). A *qualitative* atestado is
   satisfied by **one prior sale of any size** and must NOT be rejected — that filter, as originally written,
   would have discarded most of the market. Measured on five live editais: 1 quantitative, 2 qualitative,
   2 none at all.
3. **REJECT `CONFORME MODELO DO ÓRGÃO`** — custom spec.
4. **REJECT assembled-kit lots over ~18 items** — and price every kit from its BOM, never from a per-item
   rule of thumb.
5. **DROP rows outside a plausible unit-price window per SKU before computing any median** — buyers type the
   lot total into `precoUnitario` with `quantidade = 1`. On one PDM this was 126 of 1.934 rows and R$2,33M of
   phantom value, landing in the smallest quantity band by construction.
6. **NORMALISE to pieces**: `quantidade × capacidadeUnidadeFornecimento`, `C`/`CENTO` = 100,
   **`MIL`/`MILHEIRO` = 1000**, and regex the pack count out of the free-text description
   (*"FRALDA COM BAINHA - 3 UNIDADES"*) — PNCP items carry no capacity field.
7. **SPEC-CONTROL on material, size, capacity and brand grade before believing any margin.** The banheira
   error in §4.1 is worth 36 margin points.
8. **CHECK `LC 123 art. 48 I`**: items **≤R$80.000 are reserved exclusively to ME/EPP**. It is **per item,
   not per tender** — one live ARP had 9 of 38 lines under the threshold and all 38 flagged `Sem benefício`.
   The impugnação is free, written and statutory.
9. **SCREEN THE BUYER'S PAYMENT RECORD** — §10.
10. **GREP the pagamento clause for `Decreto Municipal`** and extract the two deadlines. There is no national
    figure to assume: `IN SEGES/ME 77/2022` is **federal only** (art. 1º), reaching a município only for
    *transferências voluntárias* (art. 2º), and the kit market is 97% municipal. Paracatu/MG quotes its own
    Decreto 7.088/2024: 5 + 15 working days ≈ 28 calendar days.
11. **GREP for `pagamento antecipado`** — `art. 145` permits it only where expressly in the edital. Rare, and
    where it appears the working-capital problem is zero.

**And instrument the log from day one** — date, PDM, spec, quantity band, her cost, her bid, result, and the
winning price when she loses. **PNCP never publishes who lost, so her own bid log is the only asset in this
plan that compounds and cannot be bought.** It is also the reason no vendor can build this: eleven inspected
competitors sell historical *award* prices; **none has a cost input, because her cost is her own invoice.**

---

## 10. Buyer selection is worth more than any price advantage she could engineer

Three independent rails found this same law, which is why it is load-bearing.

**The screen is free, national, keyless, one GET per buyer:**
```
apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio=2026&nr_periodo=3
  &co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2007&co_esfera=M&id_ente={cod_ibge}
```
It returns *restos a pagar processados* — invoices already delivered, attested, liquidated and **unpaid**.
The CNPJ↔IBGE join is free at `/siconfi/tt/entes` and **matched 699 of 699 kit-buying municípios.**

Measured on 148 of the 200 largest: **median 76,7% paid, p25 44,9%, p10 23,5%** ⇒ 43,2% still owed >30% of
the prior year's liquidated invoices at mid-year, 29,1% owed >50%. But **only 6,1% wrote off more than 5%,
so the risk is DELAY, NOT DEFAULT.** Named and live: **Nhamundá/AM paid 0,0% and published a R$2,12M kit
tender**; Icatu/MA 0,0% on R$1,09M. Against Pinheiro/MA, Bertioga/SP and Colíder/MT at 100%.

**Rule: reject where `saldo ÷ inscritos > 0,30` or `cancelados > 2%`.** Back it with RGF Anexo 05 for
*Disponibilidade de Caixa Líquida*.

⚠ **This is no longer proprietary.** SIGA Pregão ships *"Pagômetro: avalie a capacidade de pagamento do
órgão antes de disputar"* on its Ultra plan at **12× R$389,42**. She gets it free; she does not get to call
it a moat.

---

## 11. The vehicle and the fiscal setup

- **ME/EPP on Simples Anexo I.** Effective rate **4,00% at RBT12 R$180k · 5,65% at R$360k · 6,73% at R$500k ·
  7,58% at R$720k**. **MEI is arithmetically dead** — the ceiling is still R$81.000 (LC 123 art. 18-A §1º;
  LC 227/2026 did not touch it), and Resolução CGSN 140/2018 Anexo XI contains *"ATACADISTA"* zero times.
- **Capital social R$20–30.000 integralizado.** Her own money, not a fee. It caps the maximum an edital may
  lawfully demand under `art. 69 §4º` and makes the opening balance sheet clear LG/LC/SG > 1.
- **The two feared habilitação blockers are not blockers.** `Decreto 8.538/2015 art. 3º`: no balanço
  patrimonial may be demanded of an ME/EPP for *bens para pronta entrega*. `Lei 14.133 art. 65 §1º`: a company
  created in the year of the licitação substitutes a **balanço de abertura**. `art. 69 §2º`: *"é vedada a
  exigência de valores mínimos de faturamento anterior."* Measured: **0 of 5 live kit editais demanded capital
  social, PL mínimo, garantia de proposta or garantia de execução.**
- **File the IN RFB 1.234/2012 Anexo IV declaration with every contracting body.** IN RFB 2.145/2023 inserted
  art. 2º-A obliging municípios to withhold IRRF on goods; the carve-out is art. 4º XI (Simples) and art. 6º
  requires the declaration **per contract**. *(That art. 4º XI reaches art. 2º-A is **UNVERIFIED** — no COSIT
  ruling squarely on it. File it in every case regardless.)*
- **Put the empenho number on the face of the nota fiscal.** A wrong NF restarts the whole cash cycle.
- **Five free registrations** — Compras.gov.br/SICAF · Portal de Compras Públicas · BLL · BNC · Licitanet —
  reach **74,3%** of open kit tenders; eight reach 82,9%. `art. 87 §2º` prohibits a município demanding its
  own complementary cadastro. Bid fees ≈R$75 weighted; **R$0 on Compras.gov.br, and BLL charges 1,5% capped
  R$600 ONLY IF SHE WINS.**
- **Levers only an ME/EPP holds:** `art. 141 §1º II` lets the chronological payment queue be jumped for an
  ME/EPP on demonstrated risk of discontinuity; `art. 141 §3º` makes every body publish its payment queue
  monthly; `art. 137 §2º` gives the right to terminate on *atraso superior a 2 meses*.

---

## 12. What is NOT verified — the honest list

**Nothing in this section is a reason not to start. Every item is a reason not to scale past step 2 until it
returns.**

1. **11 of 17 BOM lines have no verified São Paulo price**, and the worst gap is the **mochila — the most
   expensive item in the kit, which her one verified supplier does not stock.** The BOM band
   R$169,35–229,75 is 45% estimate by value. **This is the single largest uncertainty in the document and it
   is closed by one afternoon of catalogue work.**
2. **The 30%/45% supplier discount is an INFERENCE, not a quote** — derived backwards (Chamex published
   R$30,60, the state pays R$19,83, so winners are invoiced at ~R$16–18). **Nobody has been asked.**
3. **FREIGHT ON BULKY GOODS IS UNQUOTED AND IS THE MOST LIKELY UNPRICED COST.** The measured freight study
   was run on **paper** (3,6 kg, dense). A 24 L banheira is ~0,5 kg actual and ships at **dimensional
   weight**; an assembled kit is low-density by construction. Correios hard-caps a parcel at ~29 kg and
   **every B2B road carrier — Braspress, Jadlog, TNT, Total Express, Melhor Envio, SuperFrete, Kangu —
   refuses to quote without a contract.** At 3.750 kits this is a truckload, not parcels. ⚠ And the edital
   settles that she eats it: Riachão do Bacamarte/PB cl. 9.8 — *"Não será admitida a previsão de preços
   diferentes em decorrência do local de entrega"*, with *frete*, *CIF* and *FOB* appearing **zero times in
   43 pages**.
4. **The win rate is structurally unmeasurable** before operating. It can only be bounded.
5. **Coari/AM is 34,8% of the clearing pool** (§5) and may not repeat.
6. **The ICMS position after the 1 Jul 2026 ST revocation is net-uncomputed** for this category, and
   **substituição tributária on interstate purchases into a Simples ME** is an unbudgeted line the
   wholesalers warn about on their own product pages. **STF ADI 5464** suspended the EC 87/2015 DIFAL for
   Simples senders — **UNVERIFIED as applied.**
7. **Whether SUAS fundo-a-fundo transfers count as *transferências voluntárias*** under IN 77/2022 art. 2º —
   if they do, a large slice of kit buyers falls back under the faster federal 5+5 clock. **UNVERIFIED**,
   worth an hour.
8. **Mamadeiras and chupetas are certified** under Portaria Inmetro 490/2014 — **keep them out of the SKU
   set.** Textiles need only labelling (Portaria 118/2021); rigid baths are uncertified (Portaria 563/2016
   covers inflatable only).

---

## 13. The sequence, with a bar on every step

| # | step | cost | bar to pass before the next step |
|---|---|---|---|
| **0** | **Price the other 11 BOM lines** at Emilio, Brascol, Yanai and two more Brás sellers. | R$0, one afternoon | **BOM ≤R$200 for the 17-item kit.** Below that, proceed. Above R$230, the assembled band is marginal at the published tier and step 1 becomes mandatory rather than optional. |
| **1** | **Fifteen supplier emails** with a number per SKU: body ≤R$8,40 · macacão ≤R$13,70 · toalha c/capuz ≤R$10,50 · banheira 24 L ≤R$14,85 · manta ≤R$10,00 · **mochila ≤R$25,00**. Ask for faturado price, *venda à ordem*, and first-purchase credit terms — **and read the cadastro page before the price list**. | R$0 | **≥3 of 15 answer with a clearing number.** |
| **2** | **Open the entity**: ME, Simples Anexo I, capital R$20–30k, five free platform registrations, certificado digital. | ~R$1.500 | live on Compras.gov.br |
| **3** | **Build the cron + parser** — PNCP `art. 54` descent, `/itens`, the eleven rules, SICONFI screen, bid log. | ~R$2–4k or her own time on a R$30/mo VPS | 30 days of output, instrumented |
| **4** | **Bid small and local first** — dispensa lines, median R$281, decided in days. **Use the dead channel to mint the qualitative atestado**, which transfers across the whole class. | float only | **one completed delivery + one atestado** |
| **5** | **Scale to assembled kits.** Terms by the second purchase (Flora Saúde: *"avaliado pelo setor financeiro a partir da segunda compra… prazo inicial 21 dias"*). FGI PEAC R$15–20k only if terms do not arrive. | R$15–20k borrowed | **21 wins/yr run-rate** |

**Honest timeline: 12–18 months to US$2.000–2.400/month. With the account and terms inside year one,
US$4.500–5.000 is reachable but needs 23,2% of the ex-Coari published-tier pool, which is the top edge of
what a greenfield entrant should underwrite.**

---

## 14. Kill conditions, written in advance

- **Fewer than 3 of 15 suppliers** answer with a clearing number **and** the step-0 BOM comes in above R$230
  ⇒ the assembled band is marginal and the business is the two-SKU version (fralda pano + manta, R$0,85M
  pool) at well under the bar. **Stop.**
- **Measured win rate below 3%** after 150 logged bids ⇒ 21 wins needs 700 bids, and the funnel does not
  exist at 4 editais a working day.
- **Median buyer payment beyond 60 days** across her first ten wins ⇒ turns halve and the required margin
  rises above what any line clears.
- **A freight quote above ~12% of line revenue** on a bulky assembled kit to the Northeast ⇒ the arbitrage in
  §8 is gone and the business is São Paulo-regional, which is the worst-margin region.
- **Coari does not repeat AND the ex-Coari pool falls below R$2,5M** ⇒ the required share exceeds 25% and
  `THE MARKET-MULTIPLE RULE` fails.

---

## 15. What would make this fail that is nobody's fault

`THE STEADY-STATE KILL` does not apply — there is no subscriber base to decay, and demand is republished by
statute every morning. `THE FREE FRONT DOOR` does not apply — no upstream party earns margin on this flow
and funds the identification layer to zero; the state publishes the tender and nobody gives away the goods.
`THE CATALOGUE SCISSORS` is escaped by the bundle (§3.1). `THE ATTENTION TRILEMMA`, the expert veto,
`THE ONBOARDING LAW` and the platform-arbiter law are all inapplicable.

**What remains is ordinary business risk: a thin margin measured against an incomplete BOM, one buyer worth
a third of the clearing pool, an unquoted freight leg, and a win rate nobody can know until she bids.**
That is a materially better position than any of the other 130 candidates reached, and all four are
measurable inside sixty days for under R$5.000.
