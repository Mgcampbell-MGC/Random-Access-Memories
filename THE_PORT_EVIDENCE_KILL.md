# THE APPOINTMENT-EVIDENCE ARCHIVE — KILLED, 19 Aug 2026

**Proposed in the morning as the first candidate in seventy-three the founder said he loved. Killed the same
day by a red team, on three independent grounds, any one of which is sufficient. Recorded in full because the
causes of death are reusable and the candidate is not.**

---

## 0. ⚠ FIRST, MY OWN ERROR — I reported a data table that was a cookie policy

I told the founder that `losangeles.trapac.com/real-time-yard-status/` was *"public, 83.829 bytes, with a real
data table and no login."* **It is not.**

**Verified against my own captured file:**
- The page body contains **`Real-Time Yard Status Quick Check Loading...`** — the data is **not server-rendered**.
- **The single `<table>` in those 83KB is the COOKIE-POLICY TABLE** — literal cell headers *"Third Party | Type
  of Cookie | More Information"*.
- `grecaptcha` and `admin-ajax.php` are both present in the source.
- The red team POSTed to the endpoint. TraPac's own reply, verbatim:
  > `{"code":"robot","html":"<p>Hmm... something went wrong. Your request is being identified as a form of
  > robotic data scrapping.</p>…<p>To obtain more information about our TraPacAPI or sign-up for free access,
  > please contact <a href="mailto:…@trapac.com">…</a>.</p>"}`

**I ran a table COUNT and reported it as a data CHECK.** That is the third time in one day this exact failure
mode has produced a confident wrong number here — after the vocabulary count that returned "30/30 clean"
because the extractor was reading page boilerplate, and the FDA join before it.

> ### **A COUNT OF STRUCTURES IS NOT A CHECK OF CONTENT. Print the first row and READ IT before reporting that a table, a column or a field exists.** *(`CLAUDE.md`'s standing rule held again: the result was too clean to be true, and it was.)*

---

## 1. ★★ KILL ONE — 0 OF 17. Not a shortfall; a unanimous zero

**Numerator 0, denominator 17.** Across every operator, both coasts, and every software stack — Navis,
TERMPoint, eModal, WordPress, bespoke Angular — **not one terminal exposes APPOINTMENT AVAILABILITY
anonymously.**

And the pattern in what they *do* publish is the finding:

| What terminals publish anonymously | Count of 17 |
|---|---|
| **(a) Appointment availability by shift** — *what carriers actually demand* | **0** |
| (b) Gate / yard status, turn times, cameras | 3 (TTI, NWSA, gate cams) |
| (c) Empty-return restrictions | 2 fully server-rendered (ITS — shift-granular; PNCT) |

> ### **★ THE BOOKING-INVENTORY LAW — (b) and (c) are MARKETING for the terminal; (a) IS THE BOOKING ENGINE'S REMAINING INVENTORY. An operator will publish how busy it is and what it will accept, and will never publish how many slots are left. The one number the business needed is the one number no booking system on earth gives away.**

