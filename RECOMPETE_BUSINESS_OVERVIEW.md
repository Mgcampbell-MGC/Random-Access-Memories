# RECOMPETE — Business Overview & Execution Plan

**Done-For-You AI Proposal Production for Small & Mid-Market Federal Contractors**

*Execution-ready overview · Target: $1,000,000+/mo net profit by month 36 · Starting capital: $250,000*

---

## 1. The Business in One Paragraph

RECOMPETE is a done-for-you service that produces finished, compliant federal proposal drafts for small government contractors who have no in-house proposal team. An agentic AI pipeline monitors SAM.gov for a client's opportunities, shreds each RFP into a compliance matrix, drafts every volume grounded in the client's own past-performance corpus, and runs adversarial color-team review — then a named human proposal engineer QAs every deliverable before it goes back to the client. **We sell the finished work product, not software seats.** The client reviews, signs, and submits; we are never in the certification chain. High gross margins come from AI doing 90%+ of the production labor at roughly $220–$250 of inference per proposal, while a thin, honestly-costed human QA layer guarantees quality.

---

## 2. The Problem We Solve

Small federal contractors live and die by recompetes and new bids, but proposal production is brutal:

- **Bid & Proposal (B&P) cost runs 1–4% of contract value**, at **150–400 labor hours per bid**.
- **Consultants charge $10,000–$40,000 per bid**; the only cheaper option is a $300/mo tool plus the owner's nights and weekends.
- Firms **self-throttle to 6–10 bids per year** because they can't staff more — leaving pipeline on the table.
- **A single missed Section L "shall" statement = automatic disqualification.** The stakes are pass/fail, and the work is unforgiving.

The pain is acute, recurring, and — critically — **already in the budget.** B&P is a recognized, pre-approved cost line (FAR 31.205-18). We are not asking a CFO to create a new spend category; we are asking them to spend an existing line more effectively.

---

## 3. The Customer

**Who:** The CEO or lone business-development lead of a US federal/SLED services contractor doing **$3M–$75M in revenue** with **no dedicated proposal staff.** Core codes NAICS 541512 (IT), 541611 (management consulting), plus engineering, logistics, and facilities.

**Purchase triggers (the moments they need us most):**
- An incumbent contract expiring within 270 days (their first-ever recompete).
- 8(a) program graduation window — ~1,200–1,500 firms in-window at any time (our beachhead).
- SDVOSB / Sback verification, or a new multiple-award IDIQ on-ramp.

**Honest market size:** Of ~30,000–40,000 actively-bidding firms, our true-payer serviceable market — firms already paying consultants or demonstrably buying tools with real bid volume — is **~9,000–14,000 firms.** Reaching 550 subscribers is **4–6% penetration of actual payers.** Demand is not the binding constraint.

---

## 4. The Offer

We contract on **outcomes we control**, never on "wins" (win rates fall category-wide as AI floods every solicitation pool — promising wins would be dishonest):

- **100% on-time submission with zero disqualifications.**
- **Recompete-capture readiness** — never scrambling at the deadline again.
- **150+ owner-hours returned per quarter.**
- **Bid/no-bid discipline as a feature:** we *decline ~15% of requested pursuits* when they can't be honestly grounded in the client's corpus. Saying no is part of the value.

**Deliverables:** recompete radar; compliance matrix + outline by next business day; full draft within 3 business days of queue entry; every factual claim cited to the client's own corpus, every forward-looking claim flagged for client attestation; Pink/Red/Gold color-team passes scored against Section M; a named reviewer and dedicated account manager per account.

---

## 5. Pricing & Packaging

Annual contracts, invoiced quarterly **upfront** (this generates float instead of consuming working capital). Month-to-month available at +8%.

