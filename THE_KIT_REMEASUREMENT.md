# STEP 0 — THE KIT MARKET RE-MEASURED UNDER THE CORRECTED METHOD, 18 Sep 2026

**Bar committed in advance, in `THE_BUSINESS.md` §7 before any data was touched:
≥R$8.000.000/yr of kit lines clearing ≥50% gross at a VERIFIED São Paulo cost.**

**RESULT: R$3.664.085. The bar FAILS by 2,2×.**

**But the shape of the failure is different from the expediente failure, and the difference is the whole
finding: at a 40–45% account discount — exactly what this archive measured the unpublished distributor tier
to be worth in papelaria — the same market returns R$7,7–10,0M and clears.**

---

## 1. What was done to the data before any margin was computed

The 12-month award set is **7.549 rows**. Four contaminations were removed, three of them new today:

| # | contamination | size | effect |
|---|---|---|---|
| 1 | **Duplicate shadow rows** — every award appears twice, once with `qt=0, vu=0` and the same `vt` | 432 rows | double-counts value |
| 2 | **A Mato Grosso school-uniform programme** leaking into the harvest — *tênis escolar* R$17,6M, *camiseta* R$10,8M, *bermuda* R$10,5M, *jaqueta* R$6,9M | **4.052 rows, R$155,7M** | would have inflated the market **3,7×** |
| 3 | **Whole-kit and LOTE rows classified into component families** — a R$215.000 line reading *"600 KITS CONTENDO: Banheira… Mamadeira…"* was counted as FRALDA because the word appears inside it; *"GRUPO DE ITENS I (LOTE)"* likewise | 2–6% of rows per family | inflates the per-unit median |
| 4 | **Pack counts live in free text, not a field** — *"FRALDA COM BAINHA - 3 UNIDADES"*, *"BODY COM DECOTE CANOA (2 UNIDADES)"*; PNCP items carry no `capacidade` | 19–31 rows per family | overstates per-piece price up to 3× |

