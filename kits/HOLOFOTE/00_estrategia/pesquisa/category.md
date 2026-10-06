# Category research: scented candles in Brazil, and the global Gen Z references

Research date: 6 Oct 2026. Purpose: the category input for a fictional Gen Z candle brand launching for **Dia das Mães, Sunday 9 May 2027**. It complements `culture.md`, which covers the date, the audience and mum's vocabulary.

**How prices were read.**
- Brazilian prices come from each store's own catalogue: the public VTEX catalogue API, `…/api/catalog_system/pub/products/search?ft=vela…`, which is what the product page renders. Where that was not available, they come from the product page's own schema.org JSON-LD.
- Global prices come from each brand's Shopify `/products.json`, which feeds the product page, or from the product page itself.
- Every price was fetched on 5–6 Oct 2026. Promotional prices are shown with the list price as "(de R$…)".
- **Exchange rates:** BCB PTAX selling rate, close of 5 Oct 2026: **US$1 = R$4,9859** and **€1 = R$5,5897**, from the [BCB Olinda API](https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/). The dollar fell from R$5,2238 on 2 Oct to R$4,9859 on 5 Oct, so conversions move about 5% with the day chosen.
- **Blocked:** granado.com.br, phebo.com.br, belezanaweb.com.br, natura.com.br, boticario.com.br, taniabulhoes.com.br, zara.com/br, bathandbodyworks.com and Mercado Livre all returned bot walls (403 or captcha). They were not retried. Granado and Phebo are therefore priced at retailers' own pages.
- **Raw captures:** `research/raw/` and `research/raw_cat/`. The visual contact sheets are `raw_cat/img/sheet.jpg` (global) and `raw_cat/img/br_sheet.jpg` (Brazil).

---

## 0. The findings that matter most

1. **The Brazilian middle band is R$90–145 for 170–200 g, about R$50–80 per 100 g.**
   - Granado sells the same 180 g candle at R$60–136 depending on the retailer.
   - Then Bendita Vela R$99 for 200 g, Naturel R$109 for 180 g, Herô R$110,90 for 200 g (list R$180), L'Occitane au Brésil R$139,99 for 170 g, and Mels Brushes R$144,90 for 200 g.
   - The entry tier is Océane, Glow Vibes and Tok&Stok at R$50–80. The premium tier is Antik at R$247–284 for 190 g.
   - The imports above that are Sisley at R$450 and Jo Malone at R$595 (list R$700).
2. **The Brazilian shelf looks the same.**
   - **Vessel:** a clear or frosted glass tumbler.
   - **Label:** a small white or kraft label in a thin sans or serif.
   - **Lid:** none, a bamboo or wood lid, or a gold or silver lid.
   - **Names:** ingredient names (*Lavanda, Gengibre, Chá Branco, Capim-Limão*) or place names (*Ipanema Beach, Amalfi, Jardim Mediterrâneo*).
   - In my visual sample of 11 Brazilian products, 8 were clear or frosted glass. **None was an opaque, saturated-colour vessel, and none carried big type.**
   - **The amber jar is a US cliché** (P.F. Candle Co.), **not a Brazilian one.** The Brazilian cliché is the *frosted tumbler with a bamboo lid*.
3. **Personality naming is almost absent.**
   - About 6 of ~100 Brazilian candle names carry a mood or a joke: *Glow Vibes "No Bad Vibes"*, *Lucci Birthday Cake*, *Lucci Love*, *Hello Hello by Nah Cardoso*, *Orgânica Felicidade*, and Tok&Stok's *Saudade Tropical* and *Tão Longe Tão Perto*.
   - **None of the ~100 is about mothers.**
   - The closest thing to Gen Z play is Lucci's *Birthday Cake*: sprinkles, a wood lid, and **"Happy B-Day!" revealed as the wax burns**, at R$126,31 for 250 g of soy wax.
4. **Global icons win on one owned visual idea, not on scent.**
   - Glossier: a glossy red glass with an embossed logo and no label.
   - Otherland: saturated tinted glass with collage art.
   - Homesick: one giant black phrase on a white label, *"THANK YOU, MOM"*.
   - Boy Smells: black glass, a flat pink label and the name embossed on the base.
   - Diptyque: the oval label with dancing letters.
   - Liquid Death × Martha Stewart: a hand-shaped sculpture.
   - Every one of these can be recognised in silhouette or by colour at thumbnail size. No Brazilian candle in my sample can.
5. **Homesick already sells a Mother's Day candle: "Thank You, Mom"**, US$29,95 for 13,75 oz, with *"a handwritten note on the box"*. It also sells *"Mom's Day Off"*.
   - It is sincere and generic. That leaves the **Gen Z, affectionate, mum's-own-vocabulary register** open, in the US as well as in Brazil.
6. **The spec standard is not secret.**
   - A container candle burns about **3,5–6,7 g per hour**, median about 4,8; this is computed from 13 published size and burn-time pairs in §5.
   - So **200 g gives roughly 35–55 h**. Brazilian brands claim 25–40 h for 145–200 g.
   - Waxes: soy, a coconut blend, or "vegetable" wax. Wicks: cotton, or wood for the crackle.
   - The safety copy is near-universal: trim the wick, do a full melt pool on the first burn, never more than 4 h at a time.
7. **"Coconut apricot" wax contains paraffin.** CandleScience lists its blend as *"Apricot, Coconut, Paraffin, Soy"*, and says *"the inclusion of paraffin is key to this wax's strong fragrance throw."*
   - So a label claiming *"100% vegetal"* cannot use that wax. Choose the wax before writing the claim.
8. **Mothers' habits supply vessel ideas.**
   - Brazilian mums keep everything: the ice-cream tub full of beans (named in a PiniOn survey of national habits), the requeijão glass used as a drinking glass, and the cookie tin full of sewing thread.
   - **A vessel designed for its second life in mum's kitchen is a joke she gets and a sustainability story at the same time.** See §7.
