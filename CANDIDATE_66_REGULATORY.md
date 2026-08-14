# CANDIDATE 66 — THE EU/UK REGULATORY ANGLE

**Measured 14 Aug 2026, primary sources, by an agent that then destroyed its own finding.**

> **VERDICT: the regulatory tailwind is largely NOT THERE. GPSR is a per-brand chore, not a
> per-product problem; Great Britain requires nothing in a listing at all; and the deadline passed
> twenty months ago. Three narrow things survive.**

---

## 1. What the law actually requires — and the granularity that kills the pitch

**Regulation (EU) 2023/988 (GPSR), Article 19**, applicable since **13 December 2024**, requires
every online offer to EU consumers to *"clearly and visibly indicate"*: manufacturer name and
postal **and electronic** address; the EU Responsible Person block where the manufacturer is
non-EU; product picture, type and identifier; and any warnings or safety information **in the
language determined by the Member State**.

**Article 4 makes it extraterritorial** — it catches any offer *"targeted at consumers in the
Union."* **Article 16(1)** extends the EU-established-responsible-person requirement from ~19 named
sectors to **all consumer products in scope**. Article 19 sits in Chapter III Section 2 and is
**never disapplied**, so it binds CE-marked goods too.

### Then the agent counted the fields properly, and the pitch collapsed

| Fields | Granularity | Consequence |
|---|---|---|
| 1–6: manufacturer identity + RP identity | **Per MANUFACTURER** | A merchant with 5.000 SKUs from 40 brands needs **40 records, entered once** |
| 7–9: picture, type, identifier | **Already in every live listing** | No merchant on Amazon or eBay lacks a picture and a model number |
| 10: warnings and safety information | Per SKU × per market language | **Art. 9(7) carve-out: not required at all "where the product can be used safely and as intended without such instructions."** For a T-shirt, mug, poster or phone case there is **no required warning in any language** |

> **Of ten listing fields, six are per-brand reference data, three are content the merchant already
> has, and one is per-SKU but frequently null. The "per-product data problem" does not survive
> contact with the article text.**

**And the platforms already built the forms.** bol creates the economic operator as **a profile with
a unique ID linked to products**; Allegro accepts responsible-person data *"through the My
Assortment tab, Allegro API, or from a file."* Reference-data flows — precisely the shape that
cannot sustain per-SKU billing.

## 2. The three pieces of evidence that close it

**a) The legislature that wrote the strictest version says it costs nothing.** Germany's own impact
assessment for the law extending German-language duties to Art. 19(d) listings:

> ***"Das Gesetz verursacht keinen neuen Erfüllungsaufwand für die Wirtschaft."***
> *(The law creates no new compliance burden for business.)* — classified as **"Sowieso-Kosten"**.

**If the government imposing the requirement assesses marginal cost at zero, marginal willingness
to pay is near zero.**

**b) Enforcement is a rounding error.** From the same official document, the predecessor regime:
**seven federal states, five years, ~110 administrative proceedings, fines of €200–9.000.** No
criminal cases. Germany is the EU's largest and most litigious product-safety market.

**c) The platform sanction is soft and self-healing.** **eBay's own words:** on supplying the data,
visibility restores with ***"no impact to that listing's history or search ranking."*** Account
action only for *"a relevant amount of listings"* or repeated violations after warnings.

> **Worst realistic outcome: temporary, reversible, regional invisibility. Merchants rationally
> wait until suppressed, then type an address into a form.**

## 3. Great Britain requires nothing — which halves the user's expansion request

**GPSR 2005 (SI 2005/1803) reg. 7(4)(a)** requires producer name, address and product reference —
***"by means of the product or its packaging"***, and only ***"except where it is not reasonable to
do so."***

> **There is no Article 19 equivalent in Great Britain. GB law regulates the product. It does not
> regulate the web page.**

**Amazon confirms it operationally:** *"For listings on Amazon UK-based store, you don't need to
submit any information"* (unless deliverable to Northern Ireland).

The **Product Regulation and Metrology Act 2025** is an **enabling act with no requirements made**;
the OPSS/DBT consultations only closed 23 June 2026.

> **So "EU and UK" is really "EU + Northern Ireland" — and NI is 1,9 million people.** A merchant
> building to EU spec is automatically over-compliant for GB. The reverse is not true.
>
> **UK remains a good MARKET. It is not a regulatory driver.**

