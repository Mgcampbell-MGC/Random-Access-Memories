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
    const medida = x1 - x0;
    const sBase = Object.assign({ f: o.f || 'C', cor: o.cor || TINTA }, o.estilo || {});
    sBase.fs = o.fs || HF.fsDeCap(sBase.f, o.cap);
    const pal = texto.split(/\s+/).filter(Boolean);
    const larg = (t) => { const e = HF.texto(parent, Object.assign({}, sBase, { t })); const w = e.adv; e.el.remove(); return w; };
    const ws = pal.map(larg), esp = larg('a a') - larg('aa');
    const quebrar = (k) => {
      const L = []; let cur = [], w = 0;
      pal.forEach((p, i) => {
        const add = cur.length ? esp * k + ws[i] * k : ws[i] * k;
        if (cur.length && w + add > medida) { L.push({ ids: cur, w }); cur = [i]; w = ws[i] * k; } else { cur.push(i); w += add; }
      });
      L.push({ ids: cur, w });
      return L;
    };
    // custo: distância do corpo pedido + maior espaço entre palavras + o que falta na última linha
    const avaliar = (ultMin, gapMax) => {
      let best = null;
      for (let i = -60; i <= 60; i++) {
        const k = 1 + i * 0.0025, L = quebrar(k);
        if (o.maxLinhas && L.length > o.maxLinhas) continue;
        const ultL = L[L.length - 1];
        if (L.length > 1 && ultL.ids.length < 2) continue;                 // nunca uma palavra sozinha na última linha
        const ult = ultL.w / medida;
        if (L.length === 1 ? ult < 0.97 : ult < ultMin) continue;
        const gap = Math.max(...L.map((l) => (l.ids.length > 1 ? (medida - l.w) / (l.ids.length - 1) : 0))) / (sBase.fs * k);
        if (gap > gapMax) continue;
        const custo = Math.abs(k - 1) * 8 + gap + (1 - ult) * 1.5;
        if (!best || custo < best.custo) best = { k, L, custo };
      }
      return best;
    };
    let melhor = avaliar(o.ultimaMin || 0.8, 0.8) || avaliar(0.62, 1.2);
    if (!melhor) { console.warn('corrido: sem corpo que feche a última linha:', texto.slice(0, 40)); melhor = { k: 1, L: quebrar(1) }; }
    const passo = o.passo || g8(HF.capPx(sBase) * 1.75);
    const linhas = [];
    melhor.L.forEach((l, i) => {
      const t = l.ids.map((j) => pal[j]).join(' ');
      const s = Object.assign({}, sBase, { t, fs: sBase.fs * melhor.k });
      const e = HF.texto(parent, s);
      const n = l.ids.length - 1;
      if (n > 0) {
        let wsp = 0;
        for (let it = 0; it < 4; it++) {
          wsp += (medida - e.inkW) / n;
          e.el.style.wordSpacing = wsp + 'px';
          HF.mudar(e, {});
        }
      } else if (melhor.L.length === 1 && Math.abs(e.inkW - medida) > 0.5) HF.porTamanho(e, medida);
      HF.posicionar(e, x0, base0 + i * passo, 'left');
      (window.HF_QA = window.HF_QA || []).push({ item: 'corrido: ' + t.slice(0, 24), erro: e.inkW - medida });
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

  /*@@PRANCHAS@@*/
})();