| Tier | Price | Includes |
|---|---|---|
| **Core** | $2,500/mo | 2 proposals/mo + recompete radar |
| **Growth** | $4,500/mo | 4 proposals/mo + win/loss analytics |
| **Scale** | $7,500/mo | 8 task-order responses/mo |
| Overage | $1,200/proposal | Beyond tier entitlement |
| À la carte | $1,500/proposal | Self-serve, no subscription |
| "Active Pursuit" bridge | $2,500/mo (month-to-month) | During award-wait; converts to annual on first award |

**Blended ARPA: ~$4,200/mo.** Entry motion: a **$2,000 paid pilot** on one live RFP, credited toward the subscription.

---

## 6. How It Works — The AI + Human Stack

**Design principle:** one durable orchestration spine (Temporal) runs every proposal as a metered workflow. Every inference dollar, QA minute, and client edit is tracked per proposal ID, so quality is *measured, not asserted*.

| Layer | What it does |
|---|---|
| **Monitoring** | Daily SAM.gov bulk extracts + FPDS mirrors surface each client's opportunities |
| **Ingestion** | Two independent extraction passes (LLM + rules) reconcile the RFP; a completeness gate blocks delivery on any unresolved incorporated-by-reference clause |
| **Retrieval** | Per-client corpus in Postgres + pgvector with row-level security and per-client keys — no cross-client leakage |
| **Drafting** | Corpus-grounded generation with provenance citations on every claim |
| **Review** | Pink / Red / Gold adversarial color teams scored against Section M; deterministic shall/page/FAR compliance checks |
| **Human QA** | A named proposal engineer reviews every deliverable (~3.0 hrs/proposal, trending to 2.4) |
| **Resilience** | A second model provider kept warm at 10% of traffic; SOC 2 by month 9 |

**Cost per full proposal:** ~$161 raw inference → **$250 planning number (year 1), falling to $220 at maturity.** Human QA is the other major cost, honestly carried at loaded wages. This is what real service-as-software costs — and the margin still works.

---

## 7. Unit Economics (The Numbers That Matter)

> **Definition:** "Net profit" throughout is **pre-tax operating profit.** Post-tax at a 25% blended rate ≈ $750k/mo at month 36; $1M *post-tax* crosses around month 41.

| Metric | Value |
|---|---|
| Blended ARPA | $4,200/mo |
| Gross margin | **55% (year 1) → 60% (mature)** — humans fully costed, not assumed away |
| Blended CAC | **$6,100** (stress-tested at $12k → still <5-month payback) |
| Monthly churn | 2.9% (= 70% annual logo retention) |
| LTV | ~$84,000 |
| **LTV : CAC** | **~13 : 1** (7:1 even at stress CAC) |
| Net revenue retention | 100–103% |

**Path to $1M/mo net — the volume ladder:**

| Month | Subscribers | Net profit/mo |
|---|---|---|
| **13–14 (cash-flow positive)** | 48 | ~$0 → +$18k |
| 20 | 114 | ~$70k |
| 26 | 231 | ~$260k |
| **36** | **550 subs + 300 à-la-carte** | **≈$998k** |

At month 36: $2.31M subscription + $0.45M à-la-carte revenue, 58% blended gross margin, ~75 total headcount, ~$440k revenue per head.

---

## 8. Use of the $250,000

| Investment | Amount |
|---|---|
| Product build (2 contract engineers, months 1–5) | $120,000 |
| Outbound sales infrastructure | $15,000 |
| Tech E&O + cyber insurance (bound before first paid pilot) | $20,000 |
| Legal (MSA, conflict policy, referral agreements) | $14,000 |
| Conference / field sales | $10,000 |
| SOC 2 Type I (month 9, demand-gated) | $30,000 |
| Working-capital buffer | $41,000 |
| **Total** | **$250,000** |

**Cash trough ≈ $113k around month 5–6**, then recovers to cash-flow positive by month 13–14. Founders take $0 salary in year 1. No outside capital required; everything after compounds from contribution margin. **No acquisitions — every asset is built from scratch.**

---

## 9. The First 90 Days (Execute From Here)

