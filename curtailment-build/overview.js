const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, BorderStyle, AlignmentType, LevelFormat, PageBreak,
        HeadingLevel, ShadingType } = require('../curtailment/node_modules/docx');
const fs = require('fs');

const NAVY = '1F3864', RULE = 'BFBFBF', GREY = '595959', RED = 'C00000',
      BOXBG = 'EEF3FA', AMBER = '7F6000', W = 9360;

const PR = (runs, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, before: o.before ?? 0, line: 276 },
  alignment: o.align, indent: o.indent, numbering: o.numbering,
  children: runs.map(r => new TextRun({
    text: r.text, bold: r.bold, italics: r.italics, break: r.break,
    size: r.size ?? o.size ?? 21, color: r.color ?? o.color ?? '000000', font: 'Calibri'
  }))
});

const H1 = t => new Paragraph({
  spacing: { before: 320, after: 140 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 4 } },
  children: [new TextRun({ text: t, bold: true, size: 26, color: NAVY, font: 'Calibri' })]
});
const H2 = t => new Paragraph({
  spacing: { before: 220, after: 90 },
  children: [new TextRun({ text: t, bold: true, size: 22, color: NAVY, font: 'Calibri' })]
});
const B = t => PR([{ text: t }], { numbering: { reference: 'bullets', level: 0 } });
const N = t => PR([{ text: t }], { numbering: { reference: 'steps', level: 0 } });

const callout = (title, body, colour = NAVY) => new Table({
  columnWidths: [W], width: { size: W, type: WidthType.DXA },
  borders: {
    top:    { style: BorderStyle.SINGLE, size: 4,  color: colour },
    left:   { style: BorderStyle.SINGLE, size: 18, color: colour },
    bottom: { style: BorderStyle.SINGLE, size: 4,  color: colour },
    right:  { style: BorderStyle.SINGLE, size: 4,  color: colour },
    insideHorizontal: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    insideVertical:   { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }
  },
  rows: [new TableRow({ children: [new TableCell({
    shading: { type: ShadingType.CLEAR, fill: BOXBG, color: 'auto' },
    margins: { top: 140, bottom: 140, left: 200, right: 160 },
    children: [
      PR([{ text: title, bold: true, size: 22, color: colour }], { after: 80 }),
      ...body.map((t, i) => PR([{ text: t }], { after: i === body.length - 1 ? 0 : 100 }))
    ]
  })] })]
});

