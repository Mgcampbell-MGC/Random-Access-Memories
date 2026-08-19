# THE ERASURE MOAT — the archive's answer, 19 Aug 2026

**Third miner, data/intelligence slice. One of the twenty-nine plans in that slice clears every constraint in
this file, and it does so by DESIGN rather than by repair. It is the strongest candidate this project has
produced.**

---

## 1. THE LAW IT RESTS ON

> ### THE ERASURE MOAT — ***"FDA erases, it does not archive."***
>
> **The authority publishes a weekly extract of the current state and overwrites the last one. Nobody — not
> the buyer, not a competitor, not the agency's own public search — can reconstruct who vanished, or when,
> without a private archive of weekly snapshots. THAT ARCHIVE BEGINS ACCRUING ON DAY ONE AND CANNOT BE BUILT
> RETROACTIVELY.**

**And the plan proves the erasure rather than asserting it — four independent checks:** absent establishment
keys appear in **0 of 3.478** rows of `registration_listing.txt` · **exactly 1** survives in
`Official_Correspondent.txt` · **274** orphan keys carry no name at all · and `reg_expiry_date_year` holds
**exactly one distinct value (2026)** across 43.989 rows.

**Its build order follows from that and is the whole discipline: *"the weekly cron ships before the product
does."***

---

## 2. THE MECHANISM — a join nobody runs

**Two public tables from the same authority, joined against each other:**

| | |
|---|---|
| **The declaration table** | US importer X declares it uses foreign manufacturers A, B, C, D, E |
| **The current registry table** | Which of A–E actually exist in this week's file |
| **The product** | **The rows where the reference dangles** |

**Computed once over the whole population: 6.325 dangling links across 3.478 distinct absent keys.**

**And it separates a real lapse from a renumbering** using the stable secondary identifier (`FEI_NUMBER`,
which survives re-registration where the internal key does not) looked up across two snapshots. **That
resolver is buildable only with archive history — which is why the cron is day one.**

---

## 3. WHY IT CLEARS EVERY CONSTRAINT

| | |
|---|---|
| **C1 — never speaks** | ***"Cold email only. Delivery is a PDF attached to an email. No call, no app, no login, no English conversation: the entire funnel is written asynchronously in language that can be drafted carefully once and reused."*** Written for a written-only operator **by design, not by repair** |
| **C2 — faceless** | The finding is a factual extract. No name, no reputation, no audience required. *(And an explicit rule: **never use certificate-like graphics or agency logos**, because the agency itself publishes warnings about vendors selling fake registration certificates)* |
| **C4 — no credentials** | **It REFUSES the credential outright.** The customer's own declaration is reconstructed **from the public side**; the customer is then told to verify it in their own account. *The only design in the entire slice that solves C4 by refusal rather than by mitigation* |
| **C5 — capital** | **Under US$150 total before the first sale.** Domain $12 · sending $0–20 · contact enrichment ~$50 · archive storage ~21 MB/week ≈ 1,1 GB/year, "pennies" · **all source data free.** The only stack in the slice compatible with C5 — the others run $289–346/month |
| **THE EXPERT VETO** | ***"It never says 'you are non-compliant' or 'this shipment will be detained.' It says: your filing declares 5, FDA's current file contains 2, here are the listing IDs."*** The recipient supplies the names from their own account and confirms the absence in the regulator's own free search. **Nothing is asserted, so nothing has to be believed** |
| **THE PRODUCTION CEILING** | **FIXED-COST. One join over the whole population produces ~700 individually-computed findings at once.** *"No hosted app, no buyer-side compute, no per-transaction human step. A card purchase and an emailed attachment"* |
| **THE CONSTRAINT-SIDE LAW** | **Renewal runs 1 Oct – 31 Dec, so every January a fresh cohort drops out.** A dated, forward, calendar-driven event the buyer does not control — pre-announceable in September, deliverable in January |

### ★ And two things this project has never had before

**SOLVENCY IS FEE-GATED AND VERIFIED.** *Every prospect paid the agency **US$11.423** between October and
December 2025, or they are not in the file.* **This is the first candidate in seventy-plus where the buyer's
ability to pay is proven by the dataset itself** — and it directly answers the failure recorded in that same
plan: *"the previous candidate's buyers were charities that were delinquent precisely because they had no
money — poverty and the defect were the same thing."*

