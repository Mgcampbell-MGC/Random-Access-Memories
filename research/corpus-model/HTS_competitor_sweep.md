# HTS corpus — competitor sweep, and the whitespace it exposed

Run 9 August 2026, before writing any blueprint, per the rule adopted after Pora killed LÍQUIDO.
Four parallel sweeps plus direct verification. **Provenance is marked throughout:** [MEASURED] means
I computed it here from primary data, [FETCHED] means I read the page myself, [SWEEP] means a sweep
agent reported it and I did not independently confirm it.

## Verdict

**The field is crowded, and two of my own differentiators are already taken. A third one — which
nobody at any price occupies — turned out to be measurable, large, and unserved.**

The product survives, but not in the shape it was in this morning.

---

## The field, in five tiers

### Tier 1 — free and authoritative (the dangerous tier)

| What | Why it threatens | Status |
|---|---|---|
| **CBP CROSS**, `rulings.cbp.gov` | Same data, free, no login, full-text search, and it already cross-references revoked/modified rulings | [MEASURED] the entire index enumerates via `pageSize=500` — 54.117 apparel records in **11 seconds**. There is no scraping moat whatsoever |
| **CBP Informed Compliance Publications** — *"What Every Member of the Trade Community Should Know About: Footwear"*, *"Classification: Apparel Terminology under the HTSUS"*, *"Textile & Apparel"* | These already organise classification logic **by physical construction feature** — external surface area of upper, sole material, knit vs woven, fibre blend. That was going to be my differentiator | [SWEEP], text-extracted by the agent. They cite **no ruling numbers**, disclaim ruling status, and several sections date to 2008–2010 |
| **USITC HTS** `hts.usitc.gov` | Free, and it has a JSON API | [FETCHED] confirmed — this is what made the whitespace measurable |

### Tier 2 — enterprise

| Vendor | Price | Note |
|---|---|---|
| Descartes CustomsInfo | **$750/user/month** [SWEEP, Capterra listing — not confirmed against Descartes] | Claims 253.000 rulings including *"40,000+ ... found on no other electronic database"* |
| Thomson Reuters ONESOURCE, Westlaw, LexisNexis | Enterprise quote only | Westlaw carries CBP rulings 1962–present, Lexis 1987–present, both bundled inside general legal research |
| WCO Trade Tools, Customs IQ, KYG Trade, Altana | Not published | [FETCHED] KYG Trade's ChatRULINGS tiers are Micro→Enterprise with no figures |

### Tier 3 — the cheap AI wave (2024–2026), the real budget competition

| Vendor | Price [SWEEP unless noted] |
|---|---|
| GingerControl | $0.80 per classification credit. [FETCHED] Positions as *"an HTS classification researcher, not a replacement for customs brokers"* and — notably — already uses the exact H272798 disclaimer language: *"for general reference, educational, and planning purposes only"* |
| Quickcode.ai | $149/mo (100 classifications) → $749/mo → $2.000+/mo |
| Lenzo.ai | $99–$899/month flat |
| Camtom TariffPro | Free 10/month, then ~US$100/mo |
| Zonos Classify | 1.000 free classifications, then contact sales |
| SimplyDuty | 5 free/day, then £0.10 per lookup |
| Digicust, DutyDecoder, Flexport, FindHS.Codes | Free tiers |

### Tier 4 — the closest competitor

**TariffLens** (`tarifflens.ai`) [FETCHED myself]. Built for *"the broker who has to classify 50
products before lunch."* It claims to *"cross-reference 200,000+ CBP binding rulings from CROSS."*

And it already owns the positioning I was going to take:

> *"defensible HTS classifications"* · *"show your work"* · *"builds the audit trail that proves you
> exercised reasonable care"*

It targets Focused Assessment audits and "Your Reasonable Care Obligation" explicitly. No published
pricing.

**This is the single most important competitive finding.** "Research and defence, not
answer-generation" — the positioning I recommended this morning — is taken, by a live tool aimed at
the same buyer.

### Tier 5 — free open source, and one claim I had to correct