const cell = (t, o = {}) => new TableCell({
  shading: o.head ? { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' } : undefined,
  margins: { top: 70, bottom: 70, left: 100, right: 100 },
  children: [PR([{ text: t, bold: o.head || o.bold, color: o.head ? 'FFFFFF' : (o.color ?? '000000'),
                   size: o.size ?? 19 }], { after: 0, align: o.align })]
});
const table = (cols, rows) => new Table({
  columnWidths: cols, width: { size: cols.reduce((a, b) => a + b, 0), type: WidthType.DXA },
  borders: {
    top:    { style: BorderStyle.SINGLE, size: 2, color: RULE },
    bottom: { style: BorderStyle.SINGLE, size: 2, color: RULE },
    left:   { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    right:  { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: RULE },
    insideVertical:   { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }
  },
  rows: rows.map(r => new TableRow({ children: r }))
});

const c = [];

// ---------------------------------------------------------------- COVER
c.push(PR([{ text: 'SUTPHIN — INTERNAL', bold: true, size: 18, color: GREY }], { after: 40 }));
c.push(PR([{ text: 'The Curtailment Desk', bold: true, size: 44, color: NAVY }], { after: 40 }));
c.push(PR([{ text: 'Portaria Normativa MME nº 140/2026 — business overview, version 2',
             size: 24, color: GREY }], { after: 60 }));
c.push(PR([{ text: '26 July 2026  ·  supersedes version 1 in two material respects', size: 19, color: RED, italics: true }],
          { after: 260 }));

c.push(callout('WHAT CHANGED SINCE VERSION 1', [
  'Version 1 said payment lands in H2 2027. It does not. The Portaria fixes no calendar date — it fixes a chain of relative deadlines, and running them out gives late 2027 as the base case and H1 2028 on the outer limits.',
  'Version 1 treated 10 August as the decision point. It is not. Filing the manifestação does not waive anything; the irrevocable waiver happens at signature, which cannot occur before mid-2027. This is the single most important thing in this document and almost the entire market has it wrong.',
  'Both corrections make the opportunity better, not worse — because they turn a two-week scramble into a ten-month advisory position with a defined capital event at the end of it.'
], RED));

c.push(H1('1.  The one-paragraph version'));
c.push(PR([{ text: 'Brazil wasted 20.6 per cent of everything its wind and solar farms could have generated in 2025 — the grid could not take it. On 21 July the federal government published the rulebook for compensating part of that loss. Generators must register by 10 August, then wait until mid-2027 to sign a settlement and until late 2027 or 2028 to be paid. Most of them misunderstand what they are signing, none of them can verify the classification that decides how much they get, and the ones who most need the money are project-finance vehicles that cannot survive the wait. We have already rebuilt the eligible claim for every wind and solar complex in the country from raw grid data. Nobody else has. That is the business.' }]));

c.push(H1('2.  What actually happened'));
c.push(PR([{ text: 'When the transmission network cannot absorb what a wind or solar farm is producing, the system operator orders it to stop. The generator loses the revenue and is not automatically paid for it. This is ' }, { text: 'constrained-off', italics: true }, { text: ', or curtailment, and in Brazil it has gone from a rounding error to a crisis in four years.' }]));
c.push(table([2600, 2200, 2200, 2360], [
  [cell('Year', { head: true }), cell('Curtailed', { head: true, align: AlignmentType.RIGHT }),
   cell('Share of available output', { head: true, align: AlignmentType.RIGHT }), cell('Lost revenue', { head: true, align: AlignmentType.RIGHT })],
  [cell('2022'), cell('—', { align: AlignmentType.RIGHT }), cell('0.5%', { align: AlignmentType.RIGHT }), cell('—', { align: AlignmentType.RIGHT })],
  [cell('2023'), cell('3,150 GWh', { align: AlignmentType.RIGHT }), cell('3.6%', { align: AlignmentType.RIGHT }), cell('—', { align: AlignmentType.RIGHT })],
  [cell('2024'), cell('12,336 GWh', { align: AlignmentType.RIGHT }), cell('9.3%', { align: AlignmentType.RIGHT }), cell('R$1.6bn', { align: AlignmentType.RIGHT })],
  [cell('2025', { bold: true }), cell('36,168 GWh', { bold: true, align: AlignmentType.RIGHT }), cell('20.6%', { bold: true, align: AlignmentType.RIGHT }), cell('R$6.5bn', { bold: true, align: AlignmentType.RIGHT })],
  [cell('2026 to 25 July'), cell('17,362 GWh', { align: AlignmentType.RIGHT }), cell('18.8%', { align: AlignmentType.RIGHT }), cell('—', { align: AlignmentType.RIGHT })]
]));
c.push(PR([{ text: 'Volumes computed directly from ONS half-hourly open data. Revenue figures are Volt Robotics, the only continuous published series. 84 per cent of it lands in the Northeast; Rio Grande do Norte alone is 44 per cent of the eligible claim.', size: 18, color: GREY, italics: true }], { before: 80, after: 160 }));

c.push(PR([{ text: 'In November 2025 Congress passed a law creating a right to compensation for part of the historic losses. On 18 July 2026, published 21 July, the Ministry of Mines and Energy issued Portaria Normativa 140 — the rulebook. It is five days old.' }]));

c.push(H2('What it pays for, and what it does not'));
c.push(PR([{ text: 'The grid operator codes every curtailed hour into one of three categories. Only two of them are paid.' }]));
c.push(table([3400, 1500, 4460], [
  [cell('Reason for the cut', { head: true }), cell('Share', { head: true, align: AlignmentType.RIGHT }), cell('Compensated?', { head: true })],
  [cell('Indisponibilidade externa — a fault on the transmission network'), cell('13%', { align: AlignmentType.RIGHT }), cell('Yes, in full', { bold: true })],
  [cell('Confiabilidade elétrica — grid stability limits'), cell('41%', { align: AlignmentType.RIGHT }), cell('Yes, in full', { bold: true })],
  [cell('Sobreoferta — there was simply too much power and nowhere to put it'), cell('46%', { align: AlignmentType.RIGHT }), cell('No. Nothing.', { bold: true, color: RED })]
]));
c.push(PR([{ text: 'Classification split for 1 September 2023 to 25 November 2025, from ANEEL’s own voto in Processo 48500.000231/2026-56. In the first half of 2026 the non-compensable share had risen to roughly 65 per cent.', size: 18, color: GREY, italics: true }], { before: 80 }));

c.push(new Paragraph({ children: [new PageBreak()] }));

// ---------------------------------------------------------------- THE MISREADING
c.push(H1('3.  The misreading the whole market is making'));
c.push(PR([{ text: 'Every law firm alert, every press piece and every conversation we have seen treats 10 August 2026 as the moment a generator gives up its legal claims in exchange for compensation. That is wrong, and the error is worth a great deal of money.' }]));
c.push(PR([{ text: 'There are two separate decisions, roughly ten months apart.' }]));

c.push(callout('DECISION ONE — 10 AUGUST 2026 — COSTS ALMOST NOTHING', [
  'File a manifestação prévia de interesse with the Ministry through the CELEBRA portal. That is all.',
  'It waives nothing. ABSOLAR has stated publicly that filing does not oblige anyone to drop a lawsuit. The waiver lives in the Termo de Compromisso, which is a separate later act.',
  'It buys two things. First, optionality — you cannot join later. Second, and more valuable in the short term: under Article 6 §3, once you have filed, CCEE’s collection of the delivery-shortfall amounts you already owe stays suspended throughout the process. For a generator short of cash that relief is worth more today than the compensation itself.',
  'Conclusion: almost every eligible generator should file. This is not a hard call and we should not pretend it is.'
]));

c.push(callout('DECISION TWO — MID-2027 — IS IRREVERSIBLE', [
  'Sign the Termo de Compromisso. It is expressly irrevogável e irretratável, sem quaisquer condicionantes.',
  'Signing waives, for good, the right to litigate any curtailment event through 25 November 2025 — administratively, in arbitration, or in court. It requires you to discontinue pending suits, to have yourself struck individually from the roll of claimants in the collective action, and to surrender the protective effect of any injunction you currently hold.',
  'The convocação to sign cannot legally issue until the grid operator finishes its final database, which the statutory clock puts around late April 2027. By then CCEE has published your actual volumes — so unlike August, this decision is taken with numbers in hand.',
  'Everything of value happens between the two dates.'
], AMBER));

c.push(H2('Why the gap is the business'));
c.push(PR([{ text: 'Between August 2026 and mid-2027 four things have to be worked out, none of which a generator can do alone, and none of which is being sold today.' }]));

c.push(H1('4.  The four things worth money'));

c.push(H2('4.1  The classification is a black box — and it decides everything'));
c.push(PR([{ text: 'Whether a given hour is coded confiabilidade elétrica or sobreoferta is the difference between being paid in full and being paid nothing. The methodology is not published in a reproducible form.' }]));
c.push(B('Volt Robotics tested the Ministry’s own SOSIN formula against the grid operator’s calculation and found it produced 143 per cent more sobreoferta.'));
c.push(B('The share of cuts coded non-compensable rose from 27 per cent in 2023 to 65.5 per cent in the first half of 2026. Either the physics changed dramatically, or the coding did.'));
c.push(B('Volt’s chief executive, publicly: it is not enough to say a cut was energético — the data, assumptions and criteria must be published so the conclusion can be reproduced and audited.'));
c.push(B('There is a formal contestation window — ten days after the grid operator’s consistency analysis, around March 2027 — and after that the generator accepts the classification irretratavelmente under Cláusula Quarta.'));
c.push(PR([{ text: 'So there is a defined, dated, adversarial window in which a well-evidenced challenge converts directly into cash, and essentially nobody is preparing for it. On a R$200m claim, moving five percentage points of volume from sobreoferta to confiabilidade is worth roughly R$10m to the client.', bold: true }], { before: 100 }));
c.push(PR([{ text: 'One limit to be honest about. Article 5º’s procedure for updating anemometric and solarimetric reference data covers events only to 10 February 2025, while the compensated window runs to 25 November 2025. So for the last nine months of the window we work from the existing reference data rather than rebuilding it. That constrains the reference-data half of the exercise. It does not constrain the classification challenge, which is a separate mechanism and is where the value is.', italics: true, size: 20 }], { before: 60 }));

c.push(H2('4.2  Nobody knows which PLD applies'));
c.push(PR([{ text: 'Uncommitted volume is compensated at the spot price — the PLD — of the plant’s submarket. The Termo never says whether that means the PLD at the time of the cut or at the date of payment. Lefosse has flagged the ambiguity; nobody has resolved it.' }]));
c.push(PR([{ text: 'This is not a technicality. Northeast PLD sat at its regulatory floor of about R$58/MWh through most of early 2025 and averaged R$227/MWh across 2026. On a large book the answer is worth nine figures, and it should be settled before signature rather than after.' }]));

c.push(H2('4.3  Signing converts a suspended liability into an enforceable one'));
c.push(PR([{ text: 'This is the point that gets missed, and it is the most dangerous one in the instrument.' }]));
c.push(PR([{ text: 'Under Cláusula Oitava, on signing the generator authorises CCEE to resume billing and collecting the delivery-shortfall amounts it owes under its regulated contracts, and undertakes not to oppose provisional court orders against the Union or CCEE. Under Cláusula Sétima it simultaneously surrenders the protective effect of any injunction it currently holds.' }]));
c.push(PR([{ text: 'For a generator whose court order is the only thing keeping a nine-figure liability off its balance sheet, signing means accepting an enforceable debt today against a credit that pays in late 2027. Worse, under Subcláusula Oitava, if it then fails to prove it filed the required court petition within ten days, the compensation is suspended while every other obligation survives — including the resumed billing. It is possible to end up having waived, being billed, and not being paid.', bold: true }]));

c.push(H2('4.4  The veto is still alive, and signing surrenders it for nothing'));
c.push(PR([{ text: 'When the law was sanctioned in November 2025, the government vetoed a much broader provision — article 1º-A — which would have compensated all externally caused curtailment except sobreoferta, retroactively. Congress removed the override from its agenda on 18 June 2026 and has still not voted it. As of today the veto is neither maintained nor overridden.' }]));
c.push(PR([{ text: 'The Termo’s waiver is bounded by the date of the event, not by which law creates the right. A generator that signs and then watches Congress override the veto has given away the enlarged claim for free. That is a genuine option with genuine value, and it is not being priced by anyone.' }]));

c.push(H2('4.5  One thing on the other side of the ledger — Article 10 helps'));
c.push(PR([{ text: 'Article 10 and Cláusula Sexta provide that curtailed volumes count as generation verificada for the annual garantia física revision — expressly “passíveis ou não de compensação”.' }]));
c.push(PR([{ text: 'This is a benefit, not a cost. Counting curtailed output as generated is what prevents a plant’s physical guarantee — and therefore the volume it is allowed to contract in future — being revised down for energy it was ordered not to produce. It applies to sobreoferta cuts as well, which means it is the one place the uncompensated volume still earns the generator something.' }]));
c.push(PR([{ text: 'MME has not published the methodology, so it cannot yet be quantified. Model it as an option with a favourable direction, and put it on the positive side of the decision:' }]));
c.push(PR([{ text: 'avoided reduction in contractable MWh  ×  expected future margin  ×  duration  ×  methodology probability', bold: true, color: NAVY }], { align: AlignmentType.CENTER, before: 60, after: 60 }));

c.push(new Paragraph({ children: [new PageBreak()] }));

// ---------------------------------------------------------------- THE EDGE
c.push(H1('5.  What we already have that nobody else does'));
c.push(PR([{ text: 'The grid operator publishes constrained-off data per plant, every half hour, going back to October 2021 — and separately publishes the reason code for each restriction. Nobody has joined the two and rebuilt the claim.' }]));
c.push(PR([{ text: 'We have. Working from the raw ONS series, ANEEL’s generation register and the plant-level identifiers, we have computed the eligible claim — indisponibilidade externa plus confiabilidade elétrica only, over exactly the compensated window — for every complex in the country:' }]));
c.push(B('267 complexes, 25,326 GWh of eligible curtailment, reconciled to the grid operator’s own published percentages within 0.2 points.'));
c.push(B('Ownership joined through ANEEL’s register at a 98.9 per cent match rate, rolled up to corporate groups covering 73 per cent of the pool.'));
c.push(B('The excluded sobreoferta volume — 23,213 GWh, the part they are being asked to waive and will never be paid for — quantified alongside it, complex by complex.'));
c.push(PR([{ text: 'That means the first call is not a pitch. It is: here is your own number, computed from public data, before you have told us anything. That is a very different conversation, and it is why the door opens.', bold: true }], { before: 100 }));

c.push(H2('Where the claim sits'));
c.push(table([3300, 1700, 1700, 2660], [
  [cell('Group', { head: true }), cell('Eligible GWh', { head: true, align: AlignmentType.RIGHT }),
   cell('Est. claim', { head: true, align: AlignmentType.RIGHT }), cell('Read', { head: true })],
  [cell('Casa dos Ventos'), cell('4,754', { align: AlignmentType.RIGHT }), cell('R$619m', { align: AlignmentType.RIGHT }), cell('Largest holder. Raised US$1.1bn in June — does not need capital.')],
  [cell('Engie Brasil'), cell('1,776', { align: AlignmentType.RIGHT }), cell('R$231m', { align: AlignmentType.RIGHT }), cell('Discloses percentages, never an R$ figure.')],
  [cell('Enel Green Power'), cell('1,616', { align: AlignmentType.RIGHT }), cell('R$211m', { align: AlignmentType.RIGHT }), cell('Decision may sit in Rome.')],
  [cell('Echoenergia / Equatorial'), cell('1,092', { align: AlignmentType.RIGHT }), cell('R$142m', { align: AlignmentType.RIGHT }), cell('Already litigating — two of the twelve suits.')],
  [cell('Serena'), cell('1,057', { align: AlignmentType.RIGHT }), cell('R$138m', { align: AlignmentType.RIGHT }), cell('Highest proportional EBITDA hit of any rated name.')],
  [cell('Voltalia'), cell('920', { align: AlignmentType.RIGHT }), cell('R$120m', { align: AlignmentType.RIGHT }), cell('Only company to have booked real money — R$175m in Q2 2026.')],
  [cell('Elera / Brookfield'), cell('419', { align: AlignmentType.RIGHT }), cell('R$54m', { align: AlignmentType.RIGHT }), cell('Already litigating. Complexo Alex hit 67.7% in July 2024.')]
]));
c.push(PR([{ text: 'Full ranking of all 267 complexes, with ownership confidence flags, is in the accompanying workbook. Claim estimates apply the R$130/MWh implied by the reported pool; they are modelled, not disclosed.', size: 18, color: GREY, italics: true }], { before: 80 }));

c.push(H1('6.  Being honest about the money'));
c.push(PR([{ text: 'Three things make this smaller than the headline suggests, and they belong at the front of any internal discussion rather than buried.' }]));
c.push(N('It is mostly a book entry, not a cheque. The compensation first treats curtailed output as if it had been delivered under the generator’s regulated contracts, cancelling a debt rather than paying money. Only volume not committed to those contracts is paid in cash. Sector-wide, roughly R$3.3bn of credit nets against roughly R$6bn generators already owe CCEE — so as a sector they remain net owing even after full compensation.'));
c.push(N('Nobody outside can tell which generators get cash. The contract position of each plant sits in CCEE data behind a login. This is the single most commercially decisive variable and it is unobtainable from outside — which is precisely why it is the first question on every call, and why the call has to happen.'));
c.push(N('The litigation being waived is weak. Twelve suits, none with a surviving injunction. The one appellate win, in December 2024, was suspended by the Superior Court of Justice six weeks later and never implemented. So for most generators the honest advice is that the waiver is cheap — which is useful, correct, and not what a vendor would tell them.'));

c.push(H2('What the business could earn'));
c.push(PR([{ text: 'Two revenue lines with different timing. These are estimates built on stated assumptions, not forecasts.' }]));
c.push(table([2700, 2100, 2100, 2460], [
  [cell('Line', { head: true }), cell('When', { head: true }), cell('Range', { head: true }), cell('What has to be true', { head: true })],
  [cell('Advisory — classification audit, two-sided waiver analysis, contestation support'),
   cell('Aug 2026 – mid 2027'), cell('R$5–15m'),
   cell('8–15 mandates at R$300k–1.5m. Requires we win the first five on the strength of the data.')],
  [cell('Success fee on reclassified volume'), cell('Mar–Jun 2027'), cell('R$3–12m'),
   cell('10–20% of value created. Requires the contestation window to work as drafted and our analysis to hold.')],
  [cell('Capital — financing the net cash tranche'), cell('From mid-2027'), cell('CANNOT YET BE SIZED', { bold: true, color: RED }),
   cell('Deliberately left blank. See below — the denominator is not the pool, it is the sum of positive net cash after the full waterfall, and nobody has measured it.')]
]));
c.push(PR([{ text: 'An earlier draft of this document put R$20–60m of gross spread on the capital line. That figure is withdrawn. It was built by applying a discount to gross compensation, and gross compensation is not what anyone receives.' , bold: true }], { before: 100 }));

c.push(H2('Why the capital line cannot honestly be sized yet'));
c.push(PR([{ text: 'A generator’s position after the full waterfall can be positive cash, pure debt relief, or — and this is the case nobody has modelled — net negative. Consider a generator owing R$80m of suspended delivery-shortfall ressarcimentos with a R$50m settlement benefit. It signs, loses the injunction that was holding the liability off its books, and CCEE resumes collection. It receives no cheque. It gets R$50m of liability relief and owes R$30m. That is a real and common shape, and it is invisible from outside.' }]));
c.push(PR([{ text: 'So the addressable capital market is not the pool. It is:' }]));
c.push(PR([{ text: 'sum of positive net cash after the waterfall  ×  clean title  ×  enforceable payment control  ×  willingness to monetise  ×  our credit box', bold: true, color: NAVY }], { align: AlignmentType.CENTER, before: 60, after: 60 }));
c.push(PR([{ text: 'None of those five factors is known today. They become knowable from a sample of five real books — one CCEAR-D/CER-heavy, one merchant/ACL-heavy, one hybrid, one Proinfa, one judicially protected. Getting those five books is the actual objective of the next fortnight.' }]));

c.push(H2('The segmentation that follows from it'));
c.push(table([2400, 3400, 3560], [
  [cell('Segment', { head: true }), cell('Test', { head: true }), cell('What we sell them', { head: true })],
  [cell('Cash-rich', { bold: true }), cell('Over ~60% of the benefit converts to cash — merchant, ACL, Proinfa or large contractual residual'), cell('Recovery mandate plus financing')],
  [cell('Mixed'), cell('20–60% converts'), cell('Recovery mandate; finance only the cash tranche')],
  [cell('Debt-relief dominant'), cell('Under 20% converts; value is CCEE liability reduction'), cell('Advisory and success fee. Do not buy anything.')],
  [cell('Net payer', { bold: true, color: RED }), cell('Liability survives the settlement and the injunction is surrendered'), cell('Sign / do-not-sign advice only. This is the highest-value advice we give and the worst financing target.')],
  [cell('Encumbered'), cell('Existing lender lien, RJ restrictions, disputed title'), cell('Advisory until resolved')]
]));
c.push(PR([{ text: 'Note what this does to the call order: cashability comes before distress. A distressed CCEAR-D generator with no cash tranche is a good advisory mandate and a terrible loan. A solvent merchant generator with R$30m of expected PLD cash is the better transaction even though it has no liquidity problem at all.' }], { before: 100 }));

c.push(H2('The unlock — we do not need CCEE to pay us'));
c.push(PR([{ text: 'Every version of this idea so far, including our own earlier draft, asked the wrong question: can CCEE be made to recognise Sutphin as payee and redirect the compensation to us? That is genuinely unresolved and may stay unresolved for months — CCEE’s adapted rules are not final until September 2026, and the payment is a netting entry inside the generator’s own settlement account (Art. 6º §§3–5), not a discrete invoice that a lockbox simply intercepts.' }]));
c.push(PR([{ text: 'CCEE never has to pay us. It pays the generator, into the generator’s own account, same CNPJ, exactly as today. What we take is a security interest ' }, { text: 'over that account', bold: true }, { text: ' — not a redirection of the payment itself. This is a secured advance, not a receivables purchase requiring CCEE’s cooperation, and it is built from three instruments this desk already knows how to use:' }]));
c.push(N('A cessão fiduciária of the specific Termo receivable — Lei 4.728/1965 art. 66-B — perfected by registration and notice to CCEE and MME.'));
c.push(N('A conta vinculada in the generator’s own name and CNPJ, held at a bank that agrees to block it — which is exactly what satisfies CCEE’s same-CNPJ rule, because nothing about the account holder changes.'));
c.push(N('An irrevocable mandate letting us sweep the account the moment CCEE settles into it.'));
c.push(PR([{ text: 'The asset we advance against still has a precise name — the ' }, { text: 'Verified Net Cash Receivable', bold: true }, { text: ': the uncommitted volume valued at PLD, plus Proinfa, IPCA-adjusted, after prior payments and deductions. We never lend against the CCEAR-D/CER tranche, because that tranche is debt relief with no cash behind it to secure.' }]));

c.push(H2('The one open question, and it is narrow'));
c.push(PR([{ text: 'Cessão fiduciária is extraconcursal — it survives even if the generator enters recuperação judicial during the eighteen-month wait, under Lei 11.101/2005 art. 49 §3. But that protection is contested when the secured creditor is not a financial institution (STJ REsp 1.833.824/RS). That is the actual question, and it is narrow: does our protection hold if we lend directly, or do we need a bank as the formal secured party with us participating behind it economically?' }]));
c.push(PR([{ text: 'One lawyer, one week. If the answer is yes, we lend directly. If it is uncertain, we put a licensed institution in front of us — which costs a spread, not the deal. Either way it is answerable now, on a real question, rather than the open-ended “is this assignable” that stalled the last two drafts.', bold: true }]));
c.push(PR([{ text: 'The generator’s own ongoing compliance under the Termo — filing the renunciation within ten days of signing, not opposing a provisional court order, curing any default within five days under Subcláusula Oitava — remains real underwriting risk. It does not change with the structure above; it is priced and monitored like any covenant, and it is precisely why we do not lend into a generator with live recuperação judicial exposure, such as Rio Alto.' }]));
c.push(PR([{ text: 'A third, smaller point: if the eventual vehicle is an FIDC, CVM Resolução 175 requires an eligible direito creditório, and whether a CCEE recontabilização credit against the União qualifies is not yet tested. It is the same open question we flagged months ago about royalty-backed structures in this market — a wrapper choice does not resolve it.' }], { before: 60 }));
c.push(PR([{ text: 'Neither gate is a reason to stand down. Both are reasons the capital line is a target we are staging toward, not a product we can price today. The rule stays: no verified net cash, no purchase. No enforceable payment control, no purchase. Advisory and the classification audit run regardless of how these resolve — that business costs us nothing we have not already spent, and it is what tells us, from five real books, whether the other two even matter at scale.', bold: true }], { before: 80 }));

c.push(new Paragraph({ children: [new PageBreak()] }));

// ---------------------------------------------------------------- WHO NEEDS IT
c.push(H1('7.  Where the capital is actually needed'));
c.push(PR([{ text: 'Not at the holding companies. Casa dos Ventos holds the largest claim in the country and raised US$1.1bn in a private placement in June 2026. Essentia is buying assets, not selling claims. The stress is one level down, in the project-finance vehicles.' }]));
c.push(B('Fitch placed 13 Brazilian renewable project financings on Rating Watch Negative in October 2025, explicitly on curtailment. Six were downgraded by May 2026 and eleven left on negative outlook, with pressure projected to persist to 2030.'));
c.push(B('Tupi Energias Renováveis — BRL 820m of debentures, sponsor Ibitu, contracted to Cemig — runs a minimum debt service cover of 1.03 times and cannot distribute below 1.25 times.'));
c.push(B('Engie’s São Pedro IV issue averages 0.75 times cover from 2026 to 2031.'));
c.push(B('BNDES opened case-by-case standstills for curtailment-hit projects in October 2025, with parallel discussions at BNB and Banco do Brasil. Atlas Renewable Energy suspended roughly 1.5 GW and US$1bn of Brazilian projects in June 2026, explicitly over curtailment.'));
c.push(PR([{ text: 'These vehicles cannot wait until 2028 and cannot pay a dividend in the meantime. They are structurally unable to solve this themselves, and they are exactly the size that neither the banks nor the large funds will trouble with. That is the lending population.', bold: true }], { before: 100 }));

c.push(callout('THE ONE ACUTE NAME — AND WHY IT IS NOT A LENDING OPPORTUNITY', [
  'Rio Alto Energias Renováveis: extrajudicial recovery extinguished without resolution in June 2026, BTG enforcing security over Santa Luzia 5, 7 and 9, a sale mandated to close by end-2026 with no buyer identified, negative net worth of R$905m, and Coremas averaging 52 per cent restricted.',
  'It holds a real claim and it cannot survive to collect it. Whatever the right answer is there, it is not a bridge loan — and we should be clear about that internally before anyone gets excited about the discount.'
], RED));

c.push(H1('8.  The first two weeks'));
c.push(PR([{ text: 'The objective is not capital and it is not ten calls. It is mandates and data — specifically five complete books that let us measure cash conversion for the first time.' }]));
c.push(N('Work the list properly. Forty to sixty corporate groups, not ten. The workbook ranks 40 named groups covering 73 per cent of the eligible pool, and every one of them gets their own number before we ask them for anything. Target twenty senior conversations and ten to fifteen signed mandates.'));
c.push(N('Sell option preservation, not analysis. A short engagement to confirm eligibility, get the CELEBRA filing right, check the correct titular, CNPJ, CEG and outorga, inventory the litigation and liens, and secure exclusivity on the decision work that follows. Price it at R$25–40k per group and credit it fully against the later mandate. Waive it for a multi-plant group that signs exclusivity on the spot. This is client acquisition, not the profit centre.'));
c.push(N('Get five books of five different shapes — one CCEAR-D/CER-heavy, one merchant/ACL-heavy, one hybrid, one Proinfa, one judicially protected. Those five are what turn the cash-conversion ratio from a guess into a number, and everything downstream depends on them.'));
c.push(N('One conversation with Volt Robotics. They own the classification data and the sector’s credibility on it; they do not have capital. That is complementary, and it is the single highest-value call on the list. Decide whether they are a partner or a competitor before someone else does.'));
c.push(N('One energy-regulatory counsel, one week, to answer two questions: which PLD applies to uncommitted volume, and what the assignability position is for a credit against the Union under a Termo that is silent on the point. Neither blocks anything; both need answering before capital moves.'));
c.push(N('Nothing is filed and nothing is bought. By 10 August we want five generators who have shared their contract position with us, because that is the variable nobody else can see.'));

c.push(H1('9.  What this is not'));
c.push(B('It is not the answer to the original mandate. It does not compound, it has a defined end, and the capital line does not open until mid-2027. It is a good campaign, not a business that runs itself.'));
c.push(B('It is not recurring. Sobreoferta causes the majority of curtailment and is excluded by statute, so nothing comparable is being created behind this one.'));
c.push(B('It is not a distressed-debt trade today. There is no Termo, no quantified amount and no enforceable title until mid-2027. Anything done before then finances an expectation, not a receivable.'));
c.push(B('It is not blue ocean forever. Only two law firms have published on the Portaria and nobody has filed for clarification — but that will not last, and the classification audit is replicable by anyone with the same data and the will to build it.'));

c.push(H1('10.  The thesis, as it should now be stated'));
c.push(callout('CANONICAL VERSION — use this wording with GC and with any capital partner', [
  'Sutphin will use the 10 August deadline to acquire exclusive recovery mandates, not to buy unverified claims. We preserve generators\u2019 eligibility, then build a plant-level model that separates CCEE liability relief, contractual residual payments, merchant and ACL volume valued at PLD, Proinfa cash, resumed reimbursement obligations, garantia f\u00edsica protection, and the probability-weighted value of the claims being surrendered.',
  'The product is a sign-or-do-not-sign decision and a recovery mandate. The operating company earns onboarding, success and uplift fees and never carries claim risk.',
  'A separate vehicle advances cash secured by a cessão fiduciária over the generator’s own blocked account — never by asking CCEE to redirect payment to us — against the Verified Net Cash Receivable, once a Termo is signed and the extraconcursalidade of that security for a non-financial creditor is confirmed by counsel. Gross compensation and accounting liability relief are never treated as purchasable face value, and CCEAR-D/CER debt relief is never lent against.',
  'Mandate first. Fees first. Structure the security now — it does not depend on CCEE. Confirm the one narrow legal point. Lend against real cash once a Termo exists.'
]));

c.push(H1('Appendix — sources and how far to trust them'));
c.push(table([2900, 6460], [
  [cell('Claim', { head: true }), cell('Basis', { head: true })],
  [cell('Everything about what the Portaria says'), cell('VERIFIED against the primary text in the DOU of 21 July 2026, article by article, including the annexed model Termo. Article references in this document are exact.')],
  [cell('Curtailment volumes and the eligible claim per complex'), cell('COMPUTED by us from ONS half-hourly open data. Method reconciles to ONS’s own published percentages within 0.2 points. Not a company disclosure.')],
  [cell('Ownership of each complex'), cell('JOINED through ANEEL SIGA at 98.9% CEG match. Corporate group attribution is partly inferred from naming conventions — confidence flags are in the workbook and should be respected.')],
  [cell('The R$3.3bn pool'), cell('PRESS ONLY. No primary document states any figure. MME says values are not yet defined. Independent estimates range R$2.7–3.5bn.')],
  [cell('The 46/41/13 classification split'), cell('ANEEL’s own voto, Processo 48500.000231/2026-56.')],
  [cell('Litigation census and the STJ suspension'), cell('MegaWhat survey of 31 Oct 2024 for the twelve suits. The STJ case number could not be verified in an accessible source and has deliberately not been stated.')],
  [cell('Company-level financial impact'), cell('Fitch via NeoFeed, and company releases where they exist. Auren and CPFL disclose R$ figures; Engie does not.')],
  [cell('Named individuals'), cell('Published quotes, filings and IR pages ONLY. No contact database was used — the Apollo account returned a billing error — and no email address has been constructed or guessed.')]
]));
c.push(PR([{ text: 'Accompanying workbook: Sutphin_Curtailment_Call_List.xlsx — call list, all 267 complexes, contacts, editable assumptions, full Portaria mechanics, call script and sources.', size: 19, color: GREY, italics: true }], { before: 160 }));

const doc = new Document({
  numbering: { config: [
    { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•',
      alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 220 } } } }] },
    { reference: 'steps', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.',
      alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] }
  ]},
  sections: [{ properties: { page: { margin: { top: 1000, bottom: 1000, left: 1080, right: 1080 } } }, children: c }]
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('Sutphin_Curtailment_Desk_Overview_v2.docx', b);
  console.log('wrote Sutphin_Curtailment_Desk_Overview_v2.docx', b.length, 'bytes');
});
