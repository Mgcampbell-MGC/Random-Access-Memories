# SH2 — SHIFT MÃOS source log (25 Sep 2026)

One line per source: what it said. Local copies are in `work/sh2/` (and `work/sh2/f/`).

## Supply (contract manufacturers)
- https://vnz.ind.br/termos-terceirizacao/ — Veneza terms.
  - TERC: "Mínimo de 24 unidades por produto" plus "Pedido mínimo de R$ 5.000,00 em produtos".
  - PROJ TERC: from 240 units per product and R$10.000. PROJ CLI: R$20.000.
  - Label: "o custo do rótulo não está incluso".
  - Freight is FOB. ICMS-ST: "aproximadamente 12% do valor da NF, quando aplicável".
  - ANVISA: "Taxa por produto: R$ 437,50 por item … pago uma única vez". "Produtos de Grau 2 podem demandar exigências adicionais".
  - Lead time: "até 30 dias corridos após aprovação dos rótulos".
  - Volume classes: 24 units −7%, 48 −14%, 72 −21%, 96 −28%, 120 −35%.
- https://amostra.vnz.ind.br/produto/74705/ — "TERC – SPAPE – CREME MAOS E UNHAS RETINOL 30ML", R$9,79 (sample shop).
- https://amostra.vnz.ind.br/produto/2200/ — "TERC – SPAPE – CREME MAOS LUVAS DE SILICONE 30G", R$8,32. The description reads "Creme para Mãos e Unhas Vitturia", so Veneza also has its own brand.
- https://amostra.vnz.ind.br/produto/2210/ — "LUVAS DE SILICONE", R$8,07 (Vitturia own brand).
- https://amostra.vnz.ind.br/produto/60300/ — "TERC – PUMP – CREAM POLPA HIDRATANTE 150G", R$24,53.
- https://amostra.vnz.ind.br/?s=hidratante&post_type=product — "TERC – SPAPE – CREME HIDRATANTE PES 60G" R$21,23; body lotions 200 mL R$21,60–22,34. Searches for "neutro" returned 0 products.
- https://www.dermavita.com.br/terceirizacao/ — "pedido mínimo de 300 unidades por tipo de produto, todos regularizados pela Anvisa com validade de 3 anos". Payment: "Entrada de 30% … + Custo Notificação Anvisa à vista".
- https://novafigus.com.br/white-label/ — "a partir de 300 unidades por produto"; "300 unidades, a depender da embalagem". Label creation is included. "regulamentados pela ANVISA, seja em registro ou notificação".
- https://www.formulaart.com.br/ — "Sem limite mínimo para produção"; "projeto inicial à partir de R$ 5.000,00". "A única taxa cobrada é a da notificação do produto junto a ANVISA". "Registro na ANVISA (com sua marca própria)".
- https://www.larimarcosmeticos.com.br/produtos/creme-hidratante-para-as-maos-70g — "Creme Hidratante para as Mãos com Amêndoas e Karité 70g", SKU 70141, "Preço R$ 0,00" (not published). The INCI includes Paraffinum Liquidum, Dimethicone, Urea and Parfum.
- https://www.larimarcosmeticos.com.br/category/cremes-de-proteção-epi — the factory also runs a "Cremes de Proteção EPI" category ("Creme Protetor da Pele Isoluv 2 Óleo Resistente – 200g").
- https://www.confortocosmeticos.com.br/ — HTTP 500. "No mínimo 500 unidades" comes from a search snippet only: UNVERIFIED.
- https://www.jhscosmeticos.com.br/ — 403. https://multlabel.com.br/cosmeticos — TLS certificate expired, so not fetched.
- https://www.casadacosmetologia.com.br/terceiriza-beauty — ABC matches brands with terceiristas: "Tampouco somos comissionados para realizar tal atividade"; associated terceiristas participate "sem custo adicional". This is the free referral front door.
- https://privatecosmeticos.com.br/blog/quanto-custa-criar-marca-de-cosmeticos and https://www.florus.com.br/blog/quanto-custa-ter-a-minha-propria-marca-de-cosmeticos/ — no unit prices published; "cada projeto é um projeto".
- `work/TA_CONSULTA_COSMETICOS.CSV` (ANVISA open data, H6A copy; notification date = vencimento − 10 y). 12 months to 24 Sep 2026:
  - 791 hand-moisturiser notifications from 242 holders, 38–87 a month.
  - 15 are under Veneza's CNPJ carrying client brands (ID da Beleza, Angels Beauty, Cadoro, Teodoro Beauty and Tiarga & Inoue, all "creme para mãos retinol / nano retinol"; Ceci Lavi ×3; Plenna; BCharme; Santo Expedito; Adriana Morel; The Sirius; Ozone Quantic; Bellano).
  - ≥8 "luvas de silicone" brands. 1 "PROFISSIONAL" (Chico Beauty, mãos e pés). 0 names target the professional's own hands.