| What | Reality |
|---|---|
| `onurkafk/customs-trade-law` — a free AGPL-3.0 Claude Agent Skill for HTS classification and CROSS research [SWEEP] | This is the **methodology half, given away free.** It instructs the model to fetch rulings live rather than bundling a corpus |
| `francisfuzz/tariff-everywhere` — free MCP server, ~134.019 HTS lines [SWEEP] | Schedule only, no rulings |
| Apify actor `ryanclinton/cbp-customs-rulings` [SWEEP] | $20 per 1.000 rulings — the full corpus for tens of dollars |
| **`flexifyai/cross_rulings_hts_dataset_for_tariffs`** — reported as *"18.731 real CROSS rulings, Apache-2.0, free"*, i.e. the corpus half given away | **[MEASURED] This is not what it is, and the sweep's conclusion from it was wrong.** I pulled it: its only feature is `messages` — user/assistant **chat pairs for fine-tuning**. Of 200 sampled messages, **3 contain anything resembling a ruling citation.** No ruling numbers, no full text, no revocation fields. It is training data distilled *from* CROSS, with exactly the citable substance stripped out. It cannot serve as a reference corpus |

Also [MEASURED]: my own HuggingFace search for `customs+rulings` and `CROSS+CBP` returned **nothing**,
and the only HTS datasets found were three 350-row SFT sets with 7–15 downloads.

---

## What I had to give up

Three claims from this morning did not survive.

**1. The revocation chain is not the headline.** I implied it was the killer feature. [MEASURED]
across the complete sets:

| | Rulings | Revoked | Modified | Any | Rate |
|---|---|---|---|---|---|
| apparel | 54.117 | 227 | 329 | 548 | **1,01%** |
| footwear | 8.947 | 45 | 40 | 83 | **0,93%** |

`operationallyRevoked` is `true` for **zero** records in either set. A 1% defect that CROSS already
flags itself is not a product.

**2. "Indexed by physical feature" is partly CBP's, free.** The Footwear and Apparel Terminology
ICPs do this already.

**3. "Defence and reasonable care" is TariffLens's.** Verbatim, on their homepage.

I would rather record all three than carry them into a blueprint.

---

## The whitespace — measured, not argued

Nothing in any tier — not free CROSS, not $750/month Descartes, not TariffLens — answers this
question:

> **Does the tariff code this ruling cites still exist?**

CROSS tells you if a ruling was *revoked*. It says nothing about whether the ruling is still good law
pointing at a **code that has since been renumbered, subdivided or deleted.** The ruling stays live.
The code is dead. Nothing marks it.

### How big it is

[MEASURED] Every apparel and footwear ruling joined against the current USITC HTS (chapters 61–65,
3.535 codes, 922 distinct 8-digit lines, fetched via the USITC JSON API):

| Set | Rulings citing a ch.61–65 line | 8-digit lines cited that no longer exist | 10-digit |
|---|---|---|---|
| **apparel** | 40.211 | **28,9%** (15.790 of 54.722) | **43,2%** (23.460 of 54.335) |
| **footwear** | 7.941 | **25,0%** (2.648 of 10.574) | **25,5%** (1.544 of 6.045) |

**14.315 of 62.320 rulings (23,0%) cite at least one tariff line that no longer exists.** There are
**377 distinct dead 8-digit lines** across the two sets.

### The internal control that proves it is real

Staleness declines monotonically with recency, and recent rulings are nearly clean — which is exactly
what must happen if the measurement is sound, and is not what a parsing bug produces:

| Ruling era | apparel, 8-digit dead | footwear, 8-digit dead |
|---|---|---|
| pre-2000 | 38,4% | 38,0% |
| 2000–2014 | 24,3% | 27,6% |
| **2015+** | **4,1%** | **0,3%** |

37,2% of apparel rulings and 25,9% of footwear rulings predate 2000 [MEASURED], which is why the
aggregate is so high.

### The worst offenders

| Dead line | Rulings citing it | 6-digit heading | Newest citation | Example |
|---|---|---|---|---|
| 6211.42.00 | 1.817 | subdivided | 2017-03-02 | N283205 |
| 6211.43.00 | 1.506 | subdivided | 2017-02-02 | N282430 |
| 6201.93.35 | 889 | **gone entirely** | 2014-10-15 | N257434 |
| 6201.93.30 | 687 | **gone entirely** | 2014-07-15 | N254784 |
| 6404.19.35 | 673 | subdivided | 2012-02-15 | N200955 |
| 6110.10.20 | 586 | **gone entirely** | 2002-01-22 | 965184 |
| 6203.43.40 | 562 | subdivided | 2015-10-16 | N269005 |
| 6202.93.50 | 519 | **gone entirely** | 2015-04-21 | N263240 |
| 6210.40.50 | 506 | subdivided | 2015-02-18 | N261017 |

