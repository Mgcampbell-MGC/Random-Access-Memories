# Assessment — "Digital Product Hunt V2", CotaMRO Exact and the other eight (10 Aug 2026)

**Verdict: the best external document received so far, and its lead candidate specifies away the
only part of itself that was defensible.**

## What the document gets right, and what to steal

It kills six of its own nine candidates with named competitors and real mechanisms — SerialParts
Relay (a US$15/month Shopify fitment app does the clean case; Zeitten does it in Brazil), the PT-BR
speech benchmark (Hamming ships the identical product and gives free stress-test calls), AgencySIM
(Airalo and Tourist eSIM give the reseller rail away free upstream), StudioSlot (Spotz at a 20%
service fee), Nuvemshop PostPurchase (Adalore free to install, and no public post-success render
slot in the SDK), COLA Route Intel (TTB publishes the registry and an Apify scraper prices
extraction by the thousand). Several of those would have cost us days.

**Two methods worth adopting outright:**

1. **Buyer-side proof of loss as an entry condition.** *"A paid-test account must show its own
   evidence: at least one prior late/lost quotation… with R$53.640 annual economic exposure, equal
   to three times the proposed annual subscription."* This is Gate 0 inverted — instead of us
   estimating whether the buyer loses money, the buyer produces the evidence before we build.
   **Apply this to The Expediting Desk immediately.**
2. **UNVERIFIED as a first-class status.** *"UNVERIFIED means the evidence was not found; it does
   not mean the claim is probably true."* Correct, and stricter than we have been.

**And it independently converged on our shape.** Written without sight of this repo, it chose
"local workflow software… transforms private inputs" over monitors and feeds, and its own
comparison notes CotaMRO *"transforms private inputs"* while the others package public triggers.
Three separate processes — the DeckProof resurrection, the female-market hunt, and this document —
landed on *compute on the buyer's own private files.* That is corroboration, not coincidence.

## Why CotaMRO Exact does not survive as specified

### 1. It deleted the moat in the name of safety — THE VISE, appearance #4

The stated boundary: **XLSX/CSV inputs only**; a customer-supplied *"strict local master containing
manufacturer, exact SKU, unit, price"*; **exact composite-key joins**; fails closed on duplicates,
unit conflicts and near matches; *"never infers equivalence, selects substitutes"* — the last of
these justified by **CONFEA Resolution 218/1973 and Lei 5.194/1966**.

An exact composite-key join between two clean spreadsheets is **Power Query's Merge Queries, and
XLOOKUP/PROCX** — built into software every distributor already owns, and into LibreOffice free.
The document concedes this in Q2 and then defers it to a bake-off.

The part actually worth R$1.490/month is the opposite: reading the RFQ that arrives as a PDF, a
photographed fax or a free-text email, and resolving *"rolamento 6205 2RS"* to a SKU. **That is
precisely the act the document forbids itself on CONFEA grounds.**

> **The legally safe version is a spreadsheet formula. The differentiated version is reserved.**
> Fourth appearance of the vise, after PRUMO/CFC, the ET corpus and Recurso/OAB.

### 2. THE PRECONDITION TRAP — a new failure mode, and it generalises

CotaMRO requires the customer to supply a strict master with exact SKUs, consistent units and
current prices, and to receive ≥30 code-rich RFQs a month.

**A distributor who maintains that master has an ERP that already quotes from it. A distributor who
does not is one the product rejects by design, because it "fails closed" on exactly their data.**

> **When a product's precondition is the discipline whose absence creates the problem, the qualified
> population and the needy population are disjoint.**

This is Gate 0's adverse selection inverted. There, the visible defect selected for organisations too
poor to pay. Here, the data-quality requirement selects for organisations that no longer have the
problem. Both times the qualifying signal and the buying capacity move in opposite directions.

### 3. Contrast with the two candidates that did survive

| | Input | Why it holds |
|---|---|---|
| The Expediting Desk | Free-text vendor emails, hundreds of inconsistent formats | Sixteen vendors shipped *fields*; ingestion is the unbuilt part |
| DeckProof | A PDF deck exported from Canva/PowerPoint | RangeMe computes a perfect margin **from numbers you type in** |
| **CotaMRO as specified** | **Clean XLSX with exact keys** | **Power Query merge** |

**The messiness is the moat.** It is the reason the incumbents in both surviving markets built a
field and waited for a human to fill it. CotaMRO removed the mess from its own inputs and kept the
join.

### 4. Competitor status, corrected

**Commanda is real and is not the competitor the document assumes.** Fetched: it centralises RFQs
from **Ariba, Coupa and Nimbi** into one dashboard and scores *"a probabilidade real de ganhar esse
RFQ"* — it solves **which RFQs to bid**, from the portals, which is the acquisition problem.
CotaMRO explicitly *"never logs into portals."* So they are adjacent, not identical — the document
over-weighted Commanda as a threat and under-weighted Excel, which is the actual competitor.

**Still unverified and load-bearing:** whether a Brazilian ERP the distributor already pays for
(ERPFlex, Bling, Omie, Tiny, Sankhya) imports an RFQ spreadsheet and emits an orçamento against the
price master. If one does, that is A5 and it ends the candidate outright.

## The other two shortlisted

- **Reg2Route** — RESEARCH ONLY is too generous. It passes our alert rule (the recipient profits by
  knowing, rather than being the subject of the alert). But ANVISA's portal and open data are free,
  Pure Global gives a device database away free, and the document concedes the valuable "fit" layer
  *"approaches professional market-entry judgement"* — the vise again, a fifth time, in the same
  document.
- **CrossHire Circle** — should be **KILL**, not RESEARCH ONLY. A two-sided exchange requires
  bootstrapping both sides from zero with no audience and no network. That is the constraint trap in
  its purest form, and it is the one thing this founder structurally cannot do.

## The rescue, if the shape is worth keeping

Invert it, and it becomes the same architecture as the two survivors:

> **Read the messy RFQ — PDF, email body, photographed page — extract the line items, and present
> ranked candidate matches from the customer's own master for the seller to confirm with a click.
> The software does the reading. The human makes every equivalence judgement.**

That stays outside CONFEA for the same reason DeckProof stays outside any credential question: it
never asserts, it surfaces and the human decides. And it restores the moat, because reading a
photographed RFQ is the part Excel cannot do and the part no incumbent gives away.

**Before any of that, the document's own commodity test applies and should be run first:** seed a
synthetic fixture with the defects, send it to three freelancers; **two clean builds at ≤US$100 in
≤2 hours kills it unconditionally.**
