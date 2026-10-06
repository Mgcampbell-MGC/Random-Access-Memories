/* HOLOFOTE · LIVRO DA MARCA — pranchas 1920 × 1080 (01_MARCA/livro/). Requer holofote.js, pilha.js, pecas.js.
 * Grade: margem 96 px, 12 colunas de 122 px, calha 24 px, linhas de base na grade de 8 px.
 * As pranchas obedecem às próprias regras: toda linha enche a medida (até o texto corrido, ver HF.corrido),
 * cada fonte é uma voz, ela é a maior palavra. Espaços reservados de render: HF.reserva → placeholders.json.
 */
(function () {
  const S = HF.S;
  const X0 = 96, X1 = 1824, MED = X1 - X0, G = 24, CW = (MED - 11 * G) / 12;
  const col = (a, b) => [X0 + a * (CW + G), X0 + b * (CW + G) + CW];
  const LV = (HF.livro = {});
  const NS = 'http://www.w3.org/2000/svg';
  const g8 = (v) => Math.round(v / 8) * 8;
  let TINTA = 'preto';

  /* ---------- texto corrido justificado: TODA linha enche a medida, inclusive a última.
     Procura o corpo (±6 %) em que a quebra gananciosa deixa a última linha ≥ 80 % cheia e nenhum espaço entre
     palavras passa de 0,9 em; depois cada linha é fechada na borda da tinta por word-spacing (±0,5 px). */
  HF.corrido = function (parent, texto, x0, x1, base0, o) {
    /* Running text, ragged right (review 6 Oct 2026: forced justification of body text opened rivers on nine
       boards; "every line fills its measure" is the DISPLAY rule, not the body rule). Greedy breaks at the asked
       size, a one-letter word never ends a line (a, e, o, é, à… travel with the next word), the last line never
       holds a single word. If o.maxLinhas cannot be met at the asked size, the size steps down 1 % at a time. */
    const medida = x1 - x0;
    const sBase = Object.assign({ f: o.f || 'C', cor: o.cor || TINTA }, o.estilo || {});
    sBase.fs = o.fs || HF.fsDeCap(sBase.f, o.cap);
    const cru = texto.split(/[ \t\n]+/).filter(Boolean), pal = [];   // \u00a0 no texto = espaço que não quebra (3,2\u00a0d)
    for (let i = 0; i < cru.length; i++) {
      if (/^[aeoéàAEOÉÀ]$/.test(cru[i]) && i < cru.length - 1) { pal.push(cru[i] + '\u00a0' + cru[i + 1]); i++; } else pal.push(cru[i]);
    }
    const larg = (t, fs) => { const e = HF.texto(parent, Object.assign({}, sBase, { t, fs })); const w = e.inkW; e.el.remove(); return w; };
    const quebrar = (fs) => {
      const L = []; let cur = [];
      pal.forEach((p) => {
        const tenta = cur.concat([p]);
        if (cur.length && larg(tenta.join(' '), fs) > medida) { L.push(cur); cur = [p]; } else cur = tenta;
      });
      L.push(cur);
      if (L.length > 1 && L[L.length - 1].length < 2 && L[L.length - 2].length > 2) L[L.length - 1].unshift(L[L.length - 2].pop());
      return L;
    };
    let fs = sBase.fs, L = quebrar(fs);
    for (let n = 0; o.maxLinhas && L.length > o.maxLinhas && n < 15; n++) { fs *= 0.99; L = quebrar(fs); }
    const passo = o.passo || g8(HF.capPx(sBase) * 1.75);
    const linhas = [];
    L.forEach((l, i) => {
      const t = l.join(' ');
      const e = HF.texto(parent, Object.assign({}, sBase, { t, fs }));
      HF.posicionar(e, x0, base0 + i * passo, 'left');
      (window.HF_QA = window.HF_QA || []).push({ item: 'corrido: ' + t.slice(0, 24), erro: Math.max(0, e.inkW - medida) });
      linhas.push(e);
    });
    return { linhas, fim: base0 + (linhas.length - 1) * passo, passo };
  };

  /* ---------- peças da prancha */
  const fundo = (cor) => { HF.quadro(1920, 1080, cor); TINTA = HF.tinta[cor] || 'preto'; return TINTA; };
  const cab = (n, titulo, cor) => {
    const t = fundo(cor);
    HF.dividida(document.body, S({ t: 'HOLOFOTE · LIVRO DA MARCA', f: 'C', cap: 15, lsEm: 0.14, cor: t }),
      S({ t: String(n).padStart(2, '0') + ' · ' + titulo, f: 'C', cap: 15, lsEm: 0.14, cor: t, tnum: true }), X0, X1, 80);
    return t;
  };
  const cheia = (s, x0, x1, base, modo) => HF.cheia(document.body, S(s), x0, x1, base, modo || 'tamanho');
  const div = (e, d, x0, x1, base) => HF.dividida(document.body, S(e), S(d), x0, x1, base);
  const regua = (x0, x1, y, esp, cor) => HF.regua(document.body, x0, x1, y, esp || 2, cor || TINTA);
  // rótulo de seção: versal da Produção a +140 e um fio até o fim da medida (a linha enche a medida pelo fio, nunca
  // por tracking aberto)
  const rot = (t, x0, x1, base, cor) => {
    const o = HF.texto(document.body, S({ t, f: 'C', cap: 15, lsEm: 0.14, cor: cor || TINTA }));
    HF.posicionar(o, x0, base, 'left');
    if (o.inkX1 + 24 < x1) HF.regua(document.body, o.inkX1 + 20, x1, base - 6, 1.5, cor || TINTA);
    return o;
  };
  const etiqueta = (t, x, base, cor, align) => { const o = HF.texto(document.body, S({ t, f: 'C', cap: 15, lsEm: 0.14, cor: cor || TINTA })); HF.posicionar(o, x, base, align || 'left'); return o; };
  const img = (src, x, y, w, h, fit, estilo) => {
    const i = document.createElement('img');
    i.src = src;
    Object.assign(i.style, { position: 'absolute', left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px', objectFit: fit || 'cover' }, estilo || {});
    document.body.appendChild(i);
    return i;
  };
  const caixa = (x, y, w, h, st) => HF.caixa(document.body, x, y, w, h, st);
  const svg = (x, y, w, h) => HF.svg(document.body, x, y, w, h, `0 0 ${w} ${h}`);
  const el = (s, tag, at) => { const e = document.createElementNS(NS, tag); Object.entries(at).forEach(([k, v]) => e.setAttribute(k, v)); s.appendChild(e); return e; };
  // marcas de certo/errado (vetor: a Special Gothic não tem ✓)
  const certo = (x, y, d, cor) => { const s = svg(x, y, d, d); el(s, 'path', { d: `M${d * 0.16} ${d * 0.54} L${d * 0.4} ${d * 0.78} L${d * 0.86} ${d * 0.24}`, fill: 'none', stroke: HF.cor[cor] || cor, 'stroke-width': d * 0.13, 'stroke-linecap': 'square' }); };
  const errado = (x, y, d, cor) => { const s = svg(x, y, d, d); el(s, 'path', { d: `M${d * 0.2} ${d * 0.2} L${d * 0.8} ${d * 0.8} M${d * 0.8} ${d * 0.2} L${d * 0.2} ${d * 0.8}`, fill: 'none', stroke: HF.cor[cor] || cor, 'stroke-width': d * 0.13, 'stroke-linecap': 'square' }); };
  const K = (D, p) => D.kit + p;

  const T = (s, x, base, al, pai) => { const o = HF.texto(pai || document.body, S(s)); HF.posicionar(o, x, base, al || 'left'); return o; };
  const corpo = (texto, x0, x1, base, cap, extra) => HF.corrido(document.body, texto, x0, x1, base,
    Object.assign({ f: 'V', estilo: { wght: 400, wdth: 100 }, cap: cap || 18, passo: g8((cap || 18) * 1.8) }, extra || {}));

  /* ================= 01 · CAPA: o wordmark é o palco; o O aceso e a sua poça desenham O FOCO na proporção certa */
  LV[1] = (D) => {
    fundo('preto');
    const t = 'papel', WM = window.HF_WORDMARK;
    div({ t: 'LIVRO DA MARCA', f: 'C', cap: 18, lsEm: 0.14, cor: t }, { t: 'DIA DAS MÃES · 09.05.2027', f: 'C', cap: 18, lsEm: 0.14, cor: t, tnum: true }, X0, X1, 104);
    const base = 560;
    const wm = HF.wordmark(document.body, { x: X0, baseline: base, largura: MED, ink: 'papel', lamp: 'amarelo' });
    const k = wm.k, d = 734 * k, cx = X0 + (4466 - WM.inkX0) * k, fundoO = base + 12 * k;
    const s = svg(0, 0, 1920, 1080);
    const F = HF.FOCO;   // O FOCO redesenhado (revisão do CCO, 6 out 2026): poça 3,2 d × 0,5 d, vão 1,2 d
    el(s, 'ellipse', { cx, cy: fundoO + F.vao * d + F.alt * d / 2, rx: F.larg * d / 2, ry: F.alt * d / 2, fill: HF.cor.amarelo });
    div({ t: 'holofote nela.', f: 'X', cap: 40, lsEm: -0.01, cor: t }, { t: 'A TURNÊ · CASO DEMONSTRATIVO · SOL ESTÚDIO', f: 'C', cap: 18, lsEm: 0.14, cor: t }, X0, X1, 1000);
  };

  /* ================= 02 · A IDEIA */
  LV[2] = (D) => {
    const t = cab(2, 'A IDEIA', 'papel');
    const [a0, a1] = col(0, 7);
    const l1 = cheia({ t: 'ELA APLAUDIU DE PÉ', f: 'X', cap: 90, lsEm: -0.01, cor: t }, a0, a1, 264);
    const l2 = cheia({ t: 'O SEU PIOR SHOW.', f: 'X', cap: 90, lsEm: -0.01, cor: t }, a0, a1, 0);
    HF.posicionar(l2, a0, g8(264 + 24 + HF.capPx(l2.s)), 'left');
    const y0 = g8(l2.baseline + 104);
    rot('A IDEIA DA MARCA', a0, a1, y0);
    const c = corpo('HOLOFOTE inverte o palco: no Dia das Mães, a atração é ela e quem aplaude é você. Uma marca de velas que vira o holofote ao contrário. Por um dia ela é o show, e você é a plateia.',
      a0, a1, y0 + 64, 30, { estilo: { wght: 500, wdth: 100 }, passo: 48 });
    const y2 = g8(c.fim + 88);
    regua(a0, a1, y2 - 44, 2);
    // o Locutor é CAIXA ALTA em toda parte; só a assinatura fica em caixa baixa (revisão do CCO, 6 out 2026). A verdade
    // do produto em versal não cabe numa linha com o rótulo: a segunda frase desce para a linha de baixo, alinhada à
    // direita na coluna dos valores (continuação de tabela, sem pontilhado)
    const linhas = [['PLATAFORMA', 'MÃE AO VIVO'], ['CHAMADA', 'SUA VEZ.'], ['VERDADE DO PRODUTO', 'O MENOR HOLOFOTE DO BRASIL.'],
      [null, 'PRA MAIOR ATRAÇÃO.'], ['ASSINATURA', 'holofote nela.']];
    linhas.forEach((l, i) => {
      const v = S({ t: l[1], f: 'X', cap: 20, lsEm: -0.01, cor: t });
      if (l[0]) HF.pontilhada(document.body, S({ t: l[0], f: 'C', cap: 20, lsEm: 0.1, cor: t }), v, a0, a1, y2 + i * 40,
        { passo: 9, folga: 10, fs: HF.fsDeCap('C', 20) });
      else T(v, a1, y2 + i * 40, 'right');
    });
    const [b0, b1] = col(8, 11);
    const h = 864, w = Math.round(h * 9 / 16);
    HF.reserva(document.body, { id: 'KV-01', x: b1 - w, y: 128, w, h, fundo: 'preto', tinta: 'papel', rotulo: 'RENDER', nota: 'KV-01 · 9:16 · MÃE AO VIVO',
      conteudo: 'KV-01 9:16 (§E.1), vela acesa no palco, com o lineup' });
    div({ t: 'KV-01 · O PALCO', f: 'C', cap: 15, lsEm: 0.14, cor: t }, { t: '9:16', f: 'C', cap: 15, lsEm: 0.14, cor: t, tnum: true }, b1 - w, b1, 1032);
  };

  /* ================= 03 · O INSIGHT */
  LV[3] = (D) => {
    const t = cab(3, 'O INSIGHT', 'preto');
    const l1 = cheia({ t: 'ELA FOI SUA PRIMEIRA FÃ.', f: 'X', cap: 90, lsEm: -0.01, cor: 'amarelo' }, X0, X1, 264);
    const [a0, a1] = col(0, 7);
    const l2 = cheia({ t: 'VOCÊ NUNCA FOI FÃ DELA.', f: 'X', cap: 60, lsEm: -0.01, cor: t }, a0, a1, 0);
    const b2 = g8(264 + 40 + HF.topoTinta(l2.s));
    HF.posicionar(l2, a0, b2, 'left');
    T({ t: 'REGRA 1, NUMA FRASE SÓ: ELA, A MAIOR. VOCÊ, A MENOR.', f: 'C', cap: 15, lsEm: 0.14, cor: 'amarelo' }, X1, b2, 'right');
    const cols = [
      ['01 · O LADO DELA', 'a origem', 'O primeiro palco de todo brasileiro foi o show de Dia das Mães da escola: fantasia de girassol, fundo de TNT, um passo esquecido, um tchau para a mãe errada. Ela estava na primeira fila, filmando com o dedo na lente.'],
      ['02 · O SEU LADO', 'a metáfora', 'A geração Z é a mais fluente em fandom do Brasil. Acampa 48 horas na porta do estádio, sabe a setlist de cor e briga pela grade. A HOLOFOTE entrega a essa geração um papel que ela ensaiou a vida toda, com uma nova atração.'],
      ['03 · A LÍNGUA', 'longe dos holofotes', 'O português descreve a vida inteira dela com uma expressão: longe dos holofotes. A marca é a resposta literal: um holofote do tamanho de um copo, apontado para ela, no único domingo em que o show é dela.'],
    ];
    cols.forEach((c, i) => {
      const [x0, x1] = col(i * 4, i * 4 + 3);
      const y = 560;
      regua(x0, x1, y - 44, 2, t);
      div({ t: c[0], f: 'C', cap: 16, lsEm: 0.14, cor: t }, { t: c[1], f: 'S', x: 14, cor: 'amarelo' }, x0, x1, y);
      corpo(c[2], x0, x1, y + 64, 20, { passo: 40, cor: t });
    });
  };

  /* ================= 04 · AS TRÊS VOZES */
  LV[4] = (D) => {
    const t = cab(4, 'AS TRÊS VOZES', 'papel');
    cheia({ t: 'CADA FONTE É UMA VOZ.', f: 'X', cap: 64, lsEm: -0.01, cor: t }, X0, X1, 208);
    const vozes = [
      { n: { t: 'O LOCUTOR', f: 'X', cap: 52, lsEm: -0.01 }, num: '01', quem: 'A MARCA NO VOLUME MÁXIMO',
        fonte: 'Special Gothic Expanded One, caixa alta, tracking de −10 a 0. Frases curtas, declarativas, cerimoniosas.',
        ex: [[{ t: 'A ATRAÇÃO É ELA.', f: 'X', cap: 30, lsEm: -0.01 }, 'FILME'], [{ t: 'MÃE AO VIVO', f: 'X', cap: 30, lsEm: -0.01 }, 'PLATAFORMA'], [{ t: 'SUA VEZ.', f: 'X', cap: 30, lsEm: -0.01 }, 'CHAMADA']] },
      { n: { t: 'A PRODUÇÃO', f: 'C', cap: 52, lsEm: 0.02 }, num: '02', quem: 'A EQUIPE: PRÁTICA, DE BASTIDOR',
        fonte: 'Special Gothic Condensed One, caixa baixa a 0 ou versal de +80 a +120. Segurança, preço e instrução moram aqui.',
        ex: [[{ t: 'sessões de até 4 h.', f: 'C', cap: 34 }, 'SETLIST'], [{ t: 'reservar ingresso', f: 'C', cap: 34 }, 'BOTÃO DA LOJA'], [{ t: 'PESO LÍQUIDO 200 g', f: 'C', cap: 34, lsEm: 0.06, tnum: true }, 'COPO']] },
      { n: { t: 'a fã', f: 'S', x: 40 }, num: '03', quem: 'VOCÊ, FILHO OU FILHA: CARINHO, CAIXA BAIXA',
        fonte: 'Shantell Sans 500, INFM 60. Só caixa baixa, até seis palavras, um sinal de pontuação, uma vez por peça.',
        ex: [[{ t: '(girassol, 2007)', f: 'S', x: 25 }, 'C03'], [{ t: 'abertura: você', f: 'S', x: 25 }, 'O CARTAZ'], [{ t: 'ela fica aqui.', f: 'S', x: 25 }, 'A TAMPA']] },
    ];
    vozes.forEach((v, i) => {
      const [x0, x1] = col(i * 4, i * 4 + 3);
      regua(x0, x1, 280, 2);
      div(Object.assign({ cor: t }, v.n), { t: v.num, f: 'C', cap: 20, lsEm: 0.1, cor: t, tnum: true }, x0, x1, 360);
      rot(v.quem, x0, x1, 416);
      corpo(v.fonte, x0, x1, 464, 16, { passo: 30 });
      v.ex.forEach((e, j) => {
        const y = 640 + j * 104;
        regua(x0, x1, y - 64, 1);
        div(Object.assign({ cor: t }, e[0]), { t: e[1], f: 'C', cap: 14, lsEm: 0.12, cor: t }, x0, x1, y);
      });
    });
    regua(X0, X1, 952, 2);
    div({ t: 'DUAS EXCEÇÕES: “holofote nela.” é o Locutor em caixa baixa.', f: 'C', cap: 18, cor: t },
      { t: 'O único ponto de exclamação da marca mora em MAIS UM!', f: 'C', cap: 18, cor: t }, X0, X1, 1000);
  };

  /* ================= 05 · O LOGO: construção, respiro, tamanho mínimo, usos errados */
  LV[5] = (D) => {
    const t = cab(5, 'O LOGO', 'papel');
    const WM = window.HF_WORDMARK;
    const cap = 112, u = cap / 710, oh = 734 * u, base = g8(176 + 722 * u + oh);
    // no papel o O aceso é PRETO (§D.1: amarelo sobre papel é par 'Nunca', 1,18:1 — decisão do diretor, 6 out 2026)
    const LP = HF.lampDe('papel');
    const wm = HF.wordmark(document.body, { x: X0 + oh, baseline: base, cap, ink: 'preto', lamp: LP });
    const yT = base - 722 * u, yB = base + 12 * u, bx0 = X0, bx1 = wm.x1 + oh, lx = col(0, 8)[1];
    const s = svg(0, 0, 1920, 1080);
    const L = (x1, y1, x2, y2, tr) => el(s, 'line', { x1, y1, x2, y2, stroke: HF.cor.preto, 'stroke-width': 1.5, 'stroke-dasharray': tr || '' });
    el(s, 'rect', { x: bx0, y: yT - oh, width: bx1 - bx0, height: yB - yT + 2 * oh, fill: 'none', stroke: HF.cor.preto, 'stroke-width': 1.5, 'stroke-dasharray': '6 6' });
    const kO = (oh * 0.82) / 848;
    const Oem = (cx, cy) => { const g = el(s, 'g', { transform: `translate(${cx - 4466 * kO} ${cy - 355 * kO}) scale(${kO})` }); el(g, 'path', { d: WM.Os[2].ext, fill: 'none', stroke: HF.cor.preto, 'stroke-width': 1.4 / kO }); };
    const mx = (wm.x0 + wm.x1) / 2, my = (yT + yB) / 2;
    Oem(bx0 + oh / 2, my); Oem(bx1 - oh / 2, my); Oem(mx, yT - oh / 2); Oem(mx, yB + oh / 2);
    L(bx0, base, lx, base); L(bx0, base - cap, lx, base - cap);
    // VERSAL e BASE dentro da caixa tracejada, encostados na borda direita (revisão do CCO, 6 out 2026: fora dela, a 4 px
    // do texto corrido, liam como parte dele): VERSAL em cima da linha de versal, BASE embaixo da linha de base
    T({ t: 'VERSAL', f: 'C', cap: 15, lsEm: 0.14, cor: t }, bx1 - 12, base - cap - 10, 'right');
    T({ t: 'BASE', f: 'C', cap: 15, lsEm: 0.14, cor: t }, bx1 - 12, base + 10 + 15, 'right');
    const yd = g8(yB + oh + 48);
    L(wm.x0, yd, wm.x1, yd); L(wm.x0, yd - 12, wm.x0, yd + 12); L(wm.x1, yd - 12, wm.x1, yd + 12);
    T({ t: 'TINTA: 8,90 × VERSAL · AVANÇO: 9,03 × VERSAL · MEDIDOS NO ARQUIVO DA FONTE', f: 'C', cap: 15, lsEm: 0.12, cor: t }, mx, yd + 36, 'center');
    T({ t: 'RESPIRO = A ALTURA DO O, EM TODOS OS LADOS', f: 'C', cap: 15, lsEm: 0.14, cor: t }, bx0, yT - oh - 20, 'left');
    const ox = wm.x0 + (4466 - WM.inkX0) * u;
    L(ox, yT - oh + 8, ox, yT - 6);
    T({ t: 'O TERCEIRO O, O DO FO: A LÂMPADA ACESA', f: 'C', cap: 15, lsEm: 0.14, cor: t }, ox + 14, yT - oh + 26, 'left');
    // usos errados
    rot('NUNCA', X0, lx, 704);
    const n = 5, tw = (lx - X0 - (n - 1) * G) / n, th = 160, ty = 736;
    const erros = [['NÃO ESTICAR', (x, y) => { const w = HF.wordmark(document.body, { x: x + 20, baseline: y + 92, largura: tw - 40, ink: 'preto', lamp: LP }); w.el.style.transformOrigin = '50% 50%'; w.el.style.transform = 'scale(0.8, 1.9)'; }],
      ['NÃO MOVER A LUZ', (x, y) => HF.wordmark(document.body, { x: x + 20, baseline: y + 92, largura: tw - 40, ink: 'preto', lamp: LP, acesos: [true, false, false] })],
      ['NÃO CONTORNAR', (x, y) => { const w = HF.wordmark(document.body, { x: x + 20, baseline: y + 92, largura: tw - 40, ink: 'preto', lamp: LP }); w.el.querySelectorAll('path').forEach((p) => { p.setAttribute('fill', 'none'); p.setAttribute('stroke', HF.cor.preto); p.setAttribute('stroke-width', 18); }); }],
      ['NÃO TROCAR A COR', (x, y) => HF.wordmark(document.body, { x: x + 20, baseline: y + 92, largura: tw - 40, ink: 'preto', lamp: 'rosa' })],
      ['NÃO BRILHAR', (x, y) => { const w = HF.wordmark(document.body, { x: x + 20, baseline: y + 92, largura: tw - 40, ink: 'preto', lamp: LP }); w.el.style.filter = `drop-shadow(0 0 10px ${HF.cor.amarelo}) drop-shadow(4px 6px 3px rgba(0,0,0,0.45))`; }]];
    erros.forEach((e, i) => {
      const x = X0 + i * (tw + G);
      caixa(x, ty, tw, th, { boxShadow: `inset 0 0 0 1.5px ${HF.cor.preto}`, overflow: 'hidden' });
      e[1](x, ty + 8);
      errado(x - 4, ty + th + 12, 24, 'preto');
      T({ t: e[0], f: 'C', cap: 14, lsEm: 0.1, cor: t }, x + 26, ty + th + 32);
    });
    const [b0, b1] = col(9, 11);
    rot('CONSTRUÇÃO', b0, b1, 168);
    corpo('Special Gothic Expanded One, caixa alta, tracking −10, kerning ligado. O terceiro O é preenchido por um disco do próprio contorno: a lâmpada acesa. Os dois primeiros ficam vazados, lâmpadas apagadas. O disco é amarelo-cartaz no preto, no rosa e no violeta, e preto no papel, no amarelo e no laranja.',
      b0, b1, 224, 17, { passo: 32 });
    rot('TAMANHO MÍNIMO', b0, b1, 600);
    HF.wordmark(document.body, { x: b0, baseline: 664, largura: 96, ink: 'preto', lamp: LP });
    T({ t: '96 PX NA TELA', f: 'C', cap: 15, lsEm: 0.14, cor: t }, b1, 664, 'right');
    HF.wordmark(document.body, { x: b0, baseline: 720, largura: 18 * 96 / 25.4, ink: 'preto', lamp: LP });
    T({ t: '18 MM NA IMPRESSÃO', f: 'C', cap: 15, lsEm: 0.14, cor: t }, b1, 720, 'right');
    rot('NO AMARELO, TUDO PRETO', b0, b1, 840);
    caixa(b0, 864, b1 - b0, 112, { background: HF.cor.amarelo });
    HF.wordmark(document.body, { x: b0 + 32, baseline: 864 + 56 + 15, largura: b1 - b0 - 64, ink: 'preto', lamp: 'preto' });
  };

  /* ================= 06 · CORES DO LOGO + A AFINAÇÃO */
  LV[6] = (D) => {
    const t = cab(6, 'CORES DO LOGO · A AFINAÇÃO', 'preto');
    const cw = [['preto-sobre-amarelo', 'amarelo', 'NO AMARELO: TUDO PRETO'], ['papel-sobre-preto', 'preto', 'PRETO-PALCO'], ['preto-sobre-papel', 'papel', 'PAPEL-CARTAZ'],
      ['preto-sobre-rosa', 'rosa', 'ROSA-CHOQUE'], ['preto-sobre-laranja', 'laranja', 'LARANJA-BIS'], ['papel-sobre-violeta', 'violeta', 'VIOLETA-UV']];
    const tw = (MED - 5 * G) / 6, th = 200;
    cw.forEach((c, i) => {
      const x = X0 + i * (tw + G), y = 128;
      caixa(x, y, tw, th, { background: HF.cor[c[1]] });
      img(K(D, '01_MARCA/logo/HOLOFOTE_logo_' + c[0] + '.svg'), x, y, tw, th, 'contain');
      if (c[1] === 'preto') caixa(x, y, tw, th, { boxShadow: `inset 0 0 0 1.5px rgba(255,248,236,0.5)` });
      T({ t: c[2], f: 'C', cap: 15, lsEm: 0.14, cor: t }, x, y + th + 32);
    });
    rot('A AFINAÇÃO · O LOGO EM MOVIMENTO · TRÊS BATIDAS DE CAIXA, 6 QUADROS DE DISTÂNCIA', X0, X1, 456);
    const quadros = [['f00', 'blecaute', [0, 0, 0]], ['f06', 'CLAC', [1, 0, 0]], ['f12', 'CLAC', [1, 1, 0]], ['f18', 'CLAC', [1, 1, 1]],
      ['f19', 'apaga 1', [0, 1, 1]], ['f20', 'apaga 2', [0, 0, 1]], ['f21', 'o rig acha ela', [0, 0, 1]]];
    const qw = (MED - 6 * G) / 7, qh = 300, WM = window.HF_WORDMARK;
    quadros.forEach((q, i) => {
      const x = X0 + i * (qw + G), y = 512;
      caixa(x, y, qw, qh, { background: '#0A090B', boxShadow: `inset 0 0 0 1.5px rgba(255,248,236,0.18)` });
      const wm = HF.wordmark(document.body, { x: x + 20, baseline: y + qh / 2, largura: qw - 40, ink: 'papel', lamp: 'amarelo', acesos: q[2].map(Boolean) });
      if (i === 6) {
        const d = 734 * wm.k, cx = wm.x0 + (4466 - WM.inkX0) * wm.k, s2 = svg(0, 0, 1920, 1080);
        const F = HF.FOCO;   // a poça de O FOCO (redesenhado em 6 out 2026): vão 1,2 d, 3,2 d × 0,5 d
        el(s2, 'ellipse', { cx, cy: y + qh / 2 + 12 * wm.k + F.vao * d + F.alt * d / 2, rx: F.larg * d / 2, ry: F.alt * d / 2, fill: HF.cor.amarelo });
      }
      div({ t: q[0], f: 'C', cap: 16, lsEm: 0.1, cor: 'amarelo', tnum: true },
        q[1] === 'CLAC' ? { t: 'CLAC', f: 'X', cap: 16, lsEm: 0, cor: t } : { t: q[1], f: 'C', cap: 17, cor: t }, x, x + qw, y + qh + 40);
    });
    corpo('Os três O acendem um depois do outro, em três batidas de caixa, CLAC · CLAC · CLAC, a seis quadros de distância. Então os dois primeiros apagam, um quadro cada, e sobra só o terceiro: o rig acha ela.',
      col(0, 7)[0], col(0, 7)[1], 936, 19, { passo: 40, cor: t });
    T({ t: '24 QPS · CORTE SECO, NUNCA FUSÃO', f: 'C', cap: 15, lsEm: 0.14, cor: 'amarelo' }, X1, 936, 'right');
  };

  /* ================= 07 · O FOCO + A MARCA */
  LV[7] = (D) => {
    fundo('papel');
    caixa(960, 0, 960, 1080, { background: HF.cor.preto });
    HF.dividida(document.body, S({ t: 'HOLOFOTE · LIVRO DA MARCA', f: 'C', cap: 15, lsEm: 0.14, cor: 'preto' }), S({ t: '07 · O FOCO', f: 'C', cap: 15, lsEm: 0.14, cor: 'preto', tnum: true }), X0, 864, 80);
    HF.dividida(document.body, S({ t: 'O SÍMBOLO E O SINAL', f: 'C', cap: 15, lsEm: 0.14, cor: 'papel' }), S({ t: 'A MARCA', f: 'C', cap: 15, lsEm: 0.14, cor: 'papel' }), 1056, X1, 80);
    // O FOCO redesenhado na revisão do CCO (6 out 2026): o desenho antigo (vão 0,5 d, poça 2,4 × 0,8 d) lia como o ícone
    // genérico de usuário a 16–32 px. Agora a poça é larga e rasa e a lâmpada fica bem acima dela.
    const F = HF.FOCO, d = 168, cx = 480, top = 168;
    const s = svg(0, 0, 960, 1080);
    el(s, 'circle', { cx, cy: top + d / 2, r: d / 2, fill: HF.cor.preto });
    const ey = top + d + F.vao * d + F.alt * d / 2, rx = F.larg * d / 2, ry = F.alt * d / 2;
    el(s, 'ellipse', { cx, cy: ey, rx, ry, fill: HF.cor.preto });
    const L = (x1, y1, x2, y2) => el(s, 'line', { x1, y1, x2, y2, stroke: HF.cor.preto, 'stroke-width': 1.5 });
    const xr = cx + rx + 36, yv = top + d + F.vao * d;
    L(xr, top, xr, yv); [top, top + d, yv].forEach((yy) => L(xr - 10, yy, xr + 10, yy));
    T({ t: 'd', f: 'C', cap: 16, lsEm: 0.1, cor: 'preto' }, xr + 16, top + d / 2 + 8);
    T({ t: '1,2 d', f: 'C', cap: 16, lsEm: 0.1, cor: 'preto' }, xr + 16, top + d + F.vao * d / 2 + 8);
    L(cx - rx, ey + ry + 32, cx + rx, ey + ry + 32); L(cx - rx, ey + ry + 22, cx - rx, ey + ry + 42); L(cx + rx, ey + ry + 22, cx + rx, ey + ry + 42);
    T({ t: '3,2 d', f: 'C', cap: 16, lsEm: 0.1, cor: 'preto' }, cx, ey + ry + 66, 'center');
    L(cx - rx - 32, ey - ry, cx - rx - 32, ey + ry); L(cx - rx - 42, ey - ry, cx - rx - 22, ey - ry); L(cx - rx - 42, ey + ry, cx - rx - 22, ey + ry);
    T({ t: '0,5 d', f: 'C', cap: 16, lsEm: 0.1, cor: 'preto' }, cx - rx - 46, ey + 8, 'right');
    // o teste que decidiu o desenho: o mestre quadrado (01_MARCA/logo) no tamanho real de favicon e de avatar redondo
    const yb = 776, tams = [64, 32, 24, 16];
    rot('NO TAMANHO REAL · O MESTRE QUADRADO, CENTRADO PELA ÁREA', X0, 864, yb - 40);
    let xx = X0;
    tams.forEach((p) => {
      img(K(D, '01_MARCA/logo/O_FOCO_preto.svg'), xx, yb + 64 - p, p, p, 'contain');
      T({ t: p + ' PX', f: 'C', cap: 13, lsEm: 0.12, cor: 'preto', tnum: true }, xx, yb + 92);
      xx += Math.max(p, 52) + 28;
    });
    xx += 24;
    caixa(xx, yb, 64, 64, { background: HF.cor.preto, borderRadius: '50%', overflow: 'hidden' });
    img(K(D, '01_MARCA/logo/O_FOCO_amarelo.svg'), xx, yb, 64, 64, 'contain');
    caixa(xx + 92, yb + 32, 32, 32, { background: HF.cor.preto, borderRadius: '50%', overflow: 'hidden' });
    img(K(D, '01_MARCA/logo/O_FOCO_amarelo.svg'), xx + 92, yb + 32, 32, 32, 'contain');
    T({ t: 'AVATAR REDONDO: NADA CORTA', f: 'C', cap: 13, lsEm: 0.12, cor: 'preto' }, xx, yb + 92);
    corpo('O disco aceso e, embaixo, a poça de luz no chão: uma elipse dura de 3,2\u00a0d por 0,5\u00a0d, a 1,2\u00a0d do disco. Larga, rasa e longe, para nunca ler como o ícone de usuário. É o favicon, o avatar, a figurinha e a trama da pulseira. O tipo nunca entra na poça.',
      X0, 864, 920, 18, { passo: 32, cor: 'preto' });
    img(K(D, '01_MARCA/marca/A-MARCA_X_s927.png'), 1192, 150, 600, 600, 'contain');
    const lin = [['DUAS TIRAS A ±45°', 'COMPRIMENTO:LARGURA 3,75:1'], ['PONTAS RASGADAS À MÃO', 'UMA PONTA DESCOLA 0,5 MM'], ['MARCA ONDE O PRODUTO FICA', 'MARCADOR DE LISTA · CARIMBO DA SETLIST']];
    lin.forEach((l, i) => HF.pontilhada(document.body, S({ t: l[0], f: 'C', cap: 16, lsEm: 0.08, cor: 'papel' }), S({ t: l[1], f: 'C', cap: 16, lsEm: 0.08, cor: 'papel' }), 1056, X1, 824 + i * 36,
      { passo: 8, folga: 10, fs: HF.fsDeCap('C', 16), op: 0.6 }));
    cheia({ t: 'UMA POR QUADRO.', f: 'X', cap: 40, lsEm: -0.01, cor: 'amarelo' }, 1056, X1, 1008);
  };

  /* ================= 08 · PALETA */
  const lum = (h) => { const c = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
  const contraste = (a, b) => { const la = lum(HF.cor[a]), lb = lum(HF.cor[b]); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
  HF.contraste = contraste;
  LV[8] = (D) => {
    const t = cab(8, 'PALETA · AS TINTAS DO CARTAZ', 'papel');
    const tintas = [['preto', 'PRETO-PALCO', 'O palco, a tinta, a tampa, o case e a noite: o campo padrão de todo O PALCO.'],
      ['papel', 'PAPEL-CARTAZ', 'O papel do cartaz, a tinta clara e o fundo exato de todas as fotos da LOJA.'],
      ['amarelo', 'AMARELO-CARTAZ', 'O sinal: AO VIVO, a fita gaffer e o O aceso. A única cor que vai em todas as peças.'],
      ['rosa', 'ROSA-CHOQUE', 'CAMARIM, a faixa 01: antes do show, ela se arrumando e você assistindo da cama.'],
      ['laranja', 'LARANJA-BIS', 'MAIS UM!, a faixa 03: o bis, a festa que vem depois do show, e mais um pouco.'],
      ['violeta', 'VIOLETA-UV', 'ACÚSTICO, a faixa 04: só em render e em código, nunca numa cena gerada.']];
    const tw = (MED - 5 * G) / 6, th = 336;
    tintas.forEach((c, i) => {
      const x = X0 + i * (tw + G), y = 128, ink = HF.tinta[c[0]];
      caixa(x, y, tw, th, { background: HF.cor[c[0]], boxShadow: c[0] === 'papel' ? `inset 0 0 0 1.5px ${HF.cor.preto}` : 'none' });
      cheia({ t: c[1], f: 'C', cap: 20, lsEm: 0.06, cor: ink }, x + 20, x + tw - 20, y + 48);
      T({ t: HF.cor[c[0]], f: 'C', cap: 16, lsEm: 0.14, cor: ink }, x + 20, y + th - 24);
      corpo(c[2], x, x + tw, y + th + 40, 16, { passo: 28, rigido: true, ultimaMin: 0.7 });
    });
    rot('PARES MEDIDOS · CONTRASTE WCAG 2.2, CALCULADO AQUI A PARTIR DOS HEX', X0, X1, 640);
    const pares = [['preto', 'amarelo', 'texto'], ['preto', 'papel', 'texto'], ['preto', 'laranja', 'texto'], ['preto', 'rosa', 'texto'], ['papel', 'violeta', 'texto'],
      ['amarelo', 'violeta', 'só destaque'], ['preto', 'violeta', 'só tipo grande'], ['papel', 'rosa', 'nunca texto'], ['papel', 'laranja', 'nunca texto'], ['amarelo', 'rosa', 'nunca texto'],
      ['amarelo', 'laranja', 'nunca lado a lado'], ['rosa', 'violeta', 'nunca lado a lado'], ['laranja', 'violeta', 'nunca lado a lado'], ['papel', 'amarelo', 'nunca']];
    const pw = (MED - 6 * G) / 7, ph = 136;
    pares.forEach((p, i) => {
      const x = X0 + (i % 7) * (pw + G), y = 680 + Math.floor(i / 7) * (ph + 40);
      caixa(x, y, pw, ph - 44, { background: HF.cor[p[1]], boxShadow: p[1] === 'papel' ? `inset 0 0 0 1.5px ${HF.cor.preto}` : 'none' });
      T({ t: 'Aa', f: 'X', cap: 40, cor: p[0] }, x + 16, y + 66);
      const r = contraste(p[0], p[1]);
      T({ t: r.toFixed(2).replace('.', ',') + ':1', f: 'C', cap: 20, cor: p[0], tnum: true }, x + pw - 14, y + 66, 'right');
      const ok = ['texto', 'só destaque', 'só tipo grande'].includes(p[2]);
      (ok ? certo : errado)(x - 2, y + ph - 34, 26, 'preto');
      T({ t: p[2].toUpperCase(), f: 'C', cap: 15, lsEm: 0.14, cor: t }, x + 32, y + ph - 14);
      (window.HF_QA = window.HF_QA || []).push({ item: 'contraste ' + p[0] + '/' + p[1], erro: 0, razao: +r.toFixed(2) });
    });
    div({ t: 'UMA COR DE FAIXA + PRETO + PAPEL POR PEÇA. O AMARELO PODE ACOMPANHAR QUALQUER FAIXA.', f: 'C', cap: 15, lsEm: 0.1, cor: t },
      { t: 'AS QUATRO SÓ SE ENCONTRAM NA COLEÇÃO.', f: 'C', cap: 15, lsEm: 0.1, cor: t }, X0, X1, 1040);
  };

  /* ================= 09 · TIPOGRAFIA I */
  LV[9] = (D) => {
    const t = cab(9, 'TIPOGRAFIA · SPECIAL GOTHIC', 'papel');
    const [a0, a1] = col(0, 6), [b0, b1] = col(7, 11);
    rot('O LOCUTOR · SPECIAL GOTHIC EXPANDED ONE', a0, a1, 160);
    cheia({ t: 'Aa MÃE', f: 'X', cap: 240, lsEm: -0.01, cor: t }, a0, a1, 456);
    cheia({ t: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', f: 'X', cap: 40, lsEm: -0.01, cor: t }, a0, a1, 560);
    cheia({ t: 'ÁÂÃÀÉÊÍÓÔÕÚÇ 0123456789 · ! ?', f: 'X', cap: 40, lsEm: -0.01, cor: t, tnum: true }, a0, a1, 632);
    rot('A PRODUÇÃO · SPECIAL GOTHIC CONDENSED ONE', a0, a1, 744);
    cheia({ t: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz', f: 'C', cap: 40, cor: t }, a0, a1, 824);
    cheia({ t: 'sessões de até 4 h. PESO LÍQUIDO 200 g · 0123456789', f: 'C', cap: 40, cor: t, tnum: true }, a0, a1, 904);
    const r = [['LOCUTOR', 'CAIXA ALTA · TRACKING −10 A 0'], ['PRODUÇÃO', 'VERSAL +80 A +120 · OU CAIXA BAIXA A 0'], ['ALGARISMOS', 'SEMPRE TNUM (TABULARES)'],
      ['CONDENSED ONE', 'ALGARISMO 710 · ALTURA-X 509 · 0,717'], ['TIL EM Ã E Õ', '+31,5 % DA VERSAL ACIMA'], ['SEM GLIFO', 'CORAÇÃO E CERTO VIRAM VETOR'], ['TODA LINHA', 'ENCHE A MEDIDA POR CORPO OU WDTH']];
    rot('REGRAS, MEDIDAS NOS ARQUIVOS', b0, b1, 160);
    r.forEach((l, i) => HF.pontilhada(document.body, S({ t: l[0], f: 'C', cap: 18, lsEm: 0.08, cor: t }),
      S({ t: l[1], f: 'C', cap: 18, lsEm: 0.08, cor: t, tnum: true }), b0, b1, 216 + i * 44, { passo: 8, folga: 10, fs: HF.fsDeCap('C', 18) }));
    rot('A FRENTE DO COPO, NA MESMA PROPORÇÃO', b0, b1, 584);
    const it = [
      { tipo: 'dividida', esq: S({ t: 'HOLOFOTE APRESENTA', f: 'C', cap: 12, lsEm: 0.08, cor: t }), dir: S({ t: 'A TURNÊ · 2027', f: 'C', cap: 12, lsEm: 0.08, cor: t, tnum: true }) },
      { tipo: 'headliner', nome: 'MÃE', capRef: HF.capMae(b1 - b0), cor: t, antes: 16 },
      { tipo: 'cheia', s: S({ t: 'AO VIVO', f: 'V', wght: 700, cap: (b1 - b0) * 10 / 72, cor: t }), modo: 'wdth', antes: 10 },
      { tipo: 'dividida', antes: 12, esq: S({ t: 'DOMINGO · 09.05', f: 'C', cap: (b1 - b0) * 4 / 72, cor: t, tnum: true }), dir: S({ t: 'abertura: você', f: 'S', x: (b1 - b0) * 1.6 / 72, cor: t }) },
    ];
    // cabe a frente inteira entre 624 e 1000: a medida encolhe até caber, mantendo as proporções do copo
    const alturaFrente = (m) => 12 + 16 + HF.capMae(m) * 1.315 + 10 + m * 10 / 72 + 12 + m * 4 / 72 + 8;
    let mm = b1 - b0; while (alturaFrente(mm) > 370) mm -= 4;
    if (mm < b1 - b0) { const k2 = mm / (b1 - b0); it[1].capRef = HF.capMae(mm); it[2].s = S({ t: 'AO VIVO', f: 'V', wght: 700, cap: mm * 10 / 72, cor: t });
      it[3].esq = S({ t: 'DOMINGO · 09.05', f: 'C', cap: mm * 4 / 72, cor: t, tnum: true }); it[3].dir = S({ t: 'abertura: você', f: 'S', x: mm * 1.6 / 72, cor: t });
      it[0].esq = S({ t: 'HOLOFOTE APRESENTA', f: 'C', cap: mm * 2.6 / 72, lsEm: 0.08, cor: t }); it[0].dir = S({ t: 'A TURNÊ · 2027', f: 'C', cap: mm * 2.6 / 72, lsEm: 0.08, cor: t, tnum: true }); }
    const b1f = b0 + mm;
    HF.pilha(document.body, it, { x0: b0, x1: b1f, y0: 624, y1: 1000 });
  };

  /* ================= 10 · TIPOGRAFIA II · o eixo de largura + a Fã */
  LV[10] = (D) => {
    const t = cab(10, 'TIPOGRAFIA · O EIXO WDTH · A FÃ', 'preto');
    const [a0, a1] = col(0, 7);
    rot('SPECIAL GOTHIC VARIÁVEL · WGHT 700 · WDTH 75 → 125 · MESMA VERSAL', a0, a1 - 24, 160);
    [75, 88, 100, 112, 125].forEach((w, i) => {
      T({ t: 'AO VIVO', f: 'V', wght: 700, wdth: w, cap: 58, cor: i === 4 ? 'amarelo' : t }, a0, 248 + i * 76);
      T({ t: 'WDTH ' + w, f: 'C', cap: 15, lsEm: 0.14, cor: t }, a1 - 24, 248 + i * 76, 'right');
    });
    rot('A LINHA 3 DO COPO: O EIXO RESOLVIDO PARA ENCHER A MESMA MEDIDA', a0, a1 - 24, 664);
    const ref = HF.texto(document.body, S({ t: 'AO VIVO', f: 'V', wght: 700, wdth: 125, cap: 44, cor: t }));
    const med = ref.inkW; ref.el.remove();
    [['AO VIVO', 125], ['CAMARIM', 106], ['MAIS UM!', 111], ['ACÚSTICO', 102]].forEach((sh, i) => {
      const y = 744 + i * 64;
      const o = HF.cheia(document.body, S({ t: sh[0], f: 'V', wght: 700, cap: 44, cor: t }), a0, a0 + med, y, 'wdth');
      T({ t: 'WDTH ' + o.s.wdth.toFixed(0) + ' NA TINTA · ' + sh[1] + ' NO AVANÇO (§C.2)', f: 'C', cap: 15, lsEm: 0.14, cor: 'amarelo', tnum: true }, a1 - 24, y, 'right');
    });
    const p0 = col(8, 8)[0];
    caixa(p0, 128, 1920 - p0, 952, { background: HF.cor.papel });
    const b0 = p0 + 48, b1 = X1;
    rot('A FÃ · SHANTELL SANS 500 · INFM 60 · BNCE 0', b0, b1, 192, 'preto');
    const fa = HF.texto(document.body, S({ t: 'abertura: você', f: 'S', x: 52, cor: 'preto' }));
    HF.porTamanho(fa, b1 - b0); HF.posicionar(fa, b0, 328, 'left');
    const fb = HF.texto(document.body, S({ t: '(girassol, 2007)', f: 'S', x: 40, cor: 'preto' }));
    HF.porTamanho(fb, b1 - b0); HF.posicionar(fb, b0, 448, 'left');
    const regras = [['SÓ CAIXA BAIXA', 'NUNCA GRITA COM ELA'], ['ATÉ SEIS PALAVRAS', 'UMA PONTUAÇÃO'], ['UMA POR PEÇA', 'SETA OU SUBLINHADO'], ['BNCE 0 NO IMPRESSO', '±20 NO FILME'], ['INFM 40 A 70', 'WGHT 450 A 550']];
    regras.forEach((l, i) => HF.pontilhada(document.body, S({ t: l[0], f: 'C', cap: 17, lsEm: 0.08, cor: 'preto' }), S({ t: l[1], f: 'C', cap: 17, lsEm: 0.08, cor: 'preto' }), b0, b1, 568 + i * 44,
      { passo: 8, folga: 10, fs: HF.fsDeCap('C', 17) }));
    corpo('A Fã é você, filho ou filha, escrevendo à mão na margem: uma anotação, uma seta, um sublinhado. É a menor voz da peça, de propósito, e nunca escreve em caixa alta.', b0, b1, 832, 17, { passo: 32, cor: 'preto' });
  };

  /* ================= 11 · AS SETE REGRAS (cada uma mostrada) */
  LV[11] = (D) => {
    const t = cab(11, 'AS SETE REGRAS DO SISTEMA', 'papel');
    const pw = (MED - 3 * G) / 4, ph = 352;
    const pos = (i) => [X0 + (i % 4) * (pw + G), 128 + Math.floor(i / 4) * (ph + 104)];
    const legenda = (i, txt) => { const [x, y] = pos(i); rot(String(i).padStart(2, '0'), x, x + pw, y + ph + 36);
      const o = T({ t: txt, f: 'C', cap: 19, lsEm: 0.04, cor: t }, x, y + ph + 72); if (o.inkW > pw) { HF.porTamanho(o, pw); HF.posicionar(o, x, y + ph + 72); } };
    { const [x, y] = pos(0); caixa(x, y, pw, ph, { background: HF.cor.preto });
      HF.pilha(document.body, [{ tipo: 'cheia', s: S({ t: 'SETE', f: 'X', cap: 80, cor: 'amarelo' }), modo: 'tamanho' }, { tipo: 'cheia', s: S({ t: 'REGRAS.', f: 'X', cap: 80, cor: 'papel' }), modo: 'tamanho', antes: 12 }, { tipo: 'espaco', flex: 1 },
        { tipo: 'cheia', s: S({ t: 'mostradas, não descritas.', f: 'C', cap: 24, cor: 'papel' }), modo: 'tamanho' }], { x0: x + 32, x1: x + pw - 32, y0: y + 32, y1: y + ph - 32 }); }
    { const [x, y] = pos(1); caixa(x, y, pw, ph, { background: HF.cor.amarelo });
      const it = [{ tipo: 'headliner', nome: 'MÃE', capRef: HF.capMae(pw - 64), cor: 'preto' }, { tipo: 'cheia', s: S({ t: 'AO VIVO', f: 'V', wght: 700, cap: 40, cor: 'preto' }), modo: 'wdth', antes: 10 }, { tipo: 'espaco', flex: 1 },
        { tipo: 'dividida', esq: S({ t: 'DOMINGO · 09.05', f: 'C', cap: 16, cor: 'preto', tnum: true }), dir: S({ t: 'abertura: você', f: 'S', x: 8, cor: 'preto' }) }];
      HF.pilha(document.body, it, { x0: x + 32, x1: x + pw - 32, y0: y + 40, y1: y + ph - 36 });
      legenda(1, 'ELA É SEMPRE A MAIOR PALAVRA; VOCÊ, A MENOR.'); }
    { const [x, y] = pos(2); caixa(x, y, pw, ph, { boxShadow: `inset 0 0 0 1.5px ${HF.cor.preto}` });
      const x0 = x + 40, x1 = x + pw - 40;
      HF.pilha(document.body, [{ tipo: 'cheia', s: S({ t: 'PRONTO-SOCORRO,', f: 'V', wght: 700, cap: 40, cor: 'preto' }), modo: 'wdth' },
        { tipo: 'cheia', s: S({ t: '3H', f: 'X', cap: 40, cor: 'preto' }), modo: 'tamanho', antes: 12 },
        { tipo: 'cheia', s: S({ t: 'SEM INGRESSO. ENTROU.', f: 'V', wght: 700, cap: 40, cor: 'preto' }), modo: 'wdth', antes: 12 }], { x0, x1, y0: y + 48, y1: y + ph - 48 });
      const s = svg(x, y, pw, ph);
      [x0 - x, x1 - x].forEach((xx) => el(s, 'line', { x1: xx, y1: 20, x2: xx, y2: ph - 20, stroke: HF.cor.rosa, 'stroke-width': 2 }));
      legenda(2, 'TODA LINHA OCUPA A LARGURA INTEIRA.'); }
    { const [x, y] = pos(3); caixa(x, y, pw, ph, { background: HF.cor.preto });
      const s = svg(x, y, pw, ph);
      el(s, 'path', { d: `M${pw / 2 - 24} 0 L${pw / 2 + 24} 0 L${pw / 2 + 160} ${ph - 100} L${pw / 2 - 160} ${ph - 100} Z`, fill: HF.cor.luz, opacity: 0.06 });
      el(s, 'ellipse', { cx: pw / 2, cy: ph - 100, rx: 160, ry: 40, fill: HF.cor.luz });
      cheia({ t: 'A ATRAÇÃO É ELA.', f: 'X', cap: 18, cor: 'papel' }, x + 32, x + pw - 32, y + 64);
      legenda(3, 'A LUZ TEM BORDA. O TIPO NUNCA ENTRA NA POÇA.'); }
    { const [x, y] = pos(4); caixa(x, y, pw, ph, { boxShadow: `inset 0 0 0 1.5px ${HF.cor.preto}` });
      HF.pilha(document.body, [{ tipo: 'cheia', s: S({ t: 'O LOCUTOR', f: 'X', cap: 40, cor: 'preto' }), modo: 'tamanho' },
        { tipo: 'cheia', s: S({ t: 'a produção', f: 'C', cap: 40, cor: 'preto' }), modo: 'tamanho', antes: 32 },
        { tipo: 'cheia', s: S({ t: '(girassol, 2007)', f: 'S', x: 30, cor: 'preto' }), modo: 'tamanho', antes: 32 }], { x0: x + 40, x1: x + pw - 40, y0: y + 48, y1: y + ph - 48 });
      legenda(4, 'CADA FONTE É UMA VOZ.'); }
    { const [x, y] = pos(5);
      img(K(D, '01_MARCA/cartazes/CARTAZ-07_MAE-AO-VIVO_rosa_RASGADO-sobre-MAIS-UM.png'), x, y, pw, ph, 'cover', { objectPosition: '50% 34%' });
      legenda(5, 'TUDO É PAPEL DE VERDADE.'); }
    { const [x, y] = pos(6); const hw = pw / 2;
      caixa(x, y, hw, ph, { background: HF.cor.papel, boxShadow: `inset 0 0 0 1.5px ${HF.cor.preto}` }); caixa(x + hw, y, hw, ph, { background: HF.cor.preto });
      cheia({ t: 'O MURO', f: 'X', cap: 30, cor: 'preto' }, x + 24, x + hw - 24, y + 72); cheia({ t: 'O PALCO', f: 'X', cap: 30, cor: 'amarelo' }, x + hw + 24, x + pw - 24, y + 72);
      cheia({ t: 'de dia: o anúncio.', f: 'C', cap: 30, cor: 'preto' }, x + 24, x + hw - 24, y + ph - 40);
      cheia({ t: 'de noite: o show.', f: 'C', cap: 30, cor: 'papel' }, x + hw + 24, x + pw - 24, y + ph - 40);
      legenda(6, 'DUAS HORAS DO DIA. NUNCA AS DUAS LUZES JUNTAS.'); }
    { const [x, y] = pos(7); caixa(x, y, pw, ph, { background: HF.cor.papel, boxShadow: `inset 0 0 0 1.5px ${HF.cor.preto}` });
      img(K(D, '01_MARCA/marca/A-MARCA_X_s4.png'), x + 28, y + 28, 76, 76, 'contain');
      cheia({ t: 'SETLIST', f: 'C', cap: 44, lsEm: 0.02, cor: 'preto' }, x + 120, x + pw - 32, y + 96);
      [['3. olha no espelho', 'ela'], ['7. terceiro sinal: acende', 'você']].forEach((l, i) =>
        HF.pontilhada(document.body, S({ t: l[0], f: 'C', cap: 16, cor: 'preto' }), S({ t: l[1], f: 'S', x: 11, cor: 'preto' }), x + 32, x + pw - 32, y + 176 + i * 40, { passo: 8, folga: 8, fs: HF.fsDeCap('C', 16) }));
      regua(x + 32, x + pw - 32, y + ph - 92, 1.5, 'preto');
      cheia({ t: 'nunca deixe a vela acesa sem supervisão.', f: 'C', cap: 20, cor: 'preto' }, x + 32, x + pw - 32, y + ph - 36);
      legenda(7, 'A SEGURANÇA ESTÁ NO ROTEIRO.'); }
  };

  /* ================= 12 · AS DUAS LUZES + LOJA */
  LV[12] = (D) => {
    const t = cab(12, 'AS DUAS LUZES · E A LOJA', 'preto');
    const luzes = [
      ['O MURO', 'papel', 'ATO 1 · 19 A 30.04', 'dia · flash duro · o anúncio', 'Flash de 3 × 3 cm, 15 cm acima da lente. Sombra dura para baixo e para a direita; o papel do cartaz estoura meio stop. Reboco com os nossos cartazes colados, com rugas de cola.'],
      ['O PALCO', 'amarelo', 'ATO 2 · 01 A 08.05', 'noite · um spot duro · o show', 'Um spot de 3.200 K, cone de 26°, borda 0,04, a 55° de elevação e −30° de azimute. Uma poça dura no chão; a vela sozinha no X; a rotunda preta quatro metros atrás.'],
      ['LOJA', 'papel', 'CATÁLOGO · 1200 × 1200', 'neutra · só para o e-commerce', 'Luz principal de 30 × 30 cm a 45° à esquerda, rebatedor branco a 20 %. Fundo papel-cartaz exato, preenchido por código. Nenhum tipo dentro da imagem, nunca.'],
    ];
    const w = (MED - 2 * G) / 3, h = 512;
    luzes.forEach((l, i) => {
      const x = X0 + i * (w + G), y = 128;
      HF.reserva(document.body, { id: l[0].replace(' ', '-'), x, y, w, h, fundo: i === 1 ? 'preto' : 'papel', tinta: i === 1 ? 'papel' : 'preto', rotulo: 'RENDER',
        nota: l[0] + ' · ' + l[3], conteudo: l[0] + ': ' + l[4] });
      div({ t: l[0], f: 'X', cap: 40, lsEm: -0.01, cor: l[1] }, { t: l[2], f: 'C', cap: 16, lsEm: 0.12, cor: l[1], tnum: true }, x, x + w, y + h + 80);
      rot(l[3].toUpperCase(), x, x + w, y + h + 128);
      corpo(l[4], x, x + w, y + h + 184, 17, { passo: 32, cor: t });
    });
    div({ t: 'NUNCA AS DUAS LUZES NO MESMO QUADRO.', f: 'C', cap: 16, lsEm: 0.12, cor: t }, { t: 'A LOJA É UM TERCEIRO ESTADO, SÓ PARA O CATÁLOGO.', f: 'C', cap: 16, lsEm: 0.12, cor: t }, X0, X1, 1032);
  };

  /* ================= 13 · DISPOSITIVOS I: o cartaz, o ingresso, o espelho, a pulseira, a setlist */
  LV[13] = (D) => {
    const t = cab(13, 'DISPOSITIVOS · I', 'papel');
    const yt = 128, hh = 408;
    const [a0, a1] = col(0, 5), cw = (a1 - a0 - 2 * 18) / 3;
    ['CARTAZ-01_MAE-AO-VIVO_amarelo', 'CARTAZ-12_C01_MAE-AO-VIVO-INGRESSOS-COM-VOCE_papel', 'CARTAZ-04_MAE-AO-VIVO_violeta'].forEach((f, i) =>
      img(K(D, '01_MARCA/cartazes/' + f + '.png'), a0 + i * (cw + 18), yt, cw, hh, 'contain'));
    const leg = (tit, desc, x0, x1, y) => { rot(tit, x0, x1, y); T({ t: desc, f: 'C', cap: 15, lsEm: 0.06, cor: t }, x0, y + 30); };
    leg('O CARTAZ', 'APRESENTA / ATRAÇÃO / SHOW / DATA / ABERTURA · ATÉ 6 LINHAS', a0, a1, yt + hh + 36);
    const [b0, b1] = col(6, 8);
    caixa(b0, yt, b1 - b0, hh, { background: HF.cor.preto });
    img(K(D, '03_LANCAMENTO/D/D02_O-INGRESSO_rasgado.png'), b0, yt, b1 - b0, hh, 'contain');
    leg('O INGRESSO', 'O CANHOTO RASGA DEPOIS DA ENTREGA', b0, b1, yt + hh + 36);
    const [c0, c1] = col(9, 11), ew = c1 - c0, s = svg(c0, yt, ew, hh);
    el(s, 'rect', { x: 0, y: 0, width: ew, height: hh, fill: HF.cor.preto });
    el(s, 'rect', { x: 56, y: 56, width: ew - 112, height: hh - 112, fill: '#2b2930' });
    const bul = [];
    [0.22, 0.5, 0.78].forEach((f) => bul.push([ew * f, 28], [ew * f, hh - 28]));
    [0.36, 0.64].forEach((f) => bul.push([28, hh * f], [ew - 28, hh * f]));
    // as lâmpadas como no mestre do case (02_PRODUTO/case, _build/pack/case.py lid_inside): disco papel Ø 9 mm com o
    // filamento cinza — a espiral horizontal presa em dois fios que descem até a base (revisão do CCO, 6 out 2026: o
    // traço cinza reto lia como o botão "menos" de uma interface). Escala: r 17 px = 4,5 mm.
    const mm = 17 / 4.5, cinza = '#94908B';
    const filamento = (x, y) => {
      const x0 = x - 1.7 * mm, x1 = x + 1.7 * mm, yc = y - 0.3 * mm, amp = 0.32 * mm;
      let d = '';
      for (let i = 0; i <= 60; i++) { const xx = x0 + (x1 - x0) * i / 60, yy = yc + amp * Math.sin(i / 60 * 2 * Math.PI * 6); d += (i ? 'L' : 'M') + xx.toFixed(2) + ' ' + yy.toFixed(2); }
      d += ` M${x0} ${yc} L${x - 0.55 * mm} ${y + 2.7 * mm} M${x1} ${yc} L${x + 0.55 * mm} ${y + 2.7 * mm}`;
      el(s, 'path', { d, fill: 'none', stroke: cinza, 'stroke-width': 1.3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' });
    };
    bul.forEach(([x, y]) => { el(s, 'circle', { cx: x, cy: y, r: 17, fill: HF.cor.papel }); filamento(x, y); });
    T({ t: 'olha a atração.', f: 'S', x: 20, cor: 'papel' }, c0 + ew / 2, yt + hh - 88, 'center');
    leg('O ESPELHO', 'DEZ LÂMPADAS IMPRESSAS · NUNCA ACESAS', c0, c1, yt + hh + 36);
    regua(X0, X1, 632, 2);
    // A PULSEIRA: trama repetida que nunca corta palavra + o selo de papel
    const [d0, d1] = col(0, 5), yb = 696;
    const banda = caixa(d0, yb, d1 - d0, 64, { background: HF.cor.preto, overflow: 'hidden' });
    const un = 'ACESSO TOTAL · ATRAÇÃO · 09.05.27 · HOLOFOTE ·';
    const m = HF.texto(banda, S({ t: un + ' ', f: 'C', cap: 22, lsEm: 0.12, cor: 'amarelo', tnum: true }));
    const n = Math.max(1, Math.floor((d1 - d0 - 48) / m.adv)); m.el.remove();
    T({ t: Array(n).fill(un).join(' '), f: 'C', cap: 22, lsEm: 0.12, cor: 'amarelo', tnum: true }, 24, 43, 'left', banda);
    caixa(d0 + (d1 - d0) * 0.62, yb - 18, 168, 100, { background: HF.cor.amarelo, transform: 'rotate(-3deg)' });
    const sel = cheia({ t: 'pode rasgar.', f: 'X', cap: 22, lsEm: -0.01, cor: 'preto' }, 0, 132, 0);
    sel.el.style.transform = 'rotate(-3deg)'; HF.posicionar(sel, d0 + (d1 - d0) * 0.62 + 18, yb + 42, 'left');
    leg('A PULSEIRA', 'TRAMA REPETIDA · NUNCA CORTA PALAVRA · O SELO DE PAPEL: pode rasgar.', d0, d1, 840);
    // A SETLIST
    const [e0, e1] = col(6, 11);
    caixa(e0, yb - 24, e1 - e0, 296, { background: HF.cor.papel, boxShadow: `inset 0 0 0 1.5px ${HF.cor.preto}` });
    img(K(D, '01_MARCA/marca/A-MARCA_X_s4.png'), e0 + 24, yb - 8, 64, 64, 'contain');
    div({ t: 'SETLIST', f: 'C', cap: 40, lsEm: 0.02, cor: t }, { t: 'DOMINGO · 09.05 · CAMARIM 1', f: 'C', cap: 16, lsEm: 0.12, cor: t, tnum: true }, e0 + 104, e1 - 32, yb + 44);
    [['1. tira a pulseira do case e põe no pulso', 'ela'], ['4. tampa na mesa, X pra cima: isso é o palco', 'você (equipe técnica)'], ['7. terceiro sinal: acende', 'você']].forEach((l, i) =>
      HF.pontilhada(document.body, S({ t: l[0], f: 'C', cap: 17, cor: t }), S({ t: l[1], f: 'S', x: 11, cor: t }), e0 + 32, e1 - 32, yb + 104 + i * 40, { passo: 8, folga: 8, fs: HF.fsDeCap('C', 17) }));
    cheia({ t: 'ninguém sai de perto da vela acesa. nem pra buscar o bolo.', f: 'C', cap: 18, cor: t }, e0 + 32, e1 - 32, yb + 240);
    leg('A SETLIST', 'A LINHA DE SEGURANÇA ESTÁ SEMPRE PRESENTE', e0, e1, 1012);
  };

  /* ================= 14 · DISPOSITIVOS II: o case, a letra da fã, o lambe, o boletim */
  LV[14] = (D) => {
    const t = cab(14, 'DISPOSITIVOS · II', 'papel');
    const [a0, a1] = col(0, 5);
    caixa(a0, 128, a1 - a0, 400, { background: HF.cor.preto });
    const est = (txt, base) => {
      const o = cheia({ t: txt, f: 'C', cap: 80, lsEm: 0.06, cor: 'papel' }, a0 + 48, a1 - 48, base);
      const c = HF.capPx(o.s), gap = Math.max(3, o.s.fs * 0.05);
      caixa(a0 + 40, base - c / 2 - gap / 2, a1 - a0 - 80, gap, { background: HF.cor.preto });
      return o;
    };
    est('CASE Nº 09.05', 296); est('CAMARIM 1 · MÃE', 432);
    // the X marks where the product stands: bottom-right corner, clear of the stencil's baseline (review, 6 Oct)
    img(K(D, '01_MARCA/marca/A-MARCA_X_s4.png'), a1 - 80, 128 + 400 - 72, 56, 56, 'contain');
    div({ t: 'O CASE', f: 'C', cap: 18, lsEm: 0.1, cor: t }, { t: 'ESTÊNCIL · PONTE DE 50 % EM TODA LETRA', f: 'C', cap: 15, lsEm: 0.06, cor: t }, a0, a1, 568);
    const [b0, b1] = col(6, 11);
    caixa(b0, 128, b1 - b0, 400, { background: HF.cor.amarelo });
    const pi = T({ t: 'PIOR', f: 'X', cap: 120, lsEm: -0.01, cor: 'preto' }, b0 + 48, 392);
    const a1n = T({ t: '(girassol,', f: 'S', x: 28, cor: 'preto' }, b1 - 48, 0, 'right');
    const xa = b1 - 48 - a1n.inkW;
    HF.posicionar(a1n, xa, 288, 'left');
    T({ t: '2007)', f: 'S', x: 28, cor: 'preto' }, xa + 10, 360, 'left');
    HF.seta(document.body, xa - 16, 268, pi.inkX1 + 22, 330, 4.6, 'preto', -0.3);
    div({ t: 'A LETRA DA FÃ', f: 'C', cap: 18, lsEm: 0.1, cor: t }, { t: 'SETA, SUBLINHADO OU PARÊNTESE · UMA POR PEÇA · ATÉ SEIS PALAVRAS', f: 'C', cap: 15, lsEm: 0.06, cor: t }, b0, b1, 568);
    regua(X0, X1, 616, 2);
    const [c0, c1] = col(0, 5);
    const lb = img(K(D, '01_MARCA/cartazes/CARTAZ-08_MAE-AO-VIVO_laranja_RASGADO-sobre-CAMARIM.png'), c0, 664, c1 - c0, 272, 'none', { objectPosition: '-560px -880px' });
    div({ t: 'O LAMBE', f: 'C', cap: 18, lsEm: 0.1, cor: t }, { t: 'GRÃO, RUGA DE COLA, BORDA RASGADA, REGISTRO DE 1–2 PX · A 100 %', f: 'C', cap: 15, lsEm: 0.06, cor: t }, c0, c1, 976);
    const [d0, d1] = col(6, 11), bw = (d1 - d0 - 2 * 24) / 3;
    ['B01_BOLETIM_0205_1x1', 'B04_BOLETIM_0505_1x1', 'B08_BOLETIM_0905_1x1'].forEach((f, i) => img(K(D, '03_LANCAMENTO/B/' + f + '.png'), d0 + i * (bw + 24), 664, bw, 272, 'cover'));
    div({ t: 'O BOLETIM', f: 'C', cap: 18, lsEm: 0.1, cor: t }, { t: '06:03 · DE 2 A 9 DE MAIO · PRA MÃE ENCAMINHAR', f: 'C', cap: 15, lsEm: 0.06, cor: t, tnum: true }, d0, d1, 976);
  };

  /* ================= 15 · NUNCA (pares faça / não faça) */
  LV[15] = (D) => {
    const t = cab(15, 'NUNCA', 'papel');
    const pw = (MED - 2 * G) / 3, ph = 288;
    const par = (i, desenhaErr, desenhaOk, txt) => {
      const x = X0 + (i % 3) * (pw + G), y = 128 + Math.floor(i / 3) * (ph + 168);
      const hw = (pw - 16) / 2;
      const e = caixa(x, y, hw, ph - 40, { boxShadow: `inset 0 0 0 1.5px ${HF.cor.preto}`, overflow: 'hidden' });
      const o = caixa(x + hw + 16, y, hw, ph - 40, { boxShadow: `inset 0 0 0 1.5px ${HF.cor.preto}`, overflow: 'hidden' });
      desenhaErr(e, hw, ph - 40); desenhaOk(o, hw, ph - 40);
      errado(x - 4, y + ph - 30, 26, 'preto'); certo(x + hw + 12, y + ph - 30, 26, 'preto');
      T({ t: 'NÃO', f: 'C', cap: 15, lsEm: 0.14, cor: t }, x + 30, y + ph - 12); T({ t: 'SIM', f: 'C', cap: 15, lsEm: 0.14, cor: t }, x + hw + 46, y + ph - 12);
      corpo(txt, x, x + pw, y + ph + 40, 17, { passo: 30, ultimaMin: 0.7 });
    };
    const Tp = (p, s, x, base, al) => T(s, x, base, al, p);
    par(0, (p, w, h) => { p.style.background = HF.cor.amarelo; Tp(p, { t: 'MÃE', f: 'X', cap: 40, cor: 'preto' }, w / 2, h / 2 + 10, 'center'); Tp(p, { t: 'ao vivo', f: 'C', cap: 20, cor: 'preto' }, w / 2, h / 2 + 50, 'center'); },
      (p, w, h) => { p.style.background = HF.cor.amarelo; HF.pilha(p, [{ tipo: 'headliner', nome: 'MÃE', capRef: HF.capMae(w - 48), cor: 'preto' }, { tipo: 'cheia', s: S({ t: 'AO VIVO', f: 'V', wght: 700, cap: 30, cor: 'preto' }), modo: 'wdth', antes: 8 }], { x0: 24, x1: w - 24, y0: 40, y1: h - 24 }); },
      'Tipo centralizado e solto, ou o Locutor em caixa baixa. Toda linha enche a medida, por corpo, por wdth ou por L/R.');
    par(1, (p, w, h) => { p.style.background = HF.cor.preto; const s = HF.svg(p, 0, 0, w, h, `0 0 ${w} ${h}`); const gr = el(s, 'radialGradient', { id: 'gl' }); el(gr, 'stop', { offset: 0, 'stop-color': HF.cor.amarelo, 'stop-opacity': 0.9 }); el(gr, 'stop', { offset: 1, 'stop-color': HF.cor.amarelo, 'stop-opacity': 0 }); el(s, 'circle', { cx: w / 2, cy: h / 2, r: h * 0.45, fill: 'url(#gl)' }); [[40, 50, 9], [w - 60, 70, 6], [70, h - 50, 12], [w - 50, h - 60, 8]].forEach(([a, b, r]) => el(s, 'circle', { cx: a, cy: b, r, fill: HF.cor.papel, opacity: 0.35 })); },
      (p, w, h) => { p.style.background = HF.cor.preto; const s = HF.svg(p, 0, 0, w, h, `0 0 ${w} ${h}`); el(s, 'path', { d: `M${w / 2 - 14} 0 L${w / 2 + 14} 0 L${w * 0.86} ${h * 0.7} L${w * 0.14} ${h * 0.7} Z`, fill: HF.cor.luz, opacity: 0.05 }); el(s, 'ellipse', { cx: w / 2, cy: h * 0.7, rx: w * 0.36, ry: h * 0.11, fill: HF.cor.luz }); },
      'Brilho suave, halo, bokeh, confete e fumaça. A luz tem borda: uma fonte, uma poça dura no chão.');
    par(2, (p, w, h) => { ['rosa', 'laranja', 'violeta', 'amarelo'].forEach((c, i) => HF.caixa(p, (i * w) / 4, 0, w / 4 + 1, h, { background: HF.cor[c] })); Tp(p, { t: 'MÃE', f: 'X', cap: 40, cor: 'amarelo' }, w / 2, h / 2 + 20, 'center'); },
      (p, w, h) => { p.style.background = HF.cor.rosa; HF.pilha(p, [{ tipo: 'headliner', nome: 'MÃE', capRef: HF.capMae(w - 48), cor: 'preto' }, { tipo: 'cheia', s: S({ t: 'CAMARIM', f: 'V', wght: 700, cap: 30, cor: 'preto' }), modo: 'wdth', antes: 8 }], { x0: 24, x1: w - 24, y0: 40, y1: h - 24 }); },
      'Quatro neons brigando no mesmo layout, o flyer de rave dos anos 2000. Uma cor de faixa, mais preto e papel.');
    par(3, (p, w, h) => { p.style.background = HF.cor.papel; const o = Tp(p, { t: 'ABERTURA: VOCÊ!!', f: 'S', x: 26, cor: 'preto' }, 24, h / 2 + 16); HF.porTamanho(o, w - 48); HF.posicionar(o, 24, h / 2 + 16); },
      (p, w, h) => { p.style.background = HF.cor.papel; const o = Tp(p, { t: 'abertura: você', f: 'S', x: 26, cor: 'preto' }, 24, h / 2 + 16); HF.porTamanho(o, w - 48); HF.posicionar(o, 24, h / 2 + 16); },
      'A Fã em caixa alta, gritando, com exclamação. A Fã nunca grita com ela: caixa baixa, até seis palavras.');
    par(4, (p, w, h) => { p.style.background = HF.cor.preto; const s = HF.svg(p, 0, 0, w, h, `0 0 ${w} ${h}`); el(s, 'ellipse', { cx: w / 2, cy: h * 0.62, rx: w * 0.4, ry: h * 0.16, fill: HF.cor.luz }); Tp(p, { t: 'SUA VEZ.', f: 'X', cap: 22, cor: 'preto' }, w / 2, h * 0.62 + 11, 'center'); },
      (p, w, h) => { p.style.background = HF.cor.preto; const s = HF.svg(p, 0, 0, w, h, `0 0 ${w} ${h}`); el(s, 'ellipse', { cx: w / 2, cy: h * 0.72, rx: w * 0.4, ry: h * 0.12, fill: HF.cor.luz }); const o = Tp(p, { t: 'SUA VEZ.', f: 'X', cap: 22, cor: 'papel' }, 24, 72); HF.porTamanho(o, w - 48); HF.posicionar(o, 24, 80); },
      'Tipo dentro da poça de luz. O tipo fica fora do foco, sempre: a poça é dela, e de mais ninguém.');
    par(5, (p, w, h) => { p.style.background = HF.cor.papel; const o = Tp(p, { t: 'obrigada, mãe', f: 'C', cap: 30, cor: 'preto' }, 24, h / 2 + 15); HF.porTamanho(o, w - 48); HF.posicionar(o, 24, h / 2 + 15); },
      (p, w, h) => { p.style.background = HF.cor.amarelo; HF.pilha(p, [{ tipo: 'cheia', s: S({ t: 'ESSE ANO, NÃO AGRADECE.', f: 'V', wght: 700, cap: 22, cor: 'preto' }), modo: 'wdth' }, { tipo: 'cheia', s: S({ t: 'APLAUDE.', f: 'X', cap: 22, cor: 'preto' }), modo: 'tamanho', antes: 12 }], { x0: 24, x1: w - 24, y0: 56, y1: h - 32 }); },
      'Agradecer, rainha do lar, guerreira, mãe nota 10. Esse ano, ninguém agradece: a plateia aplaude ela.');
  };

  /* ================= 16 · SUA VEZ */
  LV[16] = (D) => {
    fundo('amarelo');
    HF.dividida(document.body, S({ t: 'HOLOFOTE · LIVRO DA MARCA', f: 'C', cap: 15, lsEm: 0.14, cor: 'preto' }), S({ t: '16 · SUA VEZ', f: 'C', cap: 15, lsEm: 0.14, cor: 'preto', tnum: true }), X0, X1, 80);
    const [a0, a1] = col(0, 7);
    cheia({ t: 'SUA', f: 'X', cap: 300, lsEm: -0.01, cor: 'preto' }, a0, a1, 480);
    cheia({ t: 'VEZ.', f: 'X', cap: 300, lsEm: -0.01, cor: 'preto' }, a0, a1, g8(480 + 360));
    const [b0, b1] = col(8, 11);
    const h = 744, w = Math.round(h * 9 / 16);
    HF.reserva(document.body, { id: 'KV-45', x: b1 - w, y: 128, w, h, fundo: 'preto', tinta: 'papel', rotulo: 'RENDER', nota: 'KV-45 · vela acesa · 46 %',
      conteudo: 'KV-45 9:16 limpo (sem tipo), vela acesa, §E.1' });
    div({ t: 'holofote nela.', f: 'X', cap: 40, lsEm: -0.01, cor: 'preto' }, { t: 'nunca deixe a vela acesa sem supervisão.', f: 'C', cap: 18, cor: 'preto' }, X0, X1, 1000);
  };
})();
