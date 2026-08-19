# LIVE CANDIDATES — the running list

**Maintained. Everything else is in `GRAVEYARD.md` or its own kill file. Status as at 19 Aug 2026.**

---

## #1 · THE WORKING-DAY LEDGER ★★ — *shipping terminal ledger*

**The pitch in one paragraph.** Importers are charged large daily late fees (demurrage and detention) when a
container sits at a US port past its free time. **But free time is counted in WORKING days — and a day the
terminal's gate was closed is legally not a working day.** Terminals publish today's gate schedule and
empty-return acceptance and then overwrite it within about a week. **Nobody keeps the series.** She scrapes it
twice daily, archives it with cryptographic timestamps, and sells the history to the firms that fight these
fees for a percentage.

| | |
|---|---|
| **Shape** | S3 + S4 — continuous operation producing a compounding dataset |
| **She never** | speaks · touches a customer system · asserts an opinion · takes title to anything |
| **Why it is not evidence but arithmetic** | Maersk's tariff: *"Free time: Working Day basis defined as **any day a gate is open**"*. **46 CFR 541.6** makes the free-time end date a **mandatory** invoice field; **541.5** voids the obligation to pay when required fields are missing. She reports the gate state; the customer does the subtraction |
| **Money** | **$210–395/container/day dry; $490–640 reefer** (Maersk's own published tariffs). One wrongly-counted day ≈ a month of subscription |
| **Buyer** | D&D recovery firms on **25–35% success fees** (Unwaived and peers) · anyone filing an FMC Charge Complaint · motor carriers in UIIA arbitration — **and IANA publishes those decisions, which is a free named prospect list** |
| **Why the wholesale fit is unusually clean** | They hold the customer's conduct evidence and **cannot buy back the past**; she holds the past and can **never** hold conduct evidence. Each side is structurally barred from the other's half |
| **Distribution** | `THE CONVERGENCE` — a public page per terminal per day *is* the dataset and *is* the marketing. Free for the last 7 days (matching the terminals' own retention); the older half is sold |
| **Cost to run** | Cloudflare R2 + Workers, **under $20/month**; ~5,8 GB/year |
| **Verified by me** | `lynx.yti.com/ClosedAreaMatrix.aspx` = the terminal operating system, **HTTP 200, no login** · Maersk's 2,7 MB empty-return directory: **200 today, 404 on all five prior dates tested** · **FreeTSA, DigiCert, Izenpe, Sectigo all returned RFC 3161 `Status: Granted`** over today's bundle, free |
| **Day 0** | **Banked** — `archive/working_day_ledger/2026-08-19.tar.gz` with all four timestamp tokens |

### ★ SURVIVED A KILL ATTEMPT, 19 Aug — the annual-calendar test

**The sharpest objection to #1: if terminals publish a full-year holiday calendar, closures are knowable in
advance and the archive has no scarcity.** Tested by reading YTI's gate schedule rather than counting it:

| | 1st shift | 2nd shift |
|---|---|---|
| 17–19 Aug | OPEN | OPEN |
| **20 Aug** | OPEN | **CLOSED** |
| **21 Aug** | OPEN | **CLOSED** |
| **22 Aug** | **CLOSED** | **CLOSED** |

**A rolling ~6-day window, values varying week to week. These are operational closures, not statutory holidays
— no annual calendar contains them.** *(And it satisfies `THE OUTCOME-IS-RETAINED LAW` uniquely: a gate
calendar has no outcome. Every day IS its own outcome and nothing supersedes it.)*

**⚠ OPEN — and the whole thing turns on the first one:**
1. **8 of 20 terminals verified publicly readable. Not twenty.**
2. **The moat is probabilistic, not structural** — plain GET pages; what protects them is that no crawler visits
   a gate schedule twice a day. **Archive risk UNVERIFIED** (`web.archive.org` blocked all day).
3. **`THE SUBSET LAW` must be re-run against this version.** It killed the previous one.

> **NEXT ACTION: the ten-day, twenty-terminal capture. Under $20, no phone, no account — and the test IS the
> build, because those ten days are the first ten days of the asset.**

---

## #2 · THE DECRS CHANGE-LOG — *FDA drug establishment register*

**The pitch.** FDA publishes a daily file of every registered drug establishment and **never publishes what
left it**. Archive the daily snapshot and the change-log becomes an artefact the agency will not produce.

| | |
|---|---|
| **Measured by me** | 10.414 rows · 9.837 unique FEIs · **100,00% email on TWO separate fields** · 43,7% of rows yield a second distinct human · all 10.414 share one expiry date (12/31/2026) · the exclusion file is **named** |
| **Why it beat the version that died** | `THE_FDA_TEST` killed the *device* register on `THE NAMEABILITY CONDITION` — the vanished records were anonymous integers. **Here the firm name, address and two working emails sit on the same row as the identifier** |
| **Day 0** | **Banked** — `archive/decrs/2026-08-19.tsv.gz` |

### ★ TWO OF THE THREE BLOCKERS CLEARED, 19 Aug — both favourably

**Q2 — is the US agent the filer? NO, on the regulation's face.** **21 CFR 207.69** makes the agent a
*communications conduit*, not a filer: *"Registrants of foreign establishments… must designate a single United
States agent"*, whose duties are *"reviewing, disseminating, routing, and responding to all communications from
FDA"*, answering questions on imported drugs, and *"assisting FDA in scheduling inspections."* **21 CFR 207.29
puts the filing on the registrant** — *"Registrants must review and update all registration information."*
**So the device-side trap does not transpose cleanly.** ⚠ It still bites in one direction: selling a US agent a
monitor of *their own client roster* remains selling a firm its own outbox. **Sell to a third party watching a
supply chain it does not file for.**

**Q3 — is the buyer already legally compelled? NO, not for third-party monitoring.** 207.29 compels a registrant
to update **its own** record annually, and *"if no changes have occurred… registrants must certify that no
changes have occurred."* **Nothing compels anyone to monitor another establishment's status.** That is the
distinction that killed the device version, where 21 CFR 807.22(b)(3) compelled the check inside FURLS.

**Q1 — does anything actually vanish? STILL OPEN, and unmeasurable from one snapshot.** Day 0 is banked; this is
now a waiting game, not a research question.

> ### ★ AND A TIMING FINDING WORTH MORE THAN THE ANSWERS: **the annual review window is 1 October – 31 December** (207.29). **The file churns hardest in Q4, which is six weeks away — so the archive started today captures the single most valuable period in the year. Starting later means missing it by twelve months.**

*(Also open: archive risk UNVERIFIED · a 2020 snapshot is publicly purchasable, so NET CHANGE is back-fillable —
only the order and dates of changes are not.)*

---

## #3 · "ANTES DE VOCÊ CHEGAR" — *the baby book*, and the book family

**The pitch.** After a 3D/4D ultrasound the mother scans a clinic QR code and buys a **R$349 hardcover**. She
uploads her own cropped images and fills a questionnaire — **the clinic transfers nothing**. The book arrives
already written: the discovery, the ultrasound timeline, the story behind the name, letters, a final page for
the birth photo. A Brazilian lab prints and ships. The clinic keeps ~R$70.

| | |
|---|---|
| **Shape** | **S1 — written work.** The over-explored shape, and the reason it must be justified deliberately rather than presented as new |
| **Founder fit** | The best in the file: never speaks · faceless · **the mother uploads her own images, so C4 is clean by design** · lightest build of 64 candidates · and it is literally the work she asked for |
| **Unit economics** | Lulu premium colour casewrap 8.5×8.5, 40pp = **$19,57**; fulfilment **$1,75** fixed; **white-label packing slip confirmed**, outer carton marking still unconfirmed |
| **⚠ The competitors, found on the correction pass** | **Qeepsake** free lite / $47,88 / $95,88+book · **Baby Notebook** free app / $49,99 yr / $99 book · **The Short Years** from $129. The prompted-app-to-printed-book category is **occupied in English** |

**⚠ THE UNRESOLVED PROBLEM, stated plainly: she personally produces every unit.** That is the production
ceiling — **~US$142 per hour of delivery time** — and it is what killed candidates 70, 71 and 72. **This
candidate lives or dies on whether the writing is genuinely a machine that runs once and serves many, or her
hands on every book.** Nothing else about it is in doubt.

**Sibling books in the family:** candidates 70, 71, 72 (all *questionnaire → she writes prose → deliverable*,
all killed as one idea with three buyers), and the wider book family. **Rule 1 applies: do not propose another
one without naming the shape out loud.**

---

## HOW THIS LIST IS MAINTAINED

- A candidate stays only while it has a **named open question and a test that answers it.**
- **Every kill gets its own file with the cause of death and the sources.** The cause is the reusable part.
- **Day 0 first.** Where a candidate depends on an accumulating archive, start capturing before deciding —
  it costs nothing and cannot be done retroactively.
