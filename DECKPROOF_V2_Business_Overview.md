# DECKPROOF V2 — Business Overview

**A ground-up rebuild. São Paulo, 10 August 2026.**

---

## 0. The decision, up front

Build **DeckProof**: a downloadable tool that reads a consumer-brand's own pitch deck against its own
cost spreadsheet and reports every place the two contradict each other, immediately before a retail
buyer meeting the brand has already paid **US$7.000–16.900** to attend.

It is the last survivor of thirty-three candidates. It is not the survivor because it is the most
exciting; it is the survivor because it is the only one that passes the three screens that killed
the rest — **no clearing party, not content, and measured solvency.**

**This rebuild makes four structural changes to the August specification.** Each one exists because
something was learned after that specification was written, and each closes a hole rather than
decorating one.

| # | Change | Because |
|---|---|---|
| 1 | **Runs locally. Free. Files never leave the machine.** Payment unlocks the report, not the scan | Solves the trust problem, the confidentiality problem and the "will they send files" problem in one move |
| 2 | **The spreadsheet is the only source of computed truth. The deck is only ever a set of claims to be checked** | Makes a wrong margin *architecturally impossible* — margins never come from pixels |
| 3 | **Drop the margin calculator and the retail-readiness checklist entirely** | RangeMe gives both away free, is owned by ECRM's parent, and is linked from the roster page itself |
| 4 | **Add a recurring second product: Cost Sheet Drift** | A one-shot US$750 sale pays full acquisition cost forever — the shape that defeated eighteen prior candidates |

---

## 1. The problem, stated concretely

A small consumer-packaged-goods brand — 5 to 50 staff, a founder who owns the company card — pays
between **US$7.000 and US$16.900** for a block of pre-scheduled meetings with retail category buyers
at an ECRM session. The meeting is ten or twenty minutes long. The brand walks in with a deck built
in Canva or PowerPoint and a cost spreadsheet built in Excel.

Those two documents are made by different people, at different times, and are never reconciled.

The deck says the retailer takes a 42% margin. The cost sheet, at the stated wholesale price and
suggested retail, implies 36%. Slide 9 says twelve units to a case; row 40 says six. The promo
price on the last slide, run through the actual cost of goods, is under water.

A category manager at Kroger or CVS does this arithmetic in their head while the founder is still
talking. The number does not merely look wrong — it makes the founder look like someone who does not
know their own business, in a ten-minute window that cost them the price of a car.

**Nobody checks this.** Not because it is hard, but because the two documents live in different
files and no software reads both.

---

## 2. The product

### What it does

The brand downloads **one self-contained HTML file** and opens it with a double-click. No install,
no account, no upload. They file-pick their cost spreadsheet and their deck. Everything computes in
the page.

**The spreadsheet is authoritative.** Every margin, every case and pallet figure, every promotional
calculation is computed *from the .xlsx*, which parses reliably and always has. **The deck is never a
source of arithmetic** — it is only a set of claims to be checked against the sheet.

That single architectural rule is what makes the tool safe. Under it:

- A misread deck number produces a **false flag** the user dismisses in ten seconds — and dismissing
  it is exactly the action the product exists to provoke.
- A missed deck number produces **silence** — equivalent to not having the feature. Cost: zero.
- **Reciting a wrong margin to a retail buyer is architecturally impossible, because margins never
  come from pixels.**

### What the buyer receives

1. **The discrepancy report** — every figure appearing in both documents, with the deck's claim, the
   sheet's computed value, the difference, and the slide and cell where each lives.
2. **The corrected one-page buyer economics sheet** — SRP, wholesale, margin, case and pallet
   configuration, formatted the way retailers ask for it. This is the reposition that earns the
   price: **they carry a document into the room, not a critique.**

### What it explicitly does not do

