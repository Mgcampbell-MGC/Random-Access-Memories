# THE BUSINESS — designed 18 Sep 2026

**Everything before this file measured whether a basket of office supplies could be resold to the Brazilian
state at a profit. The answer, measured properly, is no. This file is the business that the same evidence
does support. It is a different company, and the difference is not cosmetic.**

---

## 1. The one number that designs the company

Her capital is **R$15.600, one time, non-reloading.** She pays a supplier before a public body pays her.
With no supplier terms that cash turns about **8 times a year**; with 30-day terms, about **18**.

| gross margin | billings/yr, no terms | net/yr | verdict |
|---|---|---|---|
| 25% *(the expediente basket)* | R$169k | **R$27k** | dead |
| 30% | R$181k | R$38k | dead |
| 40% | R$211k | R$65k | dead |
| **50%** | R$253k | **R$104k** | short |
| **55%** | R$281k | **R$122k** | short |
| 60% | R$316k | R$161k | clears |

**⇒ A 25–30% reseller cannot exist on this balance sheet, at any volume, ever.** The bar is ~R$150.000/year
net. **The company must hold ≥50% gross and must be financed to about R$22–25k of working capital.** Both
of those are design constraints, not aspirations, and every decision below follows from them.

*(This is why the basket plan failed. It was never a margin problem measured wrongly — it was the right
margin for the wrong company.)*

---

## 2. What the machine is, and why it is worth keeping

The asset that survives everything is the **distribution**, and it is the rarest thing in this archive.

- **`Lei 14.133 art. 54`** compels every Brazilian public body to publish the full text of every tender on
  PNCP before it may buy anything — free, machine-readable, national, permanent.
- The daily national descent is **~5.560 calls, ~5 minutes, R$0.** Five free registrations reach 74,3% of
  the field, and `art. 87 §2º` forbids a município demanding its own cadastro.
- **She never originates demand.** After the first registration the buyer publishes the next order by law.
- **She never speaks, never holds a client, never takes a credential.** The unit is a nota fiscal.
- Total running cost, measured: **US$6–14/month** including a VPS and the model calls.

**In ~130 candidates this is the only one whose distribution is a statute.** Nothing in today's demolition
touched it. What was wrong was the product it was pointed at.

---

## 3. The thesis, restated on what was actually measured

**In Brazilian public procurement the clearing price is set by WHO BOTHERED TO BID, not by what things cost.**

Measured today, same pen, same spec, same quantity band (250–5.000 units), twelve months, cleaned of
lot-total rows:

| buyer UF | median R$/pen | vs São Paulo |
|---|---|---|
| **AM** | **2,1000** | **3,75×** |
| RN | 1,1550 | 2,06× |
| RO | 1,0400 | 1,86× |
| AC | 0,9600 | 1,71× |
| CE | 0,8988 | 1,60× |
| … | | |
| RS | 0,5645 | 1,01× |
| **SP** | **0,5600** | **1,00×** |

Nothing about a pen changes between São Paulo and Manaus. **The 3,75× is the price of nobody else showing
up.** ⚠ And the correction that comes with it: this file previously recorded Bahia at **+111% to +557%** —
measured properly **Bahia is −8,4%**, and the old figure was lot-total contamination. The gradient is real;
its size was overstated by roughly 5×, and only **AM, RN, RO, AC and CE** clear on a commodity pen at all.

⇒ **She is not trying to be the cheapest supplier in Brazil. She is trying to be the only one who knows
which lines are worth entering.** That is a different business and it has a different cost structure.

---

## 4. What she sells — and the rule that replaces the basket

**Not a basket. A watchlist, and it grows every day.**

A line is eligible only if **her verified landed cost is ≤50% of that line's own spec-controlled,
band-controlled, UF-controlled state median.** Everything else is skipped — not bid low, skipped.

The parser's admission test, in order (each rule already measured and priced in this archive):

| # | rule | why |
|---|---|---|
| 1 | spec match on **material, size, capacity, sheet-count and brand grade** | `A PDM IS NOT A PRODUCT` — this alone killed four headline lines today |
| 2 | drop rows outside a **plausible unit-price window** | `THE LOT-TOTAL ROW` — 98,7% of one band was data entry |
| 3 | normalise to **pieces** (`capacidade`, CENTO=100, **MIL=1000**) | the unit trap, eight occurrences |
| 4 | **≥50% gross** at her verified cost, in that line's quantity band | §1 — the balance sheet demands it |
| 5 | line value **≤ ~R$15.000** | one line must not consume the whole float |
| 6 | reject **lote único** (`^\s*LOTE`) | clears at 36–63% of estimate vs 97–100% per-item |
| 7 | reject **numeric atestado**, accept qualitative | `THE ATESTADO IS TWO DIFFERENT GATES` |
| 8 | reject **"conforme modelo do órgão"** | custom spec |
| 9 | **buyer pays** — SICONFI RREO Anexo 07, reject saldo÷inscritos > 0,30 | 43,2% of buyers owe >30% of last year's liquidated invoices |
| 10 | **prazo reachable** by PAC from SP (measured: all five target capitals inside 10 working days) | 31,2% of tenders demand ≤5 days |
| 11 | prefer **thin-competition UFs** (§3) | the margin is the competition gradient |

