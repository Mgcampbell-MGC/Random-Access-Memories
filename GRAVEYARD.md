# The graveyard — candidates killed, and what each one taught

---

## GATE 0 — read this before designing anything

> **CAN THE BUYER PAY? Prove it with a measured size distribution before you design a product.**

This gate exists because it was learned the most expensive way available: a complete business
case was written, verified three times, and committed to the repository before anyone checked
the target population's bank balance.

**The candidate:** monitoring for US charities that had fallen out of good standing with state
charity regulators. 16.679 organizations verified in a "may not solicit" status. US$395 then
US$119/month. It looked strong on every axis — a measured need, a recurring calendar, a verified
list of 105.022, self-evident output, a regulator's own words supplying the authority.

**Then the buyer was measured.** 150 delinquent organizations sampled and joined to IRS revenue
data via the ProPublica API. All 150 resolved.

| Annual revenue | Count |
|---|---|
| **Under US$50k** | **105** |
| US$50k–250k | 14 |
| US$250k–500k | 6 |
| US$500k–1M | 2 |
| US$1M–5M | 5 |
| Over US$5M | 1 |
| No data | 17 |

**70% under US$50.000. Only 5,3% above US$500k.** Projected across the population: ~810 solvent
prospects, below the viability floor, requiring 7,4% cold-email conversion to reach 60
subscribers. Dead.

An organization running on US$40.000 a year does not pay US$119 a month.

---

## The structural lesson: adverse selection is built into the visible-defect mechanism

This is the most valuable finding of the whole exercise, and it generalises to every
"find-the-error-and-sell-the-fix" idea.

> **Companies carrying a public compliance defect are frequently defective BECAUSE they are
> under-resourced. Neglect and poverty are the same phenomenon seen from two angles.**

So the population *with the problem* is systematically biased toward the population that
*cannot pay to fix it*. The mechanism that makes a faceless seller credible — quoting the
buyer's own public defect — simultaneously selects for the buyers least able to pay.

Any candidate using it must be designed against this. Three escapes:

| | Escape | How it works |
|---|---|---|
| **W1** | **Sell to a different party** | Report the defect about *other* companies to the solvent party bearing the exposure — a lender, insurer, franchisor, platform, general contractor, large buyer. The defect-holder's poverty becomes irrelevant because they are not the customer. |
| **W2** | **Target defects that scale with size, not neglect** | Errors caused by *complexity* rather than inattention. A company with 400 SKUs across 12 jurisdictions has conflicts because coordination is genuinely hard. The defect-holder is large by construction. |
| **W3** | **Find a counterparty with power** | Where a solvent company must *prove* something to keep getting paid, the buyer has a contract worth keeping and the deadline is set by someone who can withhold money. |

**Evidence that W2 works:** the appliance ENERGY-STAR-versus-DOE candidate found its mismatches
concentrated in mid-size importers carrying large catalogues — with exactly *one* Whirlpool and
*one* LG record across everything tested. Scale generated the defect; poverty did not.


Kept honest so no dead idea gets quietly resurrected, and so the reasons
compound into a filter.

---

## PRUMO / LASTRO — Lei Rouanet prestação de contas desk
**Killed 4 Aug 2026, ~6 hours after the blueprint was written.**

**Cause of death: CFC Resolução 1.640/2021, Art. 3º.** The activities that made
PRUMO worth more than software are reserved by name to CRC-registered
professionals:

- **Art. 3º XVIII** — *"elaboração e controle de orçamentos de qualquer tipo…
  com o respectivo acompanhamento de sua execução em quaisquer entidades."*
  That is checking spend against an approved budget line: PRUMO's core.
- **Art. 3º IX** — *"classificação das operações, transações…"* — proposing
  which rubrica an expense belongs to.
- **DL 9.295 Art. 25(c) + Art. 26** — judging a comprovante irregular is
  *revisão de contas*, privativa dos **contadores diplomados**.
- **Art. 3º XXX** additionally claims the *parameterisation of fiscal and
  accounting rules inside management software* — reaching the product design,
  not only the service.

