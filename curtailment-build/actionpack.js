const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, BorderStyle, AlignmentType, LevelFormat, PageBreak,
        ShadingType } = require('../curtailment/node_modules/docx');
const fs = require('fs');

const NAVY = '1F3864', RULE = 'BFBFBF', GREY = '595959', RED = 'C00000', BOXBG = 'EEF3FA', W = 9360;

const PR = (runs, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, before: o.before ?? 0, line: 276 },
  alignment: o.align, indent: o.indent, numbering: o.numbering,
  children: runs.map(r => new TextRun({
    text: r.text, bold: r.bold, italics: r.italics,
    size: r.size ?? o.size ?? 21, color: r.color ?? o.color ?? '000000', font: 'Calibri'
  }))
});
const H1 = t => new Paragraph({
  spacing: { before: 320, after: 140 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 4 } },
  children: [new TextRun({ text: t, bold: true, size: 26, color: NAVY, font: 'Calibri' })]
});
const H2 = t => new Paragraph({
  spacing: { before: 200, after: 90 },
  children: [new TextRun({ text: t, bold: true, size: 22, color: NAVY, font: 'Calibri' })]
});
const N = t => PR([{ text: t }], { numbering: { reference: 'steps', level: 0 } });
const B = t => PR([{ text: t }], { numbering: { reference: 'bullets', level: 0 } });

