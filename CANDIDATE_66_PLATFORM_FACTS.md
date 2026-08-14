# CANDIDATE 66 — MEASURED PLATFORM FACTS

**Platform requirements sweep, 14 Aug 2026. Source: official seller documentation, with gaps
flagged honestly where the agent hit login walls.**

---

## 1. The finding that hurts: the platforms diagnose for free

**Every major channel ships a free, first-party validator that catches most of the failure
catalogue before anything goes live:**

| Platform | Free diagnostic |
|---|---|
| Google Merchant Center | Diagnostics / "Needs attention" — every disapproved product with its specific reason |
| Amazon | Listing Quality / Fix Stranded Inventory — every stranded ASIN with reason and recommended fix |
| Shopify | Attempt the CSV import — it fails loudly, specifically, and by row |
| eBay | Taxonomy API `getItemAspectsForCategory`, or just attempt to publish |

> **This weakens the $149 diagnostic sample as a product.** The platform already tells the merchant
> what is broken, free. **The diagnosis is not the value. The fix is** — and the sample must be
> repositioned as *"we fix ten of them and you keep the file"*, not *"we tell you what's wrong."*

**And every platform now ships a free generative listing tool** — Shopify Magic, Google Product
Studio, Amazon Generate Listing Content, eBay Magical Listing (bulk mode, hundreds of photos per
batch, US/UK/DE), TikTok "List with AI". They encode their own rules perfectly and update the
instant those rules change. **A third-party generator can only ever chase them.**

## 2. The finding that pays: nobody owns the crosswalk

The agent named the defensible layer better than I had:

> **Cross-platform reconciliation.** One merchant product record, mapped correctly into
> **five independently-versioned taxonomies at once** — Google ~6.000 nodes, Shopify 10.000+,
> **Amazon ~34.000+ (algorithmically assigned, silently reassigned, no public changelog)**,
> eBay ~20.000+, plus Otto's POSO schemas and Zalando's size-chart-code library.
>
> **They revise on uncoordinated schedules — Google alone shipped changes in Apr 2026, Jun 2026,
> and has more scheduled for Jan 2027. No platform publishes the crosswalk, because it is not
> their job to.**

**That is the moat: not knowing one platform's rules, but holding all of them simultaneously and
keeping them current.**

## 3. The divergence list — the same red T-shirt, eight ways

Concrete proof that "clean product data" is not one thing. Same product: a women's red cotton
crewneck, brand Aurora Basics, size M.

| Rule | The contradiction |
|---|---|
| **Title length** | eBay **hard 80 chars, input-rejected**. Etsy 140. Google 150 submitted, ~70 rendered. **Amazon 200 → a platform-wide 75-char cap with auto-truncation, enforcement begun 27 July 2026.** **TikTok Shop 40–150 — the only platform with a MINIMUM.** A title that clears TikTok's floor can already breach eBay's ceiling |
| **GTIN** | Shopify: optional, unvalidated. Google: required, and misusing the exemption is a **suspendable** offence. Amazon: waivable per brand+category. **Zalando: EAN required at the VARIANT level — a different EAN per size** |
| **Size and colour** | Amazon: brand-general text, **no gender qualifier** ("Medium", never "Women's Medium"), dominant colour only. **Zalando: a size-chart CODE from its own library — free text not accepted.** eBay: predefined value lists. Etsy: 20-char free text. **Four platforms, four incompatible data models for two words** |
| **Description** | **TikTok: minimum 30 words / 500 characters.** Google: 5.000 max, no floor. Shopify: no limit. A good 100-char Shopify description is an automatic quality failure on TikTok |
| **Images** | Amazon: **RGB(255,255,255) exactly**, product ≥85% of frame, automated scan. TikTok: white background, **≥5 images**. Otto: **minimum 3 per SKU**. Shopify: **no restriction at all** |
| **Language** | **Otto and Zalando require content natively written in German, not translated** — assessed at onboarding. Amazon and eBay treat language as a quality signal, not an eligibility gate |
| **Compliance fields** | **Bol.com requires manufacturer + EU responsible person on essentially EVERY listing** — its stated reason is that per-SKU risk determination is "practically unfeasible" at scale. Amazon flags only what its own risk logic catches. **Shopify, Google and eBay have no native field for this at all** |

## 4. Compliance is now a listing gate, not paperwork

- **Germany LUCID / VerpackG** — registration required before selling any packaged item, **no minimum-volume exemption**; Amazon is legally obliged to suspend non-compliant listings. Draft 2026 implementing law proposes fines to **€100.000** for serious labelling violations.
- **France** — Triman logo + Info-tri sorting instructions, and SYDEREP/Citeo registration; **Cdiscount gates onboarding on it**, while Amazon France quietly pays the eco-contribution itself. *Materially different enforcement postures for the same law.*
- **GPSR responsible-person data** — **Amazon FBA inbound rejected at the warehouse regardless of category.**
- **Pan-EU FBA now requires VAT registration in five EU countries** (up from four) as of Jan 2026.
- **EPR expands EU-wide by August 2026.**

## 5. The live forcing event

> **Amazon's 75-character title cap began enforcement on 27 July 2026 — three weeks ago.**

Every Amazon seller's titles are being auto-truncated right now. That is a dated, catalogue-wide,
mandatory rewrite affecting an entire marketplace, **currently in progress**. It is the single best
demand trigger surfaced in the whole sweep, and it needs verifying independently before anything is
built on it — the agent could not reach Amazon's login-gated style guides and flagged that its
secondary sources **disagree with each other** on the exact mechanics.

## 6. What the agent could not verify — recorded honestly

- **Amazon's real per-category style guides are behind the Seller Central login wall.** Every Amazon
  character limit above is triangulated from forums and secondary sources that conflict.
- **Otto and Zalando gate their real attribute schemas behind invite-only partner portals**, 4–12
  weeks to onboard. For those two, *"public search reproduces it in a weekend"* is false.
- **Enforcement behaviour is undocumented anywhere official** — which GTIN mismatch warns versus
  disapproves, which browse-node change requests get auto-rejected, what phrase patterns Amazon's
  claim scanner flags. That layer exists only as forum folklore and shifts constantly.

## 7. Its own verdict on difficulty, which I accept

> **"The skeleton — column names, character-limit tables, taxonomy sizes — is a weekend. The living,
> cross-platform, currently-accurate, edge-case-aware version a merchant would actually pay not to
> build is closer to a maintenance operation than a research project, precisely because the
> platforms keep moving the target faster than any static document stays true."**

**That sentence is the business.** It is also the warning: the asset only holds value if it is
maintained, which makes this a standing obligation rather than a one-time build.

## 8. What this changes

1. **The sample is a FIX, not a diagnosis.** Platforms diagnose free.
2. **The headline moves from "we clean your catalogue" to "one record, every channel, correctly
   formed"** — because the crosswalk is the only part nobody else owns.
3. **Compliance fields become part of the core deliverable**, not an add-on — they are now
   listing-gating in the EU.
4. **The Amazon 75-character event is the wedge to test first**, if it verifies.
