# Import Chain Integrity

Winner of a hunt (7 Aug 2026) built entirely around **Gate 0** — prove the buyer can pay before
designing anything — after the previous winner died on a population that was 70% under
US$50.000 revenue.

## The business

A US company importing medical devices must list, in its own FDA registration, the foreign
factories it imports from. Each year a slice of those factories quietly fail to renew their FDA
registration, and **FDA deletes them from the public file without telling the importer.** The
importer's own federal filing now points at establishments FDA no longer lists.

US$350 pre-computed PDF audit → US$199/month monitoring against the weekly files.

## Gate 0 — a fee, not an inference

**Every prospect paid US$11.423 to FDA between 1 October and 31 December 2025, or it is not in
the file at all.**

- FY2026 annual establishment registration fee: **US$11.423** [VERIFIED — Federal Register doc
  2025-14412, 30 Jul 2025, and FDA's MDUFA fees page]
- **There is no small-business reduction for this fee.** A hardship waiver exists via Small
  Business Determination, but only for renewals and only on demonstrated hardship — exceptional,
  not routine. [VERIFIED]
- Initial importers are explicitly inside the paying set: FDA's *"Who Must Register, List and Pay
  the Fee"* lists Initial Importer as Register = YES 807.40(a), Pay Fee = YES. This was
  re-checked specifically, because the entire case collapses if importers were exempt.

Population: **28.535** currently-registered establishments; **5.741** carry
`INITIAL_IMPORTER_FLAG = 'Y'`; **5.920** US-addressed registrants declare at least one foreign
manufacturer. Of those, **1.147 declare 5+** foreign manufacturers and **543 declare 10+** —
declared-manufacturer count being a direct proxy for import volume.

Compare the population this replaced: 70% of delinquent charities were under US$50.000 revenue.
Here, a company that cannot find US$11.423 is *out of the file*.

## The measured need — full population, reproduced three times

| | |
|---|---|
| Registration rows / unique establishments | 43.990 / **28.535** |
| Declaration rows / distinct declaring importers | 150.426 / 6.011 |
| **US importers registered, with declarations** | **5.920** |
| Total dangling declared-manufacturer links | **6.325** (3.478 distinct absent keys) |
| **Importers with ≥1 dangling — RAW** | **1.846 = 31,18%** |
| **Importers with ≥2 dangling — CLEAN** | **891 = 15,05%** |
| Ideal customer profile (5+ declared, 2+ dangling) | **717** |
| Mid-size ICP (5–25 declared, 3+ dangling) | **381** |
| Premium tier (dangling under a cleared K/P number) | **282** |

Reproduced independently three times across two different weekly snapshots, matching to the digit.

**Raw versus clean, honestly.** A dangling link has three possible causes: the factory genuinely
failed renewal; it re-registered under a new internal key leaving a stale reference; or the
importer never removed a supplier it stopped using. 31,18% covers all three; 15,05% is the
conservative floor. Separating them requires two snapshots — which is why the archive is build
step one. **The pitch does not depend on which cause it is:** in all three the importer's own
federal filing is wrong.

## The upgrade found during verification

The declaration table joins to the device-listing table. Of 24.767 dangling declaration rows
belonging to US importers, **2.675 carry a premarket submission number** — so for **282
importers** the finding can name the *cleared device* whose declared factory has vanished.
**1.481 distinct K/P numbers implicated.**

A K-number is the most self-evident object in this vertical: the recipient looks it up in FDA's
free 510(k) database and sees their own clearance.

## The defect, as the email states it

> Randox Laboratories-US, Ltd — FDA establishment registration **2086993**.
> Your FURLS registration declares **5** foreign manufacturing establishments. **3 of the 5** do
> not appear in FDA's current establishment registration file. Those 3 are attached to **92 of
> your device listings**, including **K000375**, **K000468**, **K000469** and **K000661**.
> To check: open your FURLS account, take those three factory names off your own declared list,
> and search each in FDA's free Establishment Registration database.

Never *"you are non-compliant."* Only counts and identifiers the recipient verifies themselves.

## Why it recurs

1. **Weekly** — FDA republishes the whole extract every week.
2. **Annually, in a wave** — renewal runs 1 Oct – 31 Dec, so every January a fresh cohort drops
   out. A dated, forward, calendar-driven reason to buy, pre-announceable in September.
3. **Never completes** — supply-chain integrity has no "done" state.

## The moat: FDA erases, it does not archive

Of the 3.478 distinct absent establishment keys, **0 appear anywhere in `registration_listing.txt`**
and exactly 1 survives in `Official_Correspondent.txt`. Every `reg_expiry_date_year` in the file
is 2026; no prior year exists.

**Nobody can reconstruct who the lapsed factory was, or when it vanished, without a private
archive of weekly snapshots.** That archive starts accruing on day one and cannot be built
retroactively — which is why the cron is build step one, before the product.

## Contact coverage: 100%, from the government file

`Official_Correspondent.txt` gives a named person plus phone for **5.920 of 5.920** US importers
with declarations. FDA publishes the name of the exact human responsible for the filing that is
wrong. Names go to Apollo for email enrichment; sending is CAN-SPAM cold email, US-only.

**S10 checked and cleared:** FDA's warnings in this space target vendors selling fake "FDA
registration certificates" for a fee. Sol sells no certificate and points recipients at their own
FURLS account. Hard rule for the template: never any certificate-like graphic or FDA logo.

## The money

| Mix | Monthly |
|---|---|
| 40 retained at US$199 | US$7.960 |
| 30 retained at US$199 + 6 audits at US$350 | US$8.070 |
| 25 retained at US$249 + 5 audits at US$350 | US$7.975 |

40 subscribers is **5,6% of the 717 ICP** — a higher rate than a mass list needs, and the honest
cost of a small population. What buys it back: every email quotes the recipient's own
registration number and their own two counts.

**Capital at risk before the first sale: under US$150.** All source data is a free government
download. Archive storage ~1,1 GB/year.

**Ramp:** weeks 1–2 archive cron and join engine; weeks 3–4 the 60-email test; month 2 first
audits; months 3–4 eight to fifteen retained; months 6–9 thirty to forty-five retained and the
target range, assuming 4–6% ICP penetration and audit→monitoring conversion above 50%.

## The first test — under US$100, 14 days, corpus already in hand

60 mid-size ICP importers (5–40 declared, 3+ dangling, giants excluded), prioritising the
K-number tier. Each email quotes their registration number, both counts, affected K-numbers, and
the verification path.

| Outcome in 14 days | Decision |
|---|---|
| ≥1 paid audit, **or** ≥5 replies of which ≥3 ask price | **BUILD** |
| 2–4 replies, none commercial | **ITERATE ONCE** with K-number framing forward |
| ≤1 reply, or ≥2 saying *"that supplier re-registered, non-issue"* | **STOP** |

That third row is the real kill condition and it is cheap to reach.

## Independent verification of the mechanism

Reproduced directly against the openFDA API (free, no key, HTTP 200, 330.251 records, last
updated 2026-07-27):

| Field | Confirmed |
|---|---|
| `registration.initial_importer_flag` | Present |
| `registration.fei_number` | Present — the continuity resolver for separating true lapses from re-registrations |
| `registration.reg_expiry_date_year` | **2026 only**, consistent with the erasure moat |

**Not independently reproduced:** the specific join counts (31,18% / 15,05%). Bare
`accessdata.fda.gov` fails with `SSL_ERROR_SYSCALL` from this environment, so the raw
pipe-delimited files could not be pulled here. That is an infrastructure limit, not evidence
against the numbers — three agents reproduced them on two different snapshots. **It should be
re-run from an unblocked network before the build.**

## Three things to settle before building past the archive cron

1. **Does a dangling link land as material, or get shrugged off as a re-registration?** The real
   weakest link. Settled by the US$100 test, whose reply *content* is the measurement.
2. **Is fdadevicecheck.com's US$19/month watchlist a price ceiling or a different product?** It
   does status lookups on facilities the user already knows about and cannot read the importer's
   own declaration. But a US$19 anchor in the same inbox is a hazard. Cost to settle: zero —
   request the pilot invitation.
3. **Does Apollo return work emails for FDA official correspondents?** 5.920 named people with
   phones and no emails. Run 50 through Apollo before writing any PDF code; under 40% match and
   the channel needs rethinking.

## Why it beats ADV-Check

| | ADV-Check | This |
|---|---|---|
| Solvency | Asserted, no distribution | **US$11.423 fee-gated, verified** |
| Measured need | **Unmeasured** | **31,18% raw / 15,05% clean, full population, 3× reproduced** |
| Recurrence | Annual | **Weekly files, monthly subscription, January renewal wave** |
| Contact | Enrichment guesswork | **FDA names the responsible person — 5.920 of 5.920** |
| Defensibility | Two public documents | **FDA erases lapsed records; only a private archive can name or date a lapse** |
