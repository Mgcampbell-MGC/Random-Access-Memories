# -*- coding: utf-8 -*-
"""Fitch Rating Watch Negative project financings x our eligible-claim data.
Fitch placed 13 Brazilian renewable project financings on RWN on 22 Oct 2025
explicitly on curtailment, downgraded 6 by May 2026 and left 11 on Negative
Outlook with pressure projected to 2030. CRITICALLY: Fitch's rating cases
ASSUME ZERO COMPENSATION."""

HEADLINE = [
 "Fitch, 19 May 2026 — Brazilian Renewable Projects to Face Persistent Curtailment Headwinds:",
 "Fitch assumes NO curtailment compensation in any of these rating cases, on the stated basis that "
 "'energetic-related curtailment does not qualify for compensation under existing regulatory rules.'",
 "That is the commercial opening. Every rand of compensation these vehicles actually collect is upside "
 "the rating does not currently give them credit for — and for a project running a 1.03x minimum DSCR, "
 "that is the difference between a downgrade and a stabilisation. It gives a project-finance CFO a reason "
 "to pay for this work that a healthy holdco does not have.",
 "The portfolio generated ~85% of projected levels in the 12 months to Aug 2025. Relief is not expected "
 "until the Graça Aranha transmission line around 2030.",
]

# (fitch_entity, our_complexes, uf, elig_gwh, rating_detail, sponsor, contact, why)
ROWS = [
 ("Serra do Mel Holding / Vila Piauí 1 e 2",
  "SERRA DO MEL A, B, II A, II B, C", "RN", 2981,
  "On Rating Watch Negative 22 Oct 2025. Vila Piauí 1 and Vila Piauí 2 are separately listed on the same watch.",
  "SPEs: Vila Piauí 1 e 2 Empreendimentos; Ventos de Vila Ceará I/II; Sol Serra do Mel I/II. Group attribution unconfirmed — verify before calling.",
  "Not established — this is the single largest gap in the research and the highest-value one to close.",
  "THE BIGGEST PRIZE ON THE SHEET. The largest eligible claim in the country sits inside project financings Fitch has on negative watch. R$388m of claim against vehicles whose ratings assume they collect nothing. Find the sponsor first."),
 ("Assuruá 4 e 5 Holding Energia",
  "LARANJEIRAS, SERRA DO ASSURUÁ, GENTIO DO OURO I", "BA", 788,
  "On Rating Watch Negative 22 Oct 2025.",
  "Assuruá 1/3/4/5 SPEs are Serena Energia. Serra do Assuruá (846 MW) is ENGIE and is a different complex — do not conflate. Laranjeiras carries CARGILL AGRÍCOLA as an equity holder (autoprodução).",
  "Serena: Andrea Sztajn, Diretora Financeira e de RI. Engie: Gabriel Mann dos Santos, Diretor de Regulação.",
  "Two different sponsors inside one Fitch line item. The Cargill autoprodução element matters: self-production volume is not committed to CCEAR-D/CER, so it falls into the PLD cash tranche."),
 ("Asa Branca Holding",
  "BRISA POTIGUAR I, ASA BRANCA", "RN", 322,
  "On Rating Watch Negative 22 Oct 2025.",
  "ESSENTIA ENERGIA (Pátria Investimentos). Asa Branca Holding S.A. (CNPJ 09.359.927/0001-97) is a CVM issuer alongside Essentia PCHs S.A.",
  "Gabriel Marinho de Farias — Diretor de Relações com Investidores, Essentia, AND VP Sênior de Infraestrutura at Pátria Investimentos. Elected 07/04/2025. Francisco Moya Reina is Diretor Presidente.",
  "BEST-QUALIFIED TARGET ON THE SHEET. A Fitch-watched project financing, a named IR director who also sits at the sponsor, and a CVM-registered issuer that must disclose. Essentia has no dedicated CFO or regulatory director — Farias is the whole finance function."),
 ("Tupi Energias Renováveis",
  "Not matched to a complex name in ONS data — Tupi is a holding over 13 wind SPEs", "—", 0,
  "DOWNGRADED AA(bra) to AA-(bra), Negative Outlook, 26 Jan 2026. BRL 820m in two series (BRL 580m to Oct 2034; BRL 240m to Oct 2036). Curtailment 210.4 GWh in 2025 = 28% of projected output. Fitch applies a 15% generation haircut to 2030. MIN DSCR 1.03x, AVG 1.20x 2026–2033 — 'weak'. Cannot distribute below 1.25x.",
  "Ibitu Energia, controlled by FIP Astra. CEO Paulo Abranches since Jun 2024.",
  "Paulo Abranches, CEO, Ibitu Energia.",
  "IBITU HAS ALREADY PUT A NUMBER ON THIS ITSELF. Its audited FY2025 accounts state 441,837 MWh cut, R$120.6m of impact, and that Lei 15.269/2025 'abre caminho para o ressarcimento de aproximadamente R$54,7 milhões'. They have done the work, they are covenant-compliant but cannot distribute, and they have quantified the claim. Start here."),
 ("Central Fotovoltaica São Pedro IV",
  "Not separately identified in the eligible-claim ranking", "—", 0,
  "DOWNGRADED AAA(bra) to AA(bra), Rating Watch Negative, 16 Oct 2025. BRL 95.5m debentures to 2034. Net generation 43.4 GWh in operating year 6 = ~55% OF P-50. Grid restricting output ~33% per year through 2030. MINIMUM DSCR 0.49x, average 1.08x 2025–2034. NEGATIVE OPERATING CASH FLOW.",
  "ENGIE Brasil Energia.",
  "Gabriel Mann dos Santos, Diretor de Regulação, Estratégia e Comunicação, Engie Brasil.",
  "THE MOST DISTRESSED SINGLE CREDIT DOCUMENTED. A 0.49x minimum DSCR and negative operating cash flow at a project owned by an investment-grade sponsor. Engie has never published an R$ curtailment figure. This is the clearest case anywhere of a vehicle that needs the compensation to work."),
 ("Complexo Morrinhos Energias Renováveis",
  "CAMPO FORMOSO (partial match — verify)", "BA", 101,
  "Watch REMOVED and AAA(bra) affirmed Stable, 16 Apr 2026 — but ONLY because of a 100% Santander Brasil bank guarantee plus >BRL 100m liquidity. Average DSCR is below 1.0x through 2027 on Fitch's own rating case. BRL 102.5m debentures to Dec 2027.",
  "CGN Brasil Energia (China General Nuclear).",
  "CGN Brasil statutory board: Mingzhu Li (Diretor Presidente), Wen Zhao (Diretor Financeiro). No regulatory director published.",
  "THE COUNTER-EXAMPLE, and instructive. Sub-1.0x coverage survives only because a bank stands behind it. Every project on this list without a guarantee is exposed. Useful to cite on other calls."),
 ("Ventos de São Clemente Holding",
  "SÃO CLEMENTE", "PE", 88,
  "On Rating Watch Negative 22 Oct 2025.",
  "Echoenergia (Equatorial Energia). SPEs: Ventos de São Clemente I–VII Energias Renováveis.",
  "Cristiano de Lima Logrado — Diretor de Regulação e Mercado, Equatorial (covers Echoenergia). Liu Aquino — Diretor-Presidente, Echoenergia.",
  "Echoenergia is already plaintiff in two of the twelve lawsuits, runs 51.4% solar curtailment, and Equatorial has said publicly it is evaluating divestments over a ~R$900m curtailment cost. Group-level claim across all Echoenergia complexes is 1,092 GWh."),
 ("Itarema Geração de Energia",
  "ITAREMA V", "CE", 95,
  "On Rating Watch Negative 22 Oct 2025.",
  "SPEs: Eólica Itarema II and V S.A. Group attribution unconfirmed.",
  "Not established.",
  "Small in isolation. Worth a call only once a route is known."),
 ("Pirapora II Solar Holding",
  "PIRAPORA 2", "MG", 87,
  "On Rating Watch Negative 22 Oct 2025. Was rated AAA(bra).",
  "Historically an EDF Renewables / Canadian Solar joint venture.",
  "EDF: Thaisa Alcoforado de Almeida is EDF Power Solutions' ABEEólica board representative.",
  "Minas Gerais solar. MG ran the highest state curtailment rate in the country in 2025 at 27.4% — worse than RN. Small claim but a live credit."),
 ("Ventos de São Tito Holding · Ventos de São Tomé Holding · Voltalia São Miguel do Gostoso",
  "No direct name match in the ONS complex list — these are holdcos over SPEs", "—", 0,
  "All three on Rating Watch Negative 22 Oct 2025.",
  "São Tito is associated with Casa dos Ventos / the Araripe complex. São Miguel do Gostoso is Voltalia.",
  "Voltalia: Nicolas Thouverez, Head of Latin America. Casa dos Ventos: Fernando Elias Domingos Sé, Diretor de Regulação e Comercialização.",
  "VOLTALIA IS THE ONE COMPANY THAT HAS ALREADY BOOKED REAL MONEY — R$175m of curtailment ressarcimento recognised in Q2 2026 results, and CEO Robert Klein confirmed in Sep 2025 they were already pursuing compensation for exactly this window. Call them to learn how it actually worked, not to sell."),
]

