#!/usr/bin/env python3
"""
GateLedger daily capture. One tool, fixed slugs, deterministic root.

Fixes four defects found on 21 Aug 2026 in the hand-run captures of 19-21 Aug:
  1. filename drift  - day 0 wrote yti_gate_schedule.html, day 1 wrote yti_gate.html.
                       A differ keyed on filename reads that as delete+recreate.
                       Slugs are now frozen in SOURCES and are the ONLY names written.
  2. dropped source  - the Maersk directory was captured on day 0 only. It is the one
                       source with verified erasure, so it is also the one that cannot
                       be back-filled. Now discovered by walking back MAERSK_LOOKBACK
                       days for the live edition.
  3. no daily token  - days 1 and 2 were banked without RFC 3161 tokens.
  4. flat concat hash mislabelled "merkle" - see ROOT CONSTRUCTION below.

ROOT CONSTRUCTION (v2, authoritative):
  leaf_i  = SHA256(raw bytes of source i), ordered by SLUG ascending (ASCII).
  parent  = SHA256(left || right) over 32-byte binary digests.
  odd node at a level is PROMOTED unchanged, never duplicated (duplication makes
  distinct trees collide - CVE-2012-2459).
  root.txt = lowercase hex of the root + "\n". Tokens are taken over root.txt.

  A Merkle root lets one source on one day be proven with log2(n) sibling hashes
  and WITHOUT disclosing the other sources. The v1 flat concatenation could not:
  proving anything meant handing over everything.
"""
import hashlib, json, os, subprocess, sys, datetime, urllib.request, gzip, tarfile, io

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
MAERSK_BASE = ("https://www.maersk.com/~/media_sc9/maersk/local-information/files/"
               "north-america/united-states-of-america/import")
MAERSK_LOOKBACK = 21

SOURCES = {                                     # slug -> url   (slug order == leaf order)
    "its_empty_receiving":     "https://www.itslb.com/itslb/empty-receiving-updates/",
    "pnct_empty_return":       "https://www.pnct.net/EmptyReturn",
    "trapac_la_empty_returns": "https://losangeles.trapac.com/empty-returns/",
    "yti_closed_area_matrix":  "https://lynx.yti.com/ClosedAreaMatrix.aspx",
    "yti_gate_schedule":       "https://yti.com/terminal-schedules/gate-schedule/",
}
TSAS = {"freetsa.org":            "https://freetsa.org/tsr",
        "timestamp.digicert.com": "http://timestamp.digicert.com",
        "tsa.izenpe.com":         "http://tsa.izenpe.com:8093",
        "timestamp.sectigo.com":  "http://timestamp.sectigo.com"}


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.status


def find_maersk(today):
    """Exactly one edition is live at a time; predecessors 404 permanently.
    Verified 21 Aug 2026: 13 of 14 consecutive dates returned 404, one returned 200."""
    for i in range(MAERSK_LOOKBACK):
        d = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"{MAERSK_BASE}/us-empty-return-locations-{d}.xlsx"
        try:
            body, status = fetch(url, timeout=90)
            if status == 200 and len(body) > 100_000:
                return d, url, body
        except Exception:
            continue
    return None, None, None


def merkle_root(leaves):
    lv = list(leaves)
    if not lv:
        return b""
    while len(lv) > 1:
        nxt = [hashlib.sha256(lv[i] + lv[i + 1]).digest() for i in range(0, len(lv) - 1, 2)]
        if len(lv) % 2:
            nxt.append(lv[-1])          # promote, never duplicate
        lv = nxt
    return lv[0]


def merkle_proof(leaves, idx):
    """Sibling path so ONE source can be proven without revealing the others."""
    lv, path = list(leaves), []
    while len(lv) > 1:
        nxt = []
        for i in range(0, len(lv) - 1, 2):
            if i == idx - (idx % 2) and idx < len(lv) - (len(lv) % 2):
                path.append({"side": "right" if idx % 2 == 0 else "left",
                             "hash": (lv[i + 1] if idx % 2 == 0 else lv[i]).hex()})
            nxt.append(hashlib.sha256(lv[i] + lv[i + 1]).digest())
        if len(lv) % 2:
            nxt.append(lv[-1])
        idx //= 2
        lv = nxt
    return path