## Shelf (observed via each retailer's public VTEX catalogue API, `/api/catalog_system/pub/products/search?ft=…`)
- www.epocacosmeticos.com.br, www.drogariasaopaulo.com.br, www.paguemenos.com.br (drugstore and cosmetics), plus www.ikesaki.com.br, www.coprobel.com.br and www.iapcosmeticos.com.br (beauty-supply / manicure stores).
  - 238 distinct hand-care listings from 84 brands. Median R$32,90; median R$59 per 100 g/mL (p25 38,5, p75 111).
  - Product-level URLs are in SH2.json `shelf_br`.
- Key observations:
  - Monange 75 g R$14,19. Carmed 40 g R$13,64. Nivea 75 g R$25,99.
  - Avon Luvas de Silicone 75 g R$17,99. Sensi Luva de Silicone 40 g R$19,90.
  - Granado 50 mL R$22,95–41,00. L'Occitane au Brésil 30 mL R$29,99–45,90.
  - Neutrogena Norwegian 56 g R$46,90–68,19. La Roche-Posay Xerand 50 mL R$35,90. Isdin Ureadin Manos 51,5 g R$74,99. CeraVe 100 g R$124,90. Mavala 50 mL R$134,90–174,90.
  - Manicure channel: Repós 120 g R$22,90, Repós 500 g R$39,90, D'agua 680 g R$56,99, Corpo Dourado 300 g R$14,99, Bio Soft Lisa Mão 120 g R$12,99–19,90, Ricca 50 g R$18,90.
- https://www.dermage.com.br/api/catalog_system/pub/products/search?ft=creme%20maos — Dermage Compose creme para mãos R$89,90 (size not in the payload).
- https://bycorpus.com.br/enfermeiro-na-linha-de-frente-hidrate-suas-maos/ — a small brand (owner is an estomaterapeuta) with a pocket hand cream "pensada para profissionais de saúde", declared "Grau 2". It quotes Darlenski & Tsankov 2020: "only 22% are applying skin protective cream" (secondary).
- UNREADABLE:
  - lista.mercadolivre.com.br: account-verification redirect. api.mercadolibre.com: 403.
  - amazon.com.br: 503. shopee.com.br API: 403. magazineluiza.com.br: 403.
  - natura.com.br: 403. granado.com.br: 403. belezanaweb, sephora and drogaraia VTEX: 403.
  - Tray-hosted micro-brand stores (sigbeauty, bittescosmeticos, vinilady): 403.
  - Review counts: NOT measured.

## Buyer, channel and population
- https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATBHE/estatisticasSinac.app/EstatisticasOptantesPorCNAE.aspx?tipoConsulta=2&optanteSimei=&anoConsulta=2026 — SIMEI optants by CNAE, "Posição Consolidada até 19/09/2026". ASP.NET postback per UF, all 27 summed:
  - 9602-5/01: 1.074.566 in Brazil (SP 307.435).
  - 9602-5/02: 353.921 (SP 102.050).
  - 4772-5/00: 210.165 (SP 49.784).
  - All SIMEI: 17.564.107.
  - Per-UF table in `work/sh2/simei_by_uf.json`.
- https://servicodados.ibge.gov.br/api/v3/agregados/6450/periodos/2021/variaveis/706|707|708?localidades=N1[all]|N3[35]&classificacao=12762[117885,117472] — CEMPRE 2021 (excludes MEI):
  - 96.02-5: 41.148 units, 123.861 people, 73.811 salaried in Brazil; SP 13.447 / 41.037 / 25.417.
  - 47.72-5: 37.074 units in Brazil, 11.710 in SP.
- https://servicodados.ibge.gov.br/api/v3/agregados/10645/periodos/2024/variaveis/502|503|1400?localidades=N1[all]&classificacao=11070[83324,83351] — PAC 2024:
  - Retail group 47.7: net resale revenue R$311,58 bn, margin R$124,07 bn, taxa de margem 66,2% (≈39,8% of revenue).
  - Wholesale 4644+4645+4646: R$371,04 bn, R$119,35 bn, 47,4% (≈32,2% of revenue).
- https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/lei/l13352.htm — Lei 13.352 (salão-parceiro).
  - §4: "A cota-parte retida pelo salão-parceiro ocorrerá a título de atividade de aluguel de bens móveis e de utensílios … e/ou … serviços de gestão, de apoio administrativo".
  - §10 IV: the contract must state "direitos do profissional-parceiro quanto ao uso de bens materiais".
  - Nothing obliges the salon to supply personal skin care.
