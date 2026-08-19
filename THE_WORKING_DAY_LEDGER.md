# THE WORKING-DAY LEDGER — the idea, rebuilt after it was killed

**19 Aug 2026. The appointment-availability archive died this afternoon on four independent grounds
(`THE_PORT_EVIDENCE_KILL.md`). A third agent, briefed to improve rather than attack, found the thing
underneath it. Every load-bearing fact below was re-verified BY ME, because I have been wrong twice today.**

---

## 1. WHAT CHANGED — drop the appointment slots, keep the calendar

| | Killed version | **The rebuild** |
|---|---|---|
| Captured | Appointment slot availability | **Gate OPEN/CLOSED per shift + empty-return acceptance per shipping line** |
| Access | **Behind a login at 17/17 terminals** | **Public, unauthenticated, server-rendered HTML** |
| Evidence type | Needed proof the customer *tried* | **Pure world-state — no claimant conduct involved** |
| What it is | Evidence in an argument | **★ An input to a legally mandatory invoice field** |

> ### **★ THE INSIGHT: gate open/closed is not evidence for a dispute. It is the DENOMINATOR OF THE INVOICE.**

**Maersk's own US Import Demurrage Tariff, effective 20 Jun 2026, defines the clock:**

> *"**Free time: Working Day basis defined as any day a gate is open for container pickup** Monday – Saturday.
> **Partial day closures are considered as a full working day**… **If a party made an appointment for a
> container but the terminal was closed, then that date shall not be considered a Working Day** with respect
> to that container."*

**And 46 CFR 541.6 makes these MANDATORY minimum invoice contents:** *"The allowed free time in days; The start
date of free time; **The end date of free time**… The specific date(s) for which demurrage and/or detention
were charged."* With **46 CFR 541.5**: failure to include required minimum information *"**eliminates any
obligation of the billed party to pay the applicable charge.**"*

**So the free-time end date on every US demurrage invoice is a function of which calendar days the gate was
open — and nobody retains that record.** She asserts nothing: she says *"YTI's published gate schedule showed
2026-08-22 1st CLOSED, 2nd CLOSED."* **The customer does the subtraction.** No expertise, no opinion, no
"before" — the shape `CLAUDE.md` says is the only sellable one.

---

## 2. ★★ WHAT I VERIFIED MYSELF TODAY

**(a) The terminal operating system is publicly readable.**
`https://lynx.yti.com/ClosedAreaMatrix.aspx` → **HTTP 200, 6.180 bytes, NO LOGIN**, rendering *"Closed Area
Matrix · 2026 · Aug 19 – Aug 25"*. **This is Yusen's TOS itself, not a marketing page.**

**(b) The erasure is real, and it is the cleanest instance in this project.**
Maersk publishes a **2,7 MB** empty-return-location directory at a date-stamped URL, *"updated each day at
1600 HRS EST"*:

| Date requested | Result |
|---|---|
| **2026-08-19 (today)** | **HTTP 200 — 2.709.258 bytes** |
| 2026-08-18 · 08-15 · 08-12 · 08-05 · 2026-07-19 | **HTTP 404 (4.309 B) — every one** |

> **★ This is `THE DATE-STAMPED FILENAME IS A BACK-FILL INVITATION` run as a test and coming back CLEAN.**
> Evergreen's identical naming convention still serves a PDF from 30 Aug 2024, so its back series is
> brute-forceable. **Maersk's 404s.** Same test, opposite answer — which is exactly why the test exists and why
> it must be run per-publisher.

**(c) The self-authentication works, is free, and needs no reputation.** Over the SHA-256 of today's captured
bundle (`a0da4396…c20aa6`), four independent publicly-trusted TSAs returned **`Status: Granted`** within
seconds:

| TSA | Result |
|---|---|
| `freetsa.org` | **Granted** — Aug 19 21:15:59 2026 GMT |
| **`timestamp.digicert.com`** | **Granted** — Aug 19 21:15:59 2026 GMT |
| `tsa.izenpe.com` | **Granted** — Aug 19 21:16:00 2026 GMT |
| **`timestamp.sectigo.com`** | **Granted** — Aug 19 21:16:00 2026 GMT |

**Nobody has to trust her clock, her brand or her word. They have to trust DigiCert and Sectigo, whose roots
are already in the reviewer's operating system**, and anyone can verify offline with `openssl ts -verify`.

> ### **★ THIS IS THE ANSWER TO THE "RECOGNITION TEST" THAT KILLED THE PREVIOUS VERSION.** Hapag-Lloyd and APL accept third-party evidence only where the source is *"in widespread use and generally recognized as reliable and accurate"* — which a new anonymous entity fails by construction. **A CA-countersigned hash chain replaces recognition with arithmetic.** And **FRE 902(13)/(14)** make such records self-authenticating on a **records custodian's** certification — *"authenticated by a process of digital identification"* — which is a fact about her own system, **never an expert opinion about the shipment.** Right side of the expert veto.

**(d) Day 0 is banked.** `archive/working_day_ledger/2026-08-19.tar.gz` — the 2,7 MB Maersk file plus five
terminal pages (TraPac LA empty returns, PNCT, ITS Long Beach shift-split, YTI gate schedule, YTI closed-area
matrix), the daily root, and all four RFC 3161 tokens. **The Maersk file is gone tomorrow.**

---

## 3. THE MONEY — measured, not argued

**Maersk US import tariffs, own published PDFs, effective 20 Jun 2026:**