**Rules 1–3 are new today and they are the product.** Eleven commercial vendors were inspected one by one:
every one sells what the state *paid*; **not one takes a cost input or outputs a bid/no-bid.** And a vendor
structurally cannot — her invoice is private. **The cost side is the white space, and it is the only
white space.**

---

## 5. Which market — and this is the decision that changed

**Point the desk at newborn/layette kits, not at material de expediente. Expediente becomes a secondary
watchlist, not the business.**

The reason is structural, not a preference between two margin numbers:

| | material de expediente | newborn kits |
|---|---|---|
| reference price | **a BIC Cristal has a national price everyone knows** | a *"body manga curta 100% algodão M"* has none |
| who bids | BIGNARDI (capital R$359.626.755), MASTER, BRINK MOBIL, bidding direct | 78,5% of winners win **exactly one edital a year** |
| line size | mostly above the ME/EPP band | R$32–79k lines, **inside** the `LC 123 art. 48 I` ≤R$80.000 exclusive reservation |
| price dispersion in one SKU | thin — it is a commodity | measured **2,5×** (body: floor R$5,14, median R$12,66) |
| measured gross | **25–30%, and every line fails spec control** | body 55% · fralda pack 51% · kit higiene 52% |
| market | R$254M across 16 PDMs, but ≥50% pools are R$0,2–1,7M each | **R$59,1M homologado/yr, 979 editais, 699 buying municípios** |

`THE LEGIBILITY–MARGIN ANTI-CORRELATION`, already in this file, predicted exactly this: **margin lives where
the price is not published.** Office supplies are the most legible category in Brazilian procurement, which
is precisely why they carry no margin.

⚠⚠ **AND THE HONEST GATE, stated before anyone acts on it: the kit margins above were measured the OLD WAY
— before `A PDM IS NOT A PRODUCT` and before the lot-total filter — and today every single expediente number
measured that way collapsed.** They are more likely to survive (a body is a simpler object than a caderno,
and R$12,66 for a bodysuit is face-plausible where R$0,33 for an envelope was not), **but "more likely" is
not measured.** ⇒ **Re-run the 843 kit award rows under the corrected method before committing a real. One
day's work, and it is the first thing on the list in §7.**

---

## 6. The operating model

**60 won lines a year, averaging R$6.000, at 50–55% gross.** Five wins a month.

| | |
|---|---|
| billings | **R$360.000** |
| gross at 52% | R$187.200 |
| less Simples Anexo I ≈5,65% of revenue | −R$20.340 |
| less freight ≈4% *(measured 1–19%, median 5–8%)* | −R$14.400 |
| less entity, portals, VPS, model calls | −R$6.000 |
| **net** | **≈R$146.000/yr ≈ US$2.340/month** |
| working capital required | **≈R$22.000** *(has R$15.600)* |

**Bid volume, and this is the one number nobody can know in advance:** at a 10% win rate, 600 bids a year =
50/month ≈ 37 h/month, comfortably inside C9's 87 h. At 5%, 1.200 bids = 75 h/month — the ceiling.
**Below ~5% the company does not fit in her week.** PNCP never publishes losing bids, so this is
unmeasurable in advance and must be instrumented from bid one.