No margin calculator from typed inputs. No retail-readiness checklist. No pitch coaching. No
retailer requirement corpus. **All of that is free from RangeMe or from ECRM's own prep site, to the
same paid attendee** — and selling it would be selling a marketing department's giveaway back to the
person it was given to.

### The free-scan mechanic

The scan is **free and complete**. The tool runs locally and reports *"31 checks run — 5
discrepancies found"*, naming the slides but not the corrected values.

Payment unlocks the detail and the corrected one-pager.

This is the screenshot sale made self-serve. The cold email does not ask for files, does not ask for
a call, and does not ask for trust. It asks for ninety seconds on their own machine, and the product
tells them — before any money moves — whether they have a problem. **Their own numbers do the
selling.**

It also makes the confidentiality objection disappear rather than requiring an answer. The cost sheet
is the most sensitive document a CPG brand owns. *"Open the file, disconnect your wifi, it still
works"* is the strongest trust substitute available to a vendor with no reputation, no face and no
reference customers.

---

## 3. The buyer, and how she finds them

**Who.** Founder or Head of Sales at an indie CPG brand, 5–50 staff. USA primarily, UK and EU
secondarily. This person owns the company card; US$750 against a sunk US$7.000–16.900 is not a
procurement event.

**The trigger.** The brand's name appears on a **public, no-login, dated seller roster** for an ECRM
session it has already paid to attend.

**Verified by direct fetch on 10 August 2026:**

- `ecrm.marketgate.com/sessions` returns HTTP 200, no login, no cookie wall
- **93 sessions** listed, August 2026 – September 2027
- **15 with live seller rosters**; the rest read *"posted in the near future"*
- **456–475 unique named companies**, essentially all carrying a clickable company website
- Per-roster counts: Vitamin/Diet/Sports Nutrition **107**, Candy Planning **61**, LatAm Beauty &
  Personal Care **56**, European Skin/Bath/Hair/Sun Care **45**, Hospital Pharmacy **34**
- Rosters publish **2 weeks to 6 months** ahead

**This is the only candidate in thirty-three where the buyer's ability to pay is observed rather than
estimated.** Every other candidate required an assumption about the buyer's wallet. This one requires
reading a page that names companies who have already wired the money.

**The operational constraint, stated plainly.** Rosters arrive in **monthly lumps, not a daily drip**
— four days elapsed between two measurements with zero new rosters published, and the same fifteen
live. Outbound must be batched against roster-publication events, and there will be dead weeks.
A session two weeks out is already too late to sell a preparation product into.

**Second source, verified live:** the **KeHE Summer Show** public exhibitor directory — no login,
named brands, dated event. Expo West, Fancy Food and PLMA are JavaScript-rendered and yield no names
to a fetch; **Cosmoprof North America is confirmed gated** to registered attendees only.

**Legal line.** ECRM's Terms of Use prohibit scraping and harvesting contact information. **No
automated scraping of ECRM, ever.** Names are read by hand — roughly thirty per roster — the company
domain is taken from the roster's own link, and the person is sourced from the company's website or a
contact database.

---

## 4. Why it survives the screens that killed thirty-three

