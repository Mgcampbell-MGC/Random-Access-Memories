# MOLDE PÚBLICO — can the hands be removed? Tested 12 Sep 2026, and the answer relocates the problem

**Founder's question, verbatim: *"LETS EXPLORE IT AND SEE HOW WE CAN MAKE IT BETTER — what can change, what can be
automated, again it's 2026, AI and outsourcing."*** The candidate's single named flaw was that she casts each
teaching model herself. **The flaw is real, it is removable, and removing it does not save the candidate —
because the hands were never the binding constraint.**

---

## 1. The automation genuinely works, and it is C3-clean

**A print bureau is a VENDOR, not a contractor.** C3 forbids hiring a person; it permits buying a finished
product. A bureau that takes an uploaded file, prices it automatically and posts the object to an address she
names is a supplier, exactly like a print shop. **Koios 3D** (`koios3d.com.br/orcamento`) does this: *"Você envia
o arquivo 3D (STL, STEP ou 3MF)… o sistema… mostra o preço na hora"*, 2–5 business days, R$35 minimum, shipping
by Melhor Envio to any CEP. Its entire cost engine is published in the page: machine R$18,50/h, labour R$60/h,
setup R$12, margin bands 50–80%, PLA R$120/kg, one Bambu A1 with a **256 mm build envelope**.
⚠ Counter-example on the same shelf: **TRIDEO** publishes `MINIMUM_PRICE_BR: 600` — *"trabalhamos com um valor
mínimo de R$600 por pedido"* — so at one of the two bureaus with published numbers a single R$930 unit is
unsellable before anything else is considered. *(fábrica3D, GoMy3D and SEN3DPrints quote from a file but publish
no prices; "Wishbox" and "3DCriar" are not bureaus at all, they sell machines and consultancy.)*

**And the file is free, in quantity, with a commercial licence.** **BodyParts3D** (Database Center for Life
Science / RIKEN) ships a whole adult male decomposed into **2.905 named parts, 1.258 OBJ meshes**, downloaded and
parsed today. ⚠ **The licence is stated two ways and the discrepancy is real:** the website says **CC-BY 4.0**
(*"freely redistribute part or whole of the data… freely create and distribute… derivative works"*), while the
header inside every `.obj` in the download still says **CC-BY-SA 2.1 Japan**. **Both permit commercial use**, and
selling a printed physical object is not distributing adapted 3D data, so share-alike is survivable — but resolve
it before selling. *(NIH 3D offers public-domain and CC-BY files but mixes NC-licensed ones in the same
repository, so it is a per-file source, never a bulk one.)*

⇒ **Two of the three limbs close cleanly: no design work, no her hands, no employee.** The third does not.

## 2. The printed object costs more than the finished one, and is worse

Geometry measured from the free meshes, priced with the bureau's own published constants:

| object | printed at Koios (derived) | **self-serve catalogue, buy-now** | state dispensa unit median |
|---|---|---|---|
| heart, life-size | R$137–217 | **R$159,77** *(2 partes, tamanho natural)* | R$437,02 (n=36) |
| skull + movable mandible | R$168–275 | **R$272,25** *(6 partes, dentes extraíveis)* | R$355,86 (n=20) |
| brain | R$242–414 | **R$264,00** *(3 partes)* | R$637,56 (n=27) |
| liver | R$311–545 | **R$305,25** *(luxo c/ vesícula)* | R$293,19 (n=13) |
| torso 45 cm, 24 partes | **exceeds the 256 mm envelope** | R$848,45 | R$2.060,00 (n=69) |
| skeleton 85 cm on stand | not printable in one piece | R$221,35 | R$890,00 (n=39) |

Catalogue census, 195 products with published buy-now prices parsed from one Brazilian retailer's schema.org
data: **median R$526,35; 72,3% of the shelf sits at or below the state's R$958 unit median.**

⇒ **`THE CATALOGUE SCISSORS` in a government costume.** A monochrome single-material one-piece PLA replica costs
**more than a painted, separable, multi-part PVC model of the same organ** for the liver and brain, and about the
same for the heart and skull while being a visibly inferior object. **There is no version of the printed unit
that is both cheaper and acceptable.**

## 3. And the buyer's own specification excludes it

**The material is a binding attribute on 94,4% of lines** (1.187 of 1.257 in twelve months): RESINA PLÁSTICA/PVC
367 · PVC E POLÍMEROS FLEXÍVEIS 159 · SILICONE 142 · RESINA PLÁSTICA 136 · ACRÍLICO 76 · … **Standalone "PLA": 0.
"PETG": 0. "ABS": 0. "impressão 3D" or "manufatura aditiva": 0.** Live example, Fundação Santo André, 10 Sep
2026, R$335/unit: *"MODELO ANATÔMICO… TIPO: PELE ARTIFICIAL, **MATERIAL: SILICONE**… FINALIDADE: TREINAMENTO DE
SUTURA… C/ 3 CAMADAS: EPIDERME, DERME E MÚSCULO"*.
⇒ **Nothing forbids 3D printing in words. It is worse than that: the TR copies the CATMAT spec verbatim, the spec
names PVC or silicone, and an FDM part is simply non-conforming.** The silicone segment is precisely the one a
printer cannot serve.

