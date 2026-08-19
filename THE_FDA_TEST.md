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

---

# PART THREE — THE CHANNEL RED TEAM. Both the candidate and the pivot are dead.

## ⚠ A SECOND CORRECTION TO ME — my concentration figures were inflated ~6×

**I quoted openFDA LISTING ROWS — one row per product listing, so an agent is counted once per device.**
Deduped against `us_agent.txt`, where one row is one establishment:

| US agent | **Actual establishments** | What I said |
|---|---:|---:|
| Registrar Corp | **1.188** | 4.910 |
| Regrek LLC | **793** | 7.270 |
| Emergo/UL | **276** | 1.981 |
| MEDAGENT | **168** | 4.650 |

**And the in-house departments are tens, not thousands:** Philips 47 · J&J 33 · BD 33 · Medtronic 31 ·
Stryker 31 · Zimmer 27.

**The shape is a very thin head on a very long tail: 13 agents hold ≥100 establishments, 91 hold ≥20, and
3.170 — 67,5% of all agents — represent exactly ONE.** The single largest domain is **gmail.com, with 1.211
establishments.** The tail is individuals on free mail.

## ★ THE ARITHMETIC KILL — and the match rate was MEASURED, not cited

**The agent ran 20 randomly-sampled real official correspondents through commercial enrichment. 5 of 20
returned a work email — a measured 25%** *(n=20, CI ≈9–49%; all five role-plausible, e.g. a Director of
Regulatory Compliance)*.

```
597 importers with the finding  ×  25% match  =  ~149 reachable inboxes
US$133.200/yr ÷ 149  =  US$892/yr each AT 100% PENETRATION
   at 10% conversion → 15 customers × US$8.925/yr
   at 20% conversion → 30 customers × US$4.462/yr
```

> **From a 149-inbox universe, a one-time PDF cannot reach the target at any conversion rate. A subscription
> needs US$4.500–17.800/yr from a buyer whose entire adjacent service — full US-agent representation — sells
> for US$250–849/yr.**
>
> **The channel does not fail. It succeeds, and the number is still too small.**

## ★★ AND THE PIVOT IS DEAD ON ARRIVAL — the obvious buyer already built it

**Registrar Corp — the #1 US agent in FDA's own file — sells ComplyHub, which "actively monitors the
importer's supplier base and provides alerts and risk scores" across "100 million shipping records," with a
0–100 risk index.**

> **The largest, most concentrated, most obvious wholesale buyer for this product has already shipped it.**

**And the whole industry is too small anyway.** At published US-agent fees of **$250 · $449 · $849**
*(vendor-published, unaudited)*, 15.477 establishments implies **$3,9M–13,1M of total annual industry gross.
She would need 1,0–3,4% of the entire US-agent industry's revenue** — sold to firms whose head competes with
her and whose tail (67,5% hold a single client) cannot buy.

## ★ THE REGULATOR HAS PRE-POISONED THE CHANNEL

**FDA's own *Important Reminders about Registration and Listing*, verbatim:**

> *"FDA is aware that various firms may be offering their services to assist domestic and/or foreign
> facilities to register with FDA… these firms are not affiliated with FDA… **FDA does not use any outside
> contractors to notify or bill regulated industry about the need to register.**"*

**And on 3 March 2021 FDA wrote to 25 firms** issuing misleading "FDA registration certificates" that *"often
have the look of an official government document and many display the FDA logo."*

**Field-observed:** Liberty Management Group — **the #10 US agent in FDA's own file, 126 establishments** —
advertises *"Free Registration Certificate"* on its homepage. **The exact artefact the regulator called
misleading is being marketed by a firm sitting inside the dataset.**

> **A structural discount on every first message, not a copywriting problem: the regulator has explicitly told
> this exact population to distrust unsolicited mail of this shape.**

## Two attacks that FAILED — reported because an honest red team reports its misses

- **CAN-SPAM: FAILS.** 15 U.S.C. §7704(a)(5)(A)(iii) requires *"a valid physical postal address of the
  sender"* **with no geographic limitation**, and the FTC's guidance is illustrative rather than exhaustive.
  **A São Paulo address satisfies the statute.** The cost is commercial, not legal.
- **Deliverability: WOUNDS, does not kill.** Every mandatory requirement is satisfiable from Brazil at ~$0,
  and she is far below the 5.000/day bulk threshold. **And the agent reported its own failure: it found NO
  primary evidence that regulated-industry gateways classify compliance-flavoured first-contact mail as
  phishing.** *"That hypothesis is UNVERIFIED and I could not substantiate it"* — my hypothesis, correctly
  refused.
