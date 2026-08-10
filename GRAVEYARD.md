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

## Corrections to the entry above, from the fuller substitutes audit

**My FSB figure was wrong and the source was weaker than I implied.** I wrote "£97,50/year for a sole
trader". £97,50 is the **associate** rate. The pricing found is sole trader/no employees **£195/yr**,
1–20 employees £345, 21–50 £545, 51–100 £895, 101+ £1.295. Worse, `fsbmembership.co.uk` is a
**reseller site** that itself discloses it "is not the official Federation of Small Businesses
corporate website" — and the official domain could not be fetched. Treat the FSB numbers as
corroborated but not primary.

**The insurance argument is weaker than I stated, not stronger.** How many UK SMEs actually hold
legal expenses cover **could not be verified in either direction**. The ABI's January 2026
underinsurance report sits behind a bot check; secondary summaries confirm employers' liability
(50%) and public liability (57%) but do not isolate legal expenses at all. The "~30%" figure in
circulation is unverified. So "someone else already pays" is true *where cover exists* and its
prevalence is unknown.

**Where cover does exist it is strong but conditional** — from Markel's own policy wording, read
directly: it names *"Employment tribunal response (ET3)"* as a covered stage, pays compensation up
to £100.000, **but** applies a 51% prospects-of-success merits test the insurer alone judges, lets
the insurer choose the representative, and **collapses the indemnity to £1.000 if the employer picks
their own solicitor**. Cover can also be reduced where the employer failed to follow the advice line
or the ACAS Code before dismissing.

**The solicitor comparison needs to be stated at the right level.** £261–£522 + VAT is the fee to
**draft the ET3**, which is roughly what this product costs. Defending the whole claim is
£6.000–£8.000 straightforward and £18.000–£28.000 end to end, with no costs-shifting — the employer
pays even when they win. So the price inversion holds at the level of the specific task the product
addresses, not for the entire defence.

**One honest point in the product's favour, recorded because it is real:** no dedicated ET3 defence
toolkit for employers was found at any price. The format appears genuinely novel here, and a narrow
segment does exist — uninsured, no HR retainer, claim small enough that self-representation is
rational. SETA 2018 puts employer representation at 70% day-to-day and 77% at final hearing, so
roughly 30% are unrepresented.

**Why the kill still stands.** The load-bearing reasons are not the insurance argument. They are:
the buyer **cannot be found** inside the 28-day window by any lawful mechanism; the corpus **is not
precedent**; the **Employment Rights Act 2025** rewrites the substrate through 2027; and the buyer
**purchases once a decade**. A narrow reachable-by-nobody segment is not a business, and reaching it
means winning panicked UK search traffic against Acas, gov.uk, Peninsula and every employment firm's
SEO budget — from Brazil, with no phone support.

## Two reusable findings from the ET audit — keep these

**1. The UK legal perimeter is clean, and now documented verbatim.**

**Employment Tribunals Act 1996 s.6(1)**: *"A person may appear before an employment tribunal in
person or be represented by— (a) counsel or a solicitor, (b) a representative of a trade union or an
employers' association, or (c) **any other person whom he desires to represent him**."*

**Legal Services Act 2007 s.12(1)** lists six reserved activities — right of audience, conduct of
litigation, reserved instruments, probate, notarial acts, administration of oaths. **ET
representation is none of them**, and employment tribunals sit outside the LSA's "court" definition.
The Employment Tribunal Procedure Rules 2024 (SI 2024/1155, in force 6 January 2025) replaced the
2013 rules and expressly recognise a *"lay representative"* — *"a person who charges for
representation in proceedings but is not a legal representative."*

FCA claims-management regulation covers employment but is built around advising a **claimant**;
art 89W excludes activity *"consist[ing] of the provision of a service to the defendant."* A
respondent-side product sits outside it.

So: no regulatory barrier ever existed here. The product died commercially, not legally.

**2. UK case-law licensing is split, and the split matters enormously.**

