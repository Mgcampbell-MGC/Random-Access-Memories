# LIVE CANDIDATES — the running list

**Maintained. Everything else is in `GRAVEYARD.md` or its own kill file. Status as at 21 Aug 2026.**

---

## #1 · THE WORKING-DAY LEDGER ★★ — *shipping terminal ledger* → **GATELEDGER**

> **★ 20 Aug: chosen by the founder as THE idea and taken through a two-counsel refinement (business-case +
> adversarial). The two-pager is `GATELEDGER_Business_Overview.docx`.** Pricing honesty preserved: the blueprint
> path to $11.111/mo (2 white-label + 8 Dispute Desk + 6 Ledger + 15 packs) stands NEXT TO the adversarial
> corridor ($150–350/mo + $49–99/extract, white-label load-bearing). **Five pre-committed kill bars are in the
> document; nothing gets built until the 30-email probe and the BlueCargo free-tier check return numbers.**

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
| **Verified by me** | `lynx.yti.com/ClosedAreaMatrix.aspx` = the terminal operating system, **HTTP 200, no login** · Maersk's 2,7 MB empty-return directory: **200 today; 13 of 14 consecutive prior dates 404** (re-tested 21 Aug — one live edition at a time, predecessors erased permanently) · **FreeTSA, DigiCert, Izenpe, Sectigo all returned RFC 3161 `Status: Granted`** over today's bundle, free |
| **Days banked** | **Three** — 19/20/21 Aug. Pipeline rebuilt 21 Aug as `bin/capture_ledger.py`: frozen slugs, Maersk edition discovery, **real Merkle root with per-source inclusion proofs** (the v1 field named `daily_merkle_root_sha256` was recovered by search and was a **flat concatenation** — it could not prove one terminal-day without disclosing all six). See `archive/working_day_ledger/README.md` |

