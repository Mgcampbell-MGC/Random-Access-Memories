# FIND A BUSINESS — BRIEF V4

**For an independent LLM. Written 13 August 2026, after 59 dead candidates.**
**Read the whole thing before you generate anything. Most of it is the record of what has already
been tried and exactly why it failed. Proposing something already in here is the single most common
failure mode of previous attempts — four external LLMs have contributed candidates and all four
died, three of them to laws written below.**

---

## 0. THE JOB

Find a business a specific Brazilian woman can start, alone, with a few hundred dollars, that nets
her **R$12.000–15.000/month within about a year and R$30.000/month within three.**

You are not being asked for a list of ideas. You are being asked for **one to three candidates, each
with a measured buyer pool, a price, a customer count, a named competitive field, and an honest
statement of how it dies.** A candidate without a real number in it is worthless here — sixty have
already been produced and killed.

---

## 1. THE FOUNDER

- ~26, woman, São Paulo, Brazil. New Brazilian CNPJ, and access to a US company. Stripe, Pix and
  boleto all work.
- **Budget: a few hundred US dollars. Total.** No capital, no runway assumption, no investors.
- **No domain expertise in anything.** Do not design a business that requires her to be, or be
  believed to be, an expert. Her expertise is the ability to research and to build with AI. Assume
  she can ship software but knows nothing about any industry until she reads about it.
- Portuguese native. **Will not take unscripted live calls in English, ever.** A business whose
  customers are American or British is worth zero to her regardless of how good it is.

### Hard constraints — these have never moved and will not

1. **FACELESS, PERMANENTLY.** No camera, no personal brand, no influencer or creator work, no
   webinars, no "build an audience" as a route to market, no name on anything. **An anonymous or
   company-branded presence IS allowed** — a company site, a topic page, ads, a brand with no human
   face attached. The precedent is a product marketed under a company handle rather than a founder's.
2. **Her personal São Paulo network is not a sales channel.** Do not propose anything that starts
   with "she asks people she knows."
3. **No employees and no contractors.** Ever. Not at any revenue level in the three-year plan.
4. **No custody of any customer credential, certificate or password.** This killed an entire
   category. A faceless unknown asking a stranger for their e-CNPJ certificate or gov.br login
   inverts the trust gradient and cannot be sold.
5. **No steady-state daily phone work.** She will do a bounded validation round of a couple of
   weeks and then never again. **The operating business must run as a system.**

### Constraints that were relaxed on 13 August 2026 — use this room

6. **Income target**: was R$30.000/month net in 12 months. Now **R$12.000–15.000/month net
   near-term, R$30.000 over ~3 years.**
7. **Founder labour**: was "no per-transaction founder labour", absolute. Now **a per-customer human
   step is permitted, provided total labour at target customer count stays under ~10 hours/week.**
   Onboarding, setup, manual exception review, hand-delivery before automation — all now legal.
   Still forbidden: anything needing employees, and anything whose labour becomes full-time before
   the target is reached.

### The channel, corrected 13 August 2026

**Brazilian B2B runs on WhatsApp, not on the telephone.** The record spent months assuming that a
97,2% landline fill rate in the Receita Federal base meant reachability. **Having a landline and
answering a cold call are different facts.** Design the go-to-market as: a one-page site plus a PDF
(launchable same-day), personalised cold WhatsApp sent by hand at low volume, and click-to-WhatsApp
ads where the prospect messages first.

**And know the wall:** Meta's Business Messaging Policy requires opt-in for business-initiated
messages. One candidate (BALCÃO) died failing opt-in, display-name matching and impersonation rules
simultaneously. Cold outreach must be human-sent from the WhatsApp Business app at 15–20/day from a
warmed number, never the Cloud API and never a bulk tool. Product messaging must be opt-in by
construction: the customer sends the counterparty a link, **the counterparty writes first**, and
reminders go as **UTILITY** templates (measured R$0,035 each, ~2,3% of subscription revenue), never
MARKETING.

---

## 2. THE ARITHMETIC — this is the most important section

Net R$12.000–15.000/month needs about **R$13.500/month gross** after Simples (~6%) and infra.