| Per container per day | d1–4 | d5–8 | d9–13 | d14+ |
|---|---|---|---|---|
| **Demurrage**, dry | Free | **$300** | $345 | $395 |
| **Detention**, dry | Free | **$210** | $260 | $290 |
| **Demurrage**, reefer/special | Free (1–2) | **$490** | $590 | $640 |

**One wrongly-counted working day on one dry box = $210–395.** A $650/month subscription is $7.800/year —
covered by **20–37 dry container-days, or 13–16 reefer container-days, per year.** For an audit firm with a
book of thousands of containers that is not close. ***"Does one alert, acted on, pay for a year?"* — now
answered YES, with a tariff.**

---

## 4. THE BUYER — and why the two halves are structurally complementary

> **`Unwaived.com`: *"Success fee: 25–35% of recovered amounts"*; they *"plug into your ports + carriers
> data… assemble proof, and file the dispute"*, doing *"calendar-aware analysis of weekends, holidays, and
> **terminal closures**."* Their inputs are the CUSTOMER'S connectors. Their page shows NO historical archive
> of terminal state — and every invoice they touch is for a container that dwelled in the PAST.**

> ### **★ THE COMPLEMENTARY-HALVES STRUCTURE — the recovery firm holds the customer's conduct evidence and cannot buy back the past; she holds the past and can never have the customer's conduct evidence (C4 forbids it). EACH SIDE IS STRUCTURALLY BARRED FROM THE OTHER'S HALF.** That is the cleanest wholesale fit found in 73 candidates, and it is exactly why the previous version failed: it tried to sell the half the buyer already had.

**Other named buyers, each with a published evidence requirement:** anyone filing an **FMC Charge Complaint** —
the regulator's own guidance names the artefact: *"**Screen captures of denied booking appointments for return
of equipment, gate closures**, or relevant emails also can be provided"* (free, to `chargecomplaints@fmc.gov`) ·
**motor carriers in UIIA binding arbitration**, where **IANA publishes the decisions** — in case
`20211129-1-XXXG-PD` the panel found against the motor carrier because it *"could not provide proof"* of a
terminal state. **Those published decisions are a free, named, self-qualifying prospect list.**

---

## 5. DISTRIBUTION — `THE CONVERGENCE`, finally instantiated

**Publish free and public a page per terminal per day:**

> `/terminal/yti-los-angeles/2026-08-22/` — *"On 2026-08-22 Yusen Terminals' published gate schedule showed
> 1st shift CLOSED and 2nd shift CLOSED. Captured 06:14 and 09:02 PT. SHA-256 …. RFC 3161: DigiCert, FreeTSA."*

**20 terminals × 365 days × 3 fact types ≈ 22.000 pages/year** of exactly the long-tail query a dispatcher
types at 06:00 — *"was Pier A closed on August 22"*. **The pages that constitute the dataset are the pages that
get cited.** Per `THE SOURCING/REPUTATION SPLIT` she never has to win *"best D&D vendor"*; she only has to be
the answer to *"what was the state on that date"*, which has no incumbent.

**Give away today and the last 7 days — matching the terminals' own retention, so she takes nothing from them.
Sell everything older, which is the half that cannot be bought anywhere.** Cost to run: **Cloudflare R2 at
$0,015/GB-month with free egress + Workers at $5/month**; ~16 MB/day ≈ **5,8 GB/year**, so five years of
history costs about **$0,45/month**. **Under $20/month all-in, inside C5 by two orders of magnitude.**

---

## 6. ⚠ WHAT IS STILL NOT TRUE, AND THE ONE NUMBER IT TURNS ON

1. **★ EIGHT terminals are verified public, not twenty.** *"That is the one number the whole thing still turns
   on."* The coverage test has not been run.
2. **★ THE MOAT IS PROBABILISTIC, NOT STRUCTURAL — say it that way.** These are plain GET pages, so they are
   crawlable in principle. What protects them is that **no crawler visits a terminal gate schedule twice a
   day**, and a single snapshot cannot reconstruct a per-shift series. **`web.archive.org` returned HTTP 429
   again today, so archive risk remains UNVERIFIED** — for the third time in this file.
3. **MSC, Hapag-Lloyd, ZIM, OOCL, APL and CMA CGM all 403'd.** CMA CGM's capture-spec wording was obtained only
   through a translation proxy — **treat as second-hand.**
4. **No cargo-insurer claims policy demanding contemporaneous terminal state was found. Do not claim that buyer.**
5. Whether the code-signing TSAs' CPS permits arbitrary-document timestamping was **not read** — FreeTSA and
   Izenpe are explicitly general-purpose; use those as primary.
6. **The `THE SUBSET LAW` check must be re-run against THIS version.** It killed the last one. Here the buyer's
   mandatory artefact is their own conduct evidence, which does **not** contain the historical gate calendar —
   **so the subset does not appear to close. That reasoning needs an adversarial pass before anything is built.**

---

## 7. THE TEST — and the test IS the build

> **Take the eight terminals verified public today, add twelve from the top-20 list, and run the capture twice
> daily for ten working days. Count how many of the twenty yielded a parseable open/closed or empty-return
> state on ≥18 of 20 runs. Fewer than ~12 ⇒ coverage too thin to sell. 12 or more ⇒ the ten days of captures
> are already the first ten days of an asset that cannot be back-filled.**
>
> **Cost: under $20. No phone, no account, no terms of service accepted.**

**In parallel, written-only:** email the D&D recovery and freight-audit firms one question — ***"When you
dispute on 'no empty return location', where do you get the terminal's state for a date three months ago?"*** —
and count the answers containing a number.
