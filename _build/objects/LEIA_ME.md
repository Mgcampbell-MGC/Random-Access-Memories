# HOLOFOTE · objects library (3D props + previs mannequin)

`objects_lib.py` builds every prop around the candle in Blender 4.5 / Cycles, plus a grey previs mannequin for
the O ANÚNCIO animatic. The candle itself is the director's `../blender/holofote.py` (used, never edited).

| File | What it is |
|---|---|
| `objects_lib.py` | The library (import it inside a Blender Python session). |
| `test_objects.py` | Low-res look-dev scenes: `python test_objects.py -- <scene> [samples] [px]`. Output goes to `02_PRODUTO/renders/_objects_tests/T_<scene>.png`. |
| `make_placeholders.py` | Neutral placeholder art (grey labels, face name, size, UP arrow), written to `placeholders/`. Used only when a packaging file is missing. |
| `placeholders/` | The generated placeholders. |

```python
import sys; sys.path.insert(0, '/home/user/Random-Access-Memories/kits/HOLOFOTE/_build/objects')
import objects_lib as O          # also puts _build/blender on sys.path (candle_lib, holofote)
```

## Conventions

- Specs are in **mm**; Blender is in **metres** (`MM = 0.001`).
- Every builder returns a `Built` (an attribute bag). Move or rotate `.root`, never the parts.
- Every object stands on z = 0 and faces the camera at **−Y**, like `holofote.copo()`.
- Beauty renders use **Khronos PBR Neutral**, look None, **exposure ≈ −3,0**. The tests also use
  `reset(view='Khronos PBR Neutral', exposure=-3.0)`.
- **Printed art always comes from an image file mapped by UV.** Every path is a parameter. With no parameter
  the library reads the packaging team's file by its **exact name** (`pfile(folder, name)`), never by keyword. If
  that file doesn't exist it uses the placeholder.
- Atlases follow `candle_lib.box()`: a 4 × 3 grid of uniform cells. The top row is `[., top, ., .]`, the middle
  row `[left, front, right, back]`, the bottom row `[., bottom, ., .]`. Top: image top = back. Bottom: image top =
  front. Sides read upright from outside. Cells may be non-square; only the grid has to be uniform.

## 1 · O CASE (§C.7)

```python
c = O.case(state='open', open_deg=100, unit='HLF-CASE-02',
           copo=dict(faixa='02', wrap=WRAP, lid_art=TAMPA),         # a holofote.copo() spec; lid forced 'on'
           setlist=True, setlist_rise_mm=20, band=True, band_kw=dict(route='drape'),
           at=(0, 0, 0), rot_deg=0)
# c.root, c.base, c.lid, c.lid_pivot (rotate X to animate the clac), c.tab, c.mirror, c.foam,
# c.copo, c.setlist, c.band (band, clasp, seal), c.contract (the files and geometry actually used)
```

- **Geometry:**
  - Outer 130 × 130 × 132: a base tray of 102 and a lid of 30. 2 mm board, 0,5 mm rounded edges.
  - The lid is hinged on the back top edge (`c.lid_pivot`).
  - Eight foil **ball corners**: domes that stand 1,7 mm proud.
  - The **hasp tab**: a 52 × 16 mm die-cut plate, 0,8 mm thick, hanging below the lid front, with R3 lower
    corners. It has **one** 16 × 3 slot, aligned with a slot in the base front (x = −13 mm, 8 mm below the lid
    edge, per the packaging json).
  - The magnets are hidden and not modelled.
- **Mirror:**
  - A 100 × 100 × 2 PMMA panel, metallic 1,0, roughness 0,02, inset in the printed bulb frame.
  - Where the packaging mirror mask is black inside the mirror, the atlas ink is printed **on** the mirror
    (*olha a atração.*).
- **EVA:**
  - Black, roughness 0,8, with a cellular bump.
  - A Ø92 × 86 cut-out for the copo with its lid on, and a 3 mm setlist slot.
  - Both positions come from the packaging json: the cut-out is centred at y = −4 and the slot sits at the back,
    y = +56,5. So the folded setlist rises **behind** the copo, in front of the mirror.
