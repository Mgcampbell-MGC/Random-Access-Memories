# ACOLHE — BUILD HANDOFF

**For a fresh Claude Code session whose job is to BUILD and AUTOMATE this business.**
Written 19 Sep 2026. Everything below is measured unless explicitly marked UNVERIFIED.

---

## 0. HOW TO USE THIS DOCUMENT

You are picking up a business that has been researched to death and built zero percent.
Research is **done**. Do not re-run hunts. Do not re-screen candidates. Do not look for a better idea.

**Your job is to build the machine described in §4 and get it to the acceptance criteria in §12.**

Read in this order:
1. This file, all of it, before writing a line of code.
2. `THE_KIT_DESK.md` — the business case with every source URL.
3. `CLAUDE.md` — the repo's working rules. It is ~150 derived laws. You do not need to absorb
   all of it, but §7 of this file extracts every one that governs code you will write.

**Do not read the other 174 markdown files.** They are a graveyard of dead candidates. They will
cost you context and teach you nothing you need. If you find yourself reading `CANDIDATE_*.md`,
stop.

**The single most important instruction in this document:** every number you compute from a
government API is wrong by default. §6 and §7 exist because nine separate measurement errors were
made on this data, most of them flattering, most of them by a previous Claude session. Apply the
five filters in §6 to every single aggregate before you believe it or show it to anyone.

---

## 1. THE MISSION

Build a one-person government-supply desk that sells **newborn layette kits (kits natalidade /
enxoval)** to Brazilian municipalities.

The whole business is a loop:

```
statute publishes the tender  →  machine reads and prices it  →  she bids
   →  wins  →  buys the goods  →  ships  →  invoices  →  paid in ~30-45 days
```

**Why it works:** `Lei 14.133/2021 art. 54` compels every contracting body in Brazil to publish the
complete tender document — including the exact item list — on one national website (PNCP), free and
machine-readable, before it may buy anything. `art. 55 I a` sets an 8-working-day minimum notice for
goods. Measured: **~4 newborn-kit tenders published per working day, median 10 working days' notice,
98,1% ≥5 days.**

There is no customer acquisition problem. There is no marketing. The buyer is legally obliged to
announce itself. **This is the only candidate in a ~130-candidate search whose distribution is a
statute.**

**Target:** 21 won tenders per year — 2,1% of the ~1.012 published — which is ≈R$360.000 of billings
at ~52% gross. Two real one-person-scale competitors already exceed that (§10.4).

**The founder is Sol**: 26, São Paulo, native Portuguese, fluent written English, not a developer.
She will operate this. You are building it *for her to run*, not for you to run.

---

## 2. FOUNDER CONSTRAINTS — THESE GOVERN EVERY DESIGN DECISION

These are hard. If a design choice violates one, the design is wrong, not the constraint.

| | Constraint | What it means for your code |
|---|---|---|
| **C1** | No daily phone-sales operation. Video/voice calls are permitted but must not be the engine. | Never design a flow that requires her to phone anyone on a schedule. Written and on-screen only. Bidding is a robot auction — that is fine. |
| **C2** | Permanently faceless. No camera, no personal brand, no audience-building. | Company brand only. Nothing she publishes may carry her name or face. The website (already built, `brand/site/`) obeys this. |
| **C3** | **No employees, no contractors, ever.** Vendors and suppliers are allowed. | You may buy SaaS, VPS, a print bureau, a courier, a wholesaler. You may NOT design anything that needs a hired person. A freelancer to "just build the scraper" is a C3 violation — you build it. |
| **C4** | Never takes custody of a customer credential or standing access to their systems. | Her own SICAF/BLL/platform logins are hers — fine. Never design anything that logs into a *buyer's* system. |
| **C5** | **US$500–2.500 ONE TIME. It does not reload.** | No per-seat subscriptions. No monthly AI agent products. Target: a ~R$30/month VPS and metered API calls. A R$4.000/yr tender-alert SaaS is out — you are building its replacement. |
| **C9** | ~87 h/month of her screen time, total. | Every hour of manual work you fail to automate comes out of her bidding capacity. Budget: ≤0,6 h per bid, ≤8 h per won order. |

**Vetoes:** construction as a buyer segment · labour-compliance document chasing · physical goods and
inventory **unless made-to-order** (this business complies: nothing is bought until the tender is won) ·
anything requiring her to be believed as an expert.

### 2.1 The two revealed preferences — these outrank stated constraints

Both were learned by showing her a real list and watching what she cut. They are the most stable
signals in the whole record:

- **THE MACHINE TEST** — a machine makes the unit · the buyer can verify it without trusting her ·
  selling does not create a relationship she must then hold.
- **ORIGINATION ONCE, NOT FOREVER** — after the first yes, the next unit of demand must arrive by
  itself. She must not have to go and fetch every sale.

The kit desk passes both. **If you are ever tempted to add a feature that makes her chase demand or
hold a client relationship, it fails the business on the two criteria she actually chose on.**

---

## 3. THE BUSINESS MODEL — enough to make judgement calls

### 3.1 What is sold

**The assembled kit, not the loose items.** This is the central economic fact and it was discovered
late, after a previous session declared the market dead by measuring only components.

- A body costs R$15,32 in São Paulo; the state's standalone body line medians R$12,66. **−21%, dead.**
- Inside a 17-item kit awarded at **R$359,05**, that same body is one of seventeen lines and is
  absorbed. BOM R$169–230 ⇒ **+36% to +53% gross.**

Every component has a published national price. *"Seventeen specified baby items in one bag"* has
none. That is where the margin lives.

### 3.2 Two tender types — read the tender type, not just the object

| Tender says | What happens | Our view |
|---|---|---|
| **menor preço por KIT** (unidade = KIT/UN, one line = one kit) | She buys all components, assembles, ships finished kits | **The good one.** R$11,1M/yr, median award R$288, **75,1% of value won by ME/EPP** |
| **menor preço por ITEM** | The town buys 3.000 towels and 3.000 blankets separately; its own staff assemble | Easier, thinner. Wholesaler drop-ships to the town. No assembly margin exists, and none is lost |

### 3.3 Who wins what — segment by supplier size BEFORE pricing

`porte` is a free field on every PNCP award row. Measured, by VALUE:

| Band | Value | ME/EPP | "Demais" | Winners | Median winner-year |
|---|---|---|---|---|---|
| **Assembled kits R$80–600** | R$11.110.510 | **75,1%** | 15,7% | 91 | **R$60.520** |
| Three live component families | R$5.048.731 | 60,8% | 27,8% | 245 | R$6.760 |
| **Body + macacão** | R$11.147.227 | 18,5% | **74,9%** | 150 | R$5.228 |