| Screen | Verdict |
|---|---|
| **Law 0 — who clears the transaction?** Killed the Expediting Desk, and explains Booksy, Momence, Insparisk, RangeMe, Arhaus | **Nobody.** No party earns a margin on whether a brand's own deck matches its own cost sheet. There is no adjacent revenue stream to fund a free version. This is the whole shield, and it is the right one |
| **Law 1 — the lead-magnet mechanism.** Killed six | Not content. A marketing department can give away a template, a guide, a checklist or a corpus. It cannot publish a computation performed on a stranger's confidential cost of goods, because there is nothing to publish |
| **Gate 0 — measured solvency.** Killed the US charities (70% under US$50k revenue) and Dossiê Patrocínio (buyers averaging R$2.815/month) | Solvency is **observed**: the qualifying signal *is* a receipt |
| **Law A — competitor sweep in vendor vocabulary.** Killed nine candidates in one run | Seventeen queries in vendor register plus six direct fetches. Five clusters exist; **none reads two of the buyer's own files and reconciles them** |
| **Law C — hunt the free competitor by funding model.** The screen that failed on the last candidate | Run. RangeMe, ECRM's prep site, and six free calculators found and accounted for. Two deliverables deleted as a result |
| **Law 6 — the human substitute** | No insured human does this arithmetic at or below US$750 |
| **Law 8 — the alert finding** | The buyer profits from knowing. The signal is about their own meeting, not an accusation against them |
| **R4 — can the buyer verify the output?** | They check it against documents they wrote themselves. Nothing rests on the author's standing — which is why her lack of domain expertise is genuinely irrelevant |
| **Reserved profession** | None. Retail arithmetic is not a regulated act |
| **The vise** (5 appearances) | Does not apply. There is no regulated perimeter to be caught between |
| **The precondition trap** | Partially applies and is handled: a brand with no cost spreadsheet is disqualified, not served badly. This is a measured threshold, not an assumption — see §9 |

---

## 5. The competitive map, with prices

Five clusters. **Not one does the whole job.**

**1 — Free forward calculators from typed input.** CPG Guy (fetched: retailer margin targets, cases
per pallet, units per pallet, suggested wholesale), BoxNCase, Margin Velocity, Bravo CPG, Foodbevy,
RGM Academy. They compute one scenario from numbers you type. **They cannot read a document, so they
cannot detect that slide 7 disagrees with row 40.** The gap between "calculates a margin" and "finds
the contradiction between two files you already wrote" is the entire product.

**2 — The free guard inside the channel.** **RangeMe Basic** — free, owned by ECRM's parent, linked
from the roster page — auto-calculates **Case Price** (cost × units per case) and **Buyer Gross
Margin** (from cost and MSRP), with free explainer articles. **And it computes from numbers you type
in, which is precisely the failure mode DeckProof catches.** A brand can hold a perfect RangeMe
profile and a deck with a wrong margin on slide 9, and RangeMe will never know, because RangeMe never
sees the deck. ECRM's own prep site gives away *"a wealth of best practices content… how to prepare
for a buyer meeting, tips on pitching"* — verified, along with the fact that neither reviews pricing,
margins, sell sheets or presentation numbers.

**3 — Deck auditors.** MyDeckAudit, Frontrunner. They ingest a deck — the only category that does —
but audit **investor fundraising narrative**. Wrong buyer, wrong arithmetic, single document, no cost
sheet to check against.

