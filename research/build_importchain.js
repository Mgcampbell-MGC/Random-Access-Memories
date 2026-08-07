const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, WidthType, BorderStyle, ShadingType,
  LevelFormat, PageBreak, Header, Footer, PageNumber,
} = require('docx');
const fs = require('fs');

const ACCENT = '14532D';
const GREY = '595959';
const RED = '9E2A2B';
const GREEN = '1E5631';
const AMBER = '8A6100';
const BODY = 21;
const FONT = 'Calibri';
const CW = 9026;

const P = (text, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, line: 276 },
  alignment: o.align, indent: o.indent,
  children: [new TextRun({ text, size: o.size ?? BODY, font: FONT, bold: o.bold, italics: o.italics, color: o.color ?? '000000' })],
});
const RICH = (runs, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, line: 276 }, alignment: o.align, indent: o.indent,
  children: runs.map((r) => new TextRun({ text: r.t, size: r.size ?? BODY, font: FONT, bold: r.b, italics: r.i, color: r.c ?? '000000' })),
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
  numbering: { reference: ref, level: 0 }, spacing: { after: 70, line: 276 },
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
      spacing: { after: 0, line: 264 }, alignment: o.align,
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
    width: { size: CW, type: WidthType.DXA }, columnWidths: w,
    borders: { top: B, bottom: B, left: B, right: B, insideHorizontal: B, insideVertical: B },
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0 && o.header !== false,
      children: r.map((c, ci) => {
        const isH = ri === 0 && o.header !== false;
        const opts = (typeof c === 'object' && !Array.isArray(c) && c.opts) ? c.opts : {};
        const val = (typeof c === 'object' && !Array.isArray(c) && c.opts) ? c.v : c;
        return cell(val, w[ci], {
          fill: isH ? ACCENT : (opts.fill ?? (ri % 2 === 0 ? 'F5F8F5' : undefined)),
          color: isH ? 'FFFFFF' : opts.color,
          bold: isH || opts.bold, align: opts.align, size: opts.size,
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
  width: { size: CW, type: WidthType.DXA }, columnWidths: [CW],
  borders: {
    top: { style: BorderStyle.SINGLE, size: 3, color },
    bottom: { style: BorderStyle.SINGLE, size: 3, color },
    left: { style: BorderStyle.SINGLE, size: 18, color },
    right: { style: BorderStyle.SINGLE, size: 3, color },
  },
  rows: [new TableRow({ children: [new TableCell({
    width: { size: CW, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: 'FAFAFA', color: 'auto' },
    margins: { top: 120, bottom: 120, left: 160, right: 140 },
    children: [
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: label, size: 19, font: FONT, bold: true, color })] }),
      new Paragraph({ spacing: { after: 0, line: 276 }, children: [new TextRun({ text, size: BODY, font: FONT })] }),
    ],
  })] })],
});
const QUOTE = (lines) => new Paragraph({
  spacing: { before: 140, after: 140 }, indent: { left: 380, right: 300 },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT } },
  children: lines.map((l, i) => new TextRun({
    text: '  ' + l, size: 20, font: FONT, italics: true,
    color: ACCENT, break: i > 0 ? 1 : 0,
  })),
});
const PB = () => new Paragraph({ children: [new PageBreak()] });

