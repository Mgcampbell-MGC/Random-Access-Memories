# HOLOFOTE · sets (`_build/sets/`)

Reusable Blender 4.5 Cycles sets for the HOLOFOTE sample case (platform §D.6, §D.8, §D.10, §E.1–E.4).
The product is the director's: `_build/blender/holofote.py` builds the candle. Nothing here edits it.

```
sets_lib.py    the sets + helpers (import this)        objetos.py   props: monobloc, handbag, paper flowers/hearts, fittings
texturas.py    procedural textures -> _tex/ (cache)    medir.py     sRGB, Khronos PBR Neutral, CIEDE2000, patch stats
calibrar.py    energy calibration (writes calibracao.json, the record)
test_palco.py  test_escola.py  test_muro.py  test_loja.py   -> 02_PRODUTO/renders/_sets_tests/*.png
```

Run anything with `/home/user/venvs/blender/bin/python <script>`. One Blender process at a time.
`_tex/` is a deterministic cache (fixed seeds) rebuilt on first use; it is git-ignored.

## Colour management (all sets)

`S.cena(res, samples, exposure=-3.0, transparent=False)` = factory reset + Cycles CPU + OIDN, view **Khronos PBR Neutral**,
look **None**, exposure **−3,0**, no scene white balance (so the director's flame keeps its tuning).

**Every key light is calibrated so the lit coating reads at the faixa hex.** The closest PBR Neutral can reach for
amarelo #FFE81A is #F5DF33 (ΔE00 2,6, saturation ratio 0,88); the sets land within 0,2–0,8 of that floor.
`medir.py` reproduces Blender's PBR Neutral within ±2 levels (checked on 24 emission patches), so `calibrar.py`
renders one scene-linear EXR with an *unprinted* copo and solves the energy analytically.

**Warm lights are recorded "balanced".** An unbalanced 3.200 K blackbody turns the amarelo coating gold
(#F8B04E, ΔE00 20,9). `S.balanced(kelvin, balance_k)` gives the colour a blackbody records as through a camera
white-balanced to `balance_k` (von Kries, luminance 1): the spot is still "3.200 K", the coating stays amarelo.

### Calibrated values (verified against the final code: re-solve scale 1,006–1,019)

| Set | Light | Constant (`ENERGIA`) | Energy at the default throw | Coating reads | ΔE00 | Sat. ratio |
|---|---|---|---|---|---|---|
| O PALCO | 3.200 K spot, balanced 3.300 K | `palco_spot_k` **593** W·m⁻² × throw² | 90,1 W at 0,390 m | #F5DC35 | 3,2 | 0,87 |
| A ESCOLA | 3.200 K spot, balanced 3.050 K* | `escola_spot_k` **700** | 7.168 W at 3,2 m | #F5DB35 | 3,4 | 0,87 |
| O MURO | on-camera flash 3 × 3 cm | `muro_flash_k` **89,5** × d² | 112 W at 1,12 m (C10) · 346 W (C01) | #F5DE35 | 2,8 | 0,87 |
| LOJA | key 30 × 30 cm | `loja_key_k` **83** × d² | 119,5 W at 1,2 m; fill = 20 % | #F5DD35 | 3,0 | 0,87 |

*the lit wooden stage bounces amber onto the back panel; at 3.300 K the panel read ΔE00 5,9, at 3.050 K 3,6.
Secondary levels: `palco_spill` 12.000 W (rotunda, light-linked), `flame_bounce` 0,08 W, `escola_spill` 2 % of the spot,
`escola_house` 1,0 (four globes), `escola_presenter` 0,22 (presenter key factor). Other faixas at the amarelo energy:
rosa ΔE00 2,3 · laranja 3,4 · violeta 0,6 (one energy serves the four-colour shots). Re-run
`calibrar.py palco|escola|muro|loja [--faixa 02] [--balance K]` after changing a rig; it appends to `calibracao.json`.

## API

### Common
- `wrap('02')`, `wrap(personal='CASE-01_DONA-CIDA')` → label master path. `tampa_art('200'|'080')` → lid UV print.
- `camera_glass(res, lens, cam_height, tilt_deg, glass_px, top_y, center_x=None, at=(0,0,0), yaw_deg=0, size='200',
  mode='silhouette', fstop=None)` → solves **distance and lens shift** so the glass (0–88 mm) spans `glass_px` with its
  top at `top_y` (silhouette = back rim to front base edge; `mode='axis'` uses the axis points). Verified with
  Blender's own projection to 0,3 px. Returns dict(location, rotation_euler, shift_x, shift_y, distance, check, object).
  - KV-45: `camera_glass((1080,1920), 85, 0.160, -5, 883, 610)` → distance 0,521 m, shift_y −0,2797, 10,03 px/mm.
  - KV-01: `camera_glass((1080,1920), 50, 0.220, -6, 384, 900)`. 16:9 hero: `((1920,1080), 50, 0.22, -6, 410, 470, center_x=1420)`.
  - `solve_glass(...)` = the same without creating the camera.
- `camera_pin(loc, yaw_deg, tilt_deg, lens, res, anchor, anchor_px, fstop, focus)` → a level camera whose shift pins a
  world point to a pixel (verticals straight). `camera_look(loc, target, lens, ...)` for free framings.
- `ride(objs, carrier)` parents keeping the world transform. `descendants(root)`.
- `flame_bounce(h, copo_root, energy=None, receivers=None, kind='disc'|'point')`, `flame_spill(h, copo_root)` — see notes.
- `clearance(min_m=0.30, raise_on_fail=False)` → §D.8 check: distance from every lit flame to every object tagged
  `inflamavel` (posters, TNT, paper décor, string, chairs, handbag, rotunda, seamless cove, stand-in). Supports tagged
  `apoio` (what a candle stands on) are exempt. Prints `ok`/`NO` per pair.
- `fila(sizes=('200',)*4, gap=0.018, at)` → lineup positions (L06, C04): `'200'`, `'080'` or a width in metres.
- `cena(...)`, `render(path)`, `balanced(k, balance_k)`, `kelvin_rgb(k)`, `link_receivers(light, objs)`, `set_haze(density)`.

### 1. O PALCO — `palco(at=(0,0,0), ...)`
Black lacquer stage, the floor X on its lift plate, rotunda 4 m back, the hard spot. Returns handles:
`place` (where the candle stands), `lift` (carrier empty on the plate), `plate`, `floor`, `tape_plate`, `tape_floor`,
`shaft`, `spot`, `throw`, `rotunda`, `spill`, `floor_objs`, `coll`.
```python
h = S.palco(at=(0, 0, 0))                     # options: lift_dz, x_rot_deg, plate_rot_deg, pool_r, spot_az/el/deg,
root = S.H.copo(spec, at=h['place'], rot_deg=-12)   # spot_blend, spot_radius, balance_k, rotunda_spill, haze,
S.ride(root, h['lift']); S.flame_bounce(h, root)    # floor_hex, downstage, tape_gain, spot=False (blackout)
S.lift(h, -0.100, frame=175)                  # F15: keyframe the plate (dz metres below flush)
```
- **Floor**: lacquer, roughness 0,15–0,30 on a 400 mm noise, fine scratches mostly along X (groove bump + pale
  abrasion, tile 0,5 m), two road-case scuff arcs and a 48 × 160 mm tape-residue ghost crossing the pool, foot-traffic
  dust, a gentle board undulation, and a downstage traffic haze (+0,30 roughness ahead of the mark) that dissolves
  the coating's reflection before the KV-01 lockup zone. The reflection stays, illegible.
- **X**: two 48 × 240 mm cloth-tape strips (woven bump, edge dirt, hand-torn ends), the second draping over the first,
  the front-right corner lifted 1 mm, **cut along the plate's seams** (0,9 mm gap): the inner piece rides the plate.
- **Lift plate**: 110 mm square hole in the deck, a black shaft 0,45 m deep, the plate sharing the floor's texture
  (seamless when flush). Lift down/up by `lift()`; the candle rides via `ride()`. (F15: hide the candle until f176.)
- **Rotunda**: black molton (sheen), vertical folds of 40 mm, 11 × 6,5 m, 4 m behind; a light-linked spill shows the
  folds upper-left, ~90 % in shadow.
- **Spot**: 3.200 K balanced, 26°, blend 0,04, elevation 55°, azimuth −30°, aimed 20 mm above the mark. Throw solved
  from `pool_r` (0,090 m → 0,39 m), matching KV-01's pool (measured rx ≈ 366 px of the layout's 380).

### 2. A ESCOLA — `escola(at=(0.0, 0.60), rot_deg=0, preset='C02'|'APRESENTADORA', ...)`
An empty school auditorium at dusk: granilite floor, sage-and-cream two-tone walls, a low wooden stage (boards along
X, worn toward the edge people sit on, painted apron, steps), a faded-pink TNT backdrop stapled in swags with a heart of
crepe-paper flowers and a garland of paper hearts on a string (**no letters**), 6 rows × 8 white **monoblocs**
(one modelled chair — the leg-arm-backrail loop, slotted wrap-around back, skirted seat, splayed channel legs —
instanced as linked duplicates; front row 2,20 m from the edge), a leather handbag on front-row seat 4, 2 × T8
fittings OFF, high vitrô windows and door panes glowing warm dusk (never blue), four globe practicals at ~5 %.
Stage edge on y = 0, stage top z = 0,45. Handles: `place`, `candle_rot`, `chairs`, `front_row`, `bag`, `backdrop`,
`decor`, `spot`, `spill`, `presenter`, `coll`.
- `escola_camera(h, 'C02')` 4:5, 85 mm, 0,72 m upstage, lens 21 cm above the stage, level with lens shift, f/16:
  the back panel pin-sharp right of centre, the front row compressed behind, the bag's seat clear of the glass.
  Rig: spot from above-upstage, elevation 60°, 18°, throw 3,2 m + its 2 % spill toward the chairs.
- `escola_camera(h, 'APRESENTADORA')` 9:16, 50 mm, eye level of a person sitting on the edge (stage + 0,78 m), 1,40 m.
  Rig: front-of-house spot from front-left (azimuth −35°, elevation 22°, 30°, throw 8 m) that carries onto the TNT.
  `figura_sentada(h)` adds a grey PREVIS stand-in (never delivered).
- Product placement: `at=(x, metres in from the stage edge)`; C02 = 0,60 m. Clearance (lit C02): TNT 2,35 m, paper flowers 2,39 m, chairs 2,83 m, bag 3,01 m.

### 3. O MURO — `muro(n=4, spacing=0.125, grade=None, posters=True, poster_w=0.32, ...)`
Plaster wall (reboco: grain bump, rain streaks, worn paint), the lambe posters in a cols × rows grid (default 4 × 3,
2:3, 0,32 m wide, 12 mm overlaps, ±0,5° skew), each a 3 mm grid **displaced by its own height map** (0,6 mm,
midlevel 0,5 — the brand team's numbers), paste-film roughness in brush strokes, a dried glue drip, a cantilevered
concrete ledge (chipped front edge, two brackets) at ⅓ of the grid. Handles: `slots` (candle positions on the
ledge), `posters`, `drip`, `ledge_z`, `grid`, `placeholders`, `flash` (after the camera).
- **Posters**: `cartazes()` reads `01_MARCA/cartazes/cartazes.json` once `PRONTO.txt` exists (it does: 12 posters,
  `3d/*_albedo.png` RGBA + `3d/*_altura.png` 16 bit) and falls back to flat placeholders otherwise. `grade` = ids
  row-major; default `C01_GRADE` puts the C01 headline poster 12 top-centre clear of the candles, violeta 04 and
  amarelo 05 behind the candle group for contrast, torn 07/08 and the old layers around. `posters=False` = bare plaster (C10).
- `muro_camera(h, 'C01'|'C10', stop=0.0)` + `flash(cam, offset=(-0.05, 0.15))`: 3 × 3 cm area light 15 cm above the
  lens and 5 cm left, parented to the camera → the hard shadow falls down-right.
- §D.8: the ledge is within 30 cm of paper. `clearance()` reports NO for any lit candle here (C01/C10 are unlit).

### 4. LOJA — `loja(at=(0,0,0), key_az=-45, key_el=35, key_dist=1.2, fill_ratio=0.20, sweep_back=0.55)`
Render with `S.cena(transparent=True)`. A papel seamless (floor + 0,35 m cove + back) that is a **shadow catcher**;
key 30 × 30 cm at 1,2 m, 45° left, elevation 35°; white bounce right at 20 % (0,8 × 1,0 m, it shows in the coat as a
reflection strip). The cove starts 0,55 m behind the product (lit L05: 0,551 m measured).
- `loja_camera(h, 'L01'|'L05', res=(1200,1200), fill=0.65, center_x=None)` — L01 85 mm at label height (52 mm), 0°
  tilt, candle at 40 % of the width; L05 ¾ front, 25° down. `tampa_encostada(h)` leans the lid (with its UV art)
  behind the candle's right side, top to camera. `loja_plate(png_alpha, png_out)` composites the exact #FFF8EC plate by code.

## Deviations from the platform, each measured

1. **Spot colour**: the 3.200 K spot is recorded balanced (3.300 K PALCO, 3.050 K ESCOLA). Raw, it turns amarelo gold.
2. **Floor albedo #1A1918, not #0A0A0B.** As an albedo, 0,3 % is darker than any real black paint and PBR Neutral's
   toe (it squares values below 0,08) erases the lit pool: the empty pool of F15 f12 rendered at ~1/255. At 1,0 % +
   dust the pool reads (21, 16, 6) against (0, 0, 0) outside. `floor_hex='#0A0A0B'` restores the literal value.
3. **Spot radius 0,0103 × throw (4 mm), not 20 mm.** At the 0,39 m throw the KV's pool size forces, 20 mm is a 2,9°
   source against a 13° half-cone and the pool edge goes soft. 20 mm suits a long throw.
4. **The flame bounce is a motivated cheat.** A flame burning below the rim of an opaque coated glass cannot light the
   floor near the base (the shadow line falls ~0,87 m out). `flame_bounce()` adds a shadowless 1.900 K disc,
   light-linked to the floor and tape, invisible to camera. Under the spot it is invisible; in blackout it is the warm
   glow in front of the base. Likewise the C06 "dimly flame-lit label" is impossible physically; `flame_spill()`
   (off by default) is a light-linked 1.900 K wash on this copo's coating and print only.
5. **"Poster paper clips by +0,5 stop"** cannot coexist with the coating rule under PBR Neutral (paper never truly
   clips). At the calibrated flash the papel poster reads (242, 236, 222); `stop=+0.5` gives (249, 243, 232) and
   costs the coating ΔE00 4,0 / saturation 0,73.
6. **Tape gain 0,70**: the floor gets ~1,5× the label's irradiance under a 55° spot; the cloth tape reads #D8C207 in
   the pool, a hair under the hero coating instead of blowing out.
7. **Haze** (world volume 0,0015) is optional and off: at the KV's short throw the spot's own cone barely shows; it
   mostly lifts the rotunda spill into a soft diagonal shaft (`test_palco.py haze`).

## Test renders (`02_PRODUTO/renders/_sets_tests/`, ≤540 px wide, 32 samples)

| File | What |
|---|---|
| `PALCO_vazio.png` | F15 f12 · cam A: the empty hard pool with the X (540 × 960) |
| `PALCO_kv01.png` · `PALCO_kv45.png` | KV-01 and KV-45 framings, AO VIVO lit, yaw 12° camera-left |
| `PALCO_elevador.png` · `PALCO_subida.png` | F15 f170 plate down 100 mm · f190 plate −40 mm carrying the unlit candle |
| `PALCO_blecaute.png` · `PALCO_haze.png` | F15 f216 / C06 flame only (+ bounce, + label spill) · optional cone |
| `ESCOLA_c02.png` · `ESCOLA_apresentadora.png` | C02 (4:5) · presenter previs (9:16, grey stand-in) |
| `ESCOLA_geral.png` | room overview under an added work light (not a look) |
| `MURO_c01.png` · `MURO_c10.png` | C01 with the brand team's 12 posters, four candles lids on · C10 on bare plaster |
| `LOJA_l01.png` · `LOJA_l05.png` (+ `_alpha`) | L01 with the leaning lid · L05 lit on its upturned lid; papel plate by code |
| `SETS_contato.jpg` | all of the above on one sheet (JPG preview) |
