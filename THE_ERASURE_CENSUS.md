# THE ERASURE HUNT — 12 registers tested, one survivor, three laws

**The pattern:** an authority publishes only *today's* state and never publishes what left. The change-log is
then the one artefact the holder will never produce — **provided nobody else is already capturing it.** This
hunt tested that proviso, and the proviso is where almost everything died.

**Result: six registers with publisher-side erasure verified by direct test, and exactly ONE that survives
every subsequent test. The three laws below are worth more than the survivor.**

---

## 1. ★★ THE THREE LAWS

> ### **★ THE UKGWA LAW — THE UNITED KINGDOM IS CLOSED, AND IT IS CLOSED BY ITS OWN ARCHIVE.**
>
> The National Archives' **UK Government Web Archive already runs this product, for free, on every UK
> public-body register.** It captures the **bulk data attachments**, not only the pages — and on high-value
> registers **it crawls MORE OFTEN THAN THE REGISTER UPDATES.**
>
> **Measured on the Register of Licensed Sponsors:** UKGWA holds **1.867 mementos** (2014-03-20 → 2026-08-12).
> Crawls per year 2020–2025: **231 · 270 · 269 · 250 · 261 · 263.** gov.uk's own change log for the same years:
> **240 · 227 · 232 · 239 · 244 · 247.** *The archive out-paces the publisher.* Of 6 sampled historical editions
> carrying a CSV link, **6 were present**, and replaying the 2024-06-03 edition returned real bytes —
> **9.820.633 bytes, 114.629 rows, 101.208 distinct organisations**, against 142.790 / 127.295 today.
> **Confirmed independently on CQC:** the May-2024 directory 404s on `cqc.org.uk` and UKGWA replays it in full
> (**17.761.801 bytes, 53.743 lines**).
>
> **The Internet Archive is not the adversary in the UK. UKGWA is, and it is far more thorough. ANY candidate
> whose bulk file sits on a gov.uk or UK public-body domain is DEAD ON ARRIVAL.**
>
> **The one thing UKGWA cannot do is capture a POST-only or session-gated result set** — which is exactly the
> shape of the only survivor.

> ### **★ THE CONDITIONAL-LICENCE KILL — FREE TO READ IS NOT FREE TO KEEP. Check the licence file inside the ZIP before celebrating.**
>
> The Environment Agency registers produced **the cleanest erasure evidence in this entire file** — and died on
> a 760-byte text file shipped inside the download:
>
> > *"You may use the Information for your internal or personal purposes and may only sublicense others to use
> > it if you do so under a written licence which includes the terms of these conditions… and in particular
> > **may not allow any period of use longer than the period licensed to you. 2) The period of permitted use is
> > one year.**"*
>
> **A one-year permitted-use window with restricted sublicensing is directly incompatible with a business whose
> entire asset is a multi-year private archive resold to third parties.** A five-second test that killed the
> two best-evidenced registers in the census.

> ### **★ THE POST-ONLY TEST — "is the result set reachable ONLY by POST?" is the fastest archive-proofness test available, and it is a STRUCTURAL guarantee rather than a probabilistic one.**
>
> No crawler — Internet Archive, UKGWA, Common Crawl — captures a POST result set behind a session cookie.
> **This does not depend on any archive being reachable to check, which matters because in practice they often
> are not.** The survivor below survives because it is POST-only, not because Canada is special.

---

## 2. THE CENSUS

