# THE SWEEP VERIFICATION — 18 Sep 2026

**What this file is: the verification of the four sweep results that returned on 16 Sep before both workflows
hit the weekly usage limit. Every verify agent and both boards failed, so the four headlines were committed
to nothing and carried into today UNVERIFIED. They have now been re-measured from the primary API, by hand.**

**The result is not a refinement. Of the sweep's four headlines, one was right, one was right and understated,
one was right in a way that refutes a law in `CLAUDE.md`, and one — the largest — dissolved completely.**
And the dissolution has a single cause that has now fired seven times in this archive in seven different
costumes: **a number was compared across two things that are not the same thing.**

---

## 0. Method, stated before the numbers

Every figure below is computed from
`dadosabertos.compras.gov.br/modulo-pesquisa-preco/1_consultarMaterial?tipo=codigoPdm&codigo=X&pagina=N&tamanhoPagina=500`,
paged to exhaustion, and filtered as follows. **Each filter was added because leaving it out produced a wrong
number in this session.**

| Filter | Why | What it moved |
|---|---|---|
| `dataResultado >= 2025-09-18` | the endpoint silently returns ~5 years with no recency filter | inflates an "annual" pool ~3× |
| pieces = `quantidade × capacidadeUnidadeFornecimento` (or ×100 for `C`=CENTO, ×1000 for `M`) | a CX of 50 is not a unit | moved band medians 30–50% |
| `estado != 'SP'` | São Paulo is the cheapest buyer in Brazil, and she buys in São Paulo | the whole arbitrage |
| **implausible unit prices dropped** | **NEW — see §1** | **moved the smallest band 3–5×** |
| **spec control on MATERIAL, SIZE, CAPACITY, SHEET COUNT** | **NEW — see §2** | **killed four of the sweep's five live lines** |

---

## 1. ★ THE LOT-TOTAL ROW — a new data trap, and it has been silently inflating this file's small-lot ladder

On PDM 99 (caneta esferográfica), in the trailing 12 months, non-SP, colour-controlled, the smallest
quantity band reads **R$5,34 per pen**. That is impossible — a BIC Cristal is under a real.

Printing the rows explains it:

```
val=R$673.553  qty=1  sigla=UN  cap=0.0  precoUnitario=R$673553,00  -> "unit price" R$673.553/pen   (RJ)
val=R$ 59.500  qty=1  sigla=UN  cap=0.0  precoUnitario=R$ 59500,00  -> "unit price" R$ 59.500/pen   (MA)
val=R$ 46.610  qty=59 sigla=UN  cap=0.0  precoUnitario=R$   790,00  -> "unit price" R$    790/pen   (RO)
```

**These are buyers who typed the LOT TOTAL into the unit-price field.** 126 of 1.934 rows, carrying
R$2,33M of apparent "value." They land, by construction, in the smallest quantity band — because a lot
entered as one unit *is* a quantity of one.

Dropping rows whose unit price is implausible for the SKU (a ballpoint over R$20):

| band (pieces) | median, no filter | median, filtered | value, no filter | value, filtered |
|---|---|---|---|---|
| 1–60 | **R$5,3400** | **R$1,6800** | R$1.004.109 | **R$12.980** |
| 60–250 | R$2,5100 | R$1,9150 | R$314.038 | R$136.288 |
| 250–1.100 | R$0,9160 | R$0,8500 | R$1.221.570 | R$614.421 |

⇒ **The archive's published caneta ladder — `≤60 → R$6,70`, the number that made "the margin lives in the
small lots" the central claim of `QUANTITY IS THE PRICE VARIABLE` — is 98,7% data-entry error in its top
band.** The monotonic *shape* survives above 250 units. The *level* at the bottom, and the entire
"micro-lot dispensa premium" story built on it, does not.

**PARSER RULE: attach a plausible unit-price window to every SKU and drop rows outside it before computing
any median. It costs one line and it is the difference between R$5,34 and R$1,68.**

---

## 2. ★★★ A PDM IS NOT A PRODUCT — the finding that killed or gutted every headline line

