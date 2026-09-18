const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,ImageRun,Table,TableRow,TableCell,WidthType,
 AlignmentType,HeadingLevel,BorderStyle,ShadingType,PageBreak,LevelFormat,convertInchesToTwip}=require('docx');

const TEAL="1F4E4A", CLAY="C96F4A", INK="2B2B2B", SAGE="8FA89B", CREAM="F7F3EC", GREY="6B6B6B", RED="A63A3A";
const W=9506;                                    // content width in DXA
const img=f=>fs.readFileSync(f);

const T=(t,o={})=>new TextRun({text:t,font:"Calibri",size:o.size||21,bold:o.b,italics:o.i,color:o.c||INK,break:o.br});
const P=(t,o={})=>new Paragraph({alignment:o.al,spacing:{before:o.before??0,after:o.after??120,line:290},
  indent:o.ind?{left:o.ind}:undefined,
  border:o.rule?{bottom:{style:BorderStyle.SINGLE,size:6,color:o.rule}}:undefined,
  children:Array.isArray(t)?t:[T(t,o)]});

const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:160},
  children:[new TextRun({text:t,font:"Calibri",size:30,bold:true,color:TEAL})]});
const H2=t=>new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:260,after:110},
  children:[new TextRun({text:t,font:"Calibri",size:24,bold:true,color:CLAY})]});
const BUL=(t,o={})=>new Paragraph({numbering:{reference:"bul",level:0},spacing:{after:70,line:280},
  children:Array.isArray(t)?t:[T(t,o)]});
const NUM=(t,o={})=>new Paragraph({numbering:{reference:"num",level:0},spacing:{after:70,line:280},
  children:Array.isArray(t)?t:[T(t,o)]});
const PIC=(f,w,h)=>new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:160},
  children:[new ImageRun({type:"png",data:img(f),transformation:{width:w,height:h}})]});

// callout box
const BOX=(lines,fill=CREAM,edge=SAGE)=>new Table({columnWidths:[W],width:{size:W,type:WidthType.DXA},
  borders:{top:{style:BorderStyle.SINGLE,size:12,color:edge},bottom:{style:BorderStyle.SINGLE,size:12,color:edge},
           left:{style:BorderStyle.SINGLE,size:12,color:edge},right:{style:BorderStyle.SINGLE,size:12,color:edge},
           insideHorizontal:{style:BorderStyle.NONE},insideVertical:{style:BorderStyle.NONE}},
  rows:[new TableRow({children:[new TableCell({width:{size:W,type:WidthType.DXA},
    shading:{type:ShadingType.CLEAR,fill},margins:{top:160,bottom:160,left:200,right:200},
    children:lines})]})]});

function TBL(head,rows,widths,opts={}){
  const cell=(txt,w,o={})=>new TableCell({width:{size:w,type:WidthType.DXA},
    shading:o.head?{type:ShadingType.CLEAR,fill:TEAL}:(o.alt?{type:ShadingType.CLEAR,fill:"F4F1EB"}:undefined),
    margins:{top:70,bottom:70,left:110,right:110},
    children:[new Paragraph({alignment:o.al,spacing:{after:0},
      children:[new TextRun({text:txt,font:"Calibri",size:o.head?19:19.5,bold:o.head||o.b,
        color:o.head?"FFFFFF":(o.c||INK)})]})]});
  const trs=[new TableRow({tableHeader:true,children:head.map((h,i)=>cell(h,widths[i],{head:true,al:opts.al&&opts.al[i]}))})];
  rows.forEach((r,ri)=>trs.push(new TableRow({children:r.map((c,i)=>{
    const s=typeof c==='object'?c:{t:c};
    return cell(s.t,widths[i],{alt:ri%2===1,b:s.b,c:s.c,al:opts.al&&opts.al[i]});
  })})));
  return new Table({columnWidths:widths,width:{size:widths.reduce((a,b)=>a+b,0),type:WidthType.DXA},
    borders:{top:{style:BorderStyle.SINGLE,size:4,color:"D8D2C6"},bottom:{style:BorderStyle.SINGLE,size:4,color:"D8D2C6"},
     left:{style:BorderStyle.NONE},right:{style:BorderStyle.NONE},
     insideHorizontal:{style:BorderStyle.SINGLE,size:2,color:"E6E1D8"},insideVertical:{style:BorderStyle.NONE}},
    rows:trs});
}
const GAP=(n=120)=>new Paragraph({spacing:{after:n},children:[]});

