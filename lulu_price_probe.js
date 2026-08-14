// Query Lulu's own pricing resolver (the one www.lulu.com/pricing uses).
//
// Usage:
//   SKUS="0850X0850FCPRECW080CW444GXX" PAGES="40,60" CURR="USD,GBP,EUR" node lulu_price_probe.js
//
// SKU grammar: trim + colour(FC|BW) + quality(PRE|STD) + binding(CW|PB|LW)
//              + paper(080CW444|060UW444) + finish(G|M) + linen flag + foil flag
// Results as of 14 Aug 2026 are recorded in CANDIDATE_64_REBUILD.md, appendix.
const Q = `query manufacturingCost($podPackageId: String!, $pageCount: Int!, $currency: CurrencyEnum) {
  manufacturingCost(podPackageId: $podPackageId, pageCount: $pageCount, currency: $currency) { amount currency }
}`;

async function cost(sku, pages, currency) {
  const r = await fetch('https://api.lulu.com/graphql/', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'apollographql-client-name': 'lulu-website',
      'origin': 'https://www.lulu.com',
      'referer': 'https://www.lulu.com/',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
    },
    body: JSON.stringify({ operationName: 'manufacturingCost', query: Q,
                           variables: { podPackageId: sku, pageCount: pages, currency } }),
  });
  const j = await r.json().catch(() => ({ raw: r.status }));
  if (j.errors) return `ERR ${j.errors.map(e => e.message).join('; ').slice(0, 110)}`;
  const m = j.data && j.data.manufacturingCost;
  return m ? `${m.amount} ${m.currency}` : JSON.stringify(j).slice(0, 140);
}

const SKUS = (process.env.SKUS || '').split(',').filter(Boolean);
const PAGES = (process.env.PAGES || '40,60').split(',').map(Number);
const CURR = (process.env.CURR || 'USD').split(',');

(async () => {
  for (const sku of SKUS) {
    for (const p of PAGES) {
      for (const c of CURR) {
        console.log(`${sku}  ${String(p).padStart(3)}pp  ${c}  ->  ${await cost(sku, p, c)}`);
      }
    }
  }
})();
