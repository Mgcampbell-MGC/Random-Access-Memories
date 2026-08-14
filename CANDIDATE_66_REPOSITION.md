# CANDIDATE 66 — REPOSITIONED: exception repair, not content generation

**14 Aug 2026. Prompted by an external LLM's Nuvemshop finding. Verified independently on three
platforms. This kills half of candidate 66 and improves the half that survives.**

---

## 1. What I verified

| Platform | Its own AI does | Free? | Bulk? | Touches structural data? | Overwrites bad data? |
|---|---|---|---|---|---|
| **[Shopify Magic](https://pagefly.io/blogs/shopify/shopify-magic)** | Text generation, image editing, Sidekick, 8 languages | **100% free, all plans, no usage limits** | **No — one product at a time.** 400 products = 400 manual runs | No | — |
| **[Nuvemshop](https://atendimento.nuvemshop.com.br/pt_BR/adicionar-um-novo-produto/como-completar-dados-dos-produtos-em-massa-com-inteligencia-artificial)** | SEO title, meta description, tags, description, alt text | Not disclosed | **Yes — 20 at a time** | **No.** Explicitly not variants, attributes, categories, dimensions or weight | **No** — *"If a field already has information, AI will not modify or replace it"* |
| **Amazon Gen AI Listing** | Titles, bullets, descriptions, category selection from an image or URL | **Free in Seller Central** | Partially | Picks a category; not variation structure | — |

## 2. The kill, stated plainly

> **The content-generation half of candidate 66 is now free, from the platform, at zero marginal
> cost to the merchant. LAW 1 fires on it.**

Selling "we write your product descriptions and SEO fields" against a free, unlimited, native
Shopify feature is not a business. My one-page overview led with exactly that, and it was wrong.

## 3. The boundary that survives — and it is structural, not a matter of quality

Read the three rows above together and a hard line appears. **Every one of these tools generates
text into a product that already exists in the platform, filling blanks it can infer.** None of them:

1. **Works before the product is in the platform.** The failure happens *at import*. A free AI
   cannot fix a CSV that will not upload.
2. **Touches structural data** — variants, parent/child SKU families, attribute schemas, category
   mapping, dimensions, weight, GTIN, image-to-variant relationships. Nuvemshop says so in writing.
3. **Repairs data that is already wrong.** Nuvemshop fills empty fields only. **A catalogue full of
   *bad* data is invisible to it.**
4. **Resolves contradictions.** Two supplier spreadsheets disagreeing on a dimension is not a
   generation problem — it is an evidence problem, and no model can safely pick a winner.
5. **Deduplicates.** Reconciling product identity across rows is structural, not textual.
6. **Supplies facts it cannot know** — exact measurements, material composition, barcodes, country
   of origin, certification numbers. *(This is Prateleira Perfeita's "Pendências da Dona", and it is
   the same insight arrived at independently.)*

> ### THE REPOSITION
> **The platforms' free AI writes what is missing. It cannot fix what is broken.**

## 4. The new product

**Catalogue exception repair.** The seven exception classes, which is what the external LLM
proposed and what the platform documentation independently confirms is out of scope for their tools:

- Broken variants and SKU families
- Conflicting supplier spreadsheets
- Failed imports
- Missing mandatory marketplace attributes
- Duplicate products
- Bad image-to-variant relationships
- Source data AI cannot safely infer

**Content generation stays in the box — but as an included by-product, never the headline.** It is
now a feature the customer could get free elsewhere, so it cannot carry the price.

## 5. Why this is a better business than what it replaces

| | Content generation | Exception repair |
|---|---|---|
| Free platform substitute | **Yes — Shopify Magic, Amazon, Nuvemshop** | **No, and the platforms have documented it as out of scope** |
| Buyer urgency | "Would be nice" | **Blocked revenue today.** A failed import is an emergency |
| Resistance to automation | Low — it is generation | **High — it needs evidence and judgement, not fluency** |
| Blame risk | High: subjective quality | **Lower: it either imports or it does not.** Success is binary and provable |
| Price tolerance | Anchored on a free tool | **Anchored on the sale being blocked** |
| Repeat trigger | Every new product | **Every import, migration, marketplace expansion and season** |

**The binary success criterion is the underrated part.** "Your file now imports without errors" is
verifiable in one click, which is exactly what a faceless supplier with no reputation needs to sell
from a page.

## 6. What changed in the plan

- **The headline offer becomes repair**, priced against a blocked launch rather than against a
  copywriter.
- **The $149 sample becomes a diagnostic**: run their file, return the exception report — every
  break found, classified, with what it will take to fix. **That is worth paying for on its own,
  and it is the perfect no-call first purchase.**
- **The validation layer is still the asset**, but it is now aimed at detecting breakage rather
  than at composing text.
- **The one-page overview and the pricing ladder both need rewriting** on this basis.

## 7. Corrections issued to the running agents

All three affected agents were redirected mid-flight rather than allowed to finish on the old brief:

- **Competitor agent** — new mandate: map every platform-native AI on five axes (free? bulk?
  structural? overwrites? works pre-import?), and sweep an entirely new market — who sells import
  rescue, migration cleanup, duplicate repair, suppression fixes, and at what price.
- **Platform agent** — the failure catalogue is promoted to primary deliverable, plus a new section
  splitting every required field into *AI can safely produce it* versus *requires a fact AI cannot
  know*. That split is now the core of the business case.
- **Buyer agent** — pain quotes retargeted from content complaints to structural breakage:
  failed imports, duplicated products, orphaned variants, suppressed listings, mangled migrations.

**Instruction given to all three: if any platform's own AI does handle structural repair, that is a
kill finding and must be reported plainly and early.**