FOOTER = [
 ("Why this tab is the lending list",
  "These are the vehicles that cannot wait. A project financing with a 1.03x minimum DSCR cannot distribute, "
  "cannot refinance, and cannot absorb an eighteen-month delay — and unlike a holdco it has no other business "
  "to cross-subsidise it. Casa dos Ventos raised US$1.1bn in June 2026 and needs nothing from us. These do."),
 ("The verification that makes it credible",
  "This tab is built from two independent directions that agree: Fitch's published watch list, and our own "
  "eligible-claim computation from raw ONS half-hourly data. Neither knew about the other. 5,414 GWh of "
  "eligible claim — 21.4% of the national pool — sits inside financings Fitch has flagged."),
 ("The caveat on matching",
  "Fitch names holding companies; ONS names physical complexes. Several matches are by name similarity and "
  "are marked for verification. Tupi, São Tito, São Tomé and São Miguel do Gostoso could not be matched to a "
  "complex at all — the holdco names do not appear in ONS's registry. Confirm each one before using it."),
 ("What is missing and matters most",
  "The sponsor behind the Serra do Mel and Vila Piauí cluster. It is the largest eligible claim in Brazil, it "
  "is on Fitch's watch list, and we have not established who controls it. That single question is worth more "
  "than any other outstanding item in this workbook."),
 ("A single-source warning",
  "Every R$ curtailment loss figure in Brazil — R$6.5bn for 2025, R$1.6bn for 2024, the R$2.7bn compensable "
  "estimate — traces back to one consultancy, Volt Robotics. Valor, XP, BTG and the trade press all re-publish "
  "the same study. That is concentration risk in the market's own understanding, and it is also why Volt is "
  "either the most valuable partner available or the most dangerous competitor."),
]
