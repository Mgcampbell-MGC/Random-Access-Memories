const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, PageBreak
} = require('docx');

const NAVY = '1F3352', ACC = '9A6B3F', GREY = '5A6472', LINE = 'D6DAE0', BG = 'F4F6F8';

const src = fs.readFileSync('DECKPROOF_V2_Business_Overview.md', 'utf8');

// ---- inline markdown (bold + code) -> TextRuns
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*.+?\*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith('**')) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: tok.slice(1, -1), font: 'Consolas', size: 19, color: ACC, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out.length ? out : [new TextRun({ text: '', ...base })];
}

const cell = (txt, { head = false, w } = {}) => new TableCell({
  width: w ? { size: w, type: WidthType.PERCENTAGE } : undefined,
  shading: head ? { type: ShadingType.CLEAR, fill: NAVY } : undefined,
  margins: { top: 90, bottom: 90, left: 130, right: 130 },
  children: [new Paragraph({
    spacing: { before: 0, after: 0 },
    children: head
      ? [new TextRun({ text: txt.replace(/\*\*/g, ''), bold: true, color: 'FFFFFF', size: 19 })]
      : runs(txt, { size: 19 })
  })]
});

const children = [];
const lines = src.split('\n');
let i = 0, tbl = null;

const flushTable = () => {
  if (!tbl || tbl.length === 0) { tbl = null; return; }
  const cols = tbl[0].length;
  const w = Math.floor(100 / cols);
  children.push(new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      left: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      right: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: LINE },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: LINE },
    },
    rows: tbl.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: r.map(c => cell(c, { head: ri === 0, w }))
    }))
  }));
  children.push(new Paragraph({ text: '', spacing: { after: 200 } }));
  tbl = null;
};

for (; i < lines.length; i++) {
  const L = lines[i];
  const t = L.trim();

  if (t.startsWith('|')) {
    const cells = t.split('|').slice(1, -1).map(s => s.trim());
    if (cells.every(c => /^:?-{2,}:?$/.test(c))) continue;
    (tbl = tbl || []).push(cells);
    continue;
  }
  flushTable();

  if (t === '' ) { continue; }
  if (t === '---') { children.push(new Paragraph({ text: '', border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LINE } }, spacing: { before: 160, after: 260 } })); continue; }

  if (t.startsWith('# ')) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 160 },
      children: [new TextRun({ text: t.slice(2), bold: true, size: 40, color: NAVY })] }));
    continue;
  }
  if (t.startsWith('## ')) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 340, after: 140 },
      children: [new TextRun({ text: t.slice(3), bold: true, size: 28, color: NAVY })] }));
    continue;
  }
  if (t.startsWith('### ')) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 260, after: 110 },
      children: [new TextRun({ text: t.slice(4), bold: true, size: 23, color: ACC })] }));
    continue;
  }
  if (t.startsWith('> ')) {
    children.push(new Paragraph({
      spacing: { before: 150, after: 150 },
      indent: { left: 400, right: 260 },
      shading: { type: ShadingType.CLEAR, fill: BG },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACC } },
      children: runs(t.slice(2), { size: 21, italics: true, color: NAVY })
    }));
    continue;
  }
  const num = t.match(/^(\d+)\.\s+(.*)$/);
  if (num) {
    children.push(new Paragraph({ spacing: { before: 60, after: 60 }, indent: { left: 420, hanging: 240 },
      children: [new TextRun({ text: num[1] + '. ', bold: true, color: ACC, size: 21 }), ...runs(num[2], { size: 21 })] }));
    continue;
  }
  if (t.startsWith('- ')) {
    children.push(new Paragraph({ spacing: { before: 50, after: 50 }, indent: { left: 420, hanging: 220 },
      children: [new TextRun({ text: '•  ', color: ACC, bold: true, size: 21 }), ...runs(t.slice(2), { size: 21 })] }));
    continue;
  }
  children.push(new Paragraph({ spacing: { before: 70, after: 70 }, alignment: AlignmentType.LEFT,
    children: runs(t, { size: 21 }) }));
}
flushTable();

const doc = new Document({
  styles: { default: { document: { run: { font: 'Calibri', size: 21, color: '20242B' } } } },
  sections: [{
    properties: { page: { margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } },
    children
  }]
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('DeckProof_V2_Business_Overview.docx', b);
  console.log('written', b.length, 'bytes');
});
