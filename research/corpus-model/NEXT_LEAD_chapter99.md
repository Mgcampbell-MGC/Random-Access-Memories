# Lead, not a candidate — Chapter 99 overlay stacking (recorded 10 Aug 2026)

Surfaced by the tariff sweep that returned *after* the currency product was killed. **This is not a
rescue of that product.** It is a different problem in the same domain, recorded so it is not lost,
and it has not been audited.

## What changed in the last twelve months

| Change | Date | Effect |
|---|---|---|
| De minimis suspended for all countries | 29 Aug 2025, re-anchored Feb 2026, indefinite by CBP regulation Jun 2026, statutory repeal 1 Jul 2027 | Every shipment needs a full HTS declaration regardless of value. The population that must classify expanded enormously |
| **Section 301 forced-labor tariffs** | **effective 24 July 2026** | 10% or 12,5% across 60 economies. China and Vietnam 12,5%; Bangladesh, India, Indonesia, Cambodia 10% |
| Chapter 99 stacking | current | A China-origin garment needs the ch.61/62 line **plus** legacy 301 (9903.88.xx) **plus** forced-labor 301 (9903.05.31), in a mandatory reporting order |
| EO 14411, penalty mitigation floor | 3 Jun 2026, effective ~1 Sep 2026 | CBP may no longer mitigate a penalty below **50%** of assessment |
| DOJ/DHS Trade Fraud Task Force | launched Aug 2025 | >US$1.000M in recoveries in under a year; apparel a named priority sector |

AAFA: apparel is ~4,78% of US import value and pays **25,70% of all US customs duties.**

## Why it is structurally different from the product that just died

The currency product failed because **ACE hard-rejects an invalid tariff number** — the error caught
itself, for free. A *missing or mis-sequenced Chapter 99 overlay* appears not to be caught the same
way: the codes are individually valid, so the entry clears and the shortfall surfaces later.
Search-level sources indicate CBP does not reliably detect a missing IEEPA-series Chapter 99 line at
entry-summary validation, and that once a CAPE declaration is accepted, post-summary corrections are
blocked. **[LOW CONFIDENCE — search summaries only. Verify against CSMS bulletins and CATAIR before
this is treated as a fact. It is the single load-bearing claim.]**

## The new test, applied

*Name who loses a specific amount when this goes uncaught, and how.* Importer of record, China-origin
apparel: a missed 12,5% overlay on US$1.000.000 of imports is **US$125.000** of underpaid duty, plus
a negligence penalty now floored at 50% of assessment, plus interest — or treble damages if it lands
on the False Claims Act track, which apparel importers already have (Alexis LLC, US$7,6M, Sept 2024;
Barco Uniforms, DOJ complaint Apr 2025).

**It passes the test the dead-code product failed.**

## What carries over as a threat

The red team's Axis 4 applies here **harder, not softer.** USITC published ~31 revisions of the 2025
HTS; Chapter 99 changes faster than anything else in the schedule, and the forced-labor tariff is
seventeen days old with textile tariff-rate quotas promised "no earlier than 1 September 2026." A
one-time downloadable file cannot hold a claim about overlays. **If this is built, it must regenerate
— which contradicts the zero-maintenance folder the corpus model was chosen for.** That tension has
to be resolved before, not after.

## Unaudited

Everything. Specifically: whether the failure lands on the importer or on their broker (most small
importers file through a broker who owns the overlay logic), whether that broker's software already
prompts for it, and whether anyone already sells overlay determination.
