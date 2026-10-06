/* HOLOFOTE · receitas das peças de lançamento (03_LANCAMENTO) e dos dispositivos (01_MARCA).
 * Requer holofote.js + pilha.js. Uma peça = uma receita: HF.receitas[nome](D), com D vindo do hash da URL.
 * Tudo em px da peça final. Caixas seguras = plataforma §D.10. Linhas de base na grade de 8 px (peças digitais).
 * Vozes (§A.6): 'X'/'V' 700 = o Locutor · 'C' (ou 'V' 500 com wdth resolvido) = a Produção · 'S' = a Fã.
 */
(function () {
  const R = (HF.receitas = {});
  // §D.10
  const FMT = (HF.FMT = {
    '9x16': { W: 1080, H: 1920, x0: 140, x1: 940, y0: 270, y1: 1500 },     // orgânico: base 420 px livre de tipo
    '4x5': { W: 1080, H: 1350, x0: 140, x1: 940, y0: 64, y1: 1286 },
    '1x1': { W: 1080, H: 1080, x0: 180, x1: 900, y0: 80, y1: 1000 },
    '16x9': { W: 1920, H: 1080, x0: 160, x1: 1760, y0: 96, y1: 984 },
  });
  // estilo com cap/x em px → fs
  const S = (HF.S = function (s) {
    if (!s) return s;
    const o = Object.assign({}, s);
    if (s.cap != null) o.fs = HF.fsDeCap(s.f, s.cap);
    if (s.x != null) o.fs = HF.fsDeX(s.f, s.x);
    delete o.cap; delete o.x;
    return o;
  });
  const quadro = (HF.quadro = function (W, H, fundo) {
    document.body.style.width = W + 'px';
    document.body.style.height = H + 'px';
    document.body.style.background = fundo === 'transparente' ? 'transparent' : HF.cor[fundo] || fundo;
  });
  // altura de versal de referência do headliner numa medida: a proporção do copo (cap 17,8 mm na medida de 72,0 mm,
  // §C.2), em que MÃE enche a linha quase sem tracking. Nunca escolher a versal "no olho": o passo 1 da escada (§C.10)
  // abre o tracking até +200 para encher, e MÃE com 5 % de folga vira M Ã E.
  HF.capMae = (medida) => (medida * 17.8) / 72;
  const tintaDe = (cor) => HF.tinta[cor] || 'preto';
  const lampDe = (cor) => (cor === 'amarelo' ? 'preto' : 'amarelo');       // §D.3, logos aprovados
  const destDe = (cor) => (cor === 'violeta' || cor === 'preto' ? 'amarelo' : tintaDe(cor));
  HF.assinatura = (cap, tinta, lamp, antes) => ({ tipo: 'assinatura', antes: antes || 0,
    esq: S({ t: 'holofote nela.', f: 'X', cap, lsEm: -0.01, cor: tinta }), marca: { ink: tinta, lamp }, capMarca: cap });

  /* ---- O BOLETIM DA TURNÊ (§E.2 B01–B08) ●
     D: {formato:'1x1'|'9x16', cor, data:'02.05', linhas:['bom dia.', '…'], hora:'06:03'} */
  R.boletim = function (D) {
    const F = FMT[D.formato || '1x1'], q = D.formato === '9x16';
    quadro(F.W, F.H, D.cor);
    const tinta = tintaDe(D.cor), dest = destDe(D.cor);
    // tamanhos do KV-01 no mesmo formato (§E.1): 1:1 L1 26 · MÃE 179 · AO VIVO 101 · L4 36 · assinatura 36
    const k = q ? { l1: 30, mae: 199, show: 112, l4: 46, ab: 18, dia: 112, ass: 42 } : { l1: 26, mae: 179, show: 101, l4: 36, ab: 15, dia: 101, ass: 36 };
    const itens = [
      { tipo: 'dividida', esq: S({ t: 'BOLETIM DA TURNÊ · ' + D.data, f: 'C', cap: k.l1, lsEm: 0.08, cor: tinta, tnum: true }),
        dir: S({ t: D.hora || '06:03', f: 'C', cap: k.l1, lsEm: 0.08, cor: tinta, tnum: true }) },
      { tipo: 'headliner', nome: D.headliner || 'MÃE', capRef: k.mae, cor: dest, antes: q ? 48 : 32, flex: 0.5 },
      { tipo: 'cheia', s: S({ t: D.show || 'AO VIVO', f: 'V', wght: 700, cap: k.show, cor: tinta }), modo: 'wdth', antes: q ? 24 : 18 },
      { tipo: 'dividida', antes: q ? 28 : 20, esq: S({ t: 'DOMINGO · 09.05', f: 'C', cap: k.l4, lsEm: 0.02, cor: tinta, tnum: true }),
        dir: S({ t: 'abertura: você', f: 'S', x: k.ab, cor: tinta }) },
      { tipo: 'regua', esp: q ? 3 : 2.5, cor: tinta, antes: q ? 40 : 28, flex: 1 },
    ];
    // a linha do dia: a Produção (Condensed One, caixa baixa), cada linha enche a medida por tamanho; as quebras são
    // escolhidas por cartão para equilibrar os comprimentos (nunca mais alta que AO VIVO: a atração é a maior palavra)
    // os três sinais (7, 8 e 9 de maio): três discos, o sino que toca hoje cheio — o mesmo desenho da figurinha
    if (D.sinal) {
      const dd = q ? 44 : 36;
      itens.push({ tipo: 'bloco', h: dd, antes: q ? 48 : 32, desenhar: (pa, xa, xb, top) => {
        const sv = HF.svg(pa, xa, top, dd * 4, dd, `0 0 ${dd * 4} ${dd}`), e = dd * 0.13;
        [0, 1, 2].forEach((i) => {
          const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          c.setAttribute('cx', dd / 2 + i * dd * 1.4); c.setAttribute('cy', dd / 2);
          const cheio = i === D.sinal - 1;
          c.setAttribute('r', cheio ? dd / 2 : dd / 2 - e / 2);
          c.setAttribute('fill', cheio ? HF.cor[tinta] : 'none');
          if (!cheio) { c.setAttribute('stroke', HF.cor[tinta]); c.setAttribute('stroke-width', e); }
          sv.appendChild(c);
        });
      } });
    }
    D.linhas.forEach((l, i) => itens.push({ tipo: 'cheia', s: S({ t: l, f: 'C', cap: k.dia, cor: tinta }),
      modo: 'tamanho', antes: i === 0 ? (D.sinal ? (q ? 32 : 24) : (q ? 48 : 32)) : (q ? 24 : 16) }));
    itens.push({ tipo: 'espaco', flex: 1.4 });
    itens.push(HF.assinatura(k.ass, tinta, lampDe(D.cor), 32));
    HF.pilha(document.body, itens, { x0: F.x0, x1: F.x1, y0: F.y0 + 4, y1: F.y1, grade: 8 });
  };

  /* ---- uma seta da Fã (traço de caneta, desenhada como vetor: a Shantell não tem seta) */
  HF.seta = function (parent, x0, y0, x1, y1, esp, cor, curva) {
    const minx = Math.min(x0, x1) - 60, miny = Math.min(y0, y1) - 60, w = Math.abs(x1 - x0) + 120, h = Math.abs(y1 - y0) + 120;
    const s = HF.svg(parent, minx, miny, w, h, `${minx} ${miny} ${w} ${h}`);
    const mx = (x0 + x1) / 2, my = (y0 + y1) / 2, dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy);
    const c = curva == null ? 0.22 : curva;
    const cx = mx - dy * c, cy = my + dx * c;
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', `M${x0} ${y0} Q${cx} ${cy} ${x1} ${y1}`);
    Object.entries({ fill: 'none', stroke: HF.cor[cor] || cor, 'stroke-width': esp, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' })
      .forEach(([a, v]) => p.setAttribute(a, v));
    s.appendChild(p);
    // ponta: duas pernas, ângulo pela tangente final
    const tx = x1 - cx, ty = y1 - cy, tl = Math.hypot(tx, ty), ux = tx / tl, uy = ty / tl, a = Math.min(L * 0.22, esp * 6.5);
    const perna = (ang) => { const ca = Math.cos(ang), sa = Math.sin(ang); return [x1 - a * (ux * ca - uy * sa), y1 - a * (uy * ca + ux * sa)]; };
    const [l1x, l1y] = perna(0.5), [l2x, l2y] = perna(-0.42);
    const h2 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    h2.setAttribute('d', `M${l1x} ${l1y} L${x1} ${y1} L${l2x} ${l2y}`);
    Object.entries({ fill: 'none', stroke: HF.cor[cor] || cor, 'stroke-width': esp, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' })
      .forEach(([k2, v]) => h2.setAttribute(k2, v));
    s.appendChild(h2);
    return s;
  };

  /* ---- C03 · O PIOR SHOW (9:16, amarelo, tipo de madeira empilhado)
     ELA / APLAUDIU / DE PÉ / O SEU / PIOR / SHOW. — cada linha enche a medida em Expanded (wdth 125 = a altura mínima
     possível para encher 800 px); entrelinha de tipo de madeira (12 px); PIOR no corpo do SHOW., com a Fã ao lado. */
  R.C03 = function (D) {
    const F = FMT['9x16'];
    quadro(F.W, F.H, 'amarelo');
    const b = document.body, tinta = 'preto', med = F.x1 - F.x0, gap = 4;
    const L = (t) => ({ tipo: 'cheia', s: S({ t, f: 'V', wght: 700, wdth: 125, cap: 100, lsEm: -0.01, cor: tinta }), modo: 'tamanho', antes: gap });
    // PIOR divide a linha com a nota da Fã (L/R que enche a medida): PIOR fica no corpo em que sobra lugar para a nota
    const itens = [L('ELA'), L('APLAUDIU'), L('DE PÉ'), L('O SEU'),
      { tipo: 'dividida', antes: gap, esq: S({ t: 'PIOR', f: 'V', wght: 700, wdth: 125, cap: 112, lsEm: -0.01, cor: tinta }),
        dir: S({ t: '2007)', f: 'S', x: 25, cor: tinta }) },
      L('SHOW.')];
    itens[0].antes = 0;
    HF.pilha(b, itens, { x0: F.x0, x1: F.x1, y0: F.y0 + 4, y1: 1400, grade: 8 });
    // a Fã: "(girassol, 2007)" em duas linhas de mão, encostada à direita da medida, na altura do PIOR; seta curta até o R
    const pr = itens[4], pior = pr.objs[0], an2 = pr.objs[1], capP = HF.capPx(pior.s);
    const an1 = HF.texto(b, S({ t: '(girassol,', f: 'S', x: 25, cor: tinta }));
    const xh = HF.xPx(an1.s), passo = Math.round(xh * 2.6 / 8) * 8;
    const xa = F.x1 - an1.inkW;
    const b1 = Math.round((pr.baseline - capP + xh * 1.2) / 8) * 8;
    HF.posicionar(an1, xa, b1, 'left');
    HF.posicionar(an2, xa + 8, b1 + passo, 'left');
    HF.seta(b, xa - 14, b1 - xh * 0.35, pior.inkX1 + 16, pr.baseline - capP * 0.62, 4.6, tinta, -0.28);
    window.HF_QA.push({ item: 'C03 nota da Fã: folga até o PIOR', erro: 0, folga: +(xa - pior.inkX1).toFixed(1) });
    // terço de baixo: o círculo preto Ø 360 com a vela acesa (miniatura, sem alegação de fidelidade, §D.7.5)
    const yFim = itens[5].baseline;
    const cy0 = Math.round((yFim + 32) / 8) * 8;
    HF.reserva(b, { id: 'C03_vela_acesa', x: F.x0, y: cy0, w: 360, h: 360, circulo: true, fundo: 'preto', tinta: 'papel',
      rotulo: 'RENDER', nota: 'vela acesa · miniatura', conteudo: 'HOLOFOTE AO VIVO acesa, sem tampa, no X, palco preto; miniatura sem alegação de fidelidade (§D.7.5)' });
    // à direita do círculo: a chamada, a assinatura e a linha de segurança (§D.8.6) — todo tipo acima de y 1500
    const xc = F.x0 + 360 + 48;
    const it2 = [
      { tipo: 'cheia', s: S({ t: 'Sua vez.', f: 'X', cap: 60, lsEm: -0.01, cor: tinta }), modo: 'tamanho' },
      { tipo: 'cheia', s: S({ t: 'holofote nela.', f: 'X', cap: 30, lsEm: -0.01, cor: tinta }), modo: 'tamanho', antes: 16 },
      { tipo: 'cheia', s: S({ t: 'nunca deixe a vela acesa sem supervisão.', f: 'C', cap: 20, cor: tinta }), modo: 'tamanho', antes: 16 },
    ];
    HF.pilha(b, it2, { x0: xc, x1: F.x1, y0: cy0, y1: Math.min(F.y1, cy0 + 360), grade: 8 });
    window.HF_QA.push({ item: 'C03 último tipo (≤ 1500)', erro: 0, base: it2[2].baseline });
  };

  /* ---- C07 · PIX (9:16, amarelo; só em 6 de maio). Ordem da tabela §E.2: título, miniatura do KV, lineup. */
  R.C07 = function (D) {
    const F = FMT['9x16'];
    quadro(F.W, F.H, 'amarelo');
    const b = document.body, tinta = 'preto';
    const L = (t, antes) => ({ tipo: 'cheia', s: S({ t, f: 'V', wght: 700, wdth: 125, cap: 100, lsEm: -0.01, cor: tinta }), modo: 'tamanho', antes });
    const itens = [L('PIX', 0), L('NÃO TEM', 16), L('CHEIRO.', 16)];
    HF.pilha(b, itens, { x0: F.x0, x1: F.x1, y0: F.y0 + 4, y1: 900, grade: 8 });
    const yb = itens[2].baseline;
    // linha de baixo (base 1496): segurança (Produção) à esquerda, a assinatura à direita — L/R que enche a medida
    const it3 = [{ tipo: 'dividida', esq: S({ t: 'nunca deixe a vela acesa sem supervisão.', f: 'C', cap: 20, cor: tinta }),
      dir: S({ t: 'holofote nela.', f: 'X', cap: 30, lsEm: -0.01, cor: tinta }) }];
    HF.pilha(b, it3, { x0: F.x0, x1: F.x1, y0: F.y1 - 40, y1: F.y1, grade: 8 });
    // miniatura do KV (vela acesa), 4:5, à esquerda; ao lado, o lineup que enche a coluna
    const ty = Math.round((yb + 56) / 8) * 8, th = Math.round((it3[0].baseline - 30 - 56 - ty) / 8) * 8, tw = Math.round(th * 0.8);
    HF.reserva(b, { id: 'C07_kv_miniatura', x: F.x0, y: ty, w: tw, h: th, fundo: 'preto', tinta: 'papel', rotulo: 'RENDER',
      nota: 'KV-01 · vela acesa', conteudo: 'miniatura do KV-01 4:5 (vela acesa no palco), sem alegação de fidelidade (§D.7.5)' });
    const xc = F.x0 + tw + 40;
    // o lineup (O CARTAZ em miniatura): MÃE enche a coluna, AO VIVO pelo eixo wdth, DOMINGO · 09.05 na base da miniatura
    const it2 = [
      { tipo: 'headliner', nome: 'MÃE', capRef: HF.capMae(F.x1 - xc), cor: tinta, antes: 0 },
      { tipo: 'cheia', s: S({ t: 'AO VIVO', f: 'V', wght: 700, cap: 58, cor: tinta }), modo: 'wdth', antes: 16 },
      { tipo: 'espaco', flex: 1 },
      { tipo: 'dividida', esq: S({ t: 'DOMINGO', f: 'C', cap: 30, lsEm: 0.06, cor: tinta }),
        dir: S({ t: '09.05', f: 'C', cap: 30, lsEm: 0.06, cor: tinta, tnum: true }) },
    ];
    HF.pilha(b, it2, { x0: xc, x1: F.x1, y0: ty - 2, y1: ty + th, grade: 8 });
  };

  /* ---- C09 · O CARTAZ DELA (9:16, saída de exemplo do gerador de cartaz) ● */
  R.C09 = function (D) {
    const F = FMT['9x16'];
    const cor = D.cor || 'rosa';
    quadro(F.W, F.H, cor);
    const b = document.body, tinta = tintaDe(cor), dest = destDe(cor), u = (F.x1 - F.x0) / 800;
    const capL = 21;
    const itens = [
      { tipo: 'dividida', esq: S({ t: 'HOLOFOTE APRESENTA', f: 'C', cap: 30, lsEm: 0.08, cor: tinta }),
        dir: S({ t: 'A TURNÊ · 2027', f: 'C', cap: 30, lsEm: 0.08, cor: tinta, tnum: true }) },
      { tipo: 'headliner', nome: D.headliner || 'DONA CIDA', capRef: 199, cor: dest, coracao: D.coracao, antes: 40, flex: 0.6 },
      { tipo: 'cheia', s: S({ t: D.show || 'AO VIVO', f: 'V', wght: 700, cap: 112, cor: tinta }), modo: 'wdth', antes: 24 },
      { tipo: 'dividida', antes: 28, esq: S({ t: 'DOMINGO · 09.05', f: 'C', cap: 46, lsEm: 0.02, cor: tinta, tnum: true }),
        dir: S({ t: 'abertura: ' + (D.abertura || 'você'), f: 'S', x: 18, cor: tinta }) },
      { tipo: 'regua', esp: 3, cor: tinta, antes: 40, flex: 1 },
      { tipo: 'cheia', s: S({ t: 'ELA ESTEVE EM TODAS.', f: 'V', wght: 700, wdth: 125, cap: 40, lsEm: -0.005, cor: tinta }), modo: 'tamanho', antes: 32 },
    ];
    (D.turne || []).forEach((l, i) => itens.push({ tipo: 'pontilhada', passo: i === 0 ? null : 40, antes: i === 0 ? 28 : 0,
      esq: S({ t: l[0], f: 'C', cap: capL, lsEm: 0.02, cor: tinta, tnum: true }),
      dir: S({ t: l[1], f: 'V', wght: 700, wdth: 75, cap: capL, lsEm: 0.01, cor: tinta }),
      opt: { passo: 0.409 * capL, folga: 0.45 * capL, fs: HF.fsDeCap('C', capL) } }));
    itens.push({ tipo: 'regua', esp: 3, cor: tinta, antes: 24 });
    itens.push({ tipo: 'espaco', flex: 1 });
    itens.push({ tipo: 'dividida', esq: S({ t: 'faz o cartaz dela.', f: 'C', cap: 34, cor: tinta }),
      dir: S({ t: 'holofote.exemplo/cartaz', f: 'C', cap: 34, cor: tinta }) });
    itens.push(HF.assinatura(42, tinta, lampDe(cor), 32));
    HF.pilha(b, itens, { x0: F.x0, x1: F.x1, y0: F.y0 + 4, y1: F.y1, grade: 8 });
  };

  /* ---- O INGRESSO ● (§D.4) e D02 · O INGRESSO e-ticket (1080 × 1350). Desenha SÓ o ingresso, em fundo transparente:
     o papel, o picote rasgado e o canhoto solto entram em Python (lancamento.py). Geometria em window.HF_INGRESSO.
     D: {cor, headliner, show, x, y, w, hCorpo, hCanhoto} */
  R.ingresso = function (D) {
    const W = D.W || 1080, H = D.H || 1350;
    quadro(W, H, 'transparente');
    const b = document.body, cor = D.cor || 'amarelo', tinta = tintaDe(cor), dest = destDe(cor);
    const x0 = D.x || 140, w = D.w || 800, y0 = D.y || 88, hc = D.hCorpo || 892, hs = D.hCanhoto || 282;
    const yp = y0 + hc, x1 = x0 + w, raio = 22, m = 56;
    // forma do ingresso (SVG): retângulo com cantos de 6 px, dois meios-círculos no picote, furos do picote
    const s = HF.svg(b, 0, 0, W, H, `0 0 ${W} ${H}`);
    let d = `M${x0 + 6} ${y0} H${x1 - 6} Q${x1} ${y0} ${x1} ${y0 + 6} V${yp - raio} A${raio} ${raio} 0 0 0 ${x1} ${yp + raio}` +
      ` V${yp + hs - 6} Q${x1} ${yp + hs} ${x1 - 6} ${yp + hs} H${x0 + 6} Q${x0} ${yp + hs} ${x0} ${yp + hs - 6} V${yp + raio}` +
      ` A${raio} ${raio} 0 0 0 ${x0} ${yp - raio} V${y0 + 6} Q${x0} ${y0} ${x0 + 6} ${y0} Z`;
    const passo = 14, n = Math.floor((w - 2 * raio - 24) / passo);
    const xi = x0 + raio + 12 + ((w - 2 * raio - 24) - (n - 1) * passo) / 2;
    for (let i = 0; i < n; i++) { const cx = xi + i * passo; d += ` M${cx - 2.6} ${yp} a2.6 2.6 0 1 0 5.2 0 a2.6 2.6 0 1 0 -5.2 0 Z`; }
    HF.path(s, d, HF.cor[cor], 'evenodd');
    // corpo
    const X0 = x0 + m, X1 = x1 - m;
    const it = [
      { tipo: 'dividida', esq: S({ t: 'INGRESSO', f: 'C', cap: 24, lsEm: 0.1, cor: tinta }),
        dir: S({ t: 'A TURNÊ · 2027', f: 'C', cap: 24, lsEm: 0.1, cor: tinta, tnum: true }) },
      { tipo: 'regua', esp: 2, cor: tinta, antes: 24 },
      { tipo: 'headliner', nome: D.headliner || 'MÃE', capRef: HF.capMae(X1 - X0), cor: dest, coracao: D.coracao, antes: 28, flex: 1 },
      { tipo: 'cheia', s: S({ t: D.show || 'AO VIVO', f: 'V', wght: 700, cap: 86, cor: tinta }), modo: 'wdth', antes: 20 },
      { tipo: 'regua', esp: 2, cor: tinta, antes: 32, flex: 1 },
      { tipo: 'pontilhada', antes: 28, esq: S({ t: 'SETOR:', f: 'C', cap: 28, lsEm: 0.06, cor: tinta }),
        dir: S({ t: 'PRIMEIRA FILA', f: 'V', wght: 700, wdth: 75, cap: 28, lsEm: 0.01, cor: tinta }),
        opt: { passo: 0.409 * 28, folga: 0.45 * 28, fs: HF.fsDeCap('C', 28) } },
      { tipo: 'pontilhada', passo: 48, esq: S({ t: 'ASSENTO:', f: 'C', cap: 28, lsEm: 0.06, cor: tinta }),
        dir: S({ t: 'O DE SEMPRE', f: 'V', wght: 700, wdth: 75, cap: 28, lsEm: 0.01, cor: tinta }),
        opt: { passo: 0.409 * 28, folga: 0.45 * 28, fs: HF.fsDeCap('C', 28) } },
      { tipo: 'regua', esp: 2, cor: tinta, antes: 28 },
      { tipo: 'dividida', antes: 24, esq: S({ t: 'DOMINGO', f: 'V', wght: 700, wdth: 75, cap: 52, cor: tinta }),
        dir: S({ t: '09.05', f: 'V', wght: 700, wdth: 75, cap: 52, cor: tinta, tnum: true }) },
      { tipo: 'espaco', flex: 1.2 },
      HF.assinatura(30, tinta, lampDe(cor), 24),
    ];
    HF.pilha(b, it, { x0: X0, x1: X1, y0: y0 + 48, y1: yp - 48, grade: 8 });
    // canhoto
    const its = [
      { tipo: 'cheia', s: S({ t: 'ADMITE 1 · ATRAÇÃO', f: 'V', wght: 700, wdth: 125, cap: 40, lsEm: -0.005, cor: tinta }), modo: 'tamanho' },
      { tipo: 'bloco', h: 76, antes: 22, desenhar: (pa, xa, xb, top) => HF.barras(pa, xa, top, xb - xa, 76, tinta, 509) },
      { tipo: 'dividida', antes: 22, esq: S({ t: 'CÓDIGO DE BARRAS FICTÍCIO', f: 'C', cap: 15, lsEm: 0.12, cor: tinta }),
        dir: S({ t: 'DOMINGO · 09.05', f: 'C', cap: 15, lsEm: 0.12, cor: tinta, tnum: true }) },
    ];
    HF.pilha(b, its, { x0: X0, x1: X1, y0: yp + 44, y1: yp + hs - 40, grade: 8 });
    window.HF_GEOM = { x0, x1, y0, yPicote: yp, y1: yp + hs, raio, cor };
  };

  /* bloco de barras fictício, não escaneável (§C.7 "CÓDIGO DE BARRAS FICTÍCIO"): larguras pseudo-aleatórias determinísticas */
  HF.barras = function (parent, x, y, w, h, cor, semente) {
    const s = HF.svg(parent, x, y, w, h, `0 0 ${w} ${h}`);
    let r = semente || 1;
    const rnd = () => ((r = (r * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
    let xx = 0, d = '';
    while (xx < w) {
      const bw = 2 + Math.floor(rnd() * 4) * 2, gap = 2 + Math.floor(rnd() * 3) * 2;
      if (xx + bw > w) break;
      d += `M${xx} 0h${bw}v${h}h${-bw}Z`;
      xx += bw + gap;
    }
    HF.path(s, d, HF.cor[cor] || cor);
    return s;
  };

  /* ---- D01 · A CARTEIRINHA (9:16 story, gerador) ●  D: {cor, headliner, anos, foto (url opcional)} */
  R.D01 = function (D) {
    const F = FMT['9x16'], cor = D.cor || 'amarelo';
    quadro(F.W, F.H, 'preto');
    const b = document.body, tinta = tintaDe(cor), dest = destDe(cor);
    // o cartão: retrato, cantos arredondados, plastificado. Ocupa a caixa segura orgânica (x 140–940, y 270–1500)
    const cx0 = 140, cy0 = 286, cw = 800, ch = 1198, r = 44, m = 56;
    const card = HF.caixa(b, cx0, cy0, cw, ch, { background: HF.cor[cor], borderRadius: r + 'px', overflow: 'hidden' });
    // faixa de cima (preto) com o nome do fã-clube
    const fx = 'FÃ-CLUBE OFICIAL';
    HF.caixa(b, cx0, cy0, cw, 168, { background: HF.cor.preto, borderRadius: `${r}px ${r}px 0 0` });
    const it0 = [{ tipo: 'cheia', s: S({ t: fx, f: 'V', wght: 700, wdth: 125, cap: 50, lsEm: -0.005, cor: 'amarelo' }), modo: 'tamanho' }];
    HF.pilha(b, it0, { x0: cx0 + m, x1: cx0 + cw - m, y0: cy0 + 56, y1: cy0 + 140, grade: 8 });
    // janela da foto (4:5) + número de sócio
    const X0 = cx0 + m, X1 = cx0 + cw - m;
    const pw = 256, ph = 320, py = cy0 + 168 + 40;
    if (D.foto) {
      const im = document.createElement('img'); im.src = D.foto;
      Object.assign(im.style, { position: 'absolute', left: X0 + 'px', top: py + 'px', width: pw + 'px', height: ph + 'px', objectFit: 'cover', borderRadius: '16px' });
      b.appendChild(im);
    } else HF.reserva(b, { id: 'D01_foto', x: X0, y: py, w: pw, h: ph, fundo: cor, tinta: tinta, rotulo: 'FOTO', nota: 'foto dela · 4:5',
      conteudo: 'foto enviada pelo usuário (gerador); recorte 4:5, cantos 16 px' });
    const caixaFoto = document.querySelector('.hf-ph:last-of-type');
    if (caixaFoto) caixaFoto.style.borderRadius = '16px';
    const xs = X0 + pw + 40;
    const it1 = [
      { tipo: 'cheia', s: S({ t: 'SÓCIO Nº', f: 'C', cap: 60, lsEm: 0.02, cor: tinta }), modo: 'tamanho' },
      { tipo: 'cheia', s: S({ t: D.socio || '0001', f: 'V', wght: 700, wdth: 125, cap: 100, lsEm: -0.01, cor: tinta, tnum: true }), modo: 'tamanho', antes: 16 },
      { tipo: 'espaco', flex: 1 },
      { tipo: 'cheia', s: S({ t: 'Validade: vitalícia', f: 'C', cap: 26, cor: tinta }), modo: 'tamanho' },
    ];
    HF.pilha(b, it1, { x0: xs, x1: X1, y0: py, y1: py + ph, grade: 8 });
    // a atração (a maior palavra do cartão) + os campos
    const anos = D.anos == null ? 22 : D.anos;
    const it2 = [
      { tipo: 'headliner', nome: D.headliner || 'MÃE', capRef: HF.capMae(X1 - X0), cor: dest, coracao: D.coracao, antes: 0 },
      { tipo: 'regua', esp: 2, cor: tinta, antes: 36 },
      ...[['Membro desde:', 'hoje'], ['Atraso:', anos + ' anos'], ['Benefício:', 'acesso total (sempre teve).']].map((l, i) => ({
        tipo: 'pontilhada', passo: i ? 52 : null, antes: i ? 0 : 36,
        esq: S({ t: l[0], f: 'C', cap: 27, cor: tinta }), dir: S({ t: l[1], f: 'C', cap: 27, cor: tinta, tnum: true }),
        opt: { passo: 0.409 * 27, folga: 0.45 * 27, fs: HF.fsDeCap('C', 27) } })),
      { tipo: 'regua', esp: 2, cor: tinta, antes: 28 },
      { tipo: 'espaco', flex: 1 },
      HF.assinatura(28, tinta, lampDe(cor), 24),
    ];
    HF.pilha(b, it2, { x0: X0, x1: X1, y0: py + ph + 48, y1: cy0 + ch - 64, grade: 8 });
    // o brilho da plastificação: uma faixa diagonal de borda dura (não é 'glow'), 9% de branco
    const gl = HF.caixa(b, cx0, cy0, cw, ch, { borderRadius: r + 'px', overflow: 'hidden', pointerEvents: 'none' });
    const st = document.createElement('div');
    Object.assign(st.style, { position: 'absolute', left: '-40%', top: '-10%', width: '180%', height: '150px',
      background: 'linear-gradient(180deg, rgba(255,255,255,0) 0, rgba(255,255,255,0.10) 6px, rgba(255,255,255,0.13) 50%, rgba(255,255,255,0.10) calc(100% - 6px), rgba(255,255,255,0) 100%)',
      transform: 'translate(0, 330px) rotate(-24deg)', transformOrigin: '50% 50%' });
    gl.appendChild(st);
    const st2 = st.cloneNode(); st2.style.height = '34px'; st2.style.transform = 'translate(0, 520px) rotate(-24deg)';
    gl.appendChild(st2);
  };

  /* ---- STK · figurinhas (512 × 512, transparente; a borda branca de adesivo entra em Python)  D: {v: nome} */
  R.stk = function (D) {
    const W = 512;
    quadro(W, W, 'transparente');
    const b = document.body;
    const rnd = (() => { let r = D.semente || 7; return () => ((r = (r * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff); })();
    // recorte de papel com borda irregular (cartaz arrancado): polígono com ruído
    const recorte = (x, y, w, h, cor, ang, pai) => {
      const s = HF.svg(pai || b, 0, 0, W, W, `0 0 ${W} ${W}`);
      const pts = [], n = 22, j = (k) => (rnd() - 0.5) * k;
      for (let i = 0; i <= n; i++) pts.push([x + (w * i) / n + j(3), y + j(i % 3 ? 4 : 9)]);
      for (let i = 1; i <= n * 0.6; i++) pts.push([x + w + j(i % 2 ? 4 : 10), y + (h * i) / (n * 0.6)]);
      for (let i = n; i >= 0; i--) pts.push([x + (w * i) / n + j(3), y + h + j(i % 3 ? 4 : 11)]);
      for (let i = Math.floor(n * 0.6) - 1; i > 0; i--) pts.push([x + j(i % 2 ? 4 : 9), y + (h * i) / (n * 0.6)]);
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.setAttribute('transform', `rotate(${ang || 0} ${x + w / 2} ${y + h / 2})`);
      const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      p.setAttribute('d', 'M' + pts.map((q) => q.map((v) => v.toFixed(1)).join(' ')).join(' L') + ' Z');
      p.setAttribute('fill', HF.cor[cor] || cor);
      g.appendChild(p); s.appendChild(g);
      return s;
    };
    const girar = (el, ang, ox, oy) => { el.style.transformOrigin = `${ox}px ${oy}px`; el.style.transform = `rotate(${ang}deg)`; };
    // grupos giram só DEPOIS de tudo medido e posicionado (medir dentro de um pai girado devolve caixas giradas)
    const grupos = [];
    const grupo = (ang) => { const g = HF.caixa(b, 0, 0, W, W, {}); grupos.push([g, ang]); return g; };
    const v = D.v;
    if (v === 'ACESSO-TOTAL') {
      // a pulseira: faixa tecida preta, jacquard amarelo
      const g = grupo(-9);
      HF.caixa(g, 16, 188, 480, 136, { background: HF.cor.preto, borderRadius: '10px' });
      HF.pilha(g, [{ tipo: 'cheia', s: S({ t: 'ACESSO TOTAL', f: 'C', cap: 64, lsEm: 0.1, cor: 'amarelo' }), modo: 'tamanho' }],
        { x0: 52, x1: 460, y0: 222, y1: 296 });
      for (const yy of [200, 312]) HF.caixa(g, 28, yy, 456, 2, { background: HF.cor.amarelo, opacity: 0.55 });
    } else if (v === 'MAIS-UM') {
      const g = grupo(-6);
      recorte(36, 150, 440, 212, 'laranja', 0, g);
      HF.pilha(g, [{ tipo: 'cheia', s: S({ t: 'MAIS UM!', f: 'X', cap: 80, lsEm: -0.01, cor: 'preto' }), modo: 'tamanho' }],
        { x0: 70, x1: 442, y0: 206, y1: 320 });
    } else if (v === 'ABERTURA-VOCE') {
      const g = grupo(-4);
      recorte(40, 160, 432, 190, 'papel', 0, g);
      const it = [{ tipo: 'cheia', s: S({ t: 'abertura: você', f: 'S', x: 40, cor: 'preto' }), modo: 'tamanho' }];
      HF.pilha(g, it, { x0: 76, x1: 436, y0: 214, y1: 300 });
      const o = it[0].objs[0];
      // sublinhado de caneta embaixo de "você" (a Fã: seta ou sublinhado, nunca os dois)
      const sv = HF.svg(g, 0, 0, W, W, `0 0 ${W} ${W}`);
      const y = it[0].baseline + 26, xa = o.inkX1 - 128, xb = o.inkX1 + 4;
      const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      p.setAttribute('d', `M${xa} ${y + 2} C ${xa + 40} ${y - 6}, ${xb - 50} ${y + 7}, ${xb} ${y - 3}`);
      Object.entries({ fill: 'none', stroke: HF.cor.preto, 'stroke-width': 5, 'stroke-linecap': 'round' }).forEach(([a, c]) => p.setAttribute(a, c));
      sv.appendChild(p);
    } else if (v === 'NAO-PRECISAVA') {
      const g = grupo(5);
      recorte(30, 168, 452, 176, 'rosa', 0, g);
      HF.pilha(g, [{ tipo: 'cheia', s: S({ t: 'não precisava.', f: 'C', cap: 80, cor: 'preto' }), modo: 'tamanho' }],
        { x0: 64, x1: 448, y0: 206, y1: 310 });
    } else if (v === 'PRECISAVA') {
      // o fundo do copo: disco amarelo com o relevo PRECISAVA. (§C.4)
      const s = HF.svg(b, 0, 0, W, W, `0 0 ${W} ${W}`);
      const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      c.setAttribute('cx', 256); c.setAttribute('cy', 256); c.setAttribute('r', 232); c.setAttribute('fill', HF.cor.amarelo);
      s.appendChild(c);
      const c2 = c.cloneNode(); c2.setAttribute('r', 206); c2.setAttribute('fill', 'none'); c2.setAttribute('stroke', HF.cor.preto); c2.setAttribute('stroke-width', 3);
      s.appendChild(c2);
      HF.pilha(b, [{ tipo: 'cheia', s: S({ t: 'PRECISAVA.', f: 'X', cap: 60, lsEm: -0.01, cor: 'preto' }), modo: 'tamanho' }],
        { x0: 84, x1: 428, y0: 222, y1: 290 });
    } else if (v === 'EQUIPE-TECNICA') {
      // credencial de equipe: crachá preto com furo de cordão
      const g = grupo(-5);
      HF.caixa(g, 106, 40, 300, 432, { background: HF.cor.preto, borderRadius: '22px' });
      HF.caixa(g, 216, 66, 80, 18, { background: 'transparent', border: `3px solid ${HF.cor.papel}`, borderRadius: '9px', boxSizing: 'border-box' });
      HF.caixa(g, 106, 108, 300, 88, { background: HF.cor.amarelo });
      HF.wordmark(g, { x: 256, baseline: 152 + 13, largura: 236, ink: 'preto', lamp: 'preto', align: 'center' });
      const it = [
        { tipo: 'cheia', s: S({ t: 'equipe', f: 'C', cap: 70, cor: 'papel' }), modo: 'tamanho' },
        { tipo: 'cheia', s: S({ t: 'técnica', f: 'C', cap: 70, cor: 'papel' }), modo: 'tamanho', antes: 12 },
      ];
      HF.pilha(g, it, { x0: 134, x1: 378, y0: 232, y1: 444 });
    } else if (v === 'TERCEIRO-SINAL') {
      // cartão de deixa (cue card) com os três sinais: três discos, o terceiro aceso
      const g = grupo(4);
      HF.caixa(g, 40, 132, 432, 248, { background: HF.cor.preto, borderRadius: '18px' });
      const s = HF.svg(g, 0, 0, W, W, `0 0 ${W} ${W}`);
      [0, 1, 2].forEach((i) => {
        const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        c.setAttribute('cx', 116 + i * 70); c.setAttribute('cy', 196); c.setAttribute('r', 24);
        c.setAttribute('fill', i === 2 ? HF.cor.amarelo : 'none');
        if (i < 2) { c.setAttribute('stroke', HF.cor.papel); c.setAttribute('stroke-width', 5); }
        s.appendChild(c);
      });
      HF.pilha(g, [{ tipo: 'cheia', s: S({ t: 'terceiro sinal', f: 'C', cap: 64, cor: 'papel' }), modo: 'tamanho' }],
        { x0: 80, x1: 432, y0: 248, y1: 340 });
    } else if (v === 'ELA-FICA-AQUI') {
      // a tira de fita gaffer (marca.py --uma) com a letra da Fã, como na tampa (§C.5)
      const ang = D.angulo || -7;
      const im = document.createElement('img'); im.src = D.tira;
      Object.assign(im.style, { position: 'absolute', left: 0, top: 0, width: W + 'px', height: W + 'px' });
      b.appendChild(im);
      const g = grupo(-ang);
      const o = HF.texto(g, S({ t: 'ela fica aqui.', f: 'S', x: 40, cor: 'preto' }));
      HF.porTamanho(o, 330);
      HF.posicionar(o, 256, 256 + HF.xPx(o.s) / 2, 'center');
    }
    grupos.forEach(([g, ang]) => girar(g, ang, W / 2, W / 2));
  };
})();
