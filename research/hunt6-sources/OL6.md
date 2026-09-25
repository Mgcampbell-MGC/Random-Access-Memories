# OL6 — The first 40 brands Sol calls (plus 20 reserves)

*Repository copy: e-mail, phone, WhatsApp and Instagram columns removed (some are personal). The full list is kept outside the repository.*

Agent OL6, 25 Sep 2026. **Hole:** "Who, by name, are the first 40 brands Sol calls?" **Verdict: closed.** There is a named list of 40 brands to call and 20 reserves, built from primary data. It is in `out/OL6_prospects.csv`, and `OL6.json` repeats it with every new SKU and its ANVISA process number. Two parts are still open: 9 of the 40 have no public packshot to build the PRÉVIA from, and CNPJ-record contacts are often not the company's own.

Scripts and intermediate files are in `hunt6/work/ol6/`. Every fetch was a curl or Python `requests` call made from this session.

## 1. How the list was built (counts at every step)

| Step | Count |
|---|---|
| Rows in ANVISA `TA_CONSULTA_COSMETICOS.CSV` (downloaded 25 Sep 2026, 227.527.719 bytes, latin-1, `;`) | **1.201.421** |
| Electronic *Notificado* rows notified in the 90-day window 26 Jun–23 Sep 2026 (notification = `DT_VENCIMENTO` − 10 y, timestamped rows only) | **29.608** (60-day window: 20.213) |
| …classified hair / face / body | **12.010** (hair 6.621 · face 2.911 · body 2.478) |
| …excluded categories | fragrance 5.957 · make-up 3.101 · hair colour/straighteners/chemical 1.503 · soap 1.189 · deo 576 · depilatory/repellent/misc 445 · infant 398 · nails 201 · sunscreen 150 · intimate 125 · oral 122 · unclassified 3.831 |
| Hair/face/body rows with a brand parsed from `NO_PRODUTO` | 10.055 (83,7%) → **3.125 distinct brand keys** |
| Re-filings removed (same name, token-set equal to any earlier row in the file, or ≥75% overlap with a pre-window name of the same brand) | **3.296 rows = 27,4%** (exact-name only: 25,1%) |
| Brands with ≥1 genuinely new SKU | 2.338 · ≥2: 1.416 · **≥3: 885** · ≥5: 388 · ≥10: 104 (≥3 within 60 days: 613) |
| ≥3 new SKUs, after dropping multinationals, large or pharma groups and pharmacy chains (holder-name screen) | 844 |
| …after dropping importer holders (`IMPORT` in the company name) | 770 |
| …after manual exclusions (Korean or foreign brands, importers of Asian lines, essential-oil or diffuser suppliers, large brands) | 716 |
| Website discovery tried (top 520 by launch score) | 520 → **155 sites matched** (137 after the exclusions) |
| Owner CNPJ resolved and looked up on publica.cnpj.ws (short-list of 121) | 79 owners resolved in the first pass, more afterwards |
| **Final: 40 to call + 20 reserves** | 40/40 have an owner CNPJ and a company contact channel. **31/40 have an e-mail, 39/40 a CNPJ phone, 31/40 a WhatsApp number published on their own site, 35/40 an Instagram handle, and 31/40 a public packshot image URL.** 24/40 are in SP. Grades: A 25 · B 15. Size: ME 21 · EPP 15 · Demais 4. |

**Launch score used for ranking:**
- base: new-SKU count, capped at 12;
- plus concentration (new SKUs ÷ filing days);
- +3 if the brand key first appears in the file in 2025 or later (a brand launch);
- +2 if the holder notifies ≤3 brands (it notifies for itself);
- +1 if the holder is in SP;
- penalties for importer holders, "professional" lines, essential-oil lines and very large filers.

