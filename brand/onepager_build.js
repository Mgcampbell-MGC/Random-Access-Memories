const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,ImageRun,Table,TableRow,TableCell,WidthType,
 AlignmentType,BorderStyle,ShadingType,LevelFormat}=require('docx');

const TEAL="1F4E4A", CLAY="A85434", INK="2B2B2B", GREY="5E5B55", CREAM="F4F1EB";
const W=9866;                      // content width (A4 minus 1020 twip margins)
const S=24;                        // 12pt body

const T=(t,o={})=>new TextRun({text:t,font:"Calibri",size:o.size||S,bold:o.b,italics:o.i,color:o.c||INK});
const P=(t,o={})=>new Paragraph({alignment:o.al,spacing:{before:o.before??0,after:o.after??100,line:264},
  children:Array.isArray(t)?t:[T(t,o)]});
const H=(t,o={})=>new Paragraph({keepNext:true,spacing:{before:o.before??200,after:70},
  children:[new TextRun({text:t,font:"Calibri",size:25,bold:true,color:TEAL})]});
const BUL=t=>new Paragraph({numbering:{reference:"b",level:0},spacing:{after:46,line:258},
  children:Array.isArray(t)?t:[T(t)]});

const BOX=(lines,fill=CREAM,edge="C9C0B0")=>new Table({columnWidths:[W],width:{size:W,type:WidthType.DXA},
  borders:{top:{style:BorderStyle.SINGLE,size:10,color:edge},bottom:{style:BorderStyle.SINGLE,size:10,color:edge},
    left:{style:BorderStyle.SINGLE,size:10,color:edge},right:{style:BorderStyle.SINGLE,size:10,color:edge},
    insideHorizontal:{style:BorderStyle.NONE},insideVertical:{style:BorderStyle.NONE}},
  rows:[new TableRow({children:[new TableCell({width:{size:W,type:WidthType.DXA},
    shading:{type:ShadingType.CLEAR,fill},margins:{top:110,bottom:110,left:150,right:150},children:lines})]})]});

function TBL(rows,widths,o={}){
  const cell=(c,w,alt)=>{const s=typeof c==='object'?c:{t:c};
    return new TableCell({width:{size:w,type:WidthType.DXA},
      shading:alt?{type:ShadingType.CLEAR,fill:"F7F5F0"}:undefined,
      margins:{top:48,bottom:48,left:100,right:100},
      children:[new Paragraph({spacing:{after:0,line:250},alignment:s.al,
        children:[new TextRun({text:s.t,font:"Calibri",size:s.size||23,bold:s.b,color:s.c||INK})]})]});};
  return new Table({columnWidths:widths,width:{size:widths.reduce((a,b)=>a+b,0),type:WidthType.DXA},
    borders:{top:{style:BorderStyle.SINGLE,size:4,color:"D6CEC0"},bottom:{style:BorderStyle.SINGLE,size:4,color:"D6CEC0"},
      left:{style:BorderStyle.NONE},right:{style:BorderStyle.NONE},
      insideHorizontal:{style:BorderStyle.SINGLE,size:2,color:"E8E2D7"},insideVertical:{style:BorderStyle.NONE}},
    rows:rows.map((r,i)=>new TableRow({cantSplit:true,children:r.map(c=>cell(c,widths[r.indexOf(c)]??widths[0],i%2===1))}))});
}
const GAP=(n=100)=>new Paragraph({spacing:{after:n},children:[]});

const body=[];
const push=(...x)=>x.forEach(i=>body.push(i));

