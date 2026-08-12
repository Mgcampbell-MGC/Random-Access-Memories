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

---

## THE LIST HUNT — killed 10 Aug 2026 (candidates 14, 15, 16)

Three survivors came out of the list hunt: two from Brazil and the US that ranked first on their
side, plus a third. All three were killed by the same check, run once, in one search each.

### 14. OFICINAS PERMISSIONÁRIAS (Brazil) — Inmetro-authorised measuring-instrument repair shops

The agent's case: CNAE 3314-7/10 = 13.867 active companies; only these shops may lawfully break the
metrological seal on a commercial scale or fuel pump; **"no vertical SaaS found across three
Portuguese search phrasings."**

**There are two guards, not one, and both were found on the first query.**

**Guard A — the government runs the workflow, free and mandatory.** **PSIE, the Portal de Serviços
do Inmetro nos Estados** (`servicos.rbmlq.gov.br` / `psie.inmetro.gov.br`), is where permissionárias
register users, record every repair, and file the service declaration — **required within 5 working
days.** Inmetro also publishes a full step-by-step wiki for it (`wiki.inmetro.rs.gov.br`) with quick
guides titled *Como Cadastrar Usuário de Oficina Permissionária*, *Como Gerenciar Minhas
Solicitações*, *Como Gerenciar Declarações da Conformidade*. The portal is also the public directory
of the shops themselves — so the "enumerable population" is enumerable because the regulator already
built and published the register it mandates.

**Guard B — a dedicated commercial product already exists, built to the exact clause.**
**SISMETRO** sells *"Gestão de Serviços para Oficinas Permissionárias do Inmetro"* at
`sismetro.com/permissionarias`. Its own copy: *"A solução atende plenamente a legislação vigente, em
especial a Portaria N° 457 de 17 de novembro de 2021 do Inmetro"* — and it states that SS-management
software is itself **provided for at item 5.12.3 of that Portaria.** It ships QR-code equipment tags,
custom checklists, digital client signature in-app, tamper-proof records, and **PSIE integration**
(the operator pastes the SS URL into the *Descrição da Ordem de Serviço* field so Inmetro and the
IPEMs can open it without a SISMETRO login). Capterra: **R$89 per user per month, 121 reviews,
4,5 rating.**

**And the price ceiling kills the arithmetic anyway.** At R$89/technician/month, R$30.000/month needs
**~337 paying seats** inside a population whose *upper bound* is 13.867 companies — most of them one
or two technicians. That is not a niche you can enter second.

### 15. NATIONAL BOARD R-CERTIFICATE REPAIR ORGANIZATIONS (US) — boiler and pressure-vessel repair

The agent's case: "more than 5,000 repair organizations in over 60 countries"; every code repair
requires an **NBIC R-1 (Report of Repair)** or **R-2 (Report of Alteration)** with dual sign-off by
the Authorized Inspector; a public directory at `buscenter.nationalboard.org`; **"no vertical
business/compliance SaaS found."**

**The National Board runs the R-1/R-2 system itself.** **EDT — Electronic Data Transfer**
(`nationalboard.org/index.aspx?pageID=9&ID=60`, now also branded JRS Register) is, in its own words,
*"an interactive document management system that both simplifies and expedites the process of
registering data reports, conveniently accomplished through the internet."* **R-1 and R-2 are both on
the form list.** *"The entire process is completed electronically with just a few clicks of a
button."* It supports the **Form Registration Log requirement of the NBIC for R Certificate
Holders** — the exact recordkeeping obligation a product would have sold.

**It also already fixed the defect the product would have sold against.** EDT's *"electronic
prompting for required information will eliminate the need for correcting reports due to omitted
information"* — reported to have **cut administrative rejection of data reports by as much as 90%.**
There is no fee to be authorised to register; *"most filing fees have been discounted for electronic
filing as compared with filing data reports on paper."* **The incumbent pays you to use its free
system.**

**The one piece EDT does not do fails on cadence and on the human substitute.** The unserved part is
the NB-415 accreditation itself — the written QMS manual and the shop audit. But the R Certificate
runs **three years** (**US$1.150**), the audit is **triennial** (~US$5.000 direct cost), and it is
performed by named humans — the National Board representative or jurisdiction Chief Inspector, plus
the AIA supervisor and the Authorized Inspector. Consultants already sell the manual: **Sperko
Engineering**, **The Welding Expert**, and off-the-shelf editable templates from **8sme Qualite**.
A triennial purchase, against insured human consultants, is not a subscription.

### 16. STATE-REGISTERED SCALE SERVICE AGENCIES (US) — ranked third, and the incumbent is stronger than ranked

Discounted in the hunt as "SmarterCerts exists but is unfunded." Unfunded is not the test — **price
is.** SmarterCerts publishes: **Starter US$210/month (3 technicians, 5.000 certs/yr) + US$995 setup;
Pro US$335/month (5 technicians) + US$1.495 setup; Enterprise custom.** No free tier. That is a
sharper, better-priced incumbent than most of what has been killed here — occupying the same niche,
in the same trade, as candidate 14.

---

## TWO NEW TESTS — and the list hunt's premise is what actually died

### Test A — "no competitor found" is a claim about the searcher, not the market

Both leaders were reported as having **no vertical software after multiple search phrasings.** Both
incumbents surfaced on **the first query I ran.** The difference was vocabulary. The agent searched
the way the *trade* talks — *software para oficina de balanças*. The vendors write the way the
*regulation* talks: *"Oficinas Permissionárias do Inmetro"*, *"Portaria N° 457"*, *"item 5.12.3"*,
*"RBMLQ-I"*, *"NBIC Form Registration Log"*, *"R-1"*, *"EDT"*.

> **Search for the incumbent in the regulation's own vocabulary — the portaria number, the form
> number, the portal's name, the accreditation document's code. That is what the vendor put on its
> landing page, because that is what the buyer types.**

A negative competitor result is only admissible once the regulation's own nouns have been used as
queries. Until then it means nothing.

### Test B — the regulator builds the software for its own mandatory filings

Candidates 14 and 15 died identically, in two countries, two languages, two legal systems: **the body
that demands the filing had already built and shipped the filing system, free, and required its use.**
Inmetro built PSIE. The National Board built EDT. Both validate the fields. Both are mandatory or
strongly preferred. Both are documented and taught for free by the mandating body.

The reason is structural, not accidental: **the recipient of a mandatory filing wants the data more
than the filer wants to send it.** Machine-readable, validated, on time. That incentive is far
stronger than any repair shop's desire for nicer paperwork, so the regulator builds first and gives
it away.

> **A mandatory filing to a government or standards body is the *worst* place to look for unserved
> software, not the best.**

**The one apparent counter-example, and what it actually shows.** Tax filing is a mandatory filing
with an enormous private software industry. The difference is population size and heterogeneity: the
IRS serves ~160 million filers with wildly varying inputs, so it cannot build one form that fits;
Inmetro serves a few thousand shops filing one repair record. So:

- **Small, homogeneous filing population → the regulator has already eaten it.** (PSIE, EDT, the DOL
  Stop-Filer Initiative, the CBP downstream validator.)
- **Enormous, heterogeneous filing population → a funded incumbent has already eaten it.** (Intuit,
  ADP, Zywave.)
- The band between them is where an independent could live — **and "regulated population that repeats
  a mandatory filing" almost never lands in it.**

### What this means for the search itself

The list hunt was built to escape the lead-magnet trap by demanding *an enumerable, contactable,
solvent population that repeats a task.* Every time, "enumerable population that repeats a task"
resolved into **"regulated population that repeats a mandatory filing"** — because a public register
is what makes a population enumerable in the first place. **The property that made the buyers
findable is the same property that guarantees the regulator built the tool.** That is the same shape
as the constraint trap recorded earlier, one level up.

> The enumerability requirement and the free-guard requirement are in direct tension. Any population
> enumerable *because a regulator registers it* is a population whose recurring task that regulator
> has an incentive to systematise for free.

**So the next hunt must find populations that are enumerable for a reason other than regulation** —
enumerable because they buy something, list themselves, publish, hold an asset, or transact on a
platform — and whose recurring task is owed to **no one who wants the data.**

---

# THE FEMALE-MARKET THESIS, TESTED — nine kills, one survivor (10 August 2026)

**The thesis:** *"markets whose buyers are overwhelmingly women running real businesses are served by
software built by people who never did the job — tech bros building for a niche they are not in, so
the incumbents are mismatched."*

Ten candidates, four independent lenses (US/UK woman-run trades; structural mismatch read out of
incumbent review text; Brazil where phone-selling in Portuguese is permitted; and the
computes-on-private-files shape). Every one went through an adversarial pass whose default was KILL
and which was required to re-run the competitor search in **vendor vocabulary**.

## Verdict on the thesis: it does not survive contact, and the way it failed is the useful part

| Candidate | Killed by |
|---|---|
| Marketplace commission audit for salons/med-spas (Fresha, Booksy) | **Booksy Biz ships the identical flow free inside the app the buyer already pays for** — Boost details lists every commissioned client with a per-client **Claim** button, reason picker and evidence attachments |
| VialCheck — injectable COGS for med spas | **Spa Ledger, US$499/month**, "injectable cost tracking… reconciled against Allergan and Galderma invoices", aimed at med spas with US$1–3m revenue. Same inputs, same computation |
| The Gown ETA Desk — bridal special orders | **BridalLive advertises it on its homepage**: *"track each special order until arrival, and receive alerts for any past-due shipments"* |
| Channel P&L for boutique fitness studios | **Momence ships it natively** — "Earned Revenue minus the Teacher's Payout… both will show on the class details page" — with a native ClassPass integration |
| RunCheck — co-manufacturer invoice vs BOM | **Guidance (guidance.so) sells exactly this, tiered by co-packer intensity**: US$199 / US$499 / US$899 per month |
| Comissão Conferida — travel-agency commission | **Monde** (2.500 agencies, R$440/mês) ships *"Importação de Extrato CVC"* — *"a conferência exata da loja com o extrato integrado do Systur"* |
| Repasse Certo — Wellhub/TotalPass audit | **DT GYM's landing page is literally titled** *"Fechamento de Gympass e TotalPass automático"*. Two more Brazilian vendors plus a human giving the audit away as lead generation |
| Comissão Limpa — OTA commission for pousadas | Physics: Booking's own rule closes the window at 48h from checkout, before the monthly invoice being audited even exists |
| RoyaltyCheck — franchisee royalty recheck | No second measurement to diff against. Xponential's 10-K: franchisees are required to use *"a uniform third-party hosted studio management system"* — the franchisor and franchisee read the identical inputs |

