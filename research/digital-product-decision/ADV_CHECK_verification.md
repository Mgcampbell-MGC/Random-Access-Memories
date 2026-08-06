# ADV-Check — independent verification, and one correction that changes the plan

The re-scan returned **displace**: ADV-Check beats DeckProof on list size and corpus depth.
I verified the load-bearing claims myself rather than accepting them.

## What holds up

**The roster is real, free, and enumerable.** Route: `catalog.data.gov` → SEC FOIA
distribution. The direct `reports.adviserinfo.sec.gov` path returns 403; the working path is
`sec.gov/files/investment/data/other/information-about-registered-investment-advisers-exempt-reporting-advisers/ia<MMDDYY>.zip`.

Downloaded and parsed the **1 May 2026** file myself (Jun/Jul/Aug returned 404 or a partial):

| Claim (agent, Aug file) | My count (May file) | Verdict |
|---|---|---|
| 17.018 registered advisers | **16.779**, all `Firm Type = Registered` | **Confirmed in substance** — delta consistent with 3 months' growth |
| 15.653 carry a website | **15.445** in `Website Address` | **Confirmed** |
| 14.761 US-based | **14.557** United States (+271 UK, +150 Canada) | **Confirmed** |

448 columns. The list is genuinely free, genuinely enumerable, and carries the domain — which
is what makes outbound possible at all.

## The correction: seasonality is far more extreme than stated

The verdict said *"Feb–Jul each carry 1.256–2.082 firms, so ~6 solid months plus a March
mega-season."* That is wrong. Counting `Latest ADV Filing Date` in the May 2026 file:

| Month | Firms | | Month | Firms |
|---|---|---|---|---|
| Jan | 670 | | Jul | 33 |
| **Feb** | **1.728** | | Aug | 23 |
| **Mar** | **11.358** | | Sep | 90 |
| **Apr** | **2.496** | | Oct | 39 |
| May | 25 | | Nov | 48 |
| Jun | 134 | | Dec | 135 |

**68% of the entire industry files in March. Feb–Apr is 93%.** The remaining nine months
carry ~1.200 firms between them.

This is not a rolling stream like ECRM's 93 dated sessions. It is **one industry-wide annual
deadline** — Rule 204-1's annual amendment, due 90 days after fiscal year end, and almost
every adviser runs a 31 December year end.

**And the next season is Jan–Mar 2027 — five to seven months from today (6 Aug 2026).**
DeckProof has live rosters with an eleven-week window *right now*.

### What this does to the verdict's arithmetic

The verdict's decisive figure was *"600–1.000 sends/month at 1,5–3% = 9–30 sales/month."*
That assumes a live trigger year-round. There isn't one.

Sending 600–1.000/month across a Nov–Mar run-up is 3.000–5.000 contacts → 45–150 sales at
US$650 → US$29k–97k **concentrated in one quarter**, i.e. US$2.400–8.100/month averaged over
a year. The midpoint sits **below** the US$7.400–8.300 target.

So the 7x list advantage is **partly illusory**: the list is 7x bigger but the window is ~4x
narrower, and the cash arrives in one lump. For a founder with no capital, lumpy matters.

## Why this reframes rather than kills it

The trigger was mis-identified. It is **not the filing deadline** — it is **the discoverable
defect**, and that is available all year.

Sol can compute the mismatch herself, from free public data, *before* she writes:

> "Item 5.F of your Form ADV says US$412M. Item 4 of your own brochure says US$353M."

Two quoted passages that disagree. Verifiable by the recipient in seconds, needing no trust in
the sender and no credential from her. That is a **stronger** hook than a date, and it defines
a trigger class the framework did not have: not *visible-dated*, not
*invisible-high-frequency*, but **visible-defect** — always-on, company-specific, self-proving.

**The cost of that reframe, stated honestly:** bulk Part 2A brochures stop at December 2024
(verified — the page directs post-2025 data to IAPD only), so computing each mismatch means
pulling that firm's brochure by hand. Volume is then capped by **Sol's time per prospect**,
not by her sending domain. That is a different constraint from every candidate assessed so far
and it has not been measured.

## The two kills that validate the corrected filter

- **CitationProof** was the strongest challenger on trigger quality — 30.273 named, dated OSHA
  inspections, US public domain, no anti-scraping terms. It died because its paid core is
  **already free**: three working no-account penalty calculators built on the same Field
  Operations Manual schedule, one of them run by a US$447 near-rival as a lead magnet. A
  genuine Bucket A / T6 kill.
- **NoticeBench 65** had the biggest anchor and list in the set (~6.420 Prop 65 notices/year,
  a real forward penalty). It died on **the self-verification trap** — its two most valuable
  layers promise *"this label is legally correct"* and *"your case is worth US$X"*, neither
  checkable by inspection, both pure borrowed authority, sold by a faceless foreign vendor into
  an active lawsuit.

That second kill is the R4 correction from earlier today working exactly as intended: it did
not ask whether Sol holds a credential, it asked whether the buyer could verify the output.

## The recommendation

**Run ADV-Check's hand-check first**, because it is the cheapest real evidence available in
this entire project and it requires nobody's cooperation:

Take 40 US firms with Feb–Apr filing dates from the roster already downloaded, pull each
brochure free from IAPD, and diff Part 1 against Part 2A by hand.

**Cost: US$0 for step one.** No domain, no mailbox, no buyer contact.

**Pass: ≥30% of the 40 carry a real, quotable discrepancy.** Above that, ADV-Check has
ammunition for every cold email it will ever send, and the seasonality problem is survivable
because the hook works year-round. Below it, ADV-Check has nothing to put in the email and
**DeckProof wins by default** on its verified live rosters.

This ordering matters because DeckProof's own US$0 gate was proved unrunnable — the public
sell-sheet corpus does not exist. ADV-Check's gate *is* runnable, today, for nothing.
