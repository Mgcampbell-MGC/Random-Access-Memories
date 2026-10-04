# Setting up Manus for Sol: one sitting, about 45 minutes

This is for the person setting Sol up. Everything Sol touches afterwards is in Portuguese: `GUIA_DA_SOL.md` (her
day-to-day messages) and `TESTE.md` (her two tests).

## What is in the kit

| File | What it is | Where it goes |
|---|---|---|
| `o-lancamento-skill.zip` | Her tools, packaged as a Manus Skill: crop to size, apply the real pack over the blue stand-in, add text beside the pack, check every piece and every film frame, make a simple film, self-test | Manus → Skills → Upload |
| `O_LANCAMENTO_pasta.zip` | The working folder for her computer: the same tools, the world library folder, and a practice client (ORVALHA, fictional) | Unzip into her Documents |
| `1_instrucao_do_projeto.txt` | The project's master instruction | Paste into the Manus Project |
| `2_base_de_conhecimento/` | 4 files: specs and the product ladder, the rules and 12-point checklist, 8 starter worlds with prompts, the brief template | Upload as the Project's knowledge base |
| `GUIA_DA_SOL.md` | Her copy-paste message for each step of a launch, plus VITRINE, EXTENSÃO, PRÉVIA | Give to Sol |
| `TESTE.md` | Test 1 (install, 9 checks) and Test 2 (three timed practice launches, bars set in advance) | Give to Sol |

## The setup, in order

1. **Manus account, on Sol's own email.**
   - Pro plan (start on the 8.000-credit tier).
   - Turn on two-factor login.
2. **Install Manus Desktop** on her Mac or Windows laptop (manus.im → Download).
   - The Video Editor only exists in the desktop app.
3. **Install Python 3** on the same laptop, from python.org.
   - On Windows, tick **"Add python.exe to PATH"** in the installer.
4. **Unzip `O_LANCAMENTO_pasta.zip` into her Documents.** You get `Documents/O LANCAMENTO/` with:
   - `_ferramentas`
   - `_biblioteca/mundos`
   - `clientes/orvalha_PRATICA`
   - her two guides.
5. **In Manus Desktop, turn on "My Computer"** and authorise **only** the `O LANCAMENTO` folder. Manus then runs her
   tools on her own laptop, and the client files stay there.
6. **Skills → + Add → Upload a skill → `o-lancamento-skill.zip`.**
7. **Create the Project.** Projects → + → name it **O LANÇAMENTO**.
   - **Master instruction:** paste all of `1_instrucao_do_projeto.txt`.
   - **Knowledge base:** upload the 4 files from `2_base_de_conhecimento/`.
   - **Project → Skills → + Add → o-lancamento**, then click the lock icon so it can't be edited by accident.
   - **Pin the project.**
8. **Run Test 1 with her.** In the project, open a new task and send the first message in `TESTE.md`. It must end
   with `AUTOTESTE: 9/9 OK`.
   - The first run installs the Python libraries and takes a few minutes.
   - If it fails, the screen says which of the 9 checks failed.
9. **Hand her `GUIA_DA_SOL.md` and `TESTE.md`.** Test 2 is three practice launches of the fictional ORVALHA serum,
   timed, before any real client.

Photoshop (already in her tool stack) is used for one step: hand-finishing shadows on the scene, never on the pack.

## Verified here, and not yet verified

**Verified on 4 Oct 2026**, on a clean install of exactly what the Skill installs (OpenCV 5.0 headless, Pillow 12.3):
- the whole still-and-film path on the ORVALHA pack;
- exact sizes (1080×1920, 1080×1350, 1080×1080);
- BT.709 film tags;
- the text tool leaving every pack pixel byte-identical;
- the checker passing exact pieces and rejecting a wrong label.

**Only Sol's first runs can answer these, and Test 2 records each one:**
- whether Manus's image generation comes out at ≥1080 px on the short side;
- whether the Video Editor exports 1080×1920 **and** its exported film passes the check. If either fails, films use
  the simple path, which is verified;
- credits per step (the estimate is 2.000–5.000 per launch);
- her real hours (the bar is ≤3 h for steps 1–7).

## Three things the kit enforces, and why

1. **The pack is never generated.** Scenes use a flat blue stand-in; the brand's real file is laid over it by code.
   Every AI tool tested, Manus included, misspells labels when it draws them.
2. **No AI editing after the pack is in.**
   - Manus's Design View, "edit image", AI upscale and object removal all redraw the whole picture, label included.
   - Text goes on by code (`texto.py`), which proves afterwards that no pack pixel changed.
3. **Every piece and every film frame is checked.**
   - The checker catches redrawn, garbled, distorted or recoloured labels.
   - It cannot reliably see a single look-alike letter in tiny print (measured: *secos*→*secas* passed). That risk only
     exists if the wrong label file is used, so the guide makes the signed Ficha name the file, and the brand approves
     the key visual in writing.

## Next: the website

`site/PROMPT_SITE_MANUS.md` is the Manus prompt for the website and a three-case portfolio, made with the same method,
so every portfolio piece is real proof with a real check report. Run it in a separate Manus project after Test 1
passes. Attach `site/EMBALAGEM_climate.png`.