**What the file is and is not.**
- It has **no category field and no brand field.** Its fields are `NU_PROCESSO; NO_PRODUTO; NU_CNPJ_EMPRESA; NO_RAZAO_SOCIAL_EMPRESA; DT_VENCIMENTO; ST_SITUACAO_PRODUTO; NU_REGISTRO; DS_TIPO_PETICAO; ST_REGISTRADO; DT_ATUALIZACAO` (header printed and read).
- Category is therefore a keyword classifier over the product name (`classify6.py`), and the brand is parsed from the name by an n-gram vote within each holder (`brand7.py`, `brand8.py`).
- **Notification date check:** the newest row is `25351171698202635` "BODY SPLASH DREAM - PERFUMOÁ", with `DT_VENCIMENTO` "23/09/2036 23:51:42", i.e. notified 23 Sep 2026 23:51:42. The year in the process number matches the derived year on **100% of the 29.608 window rows**.

**Why these categories were excluded.**
- **Sunscreen.** RDC 629/2022 (status "Vigente", fetched from anvisalegis) art. 14: *"Os protetores solares não devem possuir alegações de rotulagem que impliquem … III - denominações que induzam a uma proteção total ou bloqueio da radiação solar."* Art. 15 then lists eight mandatory label warnings, e.g. *"É necessária a reaplicação do produto para manter a sua efetividade"*. A mood image of sun and beach sits right against those claim rules, which conflicts with the offer's claim lock.
- **Hair colour and straighteners.** A shade line inflates the SKU count (one launch becomes dozens of notifications), and straighteners are chemical, professional products.
- **Infant.** Excluded as briefed. Ayllume was dropped after inspection because its own images show "+3 anos" on the bottles.
- **Salon-only lines.** Where identifiable they were graded B, not dropped (Prohall/Faube, Kice, Hoka, Kaeni).

## 2. The call list (40) and the reserves (41–60)

Ordering: pre-launch or brand-new first, then SP own brands with a store, then the rest. Owner data comes from `publica.cnpj.ws/cnpj/<CNPJ>`, fetched per CNPJ. Where the registered name is a person's name (empresário individual), it is withheld and only the CNPJ is given.

