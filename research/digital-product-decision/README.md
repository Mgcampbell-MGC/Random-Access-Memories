# The decision: DeckProof

Outcome of a 9-agent run (6 Aug 2026) using mixed models — Sonnet for verification
lookups, Fable for design and the final call, Opus to red-team — under a corrected
filter that separates **structural kills** from **unproven-but-testable** questions.

| File | Contents |
|---|---|
| `DECISION_DeckProof.md` | The full proposal in nine sections |
| `red_team_verdicts.md` | Adversarial pass over all six candidates |
| `kill_record_five.md` | Graveyard entries for the five Phase 1 kills |
| `ecrm_rosters.json` | The enumerated buyer list: 475 companies, 473 with domains, across 93 sessions |

## The product

One self-contained `.html` file, opened by double-click. The buyer file-picks their
pitch deck and cost sheet; it recomputes every margin, case-pack and promo figure,
cross-checks every number appearing in both documents, and returns a findings report
plus **a corrected one-page buyer-facing economics sheet** they carry into the room.
Nothing uploads — COGS never leaves the machine. US$750.

## The trigger, verified twice

Their company is named on a **published ECRM seller roster** for a dated session they
have already paid US$7.000–16.900 to attend.

The roster lives at an undocumented parameter — `?rt=S` — because the default
`/Attendees` view shows only *buyers*. Independently re-fetched: HTTP 200, no login,
83KB of content, 56 named sellers with their own websites on a single session page.

```
https://ecrm.marketgate.com/Sessions/2026/10/LatinAmericaBeautyPersonalCare/Attendees?rt=S&a=1
```

93 sessions on the public calendar (Aug 2026–Sep 2027); 15 have published rosters and
78 read "posted in the near future," so rosters appear 1–6 months ahead. **A rolling
stream, not one event.** ~2.300–2.600 named, dated, domained brands/year.

**ECRM's Terms of Use prohibit scraping, harvesting and automated access.** So: manual
reading only — ~30 names off a public page per session, company domain from the roster's
own link, and the *person* sourced from Apollo or the company's own site, never from ECRM.

## Why this one

It is the only candidate whose **authority rests on nothing**. The output is
self-verifying: the buyer can check the arithmetic themselves. R4 — needing a credential
the founder cannot claim — killed more candidates than any other rule, and this one is
clean on it.

The R3 defence is threefold: arithmetic across a 30-slide deck plus a workbook is where
language models are measurably unreliable, and a confidently wrong margin recited to a
Kroger buyer is worse than no answer; the retailer-requirements corpus is a genuinely
bundled dataset; and the cost sheet is confidential, so the prompt route means pasting
COGS into a chatbot.

## The honest economics

**Year one plausibly averages US$4.500–6.500/month ≈ R$18–26k/month — below the
R$30.000 target**, crossing it as a run rate around months 8–10 *if* the warm tier
performs. ECRM alone is a US$24–36k/**year** business: worth launching, not target.
Reaching target needs the warm tier (Expo West, Fancy Food, Cosmoprof NA exhibitor
lists) converting at ~1,5%.

Capital at risk before the first sale: **under US$220.**

## The first test — and it is not willingness to pay

**The parser, days 1–5, cost US$0.** Everything downstream is conditional on
deterministic extraction actually working on real CPG sell sheets. If it fails, the
product becomes a data-entry form and the R3 defence evaporates.

Pull 20 public sell sheets from the 473 domains already on disk.
**PASS = clean extraction of SRP, wholesale, case pack and margin on ≥15 of 20 with no
manual correction, AND ≥1 genuine arithmetic discrepancy found.**
≤12/20 → stop, switch to the runner-up.

**Then days 6–14, under US$200.** 200 hand-read sellers from published Aug–Oct rosters,
subject line naming their actual session and date, free single-page checker as the
opener, US$750 as the price. **PASS = 2+ paid presales, or 6+ replies asking price.**

Kill-signals in the replies: >30% saying "my broker handles this"; anyone saying the
retailer's own portal already checks the numbers.

## The one structural kill

**ANNEXCHECK** (EU/UK cosmetics annex screening) died on A5. A Responsible Person is
*legally mandatory* to sell cosmetics in the EU/UK, costs £490–690/year, and the
contracted scope already includes "ongoing horizon scanning for new legislation,
guidance, and data that impacts product compliance." The buyer cannot *not* own the
substitute. The other four survive as unproven-but-testable and are ranked in
`red_team_verdicts.md`.

## What nearly went wrong

The red team's first roster parser required a `(Country)` suffix that US-domestic
sessions omit. It returned `sellers=0` for every US session, and the analysis was one
step from killing the winner on volume. Manual inspection of one roster caught it. The
zeros were a bug — 292 of the 475 companies are exactly those untagged US-domestic
entries. **A false kill leaves no trace, which is why it costs more than a missed risk.**