- **The quality-system objection is weaker than it looks**, and the agent refused to overstate it:
  **21 CFR 820 became the Quality Management System Regulation in 2024 and §820.50 "Purchasing controls" no
  longer exists**, with ISO 13485 incorporated by reference instead.

---

# FINAL: DEAD, BOTH VERSIONS

| | |
|---|---|
| **The original** | ~149 reachable inboxes; needs $4.500–17.800/yr each from a buyer whose full service costs $250–849 |
| **The US-agent pivot** | The #1 buyer already ships the product; total industry gross is $3,9–13,1M |
| **The moat** | Free on a public data marketplace since 2013; and the change-log is two downloads a year |
| **The artefact** | 100% of vanished manufacturers are anonymous integers — **the finding cannot name the factory** |

## THE HONEST LEDGER OF MY OWN ERRORS TODAY

**Three, all caught by agents, all material:**

1. **I joined the wrong table** and accused a correct plan of a 3× overstatement.
2. **I generalised from that error** to *"every internally-computed number in that archive is now suspect."*
   **Withdrawn.**
3. **I quoted listing rows as establishment counts** and inflated the concentration figures ~6×.

> **The pattern in all three: I ran a fast computation, got a striking result, and published it without asking
> what would make it wrong. That is exactly the failure mode this file's evidence standard exists to prevent,
> and I committed it three times in one afternoon while auditing someone else for the same thing.**
>
> **The rule earned: A RECOMPUTATION THAT DISAGREES WITH A CAREFUL SOURCE IS EVIDENCE ABOUT THE
> RECOMPUTATION FIRST.**

**What this candidate cost: about two hours and zero dollars. What it produced: a fifth condition on the
erasure moat, a measured enrichment match rate, and three corrections to my own method.** The six hunts
running now carry all of it.

---

# PART FOUR — THE THIRD RED TEAM. Dead on CONSTRUCTIBILITY, before any question of law or price.

**It confirms my table error independently, and then finds the cause of death the other two missed.**

## ★★ THE EMAIL CANNOT BE WRITTEN

**Of the 3.528 absent manufacturer keys, ZERO appear in `Owner_Operator.txt`, `us_agent.txt`,
`Official_Correspondent.txt` or `registration_listing.txt`. No name, no registration number, no FEI, no
country.**

All she holds is `MANUFACTURER_REG_KEY` — **an FDA-internal surrogate integer that appears in no FDA public
interface**, so the importer cannot look it up either.

> **The specified email — *"your filing declares 5, FDA's file contains 2, here are the three listing IDs"* —
> becomes *"here are the integers 51, 4471 and 88012."* The recipient cannot resolve them, cannot verify them,
> and cannot act on them.**
>
> **The whole design rested on "they verify it themselves." There is nothing to verify against.**

### And the mechanism is the moat wearing its other face

**Every name-bearing table in the weekly extract is keyed to the 28.591 CURRENTLY-REGISTERED establishments.
When one de-registers it vanishes from the entire distribution — its name included.**

> ### **The erasure I read as a moat — "nobody can back-fill the history" — IS THE SAME FACT THAT GAGS THE PRODUCT. She cannot back-fill it either.**

**The only nameable variant: where the dangling row resolves to a listing the importer itself owns, so she can
cite a real 510(k) number. That is 88 importers of 1.846 — 4,8%.**
**US$11.100/month from 88 prospects is $126/month from every importer in the country at 100% conversion.**

## ★ FDA GIVES IT AWAY — and the buyer is LEGALLY COMPELLED to do the check

**21 CFR 807.22(b)(3), verbatim:** *"Every fiscal year, during the period beginning on October 1 and ending on
December 31, owners or operators shall **review and update all of their device listing information** that is
on file at FDA… **The accuracy of all information on file must be confirmed each year regardless of whether
any changes were made.**"*

**And FDA's own registration database tells them where:** *"Need to update your information? To modify, add,
or delete information, log onto your FURLS account."*

> **She would be selling a worse, unnameable copy of a MANDATORY ANNUAL CHORE the buyer already performs
> inside the authoritative system. THE FREE FRONT DOOR, with a statute behind it.**

## ★ AND THE IMPORTER HAS VIOLATED NOTHING