| # | Grade | Brand | Owner CNPJ | Size | City/UF | New SKUs, 90 d (first→last, 2026) | Website | Packshot page for the PRÉVIA |
|---|---|---|---|---|---|---|---|---|
| 1 | A | Venexia | 65.987.138/0001-71 | ME | São Paulo/SP | 12 (09-18→09-18) | https://venexia.com.br/ | UNVERIFIED |
| 2 | A | Alleva Beauty | 60.249.460/0001-80 | EPP | São Paulo/SP | 12 (07-01→08-10) | https://www.allevabeauty.com.br/ | https://www.allevabeauty.com.br/skincare/corpo/geleia/geleia-hidratante-corporal-fresh-vanilla-250ml-alleva-skin |
| 3 | A | Klass Vough (Klass Vough Skin) | 02.881.499/0001-19 | EPP | São Paulo/SP | 6 (08-01→08-19) | https://www.klassvough.com/ | https://www.klassvough.com/products/brush-cleanser-500ml-limpador-de-pinceis |
| 4 | A | Barrus | 38.004.418/0001-40 | ME | Amparo/SP | 12 (09-14→09-15) | https://barrus.com.br/ | https://barrus.com.br/produtos/hidratante-facial-uniformizador-60g-natural-e-vegano/ |
| 5 | A | Treeliss | 30.024.139/0001-36 | ME | Osasco/SP | 11 (07-08→09-23) | https://treeliss.com.br/ | https://treeliss.com.br/produtos/shampoo-biotechnologic-protecao-da-cor-1l/ |
| 6 | A | Isabelle la Belle | 59.793.113/0001-34 | EPP | São Paulo/SP | 9 (09-02→09-17) | https://isabellelabelleoficial.com.br/ | https://isabellelabelleoficial.com.br/produtos/creme-hidratante-corporal-angel-200ml-isabelle-la-belle/ |
| 7 | A | InVoga Cosméticos (Voga) | 46.883.458/0001-37 | EPP | Serrana/SP | 12 (07-17→07-17) | https://loja.invogacosmeticos.com.br | https://loja.invogacosmeticos.com.br/produtos/mascara-mandioca-voga-max-care-250g/ |
| 8 | A | Valenzza Cosméticos + Vzzon Fit | 38.238.464/0001-03 | ME | Valinhos/SP | 21 (07-27→09-23) | https://valenzzacosmeticos.com.br/ | UNVERIFIED |
| 9 | A | Zanphy | 05.765.886/0001-88 | ME | Jambeiro/SP | 9 (07-03→08-20) | https://www.zanphy.com.br/ | https://www.zanphy.com.br/products/serum-repair-facial-linha-pele-zanphy-colageno-vitamina-c |
| 10 | A | Mais You Beauty | 46.150.258/0001-75 | ME | Caieiras/SP | 8 (07-06→07-06) | https://www.maisyoubeauty.com.br/ | https://www.maisyoubeauty.com.br/produtos/esfoliante-pitaya-corpo-e-rosto-280g/ |
| 11 | A | Dimmp Cosméticos | 43.287.807/0001-60 | ME | Jales/SP | 5 (08-27→08-28) | https://www.dimmpcosmeticos.com.br/ | https://www.dimmpcosmeticos.com.br/pele/hidratantes-corporais/koncentre-hidratante-corporal-desodorante-maracuja-250ml |
| 12 | A | Terramor | 29.756.612/0001-90 | ME | São Paulo/SP | 9 (07-29→07-29) | https://www.terramor.com.br/ | https://www.terramor.com.br/kit-xampu-e-condicionador-capim-limao-com-alecrim-200ml500ml-500ml |
| 13 | A | Melibliss | 09.334.817/0001-70 | ME | Itanhaém/SP | 4 (09-20→09-21) | https://melibliss.com/ | UNVERIFIED |
| 14 | A | Bauny Cosméticos | 40.867.166/0001-24 | Demais | Mogi das Cruzes/SP | 6 (07-07→09-02) | https://www.bauny.com.br/ | https://www.bauny.com.br/hidratante-facial-vitamina-c/p |
| 15 | A | Zuriel Cosmetics | 13.823.813/0001-23 | ME | Araras/SP | 7 (06-29→09-11) | https://www.zurielcosmetics.com.br/ | https://zurielcosmetics.commercesuite.com.br/home-care/shampoo/shampoo-vegan-sun-300-ml |
| 16 | B | Prohall Professional + Faube | 37.088.088/0001-55 | EPP | Macatuba/SP | 19 (08-03→09-21) | https://prohall.com.br/ | https://prohall.com.br/produto/miracle-therapy |
| 17 | A | AquaOzon | 54.345.828/0001-00 | EPP | Itatiba/SP | 4 (09-15→09-17) | https://aquaozon.com.br/ | UNVERIFIED |
| 18 | A | Eizz Cosmetic Science | 24.188.188/0001-01 | ME | Votuporanga/SP | 6 (08-03→09-01) | https://eizz.com.br/ | https://eizz.com.br/shampoo-nutri-amino-reparacao-250ml-eizz/p |
| 19 | A | Silent.Ritual (Aben Beauty) | 58.114.672/0001-08 | ME | Porto Alegre/RS | 14 (06-29→09-08) | https://silentritual.com.br/ (password page) | UNVERIFIED |
| 20 | A | Kalenza Cosmetics | 15.765.912/0001-21 | EPP | Contagem/MG | 13 (06-29→09-03) | https://kalenzacosmetics.com.br/ | UNVERIFIED |
| 21 | A | Hidrabene | 82.914.334/0001-35 | Demais | Camboriú/SC | 12 (06-29→08-26) | https://hidrabene.com.br/ | https://hidrabene.com.br/products/retinol |
| 22 | A | Natuza Cosméticos | 11.761.463/0001-92 | EPP | Aparecida de Goiânia/GO | 19 (07-24→07-31) | https://natuzacosmeticos.com.br/ | https://natuzacosmeticos.com.br/ |
| 23 | A | Elefthéria Cosmetics | 59.563.068/0001-21 | EPP | Araquari/SC | 5 (07-02→07-09) | https://eleftheria.com.br/ | https://eleftheria.com.br/produtos/leave-in-liquido-eleftheria/ |
| 24 | A | Huringa | 43.327.483/0001-46 | ME | Ampére/PR | 5 (07-29→07-29) | https://usehuringa.com.br/ | https://usehuringa.com.br/produtos/bakuchiol-peptideos-advanced-serum-peles-maduras-5khxj/ |
| 25 | A | Nativa Ecocosméticos | 25.325.948/0001-48 | EPP | Vitória/ES | 6 (09-15→09-15) | https://www.nativaecocosmeticos.com.br/ | https://www.nativaecocosmeticos.com.br/geleia-em-creme-finalizador-para-cachos |
| 26 | B | Dellara Cosméticos | 37.576.363/0001-80 | EPP | Rio de Janeiro/RJ | 7 (09-04→09-04) | https://dellara.com.br/ | https://dellara.com.br/produtos/serum-reparador-de-pontas-dellara-30ml |
| 27 | A | Lunnaè Cosméticos | 63.586.252/0001-64 | Demais | Vila Velha/ES | 3 (07-08→07-08) | https://lunnaecosmeticos.com.br/ | https://lunnaecosmeticos.com.br/products/kit-summer-shampoo-condicionador-lunnae |
| 28 | B | MeiQ | 40.956.550/0001-01 | EPP | Curitiba/PR | 3 (07-18→09-11) | https://meiq.com/ | UNVERIFIED |
| 29 | B | La Vertuan | 81.362.295/0001-48 | EPP | Araquari/SC | 10 (07-06→08-07) | https://loja.lavertuan.com.br/ | https://loja.lavertuan.com.br/creme-rejuvenescedor-pdrn-cellfie-revolution-40g-la-vertuan |
| 30 | B | Sorali Cosmetics | 18.474.047/0001-52 | Demais | São Vicente/SP | 5 (07-13→07-30) | https://www.sorali.com.br/ | https://www.sorali.com.br/tratamento/golden-oil-60ml-serum-capilar-nutricao-profunda-com-oleos-de-argan-e-jojoba-sorali |
| 31 | B | Nardo Puro | 63.199.570/0001-72 | ME | Piracicaba/SP | 3 (08-26→08-26) | https://www.nardopuro.com.br/ | https://www.nardopuro.com.br/hidratantes/hidratante-corporal-brand-collection-100-dream-savage-200ml |
| 32 | B | Black Fix | 11.951.228/0001-83 | EPP | Boituva/SP | 8 (08-04→09-04) | https://www.blackfix.com.br/ | https://www.blackfix.com.br/essencia-natural/essencia-natural-shampoo-babosa-e-quiabo |
| 33 | B | White Bull Cosméticos | 36.705.063/0001-90 | ME | Mogi das Cruzes/SP | 4 (09-23→09-23) | https://www.whitebull.com.br/ | https://www.whitebull.com.br/barba/balm/beard-balm-white-bull-120g |
| 34 | B | Linda de Bonita | 28.716.486/0001-88 | ME | São Paulo/SP | 5 (06-30→07-02) | https://www.lindadebonita.com.br/ | https://www.lindadebonita.com.br/body-cream/body-cream-funny |
| 35 | B | Fox for Men | 17.073.188/0001-09 | EPP | Guarulhos/SP | 3 (09-10→09-10) | https://foxformen.com.br/ | https://foxformen.com.br/produto/serum-para-pelos-encravados-30-ml-08-unidades/ |
| 36 | B | Rigolim Hair & Co | 35.819.653/0001-81 | ME | Maringá/PR | 3 (07-21→07-21) | https://www.rigolim.com.br/ | https://www.rigolim.com.br/oleos/oleo-para-cabelo-clean-oil-rigolim-hair-co |
| 37 | B | Iozzy | 25.117.396/0001-82 | ME | Londrina/PR | 6 (08-06→09-09) | https://iozzy.com.br/ | https://iozzy.com.br/produto/mascara-bb-cream-iozzy-500ml/ |
| 38 | B | Sidarta Cosméticos | 40.384.402/0001-51 | ME | Duque de Caxias/RJ | 4 (06-30→06-30) | https://sidarta.com/ | https://sidartacosmeticos.com.br/produtos/tonico/ |
| 39 | B | Amira Glow | 60.597.154/0001-34 | ME | Ribeirão das Neves/MG | 5 (08-05→09-11) | https://www.amiraglow.com.br/ | https://www.amiraglow.com.br/products/mousse-de-limpeza-facial-100ml |
| 40 | B | Novalski | 20.696.058/0001-29 | ME | Rio de Janeiro/RJ | 29 (07-07→09-23) | https://novalski.com.br/ | https://novalski.com.br/p/manteiga-geleia-corporal-300g-musk-vanilly/ |
| 41 | B | Odália Cosméticos | 61.166.718/0001-47 | ME | Viradouro/SP | 16 (07-22→09-22) | https://www.odalia.com.br/ | UNVERIFIED |
| 42 | B | Ziv Professional | 46.347.642/0001-62 | ME | Cedral/SP | 18 (07-16→09-09) |  | UNVERIFIED |
| 43 | B | Toda Maravilhosa | 29.223.262/0001-05 | ME | Pindorama/SP | 11 (06-29→09-09) |  | UNVERIFIED |
| 44 | B | Lelook's | 30.972.048/0001-22 | ME | Santana de Parnaíba/SP | 15 (08-11→08-28) |  | UNVERIFIED |
| 45 | B | Bunny | 17.233.009/0001-45 | ME | São Paulo/SP | 13 (09-08→09-22) |  | UNVERIFIED |
| 46 | B | Kice Professional | 38.134.158/0001-27 | ME | Marília/SP | 20 (06-29→09-22) |  | UNVERIFIED |
| 47 | B | Rhuja | 41.184.544/0001-38 | ME | Pradópolis/SP | 3 (08-03→08-04) | https://rhuja.com.br/ | https://rhuja.com.br/products/condicionador-rhuja |
| 48 | B | Kaeni Cosmetic | 37.790.493/0001-10 | ME | Praia Grande/SP | 5 (07-07→07-21) | https://www.kaeni.com.br/ | UNVERIFIED |
| 49 | B | Brilhus | 34.375.297/0001-91 | ME | Echaporã/SP | 3 (08-20→08-20) | https://brilhuscosmetics.com.br/ | UNVERIFIED |
| 50 | B | Falconi Cosméticos | 22.764.249/0001-06 | ME | Itaquaquecetuba/SP | 4 (07-01→07-01) | https://falconicosmeticos.com.br/ | UNVERIFIED |
| 51 | B | Maycrene | 24.836.346/0001-92 | ME | Franco da Rocha/SP | 7 (07-01→09-02) | https://maycrene.com.br/ | UNVERIFIED |
| 52 | B | Kaffiore | UNVERIFIED |  | / | 7 (09-04→09-21) | https://kaffiore.com.br/ | UNVERIFIED |
| 53 | B | Rebka Beauty | UNVERIFIED |  | / | 4 (07-08→07-08) | https://www.rebka.com.br/ | UNVERIFIED |
| 54 | B | A'Vezza | UNVERIFIED |  | / | 4 (09-14→09-14) | https://useavezza.com.br/ | UNVERIFIED |
| 55 | B | Dionna | UNVERIFIED |  | / | 3 (08-19→08-19) | https://dionna.com.br/password/ | UNVERIFIED |
| 56 | B | LEF Cosmetics | 09.354.422/0001-30 | ME | Rio Verde/GO | 3 (09-08→09-08) | https://lefcosmetics.com.br/password/ | UNVERIFIED |
| 57 | B | Trihair | 03.967.708/0001-04 | EPP | Salvador/BA | 5 (07-15→08-18) | https://www.trihair.com.br/ | https://www.trihair.com.br/products/mel-cola-trihair-500g |
| 58 | B | Hoka Professional | 11.914.198/0001-35 | EPP | Marechal Floriano/ES | 6 (07-16→09-03) | https://hoka.com.br/ | UNVERIFIED |
| 59 | B | NG de France | 14.546.684/0001-36 | ME | Osório/RS | 5 (07-29→09-03) | https://www.ngdefrance.com.br/ | UNVERIFIED |
| 60 | B | Flora Pura | 57.378.617/0001-62 | ME | Iguatu/CE | 5 (07-09→08-21) | https://www.florapura.com.br/ | UNVERIFIED |

