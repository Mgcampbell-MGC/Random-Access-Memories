# THE EXPEDIENTE DESK

**13 September 2026. The output of the first REPAIR pass ever run in this archive — 21 agents, 8 category
families, 189 PDMs screened, two model families on the second opinion. The founder's instruction that changed
it: *"adversarial pass should lead to a BETTER business not a dead business… not another KILL the idea, but a
better idea."***

**It found a business. The same sweep under a kill brief would have returned eight nulls — and the board agent
proved it, by showing that every family that died, died on a limb measured on the wrong denominator, the wrong
cost basis or the wrong slice.**

*Workflow log: Screening 8 category families against an 8-limb structural screen · limpeza: no survivors · textil: no survivors · copa: no survivors · saude: no survivors · 189 PDMs screened, 6 verified, 3 survived both lenses*

---

I have enough verified ground. Writing the build.

---

# THE EXPEDIENTE DESK — a build

**Verification note first, because two things in the repair pass are wrong and the build changes if you believe them.**

**(1) The "verified São Paulo wholesale" is in Vitória, Espírito Santo.** `publica.cnpj.ws/cnpj/28410074000115` → ATACADO SAO PAULO LTDA, **Vitória/ES**, CNAE 4647-8/01. The lápis lens called it "Verified São Paulo wholesale, self-serve, no account needed" and built its 30,1% margin on it. The pasta lens caught it. **Believe the pasta lens.** Every margin number in this archive priced off that catalogue is an *interstate* price: LC 123 art. 13 §1 XIII h adds ~6 points, and because papelaria goods sit on the RICMS-SP art. 313-Z13 ST list, an interstate purchase without retention triggers art. 426-A antecipação on entry. **There is currently no verified São Paulo wholesale price anywhere in this record.**

**(2) The "R$5–80k band pays +43–78% more" is a product-mix artefact.** I tested it within sub-type and it inverts:

| Sub-type | <R$5k lines | R$5–80k band | Δ |
|---|---|---|---|
| ABA+ELÁSTICO | R$3,40 (n=564) | R$3,14 (n=88) | **−8%** |
| CATÁLOGO | R$13,75 (n=512) | R$13,50 (n=126) | **−2%** |
| SANFONADA | R$19,99 (n=263) | R$18,10 (n=89) | **−9%** |
| SUSPENSA | R$2,70 (n=356) | R$2,66 (n=81) | **−1%** |

The headline premium was expensive sub-types forming bigger lines. The real driver is **quantity**, and it is monotonic and enormous — caneta azul, spec-controlled, n=1.492:

`qty ≤60 → R$6,70 · 60–150 → R$3,19 · 250–450 → R$1,73 · 1.100–2.400 → R$1,04 · 2.400–5.000 → R$0,82 · 5.000–12.000 → R$0,70 · >12.000 → R$0,53`

**A 12,6× spread.** Both lenses' "bid the R$5–80k band" advice is half-right for the wrong reason. The correct rule is a **quantity ceiling, not a value band.**

**(3) What I reproduced exactly**, so the pasta lens can be trusted elsewhere: PDM 20 clean total R$40,81M (they said R$40,78M), dispensa 2,81% by value vs 20,8% by line (they said 2,8%/20,8%), four-state pool R$20,78M = 50,9% (they said R$20,76M/50,9%), catálogo median R$13,73 and tipo-L R$0,85 both exact.

---

## 1. THE BUSINESS

**One Empresário Individual in São Paulo, Simples Anexo I, zero stock, bidding the *whole material-de-expediente basket* per item on Compras.gov.br and PNCP, supplying from two São Paulo wholesalers under venda a ordem.**

Not a pencil business, not a pasta business. **The unit of sale is the edital, not the PDM.** That is the single structural fact the whole build rests on, and it is measured: of 871 tenders that bought pencils, **83,7% bought pens in the same tender** and 78% bought at least two of pen/eraser/clip; the median material-de-expediente edital carries **33 item lines** (p75 62, p90 98). One bid, one nota fiscal, one delivery, one freight.

**The economics, derived and then reconciled against real operators.** I grouped 10.819 pasta+caneta lines into 2.707 editais and measured the value sitting in the positive-margin quantity band (qty ≤2.400) per edital: **median R$1.740, mean R$11.012**. Those two PDMs are 9,5% of class 7510's R$872,5M, so a full basket is ~10,5× that → **≈R$18.235 of addressable content per edital, median**.

R$640.000 of billings ÷ R$18.235 = **35 won baskets a year, 0,7 a week.**