| Price/month | Customers needed | Segment size where that is ≤1% |
|---|---|---|
| R$397 | 34 | 3.400 |
| R$997 | 14 | 1.400 |
| R$1.500 | 9 | 900 |
| **R$2.500** | **6** | **600** |
| R$4.000 | 4 | 400 |

**The rule: she needs ~100 customers to be impossible and ~6 to be plausible. Required penetration
must be at or under roughly 1% of the real buyer pool.** Above that she needs market leadership,
which a solo founder with no capital and no face does not get.

### The price band was never a fact about Brazil

The record spent 58 candidates inside a R$150–700/month band. **That band is a property of SMALL
buyers, not of the country.** Measured counter-evidence: Dynadok's own ROI calculator uses
**R$12.800/mês** for one construtora; Auvo sells at R$529,70/mês for three seats; Sertras plans run
to R$4.857/ano; SmarterCerts (US) charges US$210–335/month with **no free tier**; an Analista de
Documentação in Brazil (CBO 261210) costs **R$4.323,84 média, ~R$7–9k loaded**.

**Design at R$1.500–4.000/month against a buyer big enough to justify it.** This is not optional
advice — it is the difference between a searchable space and one already searched to exhaustion.

### Why the expensive/small quadrant is the only one left

**Every kill mechanism in this record is a VOLUME mechanism.**
- A clearing party funds free software where the *flow* is large. It will not bother with a
  2.000-firm segment.
- A lead-magnet incumbent produces free content for *large* audiences.
- A vertical ERP at R$99–299/month only exists for trades with tens of thousands of firms.
- A free tier is customer acquisition for a market *worth acquiring*.

> **59 candidates hunted cheap software for large populations — precisely the quadrant where free
> competitors are structurally guaranteed. Hunt expensive software for small populations. It sits
> beneath everything that killed us.**

---

## 3. THE GAUNTLET — run these in this order, cheapest killer first

**Test 1 runs first, always. Three candidates passed every other test and then died on a number
obtainable in an afternoon.**

### 1. POOL
How many **real operating firms**, not CNPJs? Then: customers-needed-at-your-price ≤ ~1%?

Two traps that have each killed multiple candidates:
- **THE CNAE-MIRAGE LAW.** A CNAE count is not a buyer count. Check IBGE Concla class notes for what
  the code actually contains (one "trade marketing" code turned out to be a catch-all including
  fulfilment). Check MEI dilution — **MEI phone reachability is measured at 0%**, non-MEI 63,3%,
  EPP+ 97,5%. And check the MEI occupation name in Anexo XI of Res. CGSN 140/2018: **if it reads
  "…independente", the code is counting the workforce, not your buyer.**
- **THE SCALE SCISSORS.** *The segments where the job is big enough have too few firms; the segments
  with enough firms have firms too small to have the job.* Measured: **every visit-based Brazilian
  service segment has a mean firm of 2–5 people.** In construction, the stratum with the pain was
  4.042 firms while the stratum with the pool subcontracted R$11.263/month — about one supplier, a
  twenty-minute job. **Check the SIZE DISTRIBUTION, not just the count.**

### 2. PAIN
Is there a **first-person account, in Portuguese, from a real buyer**? Not vendor marketing. Two
candidates died because six separate interrogations could not find one person describing the loss.

### 3. SHIPPED — and note the correction
**CORRECTED LAW A1, adopted 13 Aug 2026:** *an incumbent kills only when **(a)** its version is
**FREE**, or **(b)** its measured adoption inside the specific target segment exceeds roughly 20%.
"A vendor exists and has a landing page" is a price and positioning constraint, not a kill.*

Supporting data: **Cetic.br TIC Empresas 2025 — 36% ERP adoption. Sebrae 2025 — 53% of small firms
still on spreadsheets, in the best year ever recorded.**

**But search properly. LAW A: "no competitor found" is a claim about the searcher, not the market.**
Vendors write in formal/regulatory vocabulary and you must find their word. Worked example: the
Brazilian term for supplier delivery follow-up is **"diligenciamento"**, not "follow-up" — a search
in the wrong word returned an empty field that was actually occupied by a dozen vendors.

### 4. FREE — hunt this separately, by funding model
**LAW C:** a competitor search is implicitly a search for **vendors**, and a vendor is someone who
charges — so a free competitor has no pricing page, no Capterra row and no keywords. **It cannot be
found by searching for a product. It must be found by asking "who would give this away, and why?"**