| Source | Licence | Bulk / computational use |
|---|---|---|
| **First-instance ET decisions** (gov.uk) | Generic **OGL v3.0** footer — permits commercial exploitation, attribution required | Permitted, but there is **no bulk download and no API**. The Atom feed returns only the 50 most recent; the corpus is 2.666 pages of search UI. The judgment PDFs carry **no copyright notice at all** |
| **EAT and appellate** (Find Case Law, National Archives) | **Open Justice Licence v2.0** | **Expressly bars "computational analysis of the Information (including indexing by search engines)"** without a separate application. The licence is free and ~40 have been granted since 2022 |

**This is a rule for any future UK legal-corpus product: the binding authority is under the licence
that forbids bulk processing, and the freely-processable material is the part that binds nobody.**
That inversion is not an accident — and it is exactly the trap this candidate walked into.

Also recorded: the OGL reading for first-instance ET decisions is **inferred, not stated**. No
primary source says so in terms; it rests on the generic footer, the absence of any ET carve-out in
OGL v3.0, and practitioner commentary. Anyone building on it should treat that as an open risk.

**3. The staleness dates, now precise.** Employment Rights Act 2025 received Royal Assent
18 December 2025. Commencement relevant to this corpus:

| Date | Change |
|---|---|
| **1 October 2026** — under two months away | ET claim time limit rises **3 → 6 months** |
| **1 January 2027** | Unfair dismissal qualifying period **2 years → 6 months**; **compensation caps removed**; fire-and-rehire restrictions |
| Through 2027 | Guaranteed hours, flexible working, bereavement leave, umbrella companies, collective redundancy thresholds |

Fact-pattern reasoning in old decisions stays illustrative. Any statement of time limits, qualifying
periods or remedies caps drawn from them **misstates the law within weeks.**

---

# THE FIELD IS DEAD — nine candidates, one mechanism (10 August 2026)

Three more killed today, after the workflow join bug was fixed and the real top of the field was
finally evaluated.

| Candidate | Killed by |
|---|---|
| NYC Building Compliance Radar | **Insparisk Command's free-forever plan** — unlimited buildings, deadline and violation alerts included. ViolationWatch at $99/yr + $59,99/yr Local Law Tracker. And the city itself prints the obligation on the **November property tax bill**, pre-deadline, per building — the "no free proactive notice" premise was simply false |
| Sistema de Ciclo (concursos) | Free lead magnets from **Estratégia** and **QConcursos** at the exact edital moment; **Gran Gerenciador de Estudos** auto-generates the ciclo inside the R$34,90 subscription buyers already hold; **Planilha do Aprovado** at R$29,90 with 38.000 users |
| ISO 9001 Countdown Pack | The contents are **mandatory retained records under clauses 9.2.2, 9.3.3 and 10.2.2** — possession is a precondition of being certified. Advisera's internal-audit kit is **$229 one-time** with a human expert; the full kit is $897 including the free 2026 upgrade. And **IAF CertSearch's FAQ states no user at any price tier can extract a list of certified companies** — the funnel cannot be filled |

## The mechanism, five times over

Levelset. GleanMark. Estratégia/QConcursos. iNymbus/SPS. Insparisk/ViolationWatch/NYC.

**A funded party gives away an equivalent free version, as lead generation, on the exact keywords.**

The reason is structural and specific to 2026: content and templates now cost almost nothing to
produce, so **the free tier is the marketing budget of every funded incumbent.** A solo operator
selling an artifact is not competing with a product — it is competing with someone's marketing
department, which is *designed* to give that artifact away.

Portuguese did not protect against this. Estratégia runs the identical play in Brazil.

## THE HARDER LESSON — about the search, not the market

Fifty candidates were generated across six lenses I designed to be structurally different. They were
not. Every one was **a tool, template or monitor helping a professional complete a recurring task.**
The industries varied — customs, employment, construction, trademarks, medical credentialing,
property, quality management, Brazilian exams — and the *shape* never did.

That shape is the single most commoditised category in digital products, because it is exactly what
content marketing produces for free.

**I searched one room nine times and called it a broad search.**

## The constraint trap, stated honestly

