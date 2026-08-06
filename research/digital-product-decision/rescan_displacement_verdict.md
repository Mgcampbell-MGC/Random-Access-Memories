I have what I need. Verification summary before the verdict:

**What I confirmed myself (direct fetch):**
- **Prop 65 notices** — live, no login. Detail page `2026-03832` names *Calvin Klein Corporation* + *Ross Stores, Inc.*, PFOA, filed 08/06/2026, noticing party Ecological Alliance LLC [VERIFIED]. Sequential AG numbering gives a hard volume count: 3,832 notices in 218 days = **~6,420/yr** [VERIFIED by arithmetic on the AG number]. **But the CSV export is broken** — returns a header row and zero data rows on two different queries [VERIFIED]. Enumeration is manual HTML pagination, 20/page.
- **OSHA establishment search** — live query returned named+dated records (*Southern Star Roofing*, 07/31/2026, NAICS 238160, TX) [VERIFIED]. FY2025 = 30,273 inspections, FY2024 = 34,221 — a **-11.5% decline**, not the 34,625 claimed [VERIFIED].
- **SEC adviser roster** — downloaded and parsed: **17,018 rows, all Firm Type=Registered**, 15,653 with a website, 14,761 US, filing months Mar 8,179 / Jul 2,082 / Jun 1,735 / Apr 1,572 / May 1,488 / Feb 1,256 / Jan 505 / Dec 84 [VERIFIED].
- **EDGAR** — 5,408 unique 10-Q filers in Q2 2026 alone [VERIFIED].
- **GAO-24-106173** — "about 40,000 single audits" FY2023; $1.17T severe+persistent findings [VERIFIED].

**Two claims that broke under fetching:**
- **SEC bulk Part 2A brochures stop at December 2024.** Latest file is `adv-brochures-2024-december.zip`; the page states post-Jan-2025 data is only on IAPD [VERIFIED]. ADV-Check's "pre-run at scale" flourish degrades to manual per-firm brochure pull.
- **FAC record-level data is key-gated.** Search UI is JS-rendered (0 table rows), both CSV endpoints 404, API returns `API_KEY_MISSING` [VERIFIED]. Key is free but I could not confirm record output → **UNKNOWN**.

**The finding that killed the front-runner:** CitationProof's flagship layer is already free. Three working, no-account FOM gravity-based penalty calculators, fetched HTTP 200: `mantid.ai/tools/penalty-calculator` ("Based on the FY2025 OSHA penalty schedule, Field Operations Manual", $16,550), `shiftarmor.net/osha-calculator` ("gravity-based penalty methodology from the OSHA Field Operations Manual… No account required"), `oshamap.com/tools/osha-fine-calculator` [all VERIFIED]. One of them is run by the **same $447 competitor as a free lead magnet** — whose product page is indexed with 6 named modules off the identical trigger to the identical buyer [PLAUSIBLE; site DNS-dead at fetch].

---

# VERDICT: (ii) DISPLACE — the winner is ADV-Check

## Why it clears the bar, with numbers

| Axis | DeckProof | ADV-Check |
|---|---|---|
| **B — list size** | ~2,400 named/dated/yr | **17,018 firm-deadlines/yr, 14,761 US, 15,653 domained — 7.1x**, parsed by me from the file |
| **C — recurrence** | per-event, *discretionary* (brand must re-buy a $7-16.9k ECRM session) | annual, **regulation-guaranteed** — Rule 204-1 forces all 17,018 to re-trigger every year |
| **D — corpus** | cost-sheet arithmetic | 60-80 item Part1↔2A↔CRS crosswalk + deficiency taxonomy; no free equivalent found |
| **A — anchor** | sunk cost (money already spent) | forward recurring deadline, but consequence is a probabilistic exam deficiency — **parity, not a win** |
| **Self-verification** | buyer checks arithmetic | **purer** — "Item 5.F says $412M, brochure Item 4 says $353M" is two quoted passages that disagree |

Beats on B and D with verified numbers, edge on C, parity on A. That is a displacement.

**The decisive arithmetic:** DeckProof misses target on its own list (W2: R$18-26k vs R$30k). ADV-Check's does not. 600-1,000 sends/month at 1.5-3% = 9-30 sales at $650 = **US$5,850-19,500/month** against a US$7,400-8,300 target — 11-13 sales/month sits mid-range, and 14,761 US firms gives ~14 months of runway before the list recycles annually.

**Buyer quality is the tiebreak nobody scored:** a sub-$1B RIA's CCO is an owner-principal — US, English-native, financially literate, already buying $500-900 compliance products self-serve, corporate card, no procurement. Best payer in the set. RIA in a Box publishes an article titled *"Does your RIA firm's Form ADV Part 1 match its Form ADV Part 2?"* — problem awareness is already high and no product does the check.

## Why each rival lost

- **CitationProof** *(strongest challenger; lost on T6/T4)* — best trigger in the entire set (30,273 named+dated, US public domain, no anti-scraping terms, verified by live query) and it beat DeckProof on A, B and D. But its paid core is given away free by three verified vendors, one of them the $447 near-rival, leaving a $497 product whose remaining moat is the secondary layer. **STRUCTURAL.**
- **NoticeBench 65** — **the self-verification trap, and it lands squarely.** Its two most valuable layers promise *"this label is legally correct"* and *"your case is worth $X"* — neither checkable by inspection, both pure borrowed authority, sold by a faceless foreign vendor into an active lawsuit. Verified biggest-in-class anchor and list (~6,420/yr) cannot rescue it. **STRUCTURAL.**
- **PressProof** — self-defeating: the MNPI sensitivity that blocks ChatGPT equally blocks an unsigned .html from an unknown cold-emailing vendor, and under SOX 302 the close-process toolset is a documented disclosure control. The buyer with the greatest need has the greatest policy barrier. Fails **T8**. **STRUCTURAL.**
- **SEFA Forge** — genuine runner-up, but list unverifiable by me (key-gated) and nonprofit/local-gov buyers are the worst payers with real PO risk against the approval-threshold test.
- **AbateProof** — T4 kill confirmed. **PackCheck UK / NoticeProof UK** — correctly NO; HSE list pages 500'd again for me, so UNKNOWN stands.

## Objections against ADV-Check, sorted honestly

**STRUCTURAL (accepted, priced in):** bulk brochures end Dec 2024, so brochure pull is manual per target — the same motion DeckProof already requires. Seasonality is real: Aug-Jan is thin (Jan 505, Dec 84), though Feb-Jul each carry 1,256-2,082 firms, so ~6 solid months plus a March mega-season.

**UNPROVEN (may not kill — each gets a test):** $650 acceptance; the ChatGPT floor; and the ~1/3 who outsource to COMPLY/SmartRIA.

## First test — US$0-200, under two weeks

Hand-run the check on **40 US firms** with Feb-Apr filing dates: take Part 1 values from the roster already downloaded, pull each brochure free from IAPD, diff by hand. Then cold-email those 40 quoting **their own mismatch**, selling nothing. Cost: domain ~$12 + mailbox ~$8 + free-tier contact lookup = **under $50**.

**Pass threshold:** ≥20 of 40 firms show at least one real Part1-vs-2A discrepancy (proves the pitch has ammunition), **and** ≥4 of 40 replies ask how it was found or whether they can buy it (10%).

**The one sentence that would flip me back to DeckProof:** if that hand-check shows fewer than ~30% of firms carry a real discrepancy, ADV-Check has nothing to put in the cold email and DeckProof's verified roster wins by default.