**AND THE BUYER IS 100% CONTACTABLE — checked, not assumed.** The agency publishes **the responsible person's
name and phone for 5.920 of 5.920** registrants. *(See §5 — this is also where the one serious problem sits.)*

---

## 4. THE FUNNEL, WITH ITS OWN ARITHMETIC

| | |
|---|---|
| Currently-registered establishments | **28.535** |
| US registrants declaring ≥1 foreign manufacturer | **5.920** |
| With at least one dangling reference | **1.846 = 31,18% raw** |
| With two or more — the conservative floor | **891 = 15,05% clean** |
| **Ideal customer profile after exclusions** | **717** |
| Of those, with a K-number finding | **282** |

**Giants are deliberately excluded as procurement-gated** — Walmart, Medline, Cardinal, Henry Schein.

> **THE RAW/CLEAN DOUBLE RATE is itself a mechanism worth keeping: publish both prevalence numbers, never one.
> Reproduced three times on two different weekly snapshots, matching to the digit.** And the pitch is written
> so it **holds under all three possible causes** of a dangling reference — genuine lapse, re-registration,
> or a stale entry the filer never removed — because in every case *"your own federal filing is wrong and only
> you can correct it."*

---

## 5. WHAT WOULD KILL IT — in order

**★ 1. THE CHANNEL. The agency publishes NAME AND PHONE. It does not publish EMAIL.** That is
**THE POSTAL LIST LAW biting on the single best-contactable register found anywhere in this project.** The
plan routes around it with commercial contact enrichment at an **explicitly unverified match rate**, and its
own instruction is to run 50 through enrichment **before building anything.** **She cannot use the phone
numbers. This is the first thing to test and it can be settled in an afternoon.**

**2. THE HEADLINE NUMBERS COULD NOT BE RE-VERIFIED.** *"Bare `accessdata.fda.gov` fails with SSL_ERROR_SYSCALL
from this environment, so the raw files could not be pulled to recompute the 31,18% and 15,05% figures
directly."* The plan's own instruction: ***"should be re-run from an unblocked network as the first act of
the build."*** **Until that is done, the two numbers the whole business rests on are UNVERIFIED.**

**3. THE RECIPIENT MIGHT SHRUG.** *"That supplier re-registered."* The continuity resolver exists precisely to
pre-empt this, but whether it lands is untested.

**4. A LIVE PRICE ANCHOR.** `fdadevicecheck.com` sells a watchlist at **US$19/month.** The plan names it as a
hazard to a US$199 subscription and notes the cost to settle is zero.

**5. THE BACK-FILL WAS BLOCKED.** Whether the Internet Archive holds prior weekly snapshots — which would
back-fill lapse dates instantly instead of over eight weeks — was *"attempted and blocked; worth one retry
from an unblocked network."* **Framed correctly in the plan as something that "accelerates rather than
enables."**

---

## 6. WHY IT IS THE ANSWER TO THE SEAM

**Two earlier miners found that every plan in the archive splits into a fixed-cost COMPUTATION half and a
per-customer ACTION half — and that seven of eight priced the action and gave the computation away.**

> ### **This plan is the one that sells the computation and never touches the action.** It computes a finding from two free public tables, delivers it as a PDF, and tells the buyer to fix it themselves inside their own account. **There is no filing, no signature, no portal, no credential and no conversation — because there is no action half at all.**

**And it holds the only genuine moat named in twenty-nine data plans: an archive of a state the authority
destroys weekly.** *(Compare ClinicEdge, which builds exactly the same asset and then sets its retention to
30 days — deleting the one thing a competitor could not copy.)*

---

## 7. THE CAPABILITY POINT, WHICH INVERTS THE USUAL ONE

**No amount of model capability back-fills an erased archive.** A better-resourced competitor with better
tooling still starts their snapshot series on the day they start it.

> **Agents and cheap inference give her 10× on BUILDING this and 0× on the MOAT — and that is the good news,
> because the same is true for everyone who comes after her. The moat accrues at one week per week and cannot
> be bought.**

**Which sets the priority unambiguously: the cron is not the first feature. It is the first ACT.** Every day
it is not running is a day of moat that can never be recovered.

*(Two miners and the capability agent still out. This has not been red-teamed.)*