9. **Recommended price band:**
   - **Hero 200 g: R$139.** That is R$69,50 per 100 g, the L'Occitane and Mels tier: above drugstore Granado, below Antik.
   - **Gift box with a write-on card: R$159.**
   - **Duo (hero plus an 80 g mini): R$199.**
   - **Mini: R$59.**
   - All of these sit inside the R$100–200 Gen Z gift band and under the R$262–294 average Mother's Day ticket (`culture.md` §1).

---

## 1. Brazil: priced candles, read on the seller's own page

**Notes on reading the table:**
- "R$/100 g" is computed by me from the price and the stated net weight.
- "Stock" is the store's own `AvailableQuantity` at fetch time; 0 means out of stock, but the price is still published.
- Época Cosméticos product URLs are given in their public form, `https://www.epocacosmeticos.com.br/{slug}/p`. The API returned an internal VTEX host; I resolved one public URL to HTTP 200 to confirm the mapping.

| # | Brand (origin) | Product | Vessel and closure *(observed in photo where marked)* | Net fill | Burn time stated | Wax and wick (as stated) | Price | R$/100 g | Source (fetched 5–6 Oct 2026) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Granado** (pharmacy heritage, *"mais de 140 anos"* per its own copy) | Vela Perfumada Terrapeutics Gengibre / Calêndula / Lavanda / Chá Branco | Frosted glass embossed with a floral motif; printed carton (photo) | 180 g | Not stated ("duração prolongada") | *"cera vegetal de coco 100% de origem natural"*; Pague Menos: *"Ceras vegetais (coco e palma)"* | **Época R$135,95** (Gengibre) and R$128,95 (Calêndula), in stock · **Drogaria São Paulo R$89,99–92,99**, stock 0 · **Pague Menos R$113,95** (Calêndula), and R$59,99 promo (de R$87,99), stock 0 | 33–76 | [Época](https://www.epocacosmeticos.com.br/vela-perfumada-terrapeutics-gengibre-180g---granado-248572/p) · [DSP](https://www.drogariasaopaulo.com.br/vela-perfumada-vegetal-granado-terrapeutics-calendula-180g/p) · [Pague Menos](https://www.paguemenos.com.br/vela-perfumada-terrapeutics-calendula-180g-granado-1i7p2121946w5428/p) |
| 2 | **Phebo** (*"Fundada em Belém"*) | Cajueiro *Isolda* collab · Folhas de Figo | Cajueiro: *"copo decorado de vidro fosco e arte em hot stamping dourado"* plus a printed fabric pouch. Figo: *"latinha"*, a tin | 180 g · 260 g | Not stated | *"cera vegetal"* (Cajueiro) | **R$116,90** (Cajueiro) · **R$103,90** (Figo) · R$68,90 promo on Vic Meirelles collab (de R$103,90); all stock 0 | 65 · 40 | [Época Cajueiro](https://www.epocacosmeticos.com.br/vela-phebo-cajueiro-isolda/p) · [Época Figo](https://www.epocacosmeticos.com.br/vela-perfumada-phebo-folhas-de-figo/p) |
| 3 | **L'Occitane au Brésil** | Vela Perfumada Bem-Estar Relaxante (line *Casa Brasileira*) | Frosted glass with a colourful "CASA" label (photo); protective disc on the wax | 170 g | Not stated; *"máximo de 4 horas"* per burn | Not stated on page | **R$139,99** | 82 | [L'Occitane au Brésil](https://br.loccitaneaubresil.com/pt-br/p/vela-perfumada-bem-estar-relaxante-170g/BROBVS100659.html) · [Casa Brasileira line](https://br.loccitaneaubresil.com/pt-br/casabrasileira.html) |
| 4 | **Bendita Vela** (DTC, Nuvemshop) | Vela Ipanema Beach · Vela Baunilha *olho grego* | Ipanema: clear glass, silver metal lid, *"Vidro importado"*. Olho grego: glass with a suede cord and evil-eye pendant, *"Acompanha lata da marca"* | 200 g · 145 g | **35 h** · **25 h**; *"Expansão da fragrância: até 30 m² / 20 m²"* | *"cera vegetal, sem adição de parafinas"* | **R$99,00** · **R$59,99** on the product page (home tile shows R$62,99) | 49,5 · 41,4 | [Ipanema](https://benditavela.com.br/produtos/vela-ipanema-beach-200-g-7i5xr) · [Olho grego](https://benditavela.com.br/produtos/vela-baunilha-olho-grego) |
| 5 | **Naturel velas** (DTC) | Vela Aromática Figo & Cassis | Matte black vessel, wood lid, **wooden wick**, a floral pop-up gift box (photo); sells a **refill** | 180 g | Not stated | *"cera 100% vegetal em um frasco de vidro com tampa e pavio de madeira, 180g"*; ships with a box of matches | **R$109,00** (range R$109–119 on the catalogue tiles) | 60,6 | [Naturel](https://lojanaturel.com.br/produtos/vela-aromatica-figo-cassis/) |
| 6 | **Herô Skin Beauty** (indie beauty) | Vela Manjerona · Vela Mushroom | Clear glass tumbler, minimal white label *"200g / 7.05 oz"* (photo) | 200 g | Not stated | *"cera vegetal… livre de parafina"* | **R$110,90** (de R$180,00); Mushroom R$118,90 (de R$180) | 55,5 (90 at list) | [Época Manjerona](https://www.epocacosmeticos.com.br/vela-manjerona-200-g/p) |
| 7 | **Mels Brushes** (beauty brand) | Vela Aromática Café Brasil | Not described | 200 g | Not stated | Not stated | **R$144,90** | 72,5 | [Preço Popular](https://www.precopopular.com.br/vela-aromatica-mels-brushes-200gr-cafe-brasil/p) |
| 8 | **Lucci** (sold by aiká body & soul) | **Birthday Cake** · **Love** | Clear glass with a **wood lid**, coloured sprinkles or **wax hearts on top**; *"Happy B-Day!"* appears as it burns; 8,5 cm × 8 cm | 250 g | Not stated | *"cera de soja e barbante"* | **R$126,31** each | 50,5 | [Época Birthday Cake](https://www.epocacosmeticos.com.br/vela-decorativa-aromatica-birthday-cake-vidro-com-tampa-250g-231047/p) · [Época Love](https://www.epocacosmeticos.com.br/vela-decorativa-aromatica-love-vidro-com-tampa-madeira-250g-231048/p) |
| 9 | **Océane** (beauty brand, own site) | Scented Candle Bergamota e Âmbar · 3-Pavios 290 g · Kit 3 × 50 g | Not described; 3-wick format | 180 g · 290 g · 3 × 50 g | Not stated (*"duração prolongada"*) | **Paraffin**: *"Paraffin, Paraffinum liquidum, Oils, Palm, Stearins, Synthetic wax, Fragrance"* | **R$69,90** (de R$99,90) · **R$99,90** (de R$130,90) · **R$99,90** (de R$145,90) | 38,8 · 34,4 · 66,6 | [Océane 180 g](https://www.oceane.com.br/vela-de-bergamota-e-amber-scented-candle-180g-ap2000598cr1003/p) · [3 pavios](https://www.oceane.com.br/vela-3-pavios-de-bergamota-e-amber---scented-candle-290g-ap2000600cr1003/p) |
| 10 | **Glow Vibes** | "Amor à Primeira Faísca", label *"NO BAD VIBES"* | Clear glass, lilac full-front label with hand lettering (photo) | 170 g | Not stated | *"Massa de soja: 2x mais essência"* | **R$74,90**, stock 0 | 44,1 | [Época](https://www.epocacosmeticos.com.br/vela-aromatica-glow-vibes/p) |
| 11 | **Hello Hello by Nah Cardoso** (Ciclo Cosméticos, influencer line, Época exclusive) | Vela Hello Hello | Not described | Not stated | Not stated | *"óleos naturais de coco e palmiste"*, cotton wick | **R$79,99**, stock 0 | n/a | [Época](https://www.epocacosmeticos.com.br/vela-hello-hello-by-nah-cardoso/p) |
| 12 | **Tok&Stok** (house brand) | Lines: Essencials, Black, Naturals, Minerals, Mon Jardin, Ritual Spa, Caminhos do Sol and others | Glass *pote* in colour editions; Mon Jardin is **frosted pastel pink** (photo) | Not stated; shipping weight 0,32–0,46 kg *including glass* | Not stated | *"cera vegetal"* (Naturals); *"Parafina"* listed as material on Minerals, Mon Jardin and Bonnieux | **R$52,90–109,90** on promo (list R$99,90–139,90) | n/a | [Tok&Stok API](https://www.tokstok.com.br/api/catalog_system/pub/products/search?ft=vela%20perfumada) · e.g. [Mon Jardin Vanilla](https://www.tokstok.com.br/jardin-i-vela-perfumada-pote-vanilla-bege-branco-mon/p) |
| 13 | **Perfuma & Decora** | Pistache Cream · Manga & Damasco · Canela & Patchouli | Clear glass, gold lid, cream label (photo); **2 wicks** | 400 g | Not stated; first burn *"3 a 4 horas"* | *"cera de coco natural"*, *"dois pavios de algodão"* | **R$159,90–169,90** | 40–42,5 | [Época Pistache](https://www.epocacosmeticos.com.br/vela-aromatica-pistache-cream-perfuma---decora-400g-291753/p) |
| 14 | **Antik** (premium perfumery) | Sementes do Brasil · Jardim Mediterrâneo · 30 Memórias | Dark textured vessel, burnt-orange label, white box (photo) | 190 g (90 g mini) | Not stated; *"Não deixe a vela acesa mais que três horas seguidas"* | *"Contém parafina vegetal"* | **R$247–284** for 190 g; R$247,20 for 90 g (de R$309) | 130–149 | [Época Sementes](https://www.epocacosmeticos.com.br/vela-perfumada-sementes-do-brasil---190g-207724/p) |
| 15 | **L'odorat** | Vela Verbena | Glass, lid of reclaimed wood, **wooden wick** (*"pequenos estalos"*) | Not stated | **30 h** | *"Ceras vegetais, cera de abelha e fragrância"* | **R$109,90**, stock 0 | n/a | [Época](https://www.epocacosmeticos.com.br/vela-perfumada-lodorat-verbena/p) (lodorat.com.br blocked) |
| 16 | **Imaginarium** (licensed toys and gifts) | Vela no Pote Harry Potter: Caldeirão, Edwiges, **Chapéu Seletor** | Themed pot; the Sorting Hat candle's *"cera derrete e revela o papel vegetal interno"* | Not stated | Not stated | *"cera de parafina"* | **R$139,90–199,90** | n/a | [Imaginarium](https://loja.imaginarium.com.br/vela-no-pote-hp-chapeu-seletor/p) |
| 17 | **Westwing** (design marketplace) | Decorative, sculptural and coloured candles | Bubble and bust candles, checkerboard and spiral *candy colors* tapers, house-shaped candles; *Pirilampa* designer candles | Not stated | Not stated | Not stated | **Velas Bubble R$42,90 · Vela Busto (Wolff) R$59,90 · Pirilampa R$209,90–269,90 · Candy Colors Espirais 6 pç R$272,90** | n/a | [Westwing velas](https://www.westwing.com.br/velas-e-aromas/velas/) |
| 18 | **Jo Malone London** (import) | English Pear & Freesia | Brand box, *"modelo da caixa… envio aleatório"*; lid usable as a snuffer | Not on page | **45 h** | Not stated | **R$595,00** (de R$700,00) | n/a | [Época](https://www.epocacosmeticos.com.br/vela-perfumada-jo-malone-london-english-pear--freesia/p) |
| 19 | **Sisley** (import) | Rose / Tuberose / Campagne Candle | *"cera negra"* (Tuberose) | Not stated | 4 h max per burn | Not stated | **R$450,00**, stock 0 | n/a | [Época](https://www.epocacosmeticos.com.br/rose-candle-sisley-vela-perfumada/p) |

**Also seen, for context:**
- Nesti Dante (Italy): R$170,98–216,06, *"cera vegetal"*.
- Elemento Mineral: R$141,55, carnaúba plus vegetable oils, 20–25 h.
- Orgânica: R$89,99–98,60, palm wax, 2 wicks.
- La Florentina: kit with a 160 g candle, *"40 horas"*, R$165–172.
- Gift kits that bundle a candle: Granado diffuser plus candle R$212 · Felisa perfume plus candle R$579,90 · Guerlain R$450 · Océane "Kit Ritual do Sono" R$184,90.
- All of these are from the [Época API "vela perfumada"](https://www.epocacosmeticos.com.br/api/catalog_system/pub/products/search?ft=vela%20perfumada) and the [Océane API](https://www.oceane.com.br/api/catalog_system/pub/products/search?ft=vela).

**The artisanal floor:**
- *"No mercado online, velas artesanais costumam ser vendidas entre R$ 16 e R$ 55, enquanto kits personalizados podem ultrapassar R$ 100"* ([O Hoje, 11 May 2026](https://ohoje.com/2026/05/11/mercado-de-velas-aromaticas-cresce-quase-200-no-brasil/)).
- Wedding-favour minis come in packs of 10–50 ([Casamentos.com.br, Encanto Decor](https://www.casamentos.com.br/lembrancas-de-casamento/encanto-decor-aromas--e424403)).

**Market growth, with a scope conflict:**
- Candle-making MEIs went from **570 (2021) to 1.685 (2025), +195,6%**.
- [O Hoje](https://ohoje.com/2026/05/11/mercado-de-velas-aromaticas-cresce-quase-200-no-brasil/) says *"no país"*. [ABC do ABC](https://www.abcdoabc.com.br/velas-aromaticas-setor-cresce-195-meis-sp/) attributes the same numbers to **Sebrae-SP, "no estado"**.
- Since the source is Sebrae-SP, **read it as São Paulo state; the national scope is UNVERIFIED.** `culture.md` §0.10 says national and should be corrected.

---

## 2. What is saturated in Brazil

This is observed, from ~100 distinct candle names across Época, Tok&Stok, Océane, Granado retailers and Bendita/Naturel, plus 11 product photos.

| Dimension | The saturated default | Evidence |
|---|---|---|
| **Vessel** | Clear or frosted glass tumbler, 7–9 cm tall | 8 of 11 photos: Granado, Lucci, Perfuma & Decora, Herô, Glow Vibes, Tok&Stok, Bendita, L'Occitane. The other 3 are dark or matte (Antik, Naturel) and white with gold foil (Phebo) |
| **Lid** | Bamboo or wood (artisanal and "natural" positioning), or gold or silver metal | Lucci, Naturel and L'odorat (wood); Perfuma & Decora and Bendita (metal) |
| **Label** | Small, quiet, white or kraft; thin type; product name plus weight | Herô, Perfuma & Decora, Granado |
| **Colour** | White, cream, beige, frosted, pastel pink, occasional black | Tok&Stok *Mon Jardin* rosé; Antik and Naturel black |
| **Naming** | Ingredient (flowers 14, citrus 8, ginger 7, lavender 7, bergamot 7, sandalwood 5, white tea 5, lemongrass 5) or place (9: Ipanema, Amalfi, Mediterrâneo, Brasil, Portofino) | Keyword tally on 102 names (§ method in raw scripts) |
| **Claim** | *"cera vegetal"*, *"vegano"*, *"artesanal"*, *"não libera fumaça escura"*, *"bem-estar"* | Granado, Herô, Bendita, Phebo, L'odorat |
| **Positioning** | Spa, self-care and ritual (Terrapeutics, Ritual Spa, Bem-Estar Relaxante, Time to Relax) | Granado, Tok&Stok, L'Occitane, Elemento Mineral |
| **Gift format** | Kit with a perfume, cream or diffuser; printed carton | Granado, Océane, Felisa, Guerlain |

**On the beige amber jar the brief asks about:** the amber jar with a kraft label and brass lid is **P.F. Candle Co.'s** signature (US). It is not the Brazilian default. **In Brazil the cliché is the frosted or clear tumbler with a bamboo lid and a whisper-quiet label**, in the spa-wellness register. The effect for a new brand is the same: everything reads as one beige, calm, interchangeable shelf.

---

## 3. What is missing in Brazil, which is the white space

1. **An owned colour.** No opaque, saturated-colour vessel was found in the sample. Glossier's red and Otherland's yellow show what one does globally.
2. **Big type.** No Brazilian label I saw uses one huge phrase as the design. Homesick built a business on that alone.
3. **A voice.** About 6% of names carry any mood. The few that do are generic English (*No Bad Vibes, Love, Happy B-Day*) or an influencer's name. **Nobody writes in mum's Portuguese.**
4. **Mother's Day as a candle occasion.** Zero Brazilian candles in the sample are built for the date. The big-brand Mother's Day gift kits are perfume and body care (O Boticário: 16 kits plus 20 combos in 2026, per [Bem Paraná](https://www.bemparana.com.br/publicacao/blogs/simonebello/boticario-lidera-preferencia-de-presente-sem-erro-para-o-dia-das-maes-e-oferece-mais-de-35-kits-e-combos-presenteaveis-com-ate-30-de-desconto/), secondary). The candle appears only as an add-on inside those kits.
5. **Play mechanics, which do exist and are proven sellers but are not owned by anyone:**
   - Lucci's message that appears as the candle burns.
   - Imaginarium's Sorting Hat paper revealed as the wax melts.
   - Westwing's sculptural, bubble, bust, checkerboard and twisted-taper decor candles at R$27,90–272,90.
   - **A brand could own "the reveal"** as a system, for example a phrase from mum that appears as the wax goes down. **This needs to be checked for safety. A paper insert that is exposed as the wax melts is a fire question: UNVERIFIED, and it needs a candle maker's sign-off.**
6. **A gourmand of Brazilian home food.** Gourmand appears in only 5 of 102 names, and those are *pistache cream, café, macaron, coconut lemonade*. Nobody does *bolo de fubá, café passado, arroz-doce* or *roupa no varal*, though `culture.md` already proposes the first three.

---

## 4. Global references: what makes each iconic

Vessel descriptions marked *(photo)* are what I saw in the brand's own product image, downloaded to `raw_cat/img/` and viewed. Prices are the brand's own; BRL is at PTAX of 5 Oct 2026.

| Brand | Hero product | Vessel and pack *(photo)* | Size, burn, wax | Price (≈R$) | Naming and copy | The one thing to steal |
|---|---|---|---|---|---|---|
| **Homesick** (US) | **Thank You, Mom** | Clear glass in a **soda-can silhouette**; label reads *"13.75oz | 390g"*; plain white label with **huge black "THANK YOU, MOM"**; **floral-printed box**, *"Make it personal with a handwritten note on the box"* *(photo)* | 13,75 oz (390 g) · **60–80 h** · *"natural soy wax blend"*, cotton wick | **US$29,95** (≈R$149) | Places, moments and pop collabs (nav shows Harry Potter, FRIENDS, Seinfeld, Powerpuff Girls, Gilmore Girls, OLIPOP, **KFC**); also *"Mom's Day Off"*. Copy: *"A house made home because of you."* | **The phrase is the product.** One line, set huge. A write-on box. [page](https://homesick.com/products/thank-you-mom) |
| **Glossier** (US) | Glossier You candle · Birthday Cake candle | **Glossy red glass with an embossed G and no label** (You) *(photo)*; Birthday Cake *"custom-molded glass jar with a chrome finish"* | 8 oz / 226 g · **~45 h** · *"vegan, non-paraffin blend of soy and coconut"* | **US$45** (≈R$224) · Birthday Cake **US$50** (≈R$249) | Turns the brand's own icon into a scent (*Glossier You*, *Birthday Balm Dotcom*). Copy: *"You(r space) smells good."* | **Colour plus emboss, no label at all.** A vessel that is the logo. [You](https://www.glossier.com/products/glossier-candle) · [Birthday Cake](https://www.glossier.com/products/birthday-cake-candle) |
| **Otherland** (US) | Canary (daffodil) | **Saturated yellow tinted glass with a printed flower collage** *(photo)*; *"Perfumer crafted. Art inspired.™"* | 8 oz / 226 g · **up to 55 h** · *"Premium coconut and soy wax blend"* · 100% cotton wick · 3,25" tall | **US$20** (≈R$100) observed today (formerly higher: UNVERIFIED) | Scent as a colour story; bundle-builder discounts of 10% for 3 and 15% for 6 | **One colour per scent; the art does the talking.** [page](https://www.otherland.com/products/canary) |
| **Boy Smells** (US) | KUSH | **Black glass with "Boy Smells" embossed round the base; a flat pink rectangular label**; boxed *(photo)* | 8,5 oz (241 g) · **50+ h** · *"US farmed soy blend"*, vegan | **US$44** list, US$31 sale on the product feed (≈R$219 / R$155) | Provocative one-word names (*KUSH, ASH, LES*); *"Feels Like: a high flower"* | **A two-colour system** (black and pink) that reads at any size. [page](https://boysmells.com/products/kush-candle-standard-9oz) |
| **Diptyque** (FR) | Roses classic candle | **Clear tumbler with the oval label whose name letters dance round the oval** *(photo)* | **190 g · ~50 h** · 9 cm × Ø 7,7 cm; the brand's own table runs from 35 g/10 h to 5 kg/300 h; **refills sold (€50)** | **€65** (≈R$363) | Poetic micro-stories: *"La bougie parfumée Roses raconte les rosiers au mois de mai."* | **A typographic device that is the brand** (the oval). Refills as ritual. [page](https://www.diptyqueparis.com/products/bougie-modele-classique-roses-ro3) |
| **Snif** (US) | **Prenup** · Old Money | **Dark smoky fluted (ribbed) glass over an opaque black base band carrying the name in white script** *(photo)* | 6 oz **35+ h** · 8,5 oz **50+ h** · soy blend · 100% cotton-fibre wicks | **US$34 / US$46** (≈R$170 / R$229) | **Joke names with straight-faced luxury copy**: *"Nothing says I love you like an iron-clad prenup."* | **Deadpan humour plus a luxe vessel**, which is exactly the Gen Z register. [page](https://snif.co/products/prenup-candle) |
| **Liquid Death × Martha Stewart** (US) | Dismembered Moments | **Sculptural black candle of a hand clutching a can** *(photo)* | n/a | **US$58** (≈R$289) | *"It is so realistic that you and your guests might wonder just how Martha made them."* | **Absurdist collab plus sculpture.** A candle as a meme object. [page](https://liquiddeath.com/products/martha-stewart-x-liquid-death-dismembered-moments-candle) |
| **P.F. Candle Co.** (US) | Teakwood & Tobacco · Spruce | **Amber glass jar, kraft paper label, brass lid**; 3,5" × 2,9" *(photo)*. This is *the* amber-jar archetype | 7,2 oz (204 g) · **40–50 h** · *"100% soy wax"*, cotton-core wicks | **US$24** (≈R$120) | Numbered scents; Californian craft | The amber archetype: **this is what not to do.** [page](https://pfcandleco.com/products/spruce-standard-candle) |
| **Brooklyn Candle Studio** (US) | Minimalist jar · Classic 2-wick | Clear jar, gold lid, white minimalist label *(photo)* | Size not stated in the feed · 100% soy, lead-free cotton wicks | **US$34** jar / **US$45** 2-wick | Travel names (*Montana Forest, Santorini, Japanese Satsuma*) | Minimal done well, but it is the same beige shelf as Brazil. [page](https://brooklyncandlestudio.com/products/montana-forest-jar-candle) |

**Patterns across the icons:**
1. One owned visual element: a colour, a typographic device, a sculpture, or one giant phrase.
2. Names that are a joke or an attitude, not an ingredient list: *Prenup, KUSH, Thank You Mom, Dismembered Moments*.
3. The vessel is designed to be kept. Glossier says so outright: *"reuse the glass vessel to store makeup, pencils or whatever your heart desires!"*
4. A gift box that does work: Homesick's write-on box, Boy Smells' box.

---

## 5. Specs primer for the product and the 3D build

### 5.1 Burn rate, computed from published size and burn-time pairs

| Product | Fill (g) | Burn (h) | g/h |
|---|---|---|---|
| Diptyque petit / classique / moyen / grand | 70 / 190 / 300 / 600 | 20 / 50 / 75 / 90 | 3,5 / 3,8 / 4,0 / 6,7 |
| Otherland | 226 | 55 | 4,1 |
| La Florentina (Época) | 160 | 40 | 4,0 |
| P.F. Candle Co. | 204 | 40–50 | 4,1–5,1 |
| Boy Smells | 241 | 50 | 4,8 |
| Snif 6 oz / 8,5 oz | 170 / 241 | 35 / 50 | 4,9 / 4,8 |
| Glossier | 226 | 45 | 5,0 |
| Homesick | 390 | 60–80 | 4,9–6,5 |
| Bendita Vela 200 g / 145 g | 200 / 145 | 35 / 25 | 5,7 / 5,8 |

⇒ **Range 3,5–6,7 g/h, median ≈4,8 g/h.** A **200 g** candle supports an honest **"até 40 horas"**: 200 ÷ 5 = 40. Claiming 50 h needs ≤4 g/h, which is Diptyque or Otherland territory and needs testing. **Any burn-time claim on the fictional label should say "aprox." and be treated as illustrative.**

### 5.2 Wax

| Wax | Who uses it here | Notes |
|---|---|---|
| Soy (100% or blend) | P.F., Brooklyn Candle Studio, Boy Smells (soy blend), Homesick, Snif, Lucci, Glow Vibes | Creamy, matte top; frosting and wet spots are normal |
| Coconut or coconut-soy | Glossier (soy plus coconut, *"non-paraffin"*), Otherland, Granado (*"cera vegetal de coco"*), Perfuma & Decora | Smooth, glossy top. **Renders well**: a slightly translucent, satin surface |
| **"Coconut apricot" (CandleScience)** | Craft-supplier blend | **Contains paraffin**: *"Apricot, Coconut, Paraffin, Soy"*; max fragrance load *"10% or 1.6 oz/lb"*; pour at 77 °C; cure *"one to two days"* ([CandleScience](https://www.candlescience.com/wax/candlescience-coconut-apricot-wax)). **Never pair it with a "100% vegetal" claim** |
| Paraffin | Océane, Tok&Stok Minerals and Mon Jardin, Imaginarium; global share 30,4% in 2025 per an aggregator (secondary, [ringly](https://www.ringly.io/nl/discover/candle-industry-statistics-2026)) | Cheapest; strongest throw |
| Palm, carnauba, beeswax | Orgânica (palm), Elemento Mineral (carnauba), L'odorat (with beeswax) | Niche |

**Recommendation for the fictional label:** *"cera vegetal de coco e soja"*, cotton wick. It is plausible, matches the Brazilian claim norm, and is consistent with Glossier and Otherland. Do not write "atóxica" or health claims.

### 5.3 Wick

- **Cotton:** the default everywhere. Renders as a thin black-tipped braid with a teardrop flame.
- **Wood:** Naturel and L'odorat in Brazil sell the crackle (*"provocando pequenos estalos enquanto queima"*). It renders as a thin flat plank with a **wide, low, horizontal flame**, a distinctive silhouette, and **the crackle is free sound design for the film.** The trade-off is that the flame is less iconic than a teardrop.
- Multi-wick (2–3) is the large-format norm: Perfuma & Decora 400 g, Océane 290 g, Otherland 26 oz.

### 5.4 Fill weights, sizes and lids

- **Brazilian standard sizes:** 145 · 170 · 180 · 190 · 200 · 250 · 260 · 290 · 400 g. **180–200 g is the modal hero.**
- **Global standard sizes:** 7,2–8,5 oz (204–241 g), with Homesick at 13,75 oz.
- **Typical tumbler:** about 8–9 cm tall × 7,5–8 cm diameter. Diptyque is 9 × 7,7; Lucci 8,5 × 8; Bendita 200 g is 9 × 8.
- **Lids:** wood or bamboo (BR artisanal, saturated) · metal gold or silver · none (Glossier, Diptyque) · the lid doubling as a snuffer (Jo Malone).
- **Gift packaging seen:**
  - printed carton (Granado);
  - fabric pouch (Phebo *Isolda*);
  - tin (Bendita *"lata da marca"*, Phebo *latinha*);
  - floral pop-up box (Naturel);
  - floral printed box with a write-on note (Homesick);
  - matches included (Naturel).

### 5.5 Care copy, used near-universally

Trim the wick to 0,5 cm. On the first burn, let the whole surface melt (3–4 h). Never burn for more than 4 h at a time. Stop when 0,5 cm of wax remains. Keep away from flammables, children and pets. This appears at Bendita, Herô, Perfuma & Decora, Boy Smells, P.F. and Diptyque. **Write this in the fictional label's back panel. It is the line that makes a mock label look real.**

---

## 6. Market and gifting signals worth citing

- **NCA (US trade body):**
  - *"Approximately 35% of candle sales occur during the Christmas/Holiday season."*
  - Gifting occasions: holidays 76%, housewarming 74%, hostess 66%, thank-you 61%, adult birthdays 58%.
  - *"Approximately three-fourths of candle users say they typically burn candles for 4 hours or less per sitting"*, and *"Three-fourths of candle buyers"* rate scent as extremely or very important.
  - US retail ≈US$3,14 bn.
  - **Mother's Day is not in the NCA's occasion list, so it is an under-claimed occasion even in the US.** Source: [candles.org/facts-figures](https://candles.org/facts-figures/).
- **2026 Gift Book Consumer Survey** (trade press, [Gifts & Decorative Accessories, 30 Oct 2025](https://www.giftsanddec.com/trending-gifts/product-trends/looking-to-light-up-your-shelves-with-fresh-inventory-here-are-the-top-candle-trends-for-2026)):
  - decorative candles are *"the No. 1 home fragrance product that consumers across all generations say they plan to buy"*;
  - floral/botanical is the favourite profile for **74% of Gen Z**;
  - 33% of Gen Z plan to buy a handmade candle.
  - **Sample size not stated: secondary.**
- **Circana via GCI Magazine:** *"TikTok driving 66% of [Gen Z] fragrance purchases"*. **UNVERIFIED**: the GCI page returned 403, so this is a search-snippet figure only. Do not quote it client-facing.

---

## 7. Recommendation: vessel and price

### 7.1 The vessel that would stand out, and render well

Three options. The first is the recommendation. All three are cylinders with flat or cylindrical labels, so they suit the production rules (Blender Cycles; the label composited as a cylinder wrap; no curved-compound label).

**A. RECOMMENDED: "O copo que fica" (the glass that stays).**
- **The vessel:** an **opaque, glossy, saturated-colour straight-wall glass tumbler**, about Ø 8 × 9,5 cm, 200 g.
  - It has a **flat, heavy base** with the brand embossed underneath: the Boy Smells and Glossier move.
  - It carries **one giant phrase in mum's voice** on a full-height label wrapping about 60% of the circumference: the Homesick move.
  - Its **colour-matched flat lid** doubles as a coaster.
  - The vessel is designed as a **drinking or storage glass for afterwards**. That is the Brazilian mother's *copo de requeijão* instinct: requeijão glasses are kept and *"mais usada… depois de usar o potinho de requeijão"* ([TudoGostoso](https://www.tudogostoso.com.br/noticias/como-reutilizar-copo-de-requeijao-a6924.htm)).
- **Why it wins:**
  - it occupies the empty cell in the Brazilian sample: an owned colour plus big type;
  - it reads at thumbnail size;
  - it is the simplest object to render photoreally: a glossy dielectric over a coloured base, a satin wax top with a slight memory-ring meniscus, an emission-plus-volume flame, and the label as UV-wrapped decal;
  - and one colour per scent gives the range an Otherland-style wall.
- **Render notes:**
  - The label is a cylinder wrap on a 1–2 mm offset shell.
  - The wax top sits 8–12 mm below the rim, with a slight concave pool when lit.
  - A cotton wick gives a teardrop flame for hero shots.
  - Hard flash plus a coloured seamless backdrop matches the Gen Z ad language; soft light suits the mum-facing shots.

**B. "A lata" (the tin).**
- A printed steel tin with a lid, about Ø 9 × 7 cm, in the lineage of Phebo's *latinha* and Bendita's *lata*.
- It plays on the mum meme of the cookie tin full of sewing thread: forum joke *"Já vem com o kit de costura dentro?"*, seen in a [Pelando deal thread](https://www.pelando.com.br/d/biscoitos-amanteigados-uva-passas-114g-b2fe), **user comments, a cultural observation, not a measurement**.
- It is very easy to render: a metal cylinder with the print as a texture.
- **The trade-off:** a tin hides the flame and the wax colour in the closed shot, and tins are already Phebo's code.

**C. "O pote de sorvete" (the ice-cream tub).**
- A candle poured into a mock 2 L ice-cream tub, a joke on the Brazilian mother's tub full of beans.
- *"colecionar potes de sorvete transformados em recipientes de feijão"* is named among national-identity habits in a **PiniOn survey** ([Mundo do Marketing](https://mundodomarketing.com.br/humor-e-memes-definem-a-identidade-do-brasil-nazare-se-torna-simbolo-nacional); sample size not stated).
- **Strongest joke, weakest product:** a wide, shallow plastic tub is a fire-safety and burn-quality problem (a wide pool needs multi-wick), and the shape reads as cheap.
- **Keep it as a campaign gag or a limited-edition gift box, not as the hero vessel.** Avoid any real ice-cream brand's trade dress.

### 7.2 Price architecture (fictional, for the sample case)

| SKU | Fill | Price | R$/100 g | Logic |
|---|---|---|---|---|
| **Hero** ("copo que fica") | 200 g, about 40 h | **R$139** | 69,5 | Sits with L'Occitane (R$139,99/170 g) and Mels (R$144,90/200 g); above Granado and Phebo at the median retailer; below Antik (R$247+). Inside the Gen Z R$100–200 budget |
| **Hero + write-on gift box + card** | 200 g | **R$159** | — | The Homesick handwritten-box move; Sebrae's own advice is *"kits prontos… embalagens especiais… cartão personalizado"* (`culture.md` §1) |
| **Duo kit** (hero + mini) | 200 g + 80 g | **R$199** | 71 | The Mother's Day "kit" format the category already sells (Granado R$212, Océane R$184,90). Under the R$262–294 average ticket, so it pairs with a card or flowers |
| **Mini** | 80 g, about 16 h | **R$59** | 74 | Gen Z self-purchase and add-on; matches Bendita's R$59,99 for 145 g as an entry-price anchor |

---

## 8. UNVERIFIED and caveats, listed so nobody quotes them as fact

- Burn times are **brand-stated**. My g/h figures inherit their optimism.
- Otherland's US$20 is today's price on its own feed and product page. Whether it is a permanent reprice or a promotion is **UNVERIFIED**.
- Boy Smells shows **US$44** on the page and **US$31** in the product feed; that is read as a sale.
- Granado's own site and Phebo's own site are bot-walled. Their prices are **retailer prices**, which vary from R$60 to R$136 for the same Granado 180 g candle.
- **Tok&Stok weights are shipping weights including the glass**, not fill weights.
- The Sebrae MEI growth figure (570 → 1.685) is **São Paulo state per Sebrae-SP**; the national framing in O Hoje and in `culture.md` is unverified.
- The Circana 66% TikTok figure is snippet-only.
- The copo americano "in MoMA" claim found in a search summary was **not confirmed** on the fetched page ([Diário do Rio](https://diariodorio.com/o-copo-americano-nascido-na-industria-virou-simbolo-das-casas-e-bares-do-rio/) says only *"criado em meados do século XX pela fábrica Nadir Figueiredo"*). Do not use it.
- **Regulatory:** ANVISA has fined Brazilian candle makers under Lei 6.360/1976, for example LUME Indústria e Comércio de Velas and ROUGE NOIR CANDLES. That is in `research/src/label/` (another agent's sources). **The label's mandatory fields belong to that research, not this file.**
- Trade-dress: the requeijão-glass, cookie-tin and ice-cream-tub references must use **generic shapes only**, with no real brand's colours or marks.

---

## 9. Sources (all fetched 5–6 Oct 2026 unless noted)

**Brazilian brands and retailers:**
- https://www.epocacosmeticos.com.br/api/catalog_system/pub/products/search?ft=vela%20perfumada
- https://www.epocacosmeticos.com.br/vela-decorativa-aromatica-birthday-cake-vidro-com-tampa-250g-231047/p (resolved HTTP 200)
- https://www.oceane.com.br/api/catalog_system/pub/products/search?ft=vela
- https://www.tokstok.com.br/api/catalog_system/pub/products/search?ft=vela%20perfumada
- https://www.drogariasaopaulo.com.br/vela-perfumada-vegetal-granado-terrapeutics-calendula-180g/p
- https://www.paguemenos.com.br/vela-perfumada-terrapeutics-calendula-180g-granado-1i7p2121946w5428/p
- https://br.loccitaneaubresil.com/pt-br/p/vela-perfumada-bem-estar-relaxante-170g/BROBVS100659.html
- https://benditavela.com.br/produtos/vela-ipanema-beach-200-g-7i5xr
- https://benditavela.com.br/produtos/vela-baunilha-olho-grego
- https://lojanaturel.com.br/produtos/vela-aromatica-figo-cassis/
- https://www.precopopular.com.br/vela-aromatica-mels-brushes-200gr-cafe-brasil/p
- https://loja.imaginarium.com.br/vela-no-pote-hp-chapeu-seletor/p
- https://www.westwing.com.br/velas-e-aromas/velas/

**Global brands:**
- https://homesick.com/products/thank-you-mom
- https://www.glossier.com/products/glossier-candle
- https://www.glossier.com/products/birthday-cake-candle
- https://www.otherland.com/products/canary
- https://boysmells.com/products/kush-candle-standard-9oz
- https://www.diptyqueparis.com/products/bougie-modele-classique-roses-ro3
- https://snif.co/products/prenup-candle
- https://liquiddeath.com/products/martha-stewart-x-liquid-death-dismembered-moments-candle
- https://pfcandleco.com/products/spruce-standard-candle
- https://brooklyncandlestudio.com/products/montana-forest-jar-candle
- Each brand's `/products.json`.

**Specs:**
- https://www.candlescience.com/wax/candlescience-coconut-apricot-wax

**Market:**
- https://candles.org/facts-figures/
- https://www.giftsanddec.com/trending-gifts/product-trends/looking-to-light-up-your-shelves-with-fresh-inventory-here-are-the-top-candle-trends-for-2026
- https://ohoje.com/2026/05/11/mercado-de-velas-aromaticas-cresce-quase-200-no-brasil/
- https://www.abcdoabc.com.br/velas-aromaticas-setor-cresce-195-meis-sp/

**Culture and vessel cues:**
- https://mundodomarketing.com.br/humor-e-memes-definem-a-identidade-do-brasil-nazare-se-torna-simbolo-nacional
- https://www.tudogostoso.com.br/noticias/como-reutilizar-copo-de-requeijao-a6924.htm
- https://www.pelando.com.br/d/biscoitos-amanteigados-uva-passas-114g-b2fe

**FX:**
- https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/ (USD 4,9859; EUR 5,5897; close of 5 Oct 2026)