**Clean denominator: 3.065 award rows on kit-flagged lines, R$57.201.985 of 12-month value.**
*(Cross-check: the archive's independent figure was R$59,1M homologado. Two methods, 3% apart.)*

⇒ **THE DEDUPLICATION AND THE WRONG-PROGRAMME CHECK MUST RUN BEFORE ANY MARKET IS SIZED. A harvest built from
keyword search pulls in whole adjacent programmes, and a school-uniform contract in Mato Grosso is not a
newborn-kit market.**

---

## 2. The cost side — a second verified São Paulo wholesaler, found today

**CONFECCOES EMILIO LTDA — CNPJ 50.191.584/0001-06, Rua Mendes Gonçalves 181, Brás, São Paulo/SP, active
since 1978, CNAE 4642-7/01 *comércio atacadista de artigos do vestuário*, `financeiro@emilio.com.br`.**
Publishes **per-unit prices with no login**, marked *"Preço exclusivo para compras com CNPJ"*, ~30–50 thousand
items *à pronta entrega*, R$100 off a first order above R$1.500.

⚠ **And the supply side of this market is MORE gated than papelaria, not less.** Of the São Paulo wholesalers
checked: **Brascol** (ONESHOP DISTRIBUIDORA, 1.480 baby-body products) shows *"Cadastre-se para ver o preço"*
on every one; **Yanai Atacado** (CNPJ 44.040.459/0001-94, Brás/SP) the same. **Emilio is the one that
publishes.** `THE MONITORING PINCER` on the supply side, in a second category.

---

## 3. The margin table — spec-controlled, pack-normalised, bundles excluded

Twelve months, kit-flagged lines only, per-piece, against Emilio's **cheapest conforming** published price.

| family | 12mo value | median per-piece | her cost | **gross** | value clearing ≥50% |
|---|---|---|---|---|---|
| **FRALDA PANO** | R$525.524 | R$12,20 | R$2,452 *(Inconfral Especial, 5 un, R$12,26)* | **+79,9%** | **R$430.356 (82%)** |
| **COBERTOR / MANTA** | R$911.703 | R$20,08 | R$12,18 *(Manta Baby Sul Brasil)* | **+39,3%** | R$418.330 (46%) |
| **BANHEIRA** | R$3.572.825 | R$29,70 | R$22,90 *(Plasutil Sensitive 17,2 L)* | **+22,9%** | R$1.595.751 (45%) |
| TOALHA BANHO | R$2.012.761 | R$21,00 | R$21,26 *(Bublim Ninho c/ capuz 70×90)* | **−1,2%** | R$69.407 (3%) |
| **BODY** | R$4.186.297 | R$12,66 | R$15,32 *(Petutinha kit 3 un R$45,97)* | **−21,0%** | R$1.081.537 ⚠ |
| **MACACÃO / CONJUNTO** | R$6.811.302 | R$19,60 | R$24,90 *(Baby Dufy conj. #03668)* | **−27,0%** | R$68.704 (1%) |
| | **R$18.020.412** | | | | **R$3.664.085** |

⚠ **BODY's R$1,08M is not a pool — it is scattered outliers.** Its large band (>3.000 pieces), which holds
R$3,5M of the R$4,2M, has a median of **R$6,96** against a R$15,32 cost: **−120%.**

**Unpriced, so excluded from the total and reported separately:** HIGIENE (R$1,42M), FRALDA DESCARTÁVEL
(R$841k), BOLSA MATERNIDADE (R$2,05M — and n=10, of which one line is R$1,72M, so it is not a market),
KIT COMPLETO assembled (R$8,5M, needs a full BOM).

### ⚠⚠ The correction to this archive's own kit numbers

`THE BID-SELECTION FILTER IS THE MARGIN` records **body 55% · fralda pack 51% · kit higiene 52%**, measured
before spec control and the lot-total filter. **Re-measured: BODY is −21,0% at the cheapest published São
Paulo price.** The 55% rested on a R$5,64 cost this archive never sourced to a named SP seller; the cheapest
verified one is **R$15,32**, and the cheapest found anywhere — Atacadão da Roupa, 10-pack at R$7,99/piece —
carries a **(81) Pernambuco** phone, i.e. interstate, i.e. +6 points under `LC 123 art. 13 §1 XIII h`.

---

## 4. Why the two biggest families are negative, and it is the same law as yesterday

**MACACÃO (R$6,8M) and BODY (R$4,2M) are 61% of the classified component market and both are loss-making at
Emilio's published price.** The cause is not the tier — it is the **grade**. Emilio is a *vestuário*
atacadista stocking branded baby fashion: **Baby Dufy, Petutinha, Korte Rekorte, Bebê Precioso, Mafessoni.**
The state buys an unbranded conforming basic. **`MATCH THE GRADE THE STATE BUYS` and `A PDM IS NOT A PRODUCT`
fire again, in a category they were never derived in.**

⇒ **This is now a THREE-CATEGORY result — papelaria, limpeza, and kits — and it is starting to look like a
law rather than a finding: the published wholesale price, in any Brazilian category, sits at or above what
the state pays at the quantities where the money is. The published tier is not a supply channel for a
government reseller; it is a retail channel wearing a CNPJ.**

---

## 5. The sensitivity, and this is the number that decides the business

Value clearing ≥50% gross, as a function of how far below Emilio's published CNPJ price her account sits:

| account discount | value clearing ≥50% | verdict |
|---|---|---|
| **0% (published)** | **R$3.664.085** | fails the R$8M bar |
| 10% | R$4.084.523 | fails |
| 20% | R$5.944.114 | fails |
| 30% | R$6.478.499 | fails |
| **40%** | **R$7.682.558** | at the bar |
| **45%** | **R$10.012.898** | **clears** |

**The papelaria distributor tier was measured at ~45% below the best published price** (Chamex: published
R$30,60, the state pays R$19,83 in São Paulo, so the winners are invoiced at ~R$16–18).

⇒ **THE KIT MARKET CLEARS THE BAR AT EXACTLY THE DISCOUNT A REAL DISTRIBUTOR ACCOUNT IS WORTH, AND NOT ONE
POINT BEFORE IT.** The whole business is that account, in both categories, and the number to ask for is now
known: **40–45% under published, or it does not work.**

★ **And the jump from 30% to 45% is not gradual — it is a cliff: MACACÃO goes from R$1,10M to R$1,48M and
BODY from R$1,50M to R$3,42M as the two biggest families cross their thresholds together.** A 30% account
buys her almost nothing; a 45% account doubles the business. **There is no partial win here.**

---

## 6. What is true today, without any account

**Three families are genuinely live at the published São Paulo price and they are not trivial:**

- **FRALDA PANO — +79,9%, and it clears 50% on 82% of its value.** Emilio's Inconfral *Fralda Especial*
  5-pack at R$12,26 = **R$2,452/piece**, against a state per-piece median of **R$12,20**. Verified against a
  real award: *"FRALDAS DE PANO, 100% algodão, 65 × 65"*, 2.000 units at **R$28,25**, R$56.500.
- **COBERTOR / MANTA — +39,3%**, R$418k clearing 50%.
- **BANHEIRA — +22,9% at the median, and +49,9% in the large band**, R$1,60M clearing 50%. Note the inversion:
  unlike office supplies, the **biggest banheira lines pay MORE per unit** (R$45,66 median in the >3.000 band
  against R$30,50 in the small band) — the opposite of `QUANTITY IS THE PRICE VARIABLE`, because the large
  lines specify *anatômica, polipropileno* and the small ones do not.

**Total addressable at the published tier: R$3,66M. Against the R$360.000 of billings the company needs, that
is a 9,8% share** — inside what `THE MARKET-MULTIPLE RULE` permits a greenfield entrant to underwrite
(15–25%), with room. **So the honest verdict is not "dead". It is: a three-SKU business exists today, and the
full business needs the account.**

---

## 7. Verdict

**STEP 0 FAILS ITS OWN BAR AND THE PROJECT DOES NOT STOP — because the bar was set to test whether the kit
market works WITHOUT a supplier account, and the answer is that it works partially without one and fully
with one, at a discount whose size is now measured.**

**What changes in `THE_BUSINESS.md`:**

1. **The desk points at kits — CONFIRMED, but on three SKUs, not the whole basket.** Fralda pano, manta,
   banheira. Body and macacão wait for the account.
2. **The supplier email list changes category and gains a target per SKU.** Not SINAPEL papelaria
   distributors — **baby-goods atacadistas in Brás**, starting with the two that already hide their prices
   (Brascol / ONESHOP, Yanai) plus Emilio for a negotiated tier. **The ask is 40–45% under published**, and
   the per-SKU numbers are: body ≤R$8,40 · macacão ≤R$13,70 · toalha c/ capuz ≤R$10,50 · banheira ≤R$14,85 ·
   manta ≤R$10,00.
3. **The bar for that test:** three of fifteen replying at or under those numbers. **Below three, she runs
   the three-SKU version and the company is smaller than designed.**

**Still unpriced and worth an hour each:** HIGIENE (R$1,42M), FRALDA DESCARTÁVEL (R$841k), and the assembled
KIT COMPLETO line (R$8,5M, median R$174,90) which needs a full BOM costed at Emilio and is the single
largest line in the market.