That number is not invented — it lands between the two measured one-person incumbents: **POLLYANA MELO DA SILVA LUSTOSA** (CNPJ 37.722.924/0001-01, Empresário Individual, capital R$80.000) at **30 tenders/year averaging R$35.182 = R$1.055.475**, and **P H P DE FREITAS RODRIGUES** (CNPJ 38.261.300/0001-05, Empresário Individual, capital **R$50.000 — exactly Sol's**) at **79 tenders averaging R$14.073 = R$1.111.800**, who is *also* the R$1,78M/yr thermal-media operator this archive already recorded. One person, R$50.000 of capital, ~R$2,9M/year across two categories.

**Monday-morning shape:**

1. **Register free, five places**, one afternoon: Compras.gov.br/SICAF (reaches 70% of open SP expediente tenders — 14 of 20 measured), then BLL, BNC, Licitanet, Portal de Compras Públicas.
2. **One cron**, PNCP `?q=material de expediente` → descend to `/orgaos/{cnpj}/compras/{ano}/{seq}/itens` on every hit. **Never match on `objetoCompra`** — only 28% of relevant tenders name the contents in the object; the items are the only truth.
3. **Price every line off a live São Paulo wholesale catalogue**, not off the painel estimate. SP estimates run 3–14× the clearing price (Jundiaí est R$2,68 → homologado R$0,19; Piracicaba R$2,80 → R$0,76).
4. **Bid per item. Reject lotes.** Then drop-ship venda a ordem per empenho.

**Honest net.** R$640k billings × 30% gross = R$192k. Less Simples (5,65–7,58%, falling to ~3,7–5,0% once ICMS-ST receita is segregated), less freight ~3%, less accountant/certificates ≈ **R$110–140k/yr = R$9,2–11,7k/month ≈ US$1.770–2.250/month**. That is the *bottom edge* of the bar, and it is the honest answer. **The comfortable number is the incumbents' number: R$1,0–1,1M of billings**, which is 55–75 won baskets a year, not 35.

---

## 2. THE RANKED BOARD

"Addressable pool" = four-state (SP/MG/PR/RJ) + UN lines + qty ≤2.400. That is the band where margin is positive after freight. **I measured it directly for PDM 20 and PDM 99; the rest carry the lápis lens's R$5–80k band figures, flagged, because I did not re-pull them.**

| # | Category (PDM) | Pool (addressable) | Maker share | Margin vs median **award** | Share of pool needed for R$640k | Best sub-segment |
|---|---|---|---|---|---|---|
| 1 | **PASTA ARQUIVO (20)** | **R$4,87M** ✅measured | **3,4%** ✅ | **+29% at retail COGS; ~50% at wholesale** (UNVERIF. wholesale) | **13,2%** ✅ | ABA+ELÁSTICO (R$1,30M four-state, median R$3,12) · CATÁLOGO (R$1,49M, R$13,53) · SANFONADA (R$0,66M, R$19,19) |
| 2 | **CADERNO** | R$15,69M band ⚠ | UNVERIFIED | UNVERIFIED | ~4% ⚠ | **top-1 supplier only 3,6% — least concentrated in the class** |
| 3 | **ENVELOPE (19705)** | R$11,71M band ⚠ | UNVERIFIED | UNVERIFIED | ~5% ⚠ | top-1 3,3%; saco kraft, low spec risk |
| 4 | **FITA ADESIVA (18071)** | R$17,26M band ⚠ | UNVERIFIED | UNVERIFIED | ~4% ⚠ | 394 suppliers, top-1 9,4% |
| 5 | **ETIQUETA ADESIVA (21/13856)** | R$5,99M band ⚠ | UNVERIFIED | UNVERIFIED | ~11% ⚠ | PHP's single biggest line (R$728.102) — a proven one-person earner |
| 6 | **CAIXA ARQUIVO (19708)** | R$6,70M band ⚠ | UNVERIFIED | UNVERIFIED | ~10% ⚠ | ⚠ value density R$0,38/litre — freight-hostile, basket-only |
| 7 | **CANETA ESFEROGRÁFICA (99)** | **R$1,00M** ✅measured | 16,9% top-1 ✅ | **+26%** (award R$0,830 vs live R$0,617) ✅ | **63,9% — FAILS** ✅ | **basket filler only, never a target** |
| — | **LÁPIS PRETO (12)** | R$3,19M band; SP pool R$985k | 12,5% | +19,5–30% (ES-priced) | 20% nationally / 58–72% in SP — **FAILS** | **probe, not product** — 0,81%/0,00%/0,33% of the three incumbents' books |

**Hard blacklist, with reasons:**
- **PASTA AZ/REGISTRADORA** — state clears R$11,00 median against a cheapest verified self-serve of R$23,84. Only factory-invoice buyers win it.
- **PASTA SUSPENSA plain** — R$2,70 median vs R$2,80–3,81 at every visible price.
- **PASTA TIPO L** — R$0,85 median, p10 R$0,59; the dumping ground where 3,4M units cleared at R$0,83.
- **PAPEL A4 (19746)** — megabuy-dominated; and 213 of 2.843 lines are coded per-sheet at R$20–500 each, a data-entry artefact worth R$16,4M.
- **TONER (13853 et al.)** — 101 of 132 lines labelled "ORIGINAL" priced R$6,40–50 against a genuine-OEM retail of R$209,97. That is either mislabelled compatibles or a field error; either way an honest bidder is undercut by something she cannot legally match.
- **Everything outside class 7510.** Limpeza, têxtil and copa each returned a clean null across 26/22/40 PDMs — different wholesalers, different editais, no shared machine.

---

## 3. THE EDGE

**The honest answer is that there is no moat. The edge is operating discipline, and the head start is zero.**

There is no absent incumbent to surprise. PDM 20 alone has **973 suppliers**; PDM 99 has **978**. `THE BUILDABILITY THRESHOLD`'s "one quarter of head start" does not apply, because nobody is absent. What she has instead is a **persistent execution differential that competitors demonstrably do not run** — and the evidence that they don't is that they keep losing money in public:

**Five bid rules, each with a measured price tag:**

1. **REJECT EVERY LOTE ÚNICO.** Per-item municipal lines clear at **97, 98, 99, 99, 100, 100, 100%** of estimate; LOTE ÚNICO lines clear at **46, 46, 46, 63, 36%**, and two of them awarded pencils at R$0,102 and R$0,069 — *below the R$0,282 wholesale floor*. Detect with `^\s*LOTE` on the item description. Costs 15% of the funnel (22 of 150 sampled editais), saves 100% of the losses.
2. **QUANTITY CEILING, NOT A VALUE BAND.** Reject any line above ~2.400 units. Above that the state pays R$0,82 → R$0,53 and she is bidding against BIGNARDI (capital R$359.626.755), MASTER (R$78.215.000) and BRINK MOBIL (R$32.018.254). This is the rule that replaces the lápis lens's "R$3.000 line floor," which is wrong at basket level — freight amortises per *delivery*, not per line.
3. **READ `siglaUnidadeFornecimento` BEFORE PRICING.** 533 PCT + 234 CX lines sit inside PDM 20's 6.343. Comparing a box price to a unit cost is how the pasta lens got 93% on suspensa before catching itself, and how the sweep got −52%. This is the archive's own unit error in a third costume.
4. **REJECT "CONFORME MODELO DO ÓRGÃO"** — custom spec, and the two largest lines in the dataset carry it.
5. **REJECT NUMERIC ATESTADO.** Presidente Venceslau PE 64/2026 demands "no mínimo 50% as solicitadas neste edital" (TCE-SP Súmula 24); Jundiaí PE 979/2024 says "inexigindo-se na espécie a comprovação de quaisquer quantitativos." Roughly half of SP editais are open to a first-time supplier. Bid those.

**Two free levers nobody is pulling:**

- **LC 123 art. 48 I is per ITEM, not per tender.** 96,7% of 4.355 sampled expediente items are ≤R$80.000 and therefore reserved *exclusivamente* to ME/EPP — yet only **32,8% carry an ME/EPP flag** (one 25-edital subsample ran 90,3% "Sem benefício"). Santa Lúcia flags all 312 items "Sem benefício" with pasta lines at R$1.498–7.805. **One free written impugnação converts an entire edital.** Lei 14.133 art. 164 gives the window; art. 87 §2º separately bars a município from demanding its own cadastro.
- **ICMS-ST segregation.** Pasta arquivo sits on RICMS-SP art. 313-Z13 (item 26-B, NCM 4820.30.00; item 7, NCM 3926.10.00). Bought inside SP the ICMS is already retained, so under Resolução CGSN 140/2018 she segregates the receita in PGDAS: **Anexo I effective falls from ~7,58% to ~5,04% at R$720k**. Worth ~R$18k/year and costs one instruction to the accountant.

**How long does it last?** Indefinitely, and it is worth little. None of this is secret; it is all in public statute and public award data. It is durable only because it is boring and because the median supplier in this class earns **R$5.485/year** (pasta) and **R$2.725/year** (caneta) and is not optimising anything. **Do not model this as a moat. Model it as a wage for discipline, competed away the moment someone else bothers — which, on twenty years of evidence, they don't.**

⚠ **The risk this edge does not answer:** pregão eletrônico is a live reverse auction and IN 73/2022 art. 19 expressly permits bidding robots. She cannot out-click a robot. Her defence is that she is competing on **knowing her floor**, not on speed — a robot bidding below cost still loses money, and the winner's curse is the incumbent's problem. The consequence is real and must be budgeted: **she wins fewer lots than her bid count implies.**

---

## 4. THE SEQUENCE

**First: PASTA ARQUIVO — and specifically, dispensa lines in pasta, for the atestado, not for the money.**

The four criteria, answered:

| | |
|---|---|
| **Feedback speed** | Dispensa lines have a **median value of R$281** and are decided in days. 1.316 of them a year in PDM 20 alone. She can complete a delivery and hold a signed atestado inside **30 days**. |
| **Working capital** | A R$281 line needs R$200 of goods. She can run twenty of them out of pocket errors and all. |
| **Certification gate** | **None.** No Inmetro, no ANVISA, no AFE, no responsável técnico. Zero "ou similar" brand-lock in 5 of 5 downloaded editais. Lei 14.133 **art. 65 §1º** lets a first-year EI substitute a **balanço de abertura** for accounts — verbatim in 2 of 5. |
| **Atestado transfer** | **Total.** 3 of 5 editais demand an atestado and *all three are qualitative* — "serviços compatíveis em características com o objeto," no quantity threshold. One completed delivery of any size discharges it, and it transfers across all 179 PDMs of class 7510 because the object is "material de expediente." |

**This is the one genuinely good use of the dead dispensa channel.** Dispensa is 2,4–2,8% of value and cannot be a revenue engine — but it is a **perfect atestado factory**: smallest lots, fastest cycle, lowest capital, and the certificate it produces unlocks the half of the pregão market that demands one.

**Then, in order:** pasta pregão per-item in SP/MG/PR/RJ (months 2–4) → add CADERNO and ENVELOPE (lowest supplier concentration, 3,6% and 3,3% top-1) → add FITA ADESIVA and ETIQUETA → let CANETA, LÁPIS and CAIXA ARQUIVO ride along as basket filler only.

**Why not caneta first**, despite a bigger headline market: its addressable pool is **R$1,00M and R$640k is 63,9% of it**. Its R$42M of national value is 40× bigger and almost entirely in lines priced below her cost.

---

## 5. PRODUCT-AGNOSTIC OR DEEP? — **Both, on different axes, and the data forces it**

**Deep in ONE CLASS. Agnostic across ITS PDMs. Never across classes.**

The data does not permit a choice:

- **Deep in one PDM is arithmetically impossible.** The best category in 179 — pasta arquivo, the largest — needs **13,2% of its addressable pool**, and only **10 of 973 suppliers (1,0%)** reach R$570k in it. Every other PDM tested is worse; caneta needs 63,9%, lápis needs 58–72% of the SP pool. **No single PDM clears.**
- **A portfolio of 3–5 *separate* categories is the wrong picture**, because it implies separate bids. They arrive in the *same edital*: 83,7% co-occurrence, 33 items median. It is not five businesses on one machine; it is **one bid covering twenty lines.**
- **Across classes it collapses.** Limpeza, têxtil and copa each returned a family-wide null — and for a *structural* reason worth keeping: continuous-consumption institutional commodities (toilet paper, cups, uniforms) get centralised into enormous SRP framework contracts precisely *because* demand is forecastable. They also need different wholesalers, which breaks the one-supplier-account model that makes venda a ordem work.

⇒ **One SICAF registration, one cron, one São Paulo wholesale account, ~40 SKUs across class 7510, bid as baskets.**

---

## 6. WHAT THE KILLS TEACH — a reusable screen

189 PDMs across 8 families died. Sorted by **sole** cause rather than by mention, they reduce to four tests, in cost order:

> **1. IS THE MONEY IN THE PUSHED CHANNEL OR THE FOUGHT CHANNEL? (free, one field)**
> Split value by `modalidade`. **Verified on three independent PDMs: dispensa is 2,81% (pasta), 2,39% (caneta), 0,30% (lápis) of value** — while being 20,8% of *lines*. **The archive's entire distribution thesis — IN 67/2021 art. 7 auto-email, the thing that made FIELDTAG work in thermal media — does not transfer to office supplies.** Here the distribution is Lei 14.133 art. 54 publication plus a per-item cron, and the selling is a robot auction. ⚠ **And always compute dispensa share BY VALUE: the by-line number is 7–70× more flattering, and every family in this sweep was scored on it.**
>
> **2. WHOSE COST BASIS IS THE "RETAIL" PRICE? (one CNPJ lookup)**
> Every LIMB0 kill in the expediente sweep compared a **Kalunga retail shelf** to a state median and called the category dead. Retail is not her cost. And the one open wholesale catalogue anyone found is **in another state**, which adds ~6 points plus ST antecipação. **Before killing on price, establish that the number you are calling COGS is a price she can actually be invoiced at, in her own state.** This single error inverted the verdict on an entire family.
>
> **3. WHAT QUANTITY IS THE LINE? (free, one field)**
> Unit price falls **12,6×** from qty ≤60 to qty >12.000, monotonically. The state's *money* sits in the quantities where the price is below her cost; the *margin* sits in quantities too small to matter alone. **This is why the basket is mandatory and why every "big market" reading is a trap** — R$42M of caneta reduces to R$1,00M of addressable pool.
>
> **4. IS THE PREMIUM REAL, OR IS IT MIX? (one group-by)**
> The R$5–80k band "paid +43–78%" and within sub-type paid **−1% to −9%**. `A COUNT OF STRUCTURES IS NOT A CHECK OF CONTENT` has now fired a fifth time in this file, three of them on agents' own output. **Any cross-sectional premium must be re-measured inside a single spec before it is believed.**

**And the meta-lesson, which is why this pass found a business where 130 candidates did not:** every family that died, died on a limb that was *measured on the wrong denominator, the wrong cost basis, or the wrong slice*. The sweep's numbers were individually defensible and its conclusions were wrong. **Split by sub-type and by unit-of-supply before scoring anything — both fields are free, both are in the row, and here they moved a margin by 81 points.**

---

## 7. THE OPEN QUESTIONS — and the cheapest test for each

Ordered by how much money they gate.

**Q1. Will a São Paulo wholesaler issue a nota fiscal de remessa por conta e ordem to a public body — and at what price? ⚠ THE WHOLE BUILD GATES ON THIS.**
Nothing in this archive verifies it either way. Every SP distributor gates prices behind a CNPJ login (wespi.com.br shows "Esqueceu a senha?" in place of every price; atacadopapelandia.com.br and distribuidoracaue.com.br both 403; gimba.com.br returns 404 on every catalogue path I tried). A self-serve checkout issues **one** nota to her with a delivery address — that is *entrega em local diverso do faturamento*, **not** venda a ordem, which needs the wholesaler's fiscal department to issue two notas.
**Test — free, written, no phone.** Email four SP wholesalers one question: *"Vocês emitem nota fiscal de remessa por conta e ordem de terceiros (CFOP 5.923 + 5.118/5.119) com entrega direta em órgão público, para cliente Simples Nacional? A partir de qual compra liberam prazo?"* **Count the answers containing a yes and a day-count.** Twenty approaches, measure the rate. The permissive end of the published credit gate is **two purchases, not twelve months** (Flora Saúde: "avaliado pelo setor financeiro a partir da segunda compra… prazo inicial 21 dias"), so a no on terms is not a no on the business.

**Q2. What is the actual landed cost per SKU, in São Paulo, for the top 40 lines? ⚠ Every margin in this document is provisional until this exists.**
The only live prices I could pull are the ES catalogue: **caneta Economic 100UN R$61,72 = R$0,617/un · pasta aba-elástico Plascony A02 10un R$20,52 = R$2,052/un · lápis HB 144UN R$40,59 = R$0,282/un** (all fetched today, all interstate, all self-serve rather than account prices — a real distributor account should be *below* these, which means the margins here are more likely understated than overstated).
**Test:** open a CNPJ cadastro with three SP distributors and request a price list on 40 SKUs. Bar to clear: pasta aba-elástico ≤R$1,80/un against a four-state award median of R$3,12.

**Q3. Does the basket margin hold outside pasta?** The pasta lens found **two of three other office SKUs negative** at the same wholesaler — caneta Compactor R$0,6314 vs a band median of R$0,545 (−16%), borracha Mercur R$0,8195 vs R$0,637 (−28,5%). The comparison is brand-mismatched (the state buys generics — FUTURO, LYKE, LEONORA, BRW, BAZZE; the catalogue lists Mercur and Compactor), but **the 29% pasta margin must not be extrapolated to the basket.**
**Test:** re-price each of the top 40 SKUs against the *awarded generic brand*, not against whatever the catalogue stocks. Free once Q2 lands.

**Q4. What is her win rate?** Everything above assumes 35 won baskets. Nothing in this archive measures a win rate, because nobody has ever bid.
**Test — the archive's own test design, and the only one that matters.** Bid **20 real dispensa lines** in month one. Count how many clear a numeric bar committed in advance. **The rate predicts everything after it**, and this is the first time in four weeks and ~130 candidates that a candidate can be tested against a buyer who can say yes, for under R$5.000 and without a phone call.

**Q5. Which buyers pay?** Verified live: `contratos.comprasnet.gov.br/api/contrato/{id}/faturas` publishes `emissao`, `ateste` and `data_liquidacao` per invoice, and the archive measured **15 days at IF de São Paulo against 67 at SAA-MS** on identical purchases — the delay is in the **ateste**, not the payment. For municípios use SICONFI RREO Anexo 07 (verified live: `apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo`, id_ente=3550308, 101 rows).
**Test:** free, and it is worth **~3× her capacity at the same R$50.000** — more than any credit line in Brazil. Bid only where the median is under 30 days.

**Q6. Working capital.** At R$53k/month of billings and 70% COGS she needs ~R$37k of goods in flight; with no supplier terms and a 45–60 day cycle that is **R$55–75k against R$50.000 of capital.** Tight, and the binding constraint at R$1,0M.
**Answers, in order of cost:** the Q5 buyer filter (free, ~3×) → supplier terms after two purchases (free, Q1) → **FGI PEAC**, the only instrument in Brazil whose published eligibility a company with no history passes (BNDES FAQ Q4: *"receita bruta anual de até R$300 milhões"*, no minimum revenue, no minimum time in business; Q11: *"É dispensada a exigência de garantias pessoais e reais"*; minimum R$1.000, 48 agents including Stone and Nubank). ⚠ Rate UNVERIFIED — no agent publishes one.

**Q7. Two small unbudgeted lines.** **Amostra** fires in 2 of 5 SP editais, post-bid, winner-only, **4 working days physical delivery** (Bauru PE 433/2026, Rua Rio Branco 5-05, with written criteria on rebarbas and elastic resistance). Answer: a **20-unit sample shelf, ~R$700 once** — one unit per SKU, which is a sample kit and not inventory. **Garantia de proposta** appeared once in five (Riachão do Bacamarte PB, **R$14.439,70**, forfeitable). Lei 14.133 **art. 58** caps it at 1% of estimate, so filtering to editais under R$500.000 bounds it at R$5.000. Both must be parser fields.

---

## Where the two lenses disagreed, and who I believe

| Dispute | Verdict |
|---|---|
| Is "Atacado São Paulo" in SP? | **Pasta lens.** It is in Vitória/ES — I confirmed at the CNPJ. The lápis lens's margin is interstate-priced. |
| Is lápis preto a business? | **Both, correctly, say no as a category.** Econ said "viable" only by redefining it as the class desk; ops said "not operable as a category, operable as a row." **These agree.** The board reflects it: lápis is a probe. |
| Does the dispensa auto-email rail work here? | **Ops lens.** "The pushed pool cannot pay in this category" — 2,81%/2,39%/0,30% by value, measured by me on three PDMs. |
| Line-size floor of R$3.000? | **Neither.** Wrong frame — freight amortises per *delivery*. The correct filter is a **quantity ceiling of ~2.400 units**. |
| Is LIMB0 as briefed inverted? | **The expediente sweeper is right** that the brief's wording inverts the economics (kill must be *retail ≥ state median*). But the sweeper then used **retail as COGS**, which is the deeper error. **Both the brief's wording and the sweep's execution were wrong.** |

**The truthful bottom line:** no single category clears — the best of 189, pasta arquivo, needs 13,2% of its addressable pool and only 1,0% of its suppliers reach the bar. **The basket clears, at the bottom edge of the target (US$1.770–2.250/month at R$640k), and comfortably at the incumbents' measured volume of R$1,0–1,1M.** Two named one-person Empresários Individuais already run exactly this, one of them on exactly R$50.000 of capital. **It is a wage for discipline, not a moat — and it is the first candidate in this archive that can be falsified for under R$5.000 in thirty days, by bidding.**

Working files: `/tmp/claude-0/-home-user-Random-Access-Memories/9aef20de-742c-52a2-b11a-a33d815230ea/scratchpad/desk/build/` — `pdm20_1..13.json` (6.343 distinct pasta lines), `c99_1..10.json` (4.506 caneta lines), `asp_cnpj.json`, `asp_*.json` (live wholesale probes), `gimba*`/`probe_*` (failed catalogue probes, kept as evidence of the login gate).

---

# ★ THE REBUILT MODEL — 16 Sep 2026, after the São Paulo price was measured

**§1 and §4 above were written against an UNVERIFIED cost basis. The cost is now measured
(`THE_SP_WHOLESALE_PRICE.md`) and three things in them are wrong.** The structure survives; the numbers and
the order of operations do not.

## What changed

1. **§4's sequence starts with PASTA ARQUIVO. Pasta is loss-making at the verified São Paulo price** —
   her R$6,90 against a state median of R$4,34 at ≤60 units and R$2,33 at 450–1.100. **The sequence must
   be reordered.**
2. **§1's ≈R$18.235 of addressable content per edital was extrapolated from pasta + caneta ×10,5.** Pasta
   is dead and **papel A4 — R$197M, the largest single PDM in the class — is dead at −23% to −40%.** The
   figure is an *account-tier* number, not a *today* number.
3. **§1 says "supplying from two São Paulo wholesalers under venda à ordem."** No such account exists, and
   **14 of 15 SINAPEL-member SP wholesalers publish no prices at all.** That sentence describes year two.

## The five lines that are bidable TODAY, at prices already verified

**Perfurador 2 furos (Jocar R$12,90 vs R$19,93–35,00 — live at EVERY band, 35–63%, n=4.720)** ·
**Envelope branco 114×229 (R$0,1399 vs R$0,38–0,455 — 63–99%, n=201 ⚠ thin)** ·
**Caneta BIC azul (R$0,9414 vs R$1,715–11,89 — 45–92% to ~1.100 un)** ·
**Fita adesiva 12×40 (R$2,90 vs R$3,65–8,90 — 20–67% to ~450 un)** ·
**Clips 4/0 (R$0,0515 vs R$0,065–0,264 — 21–80%, 150–1.100 un)**.

**Measured value share: those five are 24,5% of the twelve PDMs priced** (live R$150,0M vs dead R$461,1M;
papel A4 alone is R$196,9M). ⚠ **That 24,5% is a FLOOR, not the answer — twelve of class 7510's 179 PDMs
have been priced. The grade rule predicts many of the other 167 will clear too, wherever the state buys
unbranded.** Pricing them is a day's work and it is the highest-value day available.

## The arithmetic, and it reduces to ONE number: how many wins

| Route | Addressable per edital | Blended gross | Net per edital | **Wins needed for R$130k net** |
|---|---|---|---|---|
| **A — published tier, five live lines only** | ≈R$4.470 | ~40% | ≈R$1.325 | **≈98/year** |
| **B — half the basket sourced at matched grade** | ≈R$9.100 | ~38% | ≈R$2.400 | **≈54/year** |
| **C — supplier account, full basket** | R$18.235 | ~30% | ≈R$3.600 | **≈36/year** |

*(Net is after Simples Anexo I at 5,65–6,73%, freight ~3%, and ~R$75 of platform fees per bid.)*

**Against the two measured one-person incumbents — P H P DE FREITAS RODRIGUES at 79 wins/year and
POLLYANA MELO at 30 — route A needs MORE wins than the best of them and route C needs FEWER than the
weaker of them.** That is the whole business in one line.

## And working capital gates it independently

R$15.600 with **no terms** carries ≈R$19.500/month of billings. That is **52 small baskets a year (route A)
or 13 full ones (route C)**. Route A needs 98 and cannot be financed; route C needs 36 at R$54.700/month of
billings, which **requires 28–30 day supplier terms** — and terms are gated on twelve months of trading
(VPA) or, at the permissive end, **two prior purchases** (Flora Saúde: *"avaliado pelo setor financeiro a
partir da segunda compra… prazo inicial 21 dias"*).

> ### ⇒ EVERY ROAD RUNS THROUGH THE SUPPLIER ACCOUNT, AND IT PAYS TWICE
> It supplies the **price** (~45% on a like-for-like line) **and** the **terms** (~3× capacity at the same
> capital). Nothing else in this build is worth a fraction of either. **The fifteen SINAPEL emails are not
> diligence; they are the first operation of the company.**

## Corrected sequence

1. **Entity + five free registrations + R$20–30k capital social integralizado.** One week.
2. **The fifteen emails**, bar committed in advance (papel A4 ≤R$19,50/resma, caneta azul ≤R$0,70/un,
   faturado in SP, venda à ordem, first-purchase terms). **Count how many of fifteen answer with a number.**
3. **Dispensa lines for the ATESTADO, not the money** — median R$281, decided in days, qualitative in 3 of 5
   editais, transferable across all 179 PDMs of class 7510. ~Five deliveries out of pocket. *(This part of
   §4 stands unchanged and is the one thing that should start on day one.)*
4. **Buy twice from whichever supplier's published credit policy is permissive**, to trip the terms review.
5. **Bid the five live lines per item** while 2–4 run: reject *lote único*, reject numeric atestados, reject
   "conforme modelo do órgão", respect the quantity ceilings, and run the **SICONFI RREO Anexo 07** screen on
   every buyer before bidding.
6. **Price the other 167 PDMs at matched grade** as the cron accumulates editais — this is what moves route
   A toward route B without any supplier account at all.

## The honest timeline

- **Year 1 — no account, small basket:** 25–45 wins, billings R$150–250k, **net R$45–80k ≈ US$720–1.280/month.
  BELOW the bar.**
- **Year 2 — account, terms, atestado, full basket:** 35–55 wins, billings R$640k–1,0M, **net R$125–200k ≈
  US$2.000–3.200/month. AT or ABOVE the bar.**

**That is 18–24 months to target, not 12.**

## The one number nobody has measured, and it is cheap

**The WIN RATE.** Every figure above is expressed in *wins*, and nothing in this archive measures how many
bids produce one. P H P wins 79 a year — from how many attempts? **PNCP publishes the bidder count and the
result per item**; a week of the cron's own output answers it. **Until it is measured, "98 wins" and "36
wins" are equally unfalsifiable, and the difference between them is the entire investment case.**

## What is unchanged and still true

The unit of sale is the **edital**, not the PDM. Distribution is **Lei 14.133 art. 54** — compelled,
free, machine-readable, no origination problem. The registrations cost **R$0**. There is **no moat** (973
and 978 suppliers in the two largest PDMs) and the edge is a persistent execution differential. It passes
`THE MACHINE TEST` on all three limbs and `ORIGINATION ONCE VS ORIGINATION FOREVER` — which is why the
founder kept it.

---

# ★★★ SÃO PAULO IS THE WORST STATE IN BRAZIL TO SELL TO — 16 Sep 2026

**The founder asked "why only SP, why not Bahia" and then "if this niche is great why not scale it
nationally." Both questions are the same question and the answer is that the plan had it backwards.**

Everything above — and the four-state "addressable pool (SP/MG/PR/RJ)" that §2's whole ranked board is
built on — **restricted the SELL side to the cheapest buyers in the country.**

## Measured, three PDMs, inside each quantity band

| Product | band | **SP median** | **BA median** | rest of Brazil | BA vs SP |
|---|---|---|---|---|---|
| **Caneta azul** | 0–60 | R$1,3390 | R$8,80 | R$6,00 | **+557%** |
| | 150–450 | R$0,6700 | R$3,35 | R$1,9950 | **+400%** |
| | 450–1.100 | R$0,5570 | R$1,1750 | R$0,9250 | **+111%** |
| **Perfurador** | 0–60 | R$28,39 | R$40,01 | R$36,00 | **+41%** |
| | 60–150 | R$26,04 | R$39,00 | R$30,00 | **+50%** |
| | 450–1.100 | R$14,53 | R$18,75 | R$24,00 | **+29%** |
| **Fita adesiva** | 0–60 | R$7,10 | R$13,14 | R$9,75 | **+85%** |
| | 60–150 | R$3,7360 | R$7,80 | R$5,20 | **+109%** |
| | 450–1.100 | R$1,5070 | R$4,21 | R$2,98 | **+179%** |

**SP is the cheapest buyer at every band of every product measured.** Top of the ladder for caneta inside
her competitive band: **RO R$4,00 · MS R$3,98 · AM R$3,60 · PI R$3,07 · BA R$3,00 — against SP at R$0,7114.**

> ### ⚠ AND THE QUANTITY CONTROL PASSES, WHICH IS WHY THIS IS A FINDING AND NOT THE FILE'S SIXTH ARTEFACT
> `QUANTITY IS THE PRICE VARIABLE` predicts that a cheap state is simply a state buying bigger lines.
> **It is not.** The premium survives inside every band, and the median line quantity runs the WRONG way for
> the artefact explanation: **Bahia's median caneta line is 2.628 units — larger than São Paulo's — and BA
> still pays 111–557% more.** Three independent PDMs, twelve band-comparisons, same direction every time.

## What it does to the economics

| | Blended gross on the five live lines |
|---|---|
| Selling to **SP** buyers | **15,5%** — caneta is **−40,5%**, fita is +2,8% |
| Selling to **non-SP** buyers | **49,7%** — caneta +52,8%, perfurador +57,0%, clipe +62,0% |

**Same goods, bought at the same São Paulo price. A 3,2× difference in gross margin decided entirely by
which state's tender she bids.** Route A's win requirement falls from **98 to 73 a year** on this alone —
below P H P de Freitas Rodrigues's measured 79.

## So the business is an arbitrage, and it already has a proven operator

**Buy in São Paulo. Sell to the Centre-West, North and Northeast.**

That is not a new idea — it is what **CONDAFE COMERCIO DE ROUPAS LTDA (São Paulo EPP) already does in the
kit niche: 15 UFs, 36 municípios, R$6.135.997 in twelve months**, and what this archive already measured as
*"92,2% of winners are single-UF by headcount, while multi-UF firms (7,8%) take 33,6% OF THE VALUE."*
**The value concentration and the price ladder are the same fact seen from two ends.**

## Why the supply side genuinely IS São Paulo-only — and it is arithmetic, not preference

**LC 123 art. 13 §1 XIII (h)** makes a Simples optante pay the difference between the internal and
interstate rates on goods acquired in another state. SP internal **18%**, interstate into SP **12%** ⇒
**~6 points on every purchase from outside the state.** ⚠ **And Bahia is not special: the 7% interstate
rate runs from the South/Southeast to the North/Northeast/Centre-West/ES, NOT the reverse — BA→SP is the
general 12%, exactly like SC or RS.** ⇒ **An out-of-state supplier must beat a São Paulo one by more than
~6% to be worth using. That is the whole rule.**

> ### ⚠⚠ AND A CORRECTION TO MY OWN FILE, ONE DAY OLD, VERIFIED VERBATIM AT THE SOURCE TODAY
> `THE_SP_WHOLESALE_PRICE.md` and `CLAUDE.md` both say *"papelaria sits on the RICMS-SP art. 313-Z13 ST
> list so art. 426-A antecipação fires on entry."* **FALSE since 1 July 2026.** Portaria CAT 68/2019 on
> `legislacao.fazenda.sp.gov.br`, verbatim:
> **"ANEXO XIX ( Revogado, a partir de 1º de julho de 2026, pela Portaria SRE-09/26, de 17-03-2026;
> DOE 18-03-2026 ) PRODUTOS DE PAPELARIA E PAPEL (artigo 313-Z13 do RICMS)"**
> *(Part of a wider rollback: Portaria SRE 64/2025 revoked Anexos IX, X, XV and items of XIV from
> 1 Jan 2026.)* ⇒ **The interstate penalty is now a clean ~6 points of DIFAL with NO antecipação stacked on
> top, and the bigger of the two hits is gone.** `THE CLOCK MOVED` firing on a law this file wrote four days
> ago — **date-check the regulator's page even on your own entries.**
> ⚠ **It cuts both ways and the net is UNCOMPUTED: under ST a Simples reseller segregated the ST receita and
> paid a reduced rate (~3,7–5,0% instead of 5,65%). With ST revoked there is nothing to segregate, so the
> SELL-side Simples rate rises by roughly the ICMS share of Anexo I (~1,9 points of revenue) — while the
> purchase price should fall by roughly the MVA that is no longer embedded. Which dominates is an
> accountant's question with a real number attached. UNVERIFIED.**

## The three things that must be checked before this is acted on

1. **FREIGHT — the one real cost against the spread, and it is unquoted.** Order of magnitude: a 50-unit
   perfurador line to Salvador is ~20 kg against R$2.000 of revenue; a 2.628-unit caneta line is ~16 kg
   against R$7.884. Estimated 2–15% of revenue against gross margins of 50–75% — **it does not close the
   gap, but it has not been quoted.** One transportadora quote, SP→Salvador/Goiânia/Belém, settles it.
2. **DELIVERY DEADLINES.** Measured on kits: **median prazo de entrega 10 days, 31,2% at ≤5 days.** A
   five-day deadline from São Paulo to Acre is not serviceable. **Screen on `prazo de entrega` before
   distance** — the Centre-West and the Northeast capitals are reachable; the far North is not.
3. **INTERSTATE SALE BY A SIMPLES OPTANTE.** A Simples optante sells at its own Simples rate regardless of
   destination, and STF **ADI 5464** suspended the EC 87/2015 DIFAL clause for Simples senders — so selling
   to a Bahian órgão should carry no extra state tax on her side. **UNVERIFIED as applied; confirm with the
   accountant before the first out-of-state bid.**

⇒ **Corrected rule for the parser: SOURCE IN SÃO PAULO, BID EVERYWHERE THE PRAZO ALLOWS, AND DE-PRIORITISE
SÃO PAULO'S OWN TENDERS — they are the cheapest in the country and caneta is loss-making in them at any
quantity above ~60 units.**
