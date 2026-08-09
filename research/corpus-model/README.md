# The corpus-in-a-folder model

> **The product is the corpus. The MD file is just the interface.**

A downloadable folder that turns the buyer's own AI into an expert at one specific, expensive,
repeated task. A markdown operating procedure plus a folder of reference material, dropped into a
ChatGPT or Claude Project. The buyer installs nothing and needs no new software — only the AI
subscription they already have.

## The design rules, settled

| Rule | Why |
|---|---|
| **Plain files for a Project, never a Claude Skill** | A Skill needs a paid plan, code execution and an org-admin toggle, and Anthropic's own docs tell users to install Skills only from trusted sources. Plain markdown carries no executable code and works on free tiers. |
| **AI does the assembly, never the sourcing** | If a model can generate the corpus from nothing, the buyer's model can too — the prompt test fails by definition, and it reintroduces the hallucination the corpus exists to prevent. Every claim must trace to a real document. |
| **The moat is the context window** | The buyer's AI can read a 50-page folder. It cannot read 54.000 rulings. The product is the distillation of volume they physically cannot ingest. |
| **The corpus must be lawfully redistributable** | US government works and UK Open Government Licence material are fine. Exam board papers (AQA, Pearson, OCR) and standards bodies (ISO, ABNT, ASTM) are commercial copyright — a corpus containing their text is infringing, however useful. |
| **Sell to the professional who repeats the task** | Not the individual who faces it once. They are AI-comfortable, enumerable, have budget, and compare the price to a hire rather than to a report. |

## Hunt 1 — United States: appeals, forms, hidden criteria

Six candidates. One STRONG.

| Candidate | Price | Verdict |
|---|---|---|
| **Apparel & Footwear HTS Classification Defense Corpus** | US$297 | **STRONG** |
| CBP Cash & Goods Seizure Response | US$297 | VIABLE |
| Denied & Underpaid Home Insurance Claim Corpus | US$167 | VIABLE |
| Trademark Office Action Answer Kit | US$147 | — |
| FSVP Importer Kit | US$297 | — |
| Health Insurance Appeal Corpus | US$97 | WEAK — free advocacy overlap |

## The winner: HTS Classification Defense Corpus

A small US clothing or footwear brand importing from Asia must declare a 10-digit tariff code for
every product, and **the legal responsibility sits with the brand, not its customs broker.** Getting
it wrong costs duties, penalties, and a CBP letter with a 30-day clock.

US$297 for a folder containing every published CBP classification ruling for clothing and footwear,
normalised, revocation-chained, and indexed by the physical feature that decides the code.

### Why a prompt cannot do it — and this is measured, not argued

**ATLAS, arXiv 2509.18400** [VERIFIED by fetch]. A purpose-built fine-tune of LLaMA-3.3-70B achieves
*"40 percent fully correct 10-digit classifications and 57.5 percent correct 6-digit
classifications"* — quoted verbatim — with *"improvements of 15 points over GPT-5-Thinking and 27.5
points over Gemini-2.5-Pro-Thinking."*

So the best purpose-built model gets **40%** of 10-digit codes right, and general frontier models
sit 15–27,5 points below that. (Those baselines are subtraction from the stated improvements, not
figures the paper prints directly — stated here as derived, because it matters.)

**A bare model is wrong most of the time at exactly the digit where the duty rate lives.** No other
candidate in this project has a published, quantified failure rate for the buyer's own tool on the
buyer's own task.

### The corpus — independently verified, every figure matching

| Check | Result |
|---|---|
| `rulings.cbp.gov/api/search?term=apparel` | **HTTP 200, totalHits = 54.117** |
| `...?term=footwear` | **HTTP 200, totalHits = 8.947** |
| Revocation-chain fields present | **`revokedBy`, `modifiedBy`, `operationallyRevoked`, `revokes`, `modifies`, `relatedRulings`** |
| `rulings.cbp.gov/api/ruling/F87174` | **HTTP 200**, 2.126 chars of full text |
| That ruling's content | **`6110.30.3020`, duty `32.9%`**, 51% acrylic / 49% polyester women's knit sweater — verbatim |

