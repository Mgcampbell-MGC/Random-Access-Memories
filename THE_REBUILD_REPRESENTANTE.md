# REPRESENTANTE v2 — ground-up rebuild, 2 Sep 2026
**Working name: PROCURADOR BR. Everything below is built on measurements taken in this session, and every
design choice names the measurement that forced it.**

> ### THE ONE-SENTENCE VERSION
> **She is the Brazilian address of record for foreign companies that own Brazilian trademarks, and every week
> the same machine that finds her next client tells her existing clients what INPI just did to them.**

---

## 1. What the asset actually is — and what it is not

**The asset is a legal qualification: residence in Brazil plus civil capacity.** LPI art. 217 and IN RFB
2.119/2022 art. 6 §1 compel a foreign party to appoint someone who has it; INPI and two independent sources
confirm the qualification requires **no credential** — *"an IP agent, a specialized lawyer, or **any Brazilian
citizen** (since June 2014)."*

> **In ~130 candidates this is the only input found that the buyer cannot commission at any price.** It is the
> fourth escape from `THE REPLACEMENT-COST CEILING`, and the enumeration in that law has been amended to add it.

**What it is NOT: a licence to do legal work.** She is not an *advogado* and not an *agente da propriedade
industrial*. Everything below is designed so that the thing sold is the qualification and the reliability, never
the judgement. `THE EXPERT VETO` is satisfied by construction, not by argument.

## 2. The scope decision — the centre of the rebuild

Three duties compel a Brazil-resident representative. **They are not equally good, and v1 treated them as one.**

| Duty | Observed price | Liability | Onboarding friction | Buyer enumerable? |
|---|---|---|---|---|
| **★ INPI — LPI art. 217** | unknown, and it is THE open question | **LOW** — acts inside a written POA in an administrative proceeding | **★ NONE — see §3** | **YES**, weekly, free |
| CNPJ / RFB — IN RFB 2.119 art. 6 §1 | **US$400–1.300/month** *(Lematt tiers, published)* | **HIGH — CTN art. 135 III** | notarised + consularised POA | partly |
| Registro.br (.com.br) | trivial | none | simple | no |

> ### **DECISION: LAUNCH ON THE INPI DUTY ALONE. The money looks like it is in the CNPJ role and so is the tax liability, and a one-person business with no counsel on retainer must not carry CTN art. 135 III in year one.** The CNPJ role is a **year-two upsell to clients who already trust her**, taken only with a written legal opinion.

**⚠ And the honest consequence:** the observed US$400–1.300/month belongs to the CNPJ/entity role, which bundles
governance, banking support and compliance reporting. **It is NOT evidence for the price of the bare INPI role,
and v1 treated it as if it were.** `THE OBSERVED-PRICE CEILING`, applied to my own board. **§6 prices the INPI
role from first principles and names the probe that settles it.**

## 3. ★★ THE FRICTION THAT ISN'T THERE — the finding that makes this shippable

I flagged the apostille as the likeliest reason a warm reply goes cold. **It does not apply to this route.**
INPI's *Manual de Marcas* §5.6.1 requires of a procuração only the Civil Code art. 654 §1º data:

> *"Informações do(s) outorgante(s)… outorgado… Tipo(s) de poder(es)… Data, local e assinatura."*

**No notarisation, no legalisation, no apostille, no consular step.** A power of attorney in a foreign language
filed without its translation is even expressly salvaged — *"é aproveitado o ato da parte."* The only hard rule
is **60 continuous days from the act, on pain of definitive filing** (*arquivamento definitivo*).

> ### **ONBOARDING IS ONE SIGNED PDF, SAME DAY.** The two-week notarial errand belongs to the CNPJ route — which is the second reason to launch on INPI and not on the entity role. **This single fact is the difference between a business that closes by email and one that dies in a notary's queue.**

## 4. The product — scoped by what is deliberately excluded

**PROCURADOR BR — Brazilian representative of record, plus a weekly docket watch.**