Faceless, no audience, no network, no calls, no capital, self-serve, US$8.000/month. That set leaves
only two discovery mechanisms — **search and marketplaces** — and both are precisely where funded
incumbents spend their marketing budget. The constraints force the hunt into the most contested
channel that exists.

So the answer is not another candidate in the same room. It is one of:

1. **A distribution surface incumbents have not yet colonised.** The unlock sweep found one and it was
   never tested: MCP registries and agent tool-surfaces, roughly twelve months old, where discovery
   happens through a registry rather than Google, and where no incumbent is yet running content
   marketing. Authoritative niche data delivered *into other people's AI tools*.
2. **A category where no funded party has any reason to give anything away** — because there is no
   upsell to fund it. That usually means unglamorous, fragmented, offline-heavy markets that venture
   capital ignores. US$8.000/month is small enough that "too small to matter" is a real moat.
3. **Relaxing a constraint.** The binding one is not the money — it is having no distribution. That
   is a permanent constraint by choice, and it is the reason every path leads back to contested search.

## What must not happen next

Another hunt of the same shape. The screen is working — every kill named a competitor and a published
price — but a working screen applied to the same room repeatedly produces nine corpses and no
business.

---

## RECURSO EM 3 DIAS — Brazilian licitação impugnação/recurso (killed 10 Aug 2026)

The last shortlisted candidate, audited after the distribution constraint was relaxed to allow
Portuguese phone selling. **Relaxing distribution did not save it.** Three independent kills.

**1. The incumbent already ships the AI product.** ConLicitação sells **Dr. Licita** — *"a primeira
inteligência artificial do mercado de licitações"* — drafting petições administrativas *"em menos de
um minuto"*, **uso ilimitado**, on a proprietary base of editais, acórdãos, legislação and *"teses
reais validadas por advogados"*, inside the subscription serious licitantes already hold. The
candidate's only asset — the public TCU jurisprudência CSV — is already productised by the incumbent,
with lawyer validation the founder cannot offer.

**2. A human sells the finished document for R$190.** AM Consulte's published price list:
*"Elaboração de Recurso e/ou Contrarrazões — R$190,00 por peça"*; impugnação R$140–180. Above that,
free templates from ConLicitação itself, LicitaGov, BLL, Jusbrasil, AGU and law firms; below it,
Sebrae trains the small licitante free. Every layer occupied, for the sixth consecutive time.

**3. The statutory clock makes the sale impossible — this is the novel finding.**
**Lei 14.133/2021 art. 165 §1º**: the *intenção de recorrer* must be manifested **immediately, in
session, sob pena de preclusão**. Only the razões get 3 dias úteis. So at the only moment a bidder is
publicly identifiable — the ata, generated at session close — they have **already** either declared
intent (and are committed, usually already assisted) or are legally dead. **There is no moment at
which a cold call can create a sellable situation.** For the impugnação side it is worse: it must be
filed before the session, when participants are not yet public at all.

**4. And the differentiator is reserved.** Lei 8.906/94 **art. 1º, II** makes *"consultoria, assessoria
e direção jurídicas"* privativa de advocacia. Identifying the defect and advising which tese to argue
— the phone judgement that was to distinguish this from a free template — is the reserved part.
OAB-SP actively litigates ACPs against unlicensed practice, and São Paulo is where she lives. Same
shape as the CFC kill that ended PRUMO: **the reserved perimeter and the pricing premium are the same
feature.**

**What this proves about the diagnosis.** The distribution relaxation was correctly identified but
insufficient. Phone selling in Portuguese does not help when the statute closes the window before the
call can land, and when the incumbent's AI already ships inside a subscription the buyer holds.

---

# TEN CANDIDATES. THE SHAPE IS FARMED.

US customs · UK employment · US construction · US trademarks · US e-commerce · US property ·
US quality management · Brazilian exam prep · Brazilian public procurement.

**Nine industries. Three countries. Two languages. Both distribution models. One mechanism.**

> **"An informational or tooling product that helps a professional complete a recurring task" is
> comprehensively occupied** — because AI made content free to produce, so every funded company now
> uses free content as its acquisition channel, and in a compliance domain **a free template is
> genuinely as good as a paid one.**

