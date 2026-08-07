## RECOMMENDATION: 50-STATE SOLICITATION STATUS MONITOR (US NONPROFITS)

It beats ADV-Check. It wins on all three of the required dimensions — recurring revenue, a measured need, and a verified list six times larger — and it is the only STRONG-verdict candidate in this set whose list is bigger than ADV-Check's.

**What I re-checked myself (the two facts the whole case rests on):**
1. I re-downloaded `https://oag.ca.gov/sites/all/files/agweb/pdfs/charities/reports/charities-may-not-operate.csv` — HTTP 200, 33,885,257 bytes, 116,045 rows. Registry Status counts recomputed: Delinquent 13,080, Delinquent–Late Fees Due 89, Suspended 3,510 (**16,679 combined**), Revoked 32,609. 7,835 of the delinquent statuses were set in calendar 2026. Every figure is an exact match to the measurement pass. [VERIFIED]
2. I fetched `https://oag.ca.gov/charities/reports`. The Attorney General's own page titles that file **"May Not Operate or Solicit for Charitable Purposes"** and names Delinquent, Delinquent–Late Fees Due, Suspended and Cease-and-Desist among its statuses, and states the files are "updated on the first and third Wednesday of each month." [VERIFIED] This matters because it is the source of authority in the cold email — the prohibition is the regulator's sentence, not Sol's.

---

### 1. THE BUSINESS

American charities that ask for money in more than one state must register with each state's charity regulator and renew every year. Nobody watches all those registrations for them, so charities silently fall out of good standing while their donation page keeps taking money from those states. Sol sells a one-time evidence report showing where a charity stands in every state that requires registration, then a monthly subscription that re-checks every register and warns them before the next deadline.

### 2. THE DEFECT — exactly as the cold email states it

> "Your organization's most recent Colorado charitable-solicitation filing declares that you solicit contributions in California. The California Attorney General's downloadable registry of **17 July 2026** lists FEIN 52-1294680, AMERICAN CONSERVATIVE UNION FOUNDATION, registry number CT0157413, with Registry Status **Delinquent**. The Attorney General publishes that file under the heading 'May Not Operate or Solicit for Charitable Purposes'. Both links below are your own filing and the regulator's own list."

Two real values, from two real filings, both re-verified by me today in the live file:

| Organization | FEIN | CA status | Date status set |
|---|---|---|---|
| AMERICAN CONSERVATIVE UNION FOUNDATION | 52-1294680 | Delinquent | 2026/07/17 |
| CHILDREN AWAITING PARENTS INC. | 16-1047933 | Delinquent | 2026/07/17 |
| WONDERWORK INC. (dba Surgery For The Poor) | 27-4159217 | Revoked | 2024/10/16 |
| CONSUMER CREDIT COUNSELING SERVICE OF GREATER ATLANTA INC. | 58-0942924 | Revoked | 2025/01/09 |

All four sit in the file I downloaded, as-of date 2026/08/05. [VERIFIED by me] The Colorado side of the pair — each organization's own most recent Colorado filing declaring California solicitation — was fetched and joined by the measurement pass, which reproduced the join independently and got 107 live contradictions against the candidate's claimed 109. [VERIFIED by the measurement pass, not re-fetched by me]

The recipient needs no expertise and no trust in Sol. They Ctrl-F their own FEIN in a state file and see it.

### 3. WHY IT RECURS

This is the strongest recurrence in the set, and it is structural rather than argued.

Registration is not a repair, it is a **calendar**. Roughly 41 states require registration, each with its own annual renewal clock tied to the charity's fiscal year end (California's RRF-1 is due 4.5 months after year end; New York, Florida, Pennsylvania and the rest run on their own dates). A charity that cures its California status today owes about 41 more filings inside the next twelve months. Miss any one and a status flips. California republishes the list twice a month, and 7,835 of the delinquencies currently on it were set during 2026 alone — the pool refills continuously. [VERIFIED by me]

There is also a second, harder retention lock: the state files publish **current status only**. There is no public history. A month of snapshots Sol did not take cannot be reconstructed later. Her archive of fortnightly snapshots is therefore both the technical moat and the reason cancelling leaves a permanent hole in the customer's record.

### 4. THE MEASURED NEED