No API key. No login. **US government works, so the corpus is public domain and freely
redistributable** — which clears the licensing screen that kills the education version.

### What makes it defensible

The corpus does not make the model smarter. It converts the task from **recall** (~25% accurate)
into **retrieval-and-check** against tens of thousands of real documents with revocation status
attached. Those are different tasks.

Two specific failures it prevents:
- **The invented ruling number.** Asked to support its answer, a model names a plausible NY N-series
  ruling that does not exist — or cites one that was *revoked*, which only the `revokedBy` field
  reveals. A fabricated citation in a CF-28 response costs credibility with the officer deciding
  your culpability level.
- **The wrong statistical suffix at a different duty rate.** A single percentage point of fiber
  content moves 6110.30 to 6110.20 or 6110.10 at materially different rates. The model returns one
  confident code and no indication the breakpoint decided it.

### Why the buyer is right

A small importer classifies **every product, every season** — so it is a repeated task, which is the
"second employee" shape. They are legally responsible for the number. They are AI-comfortable by
2026. And they compare US$297 to a customs consultant's hourly rate, not to a US$20 ebook.

### The open question

**CBP HQ H350722** (Jan 2026) reportedly holds that an AI classification tool is permissible as a
suggestion aid only if separated from the entry portal, meaningfully disclaimed, and not directing
the importer or broker on the code that appears on an entry — and that a licensed broker must make
the actual entry classification when acting for others. [PLAUSIBLE — firm summaries only, the ruling
text itself was not fetched.] **This must be read directly before any copy is written**, because it
defines what the product may and may not claim.

## Still running

Hunt 2 — UK and Brazil published-decision corpora, including UK planning appeals.
Hunt 3 — education, technical practice and open domain, with the licensing screen.

---

## Hunt 2 — UK and Brazil published-decision corpora

Six candidates. **Two STRONG.**

| Candidate | Country | Price | Verdict |
|---|---|---|---|
| **ET Respondent's Corpus** — small employer facing an employment tribunal | UK | US$397 | **STRONG** |
| **Recurso em 3 Dias** — TCU licitação corpus for public-tender bidders | Brazil | US$197 | **STRONG** |
| Service Charge Tribunal Corpus — leasehold service-charge disputes | UK | US$149 | VIABLE |
| Defesa Fiscal PME — CARF corpus for tax impugnação | Brazil | US$397 | VIABLE |
| Planning Appeal Decisions Corpus | UK | US$297 | **WEAK — corpus BLOCKED** |
| Appeal Ready — planning decision-pattern library | UK | US$149 | — |

### The UK legal foundation — verified from the primary source

**Legal Services Act 2007 s.12** [VERIFIED by direct fetch of legislation.gov.uk]. Reserved legal
activities are *only*: (a) exercise of a right of audience, (b) conduct of litigation, (c) reserved
instrument activities, (d) probate activities, (e) notarial activities, (f) administration of oaths.

**General legal advice is not among them.** Unregulated providers may lawfully supply legal
information and advice in England and Wales.

And **FTT Property Chamber Rules 2013, rule 14** [VERIFIED]: *"A party may appoint a representative
(whether legally qualified or not)"* — lay representation is normal.

That makes England and Wales materially safer ground for a self-help corpus than the United States,
where unauthorised practice of law is prohibited in every state. Immigration (OISC) and claims
management (FCA) remain carved out entirely.

### The corpora — independently verified end to end

| Corpus | Decisions | Access |
|---|---|---|
| Residential property tribunal (`residential_property_tribunal_decision`) | **17.581** | gov.uk search API, HTTP 200, no key |
| ...of which Leasehold disputes (management) | **6.995** | Same, category-filtered |
| **Employment tribunal** (`employment_tribunal_decision`) | **133.287** | gov.uk search API, HTTP 200, no key |