## 4. The price anchor is already set, low, by vendors carrying real liability

| Vendor | Price | Scope |
|---|---|---|
| **REP27 / gdprrepresentative.com** | **€290/year** | Named EU Responsible Person, Art. 16(3) mandate, contact point in 8 languages, 10-year retention, **and "label wording guidance"** |
| **EU Compliance Partner** | **$500/year** ($300 first year) | RP certificate and address, **GPSR labelling guidance document**, packaging review, technical file template |

**The legally indispensable role — without which the product cannot lawfully be placed on the
market at all — clears at €290/year.** These vendors carry the liability, get first contact (the
seller must buy an RP *before* anything else), and are already drifting into advisory.

## 5. Digital Product Passport: no trigger exists

- **18 Feb 2027 battery passport covers only LMT, industrial >2 kWh and EV batteries — not the
  portable consumer cells a normal merchant sells.**
- **Textiles is an *adoption* target for 2027.** Ecodesign delegated acts customarily allow 18–24
  months, so merchant obligations land **around 2029–2030**.

> **Anyone selling "DPP readiness" to a general e-commerce merchant in 2026 is selling against a
> deadline three to four years out. No SME buys that.**

## 6. What survives — three things, stated as narrowly as the evidence allows

1. **GPSR Art. 12(1) puts an affirmative VERIFICATION duty on distributors** — they *"shall verify
   that the manufacturer and, where applicable, the importer have complied"* with Arts. 9(5)–(7)
   and 11(3)–(4). **A reseller carrying many third-party brands cannot discharge this from a form.**
   It must find each manufacturer's postal and electronic address and confirm the warnings exist in
   the right language. **The work scales with BRAND count, not SKU count.**
2. **Field 10 is real where warnings are legally mandated** — toys, electricals, chemicals,
   machinery, childcare articles. **Germany expressly extended the German-language duty to the
   listing (ProdSG § 6, in force ~19 Feb 2026) and made an Art. 19 breach an administrative
   offence (§ 28).**
3. **Both RP vendors explicitly EXCLUDE** *"product data creation or listing field population"* and
   *"individual per-product listing data creation for marketplaces."* **A verified gap — just far
   smaller than the regulation's surface area suggests.**

## 7. THE CHECK THAT DECIDES IT — and it reframes the customer

> ### `distinct(manufacturer) / distinct(sku)`
>
> **Ratio near 1:200** — a brand owner or a retailer with a few large suppliers → the obligation is
> ~40 rows entered once into a form the marketplace already built. **Opportunity destroyed.**
>
> **Ratio near 1:3** — a dropshipper, liquidator, marketplace reseller or long-tail distributor →
> hundreds of manufacturer addresses it does not have, under a statutory verification duty, with no
> bulk shortcut. **Opportunity confirmed — and it is a SUPPLIER-DATA RESEARCH service, not a
> listing-formatting service.**

**One CSV export and one line of code.** And it changes the target customer from *"merchants with
big catalogues"* to **"resellers with many brands"** — a different segment entirely.

**The second check, and note that both outcomes are bad news:** pull 50 live listings from non-EU
sellers on Amazon.de and count populated RP blocks. **High blank rate with listings still live =
enforcement is not biting and the urgency is fictional. Low blank rate = the work is already done
by someone else.**

## 8. What this changes in the plan

1. **The regulatory tailwind comes out of the core pitch.** It is a feature, not a driver.
2. **UK stays as a market, but the UK regulatory story is deleted.** GB requires nothing.
3. **If the compliance angle is used at all, it must target resellers with high brand counts** in
   warning-bearing categories (toys, electricals, childcare) — not merchants generally.
4. **DPP is not mentioned anywhere in the plan.** There is no trigger.

## 9. Gaps the agent flagged, honestly

Language determinations verified for **1 of 27** Member States. Zalando and Cdiscount pages not
obtained. Amazon's GTIN rules login-walled. Otto's deactivation policy is German trade press only.
The €100.000 German fine ceiling and the 19 Feb 2026 date are secondary. **And no verified instance
of any specific named listing being removed by any marketplace for GPSR non-compliance was found —
every such claim traced back to vendor marketing.**
