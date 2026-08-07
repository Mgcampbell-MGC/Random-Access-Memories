const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, WidthType, BorderStyle, ShadingType,
  LevelFormat, PageBreak, Header, Footer, PageNumber, TableOfContents,
} = require('docx');
const fs = require('fs');

const ACCENT = '1B4965';
const ACCENT_LIGHT = 'E4EEF4';
const GREY = '595959';
const RED = '9E2A2B';
const GREEN = '1E5631';
const AMBER = '8A6100';
const BODY = 21;
const FONT = 'Calibri';
const CW = 9026;

const P = (text, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, line: 276 },
  alignment: o.align,
  indent: o.indent,
  border: o.border,
  children: [new TextRun({ text, size: o.size ?? BODY, font: FONT, bold: o.bold, italics: o.italics, color: o.color ?? '000000' })],
});

const RICH = (runs, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, line: 276 },
  alignment: o.align,
  indent: o.indent,
  children: runs.map((r) => new TextRun({
    text: r.t, size: r.size ?? BODY, font: FONT, bold: r.b, italics: r.i, color: r.c ?? '000000',
  })),
});

const H1 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_1, spacing: { before: 340, after: 160 },
  children: [new TextRun({ text: t, size: 30, font: FONT, bold: true, color: ACCENT })],
});
const H2 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 110 },
  children: [new TextRun({ text: t, size: 24, font: FONT, bold: true, color: ACCENT })],
});
const BUL = (t, o = {}) => new Paragraph({
  numbering: { reference: 'bul', level: o.level ?? 0 },
  spacing: { after: 70, line: 276 },
  children: [new TextRun({ text: t, size: BODY, font: FONT, color: o.color ?? '000000', bold: o.bold })],
});
const NUM = (t, ref) => new Paragraph({
  numbering: { reference: ref, level: 0 },
  spacing: { after: 70, line: 276 },
  children: [new TextRun({ text: t, size: BODY, font: FONT })],
});

function cell(text, w, o = {}) {
  const runs = Array.isArray(text) ? text : [{ t: text }];
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
    margins: { top: 70, bottom: 70, left: 110, right: 110 },
    verticalAlign: 'center',
    children: [new Paragraph({
      spacing: { after: 0, line: 264 },
      alignment: o.align,
      children: runs.map((r) => new TextRun({
        text: r.t, size: o.size ?? 20, font: FONT,
        bold: o.bold || r.b, italics: r.i, color: r.c ?? (o.color ?? '000000'),
      })),
    })],
  });
}

function tbl(widths, rows, o = {}) {
  const scale = CW / widths.reduce((a, b) => a + b, 0);
  const w = widths.map((x) => Math.round(x * scale));
  const B = { style: BorderStyle.SINGLE, size: 3, color: 'BFBFBF' };
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: w,
    borders: { top: B, bottom: B, left: B, right: B, insideHorizontal: B, insideVertical: B },
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0 && o.header !== false,
      children: r.map((c, ci) => {
        const isH = ri === 0 && o.header !== false;
        const opts = typeof c === 'object' && !Array.isArray(c) && c.opts ? c.opts : {};
        const val = typeof c === 'object' && !Array.isArray(c) && c.opts ? c.v : c;
        return cell(val, w[ci], {
          fill: isH ? ACCENT : (opts.fill ?? (ri % 2 === 0 ? 'F7F9FB' : undefined)),
          color: isH ? 'FFFFFF' : opts.color,
          bold: isH || opts.bold,
          align: opts.align,
          size: opts.size,
        });
      }),
    })),
  });
}

const RULE = () => new Paragraph({
  spacing: { before: 60, after: 160 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACCENT } },
  children: [new TextRun({ text: '', size: 2 })],
});