**Nine incumbents. Every one surfaced on the verifier's first vendor-vocabulary query, after the
proposing agent had reported the space clear.** Test A fired nine times in one run.

> **These verticals are not neglected. They are densely and competently served, at real prices, by
> vendors who plainly do understand the job.** A med-spa P&L tool at US$499/month and a per-line-item
> commission dispute button inside Booksy are not the work of people who never met the buyer.

The thesis was worth testing and it was tested properly. It is wrong as stated.

## But the one survivor says something the thesis was reaching for

**THE EXPEDITING DESK — score 74, the only survivor.** Reads a residential interior-design firm's own
mailbox for vendor order acknowledgements, ship notices and delay emails, matches each to her open
purchase orders, and produces a daily "what moved / what needs chasing" list.

Interior design is the most female-dominated category in the set — so the thesis pointed at the right
place. But it survived for a **completely different reason than the thesis predicted.** The
incumbents are not bad and they are not absent:

- Studio Designer (20.000+ users, US$69–119 per seat per month) has a literal **"Expediting &
  Tracking"** help article and *"dedicated fields for acknowledgments, ship dates, and received
  dates"*
- Design Manager sells a **Purchase Order Status Window**; Materio, Programa, Mydoma, DesignFiles,
  Houzz Pro and Procurist all ship procurement modules
- Sixteen further vendors surfaced under vendor vocabulary — Knowlix, Canals.ai, Leverage AI, P1ston,
  Debales, Line, Specsources, Canoa, Focuspilot, Planify, Figurz, Mortar, Roomwork, DesignerInc,
  Daniel House Club, Uncap

**Every one of them shipped FIELDS. Not one shipped INGESTION.** The verifier proved the negative with
a date rather than by absence of search results: Studio Designer's **February 2026** release spent its
AI budget on catalog search and **reverse image search**, and the **May 2026** release on catalog
colour filters and trial-balance fixes. The market leader shipped AI twice in 2026 and pointed it at
product discovery, never at the inbox.

The horizontal version of this is funded and crowded — Canals.ai *"reads vendor PO acknowledgments,
shipping notices, and packing slips"* — but sells to **distributors** with an ERP, at contract sizes
a design firm cannot reach. The category automated the manufacturer's inbox and left the designer's
inbox alone.

**Human substitute clears decisively** — the opposite of the AM Consulte failure. Wishup's interior
design VA is **US$1.299/month** with the scope listed verbatim as *"PO creation, order placement,
tracking, and vendor/installer coordination"*; procurement staff run US$23–37/hour. Proposed price:
**US$199/month**.

**And it is the first recurring-revenue candidate in the record.** Every prior candidate was a
one-shot sale paying full acquisition cost forever. At US$199/month, an LTV near US$2.000 supports a
CAC of US$400–600 — which is 250–400 clicks at US$1,50, so paid search becomes viable for the first
time. Law #9's arithmetic loosens structurally, not by wishful pricing.

**Its two honest weaknesses**, recorded so they are not rediscovered as surprises:
1. **The parser's long tail.** Acknowledgements arrive from hundreds of to-the-trade suppliers in
   inconsistent formats. A 60%-accurate ETA feed is *worse than useless* — she still opens every
   email. This is the only thing that could make it impossible rather than merely unsold.
2. **Mailbox access granted to a faceless unknown vendor on a Brazilian CNPJ.** Bucket B. Mitigated by
   a forwarding address rather than OAuth on day one, which also sidesteps Google restricted-scope
   verification.

**Solvency evidence is the weak part and is recorded as weak.** The proposer's "US$1,7m average
small-firm billings" is invalid — it is aggregate ASID sales divided by firm count, not a measured
distribution. What *is* verified is revealed willingness to pay: this buyer already pays Studio
Designer US$69–119 per seat per month plus a separate accounting stack.

---

# DECKPROOF — cleared on two checks, narrowed hard on the third (10 August 2026)

**Competitor sweep: SURVIVES.** Seventeen queries in vendor register plus six direct fetches. Nothing
ingests a brand's own deck *and* own cost sheet and reconciles across both. What exists is five
clusters, none doing the whole job: free forward calculators from typed input (CPG Guy, BoxNCase,
Margin Velocity, Bravo CPG, Foodbevy, RGM Academy); investor-stage deck auditors (MyDeckAudit,
Frontrunner — wrong buyer, wrong arithmetic); document *generators* (Retail Path US$99 template,
Satellite CPG); enterprise deduction platforms (HighRadius, SPS, Vividly, Esker — the closest
structural analogue, but post-sale against invoices, enterprise-priced); and humans.

**Human substitute clears.** Fractional CPG consultants US$200–450/hour on US$5.000–15.000/month
retainers; broker retainers US$1.000–15.000/month plus 3–7%; sell-sheet consulting US$900–1.200. The
one cheaper human — **Emily Anne Page at US$300** — does a different job (delivery rehearsal) and her
existence is *positive* evidence: she gates her discount on **proof of ECRM purchase**, proving this
exact roster population is reachable and already converts at US$300–500.

**Parser objection: dissolved, and the original test was misread.** Of the 14 PDFs, **11 had a usable
text layer** — pdfplumber worked 79% of the time. Of the 12 failures, **9 were content-absence** (the
publisher deliberately omitted wholesale price from a public-facing catalog) and at most 3 were
OCR-fixable. **The gate was read as a parser failure; it was overwhelmingly a corpus failure.** A
blind measured test on flattened CPG economics sheets returned 84/84 clean and 82/84 degraded, with
**money fields 36/36 on both** and both errors in UPCs, which enter no margin calculation.

**The architecture that makes the accuracy question moot:** the spreadsheet is the *only* source of
computed truth; the deck is never a source of arithmetic, only a set of claims to be checked. Then an
OCR misread produces a **false flag** the user dismisses in ten seconds, an OCR miss produces
silence, and *reciting a wrong margin to a retail buyer becomes architecturally impossible, because
margins never come from pixels.* Add UPC-A check-digit validation locally and the silent-error class
shrinks again. And the confidentiality inverts: **the cost sheet never leaves the machine; the only
thing that would touch cloud vision is the deck — the document she is about to hand to a Kroger
buyer.**

## The check that did damage: LAW #1 fires on two of the three deliverables

**RangeMe is free, is owned by ECRM's parent, and is linked from the roster page itself.** It already
auto-calculates **Case Price** (cost × units per case) and **Buyer Gross Margin** (from Cost and
MSRP), with free explainer articles on margin and MSRP. And ECRM's own prep site carries *"a wealth
of best practices content… how to prepare for a buyer meeting, tips on pitching"* — free, to the same
attendee who paid US$7.000–16.900.

| Deliverable | Status |
|---|---|
| Per-retailer required-fields / retail-readiness checklist | **DEAD** — ECRM gives the informational version away free |
| Margin and case-pack calculators | **DEAD** — RangeMe Basic computes both, free, one click from the roster |
| **Cross-document discrepancy audit** | **ALIVE** — nothing at ECRM or RangeMe reads a PDF deck against a cost spreadsheet |

**RangeMe computes margin from numbers you type in — which is precisely the failure mode DeckProof
claims to catch.** A brand can hold a perfect RangeMe profile and a deck with a wrong margin on slide
9, and RangeMe will never know, because RangeMe never sees the deck.

**What survives is one sentence:** *"Your deck says one thing and your cost sheet says another, in
five places, and the buyer will find it."* Everything else in the specified product is decoration a
US$16.900 attendee already owns.

**Second finding, operational and unwelcome.** The list did not decay — 93 sessions, the same 15 live
rosters, ~456–475 unique named companies with clickable websites, no login, re-fetched today. But
**four days passed and not one new roster published.** Rosters arrive in monthly lumps, not a weekly
drip. The nearest session (24–27 Aug) is already too late to sell a preparation product into. Outbound
must be batched against roster-publication events, and there will be dead weeks. **KeHE Summer Show
is the one clean second source** — public exhibitor directory, no login, named brands, dated. Expo
West, Fancy Food and PLMA are JS-rendered and yield no names to a fetch; Cosmoprof is confirmed
gated.

---

# THE CONVERGENCE — two independent tracks, one shape

DeckProof and The Expediting Desk were produced by completely separate processes: one is a
resurrection from a shelved decision in CPG retail, the other came out of a female-market hunt in US
interior design. They are the same product:

> **Ingest the buyer's own private, messy files — the ones no incumbent can see — and compute
> something the buyer is otherwise doing by hand.**

And both survived for the same reason, which is now the most load-bearing finding in this repo:

> **Every incumbent in both markets built the FIELDS and left the INGESTION.** Studio Designer has
> dedicated fields for acknowledgment and ship dates, and spent its 2026 AI budget on reverse image
> search. RangeMe computes a perfect margin from numbers you type in by hand. The workflow layer is
> comprehensively farmed. **The data-acquisition layer — getting the buyer's own mess into the
> system — is empty, in both markets, at both ends of the price range.**

That is why the lead-magnet mechanism cannot reach either one. Content is free to produce; **reading
a stranger's inbox is not.** There is nothing to publish, so there is nothing to give away.

---

# KILL — THE EXPEDITING DESK (10 August 2026). Found by the founder, in one link.

**Object & Order — https://objectandorder.com/ — ships the identical product, to the identical buyer,
free, with no paid plan by design.**

Verbatim from their own pages:

