# S3 — CONTINUOUS OPERATION: 17 instances, one survivor, four laws

**The shape: the product IS that something was watched, without interruption. Not a document, not software — an
unbroken dated series. A competitor starting tomorrow cannot sell ninety days of history tomorrow.**

---

## 1. ★★ THE SHAPE FINDING — S3 is the first shape whose arithmetic works by construction

> **One cron produces one archive; the same archive serves every subscriber; marginal human hours per
> subscriber per month is genuinely ZERO for every candidate below. NOT ONE S3 CANDIDATE DIED ON ECONOMICS.
> All seventeen died on distribution, occupancy, or the free front door.**
>
> **S3 removes the production ceiling and changes nothing about demand.** *(Which is the same sentence this file
> has now written about capability, about buildability, and about six parallel hunts. The binding constraint has
> never once been supply.)*

At **US$650/month** the target is **18 subscribers**; at $300, **37**. That is not the problem and never was.

---

## 2. ★★ THE LAW WORTH KEEPING — THE CONTEMPORANEOUS-EVIDENCE RULE

> ### **A dated series is only THE PRODUCT where a counterparty's own published policy requires an observation MADE AT A SPECIFIED TIME ON A SPECIFIED DAY. Everywhere else the series is a nice-to-have and prices like one.**
>
> ### **So: DO NOT HUNT REGISTERS. HUNT PUBLISHED DISPUTE AND CLAIMS POLICIES.**
>
> A register tells you what is true now. **A dispute policy tells you what evidence someone will pay for, and
> when it had to be taken.** That timing requirement is the only thing found in this hunt that makes *"I was
> watching and you were not"* a purchase rather than a preference — because it makes the evidence **impossible
> to manufacture after the fact, by anyone, at any price.**

---

## 3. ★ THE SURVIVOR — THE APPOINTMENT-UNAVAILABILITY EVIDENCE ARCHIVE

**What is watched.** For every US container terminal, twice every working day, in the windows the ocean carriers
themselves specify: whether any truck appointment slots exist, per shift. Captured as screenshot + machine-
readable row + SHA-256, written to object storage. **Nothing is interpreted and nothing is asserted.**

