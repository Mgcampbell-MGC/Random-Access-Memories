/* HOLOFOTE · motor de layout dos templates (plataforma §D.2–D.5).
 *
 * Toda linha é medida NA TINTA: largura do DOM − side-bearing esquerdo do 1º glifo − side-bearing direito do último
 * (tabela em metricas.js, medida nos arquivos de fonte). Assim "toda linha ocupa a largura inteira" fecha em ±0,5 px
 * na borda do desenho da letra, não na caixa de avanço.
 *
 * Fontes (s.f):  'X' Expanded One (Locutor) · 'C' Condensed One (Produção) · 'V' Special Gothic variável
 *                (s.wght, s.wdth) · 'S' Shantell Sans 500 / INFM 60 / BNCE 0 (a Fã).
 * Tamanho:       s.fs em px (font-size). s.lsEm = tracking em em (ex.: 0.08 = +80); s.tnum = algarismos tabulares.
 * Posição:       pela LINHA DE BASE e pela borda da tinta.
 */
(function () {
  const M = window.HF_METRICAS, WM = window.HF_WORDMARK;
  const HF = (window.HF = {});
  HF.cor = { preto: '#121014', papel: '#FFF8EC', amarelo: '#FFE81A', rosa: '#FF4FA0', laranja: '#FF6A1A',
    violeta: '#8424F5', luz: '#FFE9C4', cera: '#F3E9D6', croma: '#0047BB' };
  // tinta por cor de fundo (pares medidos §D.1): preto sobre amarelo/rosa/laranja/papel; papel sobre violeta/preto
  HF.tinta = { amarelo: 'preto', rosa: 'preto', laranja: 'preto', papel: 'preto', violeta: 'papel', preto: 'papel' };
  HF.faixa = {
    amarelo: { show: 'AO VIVO', faixa: 'FAIXA 02', descr: 'rosas no palco, luz quente', wdth: 125 },
    rosa: { show: 'CAMARIM', faixa: 'FAIXA 01', descr: 'pó de arroz e batom', wdth: 106 },
    laranja: { show: 'MAIS UM!', faixa: 'FAIXA 03', descr: 'laranja, cacau e mais um pouco', wdth: 111 },
    violeta: { show: 'ACÚSTICO', faixa: 'FAIXA 04', descr: 'voz e violão, luz baixa', wdth: 102 },
  };
  HF.placeholders = [];
  const FAM = { X: "'SG Expanded'", C: "'SG Condensed'", V: "'SG'", S: "'Shantell'" };
  const C = (c) => HF.cor[c] || c;

  function ls(s) { return s.lsEm != null ? s.lsEm * s.fs : (s.ls || 0); }
  function aplicar(el, s) {
    el.style.fontFamily = FAM[s.f];
    el.style.fontSize = s.fs + 'px';
    if (s.f === 'V') el.style.fontVariationSettings = `'wght' ${s.wght || 700}, 'wdth' ${s.wdth || 100}`;
    else if (s.f === 'S') el.style.fontVariationSettings = `'wght' ${s.wght || 500}, 'INFM' ${s.infm == null ? 60 : s.infm}, 'BNCE' 0, 'SPAC' 0`;
    else el.style.fontVariationSettings = 'normal';
    el.style.letterSpacing = ls(s) + 'px';
    el.style.fontFeatureSettings = s.tnum ? "'kern' 1, 'tnum' 1, 'lnum' 1" : "'kern' 1";
    el.style.color = C(s.cor || 'preto');
    if (s.op != null) el.style.opacity = s.op;
  }
  // métrica de glifo [adv, xMin, xMax, yMin, yMax] em unidades (interpola wdth no variável)
  function gm(s, ch) {
    if (s.f === 'V') {
      // interpola wdth (passo 1) e wght (tabelas 400 e 700; os contornos do VF são lineares entre os mestres)
      const w = Math.max(75, Math.min(125, s.wdth || 100)), wg = Math.max(400, Math.min(700, s.wght || 700));
      const a = Math.floor(w), b = Math.min(125, a + 1), f = w - a;
      const em = (t) => { const ga = t[a][ch], gb = t[b][ch]; return ga ? ga.map((v, i) => v + (gb[i] - v) * f) : null; };
      // mestres de peso 400 · 500 · 700 (o VF tem um mestre intermediário: interpolar 400→700 direto erra)
      const [p0, p1] = wg <= 500 ? [400, 500] : [500, 700];
      const ga = em(M.V.g[p0]), gb = em(M.V.g[p1]);
      if (!ga || !gb) return gb || ga || null;
      const k = (wg - p0) / (p1 - p0);
      return ga.map((v, i) => v + (gb[i] - v) * k);
    }
    return M[s.f].g[ch] || null;
  }
  HF.gm = gm;
  HF.capPx = (s) => (M[s.f].cap * s.fs) / M[s.f].upm;
  HF.xPx = (s) => (M[s.f].x * s.fs) / M[s.f].upm;
  HF.fsDeCap = (f, capPx) => (capPx * M[f].upm) / M[f].cap;      // font-size que dá a altura de versal pedida
  HF.fsDeX = (f, xPx) => (xPx * M[f].upm) / M[f].x;               // font-size que dá a altura-x pedida
  // topo real da tinta (acentos incluídos) em px acima da linha de base
  HF.topoTinta = function (s) {
    let top = 0;
    for (const ch of s.t) { const g = gm(s, ch); if (g) top = Math.max(top, g[4]); }
    return (top * s.fs) / M[s.f].upm;
  };

  function medir(o) {
    const s = o.s, u = s.fs / M[s.f].upm, chars = [...s.t];
    const dr = o.el.getBoundingClientRect(), r = o.sp.getBoundingClientRect(), pr = o.pr.getBoundingClientRect();
    const g0 = gm(s, chars[0]), g1 = gm(s, chars[chars.length - 1]);
    o.adv = r.width;
    o.lead = g0 ? g0[1] * u : 0;
    o.trail = g1 ? (g1[0] - g1[2]) * u : 0;
    o.lsPx = ls(s);
    o.inkW = o.adv - o.lsPx - o.lead - o.trail;
    o.spanOff = r.left - dr.left;
    o.baseOff = pr.top - dr.top;
    o.n = chars.length;
    if (o.align) HF.posicionar(o, o.x, o.baseline, o.align);
    return o;
  }
  HF.texto = function (parent, s) {
    const d = document.createElement('div');
    d.className = 'hf-t';
    const sp = document.createElement('span');
    sp.textContent = s.t;
    const pr = document.createElement('span');
    pr.className = 'hf-probe';
    d.append(sp, pr);
    (parent || document.body).appendChild(d);
    const o = { el: d, sp, pr, s: Object.assign({ fs: 100, f: 'C' }, s) };
    aplicar(d, o.s);
    return medir(o);
  };
  HF.mudar = function (o, ch) { Object.assign(o.s, ch); aplicar(o.el, o.s); return medir(o); };
  HF.posicionar = function (o, x, baseline, align) {
    o.x = x; o.baseline = baseline; o.align = align || 'left';
    let inkLeftInDiv = o.spanOff + o.lead;
    let left;
    if (o.align === 'right') left = x - (inkLeftInDiv + o.inkW);
    else if (o.align === 'center') left = x - (inkLeftInDiv + o.inkW / 2);
    else left = x - inkLeftInDiv;
    o.el.style.left = left + 'px';
    o.el.style.top = baseline - o.baseOff + 'px';
    o.inkX0 = left + inkLeftInDiv;
    o.inkX1 = o.inkX0 + o.inkW;
    o.capTop = baseline - HF.capPx(o.s);
    o.inkTop = baseline - HF.topoTinta(o.s);
    return o;
  };
  // ---- preenchimento (regra 2) ----
  HF.porTamanho = function (o, medida, maxFs) {
    for (let i = 0; i < 6; i++) {
      let fs = (o.s.fs * medida) / o.inkW;
      if (maxFs && fs > maxFs) fs = maxFs;
      HF.mudar(o, { fs });
      if (Math.abs(o.inkW - medida) < 0.15 || fs === maxFs) break;
    }
    return o;
  };
  HF.porTracking = function (o, medida, maxEm) {
    if (o.n < 2) return o;
    for (let i = 0; i < 3; i++) {
      const add = (medida - o.inkW) / (o.n - 1);
      let em = (ls(o.s) + add) / o.s.fs;
      if (maxEm != null && em > maxEm) em = maxEm;
      HF.mudar(o, { lsEm: em, ls: undefined });
    }
    return o;
  };
  // wdth 75–125 a tamanho fixo; devolve 'curto' (mesmo a 125 não enche) ou 'longo' (nem a 75 cabe)
  HF.porWdth = function (o, medida) {
    HF.mudar(o, { wdth: 125 });
    if (o.inkW <= medida) { o.estado = o.inkW < medida - 0.5 ? 'curto' : 'ok'; return o; }
    HF.mudar(o, { wdth: 75 });
    if (o.inkW > medida + 0.5) { o.estado = 'longo'; return o; }
    let lo = 75, hi = 125;
    for (let i = 0; i < 22; i++) {
      const mid = (lo + hi) / 2;
      HF.mudar(o, { wdth: mid });
      if (o.inkW > medida) hi = mid; else lo = mid;
    }
    HF.mudar(o, { wdth: lo });
    if (Math.abs(o.inkW - medida) > 0.3 && o.n > 1) HF.porTracking(o, medida);
    o.estado = 'ok';
    return o;
  };
  // linha cheia: modo 'tamanho' | 'wdth' (cai para tamanho se não couber) | 'tracking'
  HF.cheia = function (parent, s, x0, x1, baseline, modo) {
    const o = HF.texto(parent, s), medida = x1 - x0;
    if (modo === 'wdth') {
      HF.porWdth(o, medida);
      if (o.estado === 'longo') { HF.mudar(o, { wdth: 75 }); HF.porTamanho(o, medida); }
      if (o.estado === 'curto') { HF.mudar(o, { wdth: 125 }); HF.porTamanho(o, medida); }   // nunca abre tracking
    } else if (modo === 'tracking') HF.porTracking(o, medida);
    else HF.porTamanho(o, medida);
    HF.posicionar(o, x0, baseline, 'left');
    o.erro = o.inkW - medida;
    return o;
  };
  HF.dividida = function (parent, esq, dir, x0, x1, baseline) {
    const a = HF.texto(parent, esq), b = HF.texto(parent, dir);
    HF.posicionar(a, x0, baseline, 'left');
    HF.posicionar(b, x1, baseline, 'right');
    a.par = b;
    return [a, b];
  };
  // pontilhado de tabela: "PREZINHO ....... PRIMEIRA FILA" (§C.3: ponto Condensed One, passo fixo, mínimo)
  HF.pontilhada = function (parent, esq, dir, x0, x1, baseline, opt) {
    opt = Object.assign({ passo: null, folga: null, f: 'C', cor: esq.cor, fs: esq.fs }, opt || {});
    const [a, b] = esq ? HF.dividida(parent, esq, dir, x0, x1, baseline) : [null, HF.texto(parent, dir)];
    if (!esq) HF.posicionar(b, x1, baseline, 'right');
    const ds = { t: '.', f: opt.f, fs: opt.fs, cor: opt.cor, op: opt.op };
    const g = gm(ds, '.'), u = ds.fs / M[ds.f].upm, dotW = (g[2] - g[1]) * u;
    const passo = opt.passo || ds.fs * 0.32, folga = opt.folga == null ? passo * 0.9 : opt.folga;
    const ini = (a ? a.inkX1 : x0 - folga) + folga, fim = b.inkX0 - folga;
    const n = Math.max(0, Math.floor((fim - ini - dotW) / passo) + 1);
    const pontos = [];
    if (n >= 2) {
      const p = (fim - ini - dotW) / (n - 1);
      for (let i = 0; i < n; i++) {
        const d = HF.texto(parent, Object.assign({}, ds));
        HF.posicionar(d, ini + i * p, baseline, 'left');
        pontos.push(d);
      }
    }
    return { a, b, pontos, lider: fim - ini };
  };
  HF.regua = function (parent, x0, x1, y, esp, cor) {
    const d = document.createElement('div');
    d.className = 'hf-r';
    Object.assign(d.style, { left: x0 + 'px', top: y - esp / 2 + 'px', width: x1 - x0 + 'px', height: esp + 'px', background: C(cor || 'preto') });
    parent.appendChild(d);
    return d;
  };
  HF.caixa = function (parent, x, y, w, h, estilo) {
    const d = document.createElement('div');
    d.className = 'hf-b';
    Object.assign(d.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' }, estilo || {});
    parent.appendChild(d);
    return d;
  };
  // ---- marca ----
  const NS = 'http://www.w3.org/2000/svg';
  function svg(parent, x, y, w, h, vb) {
    const s = document.createElementNS(NS, 'svg');
    s.setAttribute('viewBox', vb);
    s.setAttribute('width', w);
    s.setAttribute('height', h);
    Object.assign(s.style, { position: 'absolute', left: x + 'px', top: y + 'px', overflow: 'visible' });
    parent.appendChild(s);
    return s;
  }
  HF.svg = svg;
  function path(s, d, fill, rule) {
    const p = document.createElementNS(NS, 'path');
    p.setAttribute('d', d);
    p.setAttribute('fill', fill);
    if (rule) p.setAttribute('fill-rule', rule);
    s.appendChild(p);
    return p;
  }
  HF.path = path;
  /* wordmark: o = {x, baseline, cap | largura (na tinta), ink, lamp, acesos:[bool,bool,bool], align}
     acesos padrão = só o terceiro O. Lâmpada apagada = O vazado na cor da tinta. */
  HF.wordmark = function (parent, o) {
    const inkW = WM.inkX1 - WM.inkX0;
    const k = o.largura ? o.largura / inkW : o.cap / WM.cap;
    const w = inkW * k, top = -14, bot = 726, h = (bot - top) * k;
    let x = o.x;
    if (o.align === 'right') x -= w;
    if (o.align === 'center') x -= w / 2;
    const s = svg(parent, x, o.baseline - (WM.cap - top) * k, w, h, `${WM.inkX0} ${top} ${inkW} ${bot - top}`);
    const acesos = o.acesos || [false, false, true];
    for (const p of WM.partes) {
      if (p.d) { path(s, p.d, C(o.ink)); continue; }
      const O = WM.Os[p.o];
      if (acesos[p.o]) path(s, O.ext, C(o.lamp || 'amarelo'));
      else path(s, O.ext + ' ' + O.cont, C(o.ink), 'nonzero');
    }
    return { el: s, x0: x, x1: x + w, capTop: o.baseline - WM.cap * k, baseline: o.baseline, k, cap: WM.cap * k };
  };
  // O FOCO: disco d, elipse 2,4d × 0,8d, vão 0,5d (§D.3)
  HF.foco = function (parent, cx, top, d, cor) {
    const s = svg(parent, cx - 1.2 * d, top, 2.4 * d, 2.3 * d, `0 0 ${2.4 * d} ${2.3 * d}`);
    const c = document.createElementNS(NS, 'circle');
    c.setAttribute('cx', 1.2 * d); c.setAttribute('cy', d / 2); c.setAttribute('r', d / 2); c.setAttribute('fill', C(cor));
    const e = document.createElementNS(NS, 'ellipse');
    e.setAttribute('cx', 1.2 * d); e.setAttribute('cy', 1.5 * d + 0.4 * d); e.setAttribute('rx', 1.2 * d); e.setAttribute('ry', 0.4 * d); e.setAttribute('fill', C(cor));
    s.append(c, e);
    return s;
  };
  // coração vetorial (Special Gothic não tem ♥): em px, encaixado na altura de versal
  HF.coracao = function (parent, x, baseline, cap, cor) {
    const s = svg(parent, x, baseline - cap, cap * 1.1, cap, '0 0 110 100');
    path(s, 'M55 100 L8 50 C-6 35 0 6 26 2 C40 0 50 8 55 18 C60 8 70 0 84 2 C110 6 116 35 102 50 Z', C(cor));
    return s;
  };
  // espaço reservado para render/foto (hachurado, rotulado) — registrado em HF.placeholders para o JSON
  HF.reserva = function (parent, o) {
    const d = document.createElement('div');
    d.className = 'hf-ph' + (o.circulo ? ' hf-ph-c' : '');
    Object.assign(d.style, { left: o.x + 'px', top: o.y + 'px', width: o.w + 'px', height: o.h + 'px' });
    if (o.fundo) d.style.setProperty('--ph-bg', C(o.fundo));
    if (o.tinta) d.style.setProperty('--ph-ink', C(o.tinta));
    parent.appendChild(d);
    const lab = o.rotulo || 'RENDER';
    const t = HF.texto(d, { t: lab, f: 'C', fs: Math.max(16, Math.min(o.w, o.h) * 0.11), lsEm: 0.12, cor: o.tinta || 'preto' });
    t.el.classList.add('hf-ph-l');
    HF.posicionar(t, o.w / 2, o.h / 2 + HF.capPx(t.s) / 2, 'center');
    if (o.nota) {
      const n = HF.texto(d, { t: o.nota, f: 'C', fs: Math.max(12, Math.min(o.w, o.h) * 0.045), lsEm: 0.06, cor: o.tinta || 'preto' });
      n.el.classList.add('hf-ph-l');
      HF.posicionar(n, o.w / 2, o.h / 2 + HF.capPx(t.s) / 2 + HF.capPx(n.s) * 2.4, 'center');
    }
    HF.placeholders.push({ id: o.id, tipo: o.circulo ? 'circulo' : 'retangulo', x: o.x + (o.ox || 0), y: o.y + (o.oy || 0), w: o.w, h: o.h, rotulo: lab, conteudo: o.conteudo || '' });
    return d;
  };
  // dados: JSON no hash da URL (#{...}) sobre os padrões do template
  HF.dados = function (padrao) {
    let d = {};
    try { if (location.hash.length > 1) d = JSON.parse(decodeURIComponent(location.hash.slice(1))); } catch (e) { console.error(e); }
    return Object.assign({}, padrao, d);
  };
  HF.pronto = async function (fn) {
    await Promise.all(["100px 'SG Expanded'", "100px 'SG Condensed'", "100px 'SG'", "100px 'Shantell'"].map((f) => document.fonts.load(f, 'AÃÉÇãõ09.')));
    await document.fonts.ready;
    try { await fn(); } catch (e) { document.body.setAttribute('data-erro', String(e && e.stack || e)); console.error(e); }
    window.HF_PRONTO = true;
  };
})();
