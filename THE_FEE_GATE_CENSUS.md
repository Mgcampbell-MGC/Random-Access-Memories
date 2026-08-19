# SOLVENCY PROVEN BY THE DATASET — census of money-gated public registers, 19 Aug 2026

**The hunt:** find public registers where **every entity on the list has already written a large cheque**, so
solvency is proven by membership rather than assumed. Twelve registers examined; every fee traced to a statute,
a regulation or a Federal Register notice; every count and fill-rate measured on a downloaded file.

**★ The single most useful output is not a candidate. It is a law that inverts the search order.**

---

## 1. ★★ THE FINDING — THE GATE/CONTACT ANTI-CORRELATION

> ### **Money gate and contactability are close to ANTI-CORRELATED. The three biggest gates found publish the least contact data; the one register publishing two working emails per row has the fuzziest gate. SCREEN ON EMAIL FIRST, GATE SECOND — the reverse of how this hunt was briefed.**

| The gate | The contact data |
|---|---|
| **UK Register of Licensed Sponsors** — 127.391 orgs, £574–£1.579 each + £525 per worker | **Five columns. No address, no phone, no email, no company number.** Uncontactable |
| **UKGC** — annual fee £230 → £907.832 by GGY, non-payment ⇒ revocation | **No contact field at all.** Account number and name |
| **NRC** — $325.000 to $5.554.000 per year | No bulk licensee file with contacts |
| **DOL Form 5500** — PBGC premiums, 61.210 filings | **140 columns parsed. Zero email fields** |
| **FDA DECRS** — registration itself is FREE under FD&C §510 | **100% email on TWO fields, plus the agent's email on 45,75%** |

**This is `THE POSTAL LIST LAW` holding for the eleventh and twelfth time, and it now has a stated exception:**

> **The exception is not a country. It is US FEDERAL EXECUTIVE AGENCIES THAT COLLECT EMAIL AS PART OF AN
> ELECTRONIC FILING OBLIGATION.** Three of twelve registers publish email at scale, and all three are US
> federal: **FMCSA 75,2%** (measured, 600-broker random sample), **FCC ULS 75,4%** (44.972/59.613),
> **FDA DECRS 100%**.
>
> *(This sits beside the already-recorded Brazilian exception — Receita Federal CNPJ open data publishes
> `CORREIO ELETRÔNICO`, fill rate still UNVERIFIED and still the cheapest test in the file.)*

**Second law, smaller but load-bearing:**

> ### **A FEE IMPLIES A CALENDAR, AND THE CALENDAR IS IN THE FILE.** `EXPIRATION_DATE` · `REG_EXPIRY_DATE_YEAR` · licence anniversary (UKGC) · 1 September (BLM) · 1 June (OMUFA) · 1 Oct–31 Dec (MDUFA). **Every one is a date the payer does not control — `THE CONSTRAINT-SIDE LAW`'s condition, satisfied by statute rather than by hope.**

---

## 2. ★ FDA DECRS — INDEPENDENTLY RE-MEASURED, 19 Aug 2026

**Not taken on report. Downloaded and parsed directly.** `https://www.accessdata.fda.gov/cder/drls_reg.zip`
(2.398.726 bytes) and `drls_excluded.zip` (5.267 bytes), free, daily, no key, no browser needed.
SHA-256 of the extracted `drls_reg.txt`: `48ad8def6f3057341ffaefec5c72c538c2253441ae69b324784ae97d701aa0a0`.

**14 columns:** `FEI_NUMBER · DUNS_NUMBER · FIRM_NAME · ADDRESS · EXPIRATION_DATE · OPERATIONS ·
ESTABLISHMENT_CONTACT_NAME · ESTABLISHMENT_CONTACT_EMAIL · AGENT_DETAILS · REGISTRANT_NAME · REGISTRANT_DUNS ·
REGISTRANT_CONTACT_NAME · REGISTRANT_CONTACT_EMAIL · EXCLUSION_FLAG`