**Sanity check against reality:** 60 wins/year sits inside the measured range of real one-person operators —
**Pollyana Melo 45–100/yr and accelerating; Daiane dos Santos Martins, a micro-empresa with R$10.000 of
capital (less than Sol's budget), opened April 2022, winning across 25 UFs.** The plan is not asking her to
outperform anyone.

### The R$6.400 capital gap, and the one instrument that closes it

**FGI PEAC** is the only instrument in Brazil whose published eligibility a company with no history passes —
BNDES FAQ Q4: *"receita bruta anual de até R$ 300 milhões"*, **no minimum revenue, no minimum time in
business, no prior accounts**; Q11: *"É dispensada a exigência de garantias pessoais e reais"*; minimum
**R$1.000**; 48 agents including Stone, Nubank, Sicoob, Sicredi. ⚠ **No agent publishes a rate — UNVERIFIED.**
Budget against BizCapital's published unsecured CET of 2,91–6,60% a.m.

**R$10–20k on FGI PEAC closes the gap without touching C5** (C5 caps her *own* money, not a loan a company
takes against its own book). **And note what it does NOT buy: above ~R$35k, capital stops binding and WIN
COUNT binds instead** — R$50k of float would need 137 wins/year, beyond both her hours and the incumbents'
observed range. **So the right raise is small and specific: R$15–20k, once.**

---

## 7. The sequence — what to do, in order, with a bar on each step

**Step 0 — Re-measure the kit market under the corrected method. Nothing else starts until this returns.**
843 award rows, 230 editais, spec-controlled, unit-normalised, lot-totals dropped, by quantity band.
**Bar: ≥R$8M/yr of kit lines clearing ≥50% gross at a verified São Paulo cost.** Below that, the kit thesis
is the expediente thesis wearing different clothes and the desk has no product. *(One day. Costs R$0.)*

**Step 1 — The fifteen supplier emails, now carrying a number per SKU.** Written, no phone, bar committed in
advance. Each target is 20% under the spec-controlled state median in the band where that SKU's money sits:

| SKU | ask, faturado in SP | published today |
|---|---|---|
| caneta esferográfica azul BIC | ≤ R$0,52 | R$0,84 |
| lápis preto nº2 | ≤ R$0,29 | R$0,57 |
| pasta aba + elástico ofício | ≤ R$2,80 | R$3,99 |
| caderno capa dura 1/4 96 fl | ≤ R$5,40 | R$6,46 |
| papel A4 75 g resma | ≤ R$16,00 | R$29,00 |

**Bar: three of fifteen reply with a number that clears.** Ask for terms in the same email —
*"faturado, qual o prazo na segunda compra?"* — because Flora Saúde's published policy proves the permissive
end of the market opens at **two purchases, not twelve months**. ⇒ **Select suppliers by credit gate, not by
price list.**

**Step 2 — Entity and registrations.** ME on **Simples Anexo I** (4,00% at R$180k RBT12 · 5,65% at R$360k).
MEI is arithmetically impossible — ceiling still R$81.000, and Resolução CGSN 140/2018 Anexo XI contains the
string *"ATACADISTA"* zero times. Carry **R$20–30.000 of capital social integralizado** — her own money, not
a fee; it caps what any edital may lawfully demand and makes the opening balance sheet clear LG/LC/SG > 1.
Five free portals. **Cost ~R$1.500.**

**Step 3 — Mint the atestado on dispensa.** Median dispensa line **R$281**, decided in days, lowest capital,
no certification gate, and measured **3 of 5 editais demand an atestado and all three are QUALITATIVE** — one
completed delivery of any size discharges it, and it transfers across the whole class. **Use the channel that
carries no money to buy the credential that unlocks the channel that does.**

**Step 4 — One private B2B sale, any size, even R$2.000.** The AGU model TR and both live editais that demand
an atestado accept one issued by a *"pessoa jurídica de direito público **ou privado**"*. **One private
invoice opens the quantitative half of the public market**, and `art. 67 §2º`'s somatório lets small ones
accumulate.

**Step 5 — Run the watchlist and grow the cost table.** Every verified São Paulo price is a new eligible
line. **This is the daily work and it is the only thing in the company that accumulates.**

---

## 8. What is genuinely defensible, and what is not

**Defensible, and each is a measured fact rather than an argument:**
1. **Distribution is a statute.** It cannot be outranked, outbid or withdrawn, and it costs R$0.
2. **Her cost table is private and unbuyable.** Eleven vendors sell the state's prices; none can sell hers.
3. **Her losing-bid log is unbuyable by anyone.** `/itens/{n}/resultados` returns exactly one row — the
   winner — even on a genuine multi-bidder pregão, and `/propostas`, `/lances`, `/classificacao`,
   `/fornecedores`, `/participantes` all 404. **PNCP never publishes who lost.** Instrument it from bid one:
   date, PDM, spec, band, her cost, her bid, result, and the winning price when she loses.
4. **A frontier model release makes this better, never obsolete** — `THE TREADMILL TEST` passes.

**Not defensible, and nobody should pretend otherwise:**
1. **No moat on the goods.** 973 and 978 suppliers in two PDMs; nobody is absent. The edge is a persistent
   execution differential, and the evidence competitors do not run it is that they keep losing money in public.
2. **The win rate is unknown** and structurally unknowable until she has bid.
3. **The kit margins are unverified under the corrected method** (§5) — Step 0 exists for that reason.
4. **~100 kg road freight is still unquoted.** Correios caps a parcel at ~29 kg and every B2B carrier
   (Braspress, Jadlog, TNT, Total Express, Melhor Envio, SuperFrete, Kangu) refuses to quote without a
   contract.
5. **The FGI PEAC rate is unpublished.**

---

## 9. The kill conditions, written down in advance

**Stop, and point the desk elsewhere, if any of these returns:**

- **Step 0 returns under R$8M/yr** of kit lines clearing 50% at a verified SP cost → the kit market is
  another legible commodity and the product does not exist.
- **Fewer than 3 of 15 suppliers** answer with a clearing number **and** Step 0 also fails → there is no cost
  basis in either market and the desk has nothing to sell.
- **Measured win rate below 5%** after 100 logged bids → the bid volume required does not fit in 87 h/month.
- **Median buyer payment beyond 60 days** across her first ten wins → the cash cycle halves her turns and
  the margin requirement rises above what any line clears.

**Each of these is measurable, cheap, and has a number attached. None of them requires her to speak to
anyone, and none of them costs more than a day.**