const CALLOUT = (label, text, color) => new Table({
  width: { size: CW, type: WidthType.DXA },
  columnWidths: [CW],
  borders: {
    top: { style: BorderStyle.SINGLE, size: 3, color },
    bottom: { style: BorderStyle.SINGLE, size: 3, color },
    left: { style: BorderStyle.SINGLE, size: 18, color },
    right: { style: BorderStyle.SINGLE, size: 3, color },
  },
  rows: [new TableRow({
    children: [new TableCell({
      width: { size: CW, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: 'FAFAFA', color: 'auto' },
      margins: { top: 120, bottom: 120, left: 160, right: 140 },
      children: [
        new Paragraph({
          spacing: { after: 60 },
          children: [new TextRun({ text: label, size: 19, font: FONT, bold: true, color })],
        }),
        new Paragraph({
          spacing: { after: 0, line: 276 },
          children: [new TextRun({ text, size: BODY, font: FONT })],
        }),
      ],
    })],
  })],
});

const PB = () => new Paragraph({ children: [new PageBreak()] });

// ─────────────────────────────────────────────────────────── content

const doc = new Document({
  creator: 'Sol',
  title: 'ADV-Check — Business Overview',
  description: 'Pre-computed disclosure-mismatch reports for US investment advisers',
  numbering: {
    config: [
      { reference: 'bul', levels: [
        { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 200 } } } },
        { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 200 } } } },
      ] },
      { reference: 'pipe', levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 220 } } } },
      ] },
      { reference: 'test', levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 220 } } } },
      ] },
    ],
  },
  styles: {
    default: {
      document: { run: { font: FONT, size: BODY } },
    },
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1300, bottom: 1200, left: 1440, right: 1440 } } },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT, spacing: { after: 0 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' } },
        children: [new TextRun({ text: 'ADV-Check — Business Overview', size: 16, font: FONT, color: GREY })],
      })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: 'Every figure tagged VERIFIED carries a source fetched 6 Aug 2026  ·  ', size: 15, font: FONT, color: GREY }),
          new TextRun({ children: [PageNumber.CURRENT], size: 15, font: FONT, color: GREY }),
        ],
      })] }),
    },
    children: [
      // ── cover
      new Paragraph({ spacing: { before: 900, after: 60 }, children: [
        new TextRun({ text: 'ADV-CHECK', size: 68, font: FONT, bold: true, color: ACCENT }),
      ] }),
      new Paragraph({ spacing: { after: 40 }, children: [
        new TextRun({ text: 'Pre-computed disclosure-mismatch reports', size: 30, font: FONT, color: GREY }),
      ] }),
      new Paragraph({ spacing: { after: 420 }, children: [
        new TextRun({ text: 'for US registered investment advisers', size: 30, font: FONT, color: GREY }),
      ] }),
      RULE(),
      RICH([
        { t: 'The one-sentence version.  ', b: true },
        { t: 'Every US investment adviser files two public documents that are supposed to agree about the same facts, and they routinely do not — so Sol finds the contradiction from free public data before making contact, and sells each firm the finished report about itself.' },
      ], { after: 200 }),
      tbl([30, 70], [
        ['Field', 'Position'],
        ['Product', 'A pre-computed PDF report. The buyer installs nothing and needs no AI account.'],
        ['Buyer', 'Owner or Chief Compliance Officer at a small US investment advisory firm'],
        ['Price', 'US$650 — under genuine downward pressure; may settle at US$350–450'],
        ['Market size', { v: '16.779 registered advisers; 15.445 with a website; 14.557 US-based', opts: { b: true } }],
        ['Channel', 'Cold email only. Faceless. No calls, no camera, no personal brand.'],
        ['Capital at risk', 'Under US$220 before the first sale'],
        ['Status', { v: 'Data infrastructure VERIFIED end to end. Demand UNTESTED.', opts: { color: AMBER, b: true } }],
      ]),
      new Paragraph({ spacing: { before: 200 }, children: [
        new TextRun({ text: 'Version 1.0  ·  6 August 2026', size: 18, font: FONT, color: GREY }),
      ] }),
      PB(),

      // ── 1
      H1('1.  What the customer actually files'),
      P('In the United States, anyone who manages money professionally for other people must register with the Securities and Exchange Commission. There are 16.779 such firms. Most are small — a handful of people, one office, an owner who signs everything.'),
      P('Each of them files a document called Form ADV. It comes in two parts, and the whole business lives in the gap between them.'),
      tbl([18, 82], [
        ['Part', 'What it is'],
        [{ v: 'Part 1', opts: { b: true } }, 'A structured questionnaire — boxes and numbers. "How much money do you manage?" → $412,000,000. "How many clients?" → 340. Filed into a public database with 448 fields.'],
        [{ v: 'Part 2A', opts: { b: true } }, 'Called "the brochure." Thirty to sixty pages of plain prose that the firm must hand to every client. It describes the same facts: assets under management, fee schedules, conflicts of interest.'],
      ]),
      P('Both are public. Anyone can read either one.', { after: 200 }),

      H2('Why they disagree'),
      P('Part 1 is refreshed in the annual filing. The brochure is prose someone wrote two or three years ago, and rewriting prose is work nobody volunteers for. So the two drift apart:'),
      BUL('Part 1 reports US$412M under management. The brochure still says US$353M.'),
      BUL('Part 1 states fees reaching 1,5%. The brochure describes a maximum of 1,25%.'),
      BUL('Part 1 ticks a box disclosing a conflict of interest. The brochure never mentions it.'),
      P('Nobody did this deliberately. These are two documents written at different times by different hands that were supposed to say the same thing.', { after: 200 }),

      H2('Why the firm cares'),
      P('The SEC examines these firms. Comparing Part 1 against the brochure is among the first and cheapest things an examiner does, because a mismatch is a free finding — objective, undeniable, in writing, and an invitation to look harder at everything else.'),
      P('The fee mismatches are worse than embarrassing. If the brochure told clients 1,25% and the firm charged 1,5%, that stops being a paperwork problem.'),
      CALLOUT('The industry already names this problem',
        'A compliance vendor publishes an article titled "Does your RIA firm’s Form ADV Part 1 match its Form ADV Part 2?" — so awareness that this is a real failure mode already exists, and no product performs the check. [PLAUSIBLE — secondary source]', ACCENT),
      PB(),

      // ── 2
      H1('2.  The mechanism that makes a faceless seller work'),
      P('This is the part that distinguishes ADV-Check from every earlier candidate, and it is worth stating precisely.'),
      P('Because the buyer is on no marketplace and does not know this category exists, outbound email is the only channel. Which normally raises an unanswerable question: why would a small US firm trust an unknown vendor in Brazil?'),
      P('Here, it does not have to. Both documents are public, so Sol computes the mismatch first and puts the answer in the email:'),
      new Paragraph({
        spacing: { before: 140, after: 140 }, indent: { left: 400, right: 400 },
        border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT } },
        children: [new TextRun({
          text: '  "Item 5.F of your Form ADV says US$412M. Item 4 of your own client brochure says US$353M."',
          size: 23, font: FONT, italics: true, color: ACCENT,
        })],
      }),
      P('That is not a sales pitch. It is evidence about the recipient, which the recipient can verify in ten seconds against their own filings.', { after: 180 }),
      H2('The five properties this gives the business'),
      tbl([26, 74], [
        ['Property', 'Why it matters'],
        [{ v: 'Evidence, not a pitch', opts: { b: true } }, 'A specific verified defect converts far better than generic outreach, because there is nothing to believe — only something to check.'],
        [{ v: 'No credibility required', opts: { b: true } }, 'Authority rests on the buyer’s own documents, not the sender’s résumé. Decisive for a founder with no track record and no credential.'],
        [{ v: 'Always on', opts: { b: true } }, 'No seasonal window to wait for. She sends whenever she chooses.'],
        [{ v: 'Pre-qualified', opts: { b: true } }, 'The comparison runs in bulk before contact, so she writes only to firms she already knows have the problem.'],
        [{ v: 'AI on her side', opts: { b: true } }, 'She runs the analysis at scale. The buyer receives a finished answer and installs nothing.'],
      ]),
      CALLOUT('This defines a trigger class the earlier framework did not have',
        'Previous analysis recognised only two kinds of purchase trigger: visible-and-dated (a published deadline against a named company) and invisible-but-frequent. This is a third — the visible defect. It is computable, company-specific, permanently available, and self-proving. It is better than a deadline, because a deadline tells you when someone is busy while a defect tells you they have a problem right now.', GREEN),
      PB(),

      // ── 3
      H1('3.  The data infrastructure — verified end to end'),
      P('This section exists because it is the asset. Every endpoint below was requested directly on 6 August 2026 and returned what is recorded. No login, no API key, no paid subscription anywhere in the chain.'),
      tbl([21, 47, 32], [
        ['Piece', 'Source', 'Result'],
        [{ v: 'The firm roster', opts: { b: true } },
         'catalog.data.gov → SEC FOIA distribution, file ia050126.zip',
         { v: 'HTTP 200. 16.779 rows, all Firm Type = Registered. 448 columns.', opts: { color: GREEN, b: true } }],
        ['Websites', 'Column: Website Address', { v: '15.445 firms carry one', opts: { color: GREEN } }],
        ['Geography', 'Column: Main Office Country', { v: '14.557 US, 271 UK, 150 Canada', opts: { color: GREEN } }],
        [{ v: 'Part 1 per firm', opts: { b: true } },
         'reports.adviserinfo.sec.gov/reports/ADV/{CRD}/PDF/{CRD}.pdf',
         { v: 'HTTP 200. Real PDFs, 1,1–13,4 MB, full text layer.', opts: { color: GREEN, b: true } }],
        [{ v: 'Part 2A brochure', opts: { b: true } },
         'files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID={id}',
         { v: 'HTTP 200. 376 KB, 12 pages, 11 of 11 required Part 2A headings present.', opts: { color: GREEN, b: true } }],
        ['Search API', 'api.adviserinfo.sec.gov/search/firm', { v: 'HTTP 200, structured JSON', opts: { color: GREEN } }],
        ['Firm-detail API', 'api.adviserinfo.sec.gov/search/individual-firm-detail', { v: 'HTTP 403 — not usable', opts: { color: RED } }],
        ['Bulk brochure archive', 'SEC bulk Part 2A files', { v: 'Stop at December 2024. Post-2025 data is on IAPD only.', opts: { color: AMBER } }],
      ]),
      P('The brochure that was fetched to confirm the format belongs to Deer Isle Research & Management, LLC, and is dated 2 February 2026 — a live current filing, not an archive artefact.', { after: 180 }),

      H2('Two findings that corrected earlier assumptions'),
      CALLOUT('The Part 1 PDF does not contain the brochure',
        'A first check suggested the two documents were bundled in one file, which would have simplified everything. Testing the individual required headings refuted it: "Fees and Compensation", "Types of Clients", "Methods of Analysis", "Disciplinary Information" and "Brokerage Practices" all returned zero hits. A genuine Part 2A must contain every one. The Part 1 PDF is Part 1 only, and the brochure is a second fetch.', RED),
      CALLOUT('"Not available in bulk" was misread as "must be done by hand"',
        'The SEC stopped publishing brochures as a bulk archive after December 2024. That was initially recorded as a limit on how many firms Sol could approach — wrongly. Not-bulk means fetching them individually, which is a script. Brochure version IDs are enumerable integers: the confirming PDF above was retrieved by guessing one. The corpus can be walked rather than looked up firm by firm.', AMBER),
      PB(),

      // ── 4
      H1('4.  How it works'),
      P('Four steps. Only the last one involves a customer.'),
      NUM('Fetch. Pull the 448-column roster — already done. Walk the Part 1 PDFs and the brochure archive by script.', 'pipe'),
      NUM('Extract. Read the declared values out of Part 1 and the corresponding statements out of the brochure prose.', 'pipe'),
      NUM('Compare. Check each fact that appears in both documents. Record every disagreement with its item number and page reference.', 'pipe'),
      NUM('Contact. Email the firm one real mismatch as proof. Sell the complete report — every discrepancy, each with page citations.', 'pipe'),
      P('Claude Code builds all of steps 1 to 3. It never touches the buyer’s side of the transaction, because there is no buyer side: they receive a PDF about themselves.', { after: 180 }),

      H2('What the buyer receives'),
      BUL('A findings report: every fact stated differently in the two filings, with item numbers and page references for each.'),
      BUL('The specific wording in each document that conflicts, quoted, so nothing has to be taken on trust.'),
      BUL('No software. No login. No upload. No AI account. Nothing to install, configure or learn.'),
      CALLOUT('Why this survives "they could just use ChatGPT"',
        'They could. Pasting two documents into a chat model and asking for contradictions would get most of the way. The product does not compete with that capability — it competes with not knowing the defect exists, not having gathered both documents, and not getting round to it. The email arrives with the answer already in it. That is how most information products work, and it is an honest defence rather than a technical one.', ACCENT),
      PB(),

      // ── 5
      H1('5.  The buyer'),
      tbl([28, 72], [
        ['Attribute', 'Detail'],
        ['Role', 'Owner-principal, or Chief Compliance Officer, at a firm below roughly US$1B under management — usually the same person'],
        ['Country', 'United States (14.557 firms). CAN-SPAM is an opt-out regime, so cold B2B email is lawful.'],
        ['Language', 'English-native. No translation problem, and no call is ever required.'],
        ['Literacy', 'Financially literate by profession. Reads a discrepancy table without help.'],
        ['Spending habit', 'Already buys compliance products self-serve in the US$500–900 range [PLAUSIBLE]'],
        ['Payment', 'Holds the company card. No purchase order, no procurement, no committee.'],
      ]),
      P('This is the strongest payer profile in any candidate assessed for this business. The problem-owner and the card-holder are the same person, which is exactly what the US$250–750 price band exists to guarantee.', { after: 180 }),
      H2('Reaching them'),
      P('A new sending domain safely carries 600 to 1.000 emails per month before deliverability degrades. Against 14.557 US firms that is roughly fourteen months of runway before the list is exhausted — and it refreshes annually as filings change.'),
      P('Germany is excluded from email outright under UWG §7(2), which requires express prior consent and is enforced through competitor litigation. This costs nothing here: the market is American.'),
      PB(),

      // ── 6
      H1('6.  Economics'),
      P('The honest range, with the uncertainty left in rather than averaged away.'),
      tbl([34, 33, 33], [
        ['', 'At US$650', 'At US$400'],
        ['Sales needed per month', { v: '11–13', opts: { b: true } }, { v: '19–21', opts: { b: true } }],
        ['Emails per month at 2% reply-to-sale', '550–650', '950–1.050'],
        ['Fits a new domain’s capacity?', { v: 'Yes, comfortably', opts: { color: GREEN } }, { v: 'At the ceiling', opts: { color: AMBER } }],
        ['Months of list at that rate', '~14', '~8'],
      ]),
      P('Target is R$30.000/month net, roughly US$7.400–8.300/month in revenue.', { after: 160 }),
      H2('Capital at risk before the first sale'),
      tbl([60, 40], [
        ['Item', 'Cost'],
        ['Domain', 'US$12'],
        ['Email sending tooling', 'US$20/month'],
        ['Contact enrichment credits', 'US$50–100'],
        ['Wise Business account', 'Free'],
        ['Build', { v: 'Days of Claude Code time — no cash', opts: { b: true } }],
        [{ v: 'Total', opts: { b: true } }, { v: 'Under US$220', opts: { b: true, color: GREEN } }],
      ]),
      CALLOUT('The pricing risk, stated plainly',
        'A pre-computed report is harder to hold at US$650 than a tool would be, because the buyer is paying for a finding rather than for labour they can see. The value is real but its cost is invisible. This may settle at US$350–450, which raises required volume from 11 sales a month to about 20 and shortens the list runway from fourteen months to eight. That is a pricing question a test settles, not a structural flaw.', AMBER),
      PB(),

      // ── 7
      H1('7.  What is verified, and what is not'),
      H2('Verified by direct fetch'),
      BUL('16.779 registered advisers, 15.445 with websites, 14.557 US-based — counted from the downloaded file, not quoted from a source.'),
      BUL('Both documents are retrievable programmatically, free, with no login and no API key.'),
      BUL('The brochure format is confirmed against all eleven required Part 2A headings.'),
      BUL('Filing dates cluster hard: 11.358 firms file in March alone — 68% of the industry — and 93% file February to April.'),
      H2('Not verified — and one of these decides everything'),
      tbl([30, 40, 30], [
        ['Unknown', 'Why it matters', 'Cheapest test'],
        [{ v: 'The mismatch rate', opts: { b: true, color: RED } },
         { v: 'THE decisive question. At 5% there is no business — nothing to put in any email. At 40% she has a hook for every message she will ever send.', opts: { b: true } },
         { v: 'Script the comparison across a few hundred firms. Cost: US$0.', opts: { b: true, color: GREEN } }],
        ['Willingness to pay US$650', 'Sets whether volume is 11/month or 21/month', 'Quote a price to the first 40 replies'],
        ['Reply rate to a verified defect', 'Should beat generic outreach, but any figure above 3% is an assumption', '200 emails, measure'],
        [{ v: 'IAPD terms on automated access', opts: { color: AMBER } },
         { v: 'The endpoints work; whether the terms permit bulk fetching was NOT checked. An earlier candidate hit exactly this — a public roster whose terms prohibited scraping, forcing manual reading.', opts: { color: AMBER } },
         'Read the IAPD and SEC.gov terms of use before writing any bulk fetcher'],
      ]),
      CALLOUT('Read this before building anything',
        'The mismatch rate is the only thing that matters first, and it costs nothing to learn. Both documents are public and both are scriptable, so the comparison can be run across several hundred firms without contacting a single person, without a domain, and without spending a dollar. Everything else in this document is downstream of that one number.', RED),
      PB(),

      // ── 8
      H1('8.  The test that decides it'),
      P('One measurement, no purchase, no permission, no cash.'),
      new Paragraph({ spacing: { before: 100, after: 140 }, children: [
        new TextRun({ text: 'What fraction of firms carry a real, quotable discrepancy?', size: 27, font: FONT, bold: true, color: ACCENT }),
      ] }),
      NUM('Take a few hundred US firms from the roster already downloaded.', 'test'),
      NUM('Fetch each firm’s Part 1 PDF and its Part 2A brochure.', 'test'),
      NUM('Compare the facts that appear in both. Count how many firms show at least one genuine disagreement.', 'test'),
      P('Cost: US$0. Duration: days. Requires nobody’s cooperation.', { bold: true, after: 160 }),
      tbl([30, 70], [
        ['Result', 'What it means'],
        [{ v: 'Above ~30%', opts: { b: true, color: GREEN } }, { v: 'Proceed. Every cold email she ever sends has real ammunition, and the always-on trigger makes seasonality irrelevant.', opts: { color: GREEN } }],
        [{ v: '10–30%', opts: { b: true, color: AMBER } }, { v: 'Viable but narrower — she can only write to the subset that has a defect, so the effective list shrinks proportionally. Recompute the runway before building.', opts: { color: AMBER } }],
        [{ v: 'Below ~10%', opts: { b: true, color: RED } }, { v: 'Stop. There is nothing to put in the email, and the entire advantage of this business disappears with it.', opts: { color: RED } }],
      ]),
      P('This is the first time in this project that the cheapest available test is also the decisive one. The previous candidate’s free test turned out to be unrunnable, because the document corpus it needed did not exist publicly. This one runs today.', { after: 180 }),
      PB(),

      // ── 9
      H1('9.  Honest weaknesses'),
      tbl([26, 46, 28], [
        ['Weakness', 'The problem', 'Mitigation'],
        [{ v: 'Low repeat purchase', opts: { b: true } }, 'Essentially annual per firm. A customer has little reason to buy again soon, so the business is a continuous hunt for new strangers rather than a base of returning ones.', 'The list is large enough for ~14 months. A second product on the same data would extend it. A backup candidate is being developed specifically to beat this axis.'],
        [{ v: 'Price pressure', opts: { b: true } }, 'The value is a finding, not visible labour. US$650 may not hold.', 'Test at US$650 first. Falling back to US$400 roughly doubles required volume but does not break the model.'],
        [{ v: 'Giving away the proof', opts: { b: true } }, 'If the email shows a real mismatch free, why pay for the report?', 'The email shows one. The report has all of them, with page citations and the wording of each conflict. Build it that way deliberately.'],
        [{ v: 'Terms of use', opts: { b: true } }, 'The endpoints work; the terms were not read.', 'Read them before writing a bulk fetcher. If automated access is barred, fall back to slower fetching — the data is public regulatory disclosure, not a private platform’s roster.'],
        [{ v: 'A vendor could add this', opts: { b: true } }, 'Existing compliance software could ship the same check as a feature.', 'Real risk and not preventable. It argues for moving quickly and for the price staying self-serve rather than enterprise.'],
      ]),
      H2('Why it was chosen anyway'),
      P('It is the only candidate assessed whose authority rests on nothing. Every other survivor needed the buyer to believe something about the seller — that she understood a regulation, that her benchmark data was right, that her legal reading held. Here the buyer believes only their own two documents.'),
      P('For a faceless founder with no credential, no track record, no audience and no capital, that is the single most valuable property a product can have.'),
      PB(),

      // ── 10
      H1('10.  What was rejected to get here'),
      P('Recorded so nothing gets quietly revisited.'),
      tbl([24, 76], [
        ['Candidate', 'Cause of death'],
        ['DeckProof', 'Ranked first before this one. Displaced on list size (2.400/year against 16.779) and because its anchor was a sunk cost. Its free validation test also proved unrunnable — only 7 usable documents existed across 262 brand websites, and 12 of 14 real files had no extractable pricing.'],
        ['CitationProof', 'Best trigger of any candidate — 30.273 named, dated OSHA inspections. Killed because its paid core is already free: three working no-account penalty calculators, one operated by a US$447 rival as a lead magnet.'],
        ['NoticeBench 65', 'Biggest anchor and list in the set. Killed by the self-verification trap — it promised "this label is legally correct" and "your case is worth US$X", neither checkable by inspection, both requiring borrowed authority a faceless foreign vendor cannot supply.'],
        ['ANNEXCHECK', 'A legally mandatory Responsible Person at £490–690/year already contracts to do the job. The buyer cannot not own the substitute.'],
        ['PressProof', 'The confidentiality that blocks a chat model equally blocks an unsigned file from an unknown vendor. The buyer with the greatest need has the largest policy barrier.'],
        ['LINELOCK, RIO BLOCKS, CREDIT LAB, PITCH & PAID, WRAPCHECK', 'Killed earlier on identical products already shipping, or on substitutes doing the whole job at US$0–25.'],
      ]),
      CALLOUT('The rule that produced this shortlist',
        'A cheaper substitute kills a candidate only when it does the whole job. A substitute doing most of the job is an open question about willingness to pay, and willingness to pay cannot be settled from a desk. Applied the other way, that logic kills Notion because a text file is free. Nineteen candidates were rejected before this rule was corrected — several of them, on the evidence, wrongly.', ACCENT),
      new Paragraph({ spacing: { before: 260 }, children: [
        new TextRun({ text: 'Next action: run the mismatch-rate test. It costs nothing and everything else depends on it.', size: 23, font: FONT, bold: true, color: ACCENT }),
      ] }),
    ],
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync('/home/user/Random-Access-Memories/ADV_Check_Business_Overview.docx', b);
  console.log('written', b.length, 'bytes');
});