`MATCH THE GRADE THE STATE BUYS` (16 Sep) said: read the state's `descricaoItem` for a **brand** before
pricing against its median. **That was necessary and nowhere near sufficient.** A PDM is a *catalogue
heading*, and it contains materially different objects at 2–10× different prices. Compare across them and
you manufacture a margin out of nothing.

Every case below is from this session. In each, the left column is what the sweep (or this archive) reported;
the right is what the same data says once the comparison is like-for-like.

### CADERNO — reported R$67,3M/yr and LIVE at 23–28%. Actually ~R$1,06M addressable and ~4% gross.

The sweep priced a **Sixpel "Caderno Capa Dura Brochura 1/4, 96 folhas" at R$6,46** against the whole of
PDM 196. The whole of PDM 196 contains:

```
R$8.916.446  200 FL, 320 mm                          (a 200-sheet hardback, not a 1/4)
R$4.185.986   80 FL, capa cartão duplex 250 g
R$3.337.800  FICHÁRIO, capa PU, R$11.126,00 PER UNIT (a leather folio, 300 of them)
R$2.384.465  "CADERNO DO ALUNO", R$109,55 per unit   (a printed workbook — not a notebook at all)
R$1.694.310  200 FL capa dura 200×275 mm             (×6 near-identical lines, R$1,6–1,7M each)
```

Controlled to **96 folhas AND a 1/4 format (≤230×170 mm)** — the object she can actually buy:

| band (pieces) | n | state median | gross @ R$6,46 | value |
|---|---|---|---|---|
| 1–60 | 48 | R$7,70 | +16,1% | R$15.685 |
| 60–250 | 75 | R$6,80 | +5,0% | R$86.486 |
| 250–900 | 39 | R$5,98 | **−8,0%** | R$189.396 |
| 900–3.000 | 31 | R$7,95 | +18,7% | R$497.389 |
| >3.000 | 35 | R$5,36 | **−20,5%** | R$4.685.430 |

**Median gross across the whole spec-matched set: +4,2%.** 12-month non-SP value on the spec: R$5,47M, of
which R$4,69M sits in the band that loses 20 points. **CADERNO is not the largest live line in the class.
It is not a live line.**

### PRANCHETA — reported LIVE at every band, 2,6–41%. Actually dead above 50 units.

PDM 18065 is **331 acrylic rows and 248 wood rows.** The sweep's R$9,35 Acrimet MDF was being priced against
acrylic clipboards, which the state buys at R$9,95–17,48 and which cost R$20,76 wholesale.