| **IN** | **OUT, and stated in the contract** |
|---|---|
| Named as procurador on the client's Brazilian marks | Responding on the merits to anything |
| Receiving every INPI communication | Filing oppositions, appeals, defences |
| **Forwarding within 24 h with the deadline stated in English** | Advising whether to fight, abandon or settle |
| **A weekly docket report: what INPI published about your marks this week, and by when you must act** | Classifying goods, arguing distinctiveness, valuing rights |
| Filing the POA itself and address changes | Any tax, corporate or customs representation *(year two, with counsel)* |
| An annual "your marks, your dates" summary | Marketplace takedowns *(see §9)* |

**The scope line, to be written into every contract, on the CONFERÊNCIA pattern:**
> *"Não opinamos sobre o mérito, não redigimos manifestações, não representamos o titular em juízo e não
> decidimos o que responder. Recebemos, registramos, traduzimos o prazo e encaminhamos. O advogado do cliente
> decide e assina."*

## 5. ★★★ THE MOVE THAT MAKES IT A MACHINE — one parse, two jobs

`bin/inpi_foreign_applicants.py` already parses the weekly RPI. **The same weekly run does both halves of the
business at once:**

```
  RPI, every Monday
        ├─► CLIENTS:   any event on a client's marks → 24 h alert + weekly docket report   (delivery)
        └─► PROSPECTS: foreign holder + hard deadline + no procurador on record            (acquisition)
```

> **This is the sub-linear delivery the file demands, and it is already built.** The marginal cost of client
> twenty-one is one more row in a filter. **And it converts the monthly fee from a mailbox charge into a
> continuous service, which is what justifies a monthly price rather than an annuity** — the distinction
> `THE CONSUMPTION-CLOCK TEST` says decides whether recurrence is real.

## 6. Pricing — built from the work, with the unknown named

**v1's error was pricing off the CNPJ tier table. Rebuilt from what is actually delivered:**

| Tier | What it is | Price |
|---|---|---|
| **Core** | Representative of record + weekly docket watch, all of one company's Brazilian marks | **US$149/month**, annual or quarterly |
| Setup | POA drafting, filing, address of record established | **US$150 once** |
| Per-event handling | Receive, log, translate the deadline, escalate to their counsel | included |
| Year two | CNPJ / entity representative | **+US$300–500/month**, only with a written legal opinion |

**Arithmetic at the bar** *(US$2.200–2.800/month gross, export, zero COGS)*:

| Clients | Gross/month | Her hours/month | Verdict |
|---|---|---|---|
| 10 | US$1.490 | ~6 h | below |
| **15** | **US$2.235** | **~9 h** | **at the bar** |
| **20** | **US$2.980** | **~11 h** | **clears it** |
| 30 | US$4.470 | ~16 h | 1,8× the bar, still inside C9 |

*Per-client load: ~30 min/month of exception handling and report review; the watch itself is automated.*

> ### ⚠ **THE ONE NUMBER THAT DECIDES EVERYTHING: what does the bare INPI representative role sell for today, unbundled?** If Brazilian IP firms include it free with a filing, or price it at R$200–800 **per year**, then US$149/month is 2–9× the market and the business is a repricing argument rather than a gap. **The 20-provider probe answers it and must be run before anything is built.** *(`PROBE_KIT_1SEP.md` B2, amended: ask specifically for the fee for the representation role ALONE, separated from filing fees.)*

## 7. Distribution — three channels, ranked by evidence

**1 · THE MEASURED DISTRESS LIST — 313 companies a month, named and dated.**
Foreign holders with a hard-deadline INPI event and **no procurador on record**: 367 processos, 313 distinct
companies in four weeks, ≈4.100/year. Top countries US 53 · CN 52 · DE 26 · CH 24 · FR 16 · GB 15.
**They have 60 days and cannot act without appointing someone.** The mail says exactly that and nothing more.

**2 · THE WARM LIST — 1.007 a month with a granted mark and no representative.**
Not compelled *(Madrid is sold on not needing a local agent — `THE PRESENT-TENSE DUTY TEST`)*, but correctly
addressable: *"your mark was granted on [date]; no representative is on record; when INPI writes you will have
60 days."* Lower urgency, far larger, and it costs nothing to include.