### ★★ SURVIVED A 24-INDUSTRY UNIQUENESS SWEEP, 20 Aug
The inverted hunt censused every contingency-fee recovery industry findable. **The structure this candidate
sits on — refund-side buyers + a posted schedule whose poster is NOT the invoice-issuer + a bounded capture
universe — occurred EXACTLY ONCE in 24 industries.** Every rival died on the go-forward split (savings-fee
buyers don't buy history), the incorporated-schedule corollary (the poster archives its own invoice inputs),
claimant-evidence, gazette, platform-arbiter, or head-start. See `THE_RECOVERY_CENSUS.md`.

### ★★ RESTATED 21 Aug — the annual-calendar objection survives, but I NAMED THE WRONG PAGE TWICE

**The objection: if terminals publish a full-year calendar, closures are knowable in advance and the archive
has no scarcity.** My 19 Aug answer — *"YTI's gate schedule is a rolling ~6-day window whose values vary"* —
was **FALSE**, and so was the follow-up correction that called it byte-identical. Three banked captures,
parsed as **content**:

| source | text lines | changed in 2 days |
|---|---|---|
| `yti_gate_schedule` | 172 | **1** — `Today's Date` |
| `yti_closed_area_matrix` | 30 | **18** |

**The gate schedule is a STATIC forward calendar** (published 9–11 days ahead; its only full-day closures are
weekends) — and Maersk's tariff, *"partial day closures are considered as a full working day"*, means its
shift detail moves no denominator. **It is not the product.**

**The product is the CLOSED-AREA MATRIX and EMPTY-RETURN ACCEPTANCE**, and both were measured changing. The
matrix rolls a 7-day window, so 21–25 Aug appear in all three captures — which tests revision for free:

| day / shift | 19 Aug | 20 Aug | 21 Aug |
|---|---|---|---|
| **Mon 24, 1st** | `1D 1E 1G 2F 3F` | `1D 1E 1G 2F 3F` | **`1C 1D 1E 1F 1G`** |
| **Mon 24, 2nd** | `1C 1F 1G 2D 2E 3D 3E` | `1C 1F 1G 2D 2E 3D 3E` | **`1C 1F 1G`** |
| **Tue 25** | `TBA` | `TBA` | **resolved to real blocks** |
| **Wed 26** | *(not in window)* | `1D 1E 2C 3C` | **withdrawn to `TBA`** |

**Monday 24 was revised twice; Wednesday 26 was published concrete then retracted. And 19–20 Aug have already
rolled off — the live page can no longer say what was closed on the 19th.** Erasure *and* revision, measured.
The legal hook for this half is **46 CFR 545.5(c)(2)(ii)** — detention charged when empty containers *"cannot
be returned"* is *"likely to be found unreasonable."*

**★ AND THE MOAT IS NOW EXPLAINED STRUCTURALLY, not observationally.** `THE UNIFICATION` (21 Aug): a party
archives an operational fact exactly when its own invoice depends on it. **YTI has no invoice to defend
because the CARRIER issues it — so YTI erases, and that is not luck.**

**⚠ OPEN — and the whole thing turns on the first one:**
1. **8 of 20 terminals verified publicly readable. Not twenty.**
2. **The moat is probabilistic, not structural** — plain GET pages; what protects them is that no crawler visits
   a gate schedule twice a day. **Archive risk UNVERIFIED** (`web.archive.org` blocked all day).
3. **`THE SUBSET LAW` must be re-run against this version.** It killed the previous one.
4. **★ NEW, 19 Aug — THE COMMODITY-CAPTURE CAVEAT.** The raw capture is not a moat: **Stillio publishes
   $29/month for scheduled dated screenshots of unlimited pages.** Anyone can point it at the same seventeen
   terminal pages tomorrow. **The defensible part is (a) starting today and (b) the PARSE — turning raw pages
   into a per-terminal, per-shift, per-day calendar joined to the carrier tariff definitions. Build the parse,
   not the screenshotter.**

### ★ PASSED TWO MORE TESTS, 19 Aug
**THE TWO-DATES TEST** *(which killed the usage-rights ledger)*: the buyer owns the invoice and the charge
period **but not which days within it the gate was open** — that belongs to a third party and is in the past.
And **a demurrage charge is a CLOSED historical interval; there is no present tense to inspect.**
**THE SPECULATIVE-CAPTURE LAW**: the universe is **~17–20 pages a day**, against the commercial web for the
candidate that died on it.

> **NEXT ACTION: the ten-day, twenty-terminal capture. Under $20, no phone, no account — and the test IS the
> build, because those ten days are the first ten days of the asset.**

### ~~THE INLAND RAIL RAMP COLUMN~~ — **KILLED 21 Aug, the day after it was added**

The split was **real**: Union Pacific's own tariff (PR2023-141, ITC §C.12) says *"if an Intermodal Terminal is
closed for an entire calendar day for any reason, that day will not be included in the Free Time or Storage
Charge calculations"* — 541.6's shape in a private tariff — and under a through B/L the ocean carrier issues
the invoice while the railroad posts the closure. **It dies on erasure instead: UP archives its closure
notices permanently.** `IM2020-82` (Yard Center IL, 1 Jun 2020) and `IM2020-140` (Houston, Hurricane Laura,
25 Aug 2020) both return **HTTP 200 verbatim today**, on **sequential integers**. See
`THE_SPLIT_PREDICTS_ERASURE.md`.

### ★★ THE CHASSIS COLUMN — UPGRADED 21 Aug to a SECOND BUYER FAMILY, same cron, zero extra capture
**Demand signals, 21 Aug (SECONDARY):** pools bill **$12–55/day**; **per-diem disputes run a 15–20% audit hit rate**; drayage is described as **the highest error-rate freight mode**; automated drayage audit recovers 3–5% of spend. **Per-diem auditors and drayage 3PLs outnumber ocean D&D recovery firms — add them to the 30-email probe.**\n\nChassis lessors bill per-diem; terminals/depots generate the acceptance state — **poster ≠ invoice-issuer, the
541.6 structure in private-contract form.** Passes two-dates and speculative-capture. **Fold into the ten-day
capture, gated on a three-part test:** dated per-location state visible from a real browser (CCM/TRAC are
Cloudflare-blocked from the container) · CCM's own `/news/` delta doesn't already reconstruct it · **and ≥5 of
20 published IANA arbitration decisions turned on world-state evidence rather than the carrier's own conduct
logs.** That last number is load-bearing. See `THE_CONVERGENCE_HUNT_RESULTS.md`.

---

## #2 · THE DECRS CHANGE-LOG — *FDA drug establishment register*

**The pitch.** FDA publishes a daily file of every registered drug establishment and **never publishes what
left it**. Archive the daily snapshot and the change-log becomes an artefact the agency will not produce.

| | |
|---|---|
| **Measured by me** | 10.414 rows · 9.837 unique FEIs · **100,00% email on TWO separate fields** · 43,7% of rows yield a second distinct human · all 10.414 share one expiry date (12/31/2026) · the exclusion file is **named** |
| **Why it beat the version that died** | `THE_FDA_TEST` killed the *device* register on `THE NAMEABILITY CONDITION` — the vanished records were anonymous integers. **Here the firm name, address and two working emails sit on the same row as the identifier** |
| **Day 0** | **Banked** — `archive/decrs/2026-08-19.tsv.gz` |

### ★ FIRST OBSERVED DEMAND COMPARABLE, 21 Aug
**Redica/FDAzilla sells FDA 483 inspection documents self-serve at $289/document** — buyers demonstrably pay
high-three-figures, self-serve, for FDA facility-level intelligence, **and Redica sells no registration
change-log.** Direct counter-evidence to the "$0–100 pincer band" weakness.

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

> ### ★★ **Q1 ANSWERED, 21 Aug — SOMETHING VANISHED.** **FEI 3011921873, LABORATOIRES EXPANSCIENCE** (Epernon,
> France; MANUFACTURE; contact `CSILLY@expanscience.com`; registrant Meena Rana; US agent Potomac Law) was
> **present on 20 Aug and ABSENT on 21 Aug.** Verified not a key change: **zero rows** match its FEI, its DUNS
> (347941502) or its firm name on the 21st. **FDA publishes no record of the departure.**
>
> **And the vanished row was FULLY NAMEABLE** — firm, address, two working emails, named US agent. That is
> precisely the property whose absence killed the DEVICE version under `THE NAMEABILITY CONDITION`.
>
> ⚠ **Honest caveat: one removal, one day.** It could be a deregistration, a data correction, or a transient
> republish. **The archive now accumulates that answer daily** — diffs so far: 19→20 **+4/−0**, 20→21 **+3/−1**.