| set | her cost | state median | gross | 12mo value |
|---|---|---|---|---|
| wood / MDF / eucatex / duratex | R$6,21 (Bacchi, cheaper than the sweep's) | R$5,20 | **−19,4%** | R$608.684 |
| acrylic / PVC / poliestireno | R$20,76 (Acrinil) | — | **−19% to −109%** | R$2.523.065 |

Bands on the wood set: **+4% / −19% / −30% / −52% / −40%.** Live only below ~15 units.

### APONTADOR — looked like the best line in the archive (+40,6%, R$3,0M addressable). Actually R$77k of market.

Sixpel sells an *apontador simples* at **R$0,41** and an *apontador com depósito* at **R$1,03–1,37**.
PDM 46 is 377 rows of **com depósito** and 84 rows of **simples**.

| set | her cost | state median | gross | 12mo non-SP value |
|---|---|---|---|---|
| simples (what R$0,41 buys) | R$0,41 | R$0,5550 | +26,1% | **R$77.492** |
| com depósito | R$1,03 | R$0,7300 | **−41,1%** | R$2.799.478 |

**The +40,6% was R$0,41 priced against a market that is 78% a different object.** The conforming market is
seventy-seven thousand reais a year, nationally.

### CAIXA ARQUIVO — looked like +23,3%. Actually +10,9%, and flat.

691 polionda rows against 234 papelão rows. Her R$3,53 is a *papelão* arquivo morto. Controlled:
**+10,9% median, bands +36 / +10 / +5 / +3 / +3%**, R$4,11M of value. Alive, barely, and not where the money is.

### PASTA A-Z — the one lead the sweep never found, and it is dead too.

Spec-split of PDM 20 turned up **552 A-Z / registrador rows at a state median of R$11,70, live at every band
at +59% to +68%, R$5,04M/yr.** That looked like the best line in the file for about four minutes.
**Sixpel's Pasta A-Z Lombo Largo Ofício (Dac) is R$33,68.** Dead by 3×. Recorded so nobody re-finds it.

### PACKING TAPE (fita 48 mm) — same shape, same death.

State median for 48×50 mm is **R$4,30**; Alltape 48×50 at Sixpel is **R$4,38**. −1,9%. The "+42,8%" it
showed against a 24 mm proxy was a width mismatch.

---

## 3. What actually survives — the spec-controlled table

12 months, non-SP buyers, pieces-normalised, implausible rows dropped, **like-for-like on material, size and
capacity.** Cost source in every row is a CNPJ-verified São Paulo seller with a published price.

| SKU (spec-controlled) | her SP cost | state median | gross | bands | 12mo non-SP value | addressable @20% |
|---|---|---|---|---|---|---|
| **ENVELOPE 114×229** | R$0,1399 | R$0,3300 | **+57,6%** | +75 / +72 / +64 / +59 / **+48** | R$1.739.994 | **R$1.247.805** |
| **PERFURADOR 2 furos, ≤25 fl** | R$12,90 | R$23,00 | **+43,9%** | +54 / +46 / +32 / +13 | R$224.563 | R$159.941 |
| RÉGUA escritório 30 cm | R$1,03 | R$1,2100 | +14,9% | +33 / +13 / −4 / +6 / −30 | R$1.378.943 | R$632.050 |
| FITA 12 mm × 30 m | R$1,39 | R$1,5825 | +12,2% | +77 / +41 / −26 / −103 | R$2.445.049 | R$1.337.329 |
| CAIXA ARQUIVO papelão | R$3,53 | R$3,9600 | +10,9% | +36 / +10 / +5 / +3 / +3 | R$4.109.454 | R$921.735 |
| CADERNO 96 fl 1/4 | R$6,46 | R$6,7500 | +4,2% | +16 / +5 / −8 / +19 / −21 | R$5.474.387 | ~R$1.062.585 |
| RÉGUA comum 30 cm | R$1,03 | R$1,1000 | +6,4% | +46 / +10 / −3 / −2 / −2 | R$1.280.925 | R$574.634 |
| CANETA azul plástica | R$0,84 | R$0,6565 | **−28,0%** | +16 / +7 / −17 / −42 / −64 | R$12.765.578 | — |
| LÁPIS preto nº2 | R$0,57 | R$0,3600 | **−58,3%** | +36 / 0 / −54 / −90 / −111 | R$7.064.346 | — |
| BORRACHA | R$0,68 | R$0,6000 | −13,3% | +23 / −1 / −31 / −36 / −113 | R$4.511.803 | — |
| PASTA aba+elástico | R$3,99 | R$3,4800 | −14,7% | +16 / −8 / −38 / −25 / −65 | R$6.716.109 | — |
| APONTADOR simples | R$0,41 | R$0,5550 | +26,1% | +51 / +33 / +20 / +4 / −43 | **R$77.492** | R$33.130 |
| PRANCHETA madeira | R$6,21 | R$5,2000 | −19,4% | +4 / −19 / −30 / −52 / −40 | R$608.684 | R$259.574 |
| LÁPIS DE COR | R$0,7075 | R$0,4917 | −43,9% | +83 / −2 / −41 / −43 / −72 | R$18.699.411 | — |
| CAPA ENCADERNAÇÃO | R$0,4357 | R$0,3528 | −23,5% | +46 / +5 / −16 / −36 / −45 | R$1.310.111 | — |
| BOBINA térmica | R$4,82 | R$4,8950 | +1,5% | +76 / +20 / −15 / −30 / −256 | R$1.592.498 | — |
| PASTA A-Z | R$33,68 | R$11,70 | **−188%** | dead everywhere | R$5.037.921 | — |
| TESOURA | R$10,81 | R$3,40–7,90 | dead | — | — | — |
| PAPEL A4 | R$29,00 | R$19,83–25,75 | dead | — | — | — |

**Exactly one line clears a workable margin at the quantities where the money is: the envelope.**
Everything else is either negative, or positive only in bands that hold a few tens of thousands of reais a
year nationally.

**Spec-controlled addressable pool at the published São Paulo tier, all lines, whole country, 12 months:
roughly R$4,5–5,0 million.** Against ≈R$640.000 of billings for the bar, that is a **13–16% share of the
addressable pool** — which fails `THE MARKET-MULTIPLE RULE` (3–5× the target; 15–25% only as an exceptional
underwrite for a greenfield entrant).

---

## 4. ★★★ THE VERDICT THIS FORCES

**`THE 45% TIER GAP` said the distributor account was worth ~45% and was "step one." That understated it.
At the published tier there is no business here at all.** The five-line "bidable today" basket recorded on
16 Sep does not survive spec control: of its five lines, **envelope survives, perfurador survives at a
R$225k spec, fita survives only below 250 units, and caneta and clips do not survive at all.**

This is not a reason to stop. It is a reason to reorder:

1. **The fifteen supplier emails are the company.** Not diligence, not step one of many — the only step.
   Until a faturado distributor price exists, A EXPEDIENTE has one product (envelopes) and a R$1,2M national
   pool to take 50% of.
2. **The bar to ask them for is now measurable, per SKU, and it is not "45% off".** It is: *caneta ≤R$0,52,
   lápis ≤R$0,29, pasta aba+elástico ≤R$2,80, caderno 1/4 96 fl ≤R$5,40, A4 ≤R$16,00* — i.e. 20% under the
   spec-controlled state median at the quantity band where that SKU's money actually sits. Those five numbers
   are the email.
3. **Two unpriced pockets are worth an hour each, and both were found by spec-splitting rather than by
   hunting:** a **26–50-folha perfurador** (state median R$34,30, R$967.390/yr, live at every band against
   *any* cost under ~R$27) and a **>50-folha perfurador** (state median R$91,83, R$705.259/yr). This archive
   has no cost for either. A punch is a machine with a wide price ladder — this is the most likely place a
   published price still clears.

---

## 5. The sweep's other three headlines, verified

### ★★★ P H P DE FREITAS RODRIGUES IS NOT AN EXPEDIENTE OPERATOR. A load-bearing law in `CLAUDE.md` is wrong.

`THE INCUMBENT IS THE PROOF` states he "wins 79 tenders a year averaging R$14.073 = R$1.111.800 in
expediente" and is "the same operator this archive already recorded at R$1,78M/yr in thermal media" — **"one
person, R$50.000, ~R$2,9M/year across two categories."** It is the plan's bracketing anchor: the sentence
that makes "35 baskets a year" look conservative.

**Measured two ways, both negative:**

- **CNPJ 38.261.300/0001-05 appears ZERO times in 82.650 award rows across all twelve priced expediente
  PDMs** (caneta, lápis, pasta, clipe, borracha, grampo, perfurador, tesoura, apontador, fita, envelope, A4).
  The sweep found the same on its own independent 92.777-row pull.
- His full PNCP contract record is **103 contracts over 3,7 years totalling R$1.681.186 ≈ R$454k/yr**, or
  **≈R$184k/yr excluding one R$1.001.430 Ceará etiqueta contract that is 60% of the entire sum.** Median
  contract R$1.900. Object tally: ETIQUETA 38, BOBINA 21, RIBBON 3, TÉRMICO 3. **He is a thermal/label
  consumables specialist and he does not compete in this basket.**

⚠ The contract search undercounts by construction (a dispensa is instrumented by nota de empenho, not a
contract — `Lei 14.133 art. 95 I`), so R$454k/yr is a floor. **But the expediente absence is measured on the
award-line rail, not the contract rail, and it is unambiguous.** `CLAUDE.md` must be corrected.

**POLLYANA MELO checks out and is larger than recorded:** 487 award lines and R$1.394.440 across the twelve
PDMs in twelve months by my own count; 160 contracts, **2024 R$295.049 → 2025 R$687.051 → 2026 R$1.316.553
through 8,5 months**, annualising to ~R$1,86M. 85% of it in Amazonas. She is a **multi-category institutional
basket operator** (EXPEDIENTE 63, CONSUMO 39, LIMPEZA 25, HIGIENE 17), not an office-supplies specialist.

**And four better anchors were found, all CNPJ-verified today:**

| | CNPJ | form | capital | base | footprint |
|---|---|---|---|---|---|
| **DAIANE DOS SANTOS MARTINS** | 45.930.390/0001-37 | Empresário Individual, ME | **R$10.000 — less than Sol's budget** | Belo Horizonte/MG, opened **Apr 2022** | **25 UFs, all 12 PDMs, 669 lines** |
| A D S QUEIROZ | 34.590.793/0001-68 | Empresário Individual, EPP | R$200.000 | Fortaleza/CE, 2019 | 11 of 12 PDMs, R$12,6M over 4,75 yrs (≈R$2,66M/yr) |
| KINGDOM COMÉRCIO DE LICITAÇÕES | 48.500.314/0001-80 | LTDA, ME | R$150.000 | Contagem/MG, 2022 | 9 UFs, all 12 PDMs, 621 lines |
| ARAÚJO LICITAÇÕES | 28.485.774/0001-79 | LTDA, ME | R$100.000 | Apucarana/PR, 2017 | 22 UFs, all 12 PDMs, 604 lines |

**Daiane is the anchor the plan should have been bracketed against all along: a micro-empresa four years old
with R$10.000 of capital, running the exact multi-UF multi-PDM playbook.** And two of the four are companies
whose *registered name says the business is winning tenders* — this is a recognised micro-business category,
not a structure nobody has noticed.

### ★★ FREIGHT DOES NOT KILL THE ARBITRAGE, and the measurement is better than it needed to be.

Reverse-engineering a verified SP wholesaler's own checkout (`POST suprimaissp.com.br/frete/`, no login)
gives live Correios quotes to any CEP. Measured on a 3,6 kg ream: **R$35,34 SP / R$44,49 Salvador / R$40,82
Goiânia / R$48,46 Belém / R$40,83 Campo Grande / R$57,06 Porto Velho**, falling to **R$4,72–10,04/kg** at
28,8 kg. On the three named lots freight is **1–19% of line revenue, median 5–8%**, against gross margins of
20–90%. **All five target UFs clear a 10-business-day bar by PAC; three clear 5 days by SEDEX.**

Two findings worth more than the numbers:

- **A live 2026 municipal edital forbids charging a different price by delivery location** — Riachão do
  Bacamarte/PB PE 7/2026 cl. 9.8: *"Não será admitida a previsão de preços diferentes em decorrência do local
  de entrega"* — and contains the words *frete*, *CIF* and *FOB* zero times in 43 pages. **Freight is embedded
  in the bid price, so the SP-origin leg is the complete freight basis.** Same edital sets a **3-day** delivery
  deadline, tighter than the archive's 10-day median.
- **Correios hard-caps a parcel at ~29 kg** (8 reams ship, 9 do not, at every destination), and **every B2B
  road carrier refuses to quote without a contract** — Braspress, Jadlog, TNT, Total Express, Melhor Envio,
  SuperFrete, Kangu. The ~100 kg tier in this file is a constructed 4-parcel proxy and remains **UNVERIFIED**.

### ★★ WIN RATE IS STRUCTURALLY UNMEASURABLE, and that fact is itself the answer to the moat question.

`/itens/{n}/resultados` returns **exactly one row — the homologated winner — even on a genuine multi-bidder
pregão**, and `/propostas`, `/lances`, `/classificacao`, `/fornecedores`, `/participantes` all 404.
**PNCP never publishes who lost.**

⇒ **Her own bid log is private information that no competitor and no vendor can reconstruct.** It is the one
asset in this plan that compounds and cannot be bought — and it costs a database table. **Instrument the cron
to log every bid from day one: date, PDM, spec, quantity band, her cost, her bid, result, and the winning
price when she loses.** Nothing else in this business accumulates.

Bounded rather than measured: both anchors' output (2,5–8,3 wins/month) fits inside her 58–116 bids/month
capacity at any win rate above ~3–15%. **Capacity is unlikely to be the binding constraint.**

### LIMPEZA / LOUÇA / UTENSÍLIOS stay closed, with one correction.

COPO DESCARTÁVEL dead on 98,5% of its value; ÁGUA SANITÁRIA dead at every band; DETERGENTE live on 3,7% of
value. **UTENSÍLIOS DOMÉSTICOS (bedding/foam, R$210,6M/12mo, the largest family sampled) is UNTESTED, not
dead** — no São Paulo seller of bedding or foam publishes a self-serve price at all. And **97–99% of these
families is pregão**, so the dispensa auto-email channel does not exist here either.

---

## 6. ★★ AND THE FOUNDER'S PREMISE IS HALF WRONG — somebody IS selling this

The brief was *"we must assume NOOOOOO one is doing this level of research."* Verified at the vendor's own
page today:

> **SIGA Pregão — "Novo · Pagômetro: Avalie a capacidade de pagamento do órgão antes de disputar, e venda
> apenas para quem está com as contas em dia."** Plan Ultra, **12× R$389,42 or R$3.997 à vista**.
> Same product also ships *"Módulo Disputa: Automatize lances… e proteja sua margem de decisões impulsivas"*
> and *"Inteligência artificial para análise de edital."*

**The free SICONFI RREO Anexo 07 municipal payment screen this archive recorded on 12 Sep as "the best thing
found in this hunt" is a commercially sold feature, launched as new, at R$3.997/year.** Alerting and
AI edital-reading are commodity across at least eight vendors from R$0 to R$580/month.

**What eleven inspected vendors do NOT sell — checked one by one — is a margin computed from the supplier's
own cost table, spec-controlled, driving a bid/no-bid decision.** Every "análise de mercado" feature shows
competitor and historical *award* prices; none has a cost input, none does margin arithmetic, none outputs
bid/no-bid. **That is the white space, it is narrow, and it is exactly the thing this file spent today
building** — §1 and §2 are its specification.

⚠ **Record the honest version: the research is not unprecedented. The COST SIDE of it is.** A vendor can sell
what the state paid because the state publishes it. No vendor can sell what *she* pays, because that is her
own invoice — which is the same structural reason her losing-bid log is unbuyable.

---

## 7. What this costs to run — and it is not the constraint

Measured live: the national PNCP descent is **~5.560 calls, ~296 s/day**. Classification of a 33-line edital
by a batched Haiku 4.5 call with a cached system prompt is **~$0,010/edital**; snippet-based field extraction
from the PDF is **~$0,008–0,015/edital**, against **~$0,069** for feeding the whole text — a 5–9× penalty for
skipping the deterministic pre-grep. **Six of six sampled 2026 editais (34–75 pages) were genuine text-layer
PDFs; zero needed OCR.** Total pipeline **$6–14/month including a R$25 VPS.**

⚠ **The grep rule this file wrote for payment terms is too narrow:** `Decreto Municipal` hit only 2 of 5
sampled editais; the others cite a federal decree or phrase the clause without the word. **Widen the pattern
to the payment clause, not the decree's name.**

⚠ **And the bidding robot does less than assumed.** `IN SEGES/ME 73/2022 art. 19`'s free native robot
automates **only the lances phase**. Initial proposal submission, document upload and habilitação remain
manual session-authenticated UI actions under **art. 18**, and no public write-API exists. Those are her
hours, per bid, forever.

---

## 8. Open, and honestly open

- **No distributor price exists yet.** Everything above is the published tier. §4 is the only route.
- **A ~100 kg road-freight rate is still unquoted.** Every carrier requires an account.
- **Win rate is unmeasurable in advance** and can only come from her own bid log.
- **The 26–50 fl and >50 fl perfurador pockets are unpriced** — R$1,67M/yr combined, and the single most
  likely place a published price still clears.
- **UTENSÍLIOS DOMÉSTICOS has no measured cost anchor at all**, and it is the largest family sampled.