## The untested hypothesis, and why its physics differ

Every one of the fifty candidates asked a woman whose career was **luxury and premium brand events**
to become a compliance analyst in a field she has never worked in, against incumbents who know it
better.

**In compliance, free is equivalent. In taste, free is visibly worse.** A free proposal template
advertises its own inferiority; a free clause library does not. That is a structural difference in
competitive physics, not a preference — it is the reason aesthetic categories resist the
lead-magnet mechanism that killed all ten candidates, and it is the only domain identified in this
entire session where the founder's actual expertise is the moat rather than the gap.

**Untested. Recorded as the next hypothesis, not as a finding.**

### Correction to the Recurso entry — the legal perimeter is better than stated, and that makes it worse

The full perimeter audit found the **product** side more defensible than the red team assumed. Recorded
so the reasoning is accurate rather than convenient:

- **Lei 8.906/94 art. 1º, I** reserves *"a postulação a qualquer órgão do Poder Judiciário e aos
  juizados especiais"* — **judicial bodies only.** Administrative licitação authorities were never in
  scope.
- **Lei 9.784/99 art. 3º, IV**: *"fazer-se assistir, **facultativamente**, por advogado."*
- **Súmula Vinculante 5**: *"A falta de defesa técnica por advogado no processo administrativo
  disciplinar não ofende a Constituição."*
- **Lei 14.133/2021 art. 164**: *"Qualquer pessoa é parte legítima para impugnar edital"* — universal
  standing, no lawyer required anywhere in arts. 164–165.
- **The "Resolve Juizado" ruling (27ª Vara Federal RJ, 17 Nov 2025)** held an AI petition-generating
  platform does **not** exercise reserved advocacy, because it *"organiza e formata informações
  inseridas pelo usuário"* without *"análise jurídica individualizada."* Conditions imposed: prominent
  disclaimers, no promise of legal outcomes. **But OAB-RJ has escalated to the STJ — live, contested,
  not settled law.**
- No OAB enforcement action was found anywhere targeting licitação recurso drafting specifically.

**THE VISE — and this generalises beyond Brazil.**

The legally safe version is a **pure self-service formatter with no individualized judgement**. That is
exactly the version **Dr. Licita already ships better**, that free templates from ConLicitação, BLL,
LicitaGov, AGU and Jusbrasil already cover, and that Sebrae already teaches free.

The differentiated version — reading *this* edital, finding *this* defect, advising *which* tese —
is **art. 1º, II** territory: *"consultoria, assessoria e direção jurídicas"*, against which OAB-SP
has filed **34 ações civis públicas with 23 favourable liminares since 2022**.

> **The legally safe version has no differentiation. The differentiated version is legally exposed.**
> The reserved perimeter and the pricing premium are the same feature — the third time this exact vise
> has appeared (PRUMO/CFC, ET corpus, now Recurso).

**What did NOT kill it, recorded for accuracy.** The buyer was fine: **700.000 SICAF suppliers**,
**over 1 million public purchases worth ~R$1 trilhão in 2025**, ME/EPP alone at **481.700 purchases
worth R$272,6 bilhões** — a derived average around **R$566.000 per ME/EPP contract**. Reachability was
fine too: atas name every participant with CNPJ, and **PNCP exposes CNPJ-level data through a
no-login public API**. Gate 0 passed and the list existed. It died on the incumbent's shipped AI, the
R$190 human, and a statutory clock that closes before a call can land.

---

## DOSSIÊ PATROCÍNIO — sponsorship architecture kit (killed 10 Aug 2026)

The taste hypothesis, tested. **Candidate eleven, and the first that used the founder's actual
expertise.** Fatal on four axes, and it disproves the thesis that produced it.

**1. Adverse selection, now with numbers.** IBGE: Brazilian cultural-sector workers average
**R$2.815/month**, women **R$2.510**, informality **44,6%**, 43% conta-própria. R$497 is ~18–20% of
the target buyer's monthly income; R$997 is ~35–40%. And the trigger selects for structural losers,
not unlucky ones: **77,4% of Rouanet money 2021–24 went to the Sudeste, SP alone 40,5%**, with
researchers attributing the gap to *"desigualdades no acesso a redes de financiamento"* — unequal
access to funding **networks**, not to deck quality. A PDF does not fix network access.