**The duty to register belongs to the foreign manufacturer — 21 CFR 807.40(a).** A dangling reference means
*the manufacturer* lapsed. The importer's declaration remains true.

- **807.22(b)(2)'s 30-day update duty reaches only the enumerated list in 807.25(b)** — establishment name and
  address, website, owner/operator contact details, official correspondent details, trade names.
  **The declared-manufacturer list is not in it.**
- **807.20(a)(5): the importer *"may fulfill their listing obligation… by submitting the name and address of
  the manufacturer."*** An option, not a supplier roster with an accuracy duty.
- **807.28's update triggers** — activities starting or ceasing, devices entering or leaving distribution.
  **"Your supplier's registration lapsed" is not among them.**
- **Import Alerts 89-16 and 99-32 were read in full: both concern REFUSED INSPECTIONS, not registration
  status.** No import alert covers this.
- **And a hazard pointing at her: 21 CFR 807.39** — *"Any representation that creates an impression of
  official approval because of registration or possession of a registration number is misleading and
  constitutes misbranding."*

## ★ THE SHRUG, MEASURED

**`MANUFACTURER_REG_KEY` is a monotonic surrogate, so its magnitude proxies age.** If dangling references
were mostly abandoned legacy suppliers, absence would concentrate in low keys. **It does not:**

| Key range | % absent |
|---|---:|
| 0–50k | 28,7% |
| 50k–100k | 34,5% |
| **100k–150k** | **38,5%** |
| 150k–200k | 35,8% |
| 200k–250k | 32,7% |
| 300k–400k | 14,9% |

> **29–38% across six of seven vintages. No single explanation dominates — which is WORSE than if one did.
> The base rate IS the message.** An importer told *"3 of your 9 are gone"* mentions it to a peer and learns
> the peer has the same ratio. **It reads as a property of the file, not a discovery about them.**

**And `Manu_ID_by_Imp.txt` has no date field at all.** She cannot distinguish *"lapsed last month"* from
*"abandoned in 2009"* — **and recency is the only thing that would make it urgent.**

## The competitor, now confirmed from the vendor's own page

**fdadevicecheck.com: free single lookup · $19/month for 25 facilities · $49/month for 250.** Same product,
already built, already priced, **and it solved the naming problem by working off the PRESENT registry rather
than the absent one.** *(Registrar Corp's Compliance Monitor is $1,99/facility/month — 2015 press release,
food-framed, possibly stale.)*

## ★ AND THE CLEANEST KILL OF THE US-AGENT PIVOT

**Under 807.40(b) and 807.25(e) the US agent / official correspondent is the party that SUBMITS the client's
registration and RECEIVES ALL FDA CORRESPONDENCE about it.**

> ### ***"You cannot sell a firm a monitor for its own outbox."***
>
> Registrar Corp does not need telling the status of registrations it files itself. **And it is not a market —
> it is about six accounts, each a bespoke enterprise sale with a procurement conversation attached.**

---

# CLOSED. Three red teams, three sufficient causes, none of them the one I attacked.

| | |
|---|---|
| **RT1 — buyer** | FDA gives it free and mandates the check annually; the importer has no duty; a competitor sells it at $19/month; **the finding cannot be named — 88 prospects** |
| **RT2 — mechanism** | Append-only table (82 added, 0 removed / 14 days); archive already public and free since 2013; annual churn = two downloads a year |
| **RT3 — channel** | ~149 reachable inboxes at a measured 25% match; needs $4.500–17.800/yr from a buyer whose full service costs $250–849 |

## THREE LAWS EARNED, AND THEY ARE THE RETURN ON THE WHOLE EXERCISE

> **1. THE NAMEABILITY CONDITION.** It is not enough that an authority overwrites. **The vanished record must
> remain IDENTIFIABLE after it vanishes.** Where erasure is total, the moat and the gag are the same fact —
> you hold a list of anonymous integers, and so does everyone, forever.

> **2. YOU CANNOT SELL A FIRM A MONITOR FOR ITS OWN OUTBOX.** Before proposing a monitoring product to an
> intermediary, ask whether they are the party who FILES the thing being monitored. If they are, they already
> know, by construction.

> **3. CHECK WHETHER THE BUYER IS LEGALLY COMPELLED TO DO YOUR CHECK ALREADY.** A mandatory annual review
> inside the authoritative system is the strongest possible version of THE FREE FRONT DOOR, and a statute
> that compels it can be found in an afternoon.
