# STATE OF PLAY — 19 Aug 2026, end of the four-hunt day

> ## ⚠ CORRECTED SAME DAY — read `THE_ERASURE_CENSUS.md` §4 before acting on §1–2 below.
>
> A sixth hunt landed after this was written and qualified two claims made here:
>
> **1. "The change-log cannot be back-filled" is TOO STRONG.** No vendor holds the DECRS *series*, but a 2020
> point-in-time snapshot is publicly purchasable from John Snow Labs. **Net change over six years is
> back-fillable by anyone; only the ORDER AND DATES of the changes are not.**
>
> **2. DECRS has NO structural archive protection.** It fails the POST-only test — a static `.zip` at a stable
> URL by plain GET is the most crawlable shape there is. **And I could not check whether it has been crawled:
> `web.archive.org` was egress-blocked from this container all day, both routes. ARCHIVE RISK IS UNVERIFIED,
> and it is the question that decides whether the archive below is worth anything.**
>
> Day 0 still cost nothing and is still worth having. It is now explicitly contingent.

**Six structural hunts ran in parallel against four different patterns. None was told about the others.
Reading them together is where the value is.**

---

## 1. ★★ THE CONVERGENCE NOBODY PLANNED

**Three of the four hunts independently arrived at the same file: the FDA Drug Establishments Current
Registration Site (DECRS), `https://www.accessdata.fda.gov/cder/drls_reg.zip`.** The fee-gate hunt found it
looking for solvency. The dangling-reference hunt found it looking for declaration/registry pairs. The erasure
hunt was already pointed near it. **I then downloaded and parsed it myself rather than take any of them on
report.**

**Measured directly, 19 Aug 2026** *(SHA-256 `48ad8def…1aa0a0`)*:

| | |
|---|---|
| Rows / **unique FEI** | 10.414 / **9.837** |
| `ESTABLISHMENT_CONTACT_EMAIL` | **100,00%** |
| `REGISTRANT_CONTACT_EMAIL` | **100,00%** |
| The two differ (⇒ a **second** named human) | **43,7% of rows** |
| `AGENT_DETAILS` (DUNS · name · **email** · phone) | 45,75% |
| `EXPIRATION_DATE` | **12/31/2026 on all 10.414** — one shared statutory calendar |
| `drls_excluded.txt` | **20 rows, and NAMED** — FEI, DUNS, firm name, address |
| Largest US agent | Registrar Corp, **418** *(a hunt report said 427; 418 is today's count)* |

### Why this is not just another register

**`THE_FDA_TEST.md` killed the FDA *device* candidate on four sufficient causes. The first — and the one that
generalised into `THE NAMEABILITY CONDITION` — was that the vanished records were anonymous integers: 0 of
3.528 absent manufacturer keys appeared in any name-bearing table.**

> **DECRS does not have that defect. Firm name, address and two working emails sit on the same row as the
> identifier, and even the exclusion file is named. The cause of death that closed the device candidate does
> not transpose to the drug register.**

**This is a RE-TEST, not a candidate, and it must not be treated as one.** Three of the other four kill causes
are untested here, in this order of cheapness:

1. **Does anything actually vanish?** The device declaration table was **append-only** (82 added, 0 removed in
   14 days). **Unmeasurable from a single snapshot — so the clock was started today** (§2).
2. **"You cannot sell a firm a monitor for its own outbox."** DECRS has **1.666 distinct US agents and the
   agent IS the filer.** This killed both the device candidate and its pivot. **Check it before anything else.**
3. **Is the buyer legally compelled to run this check already?** 21 CFR 807.22(b)(3) compelled it on the device
   side, inside FURLS. Unknown for drug establishments.
4. **The gate is real but not universal** — §510 registration is free; the five- and six-figure GDUFA/OMUFA
   facility fees hit generic and OTC-monograph facilities only.

---

## 2. ★ WHAT WAS ACTUALLY DONE, NOT DESCRIBED

`archive/decrs/2026-08-19.tsv.gz` (882.288 bytes) + `MANIFEST_2026-08-19.json` with both files' SHA-256, row
counts and measured fill rates. **Day 0 of a change-log the agency will never publish.**

**Per `THE STATE KEEPS STATE, NOT HISTORY`: no model, agent or budget back-fills a day that was not recorded.
It cost nothing and it is the one action of the day that cannot be taken later.** *(Operationally the archive
belongs on object storage, not git — 1 MB/day is 365 MB/year. Day 0 is committed to make it real.)*

---

## 3. THE LAWS THE DAY PRODUCED — ranked by how much they change the search

1. **★★ THE KNOWLEDGE-LIABILITY TEST** — *"when this finds something, does the buyer get money, or a problem?"*
   **This is the most useful screen added in weeks** and it kills or wounds a whole family of detection
   products that pass every other filter. It also puts the machine-verifiable hunt's own lead candidate on the
   wrong side of itself.
2. **★ THE FREE-VALIDATOR SCREEN** — the body that defines a standard publishes the free test, by design.
   **Sell where the CHECK is free but the RULE is scattered.**
3. **★ THE GATE/CONTACT ANTI-CORRELATION** — screen email first, gate second. Inverts how three hunts were
   briefed. Plus `THE POSTAL LIST LAW`'s second bound: **per-register, not national.**
4. **★ THE SEPARATION LAW** — the referral structure that makes maintenance windows beautiful is a property of
   **capital intensity**, not of maintenance. Only a **statutory independence rule** substitutes.
5. **★ A 30% dangle rate is more likely a schema misreading than a finding** — net against the register that
   records the cure. *(Two live demonstrations in one day; the same failure mode as my FDA join.)*
6. **★ THE BUILDABILITY THRESHOLD** — commoditised capability **admits**, never **defends**, and buys ~one
   quarter.

---

## 4. WHAT IS LIVE, WHAT IS WOUNDED, WHAT IS DEAD

**LIVE, needing a cheap test before any build:**
- **DECRS re-test** — questions 2 and 3 above. Cost: reading two CFR parts and one join. **Do this first.**
- **UK NMW recomputation as a licensed engine** — architecture is genuinely clean (**runs on the customer's
  machine, the payroll file never crosses a border, C4 and GDPR both solved by architecture**), exposure is
  primary-sourced at ~£51.000 per named employer, and the incumbent documents its own gaps. **Blocked on the
  knowledge-liability question. Test: 40 emails, one question, ~2 hours.**
- **Cutover reconciliation pack, one corridor, sold wholesale** — every constraint clean, date volunteered.
  **Blocked on price (no observed instance) and on having no separator. Test: 30 emails, ~4 hours.**
- **PCAOB Rule 2107(h) clock-start** — a cohort of audit firms deemed withdrawn **"beginning in the fall of
  2026."** A genuine clock-start, which `THE_DATASET_HUNT` says is the only level moment. **Dies on the last
  mile: 243 columns of Form ADV and no email.** Held for the parts bin.

**WOUNDED:** carrier invoice recomputation (free audits everywhere) · commission reconciliation (occupied) ·
Brazilian counterparty screening (her Portuguese is no longer a moat — `THE_CAPABILITY_ANSWER` records
translation as a loss).

**DEAD today, with causes recorded:** EUDAMED/NANDO (voluntary declaration table) · ASIC reps (the register
closes its own loop) · ATO SMSF (the authority runs the join itself) · FCC equipment authorisations
(append-only + a table last refreshed March 2021) · charity trustees vs disqualified directors (**no key, and
a false positive here is defamatory-adjacent**) · EUDR plot validation (identical product, free tier) · FBA
reimbursement (Amazon automated it away in Nov 2024) · eCTD (8–20 h/sequence) · every e-invoicing pre-flight
(free official validators) · SDS libraries · CDISC conformance · merchant-statement recomputation.

---

## 5. ONE HONEST CAVEAT, FLAGGED LOUDLY

**The single best distribution number produced today — Pay.UK's *Directory of Bacs Approved Bureaux*, 459
organisations with 401 publishing email = 87,4% — I COULD NOT REPRODUCE.** `wearepay.uk` returned 403 to a
direct request and 404 through the fetch tool. **It is recorded as reported, not verified.**

**Three fabricated or mis-joined numbers have been caught in this file, two of them mine.** That count is
load-bearing for an entire candidate and it is a five-minute job for a human with a browser. **Do not build on
it until someone has.**

---

## 6. THE THING THAT DID NOT CHANGE

**Nothing today produced a buyer.** Four hunts, sixty-odd instances, eleven registers field-inspected, and the
binding constraint is what it has been for seventy-two candidates: **demand.** Every live candidate above is
blocked on the same class of question — *will anyone pay for this* — and every one of them has a test that
costs under four hours, no phone and no capital. **Those tests are the work, not more hunting.**