- *"Track orders from confirmation to delivery with **AI-powered inbox sync**"*
- *"identify order confirmations and shipping updates from vendors, then map tracking numbers and
  delivery dates to the correct line items — **no manual copy-paste**"*
- *"the free procurement platform for design studios"*
- *"Object & Order is free. No subscription. No per-seat charge. No setup fee."*
- *"**Free isn't a trial or a teaser for a paid plan — there is no paid plan.**"*
- Monetised instead by *"a 5% margin over what the vendor charges"* embedded in trade prices.

Bucket A1. Identical product, identical buyer, price zero, and zero is not a promotion — it is the
business model.

## How the screen failed, which is the part worth keeping

The competitor sweep was the centrepiece of this session's method. Seventeen agents ran. A dedicated
adversarial verifier was given one job — kill this candidate using **vendor vocabulary** — and it ran
twenty-plus queries, surfaced sixteen vendors (Knowlix, Canals.ai, Leverage AI, P1ston, Debales,
Line, Specsources, Canoa, Focuspilot, Planify, Figurz, Mortar, Roomwork, DesignerInc, Daniel House
Club, Uncap), fetched Studio Designer's Feb and May 2026 release notes to prove the negative with a
date, and returned SURVIVES at 74.

It missed the only competitor that mattered.

> **A competitor search is implicitly a search for vendors, and a vendor is someone who charges. A
> free competitor is systematically invisible to it** — no pricing page to compare, no Capterra
> category row, no paid keywords, no G2 entry, nothing for a "price / plans / pricing" query to
> catch. Every query in the sweep had a price-shaped hole in it.

**Test C — search for the free one separately, and search for it by its funding model.** Ask *who
earns margin on the goods or money flowing past this software*, then go and look at what that party
publishes. The queries that would have found Object & Order are not software queries at all: *"free
procurement platform interior designers"*, *"designer trade pricing platform no subscription"*,
*"who pays for [vertical] software when it is free"*.

## THE LAW — seventh appearance of the lead-magnet mechanism, and its sharpest form

Previous six were content-funded: a marketing department gives away a template because content costs
nothing. This one is different and worse.

> **Where software sits beside a flow of goods or money, the margin on that flow will fund the
> software to zero. Do not sell software into a transaction you are not taking a cut of.**

The party clearing the transaction can always outprice a pure-software seller, permanently, because
the software is their customer-acquisition cost and the goods are their revenue. This retroactively
explains a string of earlier kills that were recorded separately:

| Free product | Funded by |
|---|---|
| Object & Order's inbox sync | 5% margin on trade prices |
| Booksy Biz's per-client Claim button | payments and Boost commission |
| Momence's contribution margin per class | payments |
| RangeMe's auto-computed case price and buyer gross margin | ECRM's US$7.000–16.900 meeting fees |
| Arhaus Trade Dashboard, Uncap dealer portal, Daniel House Club | goods margin |
| Insparisk Command's free-forever tier | insurance |

**My own workflow surfaced this variant and I under-read it.** The list-reverify agent wrote: *"the
party that earns margin on the goods gives order tracking away free"* — naming Arhaus, Uncap and
Daniel House Club. I recorded it as "narrows the wedge" rather than following it to its conclusion,
which was that somebody would build the entire product on that model and give it away.

## What this does to the horizontal plan

The "one engine, many verticals" expansion proposed hours earlier is damaged at every stop, because
**every vertical on the list has a party earning margin on the goods flow**: freight forwarding
(Freightos, Flexport), parts dealers (the distributor), specialty food (KeHE, UNFI), apparel
wholesale, print brokerage, dental labs (the lab bills the practice).

> **"Order status tracking" may be structurally unsellable as paid software in every vertical, for
> the same reason it is unsellable in this one.** Wherever goods move, someone with margin on the
> movement will fund the tracking to zero.

## What survives, stated narrowly

DeckProof's shield is thinner than claimed. RangeMe is free because ECRM sells meetings — the same
mechanism one step removed, and it already killed two of DeckProof's three deliverables. The single
surviving deliverable — the cross-document discrepancy audit — survives only because **nobody earns
a margin on whether a brand's own deck matches its own cost sheet.** There is no third party clearing
that transaction, so there is no adjacent revenue to fund a free version.

**That is now the test to apply before anything else: name the party who clears the transaction. If
one exists, they will give your software away.**

---

# THE NEW AXIS — complaint as trigger, screenshot as delivery (10 August 2026)

Two changes, both from outside this project, both aimed at the constraint that has actually been
binding all along.

## 1. We hunted for triggers in the wrong place, for thirty candidates

Every trigger ever chased here was a **government record** — a registration, a filing, a violation,
a delinquency, a roster, a licence. That is precisely what walked us into the enumerability trap:
a population is enumerable through a public register only because a regulator maintains that
register, and that regulator has already built and mandated the software free.

**A person complaining in public is also a trigger.** It is:

- **non-regulatory** — no agency owns it, so no agency has pre-built the fix
- **continuously refreshed** — not annual, not seasonal, not a one-time event
- **attributable** — a named person at a named company
- **invisible to incumbents**, who buy keywords rather than read complaints
- **readable by a faceless operator** who never posts anything herself

Surfaces: who liked and commented on the posts of the 10–20 accounts a buyer follows; trade
subreddits, especially the rant threads; 1- and 2-star reviews of the incumbent tools; industry
forums and Facebook groups; YouTube comments under tutorials for the painful workflow; the
incumbent's own community board where users beg for a feature; and job postings as a complaint
proxy — *a company hiring someone to do X by hand is telling you X hurts.*

**This does not revive anything killed by A1.** Nothing beats a free identical product. But it
directly re-scores every candidate killed on **"the trigger is invisible"** — LINELOCK, WRAPCHECK,
and the whole family dismissed because we could not tell when the buyer needed help. That dismissal
rested on the assumption that the only visible signals are public records. The assumption was wrong.

Cost of the whole mechanism: roughly **US$200/month** — inbox infrastructure, a sending platform,
enrichment credits. That is the entire go-to-market, not a piece of one.

**The counterweight, recorded honestly:** practitioners running this at scale report that reply
rates are collapsing across every channel as AI-generated outbound floods the zone. This works
*only* with a hand-raise signal in front of it. Generic outbound is dead, which is consistent with
everything else in this file.

## 2. The screenshot sale — the answer to the trust problem

> **"You are not selling the future. You are selling the screenshot."**

The first cold email contains a **computation performed on that prospect's own situation**, produced
before they pay anything. Not a claim, not a case study — an artifact about them, verifiable against
facts they already hold.

This is what made DeckProof work, and it had been recorded here as a *product* property. It is also
a **distribution mechanic**, and that is the more valuable reading. It is the only known answer to
the question shadowing every candidate for weeks: *why would anyone trust an unknown, faceless
seller on a new Brazilian CNPJ?*

**They do not have to.** They look at their own numbers being wrong.

**It is now a hard requirement.** If the exact artifact in the first email cannot be described —
what it computes, from which inputs, and which fact of the prospect's own lets them verify it on the
spot — the candidate is not finished and does not get proposed.

## 3. A constraint that was drawn too wide, and is hereby narrowed

The founder's rule is **no camera, no personal brand, no influencer or creator work.** That was
being applied as *no audience of any kind*, which is broader than what was actually said.

An **anonymous topic-based page** — no face, no name, no personal identity — violates none of it.
The precedent is Julian Shapiro operating **@GrowthTactics** rather than @DemandCurve: the topic
carries the following, the person stays invisible. Combined with an automated content loop (source
material → LLM → scheduled posts → analytics feeding the next round), it costs nothing and
compounds.

**Permitted from now on. The exclusion covers personal brand, not anonymous topical presence.**

## 4. What was explicitly rejected from the same material

- **Cloudflare's pay-per-crawl / x402 / agent-payment thesis.** Genuinely interesting, and it
  converges with this file's own note that MCP registries are the one uncolonised distribution
  surface. But agent wallets are nascent and "build a paid door and wait for agents to walk through
  it" has no 2026 revenue. **A 2027–28 bet, not a path to R$30.000/month in twelve months.** Build
  toward it — report → dashboard → API → MCP → per-lookup — but every rung must pay on its own.
- **"Agent readiness" / AI-visibility auditing as a business.** Filling fast: Profound, Peec,
  Otterly, Scrunch, plus Semrush and Ahrefs shipping AI-visibility tracking. The *audit* is a good
  wedge; the *fix* (llms.txt, schema markup, docs restructure) is already free content everywhere —
  law #1.
- **The niche data refinery aimed at med spas.** Walks straight into a distributor holding margin on
  the goods. Law 0.

## 5. The screening question, restated

> **Stop asking "what public record tells me this buyer needs help?"**
> **Start asking "where do these people complain out loud, by name, in a place I can read every day?"**

That surface is larger than every government registry searched in this project combined, no
regulator owns it, and no incumbent can close it.

---

# COMPLAINT-TRIGGER HUNT — 3 killed, and the axis was never actually tested (10 Aug 2026)

## The kills (candidates 31–33)

**REPACTUA** — recomputing the *planilha de custos* and repactuação claim for Brazilian outsourced-labour
firms holding public contracts. **Two independent Bucket A kills.**
1. **TOTVS Prestadores de Serviços Terceirização** — *"Mais de 7 mil clientes no segmento"* — ships it.
   From its current release notes: *"você pode reajustar automaticamente os custos dos contratos, com
   base nos dados da próxima convenção coletiva de trabalho… para precificar automaticamente os
   contratos a partir da vigência da nova convenção."* Per-posto, per-município CCT ingestion,
   automatic repricing. For the 7.000 firms already on the ERP the marginal price is **zero**.
2. **The screenshot could not be produced, and this was measured.** The proposer set its own gate:
   ≥15 of 40 contracts must carry a readable planilha de custos. The verifier hit the free PNCP API
   across **1.950 contract records** in four windows and opened the anexos: of 19 labour-intensive
   continuous-service contracts, **0 carried a planilha de custos, a formação de preços file, or the
   winning proposta.** What is attached is the contract PDF, the nota de empenho, the portaria de
   designação de fiscal and the termos aditivos. **0/19 against a required 37,5%.**