**4 — Document generators.** Retail Path DIY Sales Sheet template **US$99** (fetched: one fill-in
template plus six examples; *"contains no text referencing margin calculation, retailer margin, case
pack, pricing calculator, or number checking"*). Satellite CPG generates dynamic sell sheets. They
**produce** the document; they never verify it.

**5 — Enterprise deduction platforms.** HighRadius, SPS Commerce, Vividly, Esker, Confido. The
closest structural analogue — they genuinely reconcile a deducted price against the brand's own cost
file — but they fire **post-sale**, against invoices and debit memos, for brands already shipping with
accounts-receivable deductions. Enterprise-priced, wrong moment, wrong buyer.

**And the humans.** Fractional CPG consultants **US$200–450/hour** on **US$5.000–15.000/month**
retainers; broker retainers **US$1.000–15.000/month plus 3–7% commission**; sell-sheet consulting
quoted at **US$900–1.200**. *(Human prices are snippet-derived and marked UNVERIFIED — re-verify on
the vendor pages before any of them appears in customer-facing copy.)*

**The one cheaper human is net-positive evidence.** Emily Anne Page sells **US$300** ECRM pitch
coaching (US$500 list) — a real ex-buyer, coaching *delivery*, not arithmetic. She gates her discount
on **proof of ECRM purchase**, which independently proves this exact roster population is reachable
and already converts at a US$300–500 price point.

---

## 6. Economics

### Two revenue lines, deliberately

**Line 1 — the audit. US$750, one-time, at the acute moment.**
Priced at 4–9% of the session fee the brand has already sunk. Above Emily Anne Page's US$300, far
below any human who would actually check the arithmetic.

**Line 2 — Cost Sheet Drift. US$79/month, recurring.** *This is the structural fix for the one-shot
problem, and it invents no demand.*

A CPG brand's cost sheet moves — cost of goods, freight, tariffs, packaging, a co-packer price
change. **The moment it moves, every document that quotes the old numbers is silently wrong**: the
deck, the sell sheet, the line sheet, the price list sent to three distributors, the promo plan.
Drift watches the sheet and reports *"your landed cost moved 4,1% on 3 March; six documents still
cite the old figure, and two of them now show a margin you cannot honour."*

The trigger is continuous, it is generated by the customer's own business, and no clearing party
touches it.

### The arithmetic to R$30.000/month net

Target: **US$7.400–8.300/month revenue.**

| Mix | Composition | Monthly |
|---|---|---|
| Audit-only | 11 audits × US$750 | US$8.250 |
| **Blended (the plan)** | **6 audits × US$750 + 45 Drift × US$79** | **US$8.055** |
| Drift-heavy (steady state) | 2 audits × US$750 + 80 Drift × US$79 | US$7.820 |

**Why the blend is the plan.** Audit-only requires eleven *new* customers every month, forever,
against a run-rate of roughly 2.500 new roster names per year — a sustained ~5,3% conversion of the
entire annual population. That is the treadmill that defeated eighteen prior candidates. The blend
requires **six** new audits a month and lets the base accumulate. At 45 Drift accounts the business
has a floor that does not reset on the first of the month.

**Acquisition.** At US$750 with acquisition capped at 30%, the budget is US$225 per audit — roughly
150 clicks at US$1,50, or one cold-email sequence to a named, qualified, receipt-carrying prospect.
Drift's lifetime value at even ten months is ~US$790, which supports a CAC of US$230 and makes paid
search viable on the audit as the entry point.

**Capital at risk before the first sale: under US$220.** Domain ~US$12, email tooling ~US$20/month,
contact-data credits US$50–100, Stripe/Wise free. The build is days of agent-directed work, not money.

**Stated honestly: these are gross figures.** Before Brazilian and US tax, Stripe fees, tooling,
refunds and founder time. US$8.055 gross is not R$30.000 net, and the net calculation must be done
with an accountant before this document is used to make a decision.

---

## 7. Go to market

**The whole motion is written English, fully scripted, faceless.** No calls, no camera, no name, no
audience, no network. This is not a workaround; it is the design.

**Step 1 — the list.** Read the live rosters by hand. ~30 names per roster, ~456 available today,
~2.500 per year. Take the domain from the roster's own link. Source the person from the company site.
**No automated scraping of ECRM.**

**Step 2 — the email.** One paragraph. It does not pitch, does not ask for a call, does not ask for
files:

> *You're on the seller roster for [session name], [dates]. Attached is a 40kb file — open it, pick
> your deck and your cost sheet, and it will tell you in about ninety seconds how many numbers in
> your deck disagree with your own spreadsheet. It runs entirely on your computer; nothing is
> uploaded and I never see your costs. The count is free. If it finds something and you want the
> detail plus a corrected one-page buyer economics sheet, that's US$750.*

**Why this works where a normal cold email does not.** It carries an artifact, not a claim. It asks
for ninety seconds, not a meeting. It pre-empts the confidentiality objection in the same sentence
that raises it. And the qualifying event happens *on their machine* — a brand with five discrepancies
converts itself.

**Volume and legality.** ~200 emails/month against a new domain's safe 600–1.000. **USA:** CAN-SPAM
permits opt-out B2B commercial email if the formal requirements are met. **UK:** workable under PECR
for corporate subscribers. **Germany: excluded entirely** — UWG §7(2) is consent-based and
competitor-enforceable. Canada's CASL is consent-based; treat as excluded pending advice.

**Step 3 — checkout.** Stripe payment link. Licence key unlocks the report. No account, no onboarding
call, no implementation.

**Step 4 — Drift.** Offered only after a paid audit, to a customer who has already seen the tool find
something real.

---

## 8. Build

**One self-contained HTML file.** SheetJS and pdf.js inlined in a single classic script so it works
over `file://`. No server, no account, no dependency at runtime.

**Input design, in priority order:**
1. **`.xlsx`/`.csv` — primary and authoritative.** Always machine-readable. Every computed number
   comes from here.
2. **PDF with a text layer — opportunistic.** Verified reality: of 14 real CPG PDFs tested, **11 had
   a usable text layer** — the extraction path works 79% of the time.
3. **Flattened/image slides — vision fallback.** A blind measured test on flattened CPG economics
   sheets returned **84/84** on a clean sheet and **82/84** on a badly degraded one (navy background,
   6pt reversed type, JPEG quality 38, rotated), with **money fields 36/36 on both** and both errors
   in UPCs, which enter no margin calculation. Optional, off by default, and the only thing that
   would ever touch a network — and it touches only the *deck*, which is a document the brand is
   about to hand to a stranger anyway.
4. **Typed fallback — a first-class path, not an apology.** *"Three slides had image-only numbers —
   type them here."*

**Two local error detectors, free and deterministic:** UPC-A check-digit validation, and internal
consistency of the sheet itself (case price versus unit cost × pack, margin versus the stated
wholesale and SRP).

---

## 9. What is NOT proven — and the three numbers that decide everything

This is the honest core of the document. Three unknowns, none resolvable from a desk, all resolvable
in one twelve-day test.

**A. INPUT EXISTENCE — do these brands have a usable cost spreadsheet at all?**
The August parser gate found public sell sheets exist for only **2,7% of brands** (7 documents from
262 probed). That was read at the time as a parser failure. **It was an input-existence failure** —
and it measured the wrong artifact class, because published marketing catalogs deliberately omit
wholesale pricing for editorial reasons and are disproportionately flattened. *A private line sheet
emailed to one buyer has neither property.* But the real rate is unmeasured, and if a brand pitching
at ECRM does not maintain a structured cost sheet, there is no product for them.

**B. DEFECT RATE — how often do the two documents actually disagree?**
**This is the number nobody has ever measured, and it is the one that decides the business.** The
product's value is `P(discrepancy exists) × cost of a discrepancy`. If a brand builds its deck from
its cost sheet and nothing has changed since, the scan returns zero and the tool has nothing to sell.
No prior version of this plan named this risk. It is now the primary kill criterion.

**C. WILL A STRANGER RUN A FILE FROM AN UNKNOWN SENDER?**
The local-first design removes the confidentiality objection but introduces a new one: a founder must
open an HTML attachment from a Brazilian sender they have never heard of. Mitigations: host it on a
plain HTTPS page rather than attach it; make the page inspectable; publish the checks it runs. But
this is unmeasured.

**Also unverified, and recorded rather than buried:** the human-substitute prices in §5 are
snippet-derived; whether ECRM or RangeMe would build the cross-document check as retention (they have
had the opportunity and instead shipped catalog search and reverse image search); the net figure
after Brazilian and US tax; whether Drift retains; and whether roster publication cadence supports
six audits a month rather than three.

---

## 10. The test — US$200, twelve days, three thresholds

**Do not build the full product first.** Build the scan and the count. Nothing else.

**Days 1–4.** Build the local scanner against the two error classes that are certain to exist —
margin-versus-cost-sheet, and case-pack-versus-unit-cost. Free count only. No report, no corrected
one-pager, no payment.

**Days 5–12.** Read the live rosters. Send **30** one-to-one emails to named brands on dated
sessions at least six weeks out. Scripted English, no calls.

**Three thresholds, all fixed before the test starts:**

| | Threshold | What it settles |
|---|---|---|
| **A** | **≥8 of 30** open the tool and complete a scan | The stranger-file objection, and reply rate |
| **B** | **≥50% of completed scans find at least one material discrepancy** | **The defect rate — the number that decides the business** |
| **C** | **≥2 pay US$750** on seeing their own count | That the business exists |

**Fail on any one and it dies for US$200 instead of two months.**

Borrowed discipline, and it governs this test absolutely:

> **Positive replies, "interested", requests to stay in touch, free pilots and refundable
> reservations do not count. And do not reinterpret a failure as "we need better positioning."**

**Run the commodity gate in parallel, at zero cost.** Seed one public fixture — a deck and a cost
sheet with five deliberate, known discrepancies — and send the identical fixed scope to three
freelancers. **If two deliver a working reconciliation for ≤US$100 in ≤2 hours, kill it
unconditionally.** Cheap promises without repository evidence do not count.

---

## 11. Post-launch kill criteria

Numeric, committed in advance, so the decision is not made by hope.

- **Defect rate below 35%** across the first 50 real scans → the product has no reliable trigger. Stop.
- **Fewer than 3 paid audits by day 60** → the channel does not convert at this price. Stop or reprice.
- **Drift conversion below 15%** of paid audit customers by day 90 → there is no recurring business,
  and the audit alone cannot reach the target. Reassess.
- **Support exceeding 4 hours per week** → this is a service, not a product. Stop.
- **ECRM or RangeMe ships cross-document reconciliation** → the shield is gone. Stop immediately.
- **Roster publication drops below ~150 new named brands per quarter** → the list cannot feed six
  audits a month. Widen to KeHE and re-test.

---

## 12. Risk register

| Risk | Class | Handling |
|---|---|---|
| Defect rate too low | **Bucket A — could be fatal** | Threshold B in the test. Primary kill criterion |
| Brands lack a structured cost sheet | **Bucket A — could be fatal** | Threshold A. Disqualify rather than serve badly |
| ECRM/RangeMe build it | Bucket A if it happens | Not actionable in advance; monitored as a kill criterion. Evidence to date: they shipped reverse image search |
| Roster stream too lumpy for 6/month | Bucket A on arithmetic | KeHE as verified second source; widen if it fires |
| Stranger will not run the file | Bucket B | Threshold A. Mitigated by hosting rather than attaching |
| Cold reply rate | Bucket B | Threshold A |
| US$750 price acceptance | Bucket B | Threshold C |
| Vision misreads a deck number | **Neutralised by architecture** | Margins never come from pixels; worst case is a dismissible false flag |
| Confidentiality of cost data | **Neutralised by architecture** | Local execution; the sheet never leaves the machine |
| Credential / regulated activity | **None** | Retail arithmetic is unregulated; output is self-verifying |
| ECRM Terms of Use | Handled | Manual reading only, never automated scraping |
| Germany / Canada outbound law | Handled | Excluded from the sending list |

---

## 13. What this is really a bet on

Not on CPG, and not on ECRM. Those are the first instance, chosen because the buyer's solvency is
printed on a public page.

The bet is on a position that four independent processes converged on after thirty-three failures:

> **When generation becomes free, verification becomes scarce.**
> Anyone can produce an artifact in seconds. Nobody can tell which ones are correct. Checking is not
> content, so no marketing department can give it away. The party who profits from free generation
> has no incentive to say its output is wrong. And the pile of unchecked artifacts grows every month,
> on its own, without anyone selling anything.

DeckProof is one instance. If the test kills it, the position survives it — and the next instance is
found by asking the same three questions: *where has free generation multiplied the artifacts, who
pays when one is wrong, and does anybody currently check?*