| REGISTER | AUTHORITY | BULK? | **KEEPS HISTORY?** | WHO IS HURT | EMAIL? | VERDICT |
|---|---|---|---|---|---|---|
| **Medical Device Establishment Licence (MDEL)** | Health Canada | **No — POST only** | **NO — *"Only active MDELs will appear"*** | Foreign manufacturer whose Canadian importer loses market access (MDR s.44) | **No** | **★ THE ONLY SURVIVOR** |
| Waste Carriers, Brokers & Dealers (England) | Environment Agency | Yes | **NO — 0 of 145.864 expiry dates are in the past** | Waste producer (EPA 1990 s.34) | No | **Killed — licence terms** |
| Waste Exemptions (England) | Environment Agency | Yes | **NO — 22 of 118.462 past-dated, all yesterday** | Landowner/operator | No | **Killed — licence terms** |
| Register of Licensed Sponsors (Workers) | Home Office | Yes | **NO — historical asset URLs 301 to today's file, identical md5** | **Sponsored worker — visa curtailed.** Best hurt-party in the census | No | **Killed twice — UKGWA + a live vendor** |
| Register of Licensed Sponsors (Students) | Home Office | Yes | **NO — 1 attachment, 2.981 updates** | Sponsored student | No | Killed — UKGWA |
| CQC Care Directory | CQC | Yes | **NO — prior editions 404** | Commissioners, families | No | Killed — UKGWA |
| Scrap Metal Dealers (England) | Environment Agency | Yes | **YES — retains ~2 years expired** | — | — | Eliminated |
| OTI / NVOCC licences | US FMC | Yes | **YES — publishes "ALL OTI History"** | — | — | Eliminated |
| Licensed Natural Health Products | Health Canada | Search | **YES — live status field** | — | — | Eliminated |
| Medical Devices Active Licence Listing (MDALL) | Health Canada | Yes + API | **YES — *"or have been licensed in the past"*** | — | — | Eliminated |
| Approved alcohol wholesalers (AWRS) | HMRC | **No — lookup by URN only** | Untested | Alcohol trade buyer | — | **Not enumerable ⇒ she cannot build the series either** |
| Accredited registrars | ICANN | Web page | Publishes termination notices | — | — | Eliminated |

**Note the deliberate asymmetry inside one agency:** Health Canada's MDALL explicitly retains devices *"or have
been licensed in the past"*, and LNHPD carries a live status field taking *active / discontinued / stop sale /
cancelled / suspended*. **It archives status where it chose to and erases it on MDEL.** Verified, not assumed.

---

## 3. THE SURVIVOR — Health Canada MDEL, and its one fatal weakness

`https://health-products.canada.ca/mdel-leim/` — **no bulk file, no API, no download link.** Access is a POST to
`/mdel-leim/dispatch-mdel-repartition-lepim.do` carrying a `jsessionid`. Returned columns: **licence number,
company id, company name and address. Nothing else** — no issue date, no status, no expiry, no email.

**Erasure stated by the authority itself:** *"**Only active MDELs will appear in this listing.** An
establishment remains active on the MDEL listing unless: Health Canada has suspended or cancelled the MDEL for
failure to comply… [or] the company requested that the MDEL be cancelled."*

**Archive risk: structurally zero.** The GET page contains no listing; the result set exists only behind a POST
with a session cookie. **This is the one candidate where the Internet Archive check does not need to succeed,
because the register is un-crawlable by construction.**

**Cost to operate:** ~250 POSTs for a full census (the country dropdown holds ~250 values). No browser
automation, no per-record cost. Observed: Canada ~2.122 rows · USA ~664 · China 123 · Germany 30 · UK 24 ·
**Brazil 2.** A few thousand licence holders total.

**Who is hurt:** *Medical Devices Regulations* SOR/98-282 **s.44** — *"No person shall import or sell a medical
device… unless the person holds an establishment licence."* **s.51.1** mandates cancellation after 12 months'
suspension. The party hurt is the **foreign manufacturer whose Canadian importer just lost its licence.** And
Health Canada states it *"does not maintain a list of products… under an MDEL"*, so **the disappearance is
invisible from the product side — nobody can reconstruct it.**