> **The reserved perimeter and the pricing premium are the same four features.**
> The six activities clean for a non-accountant — import the planilha, receive
> documents, extract fields, check the PRONAC, check the date, track deadlines —
> are exactly what HubCult ships at R$49,99 and Capte at R$349.

**Enforcement makes it worse for a new CNPJ.** DL 9.295 **Art. 20** makes
*advertising* the service the infraction, before a client signs. **Art. 15**'s
"sob qualquer forma" swallows the software/service distinction. **Art. 27(b)**
sets the PJ multa at 2–20× the anuidade. **Art. 32** gives appeals **no
suspensive effect**.

**The premise-breaker.** The target customer is already required to budget and
hire a CRC contador on every project, paid from the project's own budget. PRUMO
would be a second, less-credentialed layer sold on top — the same shape that
killed Aval, where the incumbent alternative was not merely cheaper but legally
correct.

**Economics collapsed independently.** Gestão Cultural Pro: **R$389/month for
unlimited projects** (verified from their Next.js bundle), against PRUMO's
R$4.347/month for 6,3 projects. Capte R$349–1.299. HubCult R$49,99–94,99.

**The service layer is crowded in the worst direction** — accounting firms
extending into culture (Faccioni CRC 03053-O/RS; Âmbar; Fernandes Cultural,
founder is a contador; R&C; Quality/BHub), not cultural people extending into
accounting.

**Honest counter-signal, recorded rather than buried:** Burô Assessoria runs this
exact model under CNAE 8211-3/00 (apoio administrativo) with no accounting CNAE —
R$5.000 capital, apartment address, two partners. Non-accountants do operate
here in practice. But "the incumbent gets away with it" is not a foundation for a
new CNPJ with no capital and no legal budget.

**Corrections made to my own work before killing it:**
- The 0,18% reprovação rate was wrong — wrong denominator. Of projects reaching
  the prestação de contas stage, 84 were reproved and 3.611 still await decision,
  with only 2 showing approved. The rate is **not computable** from this data;
  the claim was deleted rather than restated.
- Fator R breaks between 13 and 14 clients at a fixed R$19.500 pró-labore.
- Flat per-band pricing ranged from 10,4% of a project at the Simplificado floor
  to 0,35% at the Especial ceiling — the 2–5% norm only held mid-band.
- 150 comprovantes × 30s = 75 min, contradicting the 30–45 min target in the
  same document.

---

## LÍQUIDO — creator/talent payout closing for influence agencies
**Killed 1 Aug 2026.** Pora ships the identical product today — bulk contracts,
automated nota fiscal collection, Pix batch payout, plus the antecipação the
blueprint had refused to build — serving *"marcas e agências"* with agency
white-label, claiming **+2000 influenciadores já foram pagos**.

