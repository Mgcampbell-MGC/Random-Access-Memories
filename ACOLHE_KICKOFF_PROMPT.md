# ACOLHE — what to paste into the new session

Copy everything inside the box. Nothing else. The handoff carries the detail.

---

```
Read ACOLHE_BUILD_HANDOFF.md in full before you do anything else. Then read
THE_KIT_DESK.md. Do not read any other markdown file in this repo — there are
177 of them and 174 are a graveyard of dead candidates that will burn your
context and teach you nothing.

Context: a four-week search produced one surviving business. ACOLHE sells
newborn layette kits to Brazilian municipalities. Lei 14.133 art. 54 forces
every town hall to publish what it is about to buy, with the exact item list,
on one free national API, before it can buy. Roughly four kit tenders are
published every working day. The research is finished. Nothing about the idea
is open.

Your job is to BUILD the machine and get it to the acceptance criteria in §12
of the handoff. You are not researching, not re-screening, and not looking for
a better idea. If you find yourself evaluating whether this is a good business,
you have misread the brief.

The founder is Sol — São Paulo, native Portuguese, not a developer. You are
building this for her to operate alone at about 20 hours a week. Her hard
constraints are in §2 of the handoff. C3 in particular: no employees and no
contractors, ever. You build it; you do not propose hiring anyone.

Work in this order:

1. START AT STEP 0 and do not skip it. It is half a day of catalogue work
   with no code: price the eleven unpriced items in the 17-item kit at the
   São Paulo wholesalers named in §9. The bar is committed in advance — BOM
   at or under R$200 and you build the full system; over R$230 and the thing
   to build is different. Report the number before writing any code.

2. Then build Steps 1 through 8 in order. Each has an acceptance test. Do not
   move to the next step until the current one passes its test.

Three rules that override your defaults:

- EVERY AGGREGATE YOU COMPUTE FROM A GOVERNMENT API IS WRONG UNTIL FILTERED.
  Nine separate measurement errors have already been made on this exact data,
  nearly all flattering, most by a previous Claude session. §6 gives the five
  mandatory filters and §7 the trap catalogue. Write the regression tests in
  tests/test_traps.py before you trust a single number, and make every report
  print the top five rows behind any figure it shows.

- VERIFY AT THE SOURCE, NEVER FROM MEMORY OR A SUMMARY. Fetch the actual
  endpoint, the actual PDF, the actual statute. Every number you add to the
  repo needs a primary-source URL, and anything you cannot confirm gets
  written down as UNVERIFIED rather than smoothed over. A flagged gap is worth
  more than a plausible figure.

- WHEN YOU FIND SOMETHING THAT CONTRADICTS THE HANDOFF, THE HANDOFF IS WRONG
  AND YOU SHOULD SAY SO. It was written from measurements taken days ago
  against APIs that have already proved unstable. Correct it in place and tell
  me what changed.

Ask me before: spending any money, registering anything, contacting any
supplier or buyer, or opening a pull request.

Start by reading the two files, then tell me your plan for Step 0.
```

---

## Why the prompt is shaped this way

**It forbids re-litigating the idea.** The single largest risk with a fresh session is that it reads a
graveyard file, gets nervous, and restarts the search. Four weeks and ~130 candidates already went
that way. The prompt closes that door in the second paragraph.

**It caps reading at two files.** 177 markdown files will eat a context window and return nothing
useful. The three that matter are named; the rest are explicitly out of bounds.

**It starts on the gate, not the code.** Step 0 is half a day with no programming and it determines
what gets built. A session that starts by writing a scraper has committed to an architecture before
knowing whether the margin exists.

**It pre-commits the bar.** R$200 / R$230 is written down *before* the number comes in, so the result
cannot be rationalised after the fact. This repo has a documented habit of crowning candidates the
same afternoon they are generated, and of burying them the same way.

**It inverts the default trust in data.** The measurement traps are the most expensive thing in this
project — a 36-point margin error from one wrong bathtub, a market sized 3,7× too large from one
regex. Telling the session up front that its numbers are wrong until filtered is worth more than any
amount of architecture guidance.

**It invites contradiction.** Both PNCP API families were failing intermittently at the moment the
handoff was written. Parts of it will be stale within a week. A session that treats the handoff as
scripture will build on sand.

## What to watch for in the first hour

| Good sign | Bad sign |
|---|---|
| It reads both files and summarises Step 0 back to you | It starts writing a scraper immediately |
| It asks which wholesalers to check first | It asks whether this is really the best business |
| It reports the BOM number plainly, including if it is bad | It reports a number without saying where each price came from |
| It says "the handoff says X, I measured Y" | It quotes handoff figures back as if it verified them |

## The one thing to say if it drifts

> Stop. Re-read §0 of the handoff. You are building, not researching. What is the current step and
> what is its acceptance test?
