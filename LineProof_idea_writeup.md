# Collision repair: two versions of one idea

*Written up to hand to someone with real collision-industry knowledge. Every figure marked
VERIFIED was checked directly on 7 Aug 2026 — the URLs are included so you can re-run them.*

---

## The problem

Modern cars are full of radar, cameras and sonar. When a body shop removes a bumper or replaces a
windscreen, some of those systems may need research, calibration and documentation.

Two things go wrong constantly:

1. **The shop doesn't reliably know what's on the specific car.** Trim levels differ. One 2024
   Accord has blind-spot intervention standard and blind-spot monitoring only as an option — and
   there is a trim literally designated *"w/Out BSI."*
2. **The shop can't prove what it did.** Scan reports, calibration invoices, OEM research, customer
   authorisation and photos exist in five different places and never get connected to the estimate
   line or to what was actually paid.

The second problem is why shops eat work they performed, and why some bill work they can't
evidence.

---

## Version A — the small one: an ADAS Trigger Reference

**What it is:** a downloadable folder — a pre-decoded reference of which ADAS systems are present by
year/make/model/trim, plus an instruction file that makes the shop's own ChatGPT or Claude answer:
*"this vehicle has forward radar and a rear camera, so removing the front bumper triggers a research
requirement on these systems — here is the record to fill in, here is the evidence checklist."*

**Why it works:** NHTSA's vPIC API publishes this data free, as US government work (public domain,
so it can be redistributed commercially).

**VERIFIED, fetched directly:**
`https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{VIN}?format=json&modelyear=2024`
returns **154 fields**, of which **19 are ADAS-related**. For a 2024 Honda Accord, **14 were
populated**: AdaptiveCruiseControl `Standard`, BlindSpotIntervention `Standard`, BlindSpotMon
`Optional`, ForwardCollisionWarning `Standard`, LaneDepartureWarning `Standard`, LaneKeepSystem
`Standard`, ParkAssist `Standard`, PedestrianAutomaticEmergencyBraking `Standard`,
RearAutomaticEmergencyBraking `Standard`, plus TPMS, ABS, ESC and headlamp type. Trim returned as
*"Sport Hybrid, Sport Hybrid w/Out BSI."*

**What it deliberately does NOT do** — and this is what keeps it shippable and legal:

- **No OEM repair procedures.** Those are manufacturer copyright and cannot be redistributed.
- **Never says a calibration is required.** That is vehicle-specific OEM territory. It says only
  *what is on the car*, so the estimator's research is directed rather than guessed.
- **Says nothing about billing, and never mentions insurers.**

**Price:** roughly $149–297. It's a reference, not a service. One person can sell it with no
employees, no installation calls and no support burden.

### The honest weaknesses

- **It's one link, not the chain.** Knowing the car has radar doesn't give you the procedure.
- **vPIC coverage varies.** It's manufacturer-submitted Part 565 data. A 2011 BMW returned **empty**
  ADAS fields. Coverage must be measured by model year before anyone prices this — a reference with
  holes is worse than none in this trade.
- **The API is free and public.** The moat is the pre-decoding, the mapping to repair events, and
  the updates — not the data.
- **Someone may already sell it.** A free ADAS-by-VIN lookup for shops is an obvious product and I
  have not checked. **Check this first, before anything else.**

---

## Version B — the big one: a repair-file proof system

This is the more valuable business, and it needs someone who actually knows the trade.

**What it is:** a $995-per-location system that installs a *proof chain* — every performed operation
connected to its source, the customer's authorisation, the evidence it was done, the estimate line,
and what finally happened to the money (insurer-paid / customer-paid / denied / written off).

Its core insight is worth stating plainly:

> A checklist finds possible omissions. This proves whether each operation was necessary,
> authorised, performed, billed, and paid or absorbed.

The important discipline is what it refuses to claim. It does **not** say an insurer is legally
required to pay, does not guarantee reimbursement, and does not tell a shop to bill for something
because a checklist flagged it. Letters transmit evidence and request a written disposition — they
are not "rebuttal letters." Getting this wrong invites public-adjuster licensing problems, which
vary by state.

**Why it needs a car person:** it requires a working collision estimator's judgement to build the
trigger logic and to strip false positives, plus insurance-regulatory counsel to review the
positioning. It also needs per-shop installation. That is a real business with real people in it —
not a downloadable file.

### Things already established about Version B, worth not relearning

- **The market is smaller than it looks.** State licence databases include duplicates, inactive
  entities, paint-only, glass-only and mobile operators. A credible planning figure is roughly
  **25,000–35,000 relevant collision locations**, of which maybe **8,000–15,000** are the real
  target once chains, dealer groups and micro-shops are excluded.
- **Don't launch at $297.** At that price it reads as a template pack, attracts buyers wanting a
  magic list, and cannot fund expert review or support.
- **Margins are ~55–65%, not 88%.** Acquisition, implementation, support, refunds and legal review
  are real costs.
- **The best distribution channel is independent ADAS calibration vendors.** They already touch
  every shop, already need clean scan and calibration documentation to get paid, and one vendor can
  introduce it to dozens of shops. The pitch to them is *"help your customers produce complete,
  source-backed repair files"* — not *"help your shops fight insurers."*
- **Prove it on closed repair orders before selling widely.** Ten paid pilot shops, ~100 closed
  files, and count only value actually billed and collected — never every flagged line.

### One competitive fact to know upfront

**I-CAR's RTS portal already aggregates OEM position statements by manufacturer, free**, at
`https://rts.i-car.com/oem-information.html` [VERIFIED]. So any plan whose value is "we collected
the position statements" is already served. The value has to be the process and the proof chain, or
the vehicle-specific equipment reference — not a library of documents someone else publishes free.

---

## If I were picking one to explore

**Start with Version A**, because it can be built and tested by one person for almost nothing, and
the data is verified to exist. Check the two things that could kill it — vPIC coverage by model
year, and whether a free ADAS lookup already serves shops — before building anything.

**Version B is the better business but it is a company, not a product.** It needs a collision SME, a
lawyer, and per-shop installation. If you have the trade knowledge, that is the one with real money
in it — and the calibration-vendor channel is how it scales.