def timestamp(path, outdir):
    got = {}
    tsq = os.path.join(outdir, "root.tsq")
    subprocess.run(["openssl", "ts", "-query", "-data", path, "-sha256", "-cert", "-out", tsq],
                   check=True, capture_output=True)
    for name, url in TSAS.items():
        out = os.path.join(outdir, f"{name}.tsr")
        r = subprocess.run(["curl", "-sS", "--max-time", "60", "-H",
                            "Content-Type: application/timestamp-query",
                            "--data-binary", f"@{tsq}", url, "-o", out],
                           capture_output=True)
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 500:
            v = subprocess.run(["openssl", "ts", "-reply", "-in", out, "-text"],
                               capture_output=True, text=True).stdout
            if "Status: Granted" in v:
                got[name] = {"bytes": os.path.getsize(out),
                             "time": next((l.split(":", 1)[1].strip()
                                           for l in v.splitlines() if l.startswith("Time stamp:")), "?")}
                continue
        if os.path.exists(out):
            os.remove(out)
    os.remove(tsq)
    return got


def main():
    today = datetime.datetime.now(datetime.timezone.utc)
    day = sys.argv[1] if len(sys.argv) > 1 else today.strftime("%Y-%m-%d")
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    work = os.path.join(repo, ".capture", day)
    os.makedirs(work, exist_ok=True)

    files, notes = {}, {}
    for slug, url in SOURCES.items():
        try:
            body, status = fetch(url)
            open(os.path.join(work, slug + ".html"), "wb").write(body)
            files[slug] = {"url": url, "bytes": len(body), "http": status,
                           "sha256": hashlib.sha256(body).hexdigest()}
        except Exception as e:
            notes[slug] = f"FAILED: {e}"

    ed, murl, mbody = find_maersk(today)
    if ed:
        open(os.path.join(work, "maersk_us_empty_return_directory.xlsx"), "wb").write(mbody)
        files["maersk_us_empty_return_directory"] = {
            "url": murl, "bytes": len(mbody), "http": 200, "edition_date": ed,
            "sha256": hashlib.sha256(mbody).hexdigest()}
    else:
        notes["maersk_us_empty_return_directory"] = f"no live edition in {MAERSK_LOOKBACK}d lookback"

    slugs = sorted(files)
    leaves = [bytes.fromhex(files[s]["sha256"]) for s in slugs]
    root = merkle_root(leaves)
    rp = os.path.join(work, "root.txt")
    open(rp, "w").write(root.hex() + "\n")
    tokens = timestamp(rp, work)

    for i, s in enumerate(slugs):
        files[s]["merkle_proof"] = merkle_proof(leaves, i)

    manifest = {
        "schema": "gateledger/v2",
        "date": day,
        "captured_utc": today.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root_construction": "sha256 merkle over per-file sha256, slug-ascending, "
                             "odd node promoted not duplicated; root.txt = hex+LF",
        "merkle_root_sha256": root.hex(),
        "rfc3161_tokens": tokens,
        "sources": files,
        "notes": notes,
    }
    mp = os.path.join(work, "MANIFEST.json")
    json.dump(manifest, open(mp, "w"), indent=2, sort_keys=True)

    out = os.path.join(repo, "archive", "working_day_ledger", f"{day}.tar.gz")
    with tarfile.open(out, "w:gz") as t:
        for f in sorted(os.listdir(work)):
            t.add(os.path.join(work, f), arcname=f)
    manifest["tarball_sha256"] = hashlib.sha256(open(out, "rb").read()).hexdigest()
    json.dump(manifest, open(os.path.join(repo, "archive", "working_day_ledger",
                                          f"MANIFEST_{day}.json"), "w"), indent=2, sort_keys=True)
    print(json.dumps({"date": day, "sources": len(files), "failed": list(notes),
                      "root": root.hex()[:16], "tokens": list(tokens)}, indent=2))


if __name__ == "__main__":
    main()