> **★ AND IT DIES ON THE SAME WALL AS EVERYTHING ELSE: the register publishes company name and postal address,
> ZERO email addresses. `THE POSTAL LIST LAW`, on register twelve. The moat is real and the front door is
> bricked up — which is now the third candidate in two days to die in exactly this way** *(ISO certificate
> directories, SEC Form ADV's 243 email-free columns, and now MDEL)*.

**Competitor sweep: UNVERIFIED — not run systematically.**

---

## 4. ★★ WHAT THIS DOES TO THE DECRS ARCHIVE I STARTED THIS MORNING — a correction

**`STATE_OF_PLAY_19AUG.md` claims day 0 of the DECRS change-log is *"the one action of the day that cannot be
taken later"* and that the change-log *"cannot be back-filled."* Both need qualifying, and one is too strong.**

**1. DECRS FAILS THE POST-ONLY TEST — comprehensively.** It is a static `.zip` at a stable URL fetched by plain
GET on a government domain, updated daily. **That is the single most crawlable shape there is.** MDEL survives
because it is POST-only; DECRS has **no structural archive protection whatsoever.** The only question is
whether anyone bothered to crawl it — and that is a question about someone else's behaviour, not a guarantee.

**2. I COULD NOT ANSWER THAT QUESTION. `web.archive.org` is blocked from this container — HTTP 403 "Blocked by
egress policy" via curl AND unreachable via the fetch tool. `archive.ph` connection-reset. Common Crawl does
not index `.zip`. ARCHIVE RISK FOR DECRS IS UNVERIFIED, and it is the question that decides whether the archive
has any value at all.** *(The same block defeated the erasure hunt, which is why every "no IA copy" claim in
this census is likewise UNVERIFIED.)*

**3. A historical point DOES exist in the wild.** [John Snow Labs sells a *Drug Establishment Annual
Registration Status* dataset](https://www.johnsnowlabs.com/marketplace/drug-establishment-annual-registration-status/)
carrying `FEI_Number · DUNS_Number · Firm_Name · Address · Operations` — **temporal coverage 2020, last
modified 9 April 2020, update frequency "Irregular."**

> **So the precise position is: NO VENDOR HOLDS THE CHANGE-LOG — John Snow Labs' is a point-in-time snapshot,
> not a series — BUT at least one historical point is publicly purchasable. NET CHANGE over six years is
> therefore back-fillable by anyone; THE SEQUENCE IS NOT.**
>
> **"Nobody can back-fill it" was too strong. "Nobody can back-fill the ORDER AND DATES of the changes" is
> what the evidence supports.** *(Note also that the John Snow Labs extract carries no email — so the
> distribution asset is not in it.)*

**Day 0 still cost nothing and is still worth having.** But it is now explicitly contingent on an unanswered
question, and **that question — "has the Wayback Machine been capturing `drls_reg.zip`?" — is a two-minute job
for anyone with an unblocked browser and should be answered before one more hour goes into DECRS.**

---

## 5. HONEST LIMITS OF THIS CENSUS

- **The Internet Archive check requested in the brief was never completed** — egress-blocked and rate-limited.
  Where possible UKGWA was substituted, which for UK sources is the **stricter** test. **Every "no IA copy"
  claim here is UNVERIFIED.**
- **Australia is entirely unassessed** — every `.gov.au` host returned 403 from the same WAF, via curl and
  fetch alike. AUSTRAC, NDIS, Dept of Agriculture and TGA all unreached.
- **Brazil is largely unassessed** — `gov.br` is reachable but ANVISA's `consultas` is Cloudflare-blocked.
  **★ Brazil has no UKGWA-equivalent, which makes it the single most promising unexplored jurisdiction for
  this pattern** — and it is where the next pass should go.
- **NANDO, EUDAMED and USDA Organic Integrity are UNVERIFIED** — JavaScript SPAs whose APIs were not located.
  *(The Etsy failure mode, now on its fourth appearance.)*

## 6. WHAT TO TEST NEXT, IN ORDER

1. **Answer the DECRS archive question.** Two minutes, unblocked browser. It gates everything above.
2. **Brazil** — ANVISA AFE holders and MAPA export-eligible establishments, from a path that clears Cloudflare.
   No national web archive, delisting is catastrophic, **and the hurt party is an exporter — a business with a
   website and an inbox**, which is the wall every other candidate here died on.
3. **The POST-only species generally.** It is a structural guarantee, cheap to test, and independent of whether
   any archive is reachable.
