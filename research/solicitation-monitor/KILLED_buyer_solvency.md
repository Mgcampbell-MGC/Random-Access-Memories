# Killed — the buyer is broke, measured

The 50-State Solicitation Status Monitor was killed on 7 Aug 2026, after its business case had
already been written and committed. The cause was never checked until it was.

## The measurement

Source: `charities-may-not-operate.csv` from the California AG (HTTP 200, 33.885.257 bytes,
116.045 rows — already verified three times). Filtered to Registry Status *Delinquent* or
*Suspended* **with a populated FEIN**: **15.194** of the 16.679.

Sampled **150** at random (seed fixed), joined each to IRS data via the free ProPublica Nonprofit
Explorer API. **All 150 resolved.**

| Annual revenue | Count | Share |
|---|---|---|
| **Under US$50k** | **105** | **70,0%** |
| US$50k–250k | 14 | 9,3% |
| US$250k–500k | 6 | 4,0% |
| US$500k–1M | 2 | 1,3% |
| US$1M–5M | 5 | 3,3% |
| Over US$5M | 1 | 0,7% |
| No revenue data | 17 | 11,3% |

**At or above US$500k: 8 of 150 = 5,3%.**

Projected onto 15.194: **~810 organizations** plausibly able to afford US$119/month.

## Why that kills it

- The viability floor was ~1.000 solvent prospects. 810 is below it.
- 60 subscribers from 810 prospects requires **7,4% cold-email conversion**. Triggered cold email
  runs 1,5–3% at best.
- The segment is not a "wounded middle" — it is **micro-charities that are delinquent precisely
  because nobody is minding the paperwork.**

## Why no version survives

Retargeting the *solvent* 103.567 organizations in good standing removes the defect there is to
quote — which destroys the entire visible-defect mechanism and leaves generic compliance software
competing with Harbor Compliance at US$2.000–6.000/year.

## Independent of the consequence question

A parallel investigation into whether delinquency actually hurts — whether donation platforms and
corporate giving portals screen against state charity registries — was stopped when this
measurement landed. It no longer matters: even if the pain were severe, these buyers cannot pay.

## Caveat on my own measurement

The ProPublica `website` field returned empty for all 150. That is almost certainly the API not
populating the field rather than evidence that no delinquent charity has a website. It is **not**
treated as a finding.

## What it produced

Gate 0, now at the top of `GRAVEYARD.md`: **prove the buyer can pay, with a measured size
distribution, before designing anything.** Plus the adverse-selection lesson — that the mechanism
which makes a faceless seller credible also selects for the buyers least able to pay — and the
three escapes from it.