const body=[];
const push=(...x)=>x.forEach(i=>body.push(i));

/* ===================== COVER ===================== */
push(
 GAP(600), GAP(600),
 new Paragraph({spacing:{after:0},alignment:AlignmentType.CENTER,
   children:[new ImageRun({type:"png",data:img("logo.png"),transformation:{width:470,height:162}})]}),
 GAP(480),
 P("The business, in plain words",{al:AlignmentType.CENTER,size:36,b:true,c:TEAL,after:120}),
 P("What we sell · who buys it · what it costs · what to do first",
   {al:AlignmentType.CENTER,size:22,c:CLAY,after:700}),
 BOX([
   P("We supply newborn starter kits to Brazilian town halls.",{al:AlignmentType.CENTER,size:26,b:true,c:TEAL,after:140}),
   P("Every town hall in Brazil is required by law to publish what it is about to buy, before it buys it — free, online, in a format a computer can read. Around four newborn-kit tenders are published every working day. We read all of them, bid on the ones we can win at a profit, buy the goods only after we have won, and ship them.",
     {al:AlignmentType.CENTER,size:21,after:140}),
   P("We never look for a customer. The law makes them announce themselves.",
     {al:AlignmentType.CENTER,size:22,b:true,c:CLAY,after:0})
 ]),
 GAP(420),
 P("18 September 2026  ·  internal working document  ·  every figure measured, sources in THE_KIT_DESK.md",
   {al:AlignmentType.CENTER,size:17,c:GREY,i:true,after:0}),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 1. THE BUSINESS ===================== */
push(
 H1("1.  What the business actually is"),
 P("Brazilian municípios hand out a newborn kit — an enxoval — to mothers in social assistance programmes. It is a benefício eventual: a thing the town is obliged to give, not a gift it chooses to give. So the demand is set by births and by law, not by anybody's marketing."),
 P("To buy those kits the town must run a public tender. By law (Lei 14.133, art. 54) it must publish the full tender document, including the exact list of items it wants, on a single national website, free, before it can buy anything. It must give suppliers notice — the measured median is 10 working days."),
 P([T("That is our entire sales channel. It is a statute. ",{b:true}),
    T("It cannot be outbid by a competitor with a bigger marketing budget, it cannot be switched off, and it costs R$0 to access.")]),
 GAP(60),
 BOX([
  P("Measured over the last twelve months, nationally:",{size:20,b:true,c:TEAL,after:130}),
  BUL([T("R$57,2 million ",{b:true}),T("of newborn kits bought")]),
  BUL([T("1.012 tenders ",{b:true}),T("across "),T("699 different towns",{b:true})]),
  BUL([T("~4 kit tenders published every working day",{b:true})]),
  BUL([T("Typical tender size: ",{}),T("R$31.080",{b:true})]),
  BUL([T("96,4% are decided on price alone",{b:true}),T(" — no interview, no relationship, no presentation")],{})
 ]),
 H2("Why this one and not something else"),
 P("Four things had to be true. They all are."),
 TBL(["What matters to you","How this business answers it"],
  [["You do not want to chase customers forever","The state publishes the next order whether or not you do anything"],
   ["You do not want to be on camera or be a personality","You are a CNPJ in a bid file. Nobody ever sees you"],
   ["You do not want employees","Suppliers and couriers are vendors, not staff. It stays a one-person company"],
   ["You do not want to be believed as an expert","The town judges a written spec against a price. Nothing is claimed"]],
  [3300,6206]),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 2. BRAND ===================== */
push(
 H1("2.  The brand"),
 P([T("Name: ",{b:true}),T("ACOLHE",{b:true,c:TEAL,size:24}),
    T("  —  legal entity ",{}),T("ACOLHE COMÉRCIO DE ENXOVAIS LTDA",{b:true})]),
 P([T("“Acolher” means to welcome, to take someone in, to shelter. It is the exact word Brazilian social assistance uses for what these kits are for. It reads as serious to a procurement officer and warm to everyone else, and it says what we sell without a single explanation.")]),
 PIC("logo.png",430,148),
 H2("What the brand is for — and what it is not for"),
 P("This brand is not there to win customers. The law delivers the customers. It is there to make three specific people comfortable in under ten seconds:"),
 NUM([T("A procurement officer ",{b:true}),T("checking whether the cheapest bidder is a real company before signing the contract.")]),
 NUM([T("A wholesaler's credit department ",{b:true}),T("deciding whether to give a new buyer 28 days to pay.")]),
 NUM([T("A courier or a bank ",{b:true}),T("opening an account.")]),
 GAP(80),
 BOX([
  P("Rules the brand never breaks",{b:true,size:22,c:CLAY,after:130}),
  BUL("It is a company, never a person. No founder photo, no founder name, no “meet the team”, no social media presence."),
  BUL("It looks like a supplier, not a boutique. Calm, plain, factual. Nothing cute. Procurement officers distrust cute."),
  BUL("It never sells to mothers. The moment it looks like a consumer brand it inherits every problem a consumer brand has, and none of the protection the statute gives us.")
 ],"FAEDE6",CLAY),
 H2("Colours and type, so everything matches"),
 TBL(["Use","Colour","Where"],
  [["Deep teal","#1F4E4A","Wordmark, headings, the site header"],
   ["Terracotta","#C96F4A","One accent only — a button, a rule, a highlight"],
   ["Cream","#F7F3EC","Backgrounds, document panels"],
   ["Sage","#8FA89B","Secondary lines, charts"],
   ["Charcoal","#2B2B2B","All body text"]],
  [1900,1900,5706]),
 P("One typeface everywhere, a plain grotesque (Inter, Work Sans or Calibri are all fine). Never more than two weights on a page.",
   {size:19,c:GREY,before:120}),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 3. HOW ONE ORDER RUNS ===================== */
push(
 H1("3.  How one order runs, end to end"),
 P("This is the part that makes the business safe, so read it slowly."),
 PIC("flow.png",640,256),
 BOX([
  P("You only buy after you win. Always.",{b:true,size:24,c:TEAL,after:140}),
  P("There is no warehouse, no stock, and no guessing what will sell. The order legally exists — the town issues a nota de empenho, a binding commitment — before a single real goes out. If you lose a tender, you spent nothing and you are holding nothing.",{after:0})
 ]),
 H2("The words you will need"),
 TBL(["Term","What it means"],
  [["Edital","The tender document. Contains the item list, the deadlines and the rules"],
   ["Pregão / dispensa","The two ways they buy. Pregão is a live online reverse auction; dispensa is a small fast purchase"],
   ["Nota de empenho","The purchase order. Legally commits the town's budget to you"],
   ["Ateste","A town official signs to confirm the delivery arrived correctly. The payment clock starts here"],
   ["Nota fiscal","Your invoice. Must carry the empenho number or the clock restarts"],
   ["Atestado de capacidade","A reference letter from a past buyer. Some tenders ask for one"],
   ["SRP / ata de registro de preços","A price agreed for a year that the town draws on when it needs to"]],
  [2300,7206]),
 H2("The one real operational risk"),
 P([T("Delivery deadlines are short. The measured median is 10 days, and about one tender in three gives 5 days or fewer. ",{}),
    T("The script must reject any tender with a deadline we cannot physically hit.",{b:true}),
    T(" That is a filter, not a problem — but it is a filter we must never forget to apply.")]),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 4. THE PRODUCT ===================== */
push(
 H1("4.  What we sell"),
 P([T("We do not design the kit. ",{b:true}),T("The town hall writes the list and we price whatever it asks for. Here is one real tender we could have bid on — Itaquaquecetuba, São Paulo, 5.000 kits, sold at R$359,05 each.")]),
 PIC("kit.png",640,291),
 H2("There are two kinds of tender, and they are different jobs"),
 TBL(["Tender says","What happens","Our view"],
  [[{t:"Price per KIT",b:true},"We buy all the components, assemble the bags, and ship finished kits","The good one. This is where the margin is — R$11,1 million a year"],
   [{t:"Price per ITEM",b:true},"The town buys 3.000 towels and 3.000 blankets separately and its own staff assemble them","Easier — the wholesaler ships straight to the town. Thinner margin"]],
  [1900,3900,3706]),
 H2("The products we will not touch"),
 BUL([T("Mamadeiras and chupetas ",{b:true}),T("(bottles and dummies) — they need INMETRO certification under Portaria 490/2014. Keep them out of every bid.")]),
 BUL([T("Any tender sold as one undivided lot (",{}),T("lote único",{b:true,i:true}),T(") — measured, these clear at 36–63% of estimate and are where factories dump. We reject them on sight.")]),
 BUL([T("Any kit over about 18 items — too many things to source, too many ways to be caught short.")]),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 5. THE MONEY ===================== */
push(
 H1("5.  Where the money actually is"),
 P("This is the single most important page in the document, and it is the thing we got wrong and then fixed."),
 PIC("margin.png",640,268),
 P([T("Sell the items one by one and you lose. ",{b:true}),
    T("A bodysuit costs R$15,32 in São Paulo and towns pay a median of R$12,66 for one — you are 21% underwater before you start. That is not bad luck: those lines are dominated by manufacturers bidding direct. One of them, BRINK MOBIL, has R$32 million of capital. We cannot beat a factory on a single commodity garment and should never try.")]),
 P([T("Sell the assembled kit and it works. ",{b:true}),
    T("Everybody knows what a bodysuit costs. Nobody publishes a price for “seventeen specified baby things in a bag”, so the price is set by who shows up rather than by a catalogue. And in that band "),
    T("75% of the money is won by small firms our own size",{b:true}),T(" — not by the giants.")]),
 GAP(60),
 BOX([
  P("The rule, in one line",{b:true,size:22,c:CLAY,after:120}),
  P("Sell the bag. Never sell the things in the bag.",{b:true,size:26,c:TEAL,al:AlignmentType.CENTER,after:0})
 ],"FAEDE6",CLAY),
 H1("6.  Where we sell"),
 P([T("We buy in São Paulo, because that is where the wholesalers are and because buying out of state costs about 6 extra points of tax. "),
    T("We sell almost anywhere except São Paulo.",{b:true}),
    T(" São Paulo has the most kit tenders in the country and the worst prices — their suppliers are all local and the bidding is crowded.")]),
 PIC("states.png",640,256),
 P([T("Bid first in ",{}),T("MG · MA · BA · CE · PE · SE · PA · RN",{b:true}),
    T(". De-prioritise SP, ES, MT and MS. The rule underneath it: ",{}),
    T("bid where few people bother to bid, not where it is far away.",{b:true,c:CLAY})]),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 7. NUMBERS ===================== */
push(
 H1("7.  The numbers"),
 P("Target: around R$360.000 of sales a year, which nets roughly R$146.000 — about US$2.340 a month. That needs 21 won tenders a year."),
 TBL(["","Number","What it means"],
  [["Tenders published a year","1.012","The pool"],
   [{t:"Tenders we need to win",b:true},{t:"21",b:true,c:TEAL},{t:"2,1% of them",b:true}],
   ["Sales that produces","R$360.000",""],
   ["Gross margin","~52%","After goods and freight"],
   ["Net after tax and costs","~R$146.000","Simples Anexo I, ~5,65% on sales"],
   [{t:"Per month, take-home",b:true},{t:"≈ US$2.340",b:true,c:TEAL},{t:"The target",b:true}]],
  [3300,2100,4106]),
 H2("Is 21 wins a year realistic?"),
 P("Two real one-person-scale companies are already doing more than that, and we can see their whole record:"),
 TBL(["Company","Where","Tenders won / year","Revenue"],
  [["CONDAFE COMÉRCIO DE ROUPAS","São Paulo EPP, ships to 15 states","44","R$6.135.997"],
   ["AMA COMÉRCIO E SERVIÇOS","16 states","38","—"],
   ["J.J.A. ENXOVAIS","registered Jan 2024, wins in 4 states","—","—"]],
  [3300,3000,1600,1606]),
 P([T("The last one matters most. ",{b:true}),
    T("A micro-company registered in January 2024 is already winning in four states. The playbook is not secret and it is not closed — it is just work nobody is doing carefully.")]),
 H2("The ceiling, if it goes well"),
 TBL(["Stage","Sales","Take-home / month","What limits it"],
  [["Year 1, no supplier credit","R$264.000","≈ US$1.600","Cash"],
   ["Year 1 + a small credit line","R$360.000","≈ US$2.250","Number of wins"],
   ["Year 2, with a supplier account","R$640.000","≈ US$4.760","Number of wins"],
   ["Year 3","R$1.000.000","≈ US$7.550","Number of wins"]],
  [3000,2100,2300,2106]),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 8. MONEY IN / OUT ===================== */
push(
 H1("8.  Money — what you have, what you need"),
 P([T("You have R$15.600. That is enough to start. ",{b:true}),
    T("It is not stock money — it is gap money. You pay the wholesaler around day 11 and the town pays you around day 45, so you are covering a gap of roughly 34 days.")]),
 GAP(60),
 BOX([
  P("The clearest way to think about your capital",{b:true,size:22,c:TEAL,after:130}),
  P("With R$15.600 and no supplier credit you can carry exactly ONE average tender at a time. That caps you at about 8 or 9 orders a year no matter how good the script is.",{after:120}),
  P("Once a wholesaler gives you 28 days to pay, you can carry THREE at once — which is worth more than R$20.000 of borrowed money, and it is free.",{b:true,c:CLAY,after:0})
 ]),
 H2("So the order of operations is: supplier credit first, bank loan second"),
 TBL(["Route","Cost","Orders you can run at once"],
  [["Your own R$15.600, no credit","—","1,0"],
   ["+ R$20.000 borrowed (FGI PEAC)","R$8.200–23.000 a year in interest","2,4"],
   [{t:"28-day supplier terms — free",b:true,c:TEAL},{t:"R$0",b:true,c:TEAL},{t:"2,8–3,2",b:true,c:TEAL}]],
  [3900,3100,2506]),
 P("Most wholesalers say a new buyer must be trading 12 months before they give terms. But at least one says terms are reviewed from the second purchase onward. So: read the credit policy page before the price list, and choose suppliers on their credit rules, not on their prices. That single choice is the difference between year one and year two, and it costs nothing but reading.",{before:100}),
 H2("If we do need to borrow"),
 P([T("FGI PEAC is the only credit instrument in Brazil whose published rules a company with no trading history actually passes — no minimum revenue, no minimum time in business, no personal guarantee required. Offered through 48 banks including Stone, Nubank, Sicoob and Sicredi. ",{}),
    T("Take R$15–20.000, once, and no more.",{b:true}),
    T(" Above about R$35.000 of cash the constraint stops being money and becomes how many tenders we can win, and more money just sits there costing interest.")]),
 P([T("Warning: ",{b:true,c:RED}),T("no FGI PEAC bank publishes its rate. Budget against the only published Brazilian unsecured rate we could find — 2,91% to 6,60% per month — and check the real number before signing anything.")]),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 9. THE RULES ===================== */
push(
 H1("9.  The bidding rules — this is the actual business"),
 P("There is no clever pricing that rescues a tender we should not have entered. The filters are the company. Every one of these has a measured reason behind it."),
 TBL(["#","Rule","Why"],
  [["1","Reject any lote único","They clear at 36–63% of estimate — that is where factories dump stock"],
   ["2","Reject any atestado clause with a NUMBER in it","A percentage or quantity excludes a first-time supplier. A plain atestado clause does not — one prior sale of any size satisfies it"],
   ["3","Reject “conforme modelo do órgão”","Custom spec we cannot source"],
   ["4","Reject kits over ~18 items","Too many sourcing points to be safe on"],
   ["5","Reject deadlines we cannot physically hit","One in three tenders gives 5 days or fewer"],
   ["6","Check the buyer's payment record before bidding","Free, one web call. Some towns have paid 0% of last year's invoices"],
   ["7","Check whether the line is under R$80.000","Those are legally reserved for small companies only — less competition"],
   ["8","Price every line from our own cost table, spec by spec","A “baby bath” at 17 litres and at 24 litres are different products with a 36-point margin difference"],
   ["9","Log every bid — win or lose","See below"]],
  [500,3400,5606]),
 GAP(80),
 BOX([
  P("The one asset that compounds",{b:true,size:22,c:TEAL,after:130}),
  P("Brazil publishes who WON a tender. It never publishes who lost, or what they bid. That means nobody — not us, not any competitor, not the R$4.000-a-year software vendors — can know the real win rate or the real losing prices.",{after:120}),
  P("Except us, about our own bids. From day one, log: date, town, item, spec, quantity, our cost, our bid, result, and the winning price when we lose. After six months that file tells us exactly where to bid, and it is a file nobody can buy.",{b:true,after:0})
 ]),
 P([T("Worth knowing: there are already companies selling tender-alert software (SIGA Pregão charges R$3.997 a year). They sell what the STATE paid. ",{}),
    T("None of them can sell what WE pay, because that is our own invoice.",{b:true}),
    T(" The cost side is the only part of this nobody can package and resell.")],{before:120}),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 10. TO DO ===================== */
push(
 H1("10.  Everything that needs doing"),
 P("In order. Do not skip ahead — step 0 decides whether the rest is worth doing at all."),

 H2("STEP 0 — this week, costs nothing"),
 BOX([
  P("Price the other 11 items in the kit.",{b:true,size:23,c:TEAL,after:120}),
  P("We have verified São Paulo prices for 6 of the 17 items. The missing ones — above all the backpack, the most expensive item in the kit — have no price anywhere in our research. Spend an afternoon on the Brás wholesalers' websites and fill in the table.",{after:120}),
  P([T("Bar, decided in advance: total under R$200 → start the business now. Over R$230 → we need a proper supplier account before anything else.",{b:true,c:CLAY})],{after:0})
 ]),

 H2("STEP 1 — open the company  (~R$1.500–2.500)"),
 TBL(["Task","Cost","Note"],
  [["Hire a contador","R$200–400 / month","Non-negotiable. Handles Simples, notas fiscais, the opening balance sheet"],
   ["Open an ME on Simples Nacional, Anexo I","~R$1.000 one-off","Tax is 4,0% of sales up to R$180k, 5,65% up to R$360k"],
   [{t:"Register SEVERAL CNAEs",b:true},"included","Vestuário, enxoval, higiene pessoal, brinquedos. A tender can disqualify you if your registered objeto social does not cover what it is buying. This is a real and avoidable loss"],
   ["Capital social R$20–30.000 integralizado","your own money","Not a fee. It caps what any tender may legally demand of you and makes the opening balance sheet pass"],
   ["Certificado digital e-CNPJ A1","~R$200–300 / year","Required to bid"],
   ["Conta PJ","free","Cora or Nubank PJ"]],
  [3000,1800,4706]),
 P("Two things we were worried about turn out not to be problems, both settled in law: a first-year company cannot be required to show a balanço patrimonial for ready-delivery goods (Decreto 8.538/2015, art. 3), and no tender may demand a minimum past revenue (Lei 14.133, art. 69 §2).",{size:19,c:GREY,before:100}),

 H2("STEP 2 — get registered to bid  (free)"),
 P("Five free registrations reach 74% of kit tenders. Eight reach 83%."),
 BUL("Compras.gov.br / SICAF  ·  Portal de Compras Públicas  ·  BLL  ·  BNC  ·  Licitanet"),
 P("Bidding itself is free on Compras.gov.br. BLL charges 1,5% capped at R$600 — and only if we win.",{size:19,c:GREY}),

 H2("STEP 3 — the supplier account  (free, and it is the real gate)"),
 P("Fifteen emails to São Paulo wholesalers. Ask for a faturado price on specific items, whether they do venda à ordem (shipping straight to our customer), and what their credit terms are for a new buyer."),
 TBL(["Item","Price we need"],
  [["Body","≤ R$8,40"],["Macacão / pagão","≤ R$13,70"],["Toalha com capuz","≤ R$10,50"],
   ["Banheira 24 L","≤ R$14,85"],["Manta","≤ R$10,00"],[{t:"Mochila",b:true},{t:"≤ R$25,00  — no price found anywhere yet",b:true,c:CLAY}]],
  [4700,4806]),
 P("Bar: three of fifteen answering with a number that clears. Below that, we are a smaller business than this document describes and we should say so out loud.",{b:true,before:100}),

 H2("STEP 4 — the machine  (~R$2.000–4.000, or your own time)"),
 BUL("A script that reads the national tender site every morning, pulls the item lists, applies the nine rules, prices each line against our cost table, and produces a short list of tenders worth bidding on."),
 BUL("Runs on a R$30/month server. No subscriptions — a per-seat software subscription would cost more per year than our entire startup budget."),
 BUL("Builds the bid log from the first day."),

 H2("STEP 5 — the website  (~R$300 first year)"),
 P("We need one, but not for the reason websites usually exist. Nobody will find us through it. It exists so that a procurement officer, a wholesaler's credit department and a bank can check in ten seconds that we are real."),
 TBL(["Must have","Must NOT have"],
  [["Company name, CNPJ, full address","A shop or any prices"],
   ["What we supply, in one paragraph","Any founder photo, name or bio"],
   ["A products page — the kit and its components","Any social media links"],
   ["A licitações page: “we supply the public sector”","A blog, a newsletter, a chatbot"],
   ["One email address and one phone number","Anything aimed at mothers"]],
  [4700,4806]),
 P("One page, calm, in the brand colours. A domain is about R$40/year and a one-page site can be built free. Budget R$300 and half a day.",{size:19,c:GREY,before:100}),

 H2("STEP 6 — first bids"),
 BUL([T("Start with ",{}),T("dispensa",{b:true,i:true}),T(" — the small fast purchases. Median R$281, decided in days, lowest capital at risk.")]),
 BUL([T("The goal of the first few is not profit. It is the ",{}),T("atestado de capacidade técnica",{b:true}),T(" — a reference letter from a completed delivery, which unlocks the half of the market that asks for one. One sale of any size does it, and a private customer can issue it too.")]),
 BUL("Then move up to assembled kits."),

 H2("STEP 7 — financing, only if step 3 fails"),
 BUL("Apply for FGI PEAC, R$15–20.000, through Stone / Nubank / Sicoob / Sicredi."),
 BUL("Do this only after supplier terms have been asked for and refused. Terms are worth more and cost nothing."),
 new Paragraph({children:[new PageBreak()]})
);

/* ===================== 11. RISKS ===================== */
push(
 H1("11.  What we still do not know"),
 P("None of these is a reason not to start. All four are answerable inside about two months for under R$5.000, and we should be honest that they are open."),
 TBL(["Open question","Why it matters","How we close it"],
  [[{t:"11 of the 17 kit items have no verified price",b:true},"45% of our cost estimate is a guess, and the worst gap is the backpack — the most expensive item","One afternoon on wholesaler websites. This is STEP 0"],
   [{t:"One town is a third of the good business",b:true},"Coari, in the Amazon, is 34,8% of everything we could win at a real margin. If they do not buy again, the market shrinks","Plan on the number excluding them and treat a repeat as a bonus"],
   [{t:"Freight is not quoted",b:true},"A baby bath is big and light — it ships on volume, not weight. Every freight company refuses to quote without a contract","Get one real quote before bidding anything heading north"],
   [{t:"Nobody can know the win rate",b:true},"Brazil publishes winners, never losers. We cannot know how many bids make one win until we bid","Bid small first, log everything, and know the answer in 90 days"]],
  [2900,3700,2906]),
 GAP(120),
 BOX([
  P("And one piece of good news hiding in that last risk",{b:true,size:22,c:TEAL,after:130}),
  P("Because we bid on whole tenders worth around R$31.000 rather than tiny R$6.000 lines, the win rate almost stops mattering. Even if only one bid in twenty wins, that is 36 hours of work a month — comfortably inside what you want to work. On small lines the same win rate would need 138 hours a month and the business would be impossible.",{after:120}),
  P("Bidding bigger tenders does not raise the return. It removes our dependence on the one number nobody can measure.",{b:true,c:CLAY,after:0})
 ]),
 H1("12.  The decision this week"),
 P([T("Nothing above requires a commitment yet. ",{}),
    T("One afternoon pricing eleven items decides whether this is a business or not.",{b:true,c:TEAL,size:23})]),
 GAP(60),
 TBL(["If the kit costs…","Then…"],
  [[{t:"under R$200",b:true,c:TEAL},{t:"The margin is real at prices we can already buy at. Open the company and start.",b:true}],
   [{t:"R$200–230",b:true},"It works but it is tight. Open the company and make the supplier account the first priority."],
   [{t:"over R$230",b:true,c:CLAY},"Do not open anything yet. Send the fifteen supplier emails first and decide on the answers."]],
  [2600,6906]),
 GAP(200),
 P("Sources and every calculation behind this document: THE_KIT_DESK.md in the repository.",
   {al:AlignmentType.CENTER,size:18,c:GREY,i:true,after:0})
);

const doc=new Document({
 creator:"ACOLHE",title:"ACOLHE — business overview",
 numbering:{config:[
  {reference:"bul",levels:[{level:0,format:LevelFormat.BULLET,text:"•",alignment:AlignmentType.LEFT,
    style:{paragraph:{indent:{left:340,hanging:200}},run:{color:TEAL}}}]},
  {reference:"num",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,
    style:{paragraph:{indent:{left:340,hanging:200}},run:{color:TEAL,bold:true}}}]}]},
 styles:{default:{document:{run:{font:"Calibri",size:21,color:INK}}}},
 sections:[{properties:{page:{margin:{top:1100,bottom:1000,left:1200,right:1200}}},children:body}]
});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("ACOLHE_Business_Overview.docx",b);console.log("written",b.length)});