**The full pipeline was proven, not assumed:** search API → content API → attachment URL →
`assets.publishing.service.gov.uk` PDF, HTTP 200, 496.578 bytes. Enumerate, resolve, download.

133.287 employment tribunal decisions is the largest corpus found anywhere in this project, and it
is the context-window moat in its purest form — no buyer's AI can ingest it.

### The candidate that died, and it was the favoured one

**Planning appeals: corpus `BLOCKED`.** The Planning Inspectorate's decisions could not be
enumerated — the verifier independently attempted the same three endpoints and failed. This was the
idea flagged as "test this first" on the strength of its buyer and its money-at-stake. It failed the
one screen made mandatory after an earlier plan's free test proved unrunnable.

**The screen worked.** Counting the corpus rather than claiming it is now non-negotiable.

### Demand evidence worth noting

For the leasehold candidate, managing agents publicly report a *"sharp rise in AI-drafted
complaints… multiple challenges per week on larger portfolios"* that **fail** because the model
misapplies section 20 consultation rules [VERIFIED by fetch].

That is unusually direct evidence for this whole model: buyers are *already* using ChatGPT for this
exact task and *already* failing on the specifics a corpus would fix.

---

## Hunt 3 — education, technical practice, open domain

Six candidates. **Every one cleared the licensing screen as REDISTRIBUTABLE and every corpus came
back BULK-AVAILABLE.** Two STRONG.

| Candidate | Country | Price | Verdict |
|---|---|---|---|
| **The Classification Desk** — HTS tariff classification | US | US$397 | **STRONG** |
| **TARIFF PACK** — vertical HTS corpora | US | US$149 | **STRONG** |
| VET Assessment Architect — Australian RTO assessment tools | Australia | US$397 | VIABLE |
| The Hazard Analysis Workbench — FDA preventive controls | US | US$197 | VIABLE |
| RADAR SUPLEMENTOS — ANVISA dietary supplements | Brazil | US$127 | VIABLE |
| Licensing-Ready — Texas childcare licensing | US | US$147 | WEAK |

### The education version survives, but only in a specific form

The obvious education idea — exam board past papers and mark schemes — is **infringing** and was
correctly never proposed. What survived instead is **Australian VET**, and the licence was verified
rather than assumed:

- Training package content released after 16 Sep 2011 is **Creative Commons
  Attribution-No Derivative Works 3.0 Australia** — verbatim commercial redistribution with
  attribution is expressly permitted [VERIFIED]. The product design honours the ND term by shipping
  units verbatim and keeping all original analysis in separate files.
- The 2025 Standards instruments are **CC BY 4.0, "any purpose, even commercially"** [VERIFIED].
- Training-package Companion Volumes have varying developer licences — **excluded, not
  redistributed.**
- ASQA guidance licence obtained secondhand only (direct fetch 403) — **must be re-verified before
  shipping.**

And a genuinely useful technical finding: **training.gov.au is a JavaScript single-page app that AI
browsing tools cannot read** — a fetch returns an empty Nuxt shell. So the buyer's AI *cannot* look
this up even if it tries, while an undocumented JSON API returns 15.165 current units and per-unit
PDF/DOCX assets. That is the context-window moat plus an access moat.

---

# THE CONVERGENCE — the most significant finding of the session

**HTS tariff classification was arrived at five separate times, by five different lenses, across
two independent workflows, and rated STRONG three times.**

| Arrival | Lens | Framing given to the agent | Price |
|---|---|---|---|
| Hunt 1 | hidden-criteria | "criteria insiders know" | US$297 |
| Hunt 3 | technical-practice | "applying a complex published framework" | US$397 |
| Hunt 3 | open-domain | "richest redistributable corpus anywhere" | US$149 |

Five lenses were handed deliberately different starting points — fighting a rejection, complex
forms, hidden criteria, professional practice, and open domain — and independently optimised into
the same answer. That is not coincidence. It is the mechanism selecting for its own optimum.

**Why this specific problem wins on every axis at once:**