- **Art:** read automatically from `02_PRODUTO/case/`:

  | Channel | File |
  |---|---|
  | Colour | `<unit>_ATLAS_base.png`, `<unit>_ATLAS_tampa.png` |
  | Foil mask (metallic) | `CASE_ATLAS_base_foil.png`, `CASE_ATLAS_tampa_foil.png` |
  | 16-bit tolex height (bump 0,29 mm per unit, so the 0,15–0,85 grain is 0,2 mm) | `CASE_ATLAS_*_altura16.png` |
  | Mirror mask | `CASE_ATLAS_tampa_espelho.png` |
  | Tab art | `CASE_ABA_hasp.png` |

  To override one channel, pass `base=`, `tampa=`, `base_foil=`, `tampa_foil=`, `base_height=`,
  `tampa_height=`, `espelho=` or `tab=`. Without the files you get placeholders and an analytic foil (4 mm on the
  12 closed-box edges plus 12 × 12 corner flanges).
- **Closed or open:** the base atlas shows the case **closed**, with the tab drawn on the base front. The model has
  a real tab, so the base material hides that drawing (`hide_rect` samples the tolex 18 mm lower). The open case
  then shows a clean base front with the real slot hole.
- **Band** (`band_kw`): see §5.
  - `route='drape'` (the default): the doubled strap goes straight down the front onto the floor, then turns
    left (`floor_turn_deg=-90`) and runs across the frame in front of the case. Clasp and seal lie on the floor
    and the seal's *pode / rasgar.* reads upright from the front and from above (C05). It covers about 15 mm of
    *HOLOFOTE · AO VIVO*. With `floor_turn_deg=0` the strap runs straight at the camera and the seal reads
    sideways.
  - `route='corner'`: the strap runs left above the text, round the front-left edge, and down the left face to
    the floor. Clasp and seal sit on the upper left face, and the main panel stays clear for a front-on closed
    shot.

### The mirror rule (C05: only the dark ceiling and one bare bulb, never a face, never the pack)

```python
ang = O.open_deg_for_camera(70)            # = 140 deg for a 70 deg top-down camera
c = O.case(state='open', open_deg=ang, copo=...)
cam = camera(...); bpy.context.view_layer.update()
O.place_work_bulb(c, cam, dist=1.3)        # hangs a bare A60 bulb exactly where the mirror looks
```

A lid at angle a reflects a camera ray from elevation e to elevation 2a − 180 − e. **At e = 70° the lid must open
past ~125°, or the mirror shows the copo and the foam.** An "upright" lid (90–105°) seen from 70° is the wrong
geometry, verified in `T_case_c05.png`. `place_work_bulb` prints a warning if the mirror would look down.

Also available:
- `work_bulb(at, lit, light_w, cord_mm, filament)`: the bulb on its own. `light_w > 0` adds a point light.
- `mirror_frame(c)`: the mirror's world centre and normal.
- `mirror_reflection(c, cam_loc)`: the reflected view direction.

## 2 · O INGRESSO carton (§C.9)

```python
O.ingresso(faixa='02', sku=None, atlas_path=None, size=None, at=..., rot_deg=..., bulge_mm=0.35)
```

- 96 × 96 × 98 tuck-end SBS.
- The atlas is `02_PRODUTO/cartucho/<sku>_CARTUCHO_ATLAS.png`; `sku` defaults to `HLF-<faixa>-200`.
- The panels bow 0,35 mm, the fold edges are rounded, and a tuck slit runs along the top front and sides. The ink
  cracks faintly white on the folds.
- Pass `size=(74, 74, 76)` for O INGRESSO SINGLE and `size=(74, 74, 82)` for the NOVA TEMPORADA carton; supply an
  `atlas_path` for those.

## 3 · A SETLIST (§C.8)

```python
O.setlist(state='folded'|'fan'|'flat', fold_deg=None, side1=None, side2=None, lie=True, first_fold=-1,
          perforations=True, at=..., rot_deg=...)
O.setlist_taped(side1=None, overlap_mm=10, tape_hex=AMARELO, crease_deg=2, at=..., rot_deg=...)
```

- A 105 × 400 concertina of four 105 × 100 panels, 0,4 mm card, with fold radius 0,5.
- **Art:** `02_PRODUTO/setlist/SETLIST_lado-1.png` and `SETLIST_lado-2.png`.
  - P1 is at the image top.
  - Side 2 is drawn "turned over left to right", so the library mirrors it.
  - The die-cut perforations come from `SETLIST_picote_lado-1.png`; without it they are analytic: tickets at 325,
    350 and 375 mm, the P3/P4 fold, and a stub at x = 83.