const doc = new Document({
  creator: 'Sol',
  title: 'Import Chain Integrity — Business Overview',
  description: 'FDA supplier-registration monitoring for US medical device importers',
  numbering: {
    config: [
      { reference: 'bul', levels: [
        { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 200 } } } },
        { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 200 } } } },
      ] },
      { reference: 'bld', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 220 } } } }] },
      { reference: 'why', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 220 } } } }] },
      { reference: 'set', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 220 } } } }] },
    ],
  },
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1300, bottom: 1200, left: 1440, right: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({
      alignment: AlignmentType.RIGHT, spacing: { after: 0 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' } },
      children: [new TextRun({ text: 'Import Chain Integrity — Business Overview', size: 16, font: FONT, color: GREY })],
    })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ text: 'Figures marked VERIFIED were fetched 7 Aug 2026  ·  ', size: 15, font: FONT, color: GREY }),
        new TextRun({ children: [PageNumber.CURRENT], size: 15, font: FONT, color: GREY }),
      ],
    })] }) },
    children: [
      // cover
      new Paragraph({ spacing: { before: 800, after: 60 }, children: [new TextRun({ text: 'IMPORT CHAIN', size: 62, font: FONT, bold: true, color: ACCENT })] }),
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: 'INTEGRITY', size: 62, font: FONT, bold: true, color: ACCENT })] }),
      new Paragraph({ spacing: { after: 420 }, children: [new TextRun({ text: 'FDA supplier-registration monitoring for US medical device importers', size: 28, font: FONT, color: GREY })] }),
      RULE(),
      RICH([
        { t: 'The one-sentence version.  ', b: true },
        { t: 'A US medical device importer must list its foreign factories in its own FDA registration; every year some of those factories quietly fail to renew and FDA deletes them from the public file without telling anyone — so the importer’s own federal filing now points at establishments the regulator no longer lists, and only someone keeping a private weekly archive can prove it.' },
      ], { after: 200 }),
      tbl([30, 70], [
        ['Field', 'Position'],
        ['Product', 'A pre-computed PDF audit, then a monthly monitoring feed. The buyer installs nothing.'],
        ['Buyer', 'Regulatory-affairs or QA manager at a US medical device importer or distributor'],
        ['Price', 'US$350 one-off audit, then US$199/month monitoring'],
        ['Buyer can pay', { v: 'VERIFIED — every prospect paid FDA US$11.423 between Oct and Dec 2025', opts: { b: true, color: GREEN } }],
        ['Population', { v: '5.920 US importers declaring foreign factories; 1.846 currently defective', opts: { b: true } }],
        ['Measured need', { v: '31,18% raw / 15,05% clean — full population, reproduced 3×', opts: { b: true, color: GREEN } }],
        ['Channel', 'Cold email only. FDA publishes the responsible person’s name for all 5.920.'],
        ['Capital at risk', 'Under US$150 before the first sale'],
        ['Status', { v: 'Data and solvency VERIFIED. Demand UNTESTED.', opts: { color: AMBER, b: true } }],
      ]),
      new Paragraph({ spacing: { before: 200 }, children: [new TextRun({ text: 'Version 1.0  ·  7 August 2026', size: 18, font: FONT, color: GREY })] }),
      PB(),

      // 1
      H1('1.  What goes wrong, and why nobody notices'),
      P('Any company that imports medical devices into the United States must register with the FDA. As part of that registration it files a list of the foreign establishments — the factories — that make the devices it imports.'),
      P('Those foreign factories must hold their own current FDA registration, renewed annually between 1 October and 31 December.'),
      P('Every year a slice of them do not renew. Some go out of business, some restructure, some simply miss the window. When that happens FDA removes them from the public registration file.'),
      CALLOUT('And this is the whole business',
        'FDA sends no notice to the importer. The importer’s own federal filing still names a factory the regulator no longer lists — and because FDA erases rather than archives, the importer cannot look up what happened even if they think to check. Devices from an unregistered foreign establishment are misbranded at the border.', ACCENT),
      P('Sol sells a report that tells a named importer how many of its declared factories are missing from FDA’s current file, and which of its cleared device listings those factories sit under. Then a monthly subscription that watches the weekly files and reports every change.', { after: 180 }),

      H2('Why the importer cannot easily do this themselves'),
      BUL('The declared-factory list lives inside their FURLS account; the current registration file is a separate 44.000-row government download. Nobody joins the two.'),
      BUL('FDA’s free search works one establishment at a time, and an importer may have declared 5, 20 or 300 factories.'),
      BUL('Once a factory is deleted, its record is gone from every public source — so the absence is invisible unless someone was watching before it happened.'),
      PB(),

      // 2 — GATE ZERO
      H1('2.  Why the buyer can pay — and why this section comes first'),
      P('Every earlier version of this project answered the question "will they pay?" and never asked "can they?". The last candidate reached a full written plan before anyone measured the buyers, at which point 70% of them turned out to have annual revenue under US$50.000. That is why this section leads.', { italics: true, color: GREY }),
      new Paragraph({ spacing: { before: 140, after: 140 }, children: [new TextRun({
        text: 'Every prospect paid FDA US$11.423 between 1 October and 31 December 2025, or it is not in the file at all.',
        size: 25, font: FONT, bold: true, color: ACCENT,
      })] }),
      P('This is a fee-gated list, not an inference from company names. The population is not "companies with a problem" — it is "companies holding a current FDA establishment registration", and holding one requires writing that cheque.'),
      tbl([44, 56], [
        ['Fact', 'Source'],
        [{ v: 'FY2026 annual establishment registration fee: US$11.423', opts: { b: true } },
         'Federal Register doc 2025-14412, 30 Jul 2025; confirmed on FDA’s own MDUFA fee page [VERIFIED]'],
        [{ v: 'No small-business reduction exists for this fee', opts: { b: true, color: GREEN } },
         'A hardship waiver is available via Small Business Determination, but only on renewals and only on demonstrated hardship — exceptional, not routine [VERIFIED]'],
        ['Initial importers are inside the paying set',
         'FDA’s "Who Must Register, List and Pay the Fee": Initial Importer → Register YES 807.40(a), Pay Fee YES. Re-checked specifically, because the case collapses if importers were exempt [VERIFIED]'],
        ['Up from US$9.280 in FY2025', 'Same source [VERIFIED]'],
      ]),
      H2('Size inside the buyer set'),
      P('Declared-manufacturer count is a direct proxy for import volume, and therefore for revenue.'),
      tbl([50, 50], [
        ['Measure', 'Count'],
        ['Currently-registered establishments', '28.535'],
        ['Carry INITIAL_IMPORTER_FLAG = Y', '5.741'],
        [{ v: 'US registrants declaring ≥1 foreign manufacturer', opts: { b: true } }, { v: '5.920', opts: { b: true } }],
        ['Declaring 5 or more', '1.147'],
        ['Declaring 10 or more', '543'],
      ]),
      P('Named examples at the top of the distribution: SSPT Inc. declares 359 foreign manufacturers, Dynarex Corp. 306, Medline Industries 291, Henry Schein 253 across 12 separate registered US sites, Cardinal Health 200 LLC 244, Medical Depot Inc. 224.', { after: 160 }),
      CALLOUT('The comparison that matters',
        'A company that cannot find US$11.423 is not in the file. The previous candidate’s buyers were charities that were delinquent precisely because they had no money — poverty and the defect were the same thing. Here the defect sits with companies that have already proved they can pay a five-figure federal fee.', GREEN),
      PB(),

      // 3
      H1('3.  The defect, exactly as the email states it'),
      P('Two values, both from the recipient’s own federal filings, both checkable in FDA’s free search in under five minutes. Real companies, real numbers from the current file.'),
      QUOTE([
        'Subject: 3 of the 5 factories in your FDA filing aren’t in FDA’s current registration file',
        '',
        'Randox Laboratories-US, Ltd — FDA establishment registration 2086993, Kearneysville WV.',
        '',
        'Your FURLS registration declares 5 foreign manufacturing establishments. 3 of the 5 do not',
        'appear in FDA’s current establishment registration file. Those 3 are attached to 92 of your',
        'device listings, including K000375, K000468, K000469 and K000661.',
        '',
        'To check: open your FURLS account, take those three factory names off your own declared-',
        'manufacturer list, and search each in FDA’s free Establishment Registration database.',
        'They will not return a current registration. FDA sends no notice when this happens.',
      ]),
      H2('Four more, to show the pattern is not cherry-picked'),
      tbl([40, 14, 14, 32], [
        ['Importer', 'Declared', 'Absent', 'Implicated clearances'],
        ['Metropolis International LLC (reg 3005877899)', '13', { v: '3', opts: { b: true } }, 'K050299, K024352, K082987, K050514, K050622, K120388'],
        ['Nobel Biocare USA LLC (reg 2027971)', '17', { v: '4', opts: { b: true } }, 'K041275, K913255'],
        ['Medten USA Inc. (reg 3018817074)', '23', { v: '3', opts: { b: true } }, 'K161938'],
        ['Imperial Optical Inc. (reg 1319386)', '19', { v: '7', opts: { b: true } }, '—'],
      ]),
      CALLOUT('The K-number is what makes this land',
        'The declaration table joins to the device-listing table: of 24.767 dangling declaration rows belonging to US importers, 2.675 carry a premarket submission number. So for 282 importers the email can name the cleared device whose declared factory has vanished — 1.481 distinct K/P numbers implicated, and 171 of those importers have two or more. A K-number is the most self-evident object in this industry: the recipient looks it up in FDA’s free 510(k) database and sees their own clearance.', ACCENT),
      H2('What the product never says'),
      RICH([
        { t: 'It never says ' },
        { t: '"you are non-compliant"', b: true },
        { t: ' or ' },
        { t: '"this shipment will be detained."', b: true },
        { t: ' It says: your filing declares 5, FDA’s current file contains 2, here are the listing IDs. The count and the identifiers are facts. The recipient supplies the names from their own account and confirms the absence in the regulator’s own search.' },
      ]),
      P('That distinction is not cosmetic. Three earlier candidates in this project died because their finding required the recipient to trust an unknown foreign vendor’s judgement. Nothing here does.', { color: GREY, italics: true }),
      PB(),

      // 4
      H1('4.  The measured need'),
      P('Measured on the full population rather than a sample, and reproduced independently three times across two different weekly snapshots — matching to the digit each time.'),
      tbl([62, 38], [
        ['Measure', 'Value'],
        ['Registration rows / unique establishments', '43.990 / 28.535'],
        ['Declaration rows / distinct declaring importers', '150.426 / 6.011'],
        [{ v: 'US importers registered, with declarations', opts: { b: true } }, { v: '5.920', opts: { b: true } }],
        ['Total dangling declared-manufacturer links', '6.325 (3.478 distinct absent keys)'],
        [{ v: 'Importers with ≥1 dangling — RAW rate', opts: { b: true } }, { v: '1.846 = 31,18%', opts: { b: true, color: AMBER } }],
        [{ v: 'Importers with ≥2 dangling — CLEAN rate', opts: { b: true } }, { v: '891 = 15,05%', opts: { b: true, color: GREEN } }],
        ['Ideal customer profile (5+ declared, 2+ dangling)', '717'],
        ['Mid-size ICP (5–25 declared, 3+ dangling)', '381'],
        ['Premium tier (dangling under a cleared K/P number)', '282'],
      ]),
      H2('Raw versus clean — stated honestly'),
      P('A dangling link has three possible causes:'),
      BUL('The foreign factory genuinely failed the October–December renewal.'),
      BUL('It re-registered and FDA issued a new internal key, so the importer’s reference is merely stale.'),
      BUL('The importer never removed a supplier it stopped using.'),
      P('The 31,18% raw figure covers all three. The 15,05% two-or-more figure is the conservative floor. Separating them requires two weekly snapshots, which is why the archive is build step one.'),
      CALLOUT('And the pitch does not depend on which cause it is',
        'In all three cases the importer’s own federal filing is wrong and only the importer can correct it. The border-risk framing applies to the first cause only; the filing-accuracy framing applies to all three, and that is the framing used until the archive can tell them apart.', ACCENT),
      PB(),

      // 5
      H1('5.  Why it recurs — three independent clocks'),
      NUM('Weekly. FDA republishes the entire extract every week. Supplier relationships and device listings change continuously between snapshots.', 'why'),
      NUM('Annually, in a wave. Registration renewal runs 1 October to 31 December, so every January a fresh cohort of foreign establishments drops out of the file. That is a dated, forward, calendar-driven event that can be pre-announced to subscribers in September and delivered against in January.', 'why'),
      NUM('It never completes. Supply-chain integrity is a standing condition, not a task. The subscriber has no "done" state at which cancelling makes sense.', 'why'),
      P('The January wave is the part a one-off report can never have: a reason to buy that arrives on a known date, every year, for every prospect simultaneously.', { after: 200 }),

      H1('6.  The moat — FDA erases, it does not archive'),
      P('This is the single most defensible thing about the business, and it cannot be replicated by a competitor who starts later.'),
      tbl([62, 38], [
        ['Check', 'Result'],
        ['Absent establishment keys appearing in registration_listing.txt', { v: '0 of 3.478', opts: { b: true, color: GREEN } }],
        ['Absent keys surviving in Official_Correspondent.txt', { v: 'exactly 1', opts: { b: true } }],
        ['Orphan keys in one relationship table, no name attached', '274'],
        ['Distinct values of reg_expiry_date_year across 43.989 rows', { v: '2026 only', opts: { b: true, color: GREEN } }],
      ]),
      CALLOUT('What that means commercially',
        'Nobody — not the buyer, not a competitor, not FDA’s own public search — can reconstruct who the lapsed factory was or when it disappeared without a private archive of weekly snapshots. That archive begins accruing on day one and cannot be built retroactively. Every week it runs, the asset appreciates and a later entrant falls further behind.', GREEN),
      P('It also drives the build order: the weekly cron ships before the product does.', { bold: true }),
      PB(),

      // 7
      H1('7.  The buyer, and how she reaches them'),
      P('The buyer is the regulatory-affairs or QA manager at a US medical device initial importer or distributor. Not procurement, not legal. This person owns the FURLS account, is the one who would have to correct the declaration, and is the individual FDA already holds on file.'),
      tbl([56, 44], [
        ['Segment', 'Count'],
        ['US importers with declarations', '5.920'],
        ['Currently defective', '1.846'],
        [{ v: 'Ideal customer profile', opts: { b: true } }, { v: '717', opts: { b: true } }],
        ['Mid-size ICP (the test cohort)', '381'],
        ['With a K-number-linked finding', '282'],
        ['Giants excluded (procurement-gated)', 'Walmart, Medline, Cardinal, Henry Schein'],
      ]),
      H2('The contact is inside the government file'),
      RICH([
        { t: 'Official_Correspondent.txt gives a named person and phone number for ' },
        { t: '5.920 of 5.920', b: true },
        { t: ' US importers with declarations — 100% coverage, checked explicitly. FDA publishes the name of the exact human responsible for the filing that is wrong. Names go to Apollo for email enrichment.' },
      ]),
      P('Sending is CAN-SPAM cold email with a working opt-out, US-only — no Canadian CASL exposure, no German UWG problem. Delivery is a PDF attached to an email. No call, no app, no login, no English conversation: the entire funnel is written asynchronously in language that can be drafted carefully once and reused.', { after: 160 }),
      CALLOUT('One hard rule for the email template',
        'FDA publishes warnings about vendors who sell fake "FDA registration certificates" for a fee. This product sells no certificate, solicits no fee on FDA’s behalf, and points the recipient at their own FURLS account and FDA’s free search. The copy must therefore never contain certificate-like graphics or FDA logos. That is a template rule, not a residual risk to shrug at.', AMBER),
      PB(),

      // 8
      H1('8.  The money'),
      P('US$350 one-off Supplier Registration Integrity Audit per registered site, then US$199/month monitoring against the weekly files.'),
      tbl([56, 44], [
        ['Mix to reach US$7.400–8.300/month', 'Monthly'],
        ['40 retained at US$199', 'US$7.960'],
        ['30 retained at US$199 + 6 audits at US$350', 'US$8.070'],
        ['25 retained at US$249 + 5 audits at US$350', 'US$7.975'],
      ]),
      H2('Penetration required, stated plainly'),
      P('40 subscribers is 5,6% of the 717-member ideal customer profile, or 2,2% of the 1.846 currently defective importers. That is a higher conversion rate than a mass list would need, and it is the honest cost of a small population.'),
      P('What buys it back: every email quotes the recipient’s own registration number and their own two counts. This is not a 0,5%-reply blast — it is roughly 700 individually computed findings.'),
      H2('Capital at risk before the first sale: under US$150'),
      tbl([64, 36], [
        ['Item', 'Cost'],
        ['Domain', 'US$12'],
        ['Email sending (free tier for the first 3.000 sends)', 'US$0–20/month'],
        ['Apollo enrichment credits, ~400 lookups', '~US$50'],
        ['Weekly archive storage (~21 MB/week, ~1,1 GB/year)', 'pennies'],
        ['All FDA source data', { v: 'Free government download, no account', opts: { b: true, color: GREEN } }],
        [{ v: 'Total', opts: { b: true } }, { v: 'Under US$150', opts: { b: true, color: GREEN } }],
      ]),
      H2('The honest ramp'),
      tbl([26, 74], [
        ['Period', 'What happens'],
        ['Weeks 1–2', 'Archive cron live, join engine, PDF template. No revenue.'],
        ['Weeks 3–4', 'The 60-email test. No revenue.'],
        ['Month 2', 'First paid audits if the test clears: realistically 2–5 at US$350 = US$700–1.750'],
        ['Months 3–4', 'Audits convert to monitoring. 8–15 retained. ~US$2.500–4.000/month'],
        ['Months 6–9', { v: 'Target range reached at 30–45 retained — assuming 4–6% ICP penetration and audit-to-monitoring conversion above 50%', opts: { b: true } }],
        ['September, year 1', 'The renewal-wave email to every non-customer, delivered against in January'],
      ]),
      PB(),

      // 9
      H1('9.  The build'),
      P('Four weeks of Claude Code. The order matters, because step one is time-sensitive in a way nothing else is.'),
      NUM('The snapshot archive — day one, before anything else. A weekly cron pulling all nine FDA zips to object storage, timestamped and immutable. Every week it runs, the moat deepens. Nothing downstream needs to exist yet.', 'bld'),
      NUM('The join engine. Parse the pipe-delimited files and produce, per importer: declared count, dangling count, dangling keys, and the K/P numbers each dangling key sits under. Diff against last week.', 'bld'),
      NUM('The FEI continuity resolver — the thing that separates raw from clean. Registration.txt carries FEI_NUMBER, which is stable across a re-registration where the internal key is not. With two snapshots, a vanished key’s FEI can be looked up in the older file and checked for reappearance under a new key in the current one. That mechanically separates a genuine lapse from a re-registration. It is buildable only with archive history — which is why step one is day one.', 'bld'),
      NUM('The PDF and the email machine. Per-importer PDF with both counts, the dangling keys, the affected listings and K-numbers, the verification instructions and a fix checklist. Then Apollo enrichment off the official-correspondent names, and sending with per-recipient merge fields and a working opt-out.', 'bld'),
      H2('Three engineering gotchas already hit, so they cost nothing to avoid'),
      BUL('The download requires a browser User-Agent — plain curl gets a 302 to an abuse page.'),
      BUL('Listing_Proprietary_Name.txt uses a lowercase key field name while every sibling file uses uppercase.'),
      BUL('One field exceeds Python’s default 131.072-byte CSV limit and must be raised explicitly.'),
      P('No hosted app, no buyer-side compute, no per-transaction human step. A card purchase and an emailed attachment.', { bold: true }),
      PB(),

      // 10
      H1('10.  The first test'),
      P('One measurement: does a regulatory manager, shown two numbers from their own federal filing, reply?'),
      tbl([30, 70], [
        ['Parameter', 'Detail'],
        ['Cohort', '60 importers from the mid-size ICP — 5 to 40 declared manufacturers, 3+ dangling, giants excluded. Prioritise the K-number tier.'],
        ['Each email contains', 'Their registration number, declared count, dangling count, affected K-numbers, the verification path, and a US$350 offer with a payment link'],
        ['Cost', { v: 'Under US$100', opts: { b: true } }],
        ['Duration', '14 days from first send'],
        ['Corpus', { v: 'Already in hand — nine government files, already joined', opts: { b: true, color: GREEN } }],
      ]),
      CALLOUT('Why that last row matters',
        'An earlier candidate in this project had a free test that proved unrunnable: it needed a corpus of documents from the open web, and probing 262 company websites yielded only 7 usable files. This test’s entire input is nine government files that have already been downloaded and joined. The 60 findings can be generated before the domain is even bought.', GREEN),
      H2('Stop thresholds'),
      tbl([46, 54], [
        ['Outcome in 14 days', 'Decision'],
        [{ v: '≥1 paid audit, or ≥5 replies of which ≥3 ask price', opts: { b: true, color: GREEN } }, { v: 'BUILD. Proceed to the full engine and the 700-prospect rollout.', opts: { color: GREEN } }],
        [{ v: '2–4 replies, none commercial', opts: { color: AMBER } }, { v: 'ITERATE ONCE. Resend 60 more with the K-number framing forward and filing-accuracy language replacing any border language. One iteration only.', opts: { color: AMBER } }],
        [{ v: '≤1 reply, or ≥2 replies saying "that supplier re-registered, non-issue"', opts: { b: true, color: RED } }, { v: 'STOP. The defect is real but not felt, and no amount of engineering fixes that.', opts: { b: true, color: RED } }],
      ]),
      P('That third row is the genuine kill condition, and it is cheap to reach.', { bold: true }),
      PB(),

      // 11
      H1('11.  What is verified, and what is not'),
      H2('Confirmed independently against the free openFDA API'),
      P('330.251 records, last updated 27 July 2026, no API key required.'),
      tbl([46, 54], [
        ['Field', 'Confirmed'],
        ['registration.initial_importer_flag', 'Present — a real field'],
        ['registration.fei_number', 'Present — the continuity resolver that separates a genuine lapse from a re-registration'],
        ['registration.reg_expiry_date_year', { v: '2026 only — consistent with the erasure moat', opts: { b: true } }],
      ]),
      H2('Not independently reproduced — and this must be re-run before building'),
      CALLOUT('The join counts could not be verified from the machine this was written on',
        'Bare accessdata.fda.gov fails with SSL_ERROR_SYSCALL from this environment, so the raw pipe-delimited files could not be pulled to recompute the 31,18% and 15,05% figures directly. That is an infrastructure limit rather than evidence against the numbers — three independent passes reproduced them on two different weekly snapshots — but it should be re-run from an unblocked network as the first act of the build.', AMBER),
      H2('Three things to settle before building past the archive cron'),
      NUM('Does a dangling link land as material, or get shrugged off as a re-registration? This is the real weakest link. Settled by the US$100 test, whose reply content is itself the measurement. A near-free second route: nine scripted written questions to regulatory managers asking whether they ever audit their declared-manufacturer list.', 'set'),
      NUM('Is fdadevicecheck.com’s US$19/month watchlist pilot a price ceiling or a different product? It does current-status lookups on facilities the user already knows about, and cannot read the importer’s own declaration or date a lapse. But a US$19 anchor in the same inbox is a real hazard to a US$199 price. Cost to settle: zero — request the pilot invitation and read what arrives.', 'set'),
      NUM('Does Apollo return work emails for FDA official correspondents? There are 5.920 named people with phone numbers and no email addresses. Run 50 through Apollo before writing a line of PDF code; under a 40% match rate the channel needs rethinking before the build, not after.', 'set'),
      H2('Only matters after the first paying customer'),
      BUL('Whether a US$350 audit converts to US$199/month above 50%.'),
      BUL('Whether the Internet Archive holds prior Registration.zip snapshots, which would backfill lapse dates immediately rather than in eight weeks. Attempted and blocked; worth one retry from an unblocked network. It accelerates rather than enables — the private archive solves it by month two regardless.'),
      BUL('Whether the same engine sells a second product pointed the other way: telling foreign manufacturers which of their declared US importers have lapsed. Reg_Imp_ID_by_Manu.txt holds 258.134 rows. Same code, different recipient — but non-US outreach, so parked.'),
      PB(),

      // 12
      H1('12.  Why this one, after twenty-nine others'),
      tbl([22, 39, 39], [
        ['', 'ADV-Check (the prior pick)', 'Import Chain Integrity'],
        [{ v: 'Solvency', opts: { b: true } }, 'Asserted from "registered adviser" — no size distribution ever measured', { v: 'Every prospect paid US$11.423 to FDA. Fee-gated, verified, no small-business reduction.', opts: { color: GREEN } }],
        [{ v: 'Measured need', opts: { b: true } }, 'Unmeasured — the stated weakness', { v: '31,18% raw / 15,05% clean on the full population, reproduced 3×', opts: { color: GREEN } }],
        [{ v: 'Recurrence', opts: { b: true } }, 'Annual at best', { v: 'Weekly files, monthly subscription, plus a dated January renewal wave', opts: { color: GREEN } }],
        [{ v: 'Contact', opts: { b: true } }, 'Enrichment guesswork', { v: 'FDA names the responsible person — 5.920 of 5.920', opts: { color: GREEN } }],
        [{ v: 'Defensibility', opts: { b: true } }, 'Two public documents any analyst can pull', { v: 'FDA erases lapsed records; only a private weekly archive can name or date a lapse', opts: { color: GREEN } }],
        [{ v: 'First dollar', opts: { b: true } }, 'Cold email only; ads unavailable at US$10–30/click in finance', 'Cold email, corpus already joined, 60 findings computable today for under US$100'],
      ]),
      H2('The honest weaknesses'),
      BUL('The population is small. 717 in the ideal profile means 40 subscribers is 5,6% penetration — a real conversion requirement, not a rounding error.'),
      BUL('The 31,18% mixes three causes and only one of them is a genuine lapse. The filing-accuracy framing holds regardless, but the strongest version of the pitch needs the archive to separate them.'),
      BUL('A US$19/month competitor exists in an adjacent shape and may anchor the price down.'),
      BUL('If regulatory managers genuinely do not care that their declared list is stale, nothing here saves it — which is exactly what the US$100 test measures, and why it comes before the build.'),
      new Paragraph({ spacing: { before: 260 }, children: [new TextRun({
        text: 'Next action: re-run the join from an unblocked network, start the weekly archive cron the same day, then send 60 emails.',
        size: 23, font: FONT, bold: true, color: ACCENT,
      })] }),
    ],
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync('/home/user/Random-Access-Memories/Import_Chain_Integrity_Business_Overview.docx', b);
  console.log('written', b.length, 'bytes');
});