| Axis | HTS classification |
|---|---|
| Model failure rate | **Measured and published** — the only candidate in the project with this |
| Corpus size | 54.117 apparel + 8.947 footwear rulings, verified by fetch |
| Corpus licence | **US government works — public domain** |
| Corpus metadata | `revokedBy` / `modifiedBy` / `operationallyRevoked` — nobody has structured this |
| Repeat use | Every product, every season, every entry |
| Liability | Sits on the **importer of record**, not the broker |
| Buyer count | Importers, plus **~11.000 licensed customs brokers** |
| Buyer type | Business, AI-comfortable, compares the price to a consultant's hour |

**The pricing spread is itself a finding.** Three independent agents priced the same product at
US$149, US$297 and US$397. Nobody thought it was a US$29 product, and nobody converged on a number —
so the price is genuinely unproven and belongs in the first test rather than in the plan.

## What remains unverified, and both are an hour's work

1. **The apparel/footwear importer population.** Census confirms **239.231 identified US importers
   in 2024** [VERIFIED by fetch] and that SMEs are 98,7–98,9% of wholesaler-importers, but the
   apparel-specific slice sits in an image-based table and was not extracted. The arithmetic bounds
   the risk: US$297 × 28 sales/month = US$8.316, so 336 sales/year, which needs a population above
   roughly 5.000 for plausible penetration. Very likely, not yet measured.
2. **CBP HQ H350722** (Jan 2026), which reportedly permits an AI classification tool as a suggestion
   aid only — separated from the entry portal, meaningfully disclaimed, and not directing the code
   that appears on an entry, with the licensed broker making the actual entry classification. Only
   law-firm summaries were obtained. **Read the ruling text before writing a word of copy**, because
   it defines what may be claimed.

Note that H350722, if accurate, makes **brokers a safer buyer rather than a riskier one**: a corpus
that helps a licensed professional do their own CROSS research feeds their judgement rather than
replacing it, which is the most defensible position available.

---

# Both gaps closed — see `HTS_gap_closure.md`

Full working in `research/corpus-model/HTS_gap_closure.md`. Summary and corrections:

| Item | Previous record | Corrected, by direct fetch |
|---|---|---|
| Identified US importers, 2024 | 239.231 | **240.535** (2023: 242.515) |
| Licensed customs brokers | ~11.000 [PLAUSIBLE] | **13.952 active individual licences**, CBP's own figure in 88 FR 41224 |
| Apparel/footwear importer slice | Not extracted — image table | **6.708 identified importers as a floor** (NAICS 315: 948, 316: 311, 458: 5.449) |
| HQ H350722 | Law-firm summaries only | **Read in full** — 40.504 characters, 16 Jan 2026 |

**The population threshold set above is cleared.** The note required a population above roughly
5.000 for the sales plan to be plausible. The measured floor is 6.708, and excludes the apparel share
of 30.619 nondurable-goods wholesalers, which this Census release cannot resolve at 3-digit NAICS.

**The prior reading of H350722 from summaries was correct**, and the ruling turns out to be stronger
than the summaries suggested. It affirms **HQ H272798**, which expressly permits an unlicensed party
to build a general tariff classification database — and supplies the disclaimer wording CBP accepted.
It also adds a new holding: *"A tool does not constitute a 'person'"*, so a licensed broker must
specify what an automated tool generates. That converts the corpus into a supervision artifact and
confirms brokers as the safer buyer.

**The one forbidden business model, now on the record:** never classify a named customer's specific
goods. HQ H290535 makes that customs business even with a disclaimer attached. It is also the obvious
upsell, which is why it has to be refused in advance rather than declined in the moment.

**Gate 0: PASS on a measured distribution.** 77,6% of US importers have under twenty employees or no
reported employees — the same shape that killed the solicitation monitor. It resolves the other way
because these are trading companies with published import value: mean known import value is
US$3,08M in NAICS 315, against a verified 32,9% duty rate on knitwear. The charity case had no such
arithmetic.