**2. The law already built the buyer a better option.** Rouanet norms permit a professional
captador's fee of up to **10% of project value (cap ~R$100–150k) as a line item inside the approved
project budget**, paid only from funds actually captured. Zero upfront, success-contingent, and the
captador brings the network the data says determines the outcome. A broke producer's rational choice
is never a cash-upfront PDF.

**3. Everything informational is already free.** Sympla Academy's free certificated course covers
proposal structure, tier pricing, contract clauses, negotiation and post-event reporting. Plus
4.events, Even3, Lets, Sebrae, MinC's free 160-hour course, and Incentiv.me. Premium is occupied too
— Cultura e Mercado charges **R$3.599** for 63 hours with 14 named specialists. The R$497–997 slot is
squeezed from both ends.

**4. The one scarce ingredient cannot be built.** Sponsorship values are confidential and per-deal.
What is public is already googleable — individual events publish their own cota decks. What is not
public is what brands actually paid. And the sharpest point: **her career was executing brand events,
not closing sponsorship contracts.** She does not hold the dataset.

## THE TASTE THESIS IS DEAD, AND HERE IS EXACTLY WHY

I argued: *in compliance a free template is equivalent; in taste, free is visibly worse — so
aesthetic products resist the lead-magnet mechanism.*

**The inversion:** the premium end already retains agencies with in-house design and existing brand
relationships. **The buyer who needs someone else's taste is the buyer who lacks it — the one earning
R$2.500/month.** The thesis may hold in the founder's old world; the addressable buyer for
taste-as-a-product is precisely the one who cannot pay for it. The thesis contradicts itself.

**Founder-fit crack, recorded:** Rouanet captação is a fiscal-incentive game — renúncia fiscal
mechanics, prestação de contas, compliance. Not the luxury-brand-experience game she knows. The one
candidate built on her expertise pointed it at buyers playing a different sport.

**Correction to my own input:** the "35.000 approved-but-unfunded projects" figure was my computation
from this repo's SALIC pull (45.863 total, 10.945 with captação > 0), not a published national
statistic. The phenomenon is real and worse — nationally in 2023, **R$16,7bn requested against ~R$2bn
captured**, and in the ABC paulista region **1 project in 10** raised anything.

---

# ELEVEN CANDIDATES. THE CONSTRAINT SET IS THE PROBLEM.

The mechanism never changed across nine industries, three countries, two languages, both
distribution models, and now both product categories — compliance *and* taste.

**The chain that closes the trap:**

1. No audience and no network ⇒ discovery must come from **search or marketplaces**.
2. Search and marketplaces are **where funded incumbents place free content**, because content now
   costs nothing to produce and is the cheapest acquisition channel in existence.
3. An informational or template product is **exactly what they give away**.
4. Therefore the intersection of "digital information product" and "discovered without an audience"
   is approximately empty.

**The most expensive constraint is not capital — it is the excluded network.** Every strand of
evidence converges on it: the base-rate data showed nearly every large solo success rode an existing
audience; the GIFE research says captação outcomes are set by network access; five kills came from
incumbents who reach buyers we cannot.

Breaking the trap requires changing exactly one of three things — **the audience/network exclusion,
the product category (something that is not information), or the revenue target and timeline.**
Nothing else in the set is load-bearing.

---

# THE ALERT FINDING — who you sell a trigger to decides whether it sells at all

Researched 10 Aug 2026, before designing candidate twelve. **This is the most useful structural
finding in the file.**

## The evidence splits on one variable: who benefits from the trigger

**When the recipient is an OPPORTUNIST who profits by acting on the information, the alert sells by
itself, at real prices, sustained:**

| Business | Watches | Price |
|---|---|---|
| PropertyRadar | foreclosure / ownership change | **US$119–599/month** |
| RealtyTrac | foreclosure listings | **from US$49,95/month** |
| Owler | funding, hiring, competitor events | **US$39–350/month** |

