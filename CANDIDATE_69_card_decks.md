# CANDIDATE 69 — THE CARD DECK. Assembly 1's survivor, with verified unit economics

**17 Aug 2026. Agent 2 of 10. Six carrier categories examined; one survives, and it survives on the
exact test that matters.**

---

## 1. The finding

> **A deck of 54 cards where each card carries one written prompt, question or exercise. The value lives
> entirely in WHAT THE QUESTIONS ARE AND HOW THEY ARE SEQUENCED — which is writing and editing, not
> illustration. The design requirement collapses to one background and one typeface, repeated
> fifty-four times.**

That is the whole reason it survives. **It is the only category found where text is the payload AND
manufacturing exists at quantity one** — no minimum, no setup fee, in the buyer's own country, from
**two independent suppliers**.

### Verified unit economics, quantity 1

| Supplier | Product | Cost | Ship | **Landed** | Plant |
|---|---|---|---|---|---|
| **Printful** | Poker Playing Cards, 52+2, acrylic box, 305gsm | $13,69 | $6,49 | **$20,18** | **US, US-sourced blank** |
| **The Game Crafter** | 54-card deck + Poker Hook Box *(incl. $0,89/copy handling)* | $12,25 | **UNVERIFIED** | **$13,14 + ship** | **Madison, Wisconsin** |
| The Game Crafter | 54-card deck + Poker Tuck Box | $14,82 | UNVERIFIED | $15,71 + ship | US |
| The Game Crafter | Same deck at quantity 100 | — | — | **$7,36** | US |

**Method note, because it matters:** Printful's v1 catalogue API is unauthenticated, and The Game Crafter
embeds its entire 202-product price book as JSON in its pricing page. The agent validated TGC's cost
formula against three of their own published worked examples before using it. **These are computed from
the suppliers' own published data, not estimated.**

**Printful is the one to start with:** US plant, US blank, and **it plugs straight into Etsy with no
manual step.** TGC is cheaper on manufacturing with far more format freedom, but requires manual ordering.

### Two things that bite

1. **The Game Crafter will not ship to Brazil** — their own words: *"we are not able to ship to Brazil,
   due to restrictions on game-related items."* She can drop-ship to US buyers freely, but **she can
   never hold a physical proof of her own product.** Printful does not have this problem for US orders.
2. **TGC shipping rates are UNVERIFIED** — they publish methods, not prices. **Every TGC landed figure
   above is incomplete and understated.**
3. Printful's puzzles, cards and books are **US-only** (`availability_regions: {"US"}`). Printful has a
   Brazil facility but it does not make any of them.

**Payment shape is unchanged and safe:** Printful never pays her — she pays Printful, which charges her
Wallet for fulfilment while customer money arrives through Etsy's Brazil payout. Same structure as Lulu,
so **no new payment-rail risk.** She does need an international card that works.

---

## 2. A cost finding that changes the existing book candidate

> **The Game Crafter Digest Perfect Bound Book, 40pp, 5.375×8.375" — $11,45 + $0,89 handling = $12,34
> all-in, against the Lulu reference of $21,32.**

**That is roughly half.** A paper carrier that was never priced, in the category she is already in.
Letter-size 40pp is $12,99; a 40pp Jumbo Booklet is $8,44. Caveat: **TGC shipping is still unpriced**,
and TGC cannot send her a sample.

---

## 3. Newspaper Club — prior data confirmed exactly, and a disagreement settled

The agent found Newspaper Club's AJAX price endpoint and queried it directly with a US session
(*"Prices include delivery to the United States. Duties and taxes included."*).

| Digital Tabloid | 1 copy | 10 | 70 | 100 | 200 |
|---|---|---|---|---|---|
| 4pp | $67,00 | $84 | $168 | $213 | $348 |
| **8pp** | **$74,00** | $101 | **$267** | **$348** | $606 |
| 12pp | $75,00 | $114 | $365 | $486 | $824 |
| 16pp | $77,00 | $126 | $456 | $606 | $1.021 |

**Every prior figure in this file checks out**, and the long-running $267 disagreement is resolved:
**$267 is 70 copies at 8pp, not 100 copies at 4pp** — that cell is $213. The agent who said 70@8pp was
right; the competing claim was wrong.

**But the number nobody had quoted is the one that decides it: a single 8pp copy costs $74,00.** For a
bespoke one-per-customer product — the only quantity a personalised business ever orders — that is
**~3,5× the Lulu reference.**