**RFQ DESK** — normalised intake for job-shop quoting. **FabQuote (Jparo Systems), US$497 ONE-TIME**,
instant download, aimed at metal fabrication and welding shops: extracts *"material grades,
thicknesses, dimensions, and welding processes"* from messy customer messages, delivers a *"draft
quote summary… to Gmail Drafts"*, and sends *"automated clarification emails when specifications are
missing."* That is the candidate, verbatim, at a one-time price against a proposed US$299/month.
**CloudNC Quote Agent** also takes *"Forward customer RFQs to your Quote Agent inbox."* And the
clearing party the proposer swore did not exist: **Stella Source**, *"$500/mo for fabricators and
$800/mo for service centers, plus transaction fees"*, marketing *"lower transaction fees"*.

**PROVISIONAL** — correção monetária and juros de mora unclaimed on late public payments. Split
between two shipping parties with nothing in the middle: **RecebGov** already takes a CNPJ and
*"automatically locates all contracts in federal, state and municipal databases"* with payment-date
projections; and the computation itself is **free on at least five Brazilian calculator sites**
(DrCalc, Debit, CálculoJurídico, CalculaPrazo, eCálculos). Clearing party: the
**antecipação-de-recebíveis** layer — **bitgov**, which raised **R$8,1 milhões** and already scrapes
exactly this data to underwrite, *"se ela vem ganhando licitações, se vem recebendo."*

## THE REAL RESULT — the axis was not tested, because I pointed the agents at walls

**Two of four hunt lenses returned zero candidates.** Their transcripts say why:

> *"Reclame Aqui and Reddit are blocked. Let me find which Brazilian complaint surfaces I can
> actually read."*
> *"I've hit a hard wall that determines my output. Let me record it precisely rather than fabricate
> evidence."*

**Reddit, LinkedIn, Reclame Aqui, G2, Capterra — the entire complaint-surface stack the axis depends
on — is bot-walled to automated fetching.** The two lenses that *did* produce candidates fell back to
what they could read (job postings, Fórum Contábeis, the PNCP API) and generated from structural
hypotheses instead. **So all three candidates were the old method wearing the new label.** The
complaint-trigger axis has still never been run.

This is a design failure on my part, not evidence about the axis.

**And it is the second appearance of the identical wall.** The B2C verdict weeks ago recorded that
Etsy is bot-walled to *"search, /market, listings, curl, WebFetch, jina.ai proxy… confirmed
independently in three separate check passes"*, and concluded the question *"can only be answered by
her, in a browser, in 30 minutes."* That reconnaissance was never done either.

> **Two separate axes have now been blocked by the same wall, and both times the fix is thirty
> minutes of a human in a browser. No amount of agent capacity substitutes for it.** The surfaces
> where buyers self-identify are precisely the surfaces that defend themselves against automated
> reading — which is *why* incumbents are not mining them, and therefore why the opportunity is real.
> But it cannot be prospected from here.

## A NEW TEST, earned by the Repactua verifier

It converted *"would the screenshot's input data even exist?"* into a measured number, for free, in
an afternoon, against a public API — **0 of 19** — and killed the candidate on physics before a line
of code was written.

> **THE INPUT-EXISTENCE TEST. Before designing anything that computes on a prospect's documents,
> measure what share of real prospects actually have the input, in a readable form, obtainable
> before they pay. State the threshold first, then measure it. A screenshot you cannot produce is
> not a wedge.**

This should have been run on DeckProof in August — and in a sense it was: the parser gate found
public sell sheets exist for only **2,7%** of brands. That was read as a parser failure. It was an
input-existence failure, and the same test names it correctly.

---

# PRE-COMMITTED VERDICT RULES FOR DECKPROOF — written 10 Aug 2026, BEFORE the results landed

Recorded before the six investigation agents returned, so the go/no-go is bound to criteria set in
advance rather than to whatever the evidence happens to permit. The governing discipline, borrowed
from an external memo and adopted verbatim:

> **"Do not reinterpret a failure as 'we need better positioning.'"**

## Any ONE of these is an unconditional KILL. No restructure, no reprice, no second look.

1. **THE LLM GATE.** A single general-purpose pass in Claude or ChatGPT, on the planted fixture, finds
   substantially all the discrepancies with usable citations and no silent arithmetic errors. If the
   buyer's existing chat window does the job, there is no product — and "ours is deterministic" is a
   seller's distinction, not a buyer's, unless the buyer can be shown to feel the difference.
2. **THE DEFECT RATE.** Public sell sheets that state enough numbers to self-check show internal
   arithmetic contradictions in **under ~20%** of cases, AND no independent evidence exists that
   buyers or brokers experience this error class as costly. A checker for a defect that is rare and
   cheap is not a business, however elegant.
3. **THE POPULATION.** Fewer than ~500 reachable US independent brokers / fractional retail-sales
   teams can be enumerated from a source that actually exists, OR the evidence shows these firms
   buy essentially no software. Commission-paid, lean-on-tooling is a real risk, not a rhetorical one.
4. **THE PRECONDITION TRAP.** Brokers do not hold a structured, values-capable price sheet per brand.
   If their "cost sheet" is whatever each client emailed them, the qualified and the needy populations
   are disjoint and the product cannot run on the buyers who need it.
5. **ARITHMETIC.** No mix reaches US$7.400–8.300/month under any of the three pricing models with a
   **derived** account count — attach rate and retention both stated. A number that only works when
   the retention assumption is left unwritten is the error already made once in this file.

## These are NOT kills. They are restructures, and each must arrive with a fix.

- The roster channel being closed by ECRM's terms → change channel, not product.
- Monthly being wrong → switch to credit-pack or per-pack, which is an honest answer for an
  episodically-used tool, not a retreat.
- The brand buyer repeating poorly → sell to the broker.
- Vision or parsing limits → fail closed and disclose coverage.

## And one rule about how the answer gets read

Three of the five investigations returning UNCERTAIN is **not** a pass. It is a statement that the
business cannot be assessed from a desk — which, after thirty-three desk-based kills and zero buyer
contact, would itself be the finding, and the correct response would be the cheapest possible contact
with a real buyer, not another round of analysis.

---

# KILL — DECKPROOF (10 August 2026). Candidate 34. Pre-committed condition #1 fired.

## KILL 1 — BUCKET A, MEASURED: the free substitute does the whole job

The gate was: can the buyer just upload both files to Claude or ChatGPT? It was **measured, not
argued**. Three fixtures built on disk (16, 20 and 40 SKUs), ground truth written to a file without
being printed into context, scored by script:

| Fixture | Planted | Found | False positives | Silent arithmetic errors |
|---|---|---|---|---|
| 1 — 16 SKUs, 8pp | 10 | **10** | 0 | 0 |
| 2 — 20 SKUs, 7pp, distractor cost columns | 12 | **12** | 0 | 0 |
| 3 — 40 SKUs, 6pp, deltas at the rounding threshold | 16 | **16** | 0 | 0 |
| **Total** | **38** | **38** | **0** | **0** across ~380 checks |

The hardest fixture deliberately shrank the plants *inside real rounding noise* — margins off 2–3
points, case prices off 1,8–2,6% — sitting beside ~200 correctly-rounded claims. All separated
correctly, with checkable page-and-cell citations, nothing invented. **And both competitors execute
Python over the uploaded XLSX and PDF, so the arithmetic is not in the weights and will not regress.**

**Three further points, each sufficient on its own:**

1. **The wedge is one copyable paragraph of prompt.** That is *worse* than the funded-incumbent risk
   the candidate was designed to survive, because **a prompt needs no funding to distribute.** Any CPG
   newsletter can publish it free, once, forever.
2. **The demo is self-defeating.** To justify any price she must show the chat failing on the
   prospect's own files. The prospect will test the chat first, at 12–25 SKUs, where it does not fail.
   **The prospect's own experiment closes the sale for the competitor.**
3. **What survives technically does not sell.** Repeatability — nobody re-runs a deck check. Calibrated
   precision — protects against *noise*, and noise is a nuisance resolved at the brand's desk, never a
   wound suffered in front of a category buyer. A stated denominator — genuinely unique, and a
   **compliance artifact**.

## The finding that generalises, and it damages the thesis that led here

> **An audit trail nobody demands has no price.**

CPG pre-sale has **no** party who requires evidence that a check happened: no retailer, no regulator,
no auditor, no insurer, no lender. The coverage report is DeckProof's only structurally unique output
and there is nobody to hand it to.

**This forces a correction to the position that survived thirty-three kills.** The thesis was:
*"when generation becomes free, verification becomes scarce."* The measurement says otherwise — **free
generation brought free verification with it.** The thesis is only true under a condition it never
stated:

> **Verification sells only where a party DEMANDS EVIDENCE THAT THE CHECK HAPPENED — or where the
> check is beyond what a general model can do. Absent both, free generation verifies its own output
> for nothing.**

And the sting: the places where someone *does* demand documented evidence are regulated filings,
audits, insurance and certification — **precisely the space where Law 2 says the regulator already
built the tool free, and where the vise has fired five times.** The refinement narrows the position
rather than relocating it. That must be carried into candidate 35 rather than rediscovered.

## KILL 2 — the fail-closed spec rejects the file population it needs

Values-only XLSX with no formulas in any mapped cell. Brands author price lists in Excel *with*
formulas, with multiple cost definitions and stale references. The spec that makes the product safe
is the spec that disqualifies its own buyers — **the precondition trap, third appearance.**

## KILL 3 — the channel, and my legal reading was wrong

I concluded manual roster reading was permitted because I read the anti-scraping clause. **I missed two
means-neutral clauses in the same section**, fetched verbatim from `ecrm.marketgate.com/UserTerms`:

- **§2(a)(vii)** bars *"data mining or similar data gathering or extraction activities or retrieve data
  or other content from the ECRM Services for purposes of creating or compiling that content for any
  purpose other than your authorized use"* — **no mention of automation.**
