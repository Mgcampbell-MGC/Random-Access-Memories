# CANDIDATE 66 — CROSS-BORDER MONEY

**Measured 14 Aug 2026. Brazil-registered CNPJ selling to US/UK/EU businesses.**
**Headline: it works, the tax position is unusually good, and the payment rails have one trap.**

---

## 1. The Brazilian position is better than I assumed

**CNAE:** 6311-9/00 *tratamento de dados* is the fit (alternatives 6319-4/00, 8219-9/99). All are
ordinary Simples service CNAEs governed by Fator R.

**Fator R, worked at RBT12 = R$300.000:**

| | Effective rate |
|---|---|
| **Anexo V** (pró-labore under 28% of revenue) | **16,5%** |
| **Anexo III** (pró-labore ≥28%) | **8,08%** |

To reach Anexo III at that revenue she must draw **≈R$7.000/month as pró-labore**, which carries
11% INSS on her side. Real cash, not a paper election, and it must be monitored monthly.

**And then the export exemption stacks on top — this is the finding that matters:**

> **Export revenue segregated in the monthly PGDAS-D strips ISS, PIS and COFINS out of the DAS
> calculation entirely** (Resolução CGSN 140/2018 art. 25 §4). **The effective cash rate on export
> revenue is therefore LOWER than either table above** — only the IRPJ/CSLL/CPP shares remain.

The exact residual per-faixa split needs a PGDAS-D simulation from an accountant. **This is the
single most favourable fact in the whole assessment and it should be quantified before the plan is
finalised.**

**Legal basis:** ISS — LC 116/2003 art. 2 I (item 1.03 of the lista covers *processamento de
dados*). PIS/COFINS — MP 2.158-35/2001 art. 14 III, Lei 10.637/2002 art. 5 II, Lei 10.833/2003
art. 6 II, conditioned on service to a non-resident **and an actual ingresso de divisas**.

**Tax reform:** **exports are constitutionally IMMUNE to CBS and IBS** under LC 214/2025 arts. 80–82,
*"independentemente do setor económico."* 2026 is a calibration year only — CBS goes live 2027,
ISS/ICMS extinguished 1 Jan 2033.

### The one real legal risk

> **The ISS export exemption rests on the "resultado" test in the parágrafo único of LC 116/2003
> art. 2 — and "resultado" is not statutorily defined. It is litigated case by case.**

For a file consumed entirely by a foreign business abroad the argument is strong, but **it is not
black-letter law**, and a municipality could challenge it years later. **A domestic-only seller
never carries this risk because it never claims the exemption.** Needs a contador's sign-off on the
specific fact pattern before scale.

## 2. Payment rails — and the trap

| Rail | Works for a BR CNPJ? | Real cost |
|---|---|---|
| **Wise Business** | **Yes** — native multi-currency, real USD/GBP/EUR account details | R$250 setup; **free to receive on domestic rails**; SWIFT $6,11 / £2,16 / €2,39 flat; conversion from 0,4% |
| **Husky (by Nomad)** | **Yes**, built for PJ | **Up to 1% to receive, and 0% stated specifically for service-export receipts** |
| **Stripe** | Yes | **3,99% + R$0,39, +2% international cards, +2% FX ≈ 6–8% blended.** Native USD settlement for BR accounts **unconfirmed in Stripe's own docs** |
| PayPal | Yes | **6,4% + R$0,60 + 3,5% FX + 4,5% on withdrawal ≈ 9–10%.** Avoid |
| BTG / Inter PJ international | Yes | ~US$10 flat per wire. Good for wires, weak for checkout |
| **Nomad** | **No** — PF only, routes CNPJ to Husky | — |
| **Mercury** | **No** — requires a US-registered entity | — |

### The trap: the cheap rail and the cheap ticket do not overlap

> **A flat $6–10 wire fee is 0,2% of a $5.000 job and 4–7% of a $149 job. Card rails are the
> reverse — 6–10% regardless of size.**

