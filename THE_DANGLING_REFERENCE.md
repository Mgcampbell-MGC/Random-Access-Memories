# THE DANGLING REFERENCE — census of 15 declaration/registry pairs, 19 Aug 2026

**The pattern hunted:** a public table where entity A must **NAME** entity B with an identifier, joined against
a register of B's current status. Where B has lapsed and A's declaration still names it, A has a stale filing
with a statutory consequence. **The dangle is computable from two free files and nobody's opinion is involved.**

---

## 1. ★★ THE FOUR CROSS-CUTTING FINDINGS — worth more than any candidate below

> ### **★ 1. A 30% DANGLE RATE IS MORE LIKELY A SCHEMA MISREADING THAN A FINDING.**
>
> The hunt produced a headline result — **847 registrant DUNS values absent from the establishment DUNS set,
> 3.112 of 10.414 rows = 29,9%** — and then killed it itself: **a registrant is the entity that SUBMITS a
> registration, often a US agent or a parent, and nothing requires a registrant to be a registered
> establishment. A 30% "dangle" that is simply the normal shape of the table.**
>
> The IRS pair did the same thing in the opposite direction: raw **15,1% of filers** collapsed to **5,8%** once
> netted against Publication 78. **2.194 hits → 205.**
>
> **NET EVERY DANGLING SET AGAINST THE REGISTER THAT RECORDS THE CURE.** For revoked US charities that is
> Pub 78; for anything append-only it is the reinstatement table.
>
> *(This is the same failure mode recorded against me in `THE_FDA_TEST.md` — wrong join, confident number,
> public claim. It has now happened three times in this file. It is the single most reliable way to be wrong
> here, and the antidote is always the same: **a recomputation that disagrees with a careful source is evidence
> about the recomputation first.**)*

> ### **★ 2. SCREEN FOR THE AMENDMENT DUTY FIRST. If nobody is REQUIRED to keep the declaration current, stop.**
>
> Registries are everywhere. Public tables where A must *name* B in bulk with an identifier are rare — and the
> four best found (Form ADV Schedule D, Form 990 Schedule I, Form 5500 Schedules A/SB, SPL drug listings) are
> **all annual regulatory filings with an amendment duty.** That duty is the ONLY thing that defeats the
> append-only objection which killed the FDA device candidate. **The declaration side is the scarce half.**

> ### **★ 3. THE POSTAL LIST LAW takes a second bound: the split is PER-REGISTER, not national.**
>
> Hand-inspected this pass: **FDA drug establishments 100,0% email** · **Charity Commission 148.191 of 184.104
> registered charities = 80,5%** · **FMCSA Company Census `EMAIL_ADDRESS` 29,6% filled** over the first 391.833
> rows. Against that: **the SEC publishes no email at all in 243 columns of Form ADV**, and neither Form 990
> nor Form 5500 carries one. **Three of six inspected registers published email.**

> ### **★ 4. Nothing in this census needed browser automation.** Every measurement came from `curl` plus a flat file. The one exception — the PCAOB firm register — is ~2–4k plain GETs, not a headless browser.

---

## 2. THE THREE STRONGEST

### ★ INVESTMENT ADVISERS' AUDITORS vs PCAOB REGISTRATION — best mechanism, worst front door