**When the recipient is the SUBJECT of the problem — their own violation, liability or cost — the
alert is free or near-free and every dollar is in the fix:**

| Business | Alert price | Fix price |
|---|---|---|
| ViolationWatch | **$9/building/month** | $350 simple cure · $950 OATH hearing · $1.800+ complex · $500/month retainer |
| Insparisk | **free, unlimited buildings** | inspections $300–800 per elevator, $15k–100k facade |
| Alt Legal | watch is a **$30–95 add-on** | its own marketing tells firms the value is the **enforcement billables** the alert surfaces |
| Levelset | alerts bundled | **$59 per notice filed** — the filing is the product |

> **No example was found of anyone selling a pure alert, at a meaningful price, to the party the
> alert is about.** Sell the trigger to whoever profits from it — never to whoever it happens to.

## The success stories for trigger-based cold outreach are fabricated

Two cases circulate constantly: Baird Hall scraping the iTunes API to reach $1,3M ARR, and Jake
Atwood's $1,2M ARR from Indeed-triggered cold email. **Both were checked against primary sources and
neither survives.** The Indie Hackers transcript contains no mention of iTunes API scraping — Hall
describes hand-researched outreach, 10–30 emails a day, and explicitly criticises mass blasts. The
Atwood interview contains no trigger events, no Indeed, and no ARR figure at all. Both trace to a
cluster of cold-outreach *tool vendors'* content marketing.

**The one genuine, decades-sustained trigger→outreach industry is attorney direct mail off public
arrest, accident and bankruptcy records** — ~7,9% response, mailed within days. But: physical mail,
targeting distressed individuals, selling representation. Never a subscription.

## And the framing itself is a known fraud vector

USPTO, the FTC and multiple law firms publish active warnings about solicitors who use a business's
**own public filing data** — serial number, filing date, legal name — to send official-looking demands.
Legitimate outreach built on *"we have public data about your regulatory situation"* is
pattern-matched to that scam by recipients and probably by spam filters. Separately, CAN-SPAM carries
**US$53.088 per email, uncapped** — Verkada, an ordinary security-camera company, paid **US$2,95M** in
2024.

## What this changes

The shape requested — API trigger → direct outreach → sell to the affected company — is the
**worst-evidenced** version of a trigger business. The well-evidenced version **inverts the buyer.**

**The rule going forward:** a trigger is only sellable if there is a third party who makes money by
knowing first. Identify that party before designing anything. If the only interested party is the one
the event happened to, the alert is a lead magnet and the business is the remedy — which requires
credentials, per-customer work, or both.

---

## FORM 5500 DELINQUENCY LEAD FEED — killed 10 Aug 2026 (candidate 13)

The first candidate to satisfy the alert finding — sell the trigger to the professional who profits,
not to the company in trouble. It died on something more embarrassing.

**1. THE BUYERS ARE NOT ENUMERABLE — and that was the whole premise.**
The sponsors are beautifully enumerable: EFAST2 bulk files, free, ~800.000 plans a year. **The buyers
are not.** SPBA — the TPAs' own trade body — states plainly that no standard definition of "TPA"
exists: its comprehensive membership is **~185 firms**, while "probably a couple thousand entities may
do TPA work to some degree." NAPA's 20.000+ and ASPPA's 6.900–9.000 are **individuals, not firms**.
NABIP's 100.000+ are overwhelmingly health brokers, the wrong buyer. No BLS code isolates the
occupation. **No free bulk directory of TPAs, retirement advisers or ERISA attorneys exists** — the
buyer list requires paid commercial enrichment layered on fragmented association directories.

> **I verified the enumerability of the leads and never checked the enumerability of the buyers.**

**2. The lead itself is adverse-selected.** Delinquency correlates with dysfunction — a dead or absent
prior adviser, non-responsive sponsors, missing records. Taking on a delinquent plan means
reconstructing multi-year records and carrying DFVCP execution risk. The literature treats it as a
liability category, not a clean win. No source confirms that delinquent sponsors are a *wanted* lead
type.