- **States:**
  - `folded`: 180°, about 3 mm thick, standing with P1 facing −Y. This is what `case()` puts in the slot.
  - `fan`: a 70° zigzag lying on the floor, panels at ±35°, P1 far from the camera. `first_fold=+1` turns the
    cover panels (P1, P3) toward a front camera instead of the tickets (P2, P4). From about 60° above, all four
    panels show.
  - `flat`: open on the floor with faint residual creases.
- `setlist_taped` adds two torn strips of amarelo cloth gaffer tape, 48 mm wide, over the P1 and P4 edges. Each
  strip covers `overlap_mm` of the card and one corner lifts 1 mm. `gaffer_strip()` is public if you need more
  tape.

## 4 · NOVA TEMPORADA refill (§C.9)

```python
O.refil(faixa='02', peel=0.0, lid_art=None, band_art=None, lid_d=68.6, at=..., rot_deg=...)
```

- The holofote.py **A CÁPSULA** (black anodised, Ø68 × 74, rolled lip, wax and wood wick) stands on z = 0.
- **Peel lid:**
  - Art: `02_PRODUTO/refil/HLF-REF-0n_TAMPA-PEEL.png`, 40 px/mm. The Ø66 disc is on the left and the pull tab
    on the right, so the tab points +X.
  - The physical lid is Ø68,6, because a Ø66 lid cannot seal on the Ø67,4 lip. The ring outside the Ø66 print is
    the faixa colour.
  - The foil underside shows the lip's seal ring.
  - `peel` runs from 0 (sealed, tab slightly lifted) to 1. At **0,5** (half-peeled, L07/C08) the lid curls back
    from the tab side over a 7 mm radius, showing the foil, the wax and the wick.
- **Laser band:** `HLF-REF_CAPSULA_faixa-laser.png`. u = 0,25 is the front; the band is 10 mm tall, centred 12 mm
  below the lip, and the ink renders as bare aluminium.

## 5 · A PULSEIRA (§C.6)

```python
O.pulseira(preset='loose', ops=None, start=((0, 0, 0.5), (1, 0, 0), (0, 0, 1)), art_path=None, with_clasp=True)
# threaded through the case: O.case(..., band=True, band_kw=dict(route='drape', floor_turn_deg=-90, tail_turn_deg=55))
```

- **The band:** 15 × 350 mm, 1 mm thick, woven polyester.
  - Colour comes from `02_PRODUTO/pulseira/PULSEIRA_tecido.png`: black ground, amarelo jacquard, with x running
    along the band from the clasp end.
  - The weave bump comes from `PULSEIRA_tecido_altura16.png`.
  - The back is the same weave, mirrored and slightly duller.
- **The clasp:** a black ribbed one-way slide clasp at end A, left open.
- **Custom paths:** `ops` takes `Turtle` steps from `start`: `('fwd', mm)`, `('turn', deg, r)` (in plane),
  `('bend', deg, r)` (over the width axis), `('twist', deg, mm)`, `('fwd_to', 'z', value)` and
  `('bend_to', dir, r)`. The path is trimmed to exactly 350 mm.
- **Through the case:** the band doubles through the single aligned slot. The inner leg is the outer route offset
  by one band thickness, and the U-turn behind the wall is hidden. The paper seal (`seal()`) wraps both legs just
  before the clasp.
- **The seal** (`seal(p, t, up, read_up=(0,1,0), art_path=None, stack_mm=None)`): the packaging redesign of
  6 Oct.
  - One strip, `02_PRODUTO/pulseira/PULSEIRA_SELO_faixa.png` (60 × 15 mm, 20 px/mm, x = s along the strip),
    printed on the outside only. The inside is plain papel.
  - The panel layout comes from `PULSEIRA.json → seal`: s 0–23 is the hidden inner glue wrap; the left side is
    23–25,5; TOPO is 25,5–41,5 (*pode / rasgar.*, centre 33,5); the right side is 41,5–44; BAIXO is 44–60
    (*o que se guarda é a pulseira.*).
  - It is wrapped round a 16 × 2,5 mm stack, and each panel lands on its own face.
  - On TOPO, s increases toward `read_up`, so the letters' tops point toward the strip's higher end and away
    from a front camera.
  - The text lines run along the band, so they read upright only where the band runs across the frame.

