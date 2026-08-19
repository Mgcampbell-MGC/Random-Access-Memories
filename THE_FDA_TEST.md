# THE FDA TEST — run directly, 19 Aug 2026

> ## ⚠⚠ RETRACTION — SECTION 2 BELOW IS WRONG, AND IT IS MY ERROR, NOT THE PLAN'S.
>
> **I tested the wrong table.** Two files describe the importer→manufacturer relation from opposite sides:
> `Reg_Imp_ID_by_Manu.txt` (which I used) and **`Manu_ID_by_Imp.txt` (which the plan used).** A red-team agent
> caught it. **I then downloaded the correct table and recomputed:**
>
> | | Plan claimed | **My recomputation on the CORRECT table** |
> |---|---|---|
> | Declaring importers in the registry | 5.920 | **5.941** |
> | Distinct absent manufacturers | 3.478 | **3.477** |
> | Dangling pairs | 6.325 | **6.326** |
> | **Importers with ≥1** | **1.846 = 31,18%** | **1.846 = 31,07%** |
> | Importers with ≥2 | 891 = 15,05% | **889 = 14,96%** |
>
> **Every figure reproduces. The plan's author did the work and did it correctly.**
>
> **I publicly wrote that the numbers were "overstated by 3,3× and 4,5×" and that "every internally-computed
> number in that archive is now suspect." BOTH CLAIMS ARE WITHDRAWN.** The archive's arithmetic held up under
> the first serious audit it received; mine did not. **The lesson I drew was the opposite of the true one:
> when a recomputation disagrees with a careful source, suspect the recomputation first.**
>
> **The business is still dead. It dies for the reasons in Part Two — none of which is bad arithmetic.**


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

---

## 7. THE PROSPECT LIST, INSPECTED — and this is where it probably ends

**The 597 shrinks again once you look at who is actually in it.**

| | |
|---|---:|
| Importers with ≥1 dangling reference | **597** |
| ...US-based | **574** |
| **...and actually flagged `INITIAL_IMPORTER = Y` — the real ICP** | **440** |

**And two-thirds of them have the weakest possible finding:**

| Dangling references | Importers |
|---:|---:|
| **exactly 1** | **401 — 67%** |
| 2 | 115 |
| 3 | 50 |
| 4+ | 31 |

> **For 401 of 597 buyers the email says: "one of your ten declared manufacturers is not in the current
> file." That is a single stale row. It is the shrug, and it is the majority case.**

### ★ And the strongest findings belong to the companies that will never buy

**Sorted by number of dangling references, the top of the list is:**

| Dangling | Company |
|---:|---|
| **31** | **MEDLINE INDUSTRIES** |
| 14 | SW Technologies Inc. |
| **10** | **Cardinal Health 200** |
| **10** | **Covidien** |
| 9 | Avanos Medical |
| 8 | CareFusion 2200 · **ZIMMER** · Compass Health Brands |
| 7 | Straumann USA · **BIOMET** |

> **These are precisely the firms the plan itself said to exclude as procurement-gated. The impressive
> findings and the reachable buyers are ANTI-CORRELATED — the same pincer that killed the newsletter
> candidate, arriving in a completely different industry.**
>
> **Strip the giants and strip the single-row findings, and the genuinely sellable pool is on the order of
> 100–150 companies.**

### The arithmetic at that pool size

**US$11.100/month from ~150 prospects means 15 customers at $740/month, or 30 at $370 — against a competitor
reportedly at $19/month.** *(The median ICP importer declares 10 manufacturers; p75 is 22; the largest
declares 602.)*

---

## 8. WHAT I COULD NOT TEST, AND IT IS THE ONE THING THAT COULD SAVE IT

**Everything above is a measure of the STOCK of findings from a single snapshot. The plan's actual argument
was about FLOW** — registration renews 1 Oct – 31 Dec, so *"every January a fresh cohort drops out."*

> **A cohort that lapses annually could produce far more findings per year than the 998 standing today. I
> cannot measure it, because measuring it requires two snapshots months apart — which is precisely the moat
> the plan is built on.**

**So the honest position is: the stock is thin, the top of it is unsellable, and the flow is unknowable
without doing the thing. That is a genuinely uncomfortable place, and it should not be resolved by
assumption in either direction.**

---

## 9. STANDING VERDICT — before the red teams report

**Probably dead as specified. Three independent problems, none of which is a matter of execution:**

1. **The pool is ~150 sellable, not 717.**
2. **The channel is telephone.** 41 of 597 have any email in the data.
3. **The best findings belong to Medline and Cardinal Health.**

**Two things survive regardless:**

- **THE ERASURE MOAT IS A REAL AND VERIFIED PATTERN** — just not necessarily on this register. *(Three agents
  are now hunting it across every public register they can reach.)*
- **THE US-AGENT POPULATION IS EMAIL-PUBLISHED AND EXTRAORDINARILY CONCENTRATED** — 177.900 records, single
  firms representing thousands of establishments. **That is a different and possibly better business, and it
  is under attack by two red teams right now.**

> **Cost of learning all of this: about forty minutes and zero dollars. The plan it corrects took someone
> weeks to write.**


---

# PART TWO — THE RED TEAM. Dead, comprehensively, and not for the reason I said.

**A red-team agent obtained TWO real snapshots fourteen days apart (3 and 17 August) and tested the mechanism
by direct observation instead of argument. That is the most valuable thing produced on this candidate.**