> **The format punishes exactly what writing needs, which is pages.** Going 8pp → 16pp at 100 copies
> costs **+$258**, while adding thirty more copies costs **+$81**. A plain Bookvault paperback delivers
> **40 pages for less than Newspaper Club's 8**. **The moat-giving axis is the expensive axis.**

Plant is Glasgow — a single UK plant, so goods do cross a border, though NC absorbs duties commercially.

---

## 4. What died, and why — the writing-versus-design test applied

| Carrier | Verdict |
|---|---|
| **Puzzles** | **Design-dominant, fatal.** A jigsaw is an image the buyer destroys and rebuilds. Text is either a one-sentence reveal — *one sentence is not a craft* — or unreadable. Printful 252pc lands at $20,64, so cost was never the problem |
| **Fabric & wallpaper** | **Design-dominant.** The product is a repeating surface pattern, and typographic patterns *are* design skill. Compounded: Spoonflower is a **10% royalty public catalogue with US-only plants** — the identical structure already killed for Canva, Envato and Adobe |
| **3D-printed objects** | **Value is geometry, and the skill is CAD — further from writing than design is, not closer** |
| **Engraved / laser goods** | Ceiling of roughly twenty words. An inscription is not a body of writing. **And Printful has no engraving category at all** — a keyword scan of all 531 catalogue products found none, so the named carrier does not exist for this |
| **Board games** | Value is **mechanics** — systems design — plus art. Not prose. And the minimums close it before the argument matters: **PrintNinja 500 units, no exceptions** (*"we don't offer any items at all at lower than 500 unit quantities"*); **Panda 1.500 units** *(from a search extract, not a page read — but an order of magnitude beyond her either way)* |
| **Newspapers** | **Thesis correct, arithmetic fatal.** See above |

---

## 5. What is still unpriced — read before using any of this

The agent was explicit about its own gaps, unprompted:

- **Mixam is unpriced** — 403 on every route, and the session's search budget hit 200/200. **It runs a US
  plant and accepts single copies, making it the one genuinely unresolved competitor and the
  highest-value re-run.** *(Not re-run: the newspaper verdict is already fatal at $74/copy at quantity 1,
  so Mixam could only revive a category that fails for a second independent reason.)*
- **TGC shipping unpriced** — every TGC landed cost above is understated.
- **Seven carriers priced at zero:** Spoonflower, Printify, Gelato, Craftcloud, Sculpteo, JLCPCB, PCBWay.
  Gelato and Printify are auth/JS-gated; Cloudprinter states outright there is *"no set price list since
  the 170+ print partners are all over the world."*
- **Printful Softcover Photo Book page count unknown** — $7,95 buys an unverified number of pages, so it
  is not comparable to Lulu's 40pp.
- **Shapeways filed Chapter 7 on 2 July 2024** and relaunched 3 December 2024 at its original Eindhoven
  facility. **Present-day operating status unconfirmed.**
- **Craftcloud** is the only carrier that genuinely distributes manufacturing globally (150+ makers, 95
  countries, *"tailored to your location"*) — but it is a **buy-side quote broker** with no documented
  seller-side white-label drop-ship or API.

**And the agent's own closing warning, honoured here:** *"I asserted no saturation figures and no Etsy fee
figures. Do not let anyone convert these unit costs into a monthly order count without checking those
separately."* **No order-count arithmetic appears in this file for that reason.** The saturation question —
is the conversation-deck market crowded — is agent 1's job, still running.

---

## 6. Where this leaves Assembly 1

**The assembly's premise held.** The object genuinely did not have to be a book, and the reason a book
was chosen was never examined until today.

**But it narrowed to exactly one alternative object.** Five of six carrier categories are design- or
engineering-dominant, which is fatal for a non-designer regardless of print cost. The survivor is the
card deck, and it survives because a deck is **a container for fifty-four short pieces of writing** —
structurally the same asset as a book, at **$20,18 landed instead of $21,32**, with the same channel, the
same engine, and one act of writing sold as one object.

**What it does NOT yet have** is a demand answer. Unit economics are verified; **the market is not.**
Whether written conversation decks sell above $50, whether the winners are writing-dominant or
design-dominant in practice, and whether any *personalised* written deck exists anywhere — all three are
agent 1's questions and all three are still open.

**Ranked verdict from the carrier work:**

1. **Card decks** — Printful first for the Etsy automation, TGC as the cost and format upgrade later
2. **TGC books and booklets** — a real cost advantage over Lulu on softcover; same business, cheaper
3. **Newspapers** — thesis right, arithmetic fatal at quantity one
4. **Everything else** — design- or engineering-dominant, fatal for a non-designer