> ### ★ AND A TIMING FINDING WORTH MORE THAN THE ANSWERS: **the annual review window is 1 October – 31 December** (207.29). **The file churns hardest in Q4, which is six weeks away — so the archive started today captures the single most valuable period in the year. Starting later means missing it by twelve months.**

*(Also open: archive risk UNVERIFIED · a 2020 snapshot is publicly purchasable, so NET CHANGE is back-fillable —
only the order and dates of changes are not.)*

### ⚠ A PRICE CEILING ARRIVED 21 Aug, and it cuts the other way

`THE ATTENTION TRILEMMA` work put a ceiling on what a change-feed subscription can charge: **self-serve
monitoring tops out around $99/month** (Visualping's published rate), and everything above it is sales-force
gated — vendors answer a pricing request with *"a calendar link followed by a 90-minute discovery call"*,
which is **C1-fatal**. Enterprise regulatory intelligence starts ~$50k/yr and lives entirely on that side.

**So #2 is ~111 subscribers at $100/month, not 18 at $650.** Same target, six times the customers, all
acquired through ranking she cannot win. **This is the single biggest change to the board today and it widens
the gap between #1 and #2 more than the six-lens tournament did.** *(The $289/document Redica comparable still
stands — but it is per-document, not subscription, and it prices a DOCUMENT, not a feed.)*

---

## #3 · THE SCAN KEEPSAKE MACHINE — *formerly "the baby book", upgraded 20 Aug*

> ### ★ THE UPGRADE: the kill-condition ("does she write every book?") is resolved BY SUBTRACTION — **zero generated prose**. The artifact family (enhanced portraits from the parents' own uploads, heartbeat-soundwave print, star chart, name-and-dates typesetting) is 100% deterministic machine work; her role is QA and exceptions. **And a second, larger corridor exists: white-label to US/UK elective ultrasound studios (one UK franchise HQ = 35 clinics), invoiced per unit as an exported service at 8,1%.** Incumbents split between catalogue blanks (no margin) and digital-only AI (no print) — **the machine-personalised PRINTED artifact threads the catalogue scissors, which nothing else in two days has.** See `THE_SCAN_KEEPSAKE_MACHINE.md`.
>
> **THE TEST (serves both corridors, pre-committed bars): 20 real scan images → full pipeline → stopwatch. KILL at median >5 min/unit or <14/20 shippable; PASS at ≤3 min and ≥18/20.** No money, no phone, one week.
>
> **Weakest link, stated:** channel economics rest on one bear vendor's own marketing (~1-in-3 attach — SECONDARY); BabyFlix could add print with one integration, so the durable asset is the signed channel.

### The original consumer version, for the record

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