- **§2(a)(vi)** bars conduct that *"harvests or otherwise collects information about others, including
  names, e-mail addresses, other contact information."*
- **§1(a)** limits the licence to *"only for Your internal business purposes"*, and *"use for any other
  purpose, is explicitly prohibited."*

The roster is out, by hand or by script. *(Correcting the other reviewer too: the phrase "unauthorized
commercial solicitation" appears nowhere in the document — that was a paraphrase. The bar comes from
(vi), (vii) and §1(a).)*

## KILL 4 — the population is at the floor, and its size cannot be measured

Measured from primary Census files, downloaded and parsed: **NAICS 425120 Wholesale Trade Agents and
Brokers — 33.732 firms**, 35.819 establishments, 79,8% under five employees, 6.501 with 5–99. But
**neither CBP nor SUSB splits 425120 by commodity, so the food/CPG slice cannot be measured.** The
widely repeated *"at least 850 plausible repeat buyers"* is an assumption inside a plausible bracket,
not a finding. After a food-share assumption and a solvency filter: **~350–520 firms** — at or below
the pre-committed floor of 500.

## Recorded because it is the best work in the packet and is reusable

**THE PRICING ANSWER, and it directly answers the founder's question.**

**Neither monthly nor one-time. A credit pack** — US$149 per buyer pack checked, US$595 for 5,
US$1.790 for 20 (US$89,50 each), credits never expiring, **a credit burning only on a completed run**
so a fail-closed INCOMPLETE result costs the customer nothing.

**Monthly is dead for a brand, and this is now evidenced from the retailers' own published calendars:**

- **Sprouts'** Category Review Calendar gives each of ~50 categories exactly **one** new-item
  submission deadline and **one** reset per 12-month cycle (only three categories appear twice)
- **Whole Foods Market UK**: *"There are between 15 and 35 categories per product team, per year, that
  we will be accepting submissions for"*, with off-cycle entry *"strictly limited"*
- **NielsenIQ**: category reviews *"generally occur twice a year"*

So a brand is at **0,25–0,7 uses per month.** A monthly subscription's billing period contains zero
use in most months — one cycle, then ten months of churn to explain, with no live English call
available to save the account. And US$399/month is **18–37× the annual price** of the nearest
seat-subscription comparable (Draftable, US$129–261 per user per **year**).

**The print-preflight comparable cuts the other way, and that is the lesson.** Enfocus PitStop Pro is
US$40/month or US$480/year per seat — deterministic, fail-closed document verification, exactly this
product's shape. It is a subscription because **a print shop preflights every job every day.** Same
product shape, opposite usage shape. *Copying a pricing model without copying the usage frequency is
the error.*

> **Bill the unit the customer's own world already counts.** Retailers define the submission; the
> submission is the billable event. Where a document flow is bursty the market prices per document —
> SafeSend Returns per tax return, PDF remediation per page. Where it is continuous it prices per seat
> per year.

**And the defect rate, partially measured for the first time:** of 12 public CPG pricing documents
stating enough interlocking numbers to self-check, **3 contain a hard internal arithmetic
contradiction (25%, Wilson CI 8,9–53,2%)** and 2 more are mapping-ambiguous; **4 hard defects across
~117 verified claims = 3,4% per claim.** Including — with some irony — **Startup CPG's own
"Pricing 101" tutorial**, which states COGS of US$2,55, then uses US$2,65 in the formula, and prints a
US$4,25 result consistent with neither as written.

## Honest note on the strength of this kill

The commodity measurement is **indicative, not independent**, and every bias runs toward overstating
the free substitute: same model family as the competitor, the tester knew the plant categories a
buyer's prompt would not supply, pre-extracted text rather than uploaded files, far more effort than
one chat turn, and same-fixture repeatability measured at n=0.

And the strongest independent evidence runs the *other* way. **FinVerBench (arXiv 2605.29586)** found
calibration collapse on genuinely ambiguous financial documents: **9 of 14 frontier runs at 59,0%
accuracy with a 100% false-positive rate**, GPT-4.1 at 95,3%, DeepSeek R1 at 95,3% — against **0% FPR
for a deterministic rule-based verifier**, which managed only 51,6% recall. The paper's own words:
*"the central observed challenge is calibration rather than detection."*

**So the kill is commercial, not technical, and it is stated that way deliberately.** The deterministic
tool really is more precise. Precision protects against noise; noise is resolved at a desk; and there
is nobody who requires the certificate. That is the whole argument, and it is enough.

---

# PNCP HUNT — 8 killed (candidates 35–42), 11 Aug 2026. Top score 21.

The prediction was recorded before the run: *automation reality first, Law B second.* Both fired.
But the mechanism is sharper than predicted, and it closes a whole category permanently.

## THE CATEGORY KILL — automated action on a Brazilian government system is closed to THIS founder

Three walls, and they compound. Any one is survivable; together they are structural.

**1. The gov.br Termo de Uso bans the architecture, not just the scraping.** Downloaded and text-
extracted from `acesso.gov.br/faq/_downloads/.../TERMO_DE_USO_E_POLITICA_DE_PRIVACIDADE.pdf` —
a document no proposer had opened:

> *"o cidadão concorda que não usará robôs, sistemas de varredura e armazenamento de dados (como
> spiders ou scrapers)… ou método coletor/extrator de dados automático para acessar, adquirir, copiar
> ou monitorar o gov.br, sem permissão expressa por escrito"*

and — the clause that has not been cited anywhere and is fatal on its own —

> *"Incluem-se nos acessos os realizados através de **serviços de hospedagem (hostings)**, pois devido
> a uma política interna foram considerados **inviáveis** para prestação deste serviço público."*

**A daily cron on a VPS is an access "através de serviços de hospedagem."** The CONTINUITY pillar —
unattended scheduled execution, the thing that made these candidates more than a chat window — is
the precise thing the terms prohibit.

**2. The credential required is the company's entire fiscal identity, and facelessness forbids
asking for it.** The authenticated write needs custody of the customer's **e-CNPJ A1 `.pfx` plus
password**. That certificate reaches e-CAC, DET, eSocial, NF-e issuance, cadastral alteration and
binding digital signature — not just SICAF. So the ask at the point of sale is: *an unnamed woman,
from an anonymous page with no face and no name, cold-calls a stranger and asks them to email their
digital certificate and password, then pay by card on the same call.* Brazilian guidance on exactly
this decision says the opposite — *"Desconfie de empresas sem CNPJ visível, sem avaliações públicas
ou que não constem no registro ICP-Brasil."*

> **The faceless constraint and credential custody are structurally incompatible.** This is not a
> positioning problem and no amount of copy fixes it. **The entire class — software that performs an
> authenticated action on a government system on a customer's behalf — is closed to this founder.**

**3. The labour replaced is ~25 minutes a month.** Six certidões, all issued free and instantly;
two uploads at Compras.gov.br › Manter Fornecedor; one email per órgão.

## The individual kills, briefly

| # | Candidate | Killed by |
|---|---|---|
| 35 | **PAGÁVEL** (regularity pack pushed at each payment) | Credential custody vs facelessness; ~25 min/month of labour replaced. **Law B did NOT fire** — the State genuinely refuses this act: SICAF auto-integrates federal data but *"a comprovação da regularidade fiscal Estadual e Municipal deve ser realizada pelo fornecedor a partir do upload das certidões"* |
| 36 | **ANIVERSÁRIO** (reajuste filed on the anniversary) | **The trigger does not exist in law.** AGU Parecer 3/2023/DECOR/CGU/AGU: *"NÃO HÁ PRECLUSÃO LÓGICA DO DIREITO AO REAJUSTE… EM DECORRÊNCIA DA CELEBRAÇÃO DE ADITAMENTO."* Outer bound is Decreto 20.910/32 — **five years**, retroactive. And TCU Acórdão 1105/2008: the reajuste should be granted *de ofício*. The clock the whole subscription rested on is fiction. Also: no unified protocol system across 5.570 municipalities, and SEI/1Doc external access is *"pessoal e intransferível"* |
| 37 | **SICAF Verde** | The gov.br hosting ban, quoted above |
| 38 | **Pasta Sempre Válida** | Same wall |
| 39 | **MAPA 15** (Polícia Federal controlled-products map) | **Not an action — a file generator.** PF's own ROTEIRO 17 shows submission is a logged-in human clicking *Importar Arquivos → Selecionar o Arquivo → Processar*. No API. And PF ships a **free "Validador TXT Novo"** plus the layout, the product table and video tutorials — Law B, comprehensively |
| 40 | **MAPA TRIMESTRAL** (Exército SisFPC / Polícia Civil) | Same |
| 41 | **CERTIDÃO CONTÍNUA** | Same credential wall |
| 42 | **PUBLICA 94** | Assessed dead by its own proposer |

## WHAT THE RUN ACTUALLY PRODUCED — a data asset worth more than the candidates

All measured by direct call on 11 Aug 2026, no key, no login. **Keep this; it outlives the hunt.**

**The better register was found, and it is not PNCP.** `dadosabertos.compras.gov.br` (OpenAPI at
`/v3/api-docs`, no key) exposes **SICAF itself**:
`GET /modulo-fornecedor/1_consultarFornecedor?ativo=true` → **826.570 active suppliers** (the widely
quoted "700.000" is stale), returning `codigoCnae`, `nomeCnae`, `porteEmpresaId`, `nomeMunicipio`,
`ufSigla`, `naturezaJuridica`, `habilitadoLicitar`. Native filters on CNAE and porte.
**MICROEMPRESA 406.380 · EPP 127.624 · DEMAIS 106.521.**

**PNCP's limits, measured:** `/v1/contratos` has **no supplier filter** — unknown params are silently
ignored, so `niFornecedor` appears to work and does nothing. Page size 10–500; 1000 → HTTP 400.
Rate limiting is real and undocumented: at 8 parallel requests it returns a mix of 503 and an
**HTML page titled "Limite de Requisições Excedido" served with a 200-looking body**, so a naive
ingester silently loses pages — 628 of 760 lost on the first pass.