The full per-row fields are in the CSV:
- ANVISA holder(s) and whether the holder is the owner;
- new-SKU sample with dates and category mix;
- capital social, opening date, CNAE;
- packshot product name and image URL;
- AI- or WhatsApp-named image files found on the site;
- a one-line reason for the grade.

Every one of the 40 carries a reason. Examples:
- Venexia: *"New company (CNPJ opened 30 Mar 2026), store opens 1 Nov 2026…"*
- Klass Vough: *"brush brand filing its first skincare line"*
- Melibliss: *"4 premium skin SKUs filed 20–21 Sep 2026 — a brand launch this month"*

## 3. Findings the list turned up (with sources)

**3.1 The ANVISA holder is usually not the company Sol calls.**
- For 23 of the 40 (57%), the notification is held by a contract maker, and the owner was found only from the site footer or contact page. This matches the ~55% in the brief.
- Footer quotes (fetched pages):
  - klassvough.com: *"Klassvough Design Acessorios Para Beleza LTDA - CNPJ: 02.881.499/0001-19"*
  - barrus.com.br: *"Copyright Barrus /Fran Barros LTDA - 38004418000140 - 2026"*
  - treeliss.com.br: *"Copyright Treeliss Profissional (Alfa JF Comércio de Cosméticos Ltda) - 30024139000136 - 2026"*
  - loja.invogacosmeticos.com.br: *"Copyright AVANTE DISTRIBUIDORA DE COSMETICOS E PERFUMARIA LTDA - 46883458000137 - 2026"*
  - isabellelabelleoficial.com.br: *"São Paulo/SP - CEP 03647-000 - CNPJ: 59.793.113/0001-34"*
  - bauny.com.br: *"FFE DISTRIBUIDORA LTDA - 40.867.166/0001-24"*
  - allevabeauty.com.br/contato: *"Dados da Empresa AB COSMETICOS E ACESSORIOS LTDA CNPJ: 60.249.460/0001-80"*
  - dimmpcosmeticos.com.br/contato: *"GUIMACOR INDUSTRIA E COMERCIO DE COSMÉTICOS LTDA CNPJ: 43.287.807/0001-60"*
  - zurielcosmetics.com.br/contato: *"COURA & COURA DISTRIBUIDORA COSMETICOS LTDA CNPJ: 13.823.813/0001-23"*
  - silentritual.com.br (password page): *"Copyright Silent.Ritual - 58114672000108 - 2026"*