**3. Four detection blind spots, and timing fixes only one.**
- Form 5558 extensions are not public — fixable by computing each plan's own extended deadline rather
  than a blanket October date.
- **One-participant/5500-EZ plans are excluded from public data entirely.** IRS, verbatim:
  *"Information for a one-participant plan... will not be published on the internet."* A naive scan
  misflags compliant solo-401(k) sponsors as delinquent.
- **MEP/PEP adopting employers** correctly have no EIN-level filing — more false positives, growing
  post-SECURE.
- **EIN and plan-number matching is documented as unreliable by DOL's own watchdog**: GAO-14-441 found
  naming conventions and identification numbers inconsistent, and 18% of records unmatchable.

**4. And the competitor picture was already adverse.** DOL runs the identical algorithm internally —
its **Stop-Filer Initiative** sends inquiry letters, lifting compliance from 34,5% to 56,4% in one
cohort and 11,0% to 69,0% in another — and **the DOL letter is precisely what destroys DFVCP
eligibility**, so the product races the government for a window the government is closing. Seven
vendors already monetise this data: miEdge/Zywave (~$2.400–7.000/seat/year), Judy Diamond
($795–3.900/year with a 19-signal "Red Flags" layer and a blog series called *Prospecting the Federal
Form 5500*), and **form5500search.com at $49/month flat with unlimited unlocks and CSV export.**

**What was actually fine:** the legal perimeter. No DOL usage restriction on EFAST2 data; ABA Model
Rule 7.3 permits written B2B solicitation of entities that routinely buy such services; and the
USPTO/FTC scam warnings do **not** transfer — those concern impersonation and fake official notices,
not prospecting from public data. Legally clean, commercially dead.

## THE LESSON — a lead-data business needs TWO enumerable populations

The requirement set says *"an enumerable, contactable, solvent population."* For a data or lead
product that test must be applied **to the buyer, not to the records being sold.**

> **Check the buyer's enumerability before the lead's.** Public registries make the *subjects* of data
> easy to count and the *purchasers* of data easy to assume. Thirteen candidates in, this is the first
> that failed on the buyer side alone.

And a corollary worth keeping: **an agency that publishes a public register often works that register
itself.** DOL, IRS, CBP and USPTO all run internal programmes off their own data. Before treating a
public dataset as an unwatched signal, check whether the publishing agency is already acting on it.

### Form 5500 — red team amendment, two quantitative kills

**The feed is factually wrong for a quarter of the year.** DOL's own filing-pattern study (N=752.671):
only **50% of filings arrive by 31 July, 90% by 15 October, and under 20% of large plans file by
31 July.** So from 1 August to 15 October roughly **40% of fully compliant plans — and over 80% of
large ones — are indistinguishable from delinquents.** One batch of leads who reply *"we filed a
5558"* ends the buyer relationship.

**The signal is annual, not monthly.** For calendar-year plans the true delinquent cohort materialises
once a year, in late October. **A monthly subscription for an annual signal is structurally
mispriced.** And 8,3% of filers filed more than ~14 months after year-end — a large share self-cure
with no intervention.

**The exclusivity window is eight weeks.** In the studied year DOL's OCA mailed its inquiries on
**15 December** — about two months after the only date on which the signal stops being wrong. And the
DOL letter *itself recommends DFVCP*, so the government detects the lead and delivers the remedy
referral, free, achieving 56–69% compliance unaided.

Also corrected: miEdge sells state-level retirement prospecting at **$34,95–$59,99/month** — a far
lower floor than the enterprise seat pricing suggested.

**TWO NEW TESTS, both generalisable:**

1. **Is the signal continuous or seasonal?** A once-a-year event cannot support monthly recurring
   revenue. Establish the cadence of the underlying event before choosing the pricing model.
2. **How wide is the exclusivity window?** Measure the gap between the earliest point you can detect
   cleanly and the point the incumbent or the agency acts. Here it was eight weeks a year. If that gap
   is short, there is no subscription — at best a seasonal list.