**BRINK MOBIL** (capital social R$32.018.254) alone takes **R$5,66M of the R$11,1M** body+macacão
band. Those families are loss-making *because a manufacturer bids them direct.* **Do not build a
strategy that competes there.**

### 3.4 Geography — buy in São Paulo, sell almost anywhere else

São Paulo has the most kit tenders in the country and the worst prices. The gradient is a
**competition** gradient, not a cost one — the same kit sells for more where fewer firms bother to bid.

**Bid: MG · MA · BA · CE · PE · SE · PA · RN.** De-prioritise SP, ES, MT, MS.

Supply side genuinely is SP-only, and it is arithmetic: `LC 123 art. 13 §1 XIII (h)` charges a Simples
optante the internal-minus-interstate ICMS difference — SP internal 18% vs interstate-into-SP 12% =
**~6 points**. An out-of-state supplier must beat an SP one by more than 6%.

⚠ **Concentration warning that must survive into the product:** **Coari/AM alone was 34,8% of the
entire pool clearing ≥50% gross** — two lines from one tender. Top 10 municípios = 63,4%. Any
market-size figure the system reports must also be reported **ex-largest-buyer**.

---

## 4. THE SYSTEM TO BUILD

### 4.1 Architecture

Python 3.11+, SQLite, a cron on a ~R$30/month VPS. No server, no framework, no cloud services beyond
the VPS. Everything file-based so she can open it, and so you can diff it.

```
acolhe/
  config/
    skus.yaml            # the SKU set: spec patterns, plausible price windows, cost
    rules.yaml           # the 11 admission rules, each with a threshold
    ufs.yaml             # target UFs, prazo-de-entrega feasibility by region
  db/
    acolhe.sqlite        # everything. see §4.3
  harvest/
    pncp_client.py       # rate-limited, retrying, dual-family PNCP client (§5.1)
    daily.py             # fetch yesterday's tenders (modalidades 6,7,8)
    descend.py           # /itens descent for title-invisible tenders
    arquivos.py          # download edital PDFs
  parse/
    normalise.py         # THE FIVE FILTERS (§6). Nothing bypasses this module.
    spec.py              # SKU classification with spec control (§7.4)
    edital.py            # PDF -> text -> clause extraction (§8)
  price/
    cost.py              # cost table lookup, interstate loading, freight estimate
    bom.py               # assemble a BOM from an item list, return cost + confidence
    margin.py            # per-line and per-lot margin
  screen/
    rules.py             # the 11 rules, each a pure function returning (pass, reason)
    buyer.py             # SICONFI payment-risk screen (§5.3)
  log/
    bidlog.py            # THE COMPOUNDING ASSET. append-only. see §4.4
  report/
    digest.py            # the daily output she actually reads
  tests/
    test_traps.py        # one regression test per trap in §7. MANDATORY.
```

### 4.2 The daily loop

```
06:00  harvest.daily        fetch all tenders published yesterday, modalidades 6/7/8
       harvest.descend      for tenders whose title does not match, pull /itens
       parse.normalise      apply the five filters to every item row
       parse.spec           classify each item to a SKU with spec control
       harvest.arquivos     for candidate tenders only, download the edital PDF
       parse.edital         extract the clauses the rules need
       screen.rules         run the 11 rules -> pass/fail with reasons
       screen.buyer         SICONFI check on every surviving buyer
       price.bom            price the basket; compute gross at her cost
       report.digest        emit: BID (with a suggested price) / NO-BID (with the reason)
```

Cost: ~5.560 calls/day for the full descent, 158–265 seconds at 10 connections. Trivial.

### 4.3 The database

Tables, minimum:

- `tender` — pncp key, órgão cnpj, município, uf, ibge, modalidade, objeto, data_publicacao,
  data_encerramento_proposta, valor_estimado, srp (bool), raw json
- `item` — tender fk, numero_item, descricao, unidade, quantidade, capacidade, valor_unitario_estimado,
  **pieces** (normalised), **sku** (classified), **spec_ok** (bool), **dropped_reason**
- `award` — tender fk, numero_item, winner cnpj, winner nome, **porte**, valor_unitario, valor_total,
  data_resultado
- `buyer` — cnpj, ibge, município, uf, siconfi_pct_paid, siconfi_cancelados, last_checked,
  decreto_pagamento_dias (parsed from edital)
- `cost` — sku, supplier, url, price, unit, capacity, **spec** (json), verified_at, **is_inference** (bool)
- `bid` — **the compounding asset. §4.4**
- `rule_result` — tender fk, rule_id, passed, reason, evidence

### 4.4 THE BID LOG — the only asset in this plan that compounds

**PNCP publishes who WON. It never publishes who lost, or what they bid.** Verified:
`/itens/{n}/resultados` returns exactly one row — the homologated winner — even on a genuine
multi-bidder pregão. `/propostas`, `/lances`, `/classificacao`, `/fornecedores`, `/participantes`
all 404.

⇒ Nobody — not her, not a competitor, not the R$3.997/yr software vendors — can know the real win
rate or the real losing prices. **Except her, about her own bids.**

Log from the very first bid, append-only, never overwritten:

```
date · tender key · município · uf · sku · spec · quantity band · her cost ·
her bid · result (won/lost/cancelled) · winning price when she loses ·
number of bidders if visible · rule results at bid time
```

After six months this file tells her exactly where to bid, and **it is a file nobody can buy.** Make
it trivially exportable to CSV. Never let a migration drop rows.

### 4.5 What must stay manual

Do not automate these. They are judgement or they are legally hers:

- Submitting the bid on the platform (she does it; the system proposes a price)
- Signing anything
- The habilitação document pack
- Deciding to accept a tender the rules flagged as marginal

---

## 5. THE DATA RAILS — every endpoint, verified 19 Sep 2026

### 5.1 PNCP — two API families, and their availability INVERTS

This is a trap that cost a previous session a full re-run. **There are two PNCP APIs and they fail
independently.**

**Family A — `api/consulta/v1` (the documented public API)**
```
GET https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao
    ?dataInicial=YYYYMMDD&dataFinal=YYYYMMDD
    &codigoModalidadeContratacao={6|7|8}
    &pagina=N&tamanhoPagina=...
```
Modalidades: **6 = Pregão Eletrônico · 7 = Pregão Presencial · 8 = Dispensa**.
Verified today: **HTTP 200, but slow — 21,8 s for one page of 10.**
`CLAUDE.md` records this family rate-limiting hard (429 on 744 of 821 calls) on a previous date.

