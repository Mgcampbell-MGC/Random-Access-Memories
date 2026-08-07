# The B2C hunt — what loosening the parameters actually produced

Run 7 Aug 2026 after the founder loosened four constraints: B2C allowed, marketplaces
allowed, price band open, graveyard revisitable. Four hunt lenses (Fable) each verified
by a demand-check pass (Sonnet), then judged (Opus).

Seven candidates. **The honest headline: every one landed in the same price regime, and
the two strongest died on verified cheaper incumbents.**

## The pricing finding that shaped everything

CAC does not shrink when price does — a click costs the same at $29 as at $297. With no
repeat purchase to recover acquisition from, CAC must stay under ~30% of price. At a
US$1,50 consumer CPC:

| Price | Conversion needed | Paid ads viable? |
|---|---|---|
| $29 | ~17% | No |
| $49 | ~10% | Barely |
| $97 | ~5,2% | Borderline |
| $197 | ~2,5% | Yes |
| $297 | ~1,7% | Comfortably |

Cold high-intent landing pages convert at 1–5%. **So paid traffic only works from ~$97 up.**

That gives two coherent consumer models which do not mix:
- **Model A** — cheap + marketplace, $19–49, 160–400 sales/month, zero ad spend, wholly
  dependent on ranking in someone else's search.
- **Model B** — premium + paid search, $197–297, 26–40 sales/month, CAC $60–90, testable
  in a week with a $200–500 budget.

**All seven candidates were Model A** ($29–59). None could use the founder's ad budget.

A third consideration nobody had raised: **support load scales with unit count, not
revenue.** 26 sales and 269 sales earn the same money; one generates ten times the refund
requests and "it won't open" emails, absorbed by one person.

## The candidates

| Candidate | Price | Sales/mo needed | Outcome |
|---|---|---|---|
| **AGENCY ATLAS** (merged with SIGNED KIT) | $39 | 200 | **Judge's pick** — fast cheap test, not a path to target |
| ESTATE RUNBOOK | $59 | 132 | **Killed on substitutes** — see below |
| FLOW DECK | $49 | 159 | **Killed** — verified $49 incumbent with ratings |
| PRODUCTION BOOK | $34 | 229 | Not picked |
| SAFE START | $29 | 269 | Not picked |
| PRODUÇÃO KIT | $29 | 269 | Demand unconfirmed |

## AGENCY ATLAS — the pick, with a heavy discount

A dated, source-linked database of model/talent agencies: how each accepts submissions,
required digitals and measurements, board and size policy, whether they take foreigners,
and whether their talent-agency licence is publicly verifiable. Regional editions plus a
Portuguese Brazil edition.

**The founder's modelling background is genuinely load-bearing here** — the only candidate
where that is true — and it works facelessly, because credibility comes from dated
source-linked rows rather than from her name.

**The load-bearing negative finding.** Every comparable that could be inspected carries
`ratings: {count: 0}`:

- `modelindex.gumroad.com/l/GlobalFashionAgencyList` — **US$5**, zero ratings
- `modelindex.gumroad.com/l/ModelLaunchKit` — **US$20**, zero ratings
- `actory.gumroad.com/l/LAagentdirectory` — **US$20**, zero ratings

Gumroad search for "modeling agency list" returns **9 results total**, none of them the
incumbent. And the US$29,95 paid incumbent since 1956, Peter Glenn (`pgdirect.com`), is
now a **114-byte parked page**.

**Search intent is verified. Purchase is verified nowhere.** Etsy — the one source that
would settle it — returned HTTP 403 behind DataDome on every route across three separate
verification passes.

Against ADV-Check: fixes **B4** (time to first revenue) decisively; does **not** fix B1
(need still unmeasured), does **not** fix B2 (a model applies once), and is **worse on B3**
(three comparables at $5–20 sit under the price). Honest projection: **US$300–1.500/month**
from a first edition.

## ESTATE RUNBOOK — killed on the substitute check

It had the best demand *mechanics* of anything found: involuntary, deadline-boxed, acutely
anxious, with a buyer searching "executor of estate checklist pdf" at 11pm. Founder edge was
irrelevant here and correctly dismissed. It died on economics instead.

**Nolo does the whole job, state-specific, at book price** [VERIFIED by fetch]:

| Nolo product | Price |
|---|---|
| The Executor's Guide — settling an estate or trust | **$25,49–$39,99** |
| How to Probate an Estate in California | **$13,99–$42,99** |

Fifty-year-old trusted brand, in a category where a grieving buyer's trust *is* the purchase.

**And the A$459 premium anchor evaporates on inspection** [VERIFIED, simplyEstate's own
page]. Their stated component values:

| Component | Value |
|---|---|
| Handbook | A$29 |
| Six checklists, inventories and trackers | A$19 each |
| **Three hours of personal guidance and support** | **A$390** |

**85% of the anchor is human time** — precisely what this founder cannot deliver (no
unscripted English calls, no per-transaction human step). Digital-only, the comparable is
A$199 (~US$130) as a bundle, A$19–29 per piece.

Both claimed differentiators are already served cheaper: the reconciling-tracker gap is
filled at **US$19 on Etsy by a former probate lawyer with Star Seller status** — real
credentials in a domain where credentials convert — and Nolo's books ship downloadable
forms. Five of ten autocompletes for "estate executor spreadsheet" contain *free*.

## The pattern — the most useful output of this round

Both strongest consumer candidates died identically. FLOW DECK hit a verified $49 incumbent
with 5-star ratings and a professional review (`jenrozenbaum.gumroad.com/l/boudoirposing`)
already teaching the same flow-based method. ESTATE RUNBOOK hit Nolo plus a credentialed
Star Seller.

> **Consumer digital categories with genuinely provable demand are already served — at book
> prices, by trusted names.** Where consumer demand is real and visible, someone arrived
> first, and they are cheaper and more credible than an anonymous new shop.

This is the consumer form of the filter that killed the Brazilian B2B candidates. It is also
why the surviving candidates live in obscure B2B corners: not because obscurity is desirable,
but because it is where the trusted incumbent has not arrived.

## The one test worth running, and it is free

Four automated verification passes were defeated by DataDome. A human is not.

**Open Etsy in a browser from São Paulo. Thirty minutes, US$0.** Search `modeling agency
list`, `model agency submission`, `modeling digitals`. For the top 20 listings record: price,
**review count**, and whether it is an *information* product or a *design template*.

That single act resolves the only unknown that matters — whether anyone has ever paid for a
compiled agency directory.