**Solvency, June 2026 (n=169.505 contracts, 58.154 unique suppliers):** contract value p50 **R$5.000**,
p75 R$39.500, p90 R$243.682, p99 R$5,4mi. Supplier monthly take p50 **R$38.400**, p90 R$1.037.234.
**68% of suppliers have exactly one contract.** The top 1.000 take **69% of all value**; 2.232
suppliers account for 80%. *(11 records exceed R$1 bilhão, the largest R$3,9 trilhão — plainly typos.
Any product reporting value must winsorise.)*

**The repeat-winner list is real:** 16.220 suppliers appear in both June and February (28%).
Filtering to ≥3 distinct months, ≥R$300k cumulative and ≥2 distinct órgãos sizes the class at
**3.500–7.000** — a genuine ~5k population, not an artefact.

**And per-supplier win history does exist**, just not where anyone looked:
`/modulo-contratacoes/3_consultarResultadoItensContratacoes_PNCP_14133` **does** filter by
`niFornecedor`, returning `quantidadeHomologada`, `valorUnitarioHomologado`, `valorTotalHomologado`.

## The law this adds

> **Before proposing any product that acts on a system you do not own, read that system's terms of
> use and find out what identity the action requires.** If the action needs custody of a credential
> that is the customer's whole identity, the trust required is maximal — and maximal trust is
> exactly what a faceless seller cannot supply. Check the credential before the market.

---

# KILL — THE BRAZIL CHANNEL MODEL (11 Aug 2026). Candidate 43, and a category closes with it.

Pre-committed bar: **~30 verified qualifying vendors.** Result: **2.** Generously 4. Not close, and
not a gap more hunting closes.

## Why 2 and not 30 — the market has a structure, and it excludes her precisely

Two investigations independently enumerated close to a census: **186 PartnerStack sales programmes**
and **147 Reditus programmes**, 333 with visible terms. Of the 186, **only 18 are tagged LIFETIME —
and essentially all 18 sit under US$200/month** (SocialBee, Salesflare, CallHippo, KrispCall,
MeetGeek, Campaign Monitor, Sellfy, Ticket Tailor).

Every product genuinely in the US$200–2.000 band pays **first-year-only**, or does not publish:

| Vendor | Verbatim |
|---|---|
| Close | *"30% commission on first-year subscription revenue"* |
| PandaDoc | *"25–40% of revenue from first-year sales"* |
| Cognism | *"15% of sales for the first year"* |
| ZoomInfo | *"10% in Year 1"* |
| Pipedrive | *"20–30% for first 12 months"* |
| HubSpot | *"20% for 3 years"* — behind a US$400/month gate |

> **Published commission rate and product price are inversely correlated across the whole market, and
> the correlation has a cause: vendors pay lifetime only where CAC is trivial and self-serve, and cap
> at twelve months wherever a deal is worth a salesperson's time.**

The founder needs the high-ticket half. **That half does not publish rates and gates entry behind an
English discovery call.** So *"never an unscripted live English call"* is not a footnote in this
model — **it is the primary filter, and it removes the entire half of the market where the arithmetic
could have worked.**

The two that pass: **MRPeasy** (*"20% commission for the first three years"*, US$49–149/user/mo — but
its reseller tier demands *"at least 3 full-time consultants and a physical office in the country"*,
disqualifying) and **Katana** (Core *"Starts at $299/month"*, 20% published only on a PartnerStack
tile, duration unverified). The structurally cleanest thing found in the entire hunt was
**CleanCloud** — *"Earn 20% commission for lifetime"*, no upfront cash, no call — and it fails the
price band at US$99–335/month.

## KILL 2 — the Brazilian price gap, and it is independent of vendor count

Re-fetched 11 Aug 2026: **Bling** R$60 / R$120 / R$650 per month, every tier including unlimited
NF-e. **Conta Azul** R$159,90–719,90. **The Brazilian SME software band is roughly R$150–700/month.**

At 5,11 BRL/USD, a US$299/month product lands on the Brazilian buyer at **~R$2.060–2.260/month**
against a R$399,90 Conta Azul or a R$650 Bling Diamante — **3–5× the incumbent price**, for a product
with an English UI, no NF-e, no boleto, no Pix, and USD card billing carrying 3,5% IOF and 15–25%
cross-border decline rates.

**No commission rate repairs a price gap of that size.**

## KILL 3 — the arithmetic, derived rather than assumed

Simples Nacional Anexo III at R$396.000 RBT12 computes to **9,045% nominal**, and export segregation
removes 49,10% of the DAS repartition → **4,60% effective.** Tax was never the problem. The problem
is what is left after it:

Required gross commission **R$32.803/month = US$6.420**. At the **20%** actually verified (not the
assumed 25%), that is **US$32.100/month of managed recurring revenue** — and at Katana's real
US$299 price, **107 customers.** Not the 24–75 estimated.

The verifier also rejected its own investigation's friendlier number, correctly: *"26 customers at
US$1.000"* is arithmetically fine and practically void, **because the number of verified vendors
pairing a ~US$1.000/month product with a published recurring commission is ZERO across all five
investigations.**

## And "no Brazil presence" means the opposite of what the model assumed

The model read an absent Brazilian GTM as an open lane. The evidence reads it as **a rational vendor
decline**: the vendors most isolated from Brazil are isolated *because they are small and cheap* —
Sirvoy, the only vendor with no Portuguese anywhere, prices at **EUR11–44/month**, which makes the
arithmetic hopeless by construction.

> **Absence of a foreign vendor in a market is evidence about the market at least as often as it is
> evidence of opportunity — the same lesson as "nobody sells this", relearned on the distribution
> side.**

## What this closes

**The reseller/channel category is closed**, for a structural reason rather than a local one: the
commission market pays lifetime only below the price point that could reach the target, gates the
profitable half behind English calls, and the Brazilian buyer will not pay foreign prices for a
product without NF-e, boleto or Pix.

**And one finding cuts the other way and should be kept:** the measured Brazilian SME software band —
**R$150–700/month** — is a real, solvent, addressable market. R$30.000/month at R$300/month is **100
customers**; at R$650 it is **46**. That is not a fantasy number. It says any product for this founder
must be **built for Brazil, priced in reais inside that band, and sold on WhatsApp** — not imported,
and not priced in dollars.

---

# BRAZIL WHATSAPP B2B HUNT (11 Aug 2026) — 7 killed, **1 SURVIVOR at 72**

## First, the grounding, which is a permanent asset

An agent downloaded and processed **the entire Receita Federal CNPJ open base** (~4,9 GB, reference
2026-07: Estabelecimentos 0-9, Empresas 0-9, Simples) and counted directly.

**Definition used:** `situacao_cadastral='02'` (ativa) AND `identificador_matriz_filial='1'` (matriz)
AND not a currently-active MEI.

- 27.800.278 active establishments · 26.486.756 active matrizes · 17.195.659 active MEI
- **13.033.275 active non-MEI companies nationally — the real addressable universe**
- **133 CNAEs clear 20.000.** 59 clear 50.000. The 20k–150k band holds ~6,2 million companies
- **Volume is definitively NOT the binding constraint.** Whatever kills a candidate, it is not size.

**And it corrected my own instruction.** I told the hunt to size segments with SICAF. That was wrong:
**the SICAF/national ratio spans 580×** — 58% for atacado médico-hospitalar, 16% for construção,
**0,1% for criação de bovinos**. SICAF over-ranks government-supplier segments by two orders of
magnitude. It answers *"does this segment sell to government"* and must never be used to size a market.

Contactability is now measured per CNAE: e.g. construção de edifícios **97,2% telefone, 57,4% celular,
87,4% e-mail**; psicologia 77% mobile / 98% email.

## THE SURVIVOR — PASTA LIBERADA

*Cobrança e conferência, por WhatsApp, da documentação mensal do empreiteiro antes da liberação da
medição.*

A construtora cannot release a subcontractor's monthly payment while a labour document is missing.
Today a person in the office chases it by hand, every month, subcontractor by subcontractor. The
product chases unattended, checks, and releases the gate.

**The job, in the incumbent's own words.** Dynadok, verbatim: *"o pagamento de cada medição de obra
depende da conferência de um pacote de **10 a 20 documentos por empreiteiro por mês**"* — NF with 11%
INSS retention, GRF/FGTS with bank proof, GPS, folha analítica, controles de ponto, CND, ASO, ficha de
EPI, ART. A construtora with 8 subcontractors does this **96 times a year, for 24–36 months per site.**

**The stake is legal and specific.** CLT art. 455 (solidary liability in subempreitada) and **Súmula
331 TST** (subsidiary liability of the tomador). One claim from a subcontractor's employee lands on
the construtora at **R$20–80k, and the defence is the monthly folder.** Insoft4, verbatim: *"A falta
de rastreabilidade de apenas um mês ou de um único colaborador rompe o histórico de conformidade."*

**Five kill attempts, all failed:**

| Test | Result |
|---|---|
| **Chat window** | The value is not the reading — reading a GRF is exactly what a general model does well, and the candidate says so explicitly. The value is **unattended pursuit of 8–15 subcontractors who don't open email, every month for 36 months**, plus **the payment gate state**, plus **a 5-year archive recoverable for a hearing**. A chat session produces none of the three, and it is not a distributable prompt |
| **Contador (LAW 6)** | **The documents belong to a third legal person.** The construtora's contador has no mandate over the empreiteiro's folha, ponto or ASO — a different CNPJ with a different accountant. And half the pack (ASO, ficha de EPI, PGR/NR-1, ART) is **SST and engineering, outside DL 9.295/46**. Honest admission recorded: the contador does absorb the adjacent piece (11% retention, EFD-Reinf, DCTFWeb) — *which is precisely why construtoras believe they are covered and are convicted anyway, because a previdenciária retention proves nothing about the bricklayer's FGTS* |
| **Volume** | Re-measured independently. 4120400 = **172.616 national**, 69.365 above microempresa, 97,2% with a phone |
| **LAW 0 — clearing party** | **None found, searched by class not by name.** Supply-chain finance was the strongest hypothesis (bitgov precedent) — Painel Fornecedor/Finnet, Antecipa, Liber, Quartilho, BTG and Citi risco-sacado all monetise **the nota fiscal receivable**, not the labour dossiê. Sertras states its own model and it cuts the right way: gestão de terceiros is paid by the **contracting** company |
| **LAW B — free/government** | Nothing public delivers the tomador the prestador's folha, ponto or ASO |