**Family B — `api/pncp/v1` (the portal's own API)**
```
GET https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens?pagina=&tamanhoPagina=
GET .../itens/{numeroItem}/resultados      # ONE row: the winner. Never the losers.
GET .../arquivos                            # the edital PDF and annexes
```
`CLAUDE.md` records this family as "far more tolerant."
**Verified today: HTTP 503.**

**Then both were retested three times over ~2 minutes, same session:**

| Attempt | `api/pncp/v1` | `api/consulta/v1` |
|---|---|---|
| 1 | **HTTP 000** (timeout) | **HTTP 000** (timeout) |
| 2 | **HTTP 503** | **HTTP 500** |
| 3 | **HTTP 503** | **HTTP 000** |

⇒ **PNCP is genuinely unreliable, on both families, at the same time.** The 503 body is empty. This is
not rate-limiting you can tune around; it is an availability problem you must engineer around.

> ### ⇒ BUILD ONE CLIENT THAT KNOWS BOTH FAMILIES, WITH FALLBACK, EXPONENTIAL BACKOFF, A PERSISTENT
> ### CACHE, AND A RESUMABLE CURSOR. Never write a harvester that assumes either family is up.
> Cache every successful response to disk keyed by URL. A re-run must cost zero calls for data
> already held. Log which family served each row, and record every failure with its status code so
> outages are visible rather than silently producing a short harvest.
>
> **A harvest that returns fewer tenders than yesterday is a suspected outage, not a quiet market.**
> The digest must say "harvested N of an expected ~M" and flag the shortfall. A silent partial
> harvest is the single easiest way for this system to lose a winnable tender.

**Item-level access on a municipal tender is mandatory** — see §7.5, CATMAT is null at municipal level,
so the only way to know what a município is buying is to read `descricao` on each item.

### 5.2 Price history — `dadosabertos.compras.gov.br`

```
GET https://dadosabertos.compras.gov.br/modulo-pesquisa-preco/1_consultarMaterial
    ?tipo=codigoPdm&codigo={PDM}&pagina=N&tamanhoPagina=500
```
`tamanhoPagina` **must be 10–500**. Verified today: **HTTP 200, 2,0 s.**

Find a PDM by grepping `3_consultarPdmMaterial` (≈19.500 PDMs, paged 500 at a time).

⚠ **This endpoint silently returns ~5 YEARS of history with no recency filter.** An "annual" pool
computed off a raw pull is overstated ~3×. **Always filter `dataResultado`.**

⚠ **The federal painel carries only 38,3% municipal lines on kit components, while the kit market is
97% municipal.** For municipal sizing, use PNCP items, not this endpoint. Use this endpoint for
*price history on a spec*, not for market size.

### 5.3 Buyer payment risk — SICONFI. Free, national, keyless, one call per buyer.

```
GET https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo
    ?an_exercicio=2026&nr_periodo=3&co_tipo_demonstrativo=RREO
    &no_anexo=RREO-Anexo%2007&co_esfera=M&id_ente={cod_ibge}
```
Verified today: **HTTP 200, 1,6 s.**

Returns the prior year's **restos a pagar PROCESSADOS** — invoices already delivered, attested,
liquidated and **unpaid** — split into inscritos / pagos / cancelados / saldo. That is literally
*"how much of what suppliers already earned has this buyer actually paid."*

CNPJ↔IBGE join, also free, **matched 699 of 699 kit-buying municípios**:
```
GET https://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes
```
Verified today: **HTTP 200, 866 KB.** Cache it; it changes rarely.

Measured on 148 of the 200 largest buyers: **median 76,7% paid, p25 44,9%, p10 23,5%.** 43,2% still
owed >30% of the prior year's liquidated invoices at mid-year; 29,1% owed >50%. **But only 6,1% wrote
off more than 5% — so the risk is DELAY, NOT DEFAULT.**

**Rule: reject where `saldo ÷ inscritos > 0,30` or `cancelados > 0,02`.**

Back it with RGF Anexo 05 for *Disponibilidade de Caixa Líquida*:
`&no_anexo=RGF-Anexo%2005&co_poder=E` — resolved at 9 of 10 random small municípios.

⚠ This is **no longer proprietary**: SIGA Pregão ships the same idea as "Pagômetro" at 12× R$389,42.
She gets it free. It is not a moat; it is table stakes.

### 5.4 Company lookup — `publica.cnpj.ws`

```
GET https://publica.cnpj.ws/cnpj/{cnpj14}
```
Verified today: **HTTP 200, 0,5 s.**

⚠ **`minhareceita.org` and `brasilapi.com.br` SILENTLY REDACT the email field** — verified `None` for
Petrobras and Magazine Luiza, which `publica.cnpj.ws` serves intact. **A fill rate measured through
either is a FALSE ZERO and it fails in the direction of a kill.** Use `publica.cnpj.ws`.

### 5.5 What does NOT exist — do not waste a day looking

- **Per-invoice municipal payment data.** PNCP `/contratos/{ano}/{seq}/faturas` returns **404**.
  `contratos.comprasnet.gov.br/api/contrato/{id}/faturas` works but is **federal UASGs only**.
  SICONFI (§5.3) is the only municipal rail.
- **Losing bids.** §4.4.
- **A national payment deadline.** It is in the buyer's own municipal decree, inside the edital. §8.
- **Some large state programmes are not on PNCP at all** — Paraná's *Nascer Bem* is absent under every
  keyword tried; the R$18,98M *"Kit Maternidade Mãe Gaúcha"* has a contract on PNCP and no matching
  edital. Accept the gap; do not build around it.

### 5.6 Rail hygiene, non-negotiable

- `ordenacao=-data` on `/api/search/` **does NOT sort by date** — results are relevance-ranked.
- `/api/search/`'s `total` field is a **fuzzy-OR match count, NOT a market size.** Any number taken
  from it is wrong.
- Always send a browser `User-Agent`. Several endpoints behave differently without one.
- The environment routes HTTPS through a proxy with a CA bundle at `/root/.ccr/ca-bundle.crt`.
  **Never disable TLS verification.** If a fetch returns HTTP 000, it is a timeout or a proxy issue —
  retry with backoff, do not "fix" it by turning off verification.

---

## 6. THE MEASUREMENT METHOD — five filters, applied to everything

**This is the most important code you will write.** Put it in `parse/normalise.py` and make every
aggregate in the system go through it. Nine measurement errors have been made on this data. Each of
the five filters below exists because of a specific one.

### Filter 1 — RECENCY
```python
rows = [r for r in rows if r['dataResultado'] >= today - 365_days]
```
The price endpoint returns ~5 years silently. Without this, every pool is ~3× too large.

### Filter 2 — PIECES, not quantity
```python
pieces = quantidade * capacity_of(unidade, capacidadeUnidadeFornecimento)
```
Where `capacity_of` handles, at minimum:
- `capacidadeUnidadeFornecimento` when > 0 (often 0.0 — then fall back to the sigla)
- `C` / `CENTO` = **100**
- `MIL` / `MILHEIRO` = **1000**
- `CX`, `PCT`, `PACOTE`, `CJ`, `JOGO` = read the description for a pack count
- pack counts live in **free text**, not a field: `"FRALDA COM BAINHA - 3 UNIDADES"`,
  `"BODY COM DECOTE CANOA (2 UNIDADES)"`. PNCP items carry no capacity field at all.

**The unit trap has fired NINE times in this archive. Three of those were the previous session's own
output, within hours of writing the law warning about it.** Write a test for every unit sigla you
encounter.

### Filter 3 — DROP LOT-TOTAL ROWS
Brazilian buyers routinely type the **lot total** into `precoUnitario` with `quantidade = 1`.
Measured on one PDM: `qty=1, preço=R$673.553,00` for one pen (RJ); `qty=1, R$59.500` (MA).
**126 of 1.934 rows carrying R$2,33M of phantom value** — and they land in the smallest quantity
band by construction, because a lot entered as one unit *is* a quantity of one.

```python
lo, hi = plausible_window[sku]          # from config/skus.yaml
rows = [r for r in rows if lo <= r['unit_price'] <= hi]
```

Dropping these moved one band from R$5,34 to R$1,68 per unit and its annual value from R$1.004.109 to
R$12.980. **The published ladder's top rung was 98,7% data-entry error.**

### Filter 4 — SPEC CONTROL (material, size, capacity, sheet-count, brand grade)
**A PDM is a catalogue heading containing materially different objects at 2–10× different prices.**
A margin computed across them is manufactured out of nothing.

Worked failures, all real:
- **BANHEIRA** — priced at R$22,90, which is a **17,2 L "Sensitive Feminino"**, the cheapest of 24 on
  the page. Of 259 banheira lines, **131 state a capacity and the 20–25 L band alone is 115 lines /
  R$1.038.317**. At the cheapest *conforming* cost (R$29,71, 24 L) that band is **−13,4%**. The 17,2 L
  item conforms to **exactly ONE line in the country.**
- **CADERNO** — a 96-fl 1/4 brochura priced against a PDM whose top lines are a 200-fl hardback and an
  R$11.126-per-unit leather binder. Controlled: gross fell +23–28% → **+4,2%**, pool R$67,3M → R$5,47M.
- **APONTADOR** — a *simples* priced against a PDM that is **78% *com depósito***. The conforming
  market is **R$77.492 a year nationally**, not the R$3,0M it appeared to be.

⇒ **Before believing any margin, print the spec distribution of the PDM and ask which rows your
product actually conforms to.** `config/skus.yaml` must carry, per SKU: required material, size range,
capacity range, and an anti-pattern list.

### Filter 5 — DEDUPE, AND CHECK YOU HARVESTED ONE PROGRAMME
Of 7.549 rows in one kit harvest:
- **432 were duplicate shadow rows** (same `vt`, with `qt=0, vu=0`)
- **4.052 rows carrying R$155,7M were a MATO GROSSO SCHOOL-UNIFORM programme** swept in by keyword —
  *tênis escolar* R$17,6M, *camiseta* R$10,8M, *bermuda* R$10,5M. A `\bMEIA` regex pulled school socks
  in as "baby socks" at R$9,3M.

**Uncaught, the market would have been sized 3,7× too large.** Clean denominator: 3.065 rows, R$57,2M.

Also: **whole-kit and LOTE rows land inside component families** — a R$215.000
*"600 KITS CONTENDO: Banheira… Mamadeira…"* line was counted as FRALDA. Detect and exclude bundles
before computing a per-component median.

### 6.1 The rule that catches what the five filters miss

> **When a family's tail clears and its median does not, READ THE TAIL BEFORE BANKING IT.**

Worked failure: BODY showed R$1,08M clearing 50% against a −21% median. The two largest rows were
**"CONJUNTO BODY + BERMUDA"** and **"CONJUNTO BODY + CALÇA"** (Taiobeiras/MG, R$594.368 + R$384.120) —
**two-piece sets swept in by a `\bBODY` regex**, whose cost basis is two garments. Genuine single-body
clearing value ≈R$77k, not R$1,08M.

**Make `report/digest.py` print the top 5 rows behind any aggregate it reports.** Always.

---

## 7. THE TRAPS CATALOGUE — regression-test every one

`tests/test_traps.py` must contain one test per entry. These are not hypotheticals; each one
happened and each one produced a confidently wrong number.

| # | Trap | Test |
|---|---|---|
| 1 | Unit sigla ignored → per-piece price 30–50% wrong | Feed rows with `CX`, `C`, `MIL`, `PCT`, `capacidade=0.0` and assert pieces |
| 2 | Lot-total row inflates the smallest band | Feed `qty=1, price=673553` and assert it is dropped |
| 3 | 5 years of history counted as one | Feed rows dated 4 years back and assert excluded |
| 4 | Cross-spec comparison inside one PDM | Feed 17,2 L and 24 L bathtubs and assert they do not share a median |
| 5 | Regex family ≠ product family | Feed `"CONJUNTO BODY + BERMUDA"` and assert it is not classified BODY |
| 6 | Adjacent market swept in by keyword | Feed a MT school-uniform row and assert excluded |
| 7 | Duplicate shadow rows | Feed `qt=0, vu=0` duplicate and assert deduped |
| 8 | Bundle row inside a component family | Feed `"600 KITS CONTENDO:…"` and assert excluded from FRALDA |
| 9 | CATMAT null at municipal level | Assert the classifier never requires `catalogoCodigoItem` |
| 10 | Retail price mistaken for wholesale | Assert every `cost` row carries a supplier CNPJ and a verified_at |
| 11 | Interstate cost not loaded | Assert a non-SP supplier cost is loaded +6 points before comparison |

### 7.1 Whose cost basis is it?

**A trading name is not an address, and neither is membership of a São Paulo trade association.**
Verified: `atacadosaopaulo.com.br` → **Espírito Santo**; `oceanob2b.com` → **RS**;
`officesuprimentos.com.br` → **SC**; `rymo.com.br`, listed by the *São Paulo* sindicato itself → **AM**.

**Every cost row must carry the supplier's CNPJ and its real UF.** Non-SP costs get **+6 points**
(`LC 123 art. 13 §1 XIII h`) before any margin comparison.

### 7.2 A published wholesale price is not a wholesale price

Measured across three categories (papelaria, limpeza, newborn kits): **the published "wholesale" price
sits at or above what the state pays at the quantities where the money is.** The genuine distributor
tier is unpublished and worth **~45% off the best published price**.

⇒ The cost table must distinguish **published tier** from **account tier**, and the margin engine must
report both. See §9.

### 7.3 A catalogue price is a harder fact than a production cost

If you can find the finished object on a page with a buy button, that beats any cost you derive from
constants. Prefer observed catalogue prices.

### 7.4 Do not write the verdict before the data returns

A previous session committed "nine SKUs, two clear" with three of twelve pulls still downloading; the
missing three reversed the headline. **Do not report until every job you started has returned.**

---

## 8. THE BID RULES — implement as pure, testable functions

Each returns `(passed: bool, reason: str, evidence: dict)`. Thresholds live in `config/rules.yaml`.
**There is no pricing skill that rescues a tender she should not have entered. The filters ARE the
business.**

| # | Rule | Detection | Why — measured |
|---|---|---|---|
| **1** | Reject `LOTE ÚNICO` | `^\s*LOTE` on item description; or one item covering the whole object | Per-item lines clear at 97–100% of estimate; lote único at **36–63%**. Costs 15% of the funnel, saves 100% of the losses |
| **2** | Reject **numeric** atestado only | grep the qualificação técnica clause for a **percentage or quantity**. A *qualitative* atestado passes | Measured on 5 live editais: 1 quantitative, 2 qualitative, 2 none. A qualitative one is satisfied by **one prior sale of any size**, public **or private**. Rejecting all atestado clauses would discard most of the market |
| **3** | Reject `CONFORME MODELO DO ÓRGÃO` | literal grep | Custom spec, unsourceable |
| **4** | Reject assembled kits over ~18 items | count enumerated items in the description/TR | Too many sourcing points; the one priced 18-item kit came in at −3,1% |
| **5** | Reject deadlines she cannot hit | parse `prazo de entrega`; cross-ref `ufs.yaml` feasibility | Median 10 days, **31,2% at ≤5 days**. One live edital demanded **3 days** |
| **6** | Screen the buyer's payment record | SICONFI §5.3 | `saldo/inscritos > 0,30` or `cancelados > 0,02` → reject. Nhamundá/AM paid **0,0%** and published a R$2,12M kit tender |
| **7** | Flag lines ≤ R$80.000 | `valorTotalEstimado` per line | `LC 123 art. 48 I` reserves them **exclusively** to ME/EPP — **per item, not per tender**. One live ARP had 9 of 38 lines under the threshold and **all 38 flagged `Sem benefício`**. That is an impugnação ground: free, written, statutory |
| **8** | Price every line spec-controlled | §6 filter 4 | A 17,2 L vs 24 L bathtub is a 36-point margin difference |
| **9** | Extract the payment deadline from the buyer's own decree | grep the pagamento clause for `Decreto Municipal`, extract both numbers | **There is no national figure.** `IN SEGES/ME 77/2022` is federal only (art. 1º), reaching a município only for *transferências voluntárias* (art. 2º). Worked example: Paracatu/MG quoting Decreto 7.088/2024 — 5 + 15 working days ≈ 28 calendar days |
| **10** | Grep for `pagamento antecipado` | literal | `art. 145` permits it only where expressly in the edital. Rare — where it appears, the working-capital problem is zero |
| **11** | Log the bid | always | §4.4 |

### 8.1 Bid pricing

**Award ÷ estimate is flat across bands: median 0,75–0,80** (assembled 0,75 · components 0,80 ·
body+macacão 0,79), p25 0,52, p75 0,99, **~60% clear ≥70% of estimate.** Assembled kits are **not**
riskier to price than components. Use ~75% of estimate as the opening anchor, but **never bid below
the cost floor** computed by `price/bom.py`.

⚠ **Size against the HOMOLOGATED award, never the estimate** — the estimate is a pre-bid ceiling built
to be beaten. Haircut worsens with lot size: SE 37% · RO 42% · PB 68% against a municipal median of 79%.

### 8.2 Clauses that look like barriers and are not

Measured across 169 editais holding both full PDF text and award records, the **multi-state (≥3 UF)
win rate is HIGHER where the supposedly-protective clause exists**: amostra 43% vs 30% · entrega
parcelada 38% vs 30% · atestado 37% vs 31%. And the price is identical (median assembled-kit unit
award R$239,80 single-UF vs R$238,50 multi-UF).

**Test a suspected barrier against who actually wins before pricing it as one.**

`LC 123 art. 48 §3` is a **right of last look, not a 10% handicap.** `Decreto 8.538/2015 art. 9º II`:
where a local firm's offer is *"iguais ou até dez por cento superiores ao menor preço"*, it **may
submit a lower price** — the *empate ficto* shape. Her bid is never marked up. Prevalence: **10,8% of
222 kit editais.** Cost it as ~11% of the field lost to a last look.

---

## 9. THE COST TABLE — what is verified and what is missing

Supplier: **CONFECCOES EMILIO LTDA**, CNPJ 50.191.584/0001-06, Rua Mendes Gonçalves 181, Brás, São
Paulo/SP, active since 1978, CNAE 4642-7/01. Publishes per-unit prices with no login
(`emilio.com.br`), marked *"Preço exclusivo para compras com CNPJ"*.

### 9.1 Verified — 6 of the 17 BOM lines

| Item | Cost | Source |
|---|---|---|
| Banheira 24 L | **R$29,71** | Banheira Infantil 24L #BM2123, Monte Libano |
| Cobertor / manta | **R$12,18** | Manta Baby #88.04.0003, Sul Brasil |
| Pagão / macacão | **R$19,60** | Emilio macacão/conjunto |
| Body manga longa | **R$15,32** | Emilio body |
| Pano de boca | **R$8,47** | Pano de Boca Pinte e Borde #580856, Bublim |
| Toalha de banho | **R$17,47** | Toalha Fralda Muito Mimo #53-35, Minasrey (cheapest of 13) |
| *(also verified)* Fralda de pano | **R$2,452/peça** | Inconfral *Especial* 5-pack R$12,26 |
| *(also verified)* Toalha c/ capuz | **R$21,26** | #76143 Bublim — **2× the R$10,50 target, dead at this tier** |
| *(also verified)* Cobertor microfibra | **R$21,47** | Camesa — **−7,8%, a different product from "manta"** |

### 9.2 NOT VERIFIED — 11 of 17, ≈45% of the BOM by value

**`mochila / bolsa maternidade` — the most expensive item in the kit — is NOT STOCKED by the one
verified supplier and has no verified São Paulo price anywhere in this archive.**

Also unpriced: cueiro · fralda descartável RN (×1) · kit enxoval · par de meias · toalhas umedecidas ·
sabonete líquido · shampoo infantil · óleo infantil · kit higiene · saboneteira.

Estimated band for the eleven: **R$66,60–127,00**. BOM total **R$169,35–229,75** against R$359,05 ⇒
**+36,0% to +52,8%.**

> ### ⇒ CLOSING THIS IS STEP 0 AND IT GATES EVERYTHING. §12.

### 9.3 The account tier

The **~45% discount** off published is an **INFERENCE, not a quote** — derived backwards (Chamex
published R$30,60, the state pays R$19,83 in SP, so winners are invoiced at ~R$16–18). **Nobody has
been asked.**

Target prices for the supplier emails, each 20% under the spec-controlled state median in the band
where that SKU's money sits:

```
body            ≤ R$  8,40      macacão/pagão   ≤ R$ 13,70
toalha c/capuz  ≤ R$ 10,50      banheira 24 L   ≤ R$ 14,85
manta           ≤ R$ 10,00      mochila         ≤ R$ 25,00
```

### 9.4 Supply-side gates, already measured

- **All Nations**: *"no mínimo 1 ano de fundação"* + two years of accounts
- **Peixoto**: *"Para clientes novos, apenas… boleto/pix antecipado"*
- **VPA Atacadista** (Pari, SP): *"valor mínimo… R$600,00… a empresa deverá ter 12 meses de atividade"*
- **Flora Saúde** — the permissive end: *"avaliado pelo setor financeiro a partir da segunda compra…
  prazo inicial 21 dias"*

⇒ **SELECT SUPPLIERS BY CREDIT POLICY, NOT BY PRICE. Read the cadastro page before the price list.**
The strict end puts terms in month 13; the permissive end in month two. That single choice is the
difference between year one and year two, and it costs nothing but reading.

- **Brascol** (ONESHOP DISTRIBUIDORA, 1.480 body SKUs) and **Yanai** (44.040.459/0001-94, Brás/SP)
  both show *"Cadastre-se para ver o preço"* on every item. Register.

### 9.5 SKUs to exclude from every bid

**Mamadeiras and chupetas are certified under Portaria Inmetro 490/2014.** Keep them out of the SKU
set entirely. Textiles need only labelling (Portaria 118/2021); rigid baths are uncertified
(Portaria 563/2016 covers inflatable only).

### 9.6 Freight — UNQUOTED, and the paper study does not transfer

The measured freight study was run on **paper**: 3,6 kg, dense, R$4,72–10,04/kg at 28,8 kg. **A 24 L
banheira is ~0,5 kg actual and ships at DIMENSIONAL weight**; an assembled kit is a bag of air by
design. **Correios hard-caps a parcel at ~29 kg**, and every B2B road carrier — Braspress, Jadlog,
TNT, Total Express, Melhor Envio, SuperFrete, Kangu — **refuses to quote without a contract.**

The edital settles who eats it: Riachão do Bacamarte/PB PE 7/2026 cl. 9.8 — *"Não será admitida a
previsão de preços diferentes em decorrência do local de entrega do objeto"* — with *frete*, *CIF* and
*FOB* appearing **zero times in 43 pages**. **Freight is inside the single bid price.**

⇒ `price/bom.py` must carry a freight estimate per UF with an explicit `is_estimate=True` flag, and
the digest must show it separately. **Get one real quote before bidding anything heading north.**

---

## 10. VERIFIED REFERENCE NUMBERS

### 10.1 The market (12 months, deduped, uniform programme excluded)

| | |
|---|---|
| Homologated value | **R$57.201.985** *(independent cross-check: R$59,1M — 3% apart)* |
| Editais | **1.012** — 979 municipal · 6 estadual · 3 consórcio · **0 federal** |
| Distinct buying municípios | **699** |
| Publication rate | **~4,0 per working day** |
| Median homologated per edital | **R$31.080** |
| Judged on `Menor preço` | **96,4%** |
| Median notice | **10 working days**, 98,1% ≥5, 0 under 3 |
| Award ÷ estimate | median **0,75–0,80** |

⚠ **Three deflations that must travel with that number:** most of it is **SRP**, so
`valorTotalHomologado` is a *registered ceiling, not a sale* (the contract rail shows R$54,2M actually
contracted) · only 713 of 6.170 kit lines are assembled-kit lines against 5.457 component lines ·
**25% of kit tenders are invisible to a title search** and reachable only by descending to `/itens`.

### 10.2 The assembled-kit band

**R$11.110.510 · 19,4% of the market · median award R$288,00 · 158 lines · 91 winners · 75,1% ME/EPP
by value · median winner-year R$60.520.**

### 10.3 The clearing pool, spec-controlled, at the published tier

**R$4.380.049 across 147 municípios — but Coari/AM alone is R$1.522.728 (34,8%)**, and the top 10
municípios are 63,4%. **Ex-Coari the pool is R$2,86M.**

Required share for R$360k of billings: **8,2%**, or **12,6% ex-Coari.** Both inside
`THE MARKET-MULTIPLE RULE` (15–25%).

### 10.4 The competitors — CNPJ-verified, and the model is PROVEN not vacant

| Firm | CNPJ | Porte | Reach | 12-month |
|---|---|---|---|---|
| **CONDAFE COMERCIO DE ROUPAS** | 10.430.444/0001-10 | EPP, São Paulo/SP | 15 UFs, 36 municípios, 44 editais | **R$6.135.997** — R$2,44M of it in the assembled band |
| AMA COMERCIO E SERVICOS | — | EPP | 16 UFs, 38 editais | — |
| DEBECHE + HIGI TEX | — | ME | 14 and 9 UFs — **the same operation** (`roberto.daud@uol.com.br`) | — |
| **J.J.A. ENXOVAIS** | — | ME, **registered 17 Jan 2024** | MG, MS, PR, SP | — |
| BRINK MOBIL | — | Demais, capital R$32.018.254 | — | **avoid** — takes R$5,66M of body+macacão |

**92,2% of 451 winners are single-UF by headcount, while the 7,8% multi-UF firms take 33,6% of the
value.** Median winner takes R$22.474 and **78,5% win exactly one edital a year.**

⇒ **Never write a pitch claiming the space is empty. It is not. It is proven, and a two-year-old ME
with R$10.000 of capital is already running the playbook.**

### 10.5 Real closed tenders — use these as fixtures in your tests

| Município | Object | Qty | Cleared at | Winner |
|---|---|---|---|---|
| Itaquaquecetuba/SP | Kit maternidade 17 itens *(est. R$476,05)* | 5.000 | **R$359,05** | CONDAFE |
| Campos dos Goytacazes/RJ | Kit bebê montado | 1.560 | **R$353,07** | MULTI MAIS |
| Maués/AM | Kit enxoval montado | 1.265 | **R$298,00** | F. B. PEREIRA |
| Icatu/MA | Kit enxoval RN | 1.172 | **R$296,84** | J E C DA COSTA NETO-ME |
| Marília/SP | Kit enxoval *(est. R$392,81)* | 2.112 | **R$149,00 — −62%, DO NOT BID** | COMERCIAL DINASTIA |
| Coari/AM | Banheira anatômica PP | 12.960 | **R$62,70** *(cost R$29,71)* | — |
| Coari/AM | Macacão de soft | 12.960 | **R$43,00** *(cost R$19,60)* | — |
| Aracaju/SE | Pagão 100% algodão | 3.750 | **R$40,00** *(cost R$19,60)* | — |

PNCP keys for the first two, for direct fetching:
`46316600000164-1-000447/2025` (items 1 and 2) · `44477909000100-1-000330/2026` (item 1).

### 10.6 The 17-item BOM (Itaquaquecetuba, real)

mochila · banheira lisa · cobertor infantil · cueiro · pagão · fralda descartável RN · body manga longa ·
kit enxoval · pano de boca · par de meias infantis · toalha de banho infantil · toalhas umedecidas ·
sabonete líquido · shampoo infantil · óleo infantil · kit higiene do bebê · saboneteira

---

## 11. WHAT IS NOT VERIFIED — carry these forward honestly

| Open question | Why it matters | How to close |
|---|---|---|
| **11 of 17 BOM lines unpriced**, worst is the mochila | 45% of the cost estimate is a band, not a measurement | One afternoon of catalogue work. **This is Step 0** |
| **The ~45% account discount is an inference** | It decides whether the full basket or only three SKUs is live | 15 supplier emails, §9.3 targets |
| **Freight on low-density goods** | Could be 2% or 15% of line revenue | One real quote to a Northeast capital |
| **Win rate** | Structurally unmeasurable in advance | Bid small, log everything, know in 90 days |
| **Coari concentration** | 34,8% of the clearing pool is one buyer | Always report ex-largest-buyer |
| ICMS position after the 1 Jul 2026 ST revocation | Net uncomputed for this category | Accountant |
| Substituição tributária on interstate purchases into a Simples ME | Unbudgeted line; wholesalers warn of it on their own pages | Accountant |
| Whether SUAS fundo-a-fundo transfers are *transferências voluntárias* under IN 77/2022 art. 2º | If yes, a large slice of buyers falls under the faster federal 5+5 clock | One hour on the statute |
| **STF ADI 5464** suspended the EC 87/2015 DIFAL for Simples senders | Should mean no extra state tax on her interstate sales | UNVERIFIED as applied |
| That `IN RFB 1.234/2012 art. 4º XI` reaches the new art. 2º-A | IRRF withholding at source | No COSIT ruling found. **File the Anexo IV declaration with every body regardless** |

---

## 12. BUILD SEQUENCE — with acceptance criteria

**Do them in order. Step 0 gates everything else.**

### STEP 0 — Close the cost table *(no code; half a day; R$0)*
Price the other 11 BOM lines at `emilio.com.br`, Brascol, Yanai and two more Brás sellers.

> **ACCEPTANCE — bar committed in advance: BOM total ≤ R$200** → the margin is real at prices
> obtainable today; proceed to Step 1.
> **R$200–230** → proceed, but the supplier account becomes the first priority.
> **> R$230** → STOP building. Send the 15 supplier emails (§9.3) and decide on the answers.

### STEP 1 — The PNCP client *(the foundation; everything depends on it)*
`harvest/pncp_client.py`: both API families, fallback, exponential backoff, disk cache keyed by URL,
resumable cursor, structured logging of which family served each row.

> **ACCEPTANCE:** fetch one full day of modalidades 6/7/8 nationally, twice. The second run makes
> **zero network calls**. Kill it mid-run and restart — it resumes without duplicating.

### STEP 2 — Normalisation and the trap tests
`parse/normalise.py` + `tests/test_traps.py`.

> **ACCEPTANCE:** all 11 trap tests in §7 pass. Reproduce the known-good market figure:
> **R$57,2M ± 5% across 1.012 editais** from a fresh harvest. If you cannot reproduce it, your
> normaliser is wrong — do not proceed.

### STEP 3 — SKU classification and spec control
`parse/spec.py` + `config/skus.yaml`.

> **ACCEPTANCE:** classify the 3.065-row clean set. Assert **banheira splits by capacity band** and
> the 20–25 L band shows **−13,4%** at R$29,71. Assert `"CONJUNTO BODY + BERMUDA"` is **not** BODY.

### STEP 4 — The edital parser
`parse/edital.py`: fetch `/arquivos`, extract text, grep the clauses rules 1–5 and 9–10 need.

> **ACCEPTANCE:** on the five known editais, correctly classify the atestado clause as
> quantitative / qualitative / absent, and extract Paracatu/MG's **5 + 15 working days** from its
> Decreto Municipal 7.088/2024 citation.

### STEP 5 — The rules engine and buyer screen
`screen/rules.py` + `screen/buyer.py`.

> **ACCEPTANCE:** run all 11 rules over 30 days of harvested tenders. Every rejection carries a
> human-readable reason and its evidence. Assert **Nhamundá/AM is rejected** on SICONFI.

### STEP 6 — The margin engine
`price/cost.py`, `price/bom.py`, `price/margin.py`.

> **ACCEPTANCE:** price the Itaquaquecetuba 17-item tender and return **+36% to +53%** with the
> published-tier cost table, and separately with a 45% account discount. Freight must appear as a
> distinct, flagged estimate.

### STEP 7 — The bid log and the digest
`log/bidlog.py` + `report/digest.py`.

> **ACCEPTANCE:** a single daily email/file she can read in five minutes: N tenders seen, N passed,
> each with município, object, quantity, suggested bid, computed gross, buyer payment score, and the
> deadline. Every aggregate prints its top-5 underlying rows.

### STEP 8 — Deploy
~R$30/month VPS, cron at 06:00, SQLite on disk, daily backup of `acolhe.sqlite` and the bid log off-box.

> **ACCEPTANCE:** runs unattended for 14 consecutive days. She reads the digest and nothing else.

---

## 13. THE COMPANY — legal and fiscal setup checklist

Not code, but the machine is useless without it. Costs ≈R$1.500–2.500 one-off.

- **Contador** — R$200–400/month. Non-negotiable.
- **ME on Simples Nacional, Anexo I.** Effective rate **4,00%** at RBT12 R$180k · **5,65%** at R$360k ·
  **6,73%** at R$500k · **7,58%** at R$720k.
  **MEI is arithmetically dead**: ceiling still R$81.000 (`LC 123 art. 18-A §1º`; LC 227/2026 did not
  touch it), and Resolução CGSN 140/2018 Anexo XI contains *"ATACADISTA"* **zero times**.
- **Register SEVERAL CNAEs** — vestuário, enxoval, higiene pessoal, brinquedos. A tender can
  disqualify a bidder whose registered *objeto social* does not cover the object. Real, avoidable loss.
- **Capital social R$20–30.000 integralizado.** Her own money, not a fee. It caps what any edital may
  lawfully demand (`art. 69 §4º`) and makes the opening balance sheet clear LG/LC/SG > 1.
- **Certificado digital e-CNPJ A1** — ~R$200–300/year. Required to bid.
- **Conta PJ** — Cora or Nubank PJ, free.
- **Five free platform registrations** reach **74,3%** of open kit tenders; eight reach 82,9%:
  Compras.gov.br/SICAF · Portal de Compras Públicas · BLL · BNC · Licitanet.
  `art. 87 §2º` **prohibits** a município demanding its own complementary cadastro.
  Bidding is **R$0 on Compras.gov.br**; **BLL charges 1,5% capped R$600 ONLY IF SHE WINS**.

**Two feared blockers that are not blockers**, both settled in law:
- `Decreto 8.538/2015 art. 3º` — no balanço patrimonial may be demanded of an ME/EPP for
  *bens para pronta entrega*.
- `Lei 14.133 art. 65 §1º` — a company created in the year of the licitação substitutes a
  **balanço de abertura**. And `art. 69 §2º`: *"é vedada a exigência de valores mínimos de faturamento
  anterior."*
- Measured: **0 of 5 live kit editais demanded capital social, PL mínimo, garantia de proposta or
  garantia de execução.**

**Levers only an ME/EPP holds:**
- `art. 141 §1º II` — jump the chronological payment queue on demonstrated risk of discontinuity
- `art. 141 §3º` — every body must publish its payment queue monthly
- `art. 137 §2º` — right to terminate on *atraso superior a 2 meses*

**Operational, easy to get wrong:**
- **File the `IN RFB 1.234/2012` Anexo IV declaration with every contracting body** or be withheld at
  source. `IN RFB 2.145/2023` inserted art. 2º-A obliging municípios to withhold IRRF on goods; the
  carve-out is art. 4º XI (Simples) and art. 6º requires the declaration **per contract**.
- **Put the empenho number on the face of the nota fiscal.** A wrong NF restarts the entire cash cycle
  (Paracatu item 11.1.2 recounts from resubmission).

### 13.1 Working capital

R$15.600 available. **It is not stock money — it is gap money**: she pays the wholesaler ~day 11 and
the buyer pays ~day 45, so ~34 days to cover.

**Express capital as concurrent lots, never as a float figure.** One median edital is R$31.080; the
cycle is ~45 days:

| | COGS/lot | Float | Terms | Concurrent lots | Billings/yr |
|---|---|---|---|---|---|
| 52% gross | R$14.918 | R$15.600 | **none** | **1,0** | R$263.611 |
| 52% gross | R$14.918 | R$15.600 | **28d** | **2,8** | **R$697.794** |
| 52% gross | R$14.918 | +R$20k credit | none | 2,4 | R$601.574 |

**28-day supplier terms buy more concurrent capacity than R$20.000 of borrowed money, and cost
nothing.** Pursue terms first; credit only if terms are refused.

If credit is needed: **FGI PEAC** is the only Brazilian instrument whose published eligibility a
company with no history passes (BNDES FAQ Q4/Q11: no minimum revenue, no minimum time in business,
guarantees waived; minimum R$1.000; 48 agents incl. Stone, Nubank, Sicoob, Sicredi). **Take R$15–20k
once and no more** — above ~R$35k of float, capital stops binding and win count binds.
⚠ **No agent publishes a rate.** Budget against BizCapital's published unsecured CET of
**2,91–6,60% a.m.** — R$20.000 costs R$8.218–23.064/yr. **UNVERIFIED.**

⚰ **Dead, do not reopen:** Cartão BNDES (*"Capital de giro não é item financiável"*) · Pronampe
(capped by capital social, not revenue) · secured PJ cards (reshuffles her own money) · cessão de
crédito outside AntecipaGov (PGDF Parecer 525/2022: *"IMPOSSIBILIDADE"*) · SEBRAE (does not lend).

---

## 14. WHAT ALREADY EXISTS IN THIS REPO

| File | What it is |
|---|---|
| **`THE_KIT_DESK.md`** | The business case, 475 lines, every source URL. **Read this second.** |
| `ACOLHE_Business_Overview.docx` / `.pdf` | 13-page overview for the founder, English |
| `ACOLHE_Uma_Leitura.docx` / `.pdf` | 2-page brief for the founder, Portuguese. What she has actually read |
| `ACOLHE_Site.pdf` | The institutional website, 3 screens, rendered |
| `brand/site/` | The website source (`.dc.html` × 3 + `canvas.json` + `mkpdf.py`) |
| `brand/` | Logo and figure sources (`img1.py`, `img2.py`, `build.js`) |
| `THE_KIT_REMEASUREMENT.md` | ⚠ **Superseded.** It measured components only and wrongly declared the market dead |
| `THE_BUSINESS.md` | The capital→margin arithmetic that selected this market |
| `CLAUDE.md` | The repo's working rules and ~150 derived laws |

**Brand:** ACOLHE — *Enxovais e Suprimentos para o Setor Público*.
Legal entity `ACOLHE COMÉRCIO DE ENXOVAIS LTDA`.
Colours: teal `#1F4E4A` · terracotta `#C96F4A` · cream `#F7F3EC` · sage `#8FA89B` · charcoal `#2B2B2B`.
Type: Fraunces display over Manrope body.

### 14.1 Repo conventions — these are enforced

- Develop on branch **`claude/volta-architecture-design-txe8r5`**. Push with `git push -u origin <branch>`.
- **Do not open a pull request unless explicitly asked.**
- **Never put a model identifier in a commit message, a PR, a code comment, or any pushed artefact.**
- **Every number needs a primary-source URL.** Write **UNVERIFIED** explicitly where one cannot be had.
  A flagged gap is worth more than a plausible figure.
- **Never cite SEO content farms or vendor marketing as evidence a requirement exists.**
- **Observed listings beat published claims.**
- **When a correction lands, propagate it to every claim that depends on it.**

---

## 15. THE FIVE THINGS MOST LIKELY TO GO WRONG

1. **You believe an aggregate you did not filter.** Nine times out of nine, the unfiltered number is
   flattering. Run §6 and print the top-5 rows behind every figure.
2. **You build against one PNCP API family and it goes down.** Both were checked today; one was 503.
   Build the fallback in Step 1, not later.
3. **You price a cost against the wrong spec.** A 17,2 L bathtub against a 24 L market is 36 margin
   points of fiction. Spec control is not optional.
4. **You automate something that must stay hers** — signing, submitting, or a decision the rules
   flagged as marginal.
5. **You start building before Step 0 returns.** If the BOM comes in over R$230, the thing to build is
   different. **One afternoon of catalogue work decides the shape of the whole system.**

---

**Start at Step 0. Nothing else matters until that number is in.**