**The exact endpoint the product needed was found, and it is locked.** Pulled from eModal's Angular bundle
(`ecp2.emodal.com/main.*.js`, 5.159.907 bytes):
`GET datahub.visibility.emodal.com/datahub/api/container/availabilityslots?SellerScacCd={scac}&DateFrom=…` —
whose own export routine writes a sheet named **`empty_Appointment_Availability`** with columns *Date ·
Terminal · Size Type · Available Appointments*. **Precisely the archive product.** Anonymous call: **HTTP 401.**
Even `/shippinglines`, the reference list, is **401**. Fenix's `/Appointment-Services/api/appointment/
availability`: **403**. `SellerScacCd` confirms access is scoped to a registered carrier entity.

---

## 2. ★★ KILL TWO — THE EVIDENCE IS THE CLAIMANT'S OWN CONDUCT, and this is the deeper one

**Even with perfect access, the archive is not the artefact the buyer must submit.** OEC Group's dispute policy
(fetched, 849.789 bytes) confirms the timing premise exactly — and then requires something else:

> *"A screenshot from at least one day prior to the dispute date, **between 6:00 AM and 12:00 PM (noon)**. A
> screenshot from **between 6:00 AM and 9:00 AM on the dispute date**…"*
>
> *"**Screenshots indicating the date and time when YOU ATTEMPTED to schedule appointments.**"*
> *"Screenshots of any communication with the terminal/rail regarding appointment issues before the Last Free
> Day."*

> ### **★★ THE CLAIMANT-EVIDENCE LAW — when a dispute policy demands evidence, ASK WHOSE. World-state evidence ("slots were scarce") is corroboration nobody asked for. Claimant-conduct evidence ("I, holding THIS container, tried and was refused") is the actual requirement — and it is account-specific, container-specific, and exists only inside the claimant's own logged-in session.**
>
> **A third party can only ever sell the corroboration. And the one artefact she could legally build is the one the buyer cannot submit.**

**This inverts `THE CONTEMPORANEOUS-EVIDENCE RULE` rather than satisfying it.** The rule was right that a
specified-time observation is the thing worth selling; it was silent on *whose observation*, and that silence
is where the candidate died. **The rule now carries the WHOSE test.**

**And the terminals disclaim the cause anyway.** TTI's own D&D page: *"TTI will not be responsible for delays
for reasons such as… Chassis shortages, Container holds, **Traffic congestion**, Weather-related."* When TTI
does take a dispute it asks for **"appointment number, slot start date and time"** — **proof you HAD an
appointment, the exact inverse of the product.** ITS's dispute form has **no screenshot field at all** and
covers only its own dwell fee.

---

## 3. KILL THREE — the terms of use ban the product by name, three times

eModal is now Advent Intermodal / **CargoSprint**, whose Terms of Use (162.938 bytes) prohibit:

> *"…**scraping, bots, crawlers, data mining**… will not commercialize, copy, modify, **aggregate**, adapt,
> translate, reverse engineer, **harvest**… any portion of the Services other than as expressly permitted"*

**Scraping it, aggregating it, and commercialising it — each named.** This is a **contract prohibition, not a
robots.txt convention**: robots.txt has no direct legal force, an accepted ToS does. And TraPac routes
programmatic access through **emailing a named person** — `THE ONBOARDING LAW`, on the supply side.

---

## 4. AGAINST THIS FILE'S OWN LAWS — it was foreseeable

| Law | How it applied |
|---|---|
| **THE FREE-VALIDATOR SCREEN** | The body that defines the appointment owns the availability data and gives it free **to its registered users** — structural, not accidental |
| **C4** | Container-specific evidence exists only inside the customer's logged-in session. **Unavoidable violation** |
| **C1 / THE ONBOARDING LAW** | TraPac's API needs an email negotiation with a named person; eModal needs a registered carrier with a SCAC |
| **THE POST-ONLY TEST** | **Inverted.** The data's inaccessibility to crawlers was read as her moat. **It was her wall.** A thing crawlers cannot reach is a thing SHE cannot reach |

> ### **★ THE POST-ONLY TEST NEEDS ITS CONVERSE STATED: un-crawlable protects an archive you can BUILD. Before celebrating that no competitor can capture it, confirm that YOU can. Inaccessibility is symmetric.**

---

## 5. WHAT SURVIVES

**The shape of the reasoning, and four laws** — the booking-inventory law, the claimant-evidence law, the
count-is-not-a-check rule, and the converse of the post-only test. **Plus one live observation worth keeping:**
**ITS Long Beach publishes empty-return restrictions server-rendered and SHIFT-GRANULAR, and PNCT publishes
them fully server-rendered with no "Loading…".** Empty-return restriction *is* a named ground of relief under
46 CFR 545.5(c)(2)(ii). **That is a different, smaller candidate on two terminals — not a business, but the
only unburned thing in the wreckage.**

**Day 0 of the archive was committed this morning before the kill landed.** It cost seconds and it was the
right call under uncertainty; it is now a dated record of twelve pages that nobody needs. **The cost of
starting early was correctly near zero, which is the whole reason the rule says to start early.**

## 6. UNVERIFIED

Everport, WUT, Oakland OICT, PierPass TOS, several `*.emodal.com` hosts and Husky all failed on **egress from
this container (502 CONNECT / TLS mismatch) — that is not evidence of gating and must not be read as a kill.**
Port Liberty's subpages threw HTTP/2 errors, though its `Disallow: /` is verified. US container-volume share of
the tested set was never computed. Whether any *ocean carrier* (as opposed to OEC Group, an NVOCC) would accept
third-party archive evidence is **UNVERIFIED** — MSC, CMA CGM and APL all bot-blocked the check.

**But even granting every unverified host were wide open, four or five terminals cannot support a product whose
disputes span whichever terminal the container happened to sit at — and kill two applies at all of them.**

---

# SECOND RED TEAM — independent confirmation, and it is worse

**A separate agent attacked the buyer side without seeing the access findings. It killed the idea again, on
four further grounds, and produced the sharpest law of the day.**

## ★★ THE SUBSET LAW — the deepest kill, and it holds at any price

> ### **Before selling evidence, ask: DOES THE ACT OF PRODUCING THE EVIDENCE THE BUYER IS REQUIRED TO PRODUCE ALSO PRODUCE MINE? Where the buyer's mandatory artefact contains hers as a by-product, the archive has ZERO marginal value at any price.**

**Sharper than `THE FREE FRONT DOOR`: here the free supplier is not a competitor at all — it is the customer's
own compliance obligation.** The buyer must screenshot their own appointment attempts. That screenshot contains
the world-state inside the same image. **Her archive is never the marginal document; it is a duplicate of one
the buyer already had to make.**

## ★ THE IDENTITY REQUIREMENT — amending `THE CONTEMPORANEOUS-EVIDENCE RULE` a second time

**A timing requirement makes evidence unmanufacturable; an IDENTITY requirement makes it unsellable.** Every
major carrier names the subject of the required act:

| Carrier | The clause |
|---|---|
| **ONE** | *"the credible evidence must include **all** of the following"* → *"Screenshot(s) with the date and time **these attempts were made**"* — conjunctive |
| **MSC** | *"time-stamped screenshots **from the terminal appointment system**"*, which must show the *"**specific container number**"* and *"current date and time displayed at the **bottom-right corner of the screen**"* |
| **Maersk** | *"An e-mail to Maersk's equipment team… **must be sent prior to the first day being requested**"* — unmanufacturable by anyone but the buyer |
| **Hapag-Lloyd** D07(3)(d) | *"a statement from the motor carrier that it **attempted in good faith**"* |
| **APL / CMA CGM** | *"the billed party was unable to secure an appointment"* + the same good-faith statement |

**And a third screen to add: does the policy say the ADJUDICATOR keeps its own reports of the same fact?**
Hapag-Lloyd D06(6)(b) and APL both do — *"**Reports maintained by [the carrier] that appointments were
reasonably available** on the date/time in question."* **Third-party evidence of a fact the judge already
records itself is never decisive.** `THE CONTEMPORANEOUS-EVIDENCE RULE` assumed nobody else was watching. Two
parties were, and one of them decides the case.

## ★ "RELIABLE THIRD-PARTY VENDOR" IS A RECOGNITION TEST, NOT A CORRECTNESS TEST

Hapag-Lloyd and APL use identical words: third-party screenshots are accepted only where *"**the third-party
website is in widespread use and is generally recognized as reliable and accurate**."*

> **A new archive run by an anonymous entity fails that on day one BY CONSTRUCTION — and C2 forbids the
> brand-building that is the only cure. This is the EXPERT VETO in a new costume: not that she must be believed,
> but that her ARCHIVE must be.** No cryptographic hashing fixes it; no carrier policy contains any concept of a
> hash. What they specify is a human's desktop screenshot showing the OS taskbar clock.

## ★ THE PRODUCT HAS EXISTED SINCE 2018, PRICED AND PUBLISHED

**BlueCargo** ([bluecargo.io/pricing](https://www.bluecargo.io/pricing)) — **Pro from US$18.126/year**:
*"Terminal schedules and **appointment availability** for 23 steamship lines and **67 port terminals**"* ·
*"Start at $120,000 in per diem disputes per year **with 2 years of backup documentation**."*
**Free tier: 4 terminals, 23 lines, 5 users.** Home page: *"**the industry's only audit record with timestamped
documentation**"*, *"neutral party real-world port events and evidences"*, *"95% Dispute Success."* Distributed
inside **Trinium TMS via the CargoWise Landside partnership.**

**`THE FREE FRONT DOOR` and `THE MONITORING PINCER` on one published page** — free below, $1.510/month above,
and every incumbent gated behind "book a demo." **She would be the one unable to back-fill: BlueCargo has been
accumulating since 2018 and sells the history.**

And the TMS vendors get it as a by-product — PortPro's *"Automated Terminal Appointments"* polls availability
continuously in order to auto-book. **Anyone logged in to book already holds the history free.**

## ★ THE MONEY — "one alert pays for a year" is FALSE, now measured

**Maersk US import tariffs, own PDFs, effective 20 Jun 2026:** detention **$210/day** (d5–8), **$260** (d9–12),
**$290** (d13+); demurrage **$300/day** (d5–8), **$345** (d9–13), **$395** (d14+). **Port of LA Tariff No. 4
wharf demurrage: $13,33/day (20'), $26,66 (40').**

**A container's typical chargeable exposure is 2–5 days = US$420–1.975. Her $650/month is $7.800/year, needing
20–26 chargeable container-days to cover.** That is a book of disputes, not one alert — **and the buyer with
that book is exactly BlueCargo's Pro customer.**

**FMC FY2024 Annual Report (primary):** *"the FMC received **189 charge complaints**… **Eighty-one of those
charges, valued at $1.001.350, were voluntarily refunded or cancelled**… The total amount refunded or cancelled
during FY 2024 was **$1.874.142**."* Plus *"**18 small claims cases**."* **Nationwide, all carriers, all charge
types.** *(Total US D&D billed and disputed: **UNVERIFIED**, no primary source.)*

## ★ THE RULE WAS FINE. THAT IS THE POINT.

**46 CFR part 541 is in force** — final rule 23 Feb 2024, effective 28 May 2024. *World Shipping Council v. FMC*
(D.C. Cir., 23 Sept 2025) set aside **only §541.4**; per the FMC's own article, *"apart from section 541.4, the
rest of the Rule remains in effect."* **545.5 intact.** So 541.5, 541.6(e)(2) and 541.8(a) — every provision the
pitch leaned on — are good law.

> **The regulatory tailwind was real and it rescued nothing.** Worth remembering the next time a candidate is
> argued from a statute: **a favourable rule is not a business.**

## ★ AND SHE CANNOT GET THE LOGIN EVEN IF SHE WANTED TO

eModal's own instruction sheet: ***"You must have a valid SCAC and either an MCP or USDOT number."*** Approval
takes 2–3 business days and support *"will reply… or **contact you by phone**."* **She has no US motor carrier
authority, no USDOT, no MCP, no SCAC.** And a capture from *her* account would show neither the customer's
container number nor the customer's attempts.

## THE BUYER WAS NEVER REACHABLE EITHER

**Freight audit & payment firms are not a register** — no public list; the US ocean-relevant set is low tens
(Trax, nVision Global, CTSI-Global, Cass, Data2Logistics, Intelligent Audit, CT Logistics, enVista, A3, Ocean
Audit). **Selling 18–20 subscriptions into a 20–40 firm population is ~50% market penetration, by cold email,
from an anonymous foreign entity, with no call, ever. That is not a target, it is a wish.**
