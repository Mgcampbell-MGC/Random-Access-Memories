# 50-State Solicitation Status Monitor

Winner of a 13-agent hunt (7 Aug 2026) targeting recurring revenue, a measured need, and a
large enumerable list. Four candidates reached STRONG; this one won on all three axes.

## The business

American charities that solicit donations in more than one state must register with each
state's charity regulator and renew annually. Nobody watches those registrations for them,
so charities silently fall out of good standing while their donation page keeps taking
money from those states.

Sol sells a one-time evidence report showing where a charity stands in every state that
requires registration, then a monthly subscription that re-checks each register and warns
them before the next deadline.

**US$395 initial audit → US$119/month monitoring.**

## The measured need — independently re-verified twice

The California AG's `charities-may-not-operate.csv` was downloaded and counted by the
measurement pass, by the judge, and again independently. All three agree exactly:

| Registry Status | Count |
|---|---|
| Mutual Benefit *(a classification, not a sanction — excluded)* | 65.894 |
| **Revoked** | **32.609** |
| **Delinquent** | **13.080** |
| **Suspended** | **3.510** |
| Not Registered – Cease and Desist Order | 831 |
| Delinquent – Late Fees Due | 89 |
| **Delinquent + Suspended** | **16.679** |

HTTP 200, 33.885.257 bytes, 116.045 rows. 70.363 rows carry an empty FEIN.

- **16.679** organizations sit in a status the AG itself files under *"May Not Operate or
  Solicit for Charitable Purposes"* — roughly **16%** of the registered population.
- **7.835** of those delinquencies were set during 2026 alone. The pool refills continuously.
- The **831 Cease-and-Desist** rows are the most acute sub-segment and were not named in the
  original candidate — worth targeting first.

**The two-source contradiction:** Colorado publishes every registered charity's own signed
declaration of which other states it solicits in. Of 6.900 organizations whose 2024+ Colorado
filing declares California solicitation, **107 (1,6%)** simultaneously appear on California's
may-not-operate list.

**The artifact that was correctly stripped:** Colorado's dataset is cumulative, averaging 8,6
historical filings per organization. A naive join returns **874**. Restricting to organizations
still filing in 2024+ gives **107**. Anyone rebuilding this must get 107 (±5), not 874 —
otherwise the emails name charities that stopped soliciting years ago.

## The defect, as the email states it

> "Your organization's most recent Colorado charitable-solicitation filing declares that you
> solicit contributions in California. The California Attorney General's downloadable registry
> of 17 July 2026 lists FEIN 52-1294680, AMERICAN CONSERVATIVE UNION FOUNDATION, registry
> number CT0157413, with Registry Status **Delinquent**. The Attorney General publishes that
> file under the heading 'May Not Operate or Solicit for Charitable Purposes.' Both links below
> are your own filing and the regulator's own list."

Verified named examples, all present in the file as-of 2026/08/05:

| Organization | FEIN | Status | Set |
|---|---|---|---|
| American Conservative Union Foundation | 52-1294680 | Delinquent | 2026/07/17 |
| Children Awaiting Parents Inc. | 16-1047933 | Delinquent | 2026/07/17 |
| WonderWork Inc. | 27-4159217 | Revoked | 2024/10/16 |
| Consumer Credit Counseling Service of Greater Atlanta | 58-0942924 | Revoked | 2025/01/09 |

The recipient needs no expertise and no trust in the sender. They search their own FEIN in a
state file and see it.

## Why it recurs — structural, not argued

Registration is a **calendar, not a repair.** ~41 states require it, each with its own annual
renewal clock tied to the charity's fiscal year end. A charity that cures California today
owes ~41 more filings within twelve months. California republishes the list twice a month.

**The retention lock:** state files publish *current status only* — there is no public history.
A month of snapshots Sol didn't take cannot be reconstructed later. Her fortnightly snapshot
archive is both the moat and the reason cancelling leaves a permanent hole in the customer's
compliance record.

## The regulator's own language does the persuading

> *"While an applicable charity is so classified, it is not permitted to operate or fundraise."*
> *"Each call, mailing or request constitutes a separate violation regardless of whether it
> results in a donation."*

The authority is the Attorney General's sentence, not Sol's opinion — which is what makes this
work for a seller with no credential.

## Competitors — checked, and they validate rather than undercut

| Competitor | Shape | Price |
|---|---|---|
| Harbor Compliance / Labyrinth | Managed filing across ~40 states | Quote-only, plausibly US$2.000–6.000/yr |
| Charity Compliance Solutions | Managed filing, California focus | **Quote-only, no published price** |

Both are *filing* services sold by phone — they do the work. Neither publishes a
monitoring-only subscription. At 10–20× the price for more service, they establish the budget
line. No cheap monitoring product was found by either verification pass.

**Each state's own lookup is free but one organization at a time**, and California publishes the
very CSVs used here. No regulator or industry body publishes a multi-state aggregation or change
alerts. California mails delinquency notices directly to charities — and 13.080 sit delinquent
anyway, which is the measured proof that notices fail.

## The money

- 60 retained subscribers × US$119 = **US$7.140/month**, plus 2–3 audits at US$395 =
  **US$7.900–8.300/month**. Target met.
- At US$149/month it needs 50–55 subscribers.
- **Honest ramp: 9–15 months to 60 subscribers, not three.** Months 1–2 are audit revenue only.
- **Capital at risk before the first sale: under US$100.** Every source is a free government
  download; costs are a domain, a mailbox, and some verification credits.
- Paid ads are unnecessary, not merely unaffordable — the regulator publishes the prospect list
  with the defect already computed.

## The first test

**200 emails. Under US$100. Three weeks.**

The 107 two-source contradictions first, then the highest-quality single-source delinquents —
those with a website, a named ED, and a status set in 2026. Each email carries the two quoted
values and both links.

**Stop threshold: fewer than 2 paid audits from 200 emails.** Two is 1%, and 1% is the floor at
which a 16.679-name list carries the business.

Secondary reading, not a gate: under 4% reply rate means the copy is wrong before the offer is
wrong — rewrite once and resend to a fresh 200 before concluding anything.

## Against ADV-Check

| | ADV-Check | This |
|---|---|---|
| **Need measured?** | No | **Yes — 16.679 live, full population, verified three times** |
| **Repeat purchase** | Annual | **Monthly, against ~41 staggered deadlines** |
| **Price pressure** | US$650 one-off, hard to hold | **US$395 entry, and the report is the funnel not the business** |
| **Time to first dollar** | Unknown; ads unavailable at US$10–30/click | **List arrives pre-qualified with phone and website** |
| **List** | 16.779 advisers | **105.022 emailable, 16.679 with a live defect** |

## Settle before building

1. **The payment rail.** Stripe Brazil settles in BRL, which breaks USD-to-Wise. Note from
   earlier research: **Paddle is likely out** — its terms prohibit "human services that are not
   related to a software offering (e.g., pure consulting or advisory services)," and a
   monitoring-report subscription may fall on the wrong side of that line. Confirm a recurring
   USD rail before writing code.
2. **Reproduce the join and get 107, not 874.** If it returns 874, the cumulative-history bug is
   present and the emails will name charities that stopped soliciting years ago.

## One transferable lesson from the round

The Opposition-Window Trademark Watch candidate died because **the USPTO's own guidance
describes unsolicited email quoting a recipient's serial number as a recognised scam pattern** —
which neutralises the entire zero-credibility advantage of the evidence mechanism in that
vertical.

**Check for a regulator warning page before building any evidence-email business.** That check
was run for this candidate: no equivalent warning was found for charity registration outreach,
and the AG's own published language supports the claim rather than undermining it.