const callout = (title, body, colour = NAVY) => new Table({
  columnWidths: [W], width: { size: W, type: WidthType.DXA },
  borders: {
    top: { style: BorderStyle.SINGLE, size: 4, color: colour }, left: { style: BorderStyle.SINGLE, size: 18, color: colour },
    bottom: { style: BorderStyle.SINGLE, size: 4, color: colour }, right: { style: BorderStyle.SINGLE, size: 4, color: colour },
    insideHorizontal: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, insideVertical: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }
  },
  rows: [new TableRow({ children: [new TableCell({
    shading: { type: ShadingType.CLEAR, fill: BOXBG, color: 'auto' },
    margins: { top: 140, bottom: 140, left: 200, right: 160 },
    children: [PR([{ text: title, bold: true, size: 22, color: colour }], { after: 80 }),
      ...body.map((t, i) => PR([{ text: t }], { after: i === body.length - 1 ? 0 : 100 }))]
  })] })]
});
const cell = (t, o = {}) => new TableCell({
  shading: o.head ? { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' } : undefined,
  margins: { top: 70, bottom: 70, left: 100, right: 100 },
  children: [PR([{ text: t, bold: o.head || o.bold, color: o.head ? 'FFFFFF' : (o.color ?? '000000'), size: o.size ?? 19 }], { after: 0, align: o.align })]
});
const table = (cols, rows) => new Table({
  columnWidths: cols, width: { size: cols.reduce((a, b) => a + b, 0), type: WidthType.DXA },
  borders: { top: { style: BorderStyle.SINGLE, size: 2, color: RULE }, bottom: { style: BorderStyle.SINGLE, size: 2, color: RULE },
    left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: RULE }, insideVertical: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' } },
  rows: rows.map(r => new TableRow({ children: r }))
});

const c = [];

c.push(PR([{ text: 'SUTPHIN — INTERNAL / FOR COUNSEL', bold: true, size: 18, color: GREY }], { after: 40 }));
c.push(PR([{ text: 'Curtailment Desk — Action Pack', bold: true, size: 40, color: NAVY }], { after: 40 }));
c.push(PR([{ text: 'Two documents in one: what to send counsel this week, and what to say on the first call.', size: 22, color: GREY }], { after: 60 }));
c.push(PR([{ text: '26 July 2026', size: 19, color: RED, italics: true }], { after: 260 }));

// ============================================================ PART 1: LEGAL BRIEF
c.push(H1('Part 1 — Brief for outside counsel'));
c.push(PR([{ text: 'Send this page as-is. It scopes one narrow, answerable question — not a general assignability opinion, which would take months because the Portaria itself is silent.' }]));

c.push(callout('THE QUESTION', [
  'We intend to advance cash to a wind or solar generator secured by a cessão fiduciária over its own compensation claim under Portaria Normativa MME 140/2026, plus a conta vinculada in the generator’s own name and CNPJ, plus an irrevocable sweep mandate. CCEE continues to pay the generator exactly as it does today — we are not asking CCEE to recognise us as payee.',
  'Lei 11.101/2005, art. 49 §3, makes cessão fiduciária extraconcursal — it survives the generator’s recuperação judicial. That protection is reported as contested when the secured creditor is not a financial institution (STJ REsp 1.833.824/RS).',
  'THE QUESTION: does that extraconcursal protection hold for Sutphin lending directly, as a non-financial creditor? If not, what is the minimum structure that restores it — a licensed financial institution as titular secured party with Sutphin behind it economically, insurance, a different security instrument, or something else?'
]));

c.push(H2('What we need back'));
c.push(N('A yes / no / conditional answer to the question above, with the condition stated plainly if conditional.'));
c.push(N('If a financial institution needs to sit in front of us: which types qualify, and roughly what that costs in structure and time.'));
c.push(N('Confirmation that a conta vinculada in the generator’s own CNPJ, blocked at the account bank, satisfies CCEE’s existing requirement that settlement accounts carry the same titularity as the market agent — we believe it does, since nothing about account ownership changes, but want it confirmed rather than assumed.'));
c.push(N('Any reason the specific obligor here — a título executivo extrajudicial against the União, operationalised through CCEE recontabilização — changes the analysis versus a standard commercial receivable.'));

c.push(H2('What we do not need'));
c.push(B('A general opinion on whether the Portaria 140 credit is assignable. It is silent on assignment — neither permitted nor prohibited — and that will not be resolved by legal analysis alone. We are structuring around it, not waiting for it.'));
c.push(B('Anything on CCEE recognising a third-party payee. We are not asking for that.'));

c.push(H2('Timeline and budget'));
c.push(PR([{ text: 'One week. A few thousand reais. This is a scoping question, not a full transactional opinion — the full documentation work happens once we have a real book to lend against.' }]));

c.push(new Paragraph({ children: [new PageBreak()] }));

// ============================================================ PART 2: CALL BRIEF
c.push(H1('Part 2 — First call brief'));
c.push(PR([{ text: 'Use this for the first call — Ibitu Energia (Tupi) is the strongest opening because they have already told the market their own number.' }]));

c.push(callout('WHY IBITU FIRST', [
  'Ibitu’s audited FY2025 accounts state 441,837 MWh cut, R$120.6m of impact, and that Lei 15.269/2025 “abre caminho para o ressarcimento de aproximadamente R$54,7 milhões.”',
  'Tupi — the debenture vehicle Ibitu sponsors — was downgraded by Fitch to AA-(bra), Negative Outlook, on 26 Jan 2026, citing a minimum debt service coverage ratio of 1.03x and an inability to distribute below 1.25x.',
  'Fitch’s own rating case assumes ZERO compensation. Every real Ibitu actually collects is upside the rating does not currently credit — which is exactly the argument for why they should want liquidity now rather than wait eighteen months.'
]));

c.push(H2('The opening line'));
c.push(PR([{ text: '“You’ve already told the market you expect about R$55m under Lei 15.269. We can advance against that today — secured by a blocked account in your own name, not by asking CCEE to do anything differently. You keep dealing with CCEE exactly as you do now; we just take security over the account it pays into.”', italics: true }]));

c.push(H2('The four questions'));
c.push(N('What share of your R$120.6m of curtailment sat outside your CCEAR-D and CER contracts? That uncommitted share, plus your Proinfa position if any, is the only part we can lend against — the rest is a book-entry reduction of what you owe CCEE, not cash.'));
c.push(N('Have you signed, or filed, the manifestação prévia de interesse yet? The 10 August deadline is cheap optionality — filing does not waive anything — so if not, that is step one regardless of anything else.'));
c.push(N('What do you currently owe CCEE under CCEAR-D and CER delivery-shortfall ressarcimentos? We need the net position, not the gross claim.'));
c.push(N('Would your existing lenders consent to a security interest over a segregated account holding this specific receivable? If Tupi’s debenture documents already restrict new liens, that is the first document we need to see.'));

c.push(H2('What we offer, and on what terms'));
c.push(table([2900, 6460], [
  [cell('Term', { head: true }), cell('Position', { head: true })],
  [cell('Structure'), cell('Secured advance against the uncommitted-volume PLD claim, via cessão fiduciária plus a blocked conta vinculada in Ibitu’s own CNPJ. Not a purchase of the receivable — CCEE keeps paying Ibitu exactly as today.')],
  [cell('What we advance against'), cell('Only the Verified Net Cash Receivable — the uncommitted/Proinfa tranche, IPCA-adjusted. Never the CCEAR-D/CER debt-relief tranche.')],
  [cell('Timing'), cell('Real capital deploys once the Termo is signed and volumes are confirmed by CCEE — realistically mid-to-late 2027. Before that, we can lock exclusivity with a conditional commitment at no cost to Ibitu.')],
  [cell('Pricing'), cell('Not fixed yet — deliberately. We price off Selic plus a spread for the real risks (compliance under the Termo, timing, tenor), once we have Ibitu’s actual contract book. Anyone quoting a fixed discount today is guessing.')],
  [cell('What we are not asking for'), cell('We are not asking CCEE to recognise us, and we are not asking Ibitu to change how it deals with CCEE. The security sits on top of the existing relationship.')]
]));

c.push(H2('What not to say'));
c.push(B('Do not quote a purchase price. We do not have one until we see their book.'));
c.push(B('Do not say the credit is assignable in the abstract — say precisely what we are doing: security over their own account, not a sale requiring CCEE’s cooperation.'));
c.push(B('Do not promise a timeline shorter than the statutory one. Signature realistically lands mid-2027; say so.'));

const doc = new Document({
  numbering: { config: [
    { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360, hanging: 220 } } } }] },
    { reference: 'steps', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] }
  ]},
  sections: [{ properties: { page: { margin: { top: 1000, bottom: 1000, left: 1080, right: 1080 } } }, children: c }]
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('Sutphin_Curtailment_Action_Pack.docx', b);
  console.log('wrote Sutphin_Curtailment_Action_Pack.docx', b.length, 'bytes');
});
