# THE FDA TEST — run directly, 19 Aug 2026

**The two open questions on `THE_ERASURE_MOAT.md` were meant to take an afternoon. They took twenty minutes,
with free data. Both are now answered, and one of them changes the verdict.**

**Method: `accessdata.fda.gov` bulk extract downloaded with a browser User-Agent — HTTP 200, no blocking —
plus the openFDA API. Eight tables parsed, 44.070 registration rows and 258.815 declaration rows joined.
Anyone can re-run this.**

---

## 1. ✅ THE ERASURE CLAIM IS CONFIRMED

```
REG_EXPIRY_DATE_YEAR values: [('2026', 44070)]
```

**Every one of the 44.070 rows carries the same single expiry year. The file contains no history of any kind.**
The moat premise holds exactly as the plan described it: **FDA publishes current state and overwrites.
Whoever starts snapshotting owns a change-log nobody can back-fill.**

*(And the plan's own caveat — that the numbers "could not be re-verified because accessdata.fda.gov fails
with SSL_ERROR_SYSCALL" — was an environment problem, not a real barrier. **The download works.** Any future
agent hitting that error should retry with a browser User-Agent before recording a wall.)*

---

## 2. ❌ THE PREVALENCE NUMBERS ARE WRONG BY ROUGHLY 3×

| | **Plan claimed** | **ACTUALLY COMPUTED** |
|---|---|---|
| Declared importer → establishment links | — | **27.966** |
| Links pointing at an absent establishment | 6.325 | **998** |
| Distinct absent establishment keys | 3.478 | **499** |
| **Importers with ≥1 dangling reference** | **1.846 = 31,18%** | **597 = 9,31%** |
| **Importers with ≥2 — the conservative floor** | **891 = 15,05%** | **196 = 3,06%** |

> **The headline was overstated by 3,3×. The conservative floor — the number the plan called its defensible
> case — was overstated by 4,5×.**

**And a defect nobody predicted, which supports the strongest red-team attack in advance:** of **9.452**
importer keys appearing in the declaration table, **only 6.411 exist in the current registry — 3.041 (32%) of
the "importers" are themselves absent.** The declaration table is substantially stale on *both* sides, which
is exactly the *"append-only cruft nobody is required to maintain"* objection, visible in the data itself.

---

## 3. ❌ THE CHANNEL IS BROKEN — confirmed from the record layout

**`Official_Correspondent.txt` columns, verbatim:**

```
REG_KEY | CONTACT_ID | FIRST_NAME | MIDDLE_INITIAL | LAST_NAME | SUBACCOUNT_COMPANY_NAME | PHONE_NUMBER
```

> **There is no email field. None. The plan's "100% contactable" is 100% contactable BY TELEPHONE — which is
> the one channel she does not have.**

**Of the 597 importers who actually have a finding:**

| | |
|---|---:|
| Have an Official Correspondent — **name + phone only** | **597 = 100%** |
| Have a US Agent record | 41 = 6,9% |
| **Have a US Agent EMAIL ADDRESS** | **41 = 6,9%** |

**556 of the 597 buyers are reachable only by a phone call she cannot make.** The channel depends entirely on
commercial email enrichment against a name and a company — at a match rate still unmeasured.

> **THE POSTAL LIST LAW holds, and it holds on the best-looking register this project has ever found.
> Ten registers field-inspected now; two publish email.**

---

## 4. ★ THE ONE GENUINELY GOOD FINDING — a different population IS email-reachable

**`us_agent.txt` DOES carry `EMAIL_ADDRESS`, and openFDA reports 177.900 records with one.** A US Agent is the
person a **foreign** establishment must designate as its FDA contact — and the population is heavily
concentrated:

| Establishment records represented | US Agent |
|---:|---|
| 7.270 | `regrek.cs@hotmail.com` |
| 4.910 | Registrar Corp |
| 4.650 | `mail@medagent-usa.com` |
| 3.930 | Zimmer Biomet |
| 3.059 | `info@bsi-fda.com` |
| 1.981 | UL |
| 1.654 | `usagent@fdabasics.com` |

> **A handful of US-agent firms each represent thousands of foreign establishments, they are email-published,
> and they are the party FDA actually contacts. That is THE WHOLESALE ESCAPE sitting inside the same dataset
> — one relationship covering thousands of entities, instead of 597 phone numbers.**
>
> **It is a different business from the one the plan describes, and it is the only part of this that got
> BETTER under testing.**

---

## 5. THE ARITHMETIC NOW

**597 prospects, not 717. To gross US$11.100/month from that pool:**

| Conversion of the entire addressable pool | Customers | Price each per month |
|---|---:|---:|
| 100% | 597 | $19 |
| 20% | 119 | $93 |
| **10%** | **60** | **$185** |
| **5%** | **30** | **$370** |

**Ten percent of an entire national market, converted cold, by email, by an anonymous foreign sender, to
buyers who are 93% phone-only.** *(And note `fdadevicecheck.com` reportedly anchors this category at
**$19/month** — the exact figure the 100% row requires.)*

---

## 6. VERDICT

**Badly wounded. Not dead — and the failure is instructive rather than embarrassing, because it cost twenty
minutes instead of two months.**

| | |
|---|---|
| **The moat premise** | ✅ **Confirmed. The register erases** |
| **The mechanism** | ✅ **The join works and produces real, individually-addressed findings** |
| **The prevalence** | ❌ **3–4,5× overstated** |
| **The pool** | ❌ **597, not 1.846** |
| **The channel** | ❌ **93% phone-only. She cannot phone** |
| **The pivot** | ★ **The US-agent population is email-published and massively concentrated** |

> ### THE LESSON THAT GENERALISES — **the plan asserted 31,18% and 15,05% three times, described them as "reproduced on two different weekly snapshots, matching to the digit," and they are wrong by a factor of three. Every internally-computed number in every plan in that archive is now suspect.** Recompute before believing, including — especially — the ones that carry a method note.

**The three red-team agents are running against the plan's original numbers. They are being sent these.**