| Measured today | |
|---|---|
| Rows | **10.414** |
| **Unique FEI** | **9.837** *(so 577 rows are repeat FEIs — not previously reported)* |
| Unique firm names / registrants | 7.736 / 6.758 |
| `ESTABLISHMENT_CONTACT_EMAIL` | **10.414 / 10.414 = 100,00%** |
| `REGISTRANT_CONTACT_EMAIL` | **10.414 / 10.414 = 100,00%** |
| The two emails are the same address | 5.866 = 56,3% — **so 43,7% of rows yield a SECOND distinct human** |
| Distinct establishment emails | 7.404 |
| `AGENT_DETAILS` | 4.764 = 45,75%, formatted `DUNS - agent name - agent email - agent phone` |
| `EXPIRATION_DATE` | **12/31/2026 on all 10.414 — one shared statutory calendar** |
| Largest US agent | **Registrar Corp, 418 establishments** *(the hunt report said 427 — 418 is today's measured count)* |
| **`drls_excluded.txt`** | **20 rows — and NAMED: FEI, DUNS, FIRM_NAME and ADDRESS all populated** |

### ★ Why this matters more than any other line in the census

**`THE_FDA_TEST.md` killed the device-register candidate on four sufficient causes. The first was
`THE NAMEABILITY CONDITION`: *"the vanished record must remain IDENTIFIABLE after it vanishes"* — and it did
not, because 0 of 3.528 absent manufacturer keys appeared in any name-bearing table. The finding was a list of
anonymous integers.**

> **DECRS does not have that defect. `FIRM_NAME`, `ADDRESS` and two working email addresses sit on the same row
> as the identifier, and the exclusion file is named as well. THE CAUSE OF DEATH THAT CLOSED THE DEVICE
> CANDIDATE DOES NOT TRANSPOSE TO THE DRUG REGISTER.**

**This is a RE-TEST, not a candidate.** Three of the other four kill causes are untested here and must be
before anything is built on it:

1. **Does anything actually vanish?** The device declaration table was **append-only** (82 added, 0 removed
   over 14 days). **UNVERIFIED for DECRS — and unmeasurable from one snapshot.** Hence §3 below.
2. **Is the buyer legally compelled to do this check already?** 21 CFR 807.22(b)(3) compelled it on the device
   side, inside FURLS. **UNVERIFIED for drug establishments.**
3. **"You cannot sell a firm a monitor for its own outbox."** DECRS has **1.666 distinct US agents**, and the
   agent *is* the filer. Registrar Corp holds 418. **The same trap is almost certainly present. Check it before
   anything else** — it is the cause that killed both the device candidate *and* its pivot.
4. **The gate is real but NOT universal.** Registration under FD&C §510 is itself free. The five- and six-figure
   facility fees ([GDUFA FY26](https://www.federalregister.gov/documents/2025/07/30/2025-14411/generic-drug-user-fee-rates-for-fiscal-year-2026):
   domestic API $43.549, foreign API $58.549, domestic FDF $238.943, foreign FDF $253.943;
   [OMUFA FY26](https://www.federalregister.gov/documents/2026/03/18/2026-05276/over-the-counter-monograph-drug-facility-fee-rates-for-fiscal-year-2026):
   MDF $19.188, CMO $12.792) hit generic and OTC-monograph facilities — not all 10.414.

**Do not build. Answer 1–3 first, cheaply, in that order — and start 1's clock today, which has been done.**

---

## 3. ★ WHAT WAS ACTUALLY DONE TODAY — day 0 of the change-log

**Per `THE STATE KEEPS STATE, NOT HISTORY`: FDA publishes today's state and never publishes what left. The
change-log is the one artefact the authority will not produce and nobody can back-fill — and no model, agent or
budget recovers a day that was not recorded.**

`archive/decrs/2026-08-19.tsv.gz` (882.288 bytes) + `archive/decrs/MANIFEST_2026-08-19.json`, carrying both
files' SHA-256, the row counts and the measured fill rates. **The clock is started. It cost nothing.**

**Operationally the archive belongs on object storage, not in git** — 1 MB/day is 365 MB/year. Day 0 is
committed here to make the artefact real rather than notional.

---

## 4. THE OTHER TWO WORTH KEEPING

**② FMCSA property brokers — the $75.000 bond ([49 CFR 387.307](https://www.law.cornell.edu/cfr/text/49/387.307)).**
25.081 entities hold **ACTIVE** broker authority (91.652 inactive). Free bulk: L&I "Carrier — All With History"
(`u4i8-4m26`, 498 MB, 1.860.604 rows) joined to the Company Census File (`az4n-8mr2`). **600-broker random
sample: 599 matched (99,8%), 451 published email — net 75,2% reachable.** Today: 92 active brokers show
bond required and not on file.
**★ But FMCSA publishes `AuthHist`, `InsHist` and `Revocation` — it DOES publish history. So there is no head
start to accumulate, and per `THE HEAD-START ASYMMETRY` that is the property that makes a dataset defensible.
Good list, no moat.**

**③ FDA device register — two corrections to the existing candidate file.**
(a) `Official_Correspondent.txt` has **no email column at all**; the only email in the device family is
`us_agent.txt`, 15.479 rows, 100% filled, **foreign establishments only**. The 28.590 US establishments are
phone-only — **a hard C1 veto**, not a preference.
(b) The FY2026 notice adjusts for a **small business registration fee waiver** and projects 30.270 fee-paying
registrations against 44.070 records. **"Everyone wrote the cheque" now has a carve-out.**

---

## 5. CLEAN NEGATIVES — the cause of death is the reusable part

| Register | Cause of death |
|---|---|
| **UK Licensed Sponsors** | Best gate found, completely uncontactable (5 columns). **And the recurring calendar is gone** — the four-year renewal was abolished 6 Apr 2024, licences auto-extended to ten years *(reported by immigration firms; gov.uk primary NOT located — **UNVERIFIED**)*. The live calendar is the per-CoS £525, not the licence |
| **UKGC** | 2.658 accounts is too small, and no contact field |
| **ASIC AFS Licensees** | 6.510 rows, rich licence-condition text, **no email, no street address, no phone** |
| **DOL Form 5500 / EFAST2** | 140 columns, **zero email fields**. Large, solvent, calendar-driven — and reachable only by telephone |
| **FCC ULS** | Email verified at 75,4% — **no substantial mandatory payment behind most licence classes.** Keep as a *contactability precedent*, not a candidate |
| **FMC Ocean Transportation Intermediaries** | Bond verified $50k/$75k/$150k ([46 CFR 515.21](https://www.law.cornell.edu/cfr/text/46/515.21)) — JS-gated ASP.NET portal, no file. **Bulk files beat portals** |
| **USDA PACA** | $995/yr + $600/branch, ~14.500 firms — every route to `apps.ams.usda.gov` redirected to the AMS homepage, and USDA's own page annotates the fee *"as of 2010"*. Needs a human with a browser |
| **USDA Organic INTEGRITY** | Blazor SPA; API paths return the shell, not data. **The Etsy failure mode again** |
| **NRC** | 39 Agreement States licence their own materials users ⇒ the federal list is **structurally partial** |
| **BLM mining claims** | $200/claim/year, hard 1 September deadline — Salesforce portal, **claimant mailing address, no email** |

**One operational note worth more than several of the rows above:** eCFR, CBP, ASQA, ASIC and
federalregister.gov's HTML all returned 403/302 to automated fetch — **Akamai/Cloudflare, which is exactly
where the ~$0,20/record browser-automation cost lands.** The Federal Register **API** and **raw-text**
endpoints are wide open and were the single most reliable primary source in the pass.
