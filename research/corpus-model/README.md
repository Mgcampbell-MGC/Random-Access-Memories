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
