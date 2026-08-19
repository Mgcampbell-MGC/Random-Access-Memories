# THE SEAM — what the archive was hiding, 19 Aug 2026

**Eight Brazilian regulatory-clock business plans mined for components rather than evaluated as candidates.
The finding is not in any one of them. It is in the shape all eight share.**

---

## 1. ★★ THE SEAM

**Every one of the eight plans splits cleanly at the same joint, and none of them notices:**

| | **THE CLOCK HALF** | **THE EXECUTION HALF** |
|---|---|---|
| Cost shape | **FIXED — one harvester serves every CNPJ in Brazil** | **PER-CUSTOMER — 2 to 30 founder-hours per unit** |
| Credential | **None. Reads only public records** | Council-registered *Responsável Técnico* signature → **EXPERT VETO** |
| Access | **None. Free public consultation + free DOU feed** | Portal login + the client's *Caixa Postal Eletrônica* → **CREDENTIAL VETO** |
| Conversation | **None. Computed and delivered** | Scope, onboarding, exigência escalation → **SPEECH VETO** |
| Verdict | **Clears all four constraints** | **Breaks all four at once** |

> ### **SEVEN OF THE EIGHT PLANS PRICE ONLY THE EXECUTION HALF — AND GIVE THE CLOCK HALF AWAY FREE AS A LEAD MAGNET.**
>
> **The agent's closing line, and it is the most valuable sentence in the archive:**
> ***"Nobody in the archive ever tested whether the free Raio-X is itself the product."***

**The one file that DID price detection separately — ORIGEM — is also the only one that solved *"may never
opine"*, and it solved it with a closed vocabulary rather than a credential.** Those two facts are the same
fact.

---

## 2. THE THREE CLOCKS, RANKED BY CONSTRAINT COMPATIBILITY

### ★ CLOCK 3 · PROVA DE PORTE — the cleanest object found anywhere in the archive, treated as a throwaway line

| | |
|---|---|
| **The window** | **Opens 1 January, closes 30 April** for ME/EPP *(Junta Comercial simplified certificate)*; 30 June and the ECF deadline for other tiers. All three dates the file marks VERIFIED |
| **Consequence of missing it** | *"Automatic reclassification to Grupo I – Grande, no discount, no reimbursement"* |
| **Priced exactly** | TFVS for *Registro de cosméticos* is **R$2.500**, with reductions of **30% medium / 60% small / 90% micro** *(Lei 9.782/1999 Anexo II)* → **R$1.750 / R$1.000 / R$250**. For a Grupo III client that is **R$1.750 versus R$2.500 per registro, multiplied across a portfolio** |
| **How you know it started** | **It is a FIXED CALENDAR DATE, not an event. No gazette, no notification, no lookup, no data access of any kind** |
| **Recurrence** | **Annual, per company, forever** |
| **Who supplies the document** | **The client's own ACCOUNTANT** — so no credential of hers is involved at any point |

> **Fully fixed-cost. Clean on all four constraints. No expert judgement — the date is in a statute and the
> arithmetic is division. And the archive mentions it as a line item inside someone else's retainer.**

### CLOCK 1 · CONTINUIDADE DECENAL — the biggest pool, and the detection half is free

**RDC 907/2024 art. 41 and RDC 312/2019 art. 2 §2º.** The window **opens at `termo_fim − 6 months`** and closes
at `termo_fim` — the last six months of each product's ten-year term. **One clock per SKU, not per company**,
so a portfolio of 100 SKUs with staggered launches opens windows continuously, every month, forever.

> **Missing it CANCELS THE REGULARIZAÇÃO** — art. 2 §3º. The product loses its right to be sold in Brazil.
> **And nobody is notified.**

**The detection source is free and public:** ANVISA's consultation is **searchable by titular CNPJ and by
process-expiration period** — *the expiry-period filter is literally a "whose clock is running out" query.*
The DOU is the durable second source: **free daily PDF and XML via INLABS since 01/01/2020, with official
download scripts published by Imprensa Nacional.**

**Two honest limits:** the consultation is a JavaScript SPA with no documented public API *(a third-party
wrapper died after a redesign)*, and **INLABS only covers the DOU from 01/01/2020, so acts granted 2016–2019
sit outside the machine-readable window.**

### CLOCK 2 · MIGRAÇÃO SGAS — a real deadline that manufactures its own future pipeline, and a fatal unknown

**RDC 951/2024 art. 3:** migration must happen inside the legacy system's validity *or the regularização is
cancelled.* **Art. 6** grades the commercial consequence: migrate by 31/12/2026 and the old label may be used
six years; by 31/12/2028, four; from 01/01/2029, two. **Migration costs nothing in government fees, and
migrated products receive a fresh ten-year term.**

**Killed as a business by two things the file states itself:** *"Migration is once per SKU… the annuity the
plan describes is a decade away,"* and **nobody — including ANVISA — publishes how many unmigrated
regularizações remain.** *(VERIFIED negative: ANVISA publishes 23 analytical panels and none covers cosmetics.)*

---

## 3. THE FOUR MECHANISMS WORTH MORE THAN ANY OF THE EIGHT BUSINESSES

### ★ MECH-3 · THE CLOSED VOCABULARY — the artefact that lets a non-expert ship a paid deliverable

**From ORIGEM. The purest answer to the expert veto found anywhere in this project.**

**A closed set of permitted final statuses:** `DEFINED DIFFERENCE EXPLAINED` · `DEFINED DIFFERENCE REMAINS` ·
`EVIDENCE MISSING` · `NOT FOUND IN NAMED DATASET` · `SOURCE UNAVAILABLE` · `FIELD OR LEGAL REVIEW REQUIRED` ·
`OUT OF SCOPE`

