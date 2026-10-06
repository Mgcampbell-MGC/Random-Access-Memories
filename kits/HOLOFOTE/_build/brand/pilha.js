/* HOLOFOTE · pilha vertical (cartaz, boletim, C07…). Requer holofote.js.
 *
 * HF.pilha(parent, itens, caixa) monta uma coluna de linhas que enchem a medida (regra 2) e distribui a sobra de
 * altura pelos itens com 'flex'. Cada item:
 *   {tipo:'cheia', s:{t,f,...}, modo:'tamanho'|'wdth'|'tracking', capMax?, antes?, flex?}
 *   {tipo:'dividida', esq:{...}, dir:{...}, antes?, encher?}   L/R que enche a medida (encher: {modo:'wdth'|'tamanho', folga})
 *   {tipo:'pontilhada', esq:{...}|null, dir:{...}, opt?, antes?} com pontilhado (§C.3)
 *   {tipo:'regua', esp, cor, antes?}
 *   {tipo:'headliner', nome, capRef, cor, coracao?, antes?}     escada de encaixe §C.10 aplicada à medida
 *   {tipo:'assinatura', esq:{lockup}, marca:{ink, lamp, acesos?}, antes?}  "holofote nela." ← → wordmark
 *   {tipo:'bloco', h, desenhar:(parent,x0,x1,top)=>{}, antes?}  altura fixa (miniatura, reserva)
 *   {tipo:'espaco', flex}
 * 'antes' = espaço antes do item (px). 'flex' = peso para receber a sobra.
 * Itens com 'fundo:true' ficam colados na base da caixa (a sobra entra antes do primeiro deles).
 */
