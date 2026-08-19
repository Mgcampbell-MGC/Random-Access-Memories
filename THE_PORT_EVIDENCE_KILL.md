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