- In several cases (Treeliss, Voga, Isabelle, Dellara, Bauny) the site operator is a distributor company. It is the brand's commercial arm, the maker is a third party, and the caller should ask for the brand owner.

**3.2 The hottest prospects have the least public material.**
- Venexia (venexia.com.br): *"Abrimos em 1º de novembro de 2026 : deixe seu e-mail e avisamos no dia"* and *"Uma empresa de venda direta com foco nas pessoas"* (a direct-sales model).
- Silent.Ritual: *"Estamos reformando a loja e está ficando incrível. Volte em alguns dias!"*
- Kalenza: site title *"Kalenza Cosmetics · Em construção"*. Also pre-launch: Thereza Glow (*"Nosso novo site está em construção"*), Dionna and LEF (password pages), and Melibliss and AquaOzon (filed 15–21 Sep).
- **Nine of the 40 have no public packshot URL that could be captured** (pre-launch, or a JS-rendered site): Venexia, Valenzza, Melibliss, AquaOzon, Silent.Ritual, Kalenza and MeiQ, plus Prohall and Iozzy, where the product page exists but has no image tag.

**3.3 About a fifth of the prospects already make their images with general AI chat tools.**
- On the 119 prospect sites whose image files could be listed (Shopify `products.json`, the WooCommerce Store API, or home-page HTML), 23 host product or banner images with ChatGPT- or Gemini-generated file names, all dated 2026.
- Matched Brazilian brands: Alleva, Amira Glow, AroomHealth, Ayllume, Bealess, Bioma Care, Brscience, Cosmobeauty, Dagua, Decreína, Elefthéria, Hello, Hidrabene, Isabelle la Belle, Linda de Bonita, Lunnaè, Muriel, Novalski, Sidarta, Trihair, Welty and Zanphy. JBeauty was a mismatched French site and is not counted. One ATL hit was a false positive and was removed.
- A further 13 have "WhatsApp Image" file names; about 10 remain once mismatched sites are removed.
- Examples:
  - `…/ChatGPT_Image_19_de_ago._de_2026_15_46_19_5.png` (zanphy, Shopify CDN)
  - `…/gemini_generated_image_qppkck…webp` (Isabelle la Belle)
  - `…/chatgpt-image-9-de-set-de-2026-17_44_19…webp` (Elefthéria)
  - Novalski's WooCommerce product feed: most images are `ChatGPT-Image-…png`
