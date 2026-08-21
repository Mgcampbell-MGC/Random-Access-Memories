# CORRECTIONS — 21 Aug 2026, from the one-pager fact-check

**Three builders wrote the pages; three fact-checkers attacked them against the repo and the banked archives.
45 corrections. The four that matter, verified BY ME against the captured files.**

---

## 1. ⚠⚠ THE GATE-CALENDAR CLAIM WAS WRONG — my error, and I reported it to the founder

**I claimed candidate #1 "survived the annual-calendar kill test" because YTI's gate schedule was a rolling
~6-day window whose values varied week to week. Verified against the banked tarballs: FALSE.**

| What I said | What the captured files show |
|---|---|
| Rolling ~6-day window | **Static 14-day window, 17→30 Aug** |
| Values varied week to week | **BYTE-IDENTICAL across the 19 Aug and 21 Aug captures** |
| Operational closures no calendar contains | **9–11 days published FORWARD; the only full-day closures are weekends (22–23, 29–30 Aug)** |

**And Maersk's own tariff — quoted in `THE_WORKING_DAY_LEDGER.md` and dropped from my summary — says
"Partial day closures are considered as a full working day."** So the 2nd-shift closures I cited as evidence
**do not move the denominator at all.**

**I conflated two different pages.** The rolling window that genuinely changes is the **closed-area matrix**
(Aug 19–25 → Aug 21–27, values altered), which records yard-block closures, not the 541.6 denominator.

> ### ★ THE CORRECTED CLAIM — and the candidate survives on it. The transient facts are **EMPTY-RETURN ACCEPTANCE per line per day** and **yard-area closures**, NOT gate-open days. Verified across the banked captures: ITS dated 8/19→8/21, PNCT 8/20→8/21, TraPac and the closed-area matrix all changed. And these have their own legal hook — **46 CFR 545.5(c)(2)(ii)**: detention charged when *"empty containers cannot be returned"* is *"likely to be found unreasonable."*

## 2. ⚠ THE DAY-0 MERKLE ROOT DOES NOT REPRODUCE

The four RFC 3161 tokens are **genuine** — Status: Granted, four distinct policy OIDs, 21:15:59–21:16:00 GMT —
but their message imprint is the hash **of the root file**, and the root value inside it
(`a0da4396…c20aa6`) **does not reproduce from the six captured files under any tested construction**
(concatenated digests, hex-joined, newline-joined, filename+hash leaves, pairwise Merkle, the tarball itself,
and all 720 file orderings). **The Day-0 bundle is timestamped but not independently verifiable. Document the
construction, or re-root it.**

## 3. ⚠ FOUR MORE, EACH FAILING IN THE OPTIMISTIC DIRECTION

- **Registrar Corp is 427 rows / 417 distinct FEIs**, recounted on all three banked days. **The "418" in
  `THE_FEE_GATE_CENSUS.md` and `STATE_OF_PLAY_19AUG.md` is not reproducible under any definition** — the
  hunt's original 427 was right and my "correction" was the error. **Fourth confident wrong number in this file.**
- **The 75,2% email figure is FMCSA property BROKERS, not motor carriers.** The measured carrier figure is
  **29,6%**. `GATELEDGER_Business_Overview.docx` carries the mis-join and must be corrected.
- **"$210–395 per container-day" is what the IMPORTER saves** — the recovery firm earns 25–35% of it. The
  per-buyer value is a fraction of the headline.
- **"Six independent ways" is wrong — it is THREE.** Both `CLAUDE.md` and `THE_TOURNAMENT_VERDICT.md` say three
  jurisdictions and ~48 industries.

## 4. ⚠ COVERAGE, AND A PIPELINE DEFECT

**"8 of 20 terminals" is asserted in two files and never enumerated anywhere.** The only ENUMERATED census is
**5 of 17** (3 gate/yard status + 2 empty-return server-rendered); the running capture covers **4**. **Name the
terminals in writing before the ten-day run.**

**And my own pipeline drifted:** Day 0 wrote `yti_gate_schedule.html`, Day 2 wrote `yti_gate.html` — a diff
engine keyed on filename would have silently reported the page as deleted and recreated. **Fix before the
ten-day run.** Days 1 and 2 also carry **no timestamp tokens** (only Day 0 is countersigned), and **no Maersk
edition was captured on 20 Aug** — a permanent hole on day two of a three-day run.

## 5. WHAT THIS DOES TO THE BOARD

**Nothing is dead.** #1's scarcity claim narrows from "gate-open days" to "empty-return acceptance and yard
closures" — which are measured, transient, and independently hooked to 545.5(c)(2)(ii). #2 is unchanged and
slightly stronger (the Expanscience removal). #3 is unchanged.

**What changes is the honesty of the pitch, and one bar gets sharper:** the ten-day capture must now record
**which artefacts actually change**, not assume the gate calendar is one of them.

---

## Second pass, 21 Aug 16:20 UTC — four pipeline defects, fixed and verified

| # | Defect | Status |
|---|---|---|
| 1 | **Filename drift** — day 0 `yti_gate_schedule.html`, day 1 `yti_gate.html`. A differ keyed on filename invents a delete+recreate. | **Fixed.** Slugs frozen in `bin/capture_ledger.py`; `INDEX.json` remaps the three banked days onto them. |
| 2 | **Maersk dropped on days 1–2** — the one source with verified erasure, therefore the one that cannot be back-filled. **Confirmed unrecoverable** (404 on both dates). | **Fixed forward.** The tool now discovers the live edition by walking back 21 days. The two lost days stand as a worked example of the premise. |
| 3 | **No RFC 3161 tokens on days 1–2.** | **Fixed, honestly.** `INDEX_ROOTS.txt` timestamped by freetsa/DigiCert/Sectigo at 16:15 UTC on the 21st. That proves those bytes existed **by the 21st** — not on their capture dates. Only 19 Aug has a same-day token. Days from the 22nd are tokenised same-day. |
| 4 | **Root mislabelled `daily_merkle_root_sha256`.** Recovered by search: a **flat concatenation** of the six files in capture order. | **Fixed.** Real Merkle root, odd nodes promoted not duplicated, inclusion proof per source — all six verified against the live root end-to-end. See `THE PROOF-GRANULARITY LAW`. |

### And a fifth thing, which is the one that changes the candidate

Parsing the three captures as **content** rather than bytes overturned which page carries the transient fact.
**The gate schedule diffs to one changed line in 172 — the date stamp.** It is a static forward calendar and
it is not the product. **The closed-area matrix changed 18 lines of 30 in two days**, and the window overlap
shows published days being *revised*, not merely aged out. My earlier correction to the founder was right that
the gate schedule was not scarce; **it did not go far enough, because it never named the page that is.**

*(Also corrected: the `75,2%` email rate in `GATELEDGER_Business_Overview.docx` is FMCSA property **brokers**.
Motor carriers measure **29,6%**. The docx has been patched in place and re-verified.)*