The kill indicator was written into the blueprint ("monitor Pora's customer
count") and had **already fired before the document shipped**. Failure of
sequencing, not of analysis.

---

## AVAL — consent registry for beauty/dental networks
**Killed 31 Jul 2026.** CFO Res. 196/2019 bars dental networks from before/after
publication entirely; CFM Res. 2.336/2023 Art. 14 II(e) mandates anonymity even
with consent; TJDFT Acórdão 2108487 held missing documentation alone is not a
liability trigger; and ANPD's entire private-sector fine record was **R$14.400**.
Also required a per-transaction human step at ~1.440 reception desks.

---

## JANELA — image-rights window registry
**Killed 31 Jul 2026.** Brazil pays talent lump-sum with nothing recurring, so
the product was a calendar. Awards R$7k–39k, rare, insurable, contractually
shiftable. XR and FADEL already ship it; SATED is an incumbent registry.

---

## VOLTA / REAVER — Mercado Livre marketplace credit recovery
**Killed, then rebuilt as REAVER, then shelved.** Two facts killed it: the
recoverable pool was an unproven residue the platform was auto-repairing, and
there was no action path (no API — begging via UI). REAVER's own text concedes
the second: *"the documented claims API… does not establish a general channel for
recovering seller charges."* Its workaround outsources every submission to the
seller. Its economics also require three analysts, R$130–145k/month revenue, and
24–30 months — a different company than the one being built.

REAVER's **governance method was harvested** and is the most valuable thing to
survive: gates before spend, GREEN/AMBER/RED perimeter, numeric kill criteria,
phased build triggers, and "code calculates, AI never calculates money."

---

## The filters these deaths produced

1. **Competitor check runs FIRST.** Not last, not lightly. LÍQUIDO died to a
   competitor named in its own kill-indicator list.
2. **Regulated professions are a structural wall.** If the value sits inside a
   Brazilian reserved profession (CRC, OAB, CREA, CRM), it is closed unless
   partnered with a credential — which breaks the one-to-two-person model.
   *Check the reserved perimeter before designing the product, not after.*
3. **Do not sell protection against losses Brazil does not impose.** Janela,
   Aval, and the fear-framing of PRUMO all died here.
4. **Beware the free competitor that is legally correct.** An indemnity clause in
   dentistry; a CRC contador the client already pays. If the incumbent
   alternative is mandatory, you are the second layer.
5. **Mature markets are colonised vertical by vertical.** Brazilian repasse-gate
   and reconciliation SaaS both proved farmed out. The remaining openings are
   where the incumbent is a human consultancy — but check whether that
   consultancy needs a credential the founder lacks.
6. **Price ceilings are set by the cheapest adequate substitute**, not by the
   value delivered. R$389/month unlimited beat a R$4.347/month service.
   **But see the correction below — this filter was being applied wrongly, and
   the wrong application is more dangerous than the filter is useful.**

---

## Correction, 6 Aug 2026 — the filter above was killing good ideas

**Nineteen candidates killed, nothing launched.** That base rate is evidence
about this filter set, not only about the ideas. The diagnosis is specific.

**Filter 6 was applied to partial substitutes as though they were complete ones.**
LINELOCK was killed because Adobe Acrobat's Compare Files exists at US$19,99/month.
But Acrobat cannot verify a barcode and cannot check a change against an
authorisation sheet. It was never an *adequate* substitute — only a partial one.

Applied consistently, that reasoning kills Notion (a text file is free), kills
Superhuman (Gmail is free), and kills every vertical tool ever sold against a
spreadsheet. **Charging a premium over a partial substitute is the normal case in
software, not the anomaly.** A filter that cannot pass a good idea is not rigorous.

### The rule that replaces it

Every objection sorts into exactly one bucket, and must be **labelled**.

**Bucket A — structural. These kill.** A verified fact making the plan
*impossible*, not merely uncertain. Only five kinds qualify:

| | Test | Verified precedent from this graveyard |
|---|---|---|
| A1 | Someone ships the **identical** product to the **identical** buyer | Pora, "+2000 influenciadores já foram pagos"; Stella Luna & Co shipping the identical swimwear package |
| A2 | A **named** law reserves it to a credential the founder lacks | CFC Res. 1.640/2021 Art. 3º XVIII |
| A3 | **The list does not exist** — the buyer cannot be enumerated | — |
| A4 | **The physics fail** — chiefly, required send volume exceeds what one new domain can send | — |
| A5 | A cheaper substitute does **the whole job**, or a regulator gives it away free | Gestão Cultural Pro, R$389/mo unlimited; free government platforms covering ~60% |

**Bucket B — unproven. These may NOT kill anything.** Whether buyers pay this
price; whether the gap over a *partial* substitute is worth paying for; the
conversion rate; whether the buyer knows they have the problem; whether they act
now; whether they trust an unknown vendor.

> **Every Bucket B objection must arrive with the cheapest test that settles it —
> under two weeks, under US$200, with a numeric pass threshold. A Bucket B
> objection without a test attached is not a finding. It is a guess wearing the
> costume of rigour.**

### Why this matters more than it looks

A false kill costs more than a missed risk. A missed risk shows up in a cheap
test and gets corrected. **A false kill never shows up at all** — the business
simply never exists, and nothing ever contradicts the decision.

"Not proven" is the normal condition of every new business before it is tested.
It is not evidence of weakness.

### And a calibration fact that was being ignored

This founder's marginal cost of **building and testing** is unusually low —
she genuinely ships working software by directing Claude Code. For someone who
can produce a working artefact in days, the optimal strategy is not *analyse
until certain*; it is *find the cheapest real test and run it*.

**Therefore: prefer a candidate that can be TESTED cheaply over one that merely
SURVIVES analysis.** And always commit to one angle. Ten reasons to be cautious
is the wrong deliverable.

### Which of the deaths above still stand

Most do. LÍQUIDO (A1), RIO BLOCKS (A1), PRUMO (A2), AVAL (A2), JANELA (A1) and
the marketplace/freight/repasse candidates (A1) all died on Bucket A facts and
remain dead.

**LINELOCK's cause of death is amended:** it stays dead, but on the *trigger*,
not the substitute. The moment an agency sends artwork to print is invisible from
outside — no public feed, no filing, no announcement — which is an A3/A4 problem.
The US$19,99 substitute argument is withdrawn.

**WRAPCHECK's is amended the same way:** the free-spreadsheet argument was a
Bucket B judgement. It stays dead because its trigger is invisible *and* rare
*and* only useful for the few hours a shoot is still live.

---

## Second correction, 6 Aug 2026 — R4 was aimed at the wrong question

The old rule asked *"does the founder hold the credential?"* That is not what
predicts failure. The question that does:

> **After the buyer opens the file, can they tell whether it is right?**

| Buyer can self-verify the output | R4 status |
|---|---|
| **Yes** — the artefact carries its own authority | **Does not bind.** The founder's standing is irrelevant because nothing rests on it. Nobody asks who wrote their tax software. |
| **No** — the buyer must trust the author | **Binds hard.** Borrowed authority is the product, and it cannot be borrowed. |

DeckProof is the clean case: it recomputes arithmetic against the buyer's *own*
documents, so every line is checkable on the spot. LICENCEPROOF is the opposite —
"is my sponsor licence compliant?" cannot be self-checked, which is why it carries
the worst credential exposure in the set despite a better trigger stream.

### The credential is a one-time purchased input, not a dependency

For a **service**, the credentialed person is required on *every engagement* — that
is what breaks a one-or-two-person shop. For a **download**, they are required
*once*, during authoring.

One US$300 session with an ex-buyer to validate a checklist is a **line item**, not
a partner, not a royalty, not a standing obligation. What R4 should screen for is
therefore: *does this need the credentialed human on every transaction?* A
downloadable product, by construction, does not.

### The consequence for how candidates get screened

After the product is built, the founder's job is **marketing, not delivery.** That
is the structural advantage of a download over a service, and it should be weighted
as one.

Her build cost is one-time and close to zero — she directs Claude Code. The
*recurring* work is reading lists and writing emails. So the binding constraint was
never "can this be built simply":

> **Screen on whether it can be MARKETED simply, not on whether it can be BUILT
> simply. A harder-to-build product with a visible trigger beats an easy-to-build
> one without.**

Corollary: the bundled corpus should be *thicker*, not thinner. It is one-time
work, it is the moat, and it is the part a prompt cannot hold.

### Which deaths this revisits

**None are resurrected.** RIO BLOCKS, CREDIT LAB, AVAL and PRUMO each died on an
A1 or A2 fact — an identical product already shipping, or a named law reserving the
work. The credential was never the load-bearing objection for any of them.

---

# KILL — HTS Ruling Currency Index (10 August 2026)

Killed by its own audit, one day after it was found. The defect was real and I measured it
correctly. It is unserved because **it does not cost anyone money.**

## What it was

A US$297 downloadable index: every apparel and footwear CBP ruling joined to the current HTS, each
cited tariff code marked LIVE / SUBDIVIDED / GONE. Built on a measured finding — 28,9% of the
8-digit lines those rulings cite no longer exist, across 377 distinct dead lines, and no product at
any price flags this.

## Why it died — four structural hits, all verified

**1. The government already prescribes the check, free.** USITC's own FAQ, verbatim:
*"Once you find a potential HTS classification in CROSS, return to HTS and enter that classification
number in the search bar."* The thing the product sells is the published standard procedure, it is
free, and it takes seconds.

**2. The filing system already blocks the failure.** A dead tariff number cannot reach an entry —
ACE/ABI validates against the current Harmonized reference file and rejects it. So the cost of the
error the product prevents is a few minutes of rework, not a penalty. **A defect with no unpriced
consequence is not a product.**

**3. The headline number was inflated, by my own measurement choice.** USITC:
*"Statistical Reporting Numbers are not legal... the stat suffixes... are administratively adopted
rather than being enacted."* Legal classification ends at 8 digits; the 10-digit suffix churns
administratively. My 43,2% figure largely measured that churn. The legally meaningful figure is
28,9% — and it is concentrated in old rulings: **4,1% for rulings from 2015 onward**, which is what
anyone with a recency preference actually reads.

**4. A static file cannot hold the claim.** USITC published ~31 revisions of the 2025 HTS and was at
Revision 12 of 2026 by mid-year, driven by Chapter 99 trade actions. A staleness-checker that is
itself stale emits false verdicts on the exact dimension it charges for. USITC Investigation
1205-14, implementing the next WCO HS amendment cycle, reports to the President in September 2026 —
a scheduled mass renumbering of the apparel chapters, on the calendar, against a one-time price with
no economics to maintain it.

**5. The arithmetic never worked anyway.** 13.952 brokers + 6.708 importers = 20.660 maximum buyers.
At 1–2% conversion on a one-time purchase that is US$61k–123k of lifetime revenue, decaying. The
target is US$89–100k **per year**. I did not run this until the red team did.

## The sharpest point, which I missed entirely

**The product detects the errors that detect themselves.** A code that has *died* announces itself —
free lookup, ACE rejection. The expensive error is a code that **still exists but whose scope changed
underneath it**: ACE accepts it, the entry is wrong, nothing warns anyone. That is the staleness
worth paying for, and an existence check is structurally blind to it.

## THE LESSON — add this to Gate 0 and the two-bucket rule

> **"Nobody sells this" has two explanations, and I only seriously entertained one.**

Absence of a competitor is evidence of an *opportunity* or evidence of *no value*, and the second is
more common. Before building on an unserved defect, ask what happens today when it goes uncaught. If
the answer is "a free system catches it" or "nothing, because it self-corrects", the space is empty
for a reason.

**The new test, to run before any build:** name the specific person who loses a specific amount of
money when this defect goes undetected, and the mechanism by which they lose it. If the loss is
"minutes of rework", stop.

This sits alongside Gate 0 (prove the buyer can pay) and adverse selection (the defect may select for
buyers who cannot). Gate 0 asked *can they pay*. This asks *is there anything to pay for.*

## What survives

- **The corpus model is untouched.** What failed is this instance of it, not the model.
- **The legal perimeter research stands** — HQ H272798, HQ H350722, 19 CFR 111.2(a)(2)(i) — and is
  reusable for any future US customs product. One correction: H350722 should not be cited as a green
  light. Read fairly, its holding on automated tools is a *restriction* — a tool is not a licensed
  person — and the trade press headlined it *"Even AI Needs A License."*
- **The measurement assets are real**: a 47.627-ruling index, a 942-line currency map, and 1.586
  current tariff lines with no precedent at all, in 2,1 MB. Their honest ceiling is a free lead
  magnet, not a product.
- **Scope drift remains a genuine, unsolved, expensive problem** — and it needs a customs expert's
  judgement, which is the same wall LineProof hit.

---

# KILL — ET Respondent's Corpus, UK, US$397 (10 August 2026)

Audited on the same day it was reviewed. Five structural hits. The corpus is real and excellent;
the business around it is not.

## The verified kill: price inversion against a regulated professional

| Substitute | Price | What the buyer gets |
|---|---|---|
| **FSB membership** | **£97,50/year** (sole trader) to £1.295 (101+ employees) | Legal expenses insurance underwritten by Markel, SRA-regulated solicitors (Markel Law LLP): *"Legal representation throughout the employment tribunal process, including ACAS Early Conciliation, responding to claims, pre-hearing reviews, tribunal hearings"*, plus *"Tribunal-ordered compensation, agreed settlements"* — **up to £100.000 per claim** |
| **Solicitor drafting the ET3** | **£261–£522 + VAT** (~£313–£626) | A regulated, insured professional does the actual work |
| **gov.uk respond service + Acas helpline** | **£0** | Official guided ET3 submission and free employer advice |
| **This product** | US$397 (~£300) | A file |

**£97,50 a year buys a solicitor and the award paid. The product costs three times that, once, and
delivers markdown.** At the other end, the bottom of a solicitor's ET3 range is roughly the product's
price for the real thing. There is no band in which the file is the rational purchase.

## The legal error I should have caught myself

**First-instance Employment Tribunal decisions are not binding precedent.** Only the EAT, Court of
Appeal and Supreme Court bind. So a corpus of 133.296 first-instance decisions is not authority —
"find comparable decided cases" sounds like law and isn't. CBP rulings genuinely are citable, which
is why the tariff corpus never had this problem. I carried the analogy across jurisdictions without
checking that the thing being carried still held.

## The other three

**The buyer cannot be found.** The ET1 is confidential at filing; there is no public register of
lodged claims; hearing lists appear days before a hearing that now sits ~12 months out; the decisions
database publishes only after judgment. The buying window is the **28-day ET3 deadline**, during
which the respondent is publicly invisible. Outbound is impossible — not hard, impossible. Everything
must come from inbound search, competing with Acas, gov.uk, Peninsula and every employment firm's SEO
budget.

**The buyer buys once.** ~50.000 single claims in 2025/26 against ~1,37M UK employers with staff —
roughly 3% annual incidence, skewed toward larger employers. A small employer meets this once a
decade. No repeat purchase, no referral network (nobody advertises being sued). This violates the
project's own rule: **sell to the professional who repeats the task.**

**The statute is being rewritten underneath it.** Employment Rights Act 2025: tribunal time limits
3→6 months from ~October 2026; unfair dismissal qualifying period 2 years→6 months for dismissals
from 1 January 2027; statutory compensation caps removed. Every decision in the corpus was decided
under a regime being dismantled while the product is on sale — and the seller has no legal training
with which to maintain it.

**And it can injure its buyer.** An ET3 is a pleading; admissions in it are near-impossible to walk
back. The core loop — lay user, AI, cite comparable cases — is the workflow that produces fabricated
citations, which the High Court addressed in *Ayinde* (June 2025). A non-lawyer seller with no
professional indemnity insurance carries that.

## THE PATTERN ACROSS THREE KILLS — this is the useful part

| Candidate | Cause of death |
|---|---|
| 50-State Solicitation Monitor | The buyer could not pay (70% under US$50k revenue) |
| HTS Ruling Currency Index | The defect had no consequence — free systems already caught it |
| ET Respondent's Corpus | A regulated professional already does it cheaper, and the buyer cannot be reached |

Three different failures, one shared cause: **every one was chosen by finding a measurable defect
first and looking for the buyer afterwards.** The defect was real in all three cases. The route to a
payer was never checked until late, and it is what killed each of them.

**THE REFRAME — choose the next candidate channel-first.** Before measuring any defect, answer in
this order:

1. **Who repeats this task for money?** Not who suffers it once.
2. **Can I reach them, repeatedly, without a list I cannot legally obtain?** Is there a public,
   timely signal of need — or is the trigger invisible?
3. **What does the professional substitute cost?** If a regulated human does it for the same money,
   stop.
4. *Only then* measure the defect.

Gate 0 asked *can they pay*. The dead-code lesson asked *is there anything to pay for*. This one asks
**can they be found, and am I cheaper than the human**.

## What this says about the next candidate

**Recurso em 3 Dias (Brazil, US$197) inverts every one of these failures**, and that is worth
noticing rather than treating it as merely the next name on a list. Public procurement is public by
design: the bidders, the editais and the session records are published, so the buyer is identifiable
and the trigger is visible. A company that bids on public contracts bids continuously, so the task
repeats. And Lei 14.133/2021 art. 165 fixes the window at **3 dias úteis** with intent declared in
session *sob pena de preclusão* — a deadline that recurs for the same buyer, rather than once a
decade.

It has not been audited against the four questions above. It should be, before anything is built.