**The requirement is published by the party who will pay to see it satisfied.**
[Ocean Network Express's own dispute page](https://us.one-line.com/invoice-disputes-landing-page) requires
evidence including *"Screenshot(s) regarding appointment availability (including relevant dates and times)…"*,
taken *"(1) …between 6:00 a.m. and 12:00 p.m. (noon) the day prior to the Waiver date and (2) …between 6:00 a.m.
and 9:00 a.m. on the Waiver date"*, and *"For terminals operating on a two-shift basis… screenshots must capture
appointment unavailability for both shifts."*

**The statutory teeth, from the eCFR not a blog:**
- **46 CFR 545.5(c)(2)(ii)** — detention imposed *"when empty containers cannot be returned"* is *"likely to be
  found unreasonable."*
- **46 CFR 541.6(e)(2)** — every D&D invoice must certify that *"The billing party's performance did not cause
  or contribute to the underlying invoiced charges."*
- **46 CFR 541.5** — *"Failure to include any of the required minimum information… eliminates any obligation of
  the billed party to pay the applicable charge."*
- **46 CFR 541.8(a)** — at least **30 calendar days** from invoice issuance to request mitigation or waiver.
  **Independently confirmed on a terminal's own public page today:** Yusen Terminals' *Demurrage Dispute
  Process* — *"All requests for mitigation, refund, or waiver… must be submitted within thirty (30) calendar
  days from the invoice issuance."*

**Why it cannot be bought free.** Appointment availability is not a file, a register or a page — **it is
transient UI state inside a terminal operating system. There is nothing to crawl.** Unlike a `.zip` at a stable
URL (no structural protection at all), and unlike Health Canada's MDEL, it does not die on the contact wall.

**Every constraint clears.** C1: cold email → landing page → Wise invoice → cron → emailed pack; **no call
anywhere, and no setup call either, because there is no supplier to onboard with.** C4: **the customer sends
nothing and grants nothing** — they name a terminal and a date range. **KNOWLEDGE-LIABILITY: the finding hands
the buyer MONEY — a waived charge — never a duty to self-report.** Right side of the sharpest screen in the file.

**Sell it wholesale**, per `THE WHOLESALE ESCAPE`: not to 300 importers but to **demurrage-and-detention audit
firms, freight-bill audit firms and drayage TMS vendors**, whose revenue is a percentage of recoveries — so one
archive lifts the recovery rate across their whole book. **Twenty at $650 is the target.**

### ★ WHAT I MEASURED TODAY — partial, and it cuts the right way

The hunt's container could not reach a single terminal; every probe failed on egress. **From here, several did:**

| | |
|---|---|
| `emodal.com`, `fenixmarineservices.com`, `apmterminals.com/en/los-angeles`, `yti.com` | **HTTP 200** |
| `termpoint.emodal.com`, `tos.pierpasslb.org`, `everport.us` | 502 CONNECT tunnel failed |
| **TraPac LA `/real-time-yard-status/`** | **HTTP 200, 83.829 bytes, and it contains a real HTML `<table>` of data rendered server-side via DataTables — no login** |
| **TraPac's own URL scheme** | gated pages sit under **`/authenticated-transactions/`** (empty-yard-recap, gate-activity) — **so the pages outside it are, by the site's own structure, public** |

> **This is encouraging and it is NOT the answer.** *Real-time yard status* is not the same artefact as
> *appointment availability by shift*, and one terminal is not twenty. **The load-bearing fact remains
> UNVERIFIED.**

### The honest reasons it would fail, in order

1. **ACCESS — the whole thing.** ONE allows a screenshot from *"a reliable third-party vendor website **and/or**
   applicable terminal operating system"*, but Fenix and TraPac name their own portals, which normally gate on a
   trucking entity with a SCAC. **If she must register, she is inside someone's terms of service — which per
   `THE_DATASET_HUNT` is the real barrier, not the CFAA.**
2. **★ THE EVIDENCE-OF-CONDUCT SPLIT.** ONE also requires screenshots showing *"the date and time these attempts
   were made to secure appointments"* — **a fact about the disputing party's own conduct, which no third-party
   archive can ever supply. She can sell the state of the world; she can never sell proof that the customer
   tried.** So the pack is at best half an evidence file. *(MSC's wording is pure world-state and survives this;
   ONE's does not. MSC's page **403'd** — the wording is from a search excerpt, **UNVERIFIED**.)*
3. **Would a carrier accept a stranger's capture?** *"Reliable third-party vendor"* in context probably means
   the appointment-data vendor. Not the expert veto exactly — but **her ARCHIVE must be believed as reliable.**
4. **Buyer channel half-verified.** FMCSA gives ~75% email but does not flag who does drayage; the FMC OTI list
   is an ASP.NET search form with no bulk download and no evidence of an email column — **the twelfth time this
   file has hit that wall.**
5. **The per-diem demurrage rate was never fetched, so "one alert pays for a year" is ARGUED, NOT MEASURED.**

---

## 4. ★★ THREE MORE LAWS — each one a cheap test that kills a moat claim

> ### **★ THE DATE-STAMPED FILENAME IS A BACK-FILL INVITATION.**
> The hunt's second-best candidate — an archive of carriers' empty-return bulletins — looked excellent, then
> died on its own URL pattern. **`evergreen-shipping.us/Return_Location_LA_20240830.pdf` returns HTTP 200 and
> 609.976 bytes today** — a live PDF from 30 August 2024. **A competitor brute-forces the date space in an hour
> and owns the whole back series.**
> **Test before claiming any erasure moat: guess three superseded dates in the publisher's own naming
> convention and see whether the bytes come back.** Sixty seconds. *(Siscomex went the other way — every
> superseded date 404s.)*

> ### **★ THE REGULATOR-MANDATED ARCHIVE — the sibling of `THE FREE-VALIDATOR SCREEN`.**
> **46 CFR 520.10(a)**: carriers *"must keep the data that appeared in their tariff publication systems for a
> period of 5 years… and must provide online access to such data for 2 years."* **520.10(b)** even mandates the
> interface: *"the capability for a retriever to enter an access date… so that only data in effect on that date
> would be directly retrievable."* **520.9(c)(2)**: *"must provide free access."*
> **Where a regulator governs a disclosure, check whether it has also ordered the HISTORY retained and given
> away — for the same reason a standards body ships a free validator: it wants disputes resolvable.
> Free-to-read is not the screen. FREE-TO-READ-AS-OF-A-PAST-DATE is.**

> ### **★ THE PUBLISHER SHIPS THE DELTA — look for a `/daily/` directory before assuming erasure.**
> `data.fcc.gov/download/pub/uls/daily/` serves per-weekday transaction zips alongside `/complete/`. The FCC
> publishes its own change-log. Same kill on ClinicalTrials.gov: `/api/int/studies/NCT…/history` returns the
> full version history free.

---

## 5. THE CENSUS — causes of death

| Killed | Cause |
|---|---|
| Carriers' empty-return bulletins | **Date-stamped filenames** (above) |
| Carrier tariff as-of-date archive | **46 CFR 520.10 — the regulator mandated the archive and made it free** |
| FCC ULS change monitoring | **The publisher ships the daily deltas** |
| ClinicalTrials.gov silent protocol changes | **Free version-history API** |
| FMCSA authority/insurance monitoring | **Pincer — Carrier411 at US$34,95/mo** *(their page 403'd; **UNVERIFIED**)* |
| INPI RPI trademark deadlines (BR) | **Pincer — Velador at R$0 / R$19,90** |
| Court dockets · tenders · grants | CourtListener free · Stotles £0 · **HigherGov $500/YEAR** |
| US healthcare exclusion screening | **Exclusion Screening $40/mo per 100** |
| Retail price / buy-box / availability | Occupied; **Prisync $799 is the ceiling** and the big vendors hide price |
| Container milestones / last-free-day | **Terminal49 free tier, and Lite/Essential/Complete publish NO price** — the pincer with both jaws visible on one page |
| Health Canada MDEL delistings | Moat real, **zero emails** — `THE POSTAL LIST LAW` |
| Any UK public-body register | **`THE UKGWA LAW`** |
| Brazilian certidão monitoring via accountants | **`THE R$1.200 CEILING`** — whole-service plans observed at R$159–329/mo |
| MDR post-market surveillance logs | Expert veto + `THE ONBOARDING LAW` + **knowledge-liability: a trend finding creates an MDR Art. 88 reporting duty, so the buyer wants a log that finds nothing** |
| EU261 flight-rotation evidence | **Probable kill, UNVERIFIED** — ADS-B history archives appear to exist under ODbL but both hosts 403'd |

**★ The one WOUNDED survivor — the Brazilian tariff-quota burn-down series.** `2026.08.15_Tabeladeacompanhamento
dascotasdeimportao.ods` on gov.br/siscomex, parsed: 170 rows of NCM · cota concedida · cota consumida ·
percentual. **Erasure measured: superseded editions 404 (26 bytes).** And uniquely, **the government names the
buyers** — `2026_parcelaproporcionaltrigo.pdf` lists the contemplated firms with **CNPJ raiz**, which joins
straight into the CNPJ open data at ~76% email. **Wounded because:** Siscomex's own *Controlador de Cotas* gives
every logged-in importer the live balance free (only the RATE is scarce); the buyer set per quota is **five to
twenty named giants** with comex departments, which is not a cold-email business; and Logcomex is incumbent.

---

## 6. THE TEST — and it is the only kind worth running for S3

> **Take the top 20 US container terminals by volume. From a clean anonymous session — no login, no
> registration — try to reach appointment availability by shift. Twice a day for ten working days, in ONE's
> windows (06:00–12:00 and 06:00–09:00 local). Count: of 20 terminals, how many were readable anonymously on at
> least 18 of 20 slots?**
>
> **Fewer than ~12 ⇒ the product cannot be built. Stop.**
> **12 or more ⇒ the moat is real from that day forward — AND THE TEN DAYS OF CAPTURES ARE ALREADY THE FIRST TEN
> DAYS OF THE ASSET. The test and the build are the same act**, which is the only kind of test worth running
> here, because every day the cron is not running is a day of moat that can never be recovered.

**Then, ~3 hours and still no phone:** email thirty US drayage carriers and customs brokers — *"When you dispute
a D&D invoice on 'no appointments available', who takes the twice-daily screenshots, and how many disputes did
you drop last year because nobody had taken them?"* — **and count the answers containing a number.**

---

## 7. UNVERIFIED

Whether ANY terminal exposes appointment availability anonymously *(the load-bearing fact; TraPac's yard-status
page is public and tabular, which is adjacent evidence, not the answer)* · MSC's screenshot wording (403) ·
Carrier411's price (403) · per-diem demurrage rates at any terminal (never fetched) · whether the FMC OTI list
has email or a bulk file · CBP broker list and UIIA (403) · archive risk for the Siscomex quota files
(`web.archive.org` reset, `archive.org` 429 — **the same block that defeated the erasure census**) · ADS-B open
archives (403) · Terminal49's paid prices (**their page shows no figures at all, which is itself the finding**) ·
whether any vendor already sells an appointment-evidence archive (**two searches found none — absence of a
search hit is not absence of a product, and is equally consistent with the thing being unbuildable**).
