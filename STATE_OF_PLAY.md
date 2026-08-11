# State of play — 11 August 2026

**34 candidates killed. Zero launched. Zero contact with a real buyer.**

That last number is the one that matters most, and it has not moved in weeks.

---

## 1. What actually killed things

Roughly **28 of the 34** died to one sentence: **somebody is already doing it, and usually for free.**
Not "the market is hard", not "the idea was weak" — a named company with a fetched URL and, in most
cases, a published price of zero.

The free version arrives through four distinct funding mechanisms, and they should be checked in this
order because that is their order of deadliness:

| # | Mechanism | Named instances |
|---|---|---|
| **1** | **A general chat model does the whole job.** Newest, and the most dangerous going forward | ChatGPT / Claude — measured at 38/38 planted discrepancies, 0 false positives, ~380 checks |
| **2** | **A clearing party funds it to zero** — whoever takes a margin on the flow gives the software away as acquisition cost | Object & Order (5% goods margin), Booksy (payments), Momence (payments), RangeMe (ECRM meeting fees), Insparisk (insurance), Arhaus/Uncap/Daniel House (goods margin), Stella Source |
| **3** | **A funded incumbent gives content away as lead generation** — content costs nothing to produce, so the free tier *is* the marketing budget | Levelset, GleanMark, Estratégia/QConcursos, iNymbus/SPS, ConLicitação, Sympla Academy, Advisera |
| **4** | **The regulator built and mandated it** — the recipient of a filing wants the data more than the filer wants to send it | Inmetro's PSIE, the National Board's EDT |

The remaining six died on: a reserved profession (the vise, five appearances), a buyer with no money
(Gate 0), a cheaper insured human, or an invisible trigger.

**The conclusion this forces:** the binding constraint was never idea quality. **Anything findable by
research is already served.** An edge has to come from something research cannot find — a
relationship, a lawful data position a competitor cannot hold, a permission, or a channel.

---

## 2. The strongest candidates, honestly ranked

| | Candidate | Why it was strong | What killed it |
|---|---|---|---|
| **1** | **DeckProof** | The only candidate where buyer solvency was **observed, not estimated** — the qualifying signal was a receipt for US$7.000–16.900. Self-verifying output, no credential, no clearing party | A chat window does it, measured. Plus the ECRM licence bars the list, and the fail-closed spec disqualifies its own buyers |
| **2** | **Recurso em 3 dias (licitação)** | **The best buyer in the entire record, and it never died.** 700.000 SICAF suppliers; PNCP exposes CNPJ-level contract data through a no-login public API; ME/EPP average ~R$566.000 per contract | The *product* died — Dr. Licita ships the AI, a human charges R$190, and Lei 14.133 art. 165 §1º precludes the claim before a call can land |
| **3** | **The Expediting Desk** | Recurring at US$199/month against a US$1.299/month human substitute; 16 vendors shipped *fields* and none shipped ingestion | Object & Order ships it free with *"no paid plan"*, funded by 5% goods margin. Found by the founder in one link |
| **4** | **CotaMRO (rescued form)** | Computes on private files, no clearing party, Portuguese phone-sellable | Never tested. Exposed to Excel on the safe side and CONFEA on the differentiated side |

---

## 3. The strongest thing we hold is not a candidate

**It is a buyer population with no product attached.**

Re-verified live, 11 August 2026, with no key and no login:

```
GET https://pncp.gov.br/api/consulta/v1/contratos
    ?dataInicial=20260601&dataFinal=20260630&pagina=1&tamanhoPagina=10
→ HTTP 200 · totalRegistros: 169.505 · totalPaginas: 16.951
→ niFornecedor (CNPJ), nomeRazaoSocialFornecedor, valorInicial, objetoContrato
```

**169.505 contracts in a single month**, each naming the supplier's CNPJ, the contract value and the
object. Published by the Brazilian government *for public use* — the exact opposite of the ECRM
licence that just killed DeckProof's channel.

This is the only place in 34 candidates where **all four gates passed simultaneously**:

- **Gate 0 — solvency:** ME/EPP contracts average ~R$566.000; over a million public purchases worth
  ~R$1 trilhão in 2025
- **Enumerability:** by CNPJ, at scale, refreshed continuously — and enumerable because these firms
  **transact**, not because a regulator licenses them, so the enumerability trap does not fire
- **Lawful reachability:** a government API published to be consumed, with no terms bar
- **Channel fit:** Portuguese. She can **phone-sell**, and Brazilian CPC is ~US$0,35

Every hunt so far started from a product and searched for a buyer. **We have a verified buyer and no
product.** That is the better problem, and it has never been worked.

---

## 4. The one advantage that is actually hers

Strip out everything available to any solo founder on earth — AI-directed building, research,
faceless operation, Stripe, a US entity — and exactly one thing is left:

> **She can sell by telephone, in Portuguese, to Brazilian companies.**

A US or global competitor cannot copy that cheaply. It is the only asymmetry in the set, and **fewer
than a handful of the 34 candidates used it.**

It also happens to be the one thing the newest kill mechanism cannot touch. Which leads to the rule
that should govern the next hunt:

> **After the DeckProof measurement, any candidate whose value IS the analysis is presumed dead.**
> A chat window performs analysis for free, instantly, worldwide, and the wedge is one copyable
> paragraph of prompt — which needs no funding to distribute.
>
> **The value must sit in something a chat window structurally cannot supply:** a relationship, a
> permission or licence, a lawful data position, an action executed on someone's behalf, or a
> distribution channel.

---

## 5. What has never been done

Recorded plainly, because it is the same list as three weeks ago:

1. **No contact with a single real buyer.** 34 kills, all from a desk.
2. **The 30-minute browser reconnaissance** — Etsy, then the complaint surfaces. Prescribed twice,
   blocked to every automated method both times, never done by a person.
3. **No product has ever been priced in front of someone who could say yes.**
