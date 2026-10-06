# HOLOFOTE: finish the kit (prompt for Manus)

You are finishing a production kit that is about 85% done. Don't redesign anything: the creative direction is locked.

**Where it is:** GitHub repo `mgcampbell-mgc/random-access-memories`, branch `claude/volta-architecture-design-txe8r5`,
folder `kits/HOLOFOTE/`. Run every command from inside `kits/HOLOFOTE`.

**Read these first, in order:**
1. `06_PRODUCAO/COMECE_AQUI_PROXIMO_LLM.txt`: the full rulebook and every command.
2. `06_PRODUCAO/STATUS_ENTREGA.txt`.
3. `07_KIT_COMPLETO/HOLOFOTE_PACKET.pdf`.
4. `_build/PRODUCTION_BRIEF.md`.

If those files and this prompt disagree, the files win. The one exception is the task list below, which is this prompt's.

## Rules you must not break

1. **Keep every image of our label or pack out of every image and video generator.** That includes upscaling,
   "improve", Design View and image-to-video. Every pack pixel comes from one of two places: a Blender render that
   wears the real label master, or a code composite of that render.
2. **Burn no AI label or disclosure into any piece.** This is the owner's decision.
3. **Write no testimonial lines, ever.** The presenter never says "minha mãe".
4. **Make no AI edit to a frame once the pack is in it.** Add text by code, beside the pack, never on top of it.
5. **Check every pack image with `_build/tools/fidelidade_uv.py`.** Run it on every still, and on every film frame
   where the pack is visible.
   - Never move the pass bars.
   - A piece that fails stays out of the final set. List it, with the reason.
6. **Encode video only with `_build/tools/codificar.py --fps 24`.** Never use a renderer's default MP4: its colours
   come out wrong on phones.
7. **Get the owner's written OK before you:**
   - buy credits or tools;
   - generate people;
   - publish anything.
8. **Look at every output at 100% before you call it done.**

## Setup

The commands in the rulebook use paths from the previous machine (`/home/user/venvs/...`). Use your own instead:

- **Python 3.11** with numpy, opencv-python, OpenEXR, Pillow, and playwright with Chromium.
- **Blender 4.5 (Cycles).** Run it as `blender -b --python SCRIPT -- ARGS` wherever the files say
  `_build/shots/blender.sh SCRIPT -- ARGS`. Run only one Blender at a time.
- **ffmpeg.**
- **Fonts:** use only the ones in `_build/fonts/`.

## Tasks, in this order

1. **Make three short films. They need no new 3D**, because their inputs are already in the repo: the KV-45 renders,
   their label AOVs, the flame loop and the sound mixes.
   - Run:
     ```
     python _build/filmes/compor.py F06A F06B F06C_09-05
     python _build/filmes/fidelidade_filmes.py F06A F06B F06C_09-05
     ```
   - You should get `04_FILMES/F06A_CLAC_*`, `F06B_O-PIOR-SHOW_*` and `F06C_SINAL_09-05_*`, each with sound and
     silent.
   - Watch each film all the way through.
2. **Fix KV-01 in 1:1.** It fails the label check at the glass edge (worst tile 0,10–0,48).
   - Re-render it at 200 % (`_build/shots/campanha.py -- KV01_1x1 --pct 200`). The 2× report is the check of record.
   - Then run `python _build/shots/pecas_finais.py KV01`.
   - If it still fails, leave it out and say so.
3. **Fix C10 "MÃE ♥".** It misses the 5th-percentile bar by 0,005 (0,945 against 0,95).
   - Re-render C10 with `--pct 200`, check it, then run `pecas_finais.py C`.
   - Also check C08's result in `06_PRODUCAO/fidelidade/`.
4. **Swap the image on the brand-book page "O PALCO" (LIVRO-12).** It uses the failing KV-01 1:1 render.
   - Replace it with a passing KV-01 format: 4:5, 9:16, or the new 1:1 if task 2 passed.
   - Then run `pecas_finais.py LIVRO`.
5. **Make F15 "A ENTRADA" (15 s). It needs Blender and is the longest job.** Follow "Como refazer" in
   `04_FILMES/LEIA_ME.md`, rendering with `_build/filmes/f15_3d.py`.
   - Cam A is already rendered.
   - Render `grua` for frames 160–203. Frames with the candle (176–203) need `--pct 200`, with label AOVs.
   - Render `blecaute`.
   - Render `chama blecaute 210-223,228,229`.
   - Before the full flame render, test a 24-frame loop at low samples and check it for flicker.
   - Then run `compor.py F15` and `fidelidade_filmes.py F15`.
6. **Refresh the packet.**
   - Run `python _build/pacote/maquina.py`, then `python _build/pacote/preencher.py --pdf`.
   - Use only numbers from real reports. Never type one in by hand.
7. **Generate the people shots (H01, H02, M01) and pieces P01–P03 only if the owner approves the credits in writing.**
   - The prompts are in `05_ANUNCIO/`.
   - In a generated scene the candle is a flat, matte blue (#0047BB) stand-in. It stands on a surface: never in a
     hand, never lit.
   - Composite the real Blender render in by code afterwards, then check it.

## When you're done

For every piece, report:
- the file name;
- pass or fail, with the numbers from its JSON fidelity report;
- for anything missing, what is missing and why.

A script is not a film, and an animatic is not a filmed ad.