**3 · ★ THE WHOLESALE ESCAPE — foreign IP firms, and this is the one that scales.**
A US, UK or EU trademark firm filing into Brazil needs a Brazilian address of record and currently buys it from
a Brazilian law firm that also wants the substantive work. **Positioned as *"the administrative correspondent
who never touches your client's legal work,"* the foreign firm keeps the whole matter and buys only the seat.**
One firm = many end clients. **This is the only channel that reaches 30 clients without 30 sales conversations,
and it turns law firms from the competitor into the channel.**

⚠ **What is NOT a channel, measured:** catching Madrid designations at the moment of crisis. **Zero of the 367
unrepresented hard-deadline processos were Madrid** — those appoint within days of notification. **The gazette
is a lagging record of a solved problem for that route.**

## 8. Liability architecture — designed, not footnoted
1. **INPI only in year one.** CTN art. 135 III attaches to tax representation; an IP procurador acting inside a
   written POA is a different exposure. **UNVERIFIED as applied — one counsel opinion before the first client,
   and it is the single item worth spending capital on.**
2. **The POA is drafted narrow by her, not by the client:** receive communications, file the POA and address
   changes. **Expressly excluded: abandoning, assigning, settling, or responding on the merits.**
3. **A dated log of every notice received and forwarded**, with timestamps. If a deadline is ever missed, the
   record must show when she forwarded it. This is the whole defence and it costs nothing.
4. **Never the sole recipient.** Every notice goes to the client and, where they have one, their lawyer, in the
   same message. **She is a relay with a receipt, not a gatekeeper.**
5. **Refuse any client without their own counsel somewhere.** A client with no lawyer will ask her what to do,
   and the day she answers she is practising law.

## 9. What was CUT from v1 and GUARDA, and why
| Cut | Reason |
|---|---|
| **Takedowns as the core product** | 6–8 h/client/month against 1–2 for the representative role — **four times the hours per real earned**, and it caps her at 4–5 clients |
| **Takedowns as a retainer at all** | Brazil's public BPP record is **wrongful takedowns**; the hard cases are grey-market resellers of genuine stock (lawful, LPI art. 132 III); telling them apart is a legal judgement and the operator who submits is named. **If ever offered: per-notice, priced per URL, on the client's written instruction — never a monthly promise to police a marketplace** |
| **The fashion framing** | 65% of the qualified pool is Nice class 09; the mix is electronics, software, pharma, services and industrial. **Fashion was never the market** |
| **The CNPJ role at launch** | CTN art. 135 III, plus notarised and consularised onboarding |
| **Pricing off the Lematt tiers** | Those price the entity role, not this one |

## 10. Kill conditions — pre-committed, before any build
Any one of these is a kill, not a restructure:
- **The 20-provider probe returns a median ANNUAL fee** for the bare representative role, or firms say they
  include it free with filings.
- **Counsel says an IP procurador carries tax or joint liability** for the client's acts.
- **0 of 15 replies** from the measured distress list, or every reply is *"our attorneys will handle it."*
- **INPI announces** a simplification removing or relaxing art. 217 *(precedent: Res. Conjunta BCB/CVM 13/2024
  waived the analogous duty for small foreign investors from 1 Jan 2025 — **diary this quarterly**)*.
- She is asked to give an opinion on the merits by two of the first five clients — the scope line is not holding.

## 11. The test — 14 days, under US$60, no build, no phone
| | | Pass | Kill |
|---|---|---|---|
| **1** | **20 provider quotes**, as a prospective foreign client, asking for the fee for **representation alone**, separated from filing fees | ≥5 numbers, median **monthly** | median is annual, or "included free" |
| **2** | **15 emails to the measured distress list** — named companies, live deadline, no representative | **2 replies engaging with terms** | 0, or all defer to counsel |
| **3** | **5 emails to foreign IP firms** offering the administrative correspondent seat | 1 asks for terms | 0 of 5 |
| **4** | One counsel opinion on the liability perimeter *(the only spend)* | perimeter is the POA | joint or tax liability attaches |

**Test 1 outranks the rest.** If the bare role is an annuity, everything above is a beautifully engineered
answer to a question nobody is paying to have answered — and that is exactly the failure this file has recorded
most often.