## ★ KILL 1 — the archive already exists, free, and has since 2013

**John Snow Labs publishes all thirteen of these exact files on AWS Data Exchange, free, advertising
"All historical revisions" and "All future revisions."** Their dataset page states **Date Created 2013**,
**updated weekly**, and confirms the table carries **`Registration_Key`** and `FEI_NUMBER` — *the precise
columns the entire mechanism depends on.* Also mirrored on Databricks Marketplace.

> **AWS Data Exchange revisions are immutable timestamped snapshots. If they have accumulated since listing,
> a ~13-year weekly archive of the exact join keys is already public and free. An eight-week private archive
> is worth nothing against it.**
>
> **THE HEAD-START ASYMMETRY, pointing the wrong way.** *(Depth of the revision history is **UNVERIFIED** —
> and it is the cheapest remaining test: subscribe free and call `ListDataSetRevisions`.)*

## ★ KILL 2 — the declaration table is append-only, and that is measured

**Over fourteen days: 82 pairs added, ZERO removed. Not one stale link was cleaned.**

**And the rule explains why. 21 CFR 807.20(a)(5):** an initial importer *"may fulfill their listing
obligation… by submitting the name and address of the manufacturer."* **The duty is to describe WHO MAKES THE
DEVICE — not to assert that establishment is currently registered.** Nothing obliges an importer to drop a
manufacturer whose registration lapsed, and FDA does not purge.

**Three measurements confirm the cruft reading:**

| | |
|---|---|
| Importers named in the declaration table who are **themselves absent** from the registry | **3.041 of 9.452 = 32%** |
| **Absent manufacturer keys that appear NOWHERE ELSE in the extract** — no name, no address, no country | **I measured 3.477 of 3.477 = 100%** *(the red team found 58 nameable across all 13 files; either way ~98–100%)* |
| Orphan stock, 3 Aug → 17 Aug | **3.529 → 3.528.** 3.525 present in both. **Static** |

> ### **The deliverable is therefore: "three of your declared manufacturers are ANONYMOUS INTEGERS that FDA no longer lists." She cannot say which factory it was, where it is, or what it made — because the record is gone. That is not a finding a regulatory manager can act on, and it is the single most damaging fact about this candidate.**

## ★ KILL 3 — the resolver cannot run on the rows the product is about

The plan's continuity resolver separates a genuine lapse from a renumbering using `FEI_NUMBER`. **But `FEI_NUMBER`
exists only in `Registration.txt`, and an orphan by definition has no row there. For the 3.477 standing
orphans, lapse-versus-renumbering is permanently unresolvable by anyone, including her.**

**And for the flow it is a real confound:** of **14 keys that genuinely vanished** between the two snapshots,
**3 (21%) reappear under a new key with the same FEI and registration number** — renumberings, not lapses.
*Named: SPR Therapeutics, Seegene USA-Irvine, Piccolo Medical.*

## ★ KILL 4 — the honest caveat destroys the moat instead of saving it

**21 CFR 807.22(b)(1): annual registration runs 1 October to 31 December.** The red team measured in
mid-August — dead centre of the cycle — so its fortnightly churn figures **understate the annual number, and
it said so rather than pretending otherwise.**

> **But if erasure is an ANNUAL BATCHED EVENT, the change-log is captured by TWO DOWNLOADS A YEAR — one in
> late December, one in mid-January. That is two calendar reminders, not a proprietary archive. Continuous
> snapshotting buys nothing a newcomer cannot replicate at zero cost.**

## ★ KILL 5 — and the free front door, exactly where the file predicted it

**FDARegWatch (Liberty Management) monitors FDA registration status "complimentary."**

> **Registration monitoring is the customer-acquisition cost of whoever sells US Agent services. THE FREE
> FRONT DOOR — and it kills the US-agent pivot at the same time as the original candidate, because the
> US-agent firms are precisely the people already giving this away to win the paying work.**

## What survived the attack

**The erasure premise is TRUE.** FDA publishes no archive; its download page offers only current files;
**openFDA cannot substitute because it has no `reg_key` field at all**, so the join is literally not
reproducible from the API. And **21 CFR 807.22(c)** puts a non-renewing establishment in *"failed to register"*
status whose information *"may not appear on the FDA Web site."* **Erasure is by design.**

**The licence is clean.** openFDA is **CC0 1.0** — *"copy, modify, distribute and perform the work, even for
commercial purposes, all without asking permission."* Commercial resale is permitted.

---

## FINAL VERDICT — DEAD, and the cause of death is reusable

**Not for bad arithmetic. The arithmetic was right.** It dies because:

1. **The artefact is a static, anonymous, un-mandated backlog FDA never cleans** — and 100% of the absent keys
   are unnameable, so the finding cannot even identify the factory.
2. **The change-log is annual, so two downloads a year reproduce it.**
3. **A vendor appears to have been publishing the whole archive weekly and free since 2013.**
4. **The buyer's own service providers already monitor registration status for nothing.**

> ### THE ERASURE MOAT NEEDS A FIFTH CONDITION, AND THIS IS WHERE IT WAS LEARNED. It is not enough that the authority overwrites. **The vanished record must still be IDENTIFIABLE after it vanishes** — a name, an address, something a human can act on. **A register that erases COMPLETELY leaves you holding a list of anonymous integers, which is a moat around nothing.**
>
> **Add to the screen: does the disappearance leave a corpse you can name?**