**No credential custody** — the empreiteiro uploads its own PDF. That matters after the government-
action category closed on exactly that point.

**The WhatsApp motion is genuinely compliant, not waved through.** The *sale* is by **telephone**
(97,2% of these companies have a landline; a cold call in Portuguese violates no Meta policy and
cannot be banned), plus click-to-WhatsApp ads where the prospect messages first. The *product's*
WhatsApp use is opt-in by construction: the construtora sends each subcontractor a link, **the
subcontractor writes first**, which satisfies both conjunctive conditions of Meta's Business
Messaging Policy, and monthly reminders then go as **UTILITY** templates, never MARKETING. No chip
warming, no unofficial accounts, no rotation.

**Arithmetic:** 100 × R$397 = R$39.700 gross; net ≈ **R$34.868** after Simples (~6%), AI page reading
(~R$1.200), WhatsApp UTILITY templates (~R$750) and infra. **Target met at 88–90 clients.** The funnel
consumes at most **6,5%** of the qualified universe.

## The wound, recorded rather than suppressed

**The incumbent field is roughly twice as dense as the proposer found — Law A fired.** Beyond
Dynadok, GD3, GT Soft, Insoft4, e-Gestiona and Linkana there are **AUTODOC GD4** (construction-
specific, expiry control, integrated with a facial-recognition catraca that blocks site access),
**NETRIN**, **SERTRAS**, **VALIDE**, **SENIOR**, **BMS INTEGRA** and **ACCIO**. **~14 funded vendors
on this exact job.**

It is a wound and not a kill for one measured reason: **not one of them publishes a price, and not
one collects by WhatsApp.** Dynadok's own copy: the empreiteiro attaches *"diretamente pela
plataforma ou por um portal integrado via API ao ERP da construtora"*, billed *"com base na
quantidade de páginas processadas pela IA, com contrato padrão de 12 meses"*.

> **So the differentiation is channel + published price + same-day onboarding — and the channel leg
> is the one thing nobody has measured.** The load-bearing hypothesis, stated by the proposer against
> its own interest: *the small empreiteiro refuses the incumbent's web portal and only answers on
> WhatsApp, so the job stays manual even at construtoras that already bought a portal.* **If that is
> false, the wedge collapses to price alone, which is the weakest wedge that exists against a vendor
> with implementation and an annual contract.**

Two further risks: **Sienge** has the installed base, has medição and caução in-product, and could
ship this as a module. And the AI reading must be accurate enough that *"pasta liberada"* means
something — a false "complete" is exactly the month that breaks the traceability the customer bought.
That argues for the same fail-closed discipline as DeckProof: the product reports and gates; the
construtora decides.

## THE TEST — R$0–200, 8 working days, no code written

Filter the Receita base for 4120400 in SP, porte EPP or DEMAIS, telephone present (33.972 available).
**Call 60.** Two closed questions: *do you hold the empreiteiro's medição payment when a labour
document is missing?* and *how do you chase it today — portal, email or WhatsApp?*

- **≥20 of 60 (33%)** confirm they hold payment AND chase by hand on WhatsApp/phone
- **≥6 of 60 (10%)** commit **money on the call** — a paid 60-day pilot at R$397, card on file
- **Fewer than 6 committing money → kill**

The test is correctly aimed: it does not buy *"the pain exists"* — that is documented by the
incumbents themselves. It buys the only unmeasured claim: **that the incumbent's portal does not
close the loop, and that R$397 to close it by WhatsApp is worth paying.**

## The seven killed alongside it

| Candidate | Killed by |
|---|---|
| PASTA DO CONTRATO | LAW 0 — clearing party, fetched verbatim |
| CADERNO DO PRÉDIO | LAW 0 + LAW A on the first formal query; **Superlógica** named by the proposer as a "future" risk and shown to be a present one; volume also failed |
| PASTA DO TERCEIRO | LAW 0 |
| CIENTE | — |
| VALIDADE | — |
| **BALCÃO** | **LAW 7 via Meta policy.** Its whole differentiation was messaging *the caller*, which fails opt-in (*"businesses must clearly state that a person is opting in"*), display-name matching, and impersonation rules simultaneously |
| **PLANTÃO** | **LAW C — Meta shipped it free, nationally, six months ago.** On 24 Feb 2026 Meta launched native AI agents inside WhatsApp Business in Brazil — conversational, 24/7, free, no add-on. The candidate's own free-competitor analysis argued against a competitor state that had ceased to exist |

---

# WAVE 1 OF THE FOUNDER-FIT HUNT — FOUR LENSES, ZERO CANDIDATES (11 Aug 2026)

All four lenses were told that returning zero with a clear explanation beats returning something weak.
**All four took that option.** Their reasons converge, and the convergence is the finding.

## Lens A — solo health practitioners (psicologia 106.316, odontologia 123.639)

> *"Every structure in this lens died on the **first** formal Portuguese query — Law A fired in
> reverse: the space is dense, not neglected."*

## Lens B — beauty and aesthetics (cabeleireiros 124.273, estética 74.583)

The fullest account, and it generalises: **the operating surface of a beauty business has exactly
five parts and all five are closed.**

1. **The client** — booking, reminders, recall, reviews, loyalty. Booksy, Trinks, Avec, Belle,
   Fresha, SimplesAgenda, plus Meta's free native WhatsApp Business AI agents since 24 Feb 2026.
2. **The money** — and this is the important one. **Capterra Brasil's *free* salon-software category
   lists eleven products with free plans, one of them Square Appointments, *"free for individuals"*.**
   An acquirer giving away complete salon software to win the card flow. The Booksy Claim-button
   precedent, repeating.
3. **The product** — estoque and per-service cost. The agent's most promising non-obvious idea was
   gram-level colour costing, and it **died on the first formal Portuguese query**: **Graces** ships
   *"estoque de uso interno"* with automatic per-service deduction naming *colorações e tratamentos*
   specifically. And **ePrático** ships the whole stack **"sem mensalidade"** — a permanent-licence
   competitor structurally invisible to any pricing-page search, exactly as Law C predicts.
4. **The staff** — chair rental, splits, ponto. Law 6: a recepcionista at R$1.600–2.500 and a contador
   at R$300–800 absorb it, and owners fill chairs for free in WhatsApp and Facebook groups.

## Lens C — events, training, promotion

> *"Both leading hypotheses hit incumbents immediately."*

## Lens D — the job common to all small woman-run service businesses

> *"Every element of the shared operational spine tested dead."* Trade-marketing evidence collection
> specifically: **eMerchan** is agency-specific and **PMR** sells pay-per-visit with no monthly fee.

---

## THE STRUCTURAL FINDING — and it is uncomfortable

> **The woman-dominated small-service segments are the WORST hunting ground in Brazil for this
> founder, and for a reason that has nothing to do with the quality of the ideas.**
>
> These businesses are **payment-dense**. Every one of them takes card payments at the counter. That
> makes the acquirers — Stone, PagSeguro, Cielo, Mercado Pago, InfinitePay, Ton, Square — permanent,
> armed clearing parties who will fund *complete vertical software* to zero to win the card flow.
> **Law 0 is not an occasional risk in these segments. It is the market structure.**

This explains, retrospectively, why the earlier female-market hunt lost nine of ten and why the one
survivor was interior design — **a segment where the designer does not take card payments at a
counter, so no acquirer is funding software into it.**

**The tension is now explicit and it is the real problem:** the buyer she would most enjoy talking to
is, almost by construction, the buyer whose software somebody else is giving away free.

## What this implies for where anything can survive

A segment must be **solvent and reachable but NOT payment-dense** — where money moves by contract,
invoice, transfer or retainer rather than across a counter terminal. That is what protected interior
design, and what protects the construction candidate the founder rejected.

Wave 2 is running eight further lenses. The ones with a structural chance are precisely those least
payment-adjacent: **education and children, the celebration economy, fashion wholesale rather than
retail, new municipal and conselho obligations, and the seams between existing tools.** The ones
touching a counter terminal will die the same way.

## A process error, recorded so it does not recur

The wave-1 schema had a single `candidates` field and **no field for "what I eliminated and why."**
Four agents did substantial elimination work and had nowhere to return it — the reasoning survives
only in their transcripts, partially. **Every future hunt schema must carry an explicit
`whatIEliminatedAndWhy` field, so a zero-candidate run returns its full value.** Wave 2 has the same
flaw and its synthesis agent partially compensates.

---

# WAVE 2 — EIGHT LENSES, ZERO PROPOSALS. And the synthesis that makes it worth it. (11 Aug 2026)

Twelve lenses across two waves. Zero proposals. Not twelve candidates dying of twelve mechanisms —
**twelve agents independently concluding the assigned segments contain no reachable space.**

## PROMOTED TO THE LAW SET — Law 0 is a property of the SEGMENT, not the candidate

> **Law 0 is predictable before any candidate exists, and the predictor is one question:
> DOES THIS BUYER'S CUSTOMER PAY ACROSS A COUNTER TERMINAL?**
> If yes, an acquirer funds complete vertical software to zero to win the card flow, and every
> candidate in that segment is dead on arrival regardless of shape.
> **Apply it at lens-selection time and it costs nothing. Apply it at candidate-evaluation time and
> it costs a wave.**

**Six of the seven CNAEs were structurally closed before wave 2 started.** Four are counter-dense
(9602501, 9602502, 8630504, and 8230001 on its ticketing face). 8599604 has a non-counter clearing
party (Hotmart/Eduzz/Kiwify) plus Sebrae giving training away free. 8650003 is dense on the first
formal query plus the CFP vise.

## THE UNCOMFORTABLE COROLLARY — and it is the real finding of both waves