**So collection must be two-tier by design: cards for small jobs, wire/Wise above a threshold.**
That is a product decision, not a finance detail, and it argues for **fewer, larger jobs** — which
is the same direction every other agent has pointed.

## 3. VAT — she registers nowhere, and that is by design

- **UK B2B:** reverse charge under VATA 1994 s.8. **No UK registration.** Invoice must carry
  reverse-charge wording and **show no VAT amount**.
- **EU B2B:** Article 44 + 196 of Directive 2006/112/EC. **No EU registration.** Invoice needs the
  full Article 226 element set, **the customer's VAT ID**, and the words **"Reverse charge"**.
  **CJEU C-247/21: omitting that wording cannot be cured after the fact.** Validate every VAT
  number in VIES and keep dated proof (Reg. 282/2011 art. 18(1)(a)).
- **US:** no withholding — services performed entirely in Brazil are foreign-source. Customers will
  ask for a **W-8BEN-E** as their own audit defence, not as a precondition. **No US–Brazil tax
  treaty exists** — confirmed, and moot for this fact pattern. Texas taxes data processing (~6,6%
  effective ceiling) but the **nexus threshold is $500.000**; DC's is $100.000. **She will not cross
  either for years.**

### The strategic trap hidden in EU VAT — and it aims straight at rung 4

> **If the service qualifies as an "electronically supplied service" under Article 7 of Regulation
> 282/2011 — "automated, essentially unmanned, impossible without IT" — then for CONSUMER sales the
> non-Union OSS scheme applies from the very first euro, with no threshold.**

A bespoke, human-worked, per-job deliverable plausibly does **not** meet that test. **But rung 4 of
the expansion ladder is exactly "upload, pay per product, download, no human involved."**

> **Automating the service to remove her from the loop could flip its VAT classification and trigger
> an EU registration obligation she does not have today.** B2B sales stay on reverse charge either
> way, so the exposure is limited to consumer sales — which is a further reason to **sell B2B only,
> and to require a VAT number at checkout in the EU.**

## 4. Invoice requirements

| Market | Must show |
|---|---|
| **Brazil (always)** | NFS-e flagged *exportação de serviço*, citing LC 116/2003 art. 2 I non-incidence, value in BRL |
| **US** | Name + CNPJ, customer details, description, amount, currency, number, date. **No tax line.** W-8BEN-E held on file |
| **UK** | Standard elements + *"Reverse charge — customer to account for UK VAT under s.8 VATA 1994"*, **no VAT amount** |
| **EU** | Full Article 226 set + **customer VAT ID** + **"Reverse charge"** with a reference to Art. 194/196. Her own VAT field simply omitted |

**Three templates, built once, reused forever.**

## 5. The friction that is real

1. **Processing eats $9–15 of a $149 job** before Brazilian tax. At $5.000 the same stack is
   $300–500 — but a wire makes it $10.
2. **Export accounting is ongoing monthly work** — PGDAS-D segregation, NFS-e export flagging,
   contrato de câmbio. Accountants charge more for it.
3. **Fator R must be monitored every month**, not elected once.
4. **An EU AP clerk following a checklist may reject a supplier with no VAT number**, even though
   reverse charge is legally sufficient. Solvable with correct invoice wording; still a real
   lost-sale risk.
5. **The obvious rails a US competitor would use are unavailable** — Mercury needs a US entity,
   Nomad is PF-only, Stripe BR's multi-currency settlement is unconfirmed.

## 6. The verdict on money

**Nothing here kills the business, and one thing helps it materially.** A Brazilian solo exporter on
Anexo III with ISS/PIS/COFINS stripped from export revenue plausibly carries **a lower total tax
burden than an equivalent solo operator taxed domestically in the US, UK or EU** — which is exactly
what the Brazilian export exemptions exist to do.

**The one free check, adopted:** run a single real $149 transaction end to end through the intended
rail and pull the settlement report — gross, every fee line, the FX rate actually applied, and the
net BRL that landed. **That converts this entire section from modelled to measured, and it answers
the unconfirmed Stripe question before a real customer's payment is the first test.**