The mechanism is the ordinary HS revision cycle. 6110.10 was split into 6110.11/12/19 in HS2002 on
the wool and cashmere distinction. 6201.93 vanished in the HS2022 restructure of chapter 62
outerwear. 6211.42.00 was subdivided — the current schedule starts at 6211.42.05. **In the
subdivision cases the 6-digit heading still exists, which is what makes it invisible:** the AI's
answer looks right to six digits and is invalid at the eight and ten digits where the duty actually
sits.

### Two errors I made getting here, both corrected before reporting

- I first treated an 8-digit code as dead unless an exact 8-digit row existed. But the schedule
  sometimes expresses a line only at ten digits (`6304.93.00.00`), so `6304.93.00` read as dead when
  it is alive. Fixed with a prefix rule. This moved the apparel 8-digit figure from 37,5% to 31,2%.
- The USITC endpoint `from=H&to=H` returns **only the bare heading, not its children.** My ranges
  used inclusive endpoints, so everything in headings 6117, 6217, 6310, 6406 and 6507 was wrongly
  counted dead — including two entries in my draft top-20. Fixed by extending each range one heading
  past the last real one, which raised the loaded schedule from 514 to 922 distinct 8-digit lines and
  moved the apparel figure to its final **28,9%**.

Both errors inflated the finding in my favour. The corrected number is still large.

---

## Why this space can be occupied immediately

| Test | Result |
|---|---|
| Is the defect known? | Yes, as **advice to a human**. Trade blogs (Mallory Group, O'Meara, GingerControl) warn "verify the ruling's code is still valid" [SWEEP] |
| Does any product do it? | **No.** Not CROSS, not TariffLens, not Descartes, not KYG, not any tier-3 tool |
| Can the buyer verify it themselves in 30 seconds? | **Yes** — paste the old code into `hts.usitc.gov` and it is not there. This clears the self-evidence bar: two values that differ is information, not borrowed authority |
| Can the buyer's own AI do it unaided? | **No.** It needs a join between two datasets, one of which (the ruling's cited code) is buried in 62.320 documents |
| Does it compete with the free source? | **No — it repairs it.** That is a much better place to stand than "cheaper CROSS" |
| Does it decay? | It **worsens** with every HS revision, which gives an update reason without becoming SaaS |
| Can I build it today? | Detection, yes — done, above. **Successor mapping, not yet:** [MEASURED] the USITC API ignores its own `release` parameter and `getArchivedRevisions` 404s, so prior editions are not machine-readable from there. Mapping dead → replacement needs archived editions or Change Records, and that path is **UNVERIFIED** |

That last row is the honest limit. But detection alone carries the value, because the danger is not
"you cannot find the successor" — it is **citing a dead code with confidence.** "This precedent's
reasoning is sound; its code no longer exists; do not put it on an entry" is the whole warning.

---

## The revised product

**From:** a corpus of apparel and footwear rulings, indexed by physical feature, with revocation
status — three claims, two of them taken, one of them a 1% problem.

**To:** the currency layer on top of the free corpus.

Every apparel and footwear ruling, joined to today's HTS, with each cited code marked **LIVE /
SUBDIVIDED / GONE**, the 1% revocation chain included as hygiene rather than headline, and the
coverage gaps named — because [MEASURED] of 2.769 current 10-digit lines in chapters 61–65, only
**1.183 (42,7%)** have any ruling at all, just **476 (17,2%)** have one from 2015 or later, and
**1.586 have none.** Knowing where there is no precedent is worth as much as knowing where there is.

It keeps the legal perimeter established in `HTS_gap_closure.md`: a general reference, disclaimed per
HQ H272798, never classifying a named customer's goods.

**Price.** [SWEEP] brokers demonstrably pay $595–$1.250 for exam courses, $838 for the Boskage print
reference bundle, and $149–$299 for downloadable recorded webinars. $297 sits above the webinar
ceiling and below the course band, and no dedicated rulings-corpus SKU exists to benchmark against.

## The test, which costs nothing

The wedge and the test are the same artifact: **publish the dead-code table.** The nine rows above
are checkable by anyone in half a minute on a free government site, and they say something no vendor
in any tier is saying. Send it to brokers, and measure whether they answer.

That is the 60-email test that has been costed under US$100 since the first hunt, and it now has
something in the email worth opening.

## Still unverified

- Successor mapping feasibility (archived HTS editions / Change Records).
- Whether the ~43% 10-digit figure translates into the buyer's felt experience — that depends on
  which rulings their AI surfaces, and old rulings are over-represented in the corpus.
- TariffLens pricing, and whether it silently handles code currency without marketing it.
- Descartes' $750/user/month, which is a third-party listing.
