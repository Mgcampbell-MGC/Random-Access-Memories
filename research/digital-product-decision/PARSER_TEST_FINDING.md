# The parser gate cannot be run as specified — and what that changes

Run 6 Aug 2026, cost US$0, elapsed ~25 minutes. Raw data in `parser_test_results.json`.

## What the plan said

> Pull 20 public sell sheets from the 473 verified company domains already on disk.
> **PASS = clean numeric extraction of SRP, wholesale, case pack and margin on ≥15 of 20
> with no manual correction.** ≤12/20 → stop.

## Finding 1 — the corpus does not exist publicly

| Probed | Found |
|---|---|
| 152 reachable brand homepages | 12 link *any* PDF; **4** link a sell-sheet-type PDF |
| 110 brands' `/wholesale`, `/trade`, `/retailers`, `/catalog` subpages | **3** more |
| **262 brands total** | **7 sell-sheet-type documents** |

At ~2,7% yield, reaching 20 documents would need ~740 brands. Only 473 exist on the list.
**The specified US$0 test is not runnable from this source.**

Public sell sheets largely aren't published. They sit behind wholesale portals or travel as
email attachments — which is consistent with the premise that nobody checks them, but that
inference is speculation, not evidence.

## Finding 2 — of the 14 real CPG PDFs obtained, 2 are machine-readable

Criterion: an extractable text layer **plus** a price **plus** a case-pack or UPC.
pdfplumber reads the same embedded text objects pdf.js does, so a failure here is a failure
in the browser too.

| Outcome | Count |
|---|---|
| Text layer + price + pack/UPC | **2 / 14** |
| Text present but **no prices at all** | 9 / 14 |
| **No text layer whatsoever** — one full-page image per page, zero words | **3 / 14** |

Against a 75% gate, this is **14%**.

Two structural reasons, and only one is a parsing problem:
1. **Published catalogs deliberately omit wholesale pricing.** You request a price list. So
   "no prices" here is editorial, not technical.
2. **A real share are flattened images.** Documents 05, 09 and 13 return zero words across
   9, 52 and 13 pages — one image per page. Unrecoverable without OCR.

**Control, confirming the method is sound:** document 12 extracted cleanly —
`LONG RANGE $12.50 W/S ... GAMING EARBUDS $24.99 RETAIL EA` — 103 prices and 48 UPCs.
The extraction code works where the data is there.

## What this does and does not prove

**Does not prove the product fails.** A published marketing catalog is a different artifact
from an internal buyer-meeting deck. Decks are PowerPoint/Canva/InDesign exports and usually
*do* carry a text layer. The corpus I could assemble is **not representative of the product's
actual input.**

**Does prove three things:**
1. The US$0 gate cannot decide this. The question it was meant to answer is unanswerable from
   public data.
2. Image-only CPG documents are common enough in the wild to be a real failure mode, which is
   the exact direction the risk was predicted to fail in.
3. Any claim of "31 checks run" must degrade gracefully, because some share of real buyer
   inputs will be unparseable.

## The design change this argues for

**Make the spreadsheet the primary input, not the deck.** A cost sheet or price list is
`.xlsx`/`.csv` and is *always* machine-readable — SheetJS parsing is reliable in a way PDF
parsing is not. The deterministic engine still does its job: recompute margins, case-pack and
promo math from the sheet, then check the deck's claims against it.

PDF parsing becomes **opportunistic with a typed fallback**: *"3 slides had image-only numbers
— type them here."* That is graceful degradation instead of a dead product, and it removes
most of the parser risk without adding an approval step or buyer-side compute.

## The inversion this forces in the test order

The gating question was assumed to be *"can the parser read real decks?"* — answerable alone,
for free, in five days.

It isn't. The gating question is **"will a brand send its deck and cost sheet at all?"** — and
that requires contact with buyers.

**So the US$200 email test now comes first, and the build follows it.** That reverses the
recommended order. It also means the first real evidence costs US$200 rather than US$0 — worth
knowing before a week goes into a parser whose input distribution is unmeasured.
