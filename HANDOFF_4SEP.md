# HANDOFF — 4 Sep 2026

## What is safe, and what is not

**SAFE FOREVER: this repository.** Every finding of the last two days is committed and pushed to
`claude/volta-architecture-design-txe8r5`. Nothing below depends on a running process.

**SAFE ONLY WHILE THIS SESSION AND ITS CONTAINER LIVE:** the three in-flight workflow runs. Their journals sit
under `/root/.claude/projects/…/9aef20de-742c-52a2-b11a-a33d815230ea/subagents/workflows/` — that path carries
**this session's UUID**, so a *new* session cannot resume them. **They survive a container restart** *(proved
today: the re-screen went 15 → 43 → 69 across one)*, **but not a new session.**
⇒ **Their partial results are therefore already banked into `THE_RESCREEN_PARTIAL.md`. Nothing important is
trapped in a journal.**

## ⏸ STOPPED CLEANLY, 4 Sep — all three runs halted at the founder's request

Partial output banked before stopping: **`THE_RESCREEN_PARTIAL.md`** (60 verdicts) and
**`THE_PARTIAL_HUNTS.md`** (22 unscreened candidates from the random-collision and 12-lens generate stages —
raw leads, never screened or refuted, and they must be treated that way).

## To resume, in this session

```
Workflow({scriptPath: ".../workflows/scripts/graveyard-rescreen-c1-wf_5575e13e-85e.js",   resumeFromRunId: "wf_5575e13e-85e"})
Workflow({scriptPath: ".../workflows/scripts/sol-random-collision-hunt-wf_540362ac-50c.js", resumeFromRunId: "wf_540362ac-50c"})
Workflow({scriptPath: ".../workflows/scripts/sol-wide-hunt-c1-retired-wf_94bc67ed-6b2.js",  resumeFromRunId: "wf_94bc67ed-6b2"})
```
Completed agents replay from cache instantly; only the unfinished ones re-run.
⚠ **If a resume is refused with *"ended but its run has not exited yet"*, call `TaskStop` on the task id first.
If it stays wedged, write a v2 script with the completed results embedded** — done twice today, it works.
⚠ **Do NOT edit these scripts' BRIEF text to remove CARTA. The brief is in every agent prompt, so any edit
invalidates the whole cache and re-runs everything. Their judges will recommend a dead candidate; correct it in
the write-up instead.**

## To resume in a NEW session

**Don't.** Re-launch fresh hunts if wanted. The three scripts are committed under
`workflows/scripts/` in the session dir only — **if they matter, copy them into the repo first.**

## Where the search actually stands

**No validated candidate. Zero buyer conversations in four weeks.** That is the honest headline.

**Dead or wounded today:** CARTA (a US consulate certifies the same passport copy for **US$50**) · #64 BEFORE
YOU (differentiator is now free inside a US$99 product) · CAMPO wounded (Brazilian *correspondentes* attend an
address for **R$370**).

**Three categories closed with sources:** Brazilian SaaS · Brazilian information products · faceless
attention/YouTube.

**Still standing, all unvalidated:** `CONFERÊNCIA DE CRÉDITO` *(the file says it was "never killed on
evidence")* · the **scan keepsake machine** *(built; the only candidate whose test needs no counterparty)* ·
15 MARGINAL from the re-screen.

## The five findings that outlive every candidate

1. **★ 72% of re-screened kills are THE FREE FRONT DOOR** — 29 of 40, holding on a doubled sample. **The
   binding constraint was never speech, the target, her hours or her capital. It is that somebody upstream who
   earns margin on the future flow gives the artefact away.**
2. **THE ACCEPTANCE SCISSORS** — an accepted-liability product is backed by money (then anyone can offer it and
   search ranking wins) or by a scarce permission (then the issuer is a state and the state sells it at cost).
   **Ask what backs it, then ask what the backer charges to do it itself.**
3. **THE ORIGINATION-BUDGET TEST** — the real constraint is **~15–20 first conversations, ever**, not contract
   value. The US$3.000 ACV ceiling that capped every B2B candidate for three weeks had no source at all.
4. **THE STEADY-STATE KILL** — `N* = a/c`; a one-time US$3.000 cannot fund a subscription base, which decays
   geometrically to zero. **Screen recurring revenue on replacement rate, not customer count.**
5. **EIGHT INTERVIEWS OUTRANK EIGHTY CANDIDATES** — and eight is a *sample size for a convergence test*, not a
   sales target.

## The one thing I would do next

**Stop hunting.** Every hunt now returns the same structural answer, and the archive has diagnosed its own
monoculture three separate times. **Pick the strongest surviving candidate, write the 15–20 emails, and commit
to a numeric pass bar before sending any of them.** Measure the RATE — it predicts everything after it.