**Paired with an explicit banned-word list:** *"Never use: 'No embargo,' 'no forced labor,'
'deforestation-free,' 'legal,' 'compliant,' 'low risk,' 'cleared,' 'approved,' or 'sufficient.'"*

**And the safe form, quoted:**
> ***"No matching record was found in the named dataset and edition as of the recorded retrieval time."***

**Every statement also carries eight provenance fields** — observed fact · named source and edition ·
retrieval timestamp · query key · method version · coverage limitation · documentary status · operator-review
reminder — **plus a list of what public sources cannot prove, handed to the buyer up front.**

### MECH-1 · THE COMPUTED FREE DIAGNOSTIC

From **nothing but a CNPJ**: every SKU in the public record, its process number, which system it sits in,
status, term end date, **every computed statutory window with days remaining**, misclassification flags and
DOU enforcement history. *"Deliberately free because it is computed, not laboured."*

**Transplantable to literally any register with a per-entity expiry field.**

### MECH-7 · THE DEADLINE ENGINE AS A PURE FUNCTION

`RegraModulo × Regularizacao → Janela[]`, **idempotent, so a corrected rule retro-corrects every case.**
Business-day versus calendar-day is **stored on the rule, never inferred**, backed by a maintained national
holiday table. **The idempotence is the point: rules can be wrong and later fixed without touching cases.**

### MECH-8 · SUCCESS VERIFIED ONLY AGAINST THE PUBLIC RECORD

*"`VERIFIED_SUCCESS` is set only when a machine check finds the expected identifier with the expected status
and a publication date consistent with the filing. A human saying 'it went through' does not set this state,
and neither does an AI reading a screenshot."*

> **It converts an unfalsifiable service claim into a third-party-verifiable artefact — which is exactly what a
> seller who cannot be believed requires.**

*(Also kept: **MECH-11**, the client pays every government fee directly in their own name — which removes the
merchant-of-record and custody problem by design rather than by argument. And **MECH-16 Rule 5**, client-caused
delay pauses the case: *"ENTRA does not maintain an infinite human follow-up loop."*)*

---

## 4. THE CAUSES OF DEATH THAT NOW SCREEN EVERY FUTURE CANDIDATE

**★ COD-4 · TEST THE CONSEQUENCE'S FREQUENCY, NOT ITS SEVERITY.** From PRUMO, verbatim: *"Across 45.863
projects, **84 prestações de contas were reproved — 0,18%, roughly one in 550.** Selling this as insurance
against a three-year ban would be selling protection against a loss that almost never lands, and that is
precisely the mistake that killed three earlier candidates."*

**COD-13 · THE RIGHT TO ACT WAS ASSUMED, NOT VERIFIED.** VIGENTE's own attack A21, which it rates fatal:
*"OPEN: what representation the portal requires for a third party to petition; OPEN: whether delegated access
to a client's Caixa Postal Eletrônica is legally clean."* **That is the C4 credential constraint appearing,
unrecognised, as the plan's most serious unaddressed risk.**

**COD-6 · THE PRIVATE TRIGGER.** *"The event happens inside a franchisor's legal team and a WhatsApp
negotiation."* **Three independent files died on this same defect** — VIRA, ENTRA and PRATELEIRA.

**COD-9 · THE REGULATOR'S OWN PAGES ARE WRONG.** *"ANVISA's own frequently-asked-questions pages still cite
[a resolution] revoked in full… and still instruct users to petition through SGAS, a system retired on
07/04/2025."* → *"any tool, adviser or language model that trusts the official pages is wrong about the current
rules."* **The asset is knowing the current rule. The liability is that no source is authoritative, including
the authority.**

**COD-10 · THE DIRECTION OF TRAVEL IS DEREGULATION, and there is no mitigation for one thing.**
Lei 15.154/2025 exempts artisanal cosmetics from registration; RDC 949/2024 gives until 2030. And the flat
statement: **"Against ANVISA publishing a cosmetics expiry panel, there is no mitigation."**

**COD-14 · THE QUALIFYING VARIABLE IS PORTFOLIO SIZE, NOT REVENUE.** *"A R$5m company with 60 legacy SKUs is
a better client than a R$40m company with eight."*

**COD-1 · AND THE ONE SURVIVING CRACK, quoted:** *"Legacy SKUs from vanished suppliers and former employees
are unowned. That crack, and only that crack, is the business."*

---

## 5. WHAT THIS OPENS — the question the archive never asked

**If the clock half is fixed-cost, credential-free, conversation-free and computed from a free public source —
then the clock half is the only part of these eight businesses she can actually own.**

**And there is a buyer for detection who is not the buyer for filing.** The archive enumerates **38 Brazilian
regulatory consultancies by name, and records that 20 of 20 examined publish no price, no online checkout, no
dashboard and no SLA.** They are relationship-sold firms with the credential, the portal access and the client
relationship — **and no systematic way of knowing whose clock is running out.**

> **That is THE WHOLESALE ESCAPE, arriving from a completely different direction: she supplies the detection
> machine; they supply the face, the signature and the liability.**

**Three things must be settled before this is a candidate rather than a hypothesis, and all three are cheap:**
1. **Is the universe big enough?** 3.630 sector companies and 3.280 active CNPJs are the denominators — but
   **how many SKU windows are open in any given month is `[OPEN]` and settleable directly from the
   expiration-period filter.** One afternoon.
2. **Is the buyer the consultancy or the brand?** 38 consultancies at $11.100/month is ~$300 each at 100%
   penetration — **tight, and possibly too small.** The brand-side universe is 100× larger and pays less.
3. **Can the SPA actually be harvested at scale, lawfully?** No documented API, and MECH-5's source-access
   matrix is the discipline that answers it.

**Three miners and the capability agent are still out. This is the first half of an answer, not the answer.**