**The declaration.** Form ADV Part 1A **Schedule D §9.C** and **§7.B.(1) Q23** make an adviser name each
independent public accountant and answer *"Is the independent public accountant registered with the Public
Company Accounting Oversight Board? … If 'yes,' Public Company Accounting Oversight Board-Assigned Number:"*
([the form itself](https://www.sec.gov/about/forms/formadv-part1a.pdf)). Free bulk:
[SEC Form ADV archive](https://www.sec.gov/foia/docs/form-adv-archive-data).

| Measured on the real files | rows | PCAOB number filled | declared NOT registered | declared NOT inspected |
|---|---|---|---|---|
| **§9.C** | **157.601** | **82.611 (52,4%)** | 6.592 | 4.725 |
| **§7.B.(1) Q23** | **1.484.861** | **953.688 (64,2%)** | 11.468 | 6.563 |

**The consequence is statutory and expensive.** 17 CFR 275.206(4)-2(b)(4)(ii) grants the audited-financials
exception only where the fund is audited *"By an independent public accountant that is registered with, and
subject to regular inspection as of the commencement of the professional engagement period, and as of each
calendar year-end, by, the [PCAOB]."* **Lose that and the adviser falls back into surprise examinations plus
quarterly statements — and its Form ADV answer is a false statement under Advisers Act §207.**

> ### ★★ AND THERE IS A REAL CLOCK-START.
> [SEC Release 34-102074](https://www.sec.gov/files/rules/pcaob/2025/34-102074.pdf) (2 Jan 2025) approved PCAOB
> Rule **2107(h)**, *Constructive Requests to Withdraw from Registration*, treating two consecutive years of
> non-filing and non-payment as a constructive withdrawal — and states that such a firm *"could have its
> registration deemed withdrawn under Rule 2107(h) **beginning in the fall of 2026**."*
>
> **A cohort of audit firms stops being registered roughly three months from now, and every adviser who named
> one has a stale filing.** `THE_DATASET_HUNT` identified a clock-start as the only level moment against
> `THE HEAD-START ASYMMETRY`. **This is one.**

**Why it fails anyway — and it is the last mile, not the mechanism.**
- **No registry file.** `pcaobus.org` renders client-side; `rasr.pcaobus.org` 302s to an error page; four guessed
  API paths 404'd. The only PCAOB bulk file is **Form AP** (`FirmFilings.zip`, 93 MB, daily) — **a record of
  ISSUER audits, not a registration register.** 364 of the 661 claimed PCAOB numbers are absent from it, which
  is *expected* (a firm auditing only private funds never files Form AP) and is **NOT a dangle. Do not build on
  that count.**
- **★ She cannot reach the buyer.** `IA_ADV_Base_A` has **243 columns and not one email, phone or URL.** The form
  *asks* for an email at Items 1.J/1.K; **the SEC does not publish it.** What is published is
  `IA_Schedule_D_1I` = `FilingID, Website`. **Domain yes, mailbox no.**

### ★ GRANTMAKERS' GRANTEES vs THE IRS AUTO-REVOCATION LIST — the join was run end-to-end

**Declaration:** Form 990 **Schedule I Part II** — every domestic grantee over $5.000, **with EIN**
([bulk XML, free, monthly](https://www.irs.gov/charities-non-profits/form-990-series-downloads)).
**Registry:** [Automatic Revocation list](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip),
**1.246.174 rows**, netted against [Pub 78](https://apps.irs.gov/pub/epostcard/data-download-pub78.zip),
**1.412.318 currently-eligible EINs**. **Rule:** IRC **§4945(a)(1)** — *"20 percent of the amount thereof"*.

| Measured on `2025_TEOS_XML_01A.zip` (17.044 returns) | |
|---|---|
| Returns with Schedule I recipient EINs | **1.024** (1.018 distinct filers) |
| Grant rows | **49.863** |
| Rows naming an EIN on the revocation list | **2.194** |
| Distinct filers with ≥1 | **154 of 1.018 = 15,1%** |
| Restricted to revocations effective **before** the filer's period end | 1.749 rows / 140 filers |
| **…and still absent from Pub 78 today** | **205 rows / 59 filers = 5,8%** |

**5,8% is an UPPER BOUND, not the answer** — churches, group-ruling subordinates and government units are
legitimately absent from Pub 78 and were not eliminated. **Kills:** Candid's GuideStar Charity Check already
sells "verify before you grant" and is wired into grants-management software; **Form 990 carries no email**;
and the signal is annual per filer, not continuous.

### ★ DRUG LISTINGS vs THE DRUG ESTABLISHMENT REGISTER — the only pair publishing email at 100%

**This is the third independent arrival at DECRS in one day.** See `THE_FEE_GATE_CENSUS.md` §2 for my own
direct re-measurement. The dangle itself (NDC → establishment) requires parsing SPL XML rather than reading a
flat file, and **it is the taken example's sibling — same agency, same erasure mechanism, adjacent statute.**

**What survives regardless of the join: 10.414 establishments and ~7.000 registrants, in a free daily file,
with a working email address on every single row.** That is the best distribution asset in the census.

---

## 3. ELIMINATED, WITH THE CAUSE OF DEATH

| Killed | Cause |
|---|---|
| **EUDAMED certificates vs NANDO** | **The declaration table is VOLUNTARY** — notified bodies *"can enter information in the system on a voluntary basis since October 2021"* ([EC](https://health.ec.europa.eu/medical-devices-eudamed/notified-bodies-and-certificates-module_en)). **An incomplete declaration table makes absence uninterpretable: you cannot tell a dangle from a non-entry** |
| **ASIC authorised reps vs licensee registers** | **The register maintains its own referential integrity** — every representative row carries `Date ceased`, and ASIC ceases reps when the licence goes. The authority already closed the loop |
| **ATO SMSF auditor numbers vs the auditor register** | **The authority runs this join itself** as the published SAN-misuse programme. Same law as the Form 5500 kill in `GRAVEYARD.md`: *an agency that publishes a public register often works that register itself* |
| **FCC equipment authorisations vs accredited labs/TCBs** | **Append-only cruft.** A grant is a permanent historical record; the lab's accreditation lapsing later is normal and means nothing. And the open-data grantee table was last refreshed **March 2021** |
| **UK EPC assessors vs scheme accreditation** | Same disease — an EPC is valid ten years, assessors retire, **a dangle is the expected state** |
| **Charity trustees vs disqualified directors** | **No key, and the finding is defamatory-adjacent.** The `charity_trustee` extract is `trustee_name` + internal id, **no DOB, no address** (921.892 rows verified); Companies House publishes no bulk disqualification file. **Name-only matching on "your trustee is disqualified" is the one place in this pattern where a false positive is not merely embarrassing** |
| **Companies House ACSP register** | **Opt-in** — providers choose whether to appear, so absence proves nothing |
| **Enrolled actuaries (Form 5500 Sch. SB)** | Declaration is perfect — `SB_ACTRY_ENRLMT_NUM` **100,0% filled**, 42.418 rows — but **the registry does not exist in usable form**: the IRS RPO directory has name/city/state only, no enrolment number. And 1.927 actuaries is a thin population |
