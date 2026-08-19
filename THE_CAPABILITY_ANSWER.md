# THE CAPABILITY ANSWER — what actually moved by August 2026

**The founder's question: Grok bots, and *"other things that give her 10x 100x abilities."* Researched with
primary sources only. It corrects my own prediction.**

---

## 1. I PREDICTED WRONG, AND THE CORRECTION IS THE FINDING

**I said vision models reading scanned documents would be the 10×.** The capability is real and the prices are
extraordinary — **$1,50 per 1.000 pages** at Google, AWS and Azure alike; **10.000 pages costs $13,50;
a million pages costs $1.499.**

> ### **But it is a COMMODITISER, not a moat.** *"Machine-readability is not a barrier to entry; it is a subsidy paid to everyone simultaneously."*
>
> **The incumbent can buy the same $1,50 API this quarter. So can the registry. So can the next reader of this
> file. Reading a scanned corpus faster than an incumbent buys roughly ONE QUARTER of lead time, because
> their procurement cycle is the only thing slowing them down.**

**The half that survives:** it is asymmetric **only where ACCESS to the corpus is hard** — per-document
paywalled, request-only, delivered on paper, held locally. **There the pipeline that GETS the documents is the
moat, and OCR is merely what finally makes that pipeline economic.**
*(Which is RULE 2's "Brazilian eyes on the ground" finding arriving from a completely different direction.)*

**And accuracy is not what the marketing implies.** olmOCR-Bench, 7.010 unit tests over 1.403 PDFs, published
by the team that ran it: best scores are **81,7 on multi-column, 79,4 on old scans, 44,5 on old-scan maths.**
**Handwriting: no published per-category accuracy from any vendor or benchmark — UNVERIFIED.** Stamps and
seals: nothing published. **~75–85% on hard material is fine for a triage layer and is not fine for a register
of record without a verification step.**

---

## 2. ★★ THE TWO THINGS THAT ARE GENUINELY ASYMMETRIC

### ★ ENTITY RESOLUTION ACROSS REGISTERS — the strongest capability on the list

**OpenSanctions Pairs (arXiv 2603.11051): 755.540 labelled pairs across 293 heterogeneous sources in 31
countries, multilingual, incomplete.**

| | F1 |
|---|---|
| Production rule-based baseline | **91,33%** |
| **GPT-4o** | **98,95%** |
| **A self-hostable 14B distilled model** | **98,23%** |

> **Matching company names across registers with no shared key was an NLP project needing a team and labelled
> data. It is now a prompt at frontier accuracy — and at near-frontier accuracy on a model she can run
> herself.** *(Residual failures: cross-script transliteration, and minor identifier/date inconsistencies.)*

**Why it is asymmetric rather than a subsidy:** *"the value is in the JOIN, not the tool"* — and **the output,
a resolved link table across sources nobody has joined, ACCUMULATES. Nobody who starts in 2027 can retro-build
the 2026 half of it.**

### ★ BROWSER AGENTS AGAINST PORTALS WITH NO BULK EXPORT

**Asymmetric because it eliminates a per-record human cost that incumbents with API relationships never paid
and therefore never automated away.** *(Shortest half-life on the list — registries add APIs and bot defences.)*

**But the published reliability is far worse than the marketing.** OSWorld-Verified, official results run by
the benchmark team, 361 tasks, human baseline **72,36%**:

| Verified | Success |
|---|---|
| **claude-4-sonnet, 50 steps** | **43,9%** |
| OpenAI computer-use-preview | 31,4% |
| o3 | 23,0% |

**No verified result reaches the human baseline.** Cost is **~$0,15–0,25 per record** — **an order of magnitude
more than reading a page of PDF**, which is the reason to prefer a bulk file wherever one exists. And
Anthropic's own docs warn against exactly the unattended overnight use this file would want: the
prompt-injection classifier *"will automatically steer the model to ask for user confirmation,"* which
*"won't be ideal for… use cases without a human in the loop."*

### The property they share, and it is not the AI

> ***"They are the two places where the new capability attaches to something she can hold that the capability
> does not create: a RECORD THAT ONLY EXISTS BECAUSE SHE KEPT IT, and ACCESS TO A SOURCE THAT HAS NO OTHER
> MACHINE DOOR."***

> ### THE OPERATIONAL INSTRUCTION — **stop asking "what can AI now read?" Everyone can read it. Ask "WHAT CAN I NOW READ *AND KEEP*, THAT NOBODY ELSE IS POSITIONED TO KEEP?"**
>
> **That question points at S4 — the compounding dataset — and away from S1, where the deliverable is the
> output of a model anyone can rent.**

---

## 3. ★ VOICE AGENTS — the honest answer, and it does NOT reopen the onboarding law

**Cost is not the constraint and never was: $0,05–0,31 per minute. A twenty-minute onboarding call costs
$2–6.**

### The law, and most of what is written about it is wrong

| | |
|---|---|
| **EU** | **AI Act Art. 50(1) became APPLICABLE 2 August 2026 — seventeen days ago.** Systems interacting directly with natural persons must inform them they are interacting with an AI system, unless obvious |
| **US federal** | **No general disclosure statute. The real constraint is FCC 24-17 (Feb 2024) under the TCPA — and it is a CONSENT rule on OUTBOUND calls, not a disclosure rule.** It reaches residential and wireless numbers, and a great many small suppliers answer on a mobile. **An agent ANSWERING an inbound call is outside it** |
| **California** | **The most-miscited statute in this field.** The B.O.T. Act defines a bot as *"an automated **online** account"* and applies only to platforms with **10.000.000+ unique monthly US visitors**. *"It does not reach a business-to-business phone call. Anyone citing it for voice agents has not read it"* |
| **Utah / Colorado** | Both reorganised since. Utah's duty attaches to **consumer transactions**; Colorado's to **consequential decisions** (employment, housing, credit, insurance, healthcare) and takes effect 1 Jan 2027. **Neither is a general phone-call rule** |
| **Brazil** | **No AI-specific disclosure statute in force.** PL 2338/2023 passed the Senate Dec 2024 and sits in the Câmara. What applies is LGPD art. 20 and the CDC. *"Secondary sources asserting a current Brazilian obligation are describing pending bills, not law"* |

### The ethics, and it went further than I did

**The test is not "is it disclosed." It is: WHAT IS THE COUNTERPARTY TRYING TO LEARN FROM THIS CALL?**

- **(a) Scheduling and intake — legitimate.** Information transfer, no judgement formed. Disclose anyway.
- **(b) Supplier account setup — legitimate WITH disclosure, and it will not do what you want.** *"An agent
  can carry information; it cannot commit her, and the counterparty knows it. The realistic shape is disclosed
  agent relays → she answers in writing, which converts one call into a call PLUS a written loop.
  **It does not remove the constraint. It relocates it.**"*
- **(c) Vendor security review — NO, and not on a technicality.** *"The counterparty is not gathering facts.
  They are forming a judgement about whether a specific person is competent and trustworthy enough to hold
  their clients' data. **THE CALL IS THE CONTROL.** Putting an undisclosed agent through it does not route
  around a formality; it defeats the control by design."* And a disclosed agent fails from the other side —
  a reviewer told *"you are speaking with my AI assistant"* will correctly escalate.
  > ***"(c) is deceptive if hidden and useless if honest. There is no third door."***

**The case against, reported honestly:** nobody calls it deception when a firm uses a receptionist, an
offshore call centre or a paralegal to relay questions — *"if a DISCLOSED AI is treated as categorically
dishonest where an outsourced human doing the identical relay is not, that is status intuition, not ethics."*
And people who cannot speak already use text relay and synthetic speech; *"the morally load-bearing feature is
not the synthetic voice — it is whether the counterparty is misled about WHO IS ANSWERABLE."*

### ★★ And the reframe that settles it for this project

> ***"The constraint that kills candidates is not 'she cannot speak.' It is 'SHE CANNOT BE PRESENT AS AN
> ANSWERABLE PRINCIPAL IN REAL TIME.' A voice agent removes the first and leaves the second exactly where it
> was. Buying a voice agent does not reopen anything the ONBOARDING LAW closed."***
>
> **The frontier that actually moved is DOCUMENTS and BROWSERS — not voice.**

---

## 4. GROK AND X — priced within reach, licensed out of reach

**xAI's published prices:** grok-4.6 at $2/$6 per M tokens · and **server-side tools at $5 per 1.000
invocations, including a dedicated X SEARCH tool** with keyword, semantic and user search, handle filters and
date ranges.

**X's own API has moved to pay-per-usage: $0,005 per post, $0,010 per user, capped at 3 million post reads
per billing cycle.**

> ### **xAI sells you READINGS of X. The X API sells you RECORDS from X.** $5 per 1.000 searches returns model-mediated answers you cannot build a dataset on. $0,005 per post returns the record — **and it is the record that is licence-restricted.**

**The licence, from the X Developer Agreement:** redistribution limited to **Post IDs, DM IDs and User IDs —
not content** · **no more than 1.500.000 Post IDs to any one entity in any 30-day period** · **"aggregate
analysis of X content that does not store any personal data is permitted."**

> **So a CONCLUSION is sellable and the underlying records are not — and the sellable conclusion is precisely
> the output that carries no exclusivity, because anyone with $5 can produce it. Real-time social data is a
> COMMODITY INPUT in 2026, not a differentiated raw material.**
>
> **The one narrow exception is a derived, aggregated series ACCUMULATED OVER TIME** — legal under the
> aggregate-analysis carve-out, and unreconstructable by anyone starting later. **That is a bet on duration,
> not on access. Same shape as the erasure moat.**

**⚠ TWO STANDING GAPS, both needing a human with a browser:** the X Developer Agreement page **returned HTTP
402**, so those clauses come from indexed search results and must be re-verified. And **xAI's own Terms of
Service returned HTTP 403 to every method** — *"xAI's own restrictions on storing, deriving from and reselling
output are UNREAD."*

---

## 5. Everything else, and one loss

| | |
|---|---|
| **Cheap embeddings** | $0,02–0,20 per M tokens. Embedding a million documents costs single digits. **Commoditiser** |
| **Long context + 50% batch** | 1M tokens standard; batch at half price, most finishing under an hour. **Commoditiser** |
| **Structured outputs** | Schema-valid output now *guaranteed* rather than likely. **ASYMMETRIC AS A PRECONDITION — "it is what makes 'no employees' survivable operationally."** The old failure mode was a nightly job dying on malformed JSON with nobody on call |
| **Open weights on a cheap VPS** | **Mostly false.** ~7,7–40 tok/s CPU-only. **At her volumes APIs beat self-hosting.** The exception is the 14B entity-matcher, because that is the task you run millions of times |
| **MCP** | Portable integrations. **Commoditiser** |
| **★ Translation** | **A LOSS.** WMT24's title is still the finding: *"The LLM Era Is Here but MT Is Not Solved Yet."* Good enough that **her native Portuguese is no longer a moat**, not good enough to sell unreviewed legal translation |

**And one Brazilian fact worth keeping:** **DREI Instrução Normativa nº 81, art. 27** requires documents filed
with the Juntas Comerciais to be presented *"em via única"* meeting *"os requisitos mínimos de qualidade que
garantam o máximo de fidelidade entre o arquivo digital gerado e o documento original, quando da
digitalização."* **Fidelity to the IMAGE is the standard. A text layer is nowhere required.**

> **Brazil's company registry is an image archive — and one person can now read it.**

---

## 6. HOW THIS LANDS ON THE ARCHIVE'S BEST CANDIDATE

**`THE_ERASURE_MOAT.md` records a plan whose entire asset is a weekly snapshot of a register the authority
overwrites. Read it against this report:**

| The capability test | Import Chain Integrity |
|---|---|
| *"What can I read AND KEEP that nobody else is positioned to keep?"* | **A weekly archive of a state the agency destroys.** Exactly the question, answered |
| The strongest asymmetric capability — **entity resolution across sources** | **Its core mechanism IS an entity-resolution problem** — matching establishment keys across two snapshots using a stable secondary identifier that survives renumbering |
| Structured outputs as the precondition for unattended operation | The weekly cron is unattended by design |
| Browser agents — expensive, unreliable, short half-life | **Not needed. The source is a bulk file** |
| Voice agents — do not reopen the onboarding law | **Not needed. Cold email, PDF, no call anywhere** |
| OCR — a subsidy everyone gets | **Not needed. The source is already pipe-delimited text** |

> **The archive's strongest candidate needs NONE of the commoditised capabilities and IS BUILT ON BOTH
> ASYMMETRIC ONES. That convergence was not designed — two agents reached it from opposite ends on the same
> day, one reading a five-year-old business plan and one reading 2026 pricing pages.**

**And the priority it sets is unchanged and now better justified: the cron is not the first feature, it is the
first act.** No model, no agent and no budget back-fills a week that was not recorded.