push(
 new Paragraph({spacing:{after:26},children:[
   new TextRun({text:"ACOLHE",font:"Calibri",size:26,bold:true,color:TEAL,characterSpacing:80}),
   new TextRun({text:"   enxovais e suprimentos para o setor público",font:"Calibri",size:18,color:CLAY})]}),
 new Paragraph({spacing:{after:180},border:{bottom:{style:BorderStyle.SINGLE,size:8,color:TEAL}},
   children:[new TextRun({text:"O negócio em uma leitura",font:"Calibri",size:32,bold:true,color:TEAL})]}),

 H("A ideia",{before:0}),
 P("Prefeituras entregam um kit enxoval às mães atendidas pela assistência social. Não é um presente que elas escolhem dar: é um benefício eventual que a lei obriga. A demanda vem de nascimentos e de norma — não de marketing."),
 P([T("Para comprar esses kits, a prefeitura tem de abrir licitação. E a "),T("Lei 14.133, art. 54",{b:true}),
    T(" obriga a publicar o edital inteiro — com a lista exata dos itens — num site nacional, de graça, antes de comprar. São cerca de "),
    T("quatro licitações de kit por dia útil",{b:true}),T(", no Brasil todo.")]),
 BOX([P([T("Esse é o canal de vendas inteiro, e ele é uma lei. ",{b:true,c:TEAL}),
   T("Ninguém compra esse canal de você e ninguém desliga. Você nunca procura cliente: o comprador é obrigado a se anunciar.")],{after:0})]),

 H("Como funciona um pedido"),
 TBL([
  [{t:"Dia 0",b:true,c:TEAL},"A prefeitura publica o edital com a lista de itens"],
  [{t:"Dia 0",b:true,c:TEAL},"Seu programa lê, precifica cada linha e diz se vale a pena"],
  [{t:"Dia 1",b:true,c:TEAL},"Você dá o lance. Custa R$ 0"],
  [{t:"Dia 10",b:true,c:CLAY},"O pregão fecha. Ganhou ou não ganhou"],
  [{t:"Dia 11",b:true,c:CLAY},"SÓ AGORA você compra a mercadoria"],
  [{t:"Dia 15",b:true,c:TEAL},"Monta, embala e despacha para o endereço do edital"],
  [{t:"Dia 45",b:true,c:TEAL},"Nota atestada, prefeitura paga"]],[1250,8616]),
 P([T("Você nunca compra nada por aposta. ",{b:true}),
    T("Se perder, gastou R$ 0 e não tem estoque. Sem galpão e sem mercadoria parada.")],{before:110}),

 H("O que você vende"),
 P([T("O kit montado — nunca os itens soltos. "),
    T("Todo mundo sabe quanto custa um body; ninguém publica preço de “17 itens de bebê dentro de uma bolsa”. "),
    T("Um kit real de 17 itens foi vendido a R$ 359. A mercadoria custa R$ 169 a R$ 230. ",{b:true}),
    T("A margem só existe no kit inteiro: vendidos um a um, quase todos dão prejuízo — nessas linhas quem disputa é fábrica.")]),

 H("O que você faz, na prática"),
 BUL("O programa varre os editais e calcula. Você decide em quais entrar."),
 BUL("Dá o lance na plataforma — pregão eletrônico, tudo por tela."),
 BUL("Ganhou: manda o pedido aos atacadistas do Brás, confere e despacha."),
 BUL("Emite a nota fiscal com o número do empenho e acompanha o pagamento."),
 BUL([T("Registra cada lance numa planilha: seu custo, seu lance, quem ganhou e por quanto. "),
      T("Esse arquivo é o único ativo que ninguém consegue comprar.",{b:true})]),
 P("Sem funcionário, sem cliente para segurar, sem reunião, sem câmera. É escrito, é por tela, e cada contrato termina quando a entrega termina.",{before:80}),

 H("Os números"),
 TBL([
  ["Licitações de kit publicadas por ano",{t:"1.012",b:true,al:AlignmentType.RIGHT}],
  [{t:"Quantas você precisa ganhar",b:true},{t:"21  (2,1%)",b:true,c:TEAL,al:AlignmentType.RIGHT}],
  ["Faturamento",{t:"R$ 360.000",al:AlignmentType.RIGHT}],
  [{t:"Lucro líquido no ano",b:true},{t:"R$ 146.000  ·  US$ 2.340/mês",b:true,c:TEAL,al:AlignmentType.RIGHT}]],
  [5500,4366]),
 P([T("Duas empresas de uma pessoa só já fazem mais que isso hoje: a CONDAFE, de São Paulo, ganha 44 licitações por ano e entrega em 15 estados; e uma microempresa aberta em janeiro de 2024 já ganha em quatro estados. "),
    T("O caminho não é secreto — é só trabalho que quase ninguém faz com cuidado.",{b:true})],{before:110}),

 H("O dinheiro"),
 P([T("Você tem R$ 15.600 e isso dá para começar. Não é dinheiro de estoque: é dinheiro de intervalo. "),
    T("Você paga o atacadista por volta do dia 11 e a prefeitura paga por volta do dia 45 — são uns 34 dias a cobrir. "),
    T("Sem prazo de fornecedor você segura um pedido por vez; com 28 dias de prazo, três. Prazo de fornecedor vale mais que empréstimo e é de graça.",{b:true})]),

 H("O que ainda não sabemos"),
 P([T("Falta preço confirmado de 11 dos 17 itens (o pior é a mochila) · uma única cidade responde por um terço do mercado bom · o frete de volume ainda não foi cotado · e quantos lances dão uma vitória ninguém sabe até começar a dar lance. "),
    T("Nada disso impede começar, e tudo isso se resolve em dois meses por menos de R$ 5.000.",{b:true})]),

 GAP(60),
 BOX([
   P("O primeiro passo é uma tarde de trabalho",{b:true,size:26,c:TEAL,after:80}),
   P("Levantar o preço dos outros 11 itens nos atacadistas do Brás. A conta decide sozinha:",{after:80}),
   P([T("Total abaixo de R$ 200",{b:true,c:TEAL}),T("  →  a margem existe com o preço que já conseguimos hoje. Abre a empresa e começa.")],{after:50}),
   P([T("Total acima de R$ 230",{b:true,c:CLAY}),T("  →  não abre nada ainda. Primeiro os quinze e-mails aos fornecedores, e decide com a resposta na mão.")],{after:0})],
  "EFE8DC","C96F4A")
);

const doc=new Document({creator:"ACOLHE",title:"ACOLHE — o negócio em uma leitura",
 numbering:{config:[{reference:"b",levels:[{level:0,format:LevelFormat.BULLET,text:"•",
   alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:300,hanging:180}},run:{color:TEAL}}}]}]},
 styles:{default:{document:{run:{font:"Calibri",size:S,color:INK}}}},
 sections:[{properties:{page:{margin:{top:900,bottom:820,left:1020,right:1020}}},children:body}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("ACOLHE_Uma_Leitura.docx",b);console.log("written",b.length)});