- This is a **lower bound**, since it only counts file names.
- Three of these images were viewed. They are finished lifestyle or promo scenes with the brand's own packaging. **Whether they contain label errors was not measured.**
- **In the call list: 10 of the 40 host ChatGPT- or Gemini-named images and 6 host WhatsApp-named images (13 distinct brands).**

**3.4 The CNPJ-record e-mail is often not the company's.**
- The following were dropped: accountants' addresses (e.g. `[e-mail omitido]` for Venexia, `[e-mail omitido]` for Alleva) and personal mailboxes (per the brief, kept to company-level data).
- CNPJ-record e-mails were kept only when the address is role-based on a company domain, or named after the company.
- CNPJ phones are shown as registered. Some are pre-2016 8-digit mobiles that need a leading 9. Some may ring the accountant: Alleva's registered phone has a 19 area code while the company is in São Paulo capital.

**3.5 Rails that failed (this limits the method, not the list).**
- Instagram cannot be read without a login.
- Bing ignored the query text.
- DuckDuckGo returned a 202 challenge; Brave returned 429.
- Mercado Livre search redirected to `account-verification`.
- The WebSearch tool returned US results only and found none of the brands.
- Websites were therefore found by domain guessing plus a content check: 155 of 520 brands (30%).

## 4. Design changes