**Weeks 1–2 — Foundation**
- [ ] Form the entity (S-corp), open banking, sign founder IP-assignment agreements.
- [ ] Pull the target list from free SAM.gov / FPDS data: firms with contracts expiring in 90–270 days + 8(a) firms in graduation window.
- [ ] Engage a GovCon-literate attorney for the MSA, conflict-of-interest policy, and reasonable-procedures (FCA) posture.

**Weeks 3–6 — Product v0 + first pilots**
- [ ] Stand up the Temporal pipeline: SAM.gov ingestion → RFP shred → compliance matrix → corpus-grounded draft → color-team review.
- [ ] Build the golden set of 100+ real solicitations to measure extraction recall (gate: ≥98%).
- [ ] Bind tech E&O + cyber insurance **before** touching any client document.
- [ ] Sign **10–12 design partners** at a $1,500–$2,000 paid pilot on one live RFP each.

**Weeks 7–12 — Prove the gate, then sell**
- [ ] Deliver pilots; measure the Block-1 quality gate: **≥80% of drafts accepted with <2 hours of client-side rework**, zero compliance-matrix escapes, QA ≤3.0 hrs/deliverable.
- [ ] Convert design partners to annual subscriptions; collect testimonials and win/loss data.
- [ ] Launch founder-led outbound on the trigger list; stand up the referral program with teaming partners.
- [ ] **Do not scale go-to-market until the quality gate passes** — that discipline is the whole plan.

---

## 10. Milestone Gates (Year 1)

| By month | Milestone | Gate to keep going |
|---|---|---|
| 5 | Product built, first pilots delivered | ≥98% extraction recall + ≥80% pilot acceptance |
| 9 | SOC 2 Type I underway | Demand justifies the spend |
| 13–14 | **Cash-flow positive** | ~$160k+ MRR; QA hours trending down |
| 20 | Cohort-1 renewal defense | ≥68% logo renewal before scaling sales |

---

## 11. Top Risks & How We've Built Against Them

1. **Seasonal Q4 surge** → staffed to P90 (not average), pre-contracted 1099 reviewer bench, published queue-priority policy.
2. **Draft quality** → measured as a hard spend gate *before* GTM scales; client-edit-distance metered from day 1.
3. **Same-RFP conflicts of interest** → exclusivity on a client's own recompete; firewalled reviewers and hard assignment-blocks on open competitions; written conflict policy.
4. **False Claims Act exposure** → we're never in the certification chain; quantitative claims extracted verbatim only, never generated; client attestation + indemnity for client-supplied facts.
5. **Category win-rate saturation** → we contract on controllable outcomes, not wins.
6. **Model price / provider change** → router with a second provider warm; substitution plan for a price shock.
7. **Competitive ARPA pressure** → planning case glides ARPA and CAC to conservative levels; $998k is the case where differentiation holds, with levers (Scale-tier caps, teaming-partner channel) to defend it.

---

## 12. Why This Wins

- **The buyer already has the budget** — B&P is a recognized, pre-approved cost line. No category evangelism.
- **The work is exactly what AI is good at today** — document-heavy, structured, with published evaluation criteria we can measure against.
- **A real moat compounds** — each client's indexed past-performance corpus and win/loss history make their drafts better over time and make switching costly.
- **The math fits the constraint** — the only finalist of three whose *worst-case* year one fits inside $250k while its month-36 math stays in striking distance of $1M/mo net.
- **Built, not bought** — product, GTM engine, partner network, and client base are all built from scratch. Zero acquisition dependence.

---

*This overview was produced by a ten-agent adversarial planning team and certified "airtight" — internally consistent, arithmetically sound, and free of plan-breaking flaws as written — by an independent Lead Critic agent after two full revision rounds. "Airtight" certifies the integrity of the plan, not a guarantee of financial outcomes; execution risk is real and honestly modeled. Full diligence detail lives in the companion document, `BUSINESS_BLUEPRINT.md`.*