> **The founder-fit filter and Law 0 are ANTI-CORRELATED.** The set of buyers a 26-year-old from the
> São Paulo events world would enjoy is nearly identical to the set of businesses that take cards at
> a counter. The hunt was aimed at the intersection of *pleasant* and *viable*, and in these segments
> those two sets barely overlap.

## THE SHAPE THAT HAS EVER WORKED — one, out of 44

**PASTA LIBERADA**, scored 72, survived five kill attempts. Stripped of construction, its shape is:

> **Unattended pursuit of a document owed by a THIRD PARTY who is not the customer, sitting behind a
> gate the customer controls, with the customer's own money or liability on the far side of it.**

Four load-bearing properties, all structural rather than argued:

1. **The counterparty is not the buyer.** A chat window cannot chase a stranger for 36 months. The
   value is pursuit and gate-state, never analysis — so the chat-window test cannot fire.
2. **Money is held at the gate.** A data position plus an action, two of the five permitted classes.
3. **No credential custody** — the third party uploads its own PDF. Compatible with facelessness.
4. **Payment moves by contract, not across a terminal.** No acquirer. Law 0 silent, searched by class.
5. **Opt-in is free** — the buyer sends the link, the third party writes first, satisfying Meta's
   conjunctive conditions by the product's own physics.

> **It died on ONE thing: the buyer's daily vocabulary. The mechanism is proven; the segment failed.**

## THE UNTESTED SEAM

**7319002 — promoção de vendas / trade marketing. 179.702 companies, 73% mobile, 97% email. The
largest CNAE on the table and the only one with no clearing party ever identified.**

Wave 1 tested only its **field-evidence face** and found eMerchan (agency-specific) and PMR (pay-per-
visit, no monthly fee). Its **PAYABLES face is untested**: the agency holding a promotora's or
supplier's repasse pending a document. That is PASTA LIBERADA's exact mechanism, in a segment whose
buyer is a marketing person — someone she would talk to naturally.

**UNVERIFIED**, and it carries a live vocabulary risk (RPA, INSS on autônomos) that must be checked
against her tolerance before a single call is dialled. Adjacent and weaker: 8230001's supplier-
payables face, where the gate recurs per event rather than monthly, so the archive value is absent.

## Territory closed — do not re-search

**Segments:** 9602501, 9602502, 8630504 closed entirely — all five parts of the operating surface
occupied by free product. 8650003 dense plus the CFP vise. 8599604 on Hotmart plus Sebrae.
8230001 closed on ticketing, attendee, marketing and content faces. 7319002 closed on field evidence.

**Classes:** any candidate whose buyer's customer pays at a counter terminal — now a **pre-filter,
not a test**. Anything WhatsApp-facing resembling automated replies, and anything messaging an
inbound caller (BALCÃO died on opt-in, display-name matching and impersonation simultaneously).

**Method:** the multi-lens parallel desk hunt over the measured CNAE table. Two waves, twelve lenses,
zero proposals. **The marginal desk-hunt now has a measured expected yield of zero.**

## Process defect, recurring and now twice-recorded

Wave 1's post-mortem mandated a `whatIEliminatedAndWhy` field so a zero-candidate run returns its
value. **Wave 2 shipped without it.** Eight lenses of elimination reasoning exist only in transcripts.
Every hunt schema from here carries that field — the two runs launched after this one do.

---

# THE REFRAME WORKED — 42 candidates, 8+ viable (11 Aug 2026)

Three hunts under the reversed screen produced **24 + 18 candidates** where twelve lenses under the
old screen produced **zero**. The founder's instinct was right and the constraint was mine.

## THE EVIDENCE THAT THE OLD SCREEN WAS WRONG

**Involves** — Brazilian trade-marketing leader: **R$127 milhões revenue 2024 / ~900 clients =
R$11.750 per client per month.** 24× the top of her band. It *cannot profitably serve* a ten-person
agency and does not try.
**eMerchan** — the only vendor covering the exact stage: **200 agências against 179.702 companies =
0,11%.** Publishes no price.
**Trade Force** — *"mais de cem clientes."* **MáximaTech** — 1.300, but atacadistas not agencies.
Sum every disclosed number, zero overlap: **3.000–4.000 paying companies in the whole Brazilian
field-team software industry, mostly brands and wholesalers. Over 97% of the segment buys nothing.**

**The macro floor, fetched:** Cetic.br TIC Empresas 2025 — **36% of Brazilian companies use ERP, 31%
CRM, small firms 29%** — and the survey *excludes* the smallest firms. Sebrae 2025's "historic high"
is 47% using any integrating software: **53% run on spreadsheets in the best year ever recorded.**
Sebrae TIC 2025: **under 13%** of pequenos negócios use the internet for management platforms.

> **THE LAW THIS REPLACES: "an incumbent exists" was never a kill at this scale. The test is
> ADOPTION. If the leader has 900 clients in a 179.702-company segment, 99,5% is open, and she needs
> 0,04% of it.** Existence killed 44 candidates that adoption would have passed.

## CANDIDATE A — FECHA MÊS (score 68). The stronger business.

Turns a merchandising agency's raw field data into the month-end **medição** it sends the brand: the
invoice value, the itemised **glosa** list (visits the brand will refuse to pay for), and real margin
per contract. **R$497/mês up to 8 contracts, R$697 unlimited. 68 customers = 0,038% of the segment.**

- **It sits ABOVE the field app, not against it.** The agency exports from Involves, Contele, PDV Info,
  a Google Form or a spreadsheet; she maps columns once. **Even Involves customers still build the
  medição in Excel**, because Involves knows what happened in-store and nothing about price-per-visit
  or the glosa rule. Both ends of the market are one product.
- **v1 is CSV in, PDF out — two to three weeks.** No API, no integration, no partner, **no Meta
  dependency**, and no credential custody by design.
- **The opener disqualifies in one breath:** *"os contratos de vocês são cobrados por visita, ou é
  valor fechado no mês?"* The word **glosado** self-selects the buyer.
- **The one unmeasured number:** what share of small agencies bill per visit rather than a flat monthly
  fee. Nobody publishes it. The whole business rests on it.
- **Test: under R$500, 12 days.** Three agencies send last month's spreadsheet, she hand-builds the
  medição with no product. Then 50 dials logging the per-visita answer on every call — 50 buyers
  answer the unanswerable question free. **PASS: 2 PIX from 50 dials AND ≥12 of 50 billing per visit.
  FAIL: fewer than 8 of 50.**

## CANDIDATE B — ESCALA DA FESTA (top VIABLE, wave 3). The better founder-fit.

Freelancer shift confirmation for event producers, buffets and agencies: who is booked, who confirmed,
who checked in, per-person no-show history, and the month-end payment list. **R$297/mês.**

- **Her own world**, and the pool is bigger than measured: 72.970 non-MEI on 8230001, **plus CNAE
  5620102 bufê = 55.027** — buffets are the headcount-heavy rosterers and are the truer buyer.
- **THE COUNTERPARTY IS MOTIVATED.** The garçom confirms because the shift is money in his pocket.
  That removes the response-rate risk that every document-chasing candidate carries — a structural
  improvement on PASTA LIBERADA's shape.
- **Adoption near zero.** Buffetmax gates escala *above* its entry plan. **Food Sistemas /
  EventBuffetOS is the closest product in Brazil** — availability checks, 48h confirmation messages,
  alerts when staff do not confirm, geolocated check-in, monthly diária consolidation — buffet-ERP
  shaped, no price, no customer count, not sold standalone. **StaffPRO** has 32.000 freelancers but
  only 6.000 events and R$6MM lifetime, monetising 10% on connections to *strangers* — it sells access
  to strangers, not management of your own 60 trusted garçons.
- **Not the closed booking category** — customer appointment booking never rosters the business's own
  workforce. But **she must never pitch it with the word "agenda".**
- **Solvency holds by the staffing ratio:** 1 waiter per 15–20 guests, diárias R$80–150. A 40-person
  roster implies 600–800 guests, so the buyer grosses tens of thousands a month and R$297 is under 1%.
- **Two honest weaknesses, both arithmetic.** R$297 × 100 = R$29.700 gross ≈ R$26.000 net, so the real
  target is **~115 customers or a R$340 average ticket.** And Brazilian event demand is violently
  seasonal, so 5% monthly churn is optimistic. Both push the R$30.000 month past twelve months.
- **The build gate is the WhatsApp layer — the same wall that killed BALCÃO.** Three lawful designs;
  the shippable one is a pure web link the buffet posts to its existing group (days, zero Meta
  dependency) which degrades the "it chases them itself" promise but carries a paid pilot. Brazil moved
  to per-message pricing in Jan 2026 at **R$0,035–0,09 per UTILITY template**, so a 40-person roster
  costs R$22–58/month — **7–20% of a R$297 subscription.** And a pooled WABA means one customer's
  irritated waiters can drag every other customer's quality rating down.

## Recommendation

**FECHA MÊS first.** Better price, fewer customers, a monthly unavoidable deadline with cash at the end
of it, and — decisively — **no Meta dependency anywhere in the product.** ESCALA's core promise runs
through the exact layer that has already killed a candidate here.

**ESCALA DA FESTA is the immediate second**, and it is where her events career is directly usable. If
the 50 FECHA MÊS calls come back "valor fechado no mês", she switches list and script inside a week.

**Also worth building regardless:** *Precifica Trade* (scored 72) — a free one-page calculator of what
a CLT promoter really costs under the applicable convenção coletiva, with the annual reajuste letter.
It loses as a business (consumed once; obliges her to maintain dozens of union conventions) but the
annual dissídio is a dated, unavoidable cost increase she knows about before the owner has acted.
**Best cold-call door in the file.**

## Verification debt, recorded

The safety classifier was unavailable while eight of these subagents were reviewed. Before any of
these numbers reaches a sales conversation, re-verify by hand: eMerchan's 200 agências, Involves'
R$127mi/900, Food Sistemas' feature list, StaffPRO's 6.000 events, and the WhatsApp per-message rates.