(function () {
  const M = window.HF_METRICAS;
  function extensoes(o) {
    // topo da tinta (acentos) e fundo da tinta (descendentes) relativos à linha de base
    let top = 0, bot = 0;
    for (const ch of o.s.t) {
      const g = HF.gm(o.s, ch);
      if (!g) continue;
      top = Math.max(top, g[4]);
      bot = Math.min(bot, g[3]);
    }
    const k = o.s.fs / M[o.s.f].upm;
    return { top: top * k, bot: -bot * k };
  }
  HF.extensoes = extensoes;

  // escada de encaixe do headliner (§C.10) numa medida qualquer; capRef = altura de versal de referência
  HF.escada = function (parent, nome, x0, x1, capRef, cor, coracao) {
    const medida = x1 - x0;
    const capC = (c) => c;
    const cora = coracao ? { gap: capRef * 0.22, w: capRef * 1.1 } : null;
    const mText = (cap) => (cora ? medida - (cap / capRef) * (cora.gap + cora.w) : medida);
    const sX = { t: nome, f: 'X', fs: HF.fsDeCap('X', capRef), lsEm: -0.01, cor };
    // passo 1: Expanded One à altura de referência, tracking até +200 para encher; se faltar, centraliza
    let o = HF.texto(parent, sX);
    if (o.inkW <= mText(capRef)) {
      HF.porTracking(o, mText(capRef), 0.2);
      return fim(o, 1, o.inkW < mText(capRef) - 0.5 ? 'centro' : 'cheia', capRef);
    }
    o.el.remove();
    // passo 2: Special Gothic 700, wdth resolvido de 124 a 75
    o = HF.texto(parent, { t: nome, f: 'V', wght: 700, wdth: 124, fs: HF.fsDeCap('V', capRef), cor });
    HF.mudar(o, { wdth: 124 });
    if (o.inkW > mText(capRef)) {
      HF.mudar(o, { wdth: 75 });
      if (o.inkW <= mText(capRef)) {
        let lo = 75, hi = 124;
        for (let i = 0; i < 22; i++) { const m = (lo + hi) / 2; HF.mudar(o, { wdth: m }); if (o.inkW > mText(capRef)) hi = m; else lo = m; }
        HF.mudar(o, { wdth: lo });
        HF.porTracking(o, mText(capRef));
        return fim(o, 2, 'cheia', capRef);
      }
    }
    o.el.remove();
    // passo 3: Condensed One à altura de referência
    o = HF.texto(parent, { t: nome, f: 'C', fs: HF.fsDeCap('C', capRef), cor });
    if (o.inkW <= mText(capRef)) { HF.porTracking(o, mText(capRef), 0.2); return fim(o, 3, 'cheia', capRef); }
    // passo 4: Condensed One reduzida (mínimo 12/17,8 da referência), alinhada pela base
    for (let i = 0; i < 6; i++) {
      const cap = HF.capPx(o.s);
      HF.mudar(o, { fs: o.s.fs * mText(cap) / o.inkW });
    }
    const cap4 = HF.capPx(o.s);
    if (cap4 >= capRef * (12 / 17.8)) return fim(o, 4, 'cheia', cap4);
    o.el.remove();
    // passo 5: duas linhas em Condensed One a 8,4/17,8, quebra num espaço
    const partes = nome.split(' ');
    if (partes.length >= 2) {
      const capL = capRef * (8.4 / 17.8);
      let melhor = null;
      for (let k = 1; k < partes.length; k++) {
        const a = partes.slice(0, k).join(' '), b = partes.slice(k).join(' ');
        const oa = HF.texto(parent, { t: a, f: 'C', fs: HF.fsDeCap('C', capL), cor });
        const ob = HF.texto(parent, { t: b, f: 'C', fs: HF.fsDeCap('C', capL), cor });
        const ok = oa.inkW <= medida && ob.inkW <= mText(capL);
        if (ok && (!melhor || Math.abs(oa.inkW - ob.inkW) < melhor.d)) { if (melhor) { melhor.a.el.remove(); melhor.b.el.remove(); } melhor = { a: oa, b: ob, d: Math.abs(oa.inkW - ob.inkW) }; }
        else { oa.el.remove(); ob.el.remove(); }
      }
      if (melhor) {
        HF.porTracking(melhor.a, medida, 0.2);
        HF.porTracking(melhor.b, mText(capL), 0.2);
        return { passo: 5, linhas: [melhor.a, melhor.b], cap: capL, cora };
      }
    }
    // passo 6: recusa
    return { passo: 6, recusa: 'esse nome não cabe no cartaz. tenta um apelido?' };
    function fim(o, passo, estado, cap) { return { passo, linhas: [o], estado, cap, cora }; }
  };

  HF.pilha = function (parent, itens, cx) {
    const x0 = cx.x0, x1 = cx.x1, medida = x1 - x0;
    const QA = (window.HF_QA = window.HF_QA || []);
    // 1. cria e encaixa na horizontal; mede alturas
    for (const it of itens) {
      it.antes = it.antes || 0;
      if (it.tipo === 'cheia') {
        const o = HF.texto(parent, Object.assign({}, it.s));
        if (it.modo === 'wdth') {
          HF.porWdth(o, medida);
          if (o.estado === 'longo') { HF.mudar(o, { wdth: 75 }); HF.porTamanho(o, medida); }
          if (o.estado === 'curto') { HF.mudar(o, { wdth: 125 }); HF.porTamanho(o, medida); }   // cresce, nunca espaceja
        } else if (it.modo === 'tracking') HF.porTracking(o, medida);
        else if (it.modo === 'auto') {
          // Produção que enche: começa condensada (V 500 wdth 75 = a Condensed One) e enche por tamanho; se passar do
          // teto de versal, trava o tamanho no teto e alarga pelo eixo wdth; se nem a 125 encher, cresce por tamanho.
          HF.mudar(o, { wdth: 75 });
          HF.porTamanho(o, medida);
          if (it.capMax && HF.capPx(o.s) > it.capMax) {
            HF.mudar(o, { fs: HF.fsDeCap(o.s.f, it.capMax) });
            HF.porWdth(o, medida);
            if (o.estado === 'curto') { HF.mudar(o, { wdth: 125, lsEm: 0 }); HF.porTamanho(o, medida); }
          }
        }
        else HF.porTamanho(o, medida, it.capMax ? (it.capMax * M[o.s.f].upm) / M[o.s.f].cap : null);
        it.objs = [o];
        const e = extensoes(o);
        it.top = it.topFix != null ? it.topFix : e.top; it.bot = e.bot; it.al = it.alinhar || 'left';
        QA.push({ item: o.s.t, erro: it.modo === 'tamanho' && it.capMax ? 0 : o.inkW - medida, cap: +HF.capPx(o.s).toFixed(1), wdth: o.s.wdth });
      } else if (it.tipo === 'dividida' || it.tipo === 'pontilhada') {
        const a = it.esq ? HF.texto(parent, Object.assign({}, it.esq)) : null;
        const b = HF.texto(parent, Object.assign({}, it.dir));
        // 'encher': a coluna da esquerda enche a medida menos a da direita e uma folga (px), pelo eixo wdth (cai para o
        // tamanho se nem 75 nem 125 resolverem). Ex.: "INGRESSOS COM" (Locutor) ← → "você." (a Fã), no C01.
        if (it.encher && a) {
          const alvo = medida - b.inkW - it.encher.folga;
          if (it.encher.modo === 'tamanho') HF.porTamanho(a, alvo);
          else {
            HF.porWdth(a, alvo);
            if (a.estado === 'longo') { HF.mudar(a, { wdth: 75 }); HF.porTamanho(a, alvo); }
            if (a.estado === 'curto') { HF.mudar(a, { wdth: 125 }); HF.porTamanho(a, alvo); }
          }
          QA.push({ item: 'encher ' + a.s.t, erro: a.inkW - alvo, wdth: a.s.wdth, cap: +HF.capPx(a.s).toFixed(1) });
        }
        it.objs = [a, b].filter(Boolean);
        const es = it.objs.map(extensoes);
        it.top = Math.max(...es.map((e) => e.top)); it.bot = Math.max(...es.map((e) => e.bot));
      } else if (it.tipo === 'headliner') {
        const r = HF.escada(parent, it.nome, x0, x1, it.capRef, it.cor, it.coracao);
        it.r = r;
        if (r.recusa) {
          const o = HF.texto(parent, { t: r.recusa, f: 'C', fs: HF.fsDeCap('C', it.capRef * 0.2), cor: it.cor });
          it.objs = [o]; const e = extensoes(o); it.top = e.top; it.bot = e.bot;
        } else {
          it.objs = r.linhas;
          const es = r.linhas.map(extensoes);
          it.passoLinha = r.cap * 1.48;
          it.top = es[0].top; it.bot = es[es.length - 1].bot + (r.linhas.length - 1) * it.passoLinha;
        }
      } else if (it.tipo === 'assinatura') {
        const a = HF.texto(parent, Object.assign({}, it.esq));
        // "holofote nela." à esquerda, wordmark à direita (largura = 9,273 × versal): se não couberem com folga de
        // 1,5 versal, os dois encolhem juntos, na mesma proporção
        const WMk = (window.HF_WORDMARK.inkX1 - window.HF_WORDMARK.inkX0) / window.HF_WORDMARK.cap;
        const capM = it.capMarca || HF.capPx(a.s);
        const folga = Math.max(24, 1.5 * capM);
        const need = a.inkW + WMk * capM + folga;
        if (need > medida) {
          const k = (medida - folga) / (a.inkW + WMk * capM);
          HF.mudar(a, { fs: a.s.fs * k });
          it.capMarca = capM * k;
        }
        it.objs = [a];
        const e = extensoes(a); it.top = e.top; it.bot = e.bot;
      } else if (it.tipo === 'regua') { it.top = it.esp / 2; it.bot = it.esp / 2; }
      else if (it.tipo === 'bloco') { it.top = 0; it.bot = it.h; }
      else if (it.tipo === 'espaco') { it.top = 0; it.bot = 0; }
    }
    // passo fixo de linha de base (listas): antes = passo − fundo do anterior − topo deste
    itens.forEach((it, i) => { if (it.passo && i > 0) it.antes = Math.max(0, it.passo - itens[i - 1].bot - it.top); });
    // 2. distribui a sobra
    let total = 0;
    for (const it of itens) total += it.antes + it.top + it.bot;
    let sobra = cx.y1 - cx.y0 - total;
    const pesos = itens.reduce((s, it) => s + (it.flex || 0), 0);
    if (sobra < -0.5) console.warn('pilha: falta altura', sobra.toFixed(1));
    if (pesos > 0 && sobra > 0) for (const it of itens) it.antes += (sobra * (it.flex || 0)) / pesos;
    // 3. posiciona
    // a posição corre SEM arredondar (y) e cada linha de base é arredondada para a grade sozinha: antes o erro de cada
    // arredondamento entrava na linha seguinte e somava (revisão do CCO, 6 out 2026: a assinatura dos B variava 16 px
    // entre cartões e saía da caixa segura). A última linha arredonda para baixo se passar do fim da caixa.
    let y = cx.y0;
    const grade = cx.grade || 0;          // grade de linha de base (px): 8 nas peças digitais (§D.10)
    const ultimo = [...itens].reverse().find((it) => it.tipo !== 'espaco' && it.tipo !== 'bloco');
    itens.forEach((it, i) => {
      y += it.antes;
      const bruto = y + it.top;
      let base = bruto;
      const ant = itens[i - 1];
      if (it.passo && ant && ant.passoLista) base = ant.baseline + it.passo;      // lista de passo fixo: passo exato
      else if (grade && it.tipo !== 'bloco' && it.tipo !== 'espaco') {
        base = Math.round(bruto / grade) * grade;
        if (it === ultimo && base + it.bot > cx.y1 + 2) base = Math.floor((cx.y1 - it.bot + 2) / grade) * grade;   // 2 px: o overshoot do O
      }
      it.passoLista = !!(it.passo || (itens[i + 1] && itens[i + 1].passo));
      it.baseline = base;
      if (it.tipo === 'cheia') HF.posicionar(it.objs[0], it.al === 'right' ? x1 : x0, base, it.al);
      else if (it.tipo === 'dividida') {
        const [a, b] = it.objs;
        HF.posicionar(a, x0, base, 'left'); HF.posicionar(b, x1, base, 'right');
        if (a.inkX1 > b.inkX0 - 8) console.warn('dividida: colisão', a.s.t, b.s.t);
      } else if (it.tipo === 'pontilhada') {
        it.objs.forEach((o) => o.el.remove());
        it.p = HF.pontilhada(parent, it.esq, it.dir, x0, x1, base, it.opt);
      } else if (it.tipo === 'headliner') {
        const r = it.r;
        if (r.recusa) HF.posicionar(it.objs[0], x0, base, 'left');
        else {
          r.linhas.forEach((o, i) => {
            const al = r.estado === 'centro' ? 'center' : 'left';
            const larg = r.cora ? o.inkW + (r.cap / it.capRef) * (r.cora.gap + r.cora.w) : o.inkW;
            const xx = al === 'center' ? x0 + (medida - larg) / 2 : x0;
            HF.posicionar(o, xx, base + i * it.passoLinha, 'left');
            QA.push({ item: 'headliner ' + o.s.t + ' passo ' + r.passo, erro: r.estado === 'centro' ? 0 : (i === r.linhas.length - 1 && r.cora ? larg : o.inkW) - medida });
          });
          if (r.cora) {
            const ult = r.linhas[r.linhas.length - 1];
            const k = r.cap / it.capRef;
            HF.coracao(parent, ult.inkX1 + r.cora.gap * k, base + (r.linhas.length - 1) * it.passoLinha, r.cap, it.cor);
          }
        }
      } else if (it.tipo === 'assinatura') {
        const a = it.objs[0];
        HF.posicionar(a, x0, base, 'left');
        const capWm = it.capMarca || HF.capPx(a.s) * 1.0;
        it.wm = HF.wordmark(parent, Object.assign({ x: x1, baseline: base, cap: capWm, align: 'right' }, it.marca));
      } else if (it.tipo === 'regua') HF.regua(parent, x0, x1, base, it.esp, it.cor);
      else if (it.tipo === 'bloco') it.desenhar(parent, x0, x1, y);
      y = (it.passo && ant && ant.passoLista ? base : bruto) + it.bot;
    });
    return itens;
  };
})();
