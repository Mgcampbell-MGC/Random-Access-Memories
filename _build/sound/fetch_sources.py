#!/usr/bin/env python
"""HOLOFOTE · fetch_sources.py — download the licensed real recordings the library is built from.

Every source goes into its own empty directory under _fontes/<id>/ and is checked against the SHA-256 recorded
here when the library was built (6 Oct 2026). Zips are unpacked with Python's zipfile (names sanitised); nothing
inside a download is ever executed. The licence of each file was read on its source page that day — see
04_FILMES/som/CREDITOS.md.

    /home/user/venvs/web/bin/python -I fetch_sources.py
"""
import hashlib, os, sys, urllib.request, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(HERE, "_fontes")

# id, url, sha256, licence, page
SOURCES = [
    ("kenney_impact", "https://kenney.nl/media/pages/assets/impact-sounds/87b4ddecda-1677589768/kenney_impact-sounds.zip",
     "029d734af1582474edf3a694d1b0cebc97c1c152f2f39fa34d4c2bafc5de77f8", "CC0 1.0", "https://kenney.nl/assets/impact-sounds"),
    ("kenney_rpg", "https://kenney.nl/media/pages/assets/rpg-audio/8e99002d76-1677590336/kenney_rpg-audio.zip",
     "6dbeaf8544da958d8f2adcb4a4a4b76c1ade34a05f8ab9edccd327da7375f38b", "CC0 1.0", "https://kenney.nl/assets/rpg-audio"),
    ("kenney_ui", "https://kenney.nl/media/pages/assets/ui-audio/490d233f68-1677590494/kenney_ui-audio.zip",
     "946fc23a63d535d693eb31b2eabb80c8c28d6351e2186b344ceb71b2cb1d5eb6", "CC0 1.0", "https://kenney.nl/assets/ui-audio"),
    ("kenney_casino", "https://kenney.nl/media/pages/assets/casino-audio/2472606a04-1721639069/kenney_casino-audio.zip",
     "f36250766ac5bc378c13708ddf12a23a8e54a3251f8d482c7536e51b5dbafa18", "CC0 1.0", "https://kenney.nl/assets/casino-audio"),
    ("oga_applause", "https://opengameart.org/sites/default/files/applause-clapping-church-crowd-immersive.wav",
     "0d3bfde5a050f3c5e6685bd7f1efc7ab1d289fbad65c88c1ce9b4691228c69c9", "CC0 1.0",
     "https://opengameart.org/content/applause-in-a-large-hall-or-church"),
    ("oga_welldone", "https://opengameart.org/sites/default/files/Well%20Done%20CCBY3.flac",
     "41e7646fc7ff5ffd66947bda50a07f194683318b23cb193d57c1650a5ec4953b", "CC0 1.0 (relicensed by the author 2024-10-05)",
     "https://opengameart.org/content/well-done"),
    ("oga_crowdshout", "https://opengameart.org/sites/default/files/crowd_shouting_0.ogg",
     "a2c23a64c127c77717cbe4abb21f138bac9d9aa6cb3cc89d62bab5d0d96dd7ca", "CC0 1.0",
     "https://opengameart.org/content/crowd-shoutingspeaking-ambience"),
    ("oga_cough", "https://opengameart.org/sites/default/files/old-man-cough.flac",
     "1627a93533a47be206392af7465b0e3484dd2aade6f873ceb0b997c80a40e356", "CC0 1.0",
     "https://opengameart.org/content/old-man-cough"),
    ("oga_fire1", "https://opengameart.org/sites/default/files/fire-1.wav",
     "26702de8a195bcbafeae72034861d875a1b7917168a25106f4e1957ecdddf7e5", "CC0 1.0",
     "https://opengameart.org/content/fire-crackling"),
    ("oga_fireplace", "https://opengameart.org/sites/default/files/fire.wav",
     "85ca0cc60d0c037fff8b185e31ad1fcdbda6ce45eee17c3ee1318d1b8f59e330", "CC0 1.0",
     "https://opengameart.org/content/fireplace-sound-loop"),
    ("oga_ignition", "https://opengameart.org/sites/default/files/ignition.flac",
     "bd8281bcee65bc705755fd36bdf40d04fadddd474f52fd481233523e178b4ea1", "CC0 1.0",
     "https://opengameart.org/content/flare-ignition"),
    ("oga_lightswitch", "https://opengameart.org/sites/default/files/lightswitch_1.zip",
     "2fccfdf18abab82af7ac2cd0e8bf3406f39eab290a442882d42232543ebbee2e", "CC0 1.0",
     "https://opengameart.org/content/light-switch-turn-on-and-off-sfx-0"),
    ("oga_paper", "https://opengameart.org/sites/default/files/sounds_6.zip",
     "aa1889414310c7cfdd8dc291c19d4e4fc21ec987e9238b0d961fb72449c263a4", "CC0 1.0",
     "https://opengameart.org/content/various-paper-sound-effects"),
    ("oga_shop", "https://opengameart.org/sites/default/files/legit_audio_-_the_shop_free_sfx_wav.zip",
     "87d49c4431fdf5647f3c434455b3bcd402fc757f97f2640b2ef84e2e5db9d86e", "CC0 1.0",
     "https://opengameart.org/content/the-shop"),
]

UA = "Mozilla/5.0 (X11; Linux x86_64) HOLOFOTE-sound-build"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def safe_unzip(zp, dest):
    with zipfile.ZipFile(zp) as z:
        for m in z.infolist():
            name = m.filename.replace("\\", "/")
            if m.is_dir() or name.startswith("/") or ".." in name.split("/"):
                continue
            out = os.path.join(dest, *name.split("/"))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with z.open(m) as src, open(out, "wb") as dst:
                dst.write(src.read())


def path_of(sid):
    """Directory holding source `sid` (unpacked if it was a zip)."""
    return os.path.join(FONTES, sid)


def main():
    ok = True
    for sid, url, digest, lic, page in SOURCES:
        d = os.path.join(FONTES, sid)
        os.makedirs(d, exist_ok=True)
        fn = os.path.join(d, os.path.basename(url).replace("%20", "_"))
        if not (os.path.exists(fn) and sha(fn) == digest):
            print(f"download {sid} …", flush=True)
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r, open(fn, "wb") as f:
                f.write(r.read())
        got = sha(fn)
        if got != digest:
            print(f"  ✗ {sid}: sha256 {got} ≠ {digest}"); ok = False; continue
        if fn.endswith(".zip") and not os.path.isdir(os.path.join(d, "x")):
            safe_unzip(fn, os.path.join(d, "x"))
        print(f"  ✓ {sid:16s} {lic}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