- **16,679** organizations currently carry Delinquent or Suspended status in California — a status the AG itself files under "May Not Operate or Solicit". A further **32,609** are Revoked. Full population, 116,045 rows, not a sample. [VERIFIED by me]
- Against roughly **103,567** organizations holding a California registration number on the "may operate" side, that is about **16%** of the registered population in a status that bars solicitation right now. [VERIFIED by me for the numerator; the denominator is from the measurement pass's count of distinct registration numbers in the current may-operate file]
- **Two-source rate:** of 6,900 organizations whose most recent Colorado filing (2024 or later) declares California solicitation, **107 (1.6%)** are simultaneously on California's may-not-operate list. The measurement pass reproduced this from a clean re-fetch and explicitly stripped the trap that inflates it — Colorado's dataset is cumulative, averaging 8.6 historical filings per organization, so a naive join gives 874 and is wrong. Raw-versus-clean: 802 if you include long-dormant registrants back to 2002, **107** if you restrict to organizations still filing in Colorado in 2024+. Use 107. [VERIFIED by measurement pass]
- **773** more declare California solicitation in their current Colorado filing but appear in neither California list at all — a probable non-registration, but this claim needs name-matching because 70,363 of the 116,045 California rows have an empty FEIN field. Not for the first emails. [VERIFIED caveat]

### 5. THE BUYER AND THE LIST

The buyer is the Executive Director or finance/operations director at a US 501(c)(3) that solicits in several states, roughly US$500k–20M revenue. This segment already pays for software on an org card — Bloomerang, Little Green Light, DonorBox — so a US$119/month line item needs no purchase order and no committee.

The list arrives pre-built and pre-qualified:
- **105,022–103,567** California-registered organizations (national charities included) as the outer emailable universe.
- **16,679** with a live bad status — every one a one-click-verifiable defect.
- **6,900** Colorado filers declaring California solicitation, of whom **107** carry the two-source contradiction that makes the strongest possible first email.
- Contact data: the Colorado registration file carries phone and website per organization; California's file carries name, city, FEIN and registry number. Emails come from the organizations' own websites — nonprofits publish staff addresses far more readily than companies do.

Reach is 100% cold email into the USA, which is CAN-SPAM lawful with a working opt-out. No calls, no face, no audience, no Germany.

### 6. THE MONEY

**US$395** initial "where you stand in all 41 states" evidence report, then **US$119/month** (or US$329/quarter) monitoring: fortnightly re-check of every register the organization appears in, an alert on any status change, and a rolling 90-day deadline calendar.

- 60 retained subscribers × $119 = **$7,140/month**, plus 2–3 audits/month at $395 = **$7,900–8,300/month**. Target met.
- At $149/month it needs 50–55 subscribers. Test both prices.

**Honest ramp.** Months 1–2 are audit revenue only: 300 evidence emails might produce 3–6 audits, which is $1,185–2,370 and no subscribers yet. Subscriptions build from audit buyers converting (assume 40% until measured) plus direct subscription sales. Reaching 60 retained subscribers realistically takes 9–15 months, not three.

**Capital at risk before the first sale: under US$100.** Every data source is a free government download. Costs are a domain (~$12), a sending mailbox (~$7/month), and perhaps $50 of email verification credits. The build is Claude Code time, not money.

**Paid acquisition is not part of the plan.** Nonprofit-compliance keywords are cheap by finance standards — plausibly US$3–8 per click [UNKNOWN, not measured] — but there is no reason to buy clicks when the regulator publishes the prospect list with the defect already computed.

**The weakest link, stated plainly.** The organizations with the loudest defect skew small, distracted or dying, and the well-funded multi-state charities may already pay Harbor Compliance / Labyrinth, whose managed filing service is quote-only at a plausible US$2,000–6,000/year [PLAUSIBLE, no public price; the measurement pass fetched the page and confirmed pricing is contact-only]. That is 10–20× her price for more work, so it validates the budget line rather than undercutting it — but it means her buyer is the charity that wants to *know*, not the one that wants filing done. No cheap monitoring-only product was found by either pass.

### 7. THE BUILD

Four weeks, in this order:

1. **Ingest and normalize.** California's two CSVs (re-pulled the 1st and 3rd Wednesday) and Colorado's two Socrata datasets. Normalize FEINs, deduplicate Colorado to each entity's latest filing — this step is where the naive version goes wrong, and it must be built the way the measurement pass verified.
2. **Prospect table.** The 107 two-source contradictions, the 16,679 single-source bad statuses, names, FEINs, statuses, dates, source links, phone, website.
3. **Report generator.** One HTML template rendered to PDF per organization, containing the two quoted values, the dates, and both regulator links. No app, nothing to install.
4. **Outreach pipeline.** Website crawl for role addresses, CAN-SPAM footer, send from a warmed domain, log replies.
5. **Then, and only after money arrives:** add states one at a time (New York, Florida, Pennsylvania, Michigan, Washington), plus the deadline calendar built from each state's statutory rule and the charity's fiscal year end.
6. **The snapshot archive.** Store every register pull, forever, and diff each pull against the last. That diff is the monthly product and the thing no prompt can reproduce.

Claude Code writes all of it: the fetchers, the FEIN normalizer, the join, the PDF template, the diff engine, the send loop. Her job after week four is marketing.

### 8. THE FIRST TEST

**One measurement: does an evidence email sell a US$395 audit?**

Send **200 emails** — the 107 two-source contradictions first, then the highest-quality single-source delinquents (organizations with a website, a named ED, and a status set in 2026). Each email carries the two quoted values and both links. Nothing is built beyond the report generator for those 200 organizations.

- Cost: under **US$100** (domain, mailbox, verification credits).
- Duration: **three weeks** including follow-ups.
- **Stop threshold: fewer than 2 paid audits from 200 emails.** Two audits is 1%, and 1% is the floor at which a 16,679-name list can carry the business. Below that, stop and do not build the 41-state layer.
- Secondary reading, not a gate: reply rate. Under 4% replies means the email copy is wrong before the offer is wrong — rewrite once and resend to a fresh 200 before concluding anything.

### 9. WHAT MUST BE TRUE

**Settle before building (both are one-day checks):**
- **Card-accepting recurring billing that pays USD into Wise against a CNPJ.** Stripe Brazil settles in BRL, which breaks the payout requirement. Cheapest resolution: open a Paddle and a Gumroad account, confirm which supports monthly subscriptions with USD payout to Wise, and use it. [UNKNOWN]
- **The Colorado join reproduces on her machine.** She must get 107 (±5) and 6,900 (±100), because if she gets 874 she has built the cumulative-history bug and her emails will name organizations that stopped soliciting years ago. [Method VERIFIED; her reproduction is the check]

**Only matters after the first paying customer:**
- Conversion from a $395 audit into $119/month monitoring. Assume 40%, measure it.
- Whether $119 or $149 is the right price. Split the first 40 subscribers.
- Which of the other 40 states are bulk-downloadable versus scrape-only. She needs three states beyond California to sell "multi-state"; she does not need 41 to sell the first subscription.
- Whether the 773 "declares California, appears nowhere" organizations survive name-matching. A second, larger prospect pool if they do; nothing lost if they don't.
- Whether a $119/month subscriber churns after curing California. The snapshot-archive and deadline-calendar framing is designed to prevent that, and it is untested.

Most of the unknowns are in the second group. That is the point: the test costs under US$100 and settles the only question that can kill this — whether a charity pays for its own registry status in writing.

### 10. WHY THIS BEATS ADV-CHECK

| | ADV-Check | Solicitation Status Monitor |
|---|---|---|
| **B1 — need measured?** | No. Nobody knows what share of advisers carry a mismatch. | Yes. 16,679 organizations in a solicitation-barred status right now; 107 two-source contradictions; 7,835 new delinquencies in 2026. Full population, re-verified today. |
| **B2 — repeat purchase** | Annual, at best. Its single biggest weakness. | Monthly subscription against ~41 staggered annual deadlines per customer, a register republished twice a month, and a snapshot history that cannot be rebuilt after a lapse in coverage. |
| **B3 — price pressure** | US$650 for one pre-computed report is hard to hold. | Entry price is US$395 — 40% lower and easier to defend — and the report is a funnel, not the business. The revenue is US$119/month. |
| **B4 — time to first dollar** | Unknown; ads unavailable at US$10–30/click. | Prospect list arrives pre-qualified with the defect already computed, plus phone and website per organization. First email can go out the week the report generator works. Ads are also unnecessary here, not merely unaffordable. |
| **List size** | 16,779 advisers | 105,022 emailable, 16,679 with a live defect |

---

*One fact a future reader needs: the Opposition-Window Trademark Watch candidate is structurally dead, and for a reason that generalises — the USPTO's own published guidance describes unsolicited email quoting a recipient's serial number as a recognised scam pattern, which neutralises the zero-credibility advantage of the whole evidence mechanism in that vertical. Check for a regulator warning page before building any evidence-email business.*