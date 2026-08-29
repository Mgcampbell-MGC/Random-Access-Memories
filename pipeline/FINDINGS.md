# SCAN KEEPSAKE PIPELINE — build log and first findings, 21 Aug 2026

**Built rather than argued. Three findings, one of which changes the product.**

## What was built
`pipeline/scan_pipeline.py` — a fully deterministic 7-stage pipeline. Same input ⇒ same output.
No model, no per-unit human judgment. Stages: ingest → **redact** → despeckle → **isolate** →
tonemap → compose → export.

The two stages that make it not a catalogue item (Shutterfly/Etsy can do neither):
- **REDACT** — clinic scans carry burned-in PHI (mother's name, DOB, hospital, machine settings) as
  bright thin text over the dark surround. Detected by intensity + thin-structure morphology, then
  **inpainted from the local surround** rather than blurred (blur leaves a legible ghost). This is
  simultaneously the privacy requirement and the hardest automatable step.
- **ISOLATE** — ultrasound speckle is *multiplicative*, so ordinary denoising smears the subject.
  Handled in log space where it becomes additive.

## Finding 1 — throughput is a non-issue, by three orders of magnitude
**264 ms per unit**, end to end, at 3600×4800 output. The pre-committed bar was **≤3 min/unit**.
At 43 h/month (C9) that is **~586.000 units of theoretical capacity** against the ~40 the business needs.
**Her hands were never going to be the constraint. That question is settled and can be closed.**

## Finding 2 — the build exposed two bugs that analysis had not
1. `thumbnail()` only shrinks, never enlarges — a 223×297 source sat at native size inside a
   3600×4800 canvas. Fixed with an explicit scale-to-fill.
2. **`isolate()` was wrong for a whole input class.** It assumed a bright scan sector on a dark
   surround. A 3D/4D render fills the frame with no surround, so "largest bright component" selected
   a random blob. **Now classified by measuring dark fraction: SECTOR ⇒ cut out; FULL-FRAME ⇒ soft
   vignette.** Two input classes needing opposite treatment is a real product requirement that would
   have surfaced only on contact with real files.

## ★★ Finding 3 — RESOLUTION IS THE BINDING CONSTRAINT, AND IT RESIZES THE PRODUCT

| source | px | @200 dpi | verdict |
|---|---|---|---|
| thermal printout scan *(what we tested)* | 223×297 | 1,1×1,5 in | too small to print |
| typical clinic JPEG export | 640×480 | 3,2×2,4 in | too small to print |
| mid ultrasound digital export | 1024×768 | 5,1×3,8 in | **5×7 card OK** |
| modern machine / DICOM frame | 1920×1080 | 9,6×5,4 in | **8×10 OK** |
| 4D render, high-end studio | 2048×1536 | 10,2×7,7 in | **12×16 OK** |

> **The iris/retina comparables ($309–409) are LARGE format — 20×30 and 24×36 in. A 20×30 at 200 dpi
> needs 4000×6000 px. NO ultrasound source reaches that.**
>
> ⇒ **The ultrasound artifact is a SMALL-FORMAT product (5×7 to 8×10), not wall art, and its price
> must be set from the small-format market — NOT from the iris studio numbers.** This is the first
> hard constraint found on #3's pricing, and it was invisible from the desk.

## What this does and does not settle
- **SETTLED:** it is a machine, not her hands. Decisively.
- **SETTLED:** output quality is good enough to look like a product at the right size (see
  `out/_contact_sheet.jpg` — three palettes, one input, zero human choices).
- **OPEN, and now the top question:** *what resolution do clinics actually hand over?* That single
  number sets the print size, which sets the price, which sets everything. **It is one email to one
  clinic, or one look at a real export file.**
- **OPEN:** the redact stage has not been tested on a real scan with burned-in PHI — the only sample
  obtained was a cropped 3D render (redacted area 0,0%). **That is the stage most likely to break.**

## Sourcing note
Wikimedia rate-limited the shared proxy egress (HTTP 429) and only one usable public-domain image was
retrieved. **The 20-image stopwatch test still needs real, varied clinic files** — ideally including
2D sector scans with visible overlay text.
