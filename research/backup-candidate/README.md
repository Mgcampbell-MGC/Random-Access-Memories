# The backup: CertGap

Found 7 Aug 2026 by a hunt built around the **visible-defect** pattern — a defect
computable from free public data about a named company *before* any contact.

## What it is

Every appliance brand sold in the US files its energy numbers with the federal
government **twice** — once to earn the ENERGY STAR label, once to certify compliance
with DOE efficiency standards. Both filings are public. Both were completed by the same
manufacturer. **They routinely disagree.**

CertGap is a pre-computed PDF showing a named brand, model by model, where its own two
federal filings contradict each other. US$650 for the initial audit, US$350/quarter to
monitor.

## Verified independently

Both endpoints fetched directly, no login, no API key:

| Source | Endpoint | Result |
|---|---|---|
| ENERGY STAR | `data.energystar.gov/resource/p5st-her9.json` (Socrata) | **HTTP 200.** 4.748 refrigerators, 748 dishwashers, 394 clothes washers; ~90 datasets |
| DOE CCMS | `POST regulations.doe.gov/certification-data/solr/ccms/select` | **HTTP 200** (needs a browser User-Agent). **4.595.423 records, 73 product groups, 7.227 distinct brands** |

The flagship example reproduces exactly:

| Source | Record | Annual energy |
|---|---|---|
| ENERGY STAR | Avanti `AV1081VFK0W` | **249 kWh/yr** (federal standard: 280) |
| DOE CCMS | AVANTI `AV1081VFK0W` | **354 kWh/yr** |

## The mismatch rate — measured, not assumed

This is the reason to hold this candidate. It answers the question ADV-Check cannot.

| Category | Models matched | Mismatched | Rate |
|---|---|---|---|
| Refrigerators | 2.336 | 145 | **6,2%** |
| Dishwashers | 466 | 27 | **5,8%** |
| Clothes washers | 279 | 17 | **6,1%** |
| Dehumidifiers | 329 | 32 | **9,7%** |

Independently reproduced by a second agent using exact normalised model-string matching,
which returned **6,1%** against the designer's claimed 5,3%. Stable across four unrelated
categories.

## Two findings that go against the designer's own fears

**The defect concentrates in card-payers, not legal departments.** Affected brands are
overwhelmingly small importers and private labels — Summit, Commercial Cool, Premium
Levella, Avanti, Zephyr, Insignia, Vissani, Criterion, Upstreman. Exactly **one**
Whirlpool record and **one** LG across everything tested. The "it routes to legal at big
brands" worry is refuted by the data.

**Large deltas defeat the "the databases just lag" brush-off.** 72 findings carry gaps too
big for version skew: Zephyr 69 vs 330 kWh, Premium Levella 314 vs 493, Commercial Cool
286 vs 429.

## The curation problem — including one I found myself

The headline rate is inflated by artifacts, and **every report needs manual curation
before it goes out.** Three distinct artifact classes are now known:

1. **Internal ENERGY STAR duplicates.** The Bosch `SHX78DC**` example was two ENERGY STAR
   rows (215 and 240); DOE said 240, agreeing with one of them. Not a contradiction.
2. **Model-family suffix collisions.** The Maytag example compared `MHW5630H**` against
   `MHW5630M**` — two different models.
3. **Product-class disagreement, found during independent verification.** For the Avanti
   flagship, ENERGY STAR files it as *"Freezerless and Single Door"* while DOE certifies it
   under *"(9.) Upright freezers with automatic defrost."* Different product class means a
   different test procedure and a different standard — so the classification difference may
   **explain** the 105 kWh gap rather than prove an error.

Class 3 is the most awkward, because it is the flagship example. The honest read: the
mechanism is real and the data is free, but the clean quotable rate is likely **2–4%**, not
6%.

## The real constraint, stated plainly

**A few hundred pre-qualified prospects, not thousands.** 46 brands with ≥1 mismatch and 21
with ≥1 large unexplainable delta, from 4 of 73 categories. Extrapolating to 15–20 workable
overlapping categories gives a few hundred named prospects — far below ADV-Check's 15.445
advisers.

So **it only works as a subscription**: roughly **60 recurring customers at US$350/quarter
≈ US$7.000/month**, plus new initial audits. One-off sales at US$650 would need 12–13/month
and would exhaust the pool.

## Against ADV-Check

| Axis | Verdict |
|---|---|
| **X — repeat purchase** | **WINS.** DOE updates roughly biweekly, certification is required per model annually and on any redesign, and brands ship new SKUs across up to 73 groups. Quarterly monitoring is honest. ADV-Check is annual per firm. |
| **Y — list size** | **LOSES,** badly. A few hundred pre-qualified prospects vs 15.445. |
| **Z — price** | Tie at US$650, unproven both ways. |

**Hold both.** CertGap wins the most valuable axis and its defect rate is measured;
ADV-Check has 40x the universe and its defect rate is still unknown. They fail for different
reasons, which is what makes them a real pair rather than a duplicate.

## The kill worth reading

**RangeGap** (pay-transparency posting audit) was killed on verified grounds. The verifier
fetched the actual job ad behind its flagship finding — Vivvi requisition 7595127003 — and
found **"Competitive hourly pay: $23–$29.40 per hour"** in the body text while the API's
`pay_input_ranges` field was empty. The detector's core assumption, that an empty API field
means undisclosed pay, is false. Its claimed 31% defect rate was built on it. Two other
flags were *"Remote — United Kingdom"* (not a covered jurisdiction; a loose regex) and
*"Join our Talent Community!"* (not a requisition).

It would also have died on self-evidence: *"this ad violates NYC LL32"* is a legal
conclusion requiring borrowed authority.

## First test — under US$50

Expand the join from 4 to ~12 overlapping categories (free, one day of compute), then
**hand-verify the top 40 large-delta findings to strip all three artifact classes**, and
email those 40 brands with two values and two links.

**Drop the DOE-penalty language.** It is secondary-sourced garnish that imports authority
Sol does not have, and two contradictory federal numbers do not need it.

**Pass: ≥4 replies engaging with the numbers (10%) and ≥1 paid US$650 within three weeks.**
Below 2 replies and zero sales, fall back to PublicFile Guard — the runner-up, quarterly by
statute, whose load-bearing number could not be reproduced because `www.fcc.gov` returns 403
to this network (a blocked network, not a dead source).