## 6 · Previs mannequin (§F.1–F.2)

```python
m = O.previs(body='H01'|'H02', pose='a'|'b'|'c'|'d', key=None|'A'|'B', frames=(1, 13), at=..., rot_deg=...)
O.previs_stage(width=2.6, depth=1.4, height=0.55, at=(0, 0, 0.55))   # the sitting root sits on its front edge
# m.parts: body, trousers, tee/cardigan or sweatshirt, head, hair, hand_L/R, foot_L/R, (phone, bag, strap)
```

- **Construction:**
  - Neutral matte greys only.
  - Smooth elliptical lofts follow an IK skeleton: a two-bone solve for the arms, legs and hand targets.
  - Mitten hands are rounded-box parts, with a separate index finger and thumb.
  - Shoes are simple.
  - The head is an egg with a nose and brow so the eyeline reads. There is no other facial detail.
- **H01** (1,65 m): a platinum buzz-cut cap and an oversized cardigan. The cardigan is an open-front loft with a V
  to the chest and a placket line below, over a dark tee.
- **H02** (1,76 m): a dark curly-top fade, an oversized sweatshirt with a ribbed hem at the hip, and a crossbody
  bag with its strap.
- **Poses:**

  | Pose | What it shows | Root |
  |---|---|---|
  | `a` | Sitting on the stage edge, legs dangling, hands on the stage, looking at camera | The stage's top front edge |
  | `b` | Standing deadpan slow clap: key A hands apart, key B hands together | The floor |
  | `c` | Standing, right arm raised holding a phone back-to-camera, flash on (the logo end is in the palm) | The floor |
  | `d` | Sitting: key A a finger-heart shown to camera, key B pointing at the lens | The stage's top front edge |

- **Animation:**
  - `key=None` on `b` or `d` animates A → B between `frames` with shape keys (the body and garments) and
    transform keyframes (the hands). In pose `d` the hand also changes shape (heart → point) through a shape
    key.
  - `'A'` or `'B'` builds one static key.
  - Pointing *at the lens* is foreshortened from a frontal camera; give the animatic camera 10–20° of yaw if the
    finger must read.
- The presenter never holds the pack. No pack is ever parented to the mannequin.

## Known conflicts and decisions (for the director)

1. **Seal legibility: resolved 6 Oct.** At cap 4,0 mm, *"pode rasgar."* measures 41,6 mm and could not fit the
   ~16 mm top face. The packaging team reset it in two lines at cap 2,49 on the TOPO panel of
   `PULSEIRA_SELO_faixa.png`, and it now reads in `T_band_detail.png`.
2. **The hasp** has one aligned slot (the packaging contract). The band doubles through it with a hidden U-turn,
   which in reality needs a relief in the EVA behind the slot.
3. **A lid at 140°** (the mirror-safe angle for C05) would need a ribbon stay in reality. None is modelled.
4. **Peel lid:** Ø66 per §C.9 cannot seal on the Ø67,4 lip. It is modelled at Ø68,6, with the art at Ø66.
5. **The `drape` band covers part of the main panel.** Use `route='corner'` or `band=False` for a front-on hero.

## Test renders (`02_PRODUTO/renders/_objects_tests/`, ≤540 px, ≤24 samples)

| Render | What it shows |
|---|---|
| `T_case_open` | The open case in look-dev grey |
| `T_case_closed` | The closed case |
| `T_case_hasp` | The hasp |
| `T_band_detail` | Clasp, seal and jacquard |
| `T_case_c05` | The black stage at 70°: the mirror shows only the ceiling and the bulb |
| `T_props` | Carton, refill sealed and half-peeled, fan, loose band |
| `T_paper` | Setlist folded, fan and taped; refill peel |
| `T_previs_H01_sit`, `T_previs_H02_sit` | Poses a, d-A, d-B |
| `T_previs_H01_stand`, `T_previs_H02_stand` | Poses b-A, b-B, c |
| `T_hands` | Heart and point |
| `T_phone` | The phone grip |