**The tender also names the catalogue product as the standard** — UNEB/UFRA edital 28.2024: *"MARCA/MODELO DE
REFERÊNCIA: 3B SCIENTIFIC B50 OU SIMILAR/SUPERIOR"*; IFSC TR 93/2024 §4.3: *"só serão aceitos produtos com
características equivalentes ou superiores aos modelos de referência"*. And it demands a **sample** at the
bidder's cost (UNEB §4.4–4.8, *"amostra fora das especificações… a proposta será recusada"*), a **12-month
warranty** with corrective maintenance and transport on the contractor, and an **atestado de capacidade técnica**
(IFSC §8.29.2).

## 4. ★★★ THE ACTUAL KILL, AND IT IS NOT THE HANDS: THE PUSHED POOL IS R$557–623 THOUSAND A YEAR

| | |
|---|---|
| Whole PDM 9837, twelve months | **R$30,4–30,8 M** |
| Bought by **pregão** (robot reverse auction) | **92%** |
| Bought by **dispensa** — the auto-email channel, the entire distribution thesis | **R$557.178–622.861, i.e. 1,83–2%** |
| Distinct dispensa suppliers in the year | 67–71 |
| **Median supplier-year** | **R$3.999–12.398** |
| Won exactly one line all year | **43–49%** |
| Billings she needs at 50–60% COGS | R$292.000–477.000/yr |
| ⇒ **her required share of the entire national dispensa pool** | **47–77%** |

`THE NICHE SCREEN` says stop above ~5%. `THE MARKET-MULTIPLE RULE` wants a reachable pool 3–5× the target and the
measured multiple is **1,0×**. **The other 98,2% is pregão and it is already held: ANATOMIC R$12,1 M (39,3%) and
LAERDAL R$7,6 M (24,8%) — 64% of the code between two manufacturers who bid direct.** Winning there means beating
the factory on its own product at its own price.

**This fact is indifferent to everything the automation fixes.** Remove her hands, remove the design cost, remove
the mould capital: the pool is still R$557k and she still needs a third to three-quarters of it.

⚠ **And the two one-person winners the original write-up cited as encouragement are winning very little.** In the
dispensa channel they took eight lines and five lines in a year; at the median line value that is roughly
R$8.000–13.000 each. They are not casters either — they are resellers.

## 5. What it becomes, and the honest reclassification

**Buying the catalogue item and reselling it to the state has a WIDER spread than printing, at zero production
risk, with a conforming PVC object and a manufacturer's warranty behind it:** heart R$159,77 → R$437,02; skull
R$272,25 → R$355,86; brain R$264,00 → R$637,56; catalogue median R$526,35 against a state unit median of R$930.

⇒ **MOLDE PÚBLICO, automated, is not a machine that makes objects. It is the government-supply desk we already
have, pointed at a different CATMAT code — and it must be judged as that, against `THE NICHE SCREEN`, not as a
new candidate.** On that screen this niche **fails limb 1** (pushed pool far too small) and **fails limb 2** (a
self-serve shelf sits below the state's median on 72,3% of products), while passing limb 3 only for the two
manufacturers.

**The useful half, and it is worth keeping:** the catalogue-to-state spread is real and wide, so *modelo
anatômico* belongs on the desk's **niche list** as one line among many, bid opportunistically when a notice
arrives. It cannot be the business.

---

## ★ The law this produced

**★★★ AUTOMATION ANSWERS "CAN SHE MAKE IT", NEVER "IS THERE ENOUGH OF IT TO SELL". Size the pushed pool BEFORE
asking whether the unit can be automated.** Three days were spent treating "her hands on every unit" as this
candidate's problem. Removing the hands was possible, cheap and C3-clean — a vendor's printer and a free
CC-licensed mesh library — and it changed nothing, because the channel that delivers the buyers carries less than
two percent of the money in the category. **The hands were the visible flaw; the pool was the fatal one. Run limb
1 of `THE NICHE SCREEN` first, and only then ask what the unit costs to make.**

★ **Corollary, on the evidence class: a catalogue price is a harder fact than a production cost.** The printed
unit's cost had to be derived from a vendor's published constants; the catalogue price was a number on a page
with a buy button. **The check that killed this took one fetch and no arithmetic.**

⚠ **And a unit correction to `THE_FIVE.md`, worth propagating:** its "median R$958/line" is the **UNIT** median.
The **LINE** median is R$1.442–1.618. Do not mix the two in a units-per-month calculation.