1. **Start with the pre-launch cluster and the SP A-grades (ranks 1–18).** Their filings are 0–90 days old. H6A measured a median of ≈79 days from notification to shelf (18 pairs), so most are still before their launch.
2. **Make the PRÉVIA work without a public packshot.** For the 9 without one, offer *"PRÉVIA com o frasco neutro nas cores da marca"*: a blank placeholder bottle in the world, with the packshot composited only after the brand sends approved art. Or ask for one approved packshot on the call. This fits "fidelity by construction" and the *"Sua arte não entra em nenhuma IA"* promise.
3. **Change the opener for brands already making AI images.** For the 10 call-list brands with ChatGPT- or Gemini-named images, the competitor is free do-it-yourself, not an agency. Lead with the label-exact guarantee and the film and campaign set, not with "AI images". A free *Relatório de Fidelidade* on one image they have already published could open the call. **Whether their current images have label errors is UNVERIFIED** and must be checked image by image before it is claimed.
4. **Ask "quem é o dono da marca?" first.** For 23 of the 40 the ANVISA holder is a contract maker, and several site operators are distributor companies.
5. **Contact order:** the WhatsApp number on the site, then the SAC or contato e-mail on the site, then the CNPJ phone. Do not use CNPJ-record e-mails from free-mail or accountant domains.
6. **Refresh the list monthly with the same pipeline** (`load.py`, `classify6.py`, `brand7.py`, `brand8.py`, `agg.py`, `score.py`, `prio.py`, `disc4.py`, `pack4.py`, `build.py`). The ANVISA file updates daily. publica.cnpj.ws allows about 3 lookups a minute, so allow ~20 minutes per 60 owners.

## 5. Residual risks

- The brand parse is automatic: 16% of rows are unparsed and some keys are imperfect. All 60 listed brands were checked by hand against their SKU names and sites.
- The re-filing filter catches renamed re-filings only when names overlap by ≥75%. Some "new" SKUs may still be reformulations.
- Porte comes from the CNPJ record and can be stale; capital social ranges from R$1.000 to R$1,08M among the 40.
- "Owner" for distributor-operated stores is the commercial company on the site, which may differ from the brand's legal owner.
- AquaOzon, MeiQ, Valenzza, Melibliss and Kalenza: the site was matched on title only. Melibliss's site later timed out.
- Not SP (16/40): the brief prefers SP but does not exclude other states.