This law was bought expensively: a candidate cleared by 17 agents including a dedicated adversarial
verifier running 20+ vendor-vocabulary queries was killed by the founder with **one link** — a
competitor whose own copy read *"Free isn't a trial or a teaser for a paid plan — there is no paid
plan"*, funded by a 5% margin on the goods flowing past it.

**Free kills at any price and any target. Zero excludes nobody, and the adoption correction in test
3 has no force against it.**

### 5. REGULATOR (LAW B)
Does the regulator build and mandate its own tool, free? Killed at least five candidates — Inmetro's
PSIE, the US National Board's EDT, SINIR's MTR (*"eletrônico, numerado, autodeclaratório e
gratuito"*), the ANTT insurance webservice, Lei 14.133 art. 141 §3º publishing the public payment
queue by statute.

**THE ENUMERABILITY TRAP:** a population enumerable *because a regulator registers it* has usually
already had its task systematised free by that same regulator.

### 6. HUMAN (LAW 6)
Brazilian benchmarks: secretária R$1.600–2.500/month · contador R$300–800/month · analista ~R$3.400
· Analista de Documentação R$4.324 média (~R$7–9k loaded). **At R$2.500/month this is now a fair
fight; at R$397 it never was.** This test weakened when the price band moved — use that.

### 7. CLEARING PARTY (LAW 0)
> **Whoever earns margin on goods, payments, bookings, credit, insurance or advertising flowing past
> your product WILL give that software away free, permanently.**

Predictor: **does this buyer's customer pay across a counter terminal?** If yes, an acquirer funds
vertical software to zero. Law 0 is a property of the **segment**, not the candidate.

**Two corrections you must apply:**
- **It is a TEST, not a PRE-FILTER.** Run as a pre-filter it closed 6 of 7 candidate segments before
  any candidate existed and produced two consecutive zero-yield waves.
- **A clearing party can only fund the version that serves its own flow**, and only bothers where
  the flow is large. Worked example: supply-chain finance monetises the *nota fiscal receivable*, not
  a labour document dossiê — so it does not fire on the dossiê.

### 8. CHAT WINDOW — the measurement that closed an entire class
A general chat model was tested against a candidate's core value: **38/38 planted discrepancies
found, 0 false positives, across ~380 checks.** And the old exemptions have expired — **OpenAI
shipped a Scheduled Tasks hub on 17 June 2026**, so *"it runs on a timer"* and *"it remembers"* are
consumer features now.

> **A chat window has exactly one user, one account, one moment. It acts only inside its user's
> account, with its user's consent, on its user's data.**

A candidate survives only if its value depends on at least one of:
1. **THIRD-PARTY OBLIGATION** — someone who is not the customer, and who agreed to nothing, must act.
2. **SHARED STATE** — a status a second party reads and is bound by.
3. **CUSTODY FOR A LATER PARTY** — a record a court, auditor, insurer or client *demands* as
   evidence. (Corollary: **an audit trail nobody demands has no price.**)
4. **AN IRREVERSIBLE ACT** — money released, access revoked, a batch released.

> **One-line screen: if the whole product still works when only the buyer ever touches it, it is a
> chat window.**
> **Corollary: "unattended" alone is no longer a differentiator — only *unattended against somebody
> else* is.**

---

## 4. THE REST OF THE LAW SET

Each was bought with at least one corpse.

- **LAW 1 — THE LEAD-MAGNET MECHANISM (7 kills).** Content costs nothing to produce, so a funded
  incumbent's free tier IS its marketing budget. **Anything that is content — a guide, a template, a
  checklist, a corpus, a course, a report — is dead on arrival.**
- **LAW 7 — THE VISE (6 appearances).** The legally safe version has no differentiation; the
  differentiated version is legally exposed. Watch this in Brazil specifically: **CFC/DL 9.295**
  reserves accounting judgement (art. 25(c), art. 15 *"sob qualquer forma"*), **OAB** reserves legal
  theses, **CONFEA Res. 218/1973** reserves technical equivalence judgements. **The relaxed labour
  rule makes this MORE dangerous, not less** — the human check she could now perform is often
  precisely the reserved work.
- **THE SELLER-SIDE FUNDING LAW.** *If the party you chase is competing to SELL to your buyer,
  someone will charge that party for access and give the chasing tool to the buyer free.* Object &
  Order, Mercado Eletrônico (*"a empresa fornecedora paga uma taxa… o que faz a solução totalmente
  gratuita para compradores"*), Neogrid, SAP Ariba, Nimbi Private — **one mechanism, not five
  coincidences.** The chased party must be a **payee already under contract**.
- **THE GATEABLE-COUNTERPARTY LAW.** *Enumerability and solvency are properties of the BUYER.
  Gate-holding is a property of the buyer's COUNTERPARTY.* Check them together. 826.570 Brazilian
  government suppliers are enumerable, solvent and phone-reachable — and useless, because their only
  counterparty is the State, which cannot be gated.
- **THE COUNTERPARTY-MOTIVATION RULE.** A *coordination* job wants a motivated counterparty; a
  *chasing* job wants an **unmotivated** one. **If the document is how the counterparty gets paid,
  they are motivated and there is no chasing job.** Exception that matters: motivation is
  insufficient when the document is **burdensome or incriminating** to produce.
- **PRICE AND POOL MOVE IN OPPOSITE DIRECTIONS.** When the competitor is per-seat, escaping the
  crossover means raising price, which raises minimum client headcount, which drops the qualifying
  population into the top 2–7% of the segment. Measured in reverse too: raising price shrank the pool
  faster than the customer count in every segment tested except one.
- **THE FIELD-OWNERSHIP LAW.** *If what you sell can be described as one field changing value, ask
  who owns the record before you ask who the buyer is.* An approval gate is a status field on a
  record some system already owns — structurally a feature, not a product. (Brazil-specific: **CDC
  art. 40** makes a written orçamento with customer approval mandatory for every consumer service,
  which is why every trade's R$40–120/month app already ships approval.)
- **THE PRECONDITION TRAP (3 appearances).** If the product requires the discipline whose absence is
  the problem, the qualified and the needy populations are disjoint.
- **THE LIABILITY-EVIDENCE LAW, with its boundary.** Before building anything that records who
  worked when under whose instruction, check whether the record becomes evidence **against** your
  buyer. Brazilian boundary, established: it becomes evidence of *vínculo* only when **four
  conditions hold at once** — the operator is the **tomador** who denies employment · a **named,
  non-substitutable person** (*pessoalidade*, Súmula 331 III) · **command rather than a refusable
  offer** (a TRT-2 decision used WhatsApp records to **deny** vínculo) · **persistence proving
  habitualidade**. Remove any one and the record flips to *defensive*. **MEI/CNPJ does NOT cure it**
  — that is pejotização, live and undecided in **STF Tema 1389** with ~74.000 actions paused.
  **ETT employment (Lei 6.019/74 art. 10) and intermitente (CLT art. 443 §3º) DO cure it.**
- **THE ALERT FINDING.** Alerts sell only to whoever **profits from knowing** — never to the subject
  of the alert.
- **GATE 0.** Measured solvency as a **distribution**. An aggregate or a count is not a distribution.
  One candidate died because its buyers averaged R$2.815/month personal income.
- **RECURRENCE LAW.** An idea that keeps coming back is telling you about its **appeal**, not its
  viability. One idea has now surfaced four times in four costumes and consumed four rounds of
  analysis.

---

## 5. CLOSED CATEGORIES — do not propose anything in here

Each was closed by measurement, not opinion.

- **Information or content products** of any kind (Law 1, 7 kills).
- **Analysis, verification, reconciliation or report products** (chat window, measured 38/38).
- **Government filing tools** (Law B).
- **Authenticated action on Brazilian government systems.** gov.br's Termo de Uso bans robots **and**
  bans *"acessos realizados através de serviços de hospedagem"* — which is what any cloud agent is.
  Eight candidates died here.
- **Two-sided marketplaces** (cold start, no capital, no audience).
- **Agency or service work sold by the hour.** The permitted form is a subscription product with a
  bounded human step, never billed in hours.
- **Reselling foreign SaaS into Brazil** (commission rates and price move inversely; discovery calls
  are in English).
- **Order or shipment tracking, in any vertical.**
- **Booking, scheduling, payments or course platforms** in any segment where the customer pays at a
  counter (Law 0 fires by construction).
- **Supplier onboarding, supplier qualification, RFQ chasing, PO confirmation, delivery-date
  follow-up** — all closed by the seller-side funding law, with five named free-to-buyer incumbents.
- **Approval gates** in any segment (field-ownership law; tested across eleven segments).
- **The Brazilian public-procurement supplier population** (gateable-counterparty law).
- **PO expediting in any geography** (seller-side funding).
- **Road freight document gates.** Closed by a specific fact worth knowing: **TST 5ª Turma, September
  2024 — transport contracts are commercial, so Súmula 331 IV does not apply and the tomador has no
  subsidiary liability.** The legal engine that makes document gates valuable is judicially excluded
  from freight.
- **Construction as a buyer segment** — founder veto, permanent.
- **Labour-compliance document chasing from outsourced service providers** — founder veto, after the
  mechanism converged there three times.

---

## 6. WHAT IS ALREADY MEASURED — use these, don't re-derive them

- **13.033.275 active non-MEI Brazilian companies** (full Receita Federal CNPJ base processed,
  reference 2026-07). **133 CNAEs clear 20.000 firms. Volume is not the national constraint.**
- **Phone/WhatsApp reachability by size: MEI 0% · non-MEI 63,3% · EPP-and-larger 97,5%.**
  **E-mail is dead** — the Receita e-mail field returns the *accountant's* address.
- **IBGE keeps two registers and CEMPRE EXCLUDES MEI.** Always use CEMPRE for a firm count. Example
  of the gap: one class showed 500.092 MEIs against 50.187 real companies.
- **IBGE SIDRA API, keyless:**
  `https://apisidra.ibge.gov.br/values/t/<table>/n1/1/v/2585/p/last/c12762/all`
  - **t/9418** = companies by CNAE class · **t/7528** = companies by employee band ·
    **t/9529** = alternative size cut · **t/993** = by section only. PAIC (aggregate 10463) for
    construction, PIA for industry, PAS for services.
- **SICAF supplier counts by CNAE**, keyless:
  `https://dadosabertos.compras.gov.br/modulo-fornecedor/1_consultarFornecedor?pagina=1&tamanhoPagina=10&ativo=true&codigoCnae=<CNAE>`
  826.570 active suppliers. **WARNING: the SICAF/national ratio spans 580×. It answers "does this
  segment sell to government" and must NEVER be used to size a market.**
- **CEMPRE 2024 by block, pulled 13 Aug 2026:**

| Block | Firms | Notes |
|---|---|---|
| 47 Comércio varejista | 1.993.299 | **Excluded — counter terminal, Law 0** |
| 46.1 Representantes comerciais | 215.560 | **Excluded — mean 1,5 people, CNAE mirage** |
| 46.2–46.9 Atacado real | 301.489 | 32.099 at 10+ · 14.247 at 20+ · **5.600 at 50+** |
| 49.30-2 Transporte rodoviário de carga | 228.463 | 20.469 at 10+ · **3.627 at 50+** · legally closed, see §5 |
| C Indústrias de transformação | 619.384 | **19.691 at 50+ · 15.587 at 50–249** |
| F Construção | 313.499 | Founder veto |
| 52 Armazenagem e auxiliares | 55.386 | 52.50-8 freight agents = 9.859 |
| A Agropecuária | 106.168 | **Never searched** |

- Trade-association member counts are usually the truest pool: **ABIGRAF 15.691 printing firms**
  (79,7% micro), **ABIHPEC 3.483 cosmetics manufacturers**, **AMPRO ~160 members**, **OCB 4.400
  cooperatives**.

---

## 7. TWO FINDINGS THAT SHOULD SHAPE WHERE YOU LOOK

### The search bias
Of 59 candidates, **~45 were aimed at professional services, health, beauty, events, education,
culture, property and government paperwork. Only 5 at the real economy.**
**Strike rate: 1 of 3 Brazilian real-economy candidates cleared the gauntlet; 0 of ~40
service-sector candidates did.**

**Agropecuária (106.168 firms) has never been searched at all.** Neither has most of atacado.

### The founder-preference problem — read this carefully, it is the newest and least-understood
constraint

**The gauntlet keeps converging on one mechanism and she keeps declining it.** The mechanism is
*unattended pursuit of a document owed by a contracted third party, behind a gate the buyer
controls, with the buyer's money on the far side.* It survived in construction, then in wholesale,
then in manufacturing. **She rejected all three.** It is now closed by founder veto.

Every constraint in this record is a **negative**. There is no positive statement anywhere of what
she actually wants to build. **When you propose something, ask yourself whether a 26-year-old would
be glad to have built it in three years, or whether it is merely structurally sound.** Compliance
paperwork keeps winning the structural test and losing the human one.

**If your candidate is a compliance-document product, do not send it.** That space is exhausted and
vetoed.

---

## 8. WHAT PREVIOUS EXTERNAL LLMs RETURNED, AND WHY IT FAILED

Four external documents have been assessed. **All four candidates died**, and three died to laws in
this brief:

1. **A supplier-quote consolidation tool** — died on **LAW 7**, because the equivalence judgement it
   sold is reserved to engineers under CONFEA Res. 218/1973, and the legally safe version is a Power
   Query merge.
2. **An MCP/agent-integration service** — died on **LAW 0**, because a funded vendor ships the same
   generation on its **US$0 tier**, and because the buyer's own engineers already hold the tools.
   Also required English security calls.
3. **A beauty-sector platform** — died on **LAW 0** supplied by its own document: the distributors
   give away free training, and the biggest booking platform in that sector is owned by a payments
   company.
4. **A packaging release-gate product** — died on **POOL** (3.483 firms in the entire sector) and on
   an established software category it had not searched in the right vocabulary.

**The pattern: external proposals are strong on product logic and weak on (a) the free competitor
and (b) the boring number.** Do the boring number first.

---

## 9. WHAT A GOOD ANSWER LOOKS LIKE

For **each** candidate — one to three maximum:

1. **One sentence** describing the product as the buyer would say it, in Portuguese.
2. **The buyer**, precisely: CNAE, size band, and why *that* size band.
3. **POOL, measured**, with source and date. Total firms, and firms in the payable size band. **Then
   the arithmetic: price × customers = R$13.500 gross, and customers ÷ pool as a percentage.** If
   that number is above ~1%, do not send the candidate.
4. **PAIN**: a link or quote to a first-person Portuguese account, or an explicit "unverified".
5. **SHIPPED**: named vendors found **in Portuguese vendor vocabulary**, with prices where published,
   and an explicit judgement under corrected Law A1 — is any of them **free**, and is measured
   adoption in *this* segment above 20%?
6. **FREE**: the answer to *"who would give this away, and why?"* — reasoned by funding model, not by
   product search.
7. **CLEARING PARTY**: who earns margin on the flow? Name them or state clearly that you searched by
   class and found none.
8. **CHAT WINDOW**: which of the four survival properties does the value rest on? Quote the property.
9. **Which law is most likely to kill this**, and what single free check would settle it.
10. **The R$0 test**: the exact two closed questions, asked by WhatsApp, and the money bar.

**And one mandatory section: "WHAT I ELIMINATED AND WHY"** — everything you considered and rejected,
with the reason. Twelve previous search lenses returned zero candidates and their elimination
reasoning was the most valuable output of the run.

---

## 10. WHAT A BAD ANSWER LOOKS LIKE

- Any number without a source and a date.
- A CNAE count presented as a buyer count.
- "There is no competitor" without evidence that you searched in the vendor's own vocabulary, in
  Portuguese.
- A competitor analysis that only looks for companies **that charge** (Law C).
- Anything in §5.
- A product priced at R$150–700/month for a large population. That quadrant is fully searched.
- A product whose value is analysis, a report, a template, advice, a dashboard or an alert.
- Anything requiring her face, her name, her network, an employee, a credential, or a live English
  call.
- Enthusiasm. Six candidates were cleared enthusiastically by large agent fleets and killed later by
  a single link. **Be adversarial toward your own proposal — the last section of your answer should
  be your best attempt to destroy it.**

---

## 11. THE ONE-LINE VERSION

> **Find a Brazilian business with 600–3.400 real payable firms in it, that sells at R$1.500–4.000 a
> month to a buyer with 50+ employees, whose value depends on somebody other than the buyer being
> made to act — sold by WhatsApp, in Portuguese, by a woman with no face, no staff, no expertise and
> no money. Then spend the last third of your answer trying to kill it.**