- http://www3.mte.gov.br/sistemas/mediador/imagemAnexo/MR070412_20212022_01_10T22_06_33.pdf — the MTE-registered partnership contract model returned 503, so it was not read.
- https://www.es.senac.br/admin/data/dynamic/cursos/22/downloads/86ad2080962c0e207f97f26c02c70c55.pdf — SENAC-ES manicure material list includes "1 Hidratante para mãos e pés" (for practice). https://www.sp.senac.br/documents/20125/45326/Curso+23556+2020-01-01-v7.1-9222 and …Curso+14179+2016-01-01 — the SENAC-SP lists have no hand cream.
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35038179 — Havmose 2022 meta-analysis: hand eczema in hairdressers is 38,2% lifetime, 20,3% one-year and 7,7% point prevalence; incidence 51,8 per 1.000 person-years.
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=36698444 — La Roche-Posay survey of 391 hairdressers: dryness is the most intense issue; 28% discontinued work. The authors are brand employees.
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=1806320 — Long & Finlay 1991: "hand 1.2 FTU".
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=1497374 — Long, Finlay & Averill 1992: "The rule of hand: 4 hand areas = 2 FTU = 1 g" (title only).

## Regulation
- https://anvisalegis.datalegis.net/…numeroAto=00000907…valorAno=2024 — RDC 907/2024 (as amended by RDC 949/2024), Anexo I.
  - Grau 1 item 42: "Preparações cosméticas para umectação, hidratação e/ou refrescância do rosto, mãos, pés".
  - Grau 2 triggers, item 1: (b) "pele acneica ou sensível", (g) "antibacteriano ou antisséptico", (h) "fotoprotetora", (k) "como equipamento de proteção individual (EPI) para o trabalho".
  - Grau 2 list: item 22 antibacterial hand preparations; 23 EPI preparations; 33 sensitive skin.
  - Art. 37: titulares must hold an AFE "para fabricar". Art. 13 II f–h: the label shows the titular's AFE, CNPJ and razão social.
- https://anvisalegis.datalegis.net/…numeroAto=00000894…valorAno=2024 — RDC 894/2024.
  - Art. 1: good cosmetovigilance practices "para as empresas titulares da regularização".
  - Art. 46: execution may be outsourced, but "§ 1º O responsável pela Cosmetovigilância e seu substituto não podem ser terceirizados".
- https://anvisalegis.datalegis.net/…numeroAto=00000016…valorAno=2014 — RDC 16/2014.
  - Art. 2 VI: "distribuidor ou comércio atacadista … realizadas entre pessoas jurídicas ou a profissionais para o exercício de suas atividades".
  - Art. 3: AFE is required for "distribuição".
  - Art. 5 III: exemption for "comércio varejista de cosméticos".
  - Art. 15 I c: an inspection report is required.
  - Art. 28 I e: "comprovação do registro de responsabilidade técnica … junto ao respectivo conselho de classe".
- https://www.gov.br/pt-br/servicos/solicitar-autorizacao-de-funcionamento-2013-cosmeticos — AFE "É obrigatória para empresas que desejam realizar … Distribuir". The Vigilância Sanitária Local issues the inspection report. TFVS "variável de acordo com o porte" (amount UNVERIFIED).
- https://www.gov.br/trabalho-e-emprego/…/normas-regulamentadoras/nr-06.pdf — NR-6:
  - 6.2: EPI "só poderá ser posto à venda ou utilizado com a indicação do Certificado de Aprovação - CA".
  - Anexo I F.2: "creme protetor de segurança para proteção dos membros superiores contra agentes químicos".
  - The PDF's version date is UNVERIFIED.
- https://legislacao.fazenda.sp.gov.br/Paginas/Portaria-CAT-68-de-2019.aspx — "ANEXO XI (Revogado, a partir de 1º de abril de 2026, pela Portaria SRE-94/25…) PRODUTOS DE PERFUMARIA E DE HIGIENE PESSOAL (artigo 313-E do RICMS)".
- https://legislacao.fazenda.sp.gov.br/Paginas/RC18477_2018.aspx — RICMS/SP art. 55 IV: 25% on "perfumes e cosméticos classificados nas posições 3303, 3304, 3305 e 3307" (2018 ruling; current validity assumed, UNVERIFIED).

## Arithmetic
All arithmetic is in `work/sh2/calc.py` (output in the JSON). PTAX 5,20. Net bar R$10.400–12.950/month.
