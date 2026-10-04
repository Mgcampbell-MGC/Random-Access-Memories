# Crash course: AI for beauty launch campaigns

For Matthew · checked 4 Oct 2026 · Sol's Portuguese version is a separate doc in the same folder.

## How to use this course

In about 90 minutes, 35 of reading and 57 of video, this takes someone from "I follow an AI creator" to knowing how the whole field works, and why her studio does one thing differently. Do it in one sitting, in order.

1. **The map** (5 min): the kinds of tools and how they fit.
2. **Image models, video models, platforms** (15 min): who is good at what, as of October 2026.
3. **Why labels break** (5 min): the problem the business is built on.
4. **Prompting** (5 min): the photographer's vocabulary in prompt form.
5. **A launch, step by step, and the Brazil rules** (5 min).
6. **The eight core videos** (57 min), with the notes on what to look for.
7. **The self-test** at the end. Eight of ten right means she is ready.

This world changes every month. The model sections carry the date they were checked; anything older than three months should be re-checked.

## The map

Four kinds of tools make an AI campaign: image models, video models, the platforms that rent them, and the finishing tools. Her studio adds one thing nobody else does: the brand's real packshot never goes near a model.

| Step | What goes in | What comes out |
| --- | --- | --- |
| 1. Image models (Nano Banana, GPT Image, Seedream, FLUX, Midjourney) | The brief only | Scenes with a flat blue stand-in where the product goes |
| 2. Video models (Seedance, Kling, Veo, Gemini Omni, MiniMax H3) | The brief, or a finished still | Clips with no readable label: rain, hair, hands, a street |
| 3. Platforms (Manus, Higgsfield, Flow, Krea) | Your account | Access to the models above behind one screen |
| 4. Her method: lay in the real pack by code | The brand's packshot file, straight from the brand | Every piece with the exact label |
| 5. Her method: check every piece and every film frame | Each finished piece | Pass or fail, in a report |
| 6. Finish and deliver | Approved pieces | Shadows, sound, files in every format, the report |

**The brand's packshot never goes into steps 1–3.** That one rule is the business.

## Image models

Google's Nano Banana family is the default for product and campaign stills in October 2026, and every serious model now advertises better text. Several makers still say in their own docs that small text or brand elements can fail. Checked 4 Oct 2026.

| Model | Maker | Latest | Good for | Its own stated weakness |
| --- | --- | --- | --- | --- |
| [Nano Banana 2](https://ai.google.dev/gemini-api/docs/image-generation) | Google | 26 Feb 2026 | The Gemini app's default. 4K, "reliable text rendering", keeps up to 4 people and 10 objects consistent. Portuguese is among its best languages. | Google advises generating the text first, then the image with it; every image carries an invisible SynthID watermark |
| [Nano Banana Pro](https://ai.google.dev/gemini-api/docs/image-generation) | Google | Nov 2025 | "Accurate brand consistency", up to 14 reference images. It powers Manus's Design View. | Same advice on text |
| [GPT Image 2.5](https://developers.openai.com/api/docs/guides/image-generation) | OpenAI | Sep 2026 | Precise editing with masks, several references, transparent backgrounds, up to 4K. | "Can still struggle with precise text placement" and "brand elements" |
| [Seedream 5.0 Pro](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro) | ByteDance | 8 Jul 2026 | Dense text, lasso editing, splits an image into layers, realistic skin. | "Room to improve in finer-grained text rendering" |
| [FLUX 3 Image](https://bfl.ai/models/flux-3-image) | Black Forest Labs | Family announced 23 Jul 2026 | Native 2K and 4K, 10 references, layout by drawn boxes, a commercial licence. | Release date not published |
| [Midjourney V8.2](https://updates.midjourney.com/version-8-2/) | Midjourney | 24 Jul 2026 | The strongest "look" and mood. Text works better "when specified in quotes"; `--raw` for photographic results. | "Still working on the default aesthetics of V8" |
| [Ideogram 4.5](https://docs.ideogram.ai/) | Ideogram | 4.5 (date not published) | Built for text in images: separates text into layers, transparent backgrounds, ad resizing. | — |
| [Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) | Alibaba (open) | 14 Sep 2026 | Free open model; transparent output; keeps people and products consistent. | — |
| [Recraft V4.1](https://www.recraft.ai/docs) | Recraft | V4.1 | Vector (editable SVG) and a flat, front-lit "Utility" mode for mockups. | — |

**What this means for her.** Use Nano Banana (inside Manus or Gemini) for scenes, worlds and hands, always with the blue stand-in. "Better text" is real progress for headlines; it is not a guarantee for a brand's ingredient list at 2 mm, and the makers say so.

## Video models

In October 2026 the leaders are Seedance 2.5 and Kling, with Google's Veo and its new Gemini Omni close behind; Sora is gone. Every maker admits a weakness, and for several it is text or object detail, which is exactly the label problem. Checked at each maker's own pages on 4 Oct 2026.

| Model | Maker | Latest | Good for | Its own stated weakness |
| --- | --- | --- | --- | --- |
| [Seedance 2.5](https://ai.byteplus.com/en/activity/seedance2-5) | ByteDance | 2.5, 31 Jul 2026 | Up to 30 s in one take, native audio, up to 30 reference images, edits by timestamp, 1080p. Runs inside Manus's Video Editor. | On 2.0: "text rendering accuracy"; on 2.5: complex motion and multi-subject interaction |
| [Kling](https://www.klingai.com/blog/kling-4-vs-3) | Kuaishou | 3.0 now; 4.0 "will officially launch in October" | 3.0: 3–15 s, up to native 4K, audio, start and end frames, 7 references. 4.0: 30 s, 10 keyframes, 10-bit HDR, and adds Portuguese. | 3.0 is 8-bit SDR and Portuguese is not one of its main languages |
| [Veo 3.1](https://ai.google.dev/gemini-api/docs/veo) | Google DeepMind | 3.1 (Oct 2025; 9:16 and 4K added Jan 2026) | 4–8 s clips, 3 reference images, first and last frame, extends to 141 s, audio always on. In Flow and Gemini. | Only English speech is "fully supported"; other languages "have not been evaluated" |
| [Gemini Omni Flash](https://ai.google.dev/gemini-api/docs/video) | Google | 19 May 2026 | Google now says *"Use Gemini Omni Flash as your default model for video generation"*. Edits by conversation, extends to 40 s. | Native 720p (1080p and 4K are upscaled); character consistency across scene changes |
| [MiniMax H3](https://www.minimax.io/blog/minimax-h3) | MiniMax (formerly Hailuo) | 31 Jul 2026 | Up to 15 s at 2K, stereo audio, first and last frame. Also in Manus's Video Editor. | "Visual detail can still be improved in certain scenarios" |
| [Runway Gen-4.5 and Aleph 2.0](https://runwayml.com/changelog) | Runway | Gen-4.5 Dec 2025; Aleph 2.0 May 2026 | 2–10 s, HDR and ProRes delivery; Aleph edits footage that already exists. | Object permanence: "a cup vanishing after being occluded" |
| [Wan 3.0](https://www.alibabacloud.com/help/en/model-studio/wan3-0-video) | Alibaba | 3.0 (API only); open weights stop at 2.2 | Up to 30 s at 1080p, first and last frame. | Launch date not published |

**Gone or minor:** OpenAI shut the Sora 2 API on 24 Sep 2026 with no replacement ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)); old Sora tutorials are history. Luma Ray3.2, Pika 2.5, Grok Imagine Video 1.5, FLUX 3 Video and Midjourney's video model (5 s, 720p) exist; she does not need them.

**What this means for her.** Her daily model is Seedance, because it is the one inside Manus's Video Editor. She uses generated video only for shots with no readable label: rain, hair, hands without the product, a street. The label shots are her finished stills with a camera move.

## Platforms, finishing and sound

A platform rents several models behind one screen and adds presets; the model underneath is often the same one everyone else uses. That is why two "different" tools can give the same look. Her studio is Manus; the others are worth knowing because her clients and competitors use them.

| Platform | What it is | Worth knowing |
| --- | --- | --- |
| [Manus 2.0](https://manus.im/blog/introducing-manus-2-0) | An AI agent that plans and does the work; 2.0 launched 28 Sep 2026 | Its [Video Editor](https://manus.im/blog/introducing-video-editor) gives a layered timeline, *"You don't get a flattened MP4"*, built for 30–60 s product ads. Video Editor models: Seedance 2.5, 2.0, 2.0 Fast, MiniMax H3; Canvas adds Veo 3.1 ([help](https://help.manus.im/en/articles/11711172-what-can-manus-video-generation-feature-do)). [Design View](https://manus.im/docs/features/design-view) runs on Nano Banana Pro. |
| [Higgsfield](https://higgsfield.ai/marketing-studio) | A reseller of about 120 models plus its own | Soul 2.0 for realistic UGC and fashion; Marketing Studio for one-click product ads (4–30 s, up to 6 product images). Many YouTube creators are sponsored by it. |
| [Google Flow](https://flow.google.com/) | Google's video studio | Veo 3.1 with Ingredients, Frames to Video, Extend and Insert; Omni Flash is arriving. |
| [Krea](https://www.krea.ai/) | A multi-model studio | Its own Krea 2 plus Seedance, Nano Banana, Veo, Kling and others; an enhancer that upscales very large. |
| [Magnific](https://docs.freepik.com/llms.txt) | Freepik's developer platform, now under the Magnific name | Mystic, Kling, Seedance, and the best-known upscalers (Precision and Creative). |
| [Runway](https://docs.dev.runwayml.com/guides/models/) | Its own models, and now a reseller too | Serves Seedance, GPT Image, Nano Banana, Seedream and Magnific upscalers through one account. |
| [Adobe Firefly](https://www.adobe.com/products/firefly.html) | Adobe's models plus partners | Sits next to Photoshop, which she uses for hand finishing. Partner list not fully checked. |

**Finishing.** Photoshop is where she adds contact shadows and fixes edges, on the scene only. [Topaz](https://www.topazlabs.com/gigapixel) and Magnific upscale images and video. **An AI upscaler repaints detail, labels included**, so upscale the scene before the pack goes in, never the finished picture.

**Sound.** [ElevenLabs](https://elevenlabs.io/pricing) v4 (28 Sep 2026) makes voices in 90+ languages; its commercial licence starts on a paid plan, and its music excludes film, TV and games. [Suno](https://help.suno.com/en/articles/2416769) v6 makes songs: on a paid plan she owns them and keeps commercial rights; free-plan songs belong to Suno. For client work, only music she owns.

## Why AI breaks product labels, and the method that fixes it

Every image and video model redraws the product from scratch, so small text on a label comes out wrong. This is the single fact the whole business is built on.

**Why it happens.** A generator does not copy your file. It paints a new picture that resembles what it was shown. Big shapes survive; small letters get guessed. The smaller the text and the more the product moves, the worse it gets.

**What we measured ourselves:**

- **Climate Rescue, the founder's own fictional ad (28 Sep 2026):** the hero shot reads *RESSCUE* in every frame. Two words on the label, and the generator still added a letter, in the one shot a customer reads.
- **A real bestselling tube (25 Sep 2026):** both of Higgsfield's own product-ad options misspelled ingredient names, with 2 and 4 errors.
- **Climate case study (1 Oct 2026):** the stills read correctly, but two film frames smear the label until it cannot be read. Motion is where labels die.

**What the tool makers admit.** Manus says its first video cut is *"80 to 90 percent there"* and tells you to *"drag in your own product shot"* to fix it. Riverflow's help centre says *"small text is still one of the hardest details to preserve"* and sells human label repair per image.

**The fix: the AI never draws the label.**

1. Generate the scene with a **flat chroma-blue stand-in** where the product goes. Prompt: *"the whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare"*.
2. Lay the brand's **real packshot file** over the stand-in **by code** (`compor.py`). It is resized, tilted and relit, never redrawn.
3. **Check** every image and every film frame against the brand's file (`relatorio_fidelidade.py`). It catches a redrawn, garbled, distorted or recoloured label.
4. **Look at every label yourself at 100% zoom.** The check can miss one look-alike letter in tiny print (*secos* to *secas*), so a person always looks.

**Two rules that keep it safe.** Once the real pack is in, no AI editing of that picture: "edit image" tools repaint everything, label included. And in a film, only shots with no readable label may be generated; shots with the pack use the finished still as a layer that the camera moves over.

## Prompting for beauty and product

A good prompt reads like a photographer's shot note: what, where, light, lens, mood, and what must not appear. Her runway years are an advantage here, because she already knows how a set is lit and how a body holds a product.

**The six parts of every prompt, in this order:**

1. **Subject:** the product (as the blue stand-in) and, if any, the hand or person.
2. **Setting:** surface, props, place (*wet stone ledge, travertine counter, sea foam*).
3. **Light:** source and direction (*soft window light from the left, golden hour backlight*).
4. **Camera:** lens, distance, angle (*85mm, eye level, front-facing*).
5. **Mood and palette:** three or four words (*calm, mineral green, warm*).
6. **Constraints:** *no text anywhere in the image, no logo, no glare*, plus the stand-in sentence.

**The beauty shot list, and how each is usually made:**

| Shot | What it shows | Lens | Light |
| --- | --- | --- | --- |
| Hero / key visual | The product alone, the campaign's main picture | 85–100mm | Large soft source, one side, gentle rim behind |
| In hand | A hand holding the pack upright, label facing camera | 85mm | Soft, even, skin-flattering |
| In use | Texture on skin or hair, the pack beside it | 100mm macro | Soft key, a little gloss on the texture |
| Flat lay | Product and props from above | 35–50mm | Even, shadowless or one soft shadow |
| Lifestyle / mood | The product small in a real-feeling place | 35mm | Natural: window, golden hour, overcast |
| Detail | Cap, drop, swatch, condensation | 100mm macro | Hard light for crisp edges |

**Words that move the result:**

- **Light:** softbox, beauty dish, window light, overcast, golden hour, backlight, rim light, hard sun with crisp shadows, gobo shadow (shapes like leaves or blinds).
- **Materials:** frosted glass, amber glass, matte, satin, glossy, metallic cap, condensation droplets.
- **Skin realism:** *visible skin texture, natural pores, no retouched plastic skin*. Generated skin is too smooth by default.
- **Hands:** keep the pose simple; fingers below the middle of the label; the pack upright and front-facing. Hands are where generators still fail most often after text.

**Video: one move per clip.** Clips are usually 5–10 seconds, so give each clip one camera move and one action.

- **Push-in:** the camera moves slowly toward the product. The safest premium move.
- **Dolly or truck:** the camera slides sideways past the scene.
- **Orbit (arc):** the camera circles the product. Avoid it with a readable label: the pack turns and the text breaks.
- **Tilt, rack focus, handheld:** tilt moves up or down; rack focus shifts focus from front to back; handheld adds a light, human shake for UGC.
- **Start and end frame:** give the model the first and last pictures and let it fill the motion between. The best control there is.

**Example, key visual (with the stand-in):**

> A tall bottle standing on a wet stone ledge by a rain-streaked window, city lights blurred behind, soft overcast light from the left, cool blue-grey and mineral green palette, fine water droplets on the stone, 85mm lens, eye level, front-facing, the whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare, no text anywhere in the image.

## A launch campaign, from brief to delivery

A full O LANÇAMENTO is nine steps and about 4–4,5 hours of her own time, spread over 5–7 working days (an estimate until her first timed practice runs). The brand's waiting time is most of the calendar.

1. **Brief and files.** The brand sends its product image, label art, the product sheet and the list of phrases it approves. Nothing starts without these.
2. **Three visual worlds.** She proposes three directions (for example *After the Rain*, *Morning Bathroom*, *Solid Colour Studio*), each with the real pack already applied. The brand picks one in writing.
3. **Scenes with the blue stand-in.** The key visual in 9:16, six campaign images in 4:5, three store images in 1:1. Two or three options each; she picks.
4. **Apply the real pack and check.** The script lays the brand's file over the stand-in; the checker passes or fails each piece.
5. **Hand finishing.** Contact shadow, edges and reflections, on the scene only, never on the pack.
6. **Text.** The approved phrases go beside the pack by code, never over it.
7. **Film.** The approved key visual becomes a 15 s vertical film: a slow camera move, an opening shot with no product (rain, hair, a street), the phrases, AI-made music. Two 6 s cuts. Every frame is checked.
8. **Approval and one round of changes.** The brand approves in writing. A change is made by changing the scene, never by editing the finished picture.
9. **Delivery.** The files in every format, the check report, and the licence and rights transfer.

**What she sells is the whole set in one visual world, with labels proven against the brand's own file.** Any single picture is cheap; a coherent launch with a guarantee is not.

## The rules in Brazil

No Brazilian law requires an "AI" label on an ad today, but the platforms do, and four rules decide what she may make and sell. Laws are moving, so re-check these every quarter.

**AI labelling.**

- The AI bill, [PL 2338/2023](https://dadosabertos.camara.leg.br/api/v2/proposicoes/2487262), was still *"Aguardando Parecer"* in the Câmara on 2 Sep 2026. Not law.
- [CONAR's codes](https://www.conar.org.br/codigos?section=codigo) apply the normal advertising rules to AI-made ads. CONAR has already suspended an ad that used a deepfake of a known TV presenter.
- [TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-ai-generated-content) requires a label on realistic AI-made people and scenes. [Meta](https://transparency.meta.com/governance/tracking-impact/labeling-ai-content/) adds "AI info" from the file's provenance marks.
- **Her practice:** the delivery note tells the brand to switch the platform's AI label on. Wherever a synthetic person appears, a small *"imagem ilustrativa criada com IA"*.

**Who owns the pictures.** Brazilian copyright law ([Lei 9.610, art. 11](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm)) names a natural person as the author, and purely AI-made elements may not be protected. So she never says "the images are yours". She sells an **exclusive licence**, a **written transfer of whatever rights she holds**, and **her promise never to reuse** the work.

**Claims belong to the brand.** Only phrases from the brand's signed list appear, word for word. Watch words like *trata, cura, previne, clinicamente comprovado, %, em X dias, aprovado pela Anvisa, natural, vegano* appear only if they are on the label or the brand has the proof.

**Never make:**

- before-and-after, or any sequence that implies a result;
- treatment or cure claims; lab coats, clinics, stethoscopes;
- a synthetic person giving a testimonial or review;
- a face that resembles any real person, famous or not;
- an ingredient that is not on the label;
- anything aimed at children.

**Keep a record.** For every synthetic person, save the prompt and the date it was generated. If anyone ever asks, she can show it was invented.

## The watch list

Eight core videos, 57 minutes, in this order; everything after them is optional. Every link was checked against YouTube on 4 Oct 2026. Most creators sell a course or are sponsored by a tool (several by Higgsfield), so treat their verdicts as marketing, and note that none of them composites the real pack: they let the AI draw it.

**Core, in order (57 min):**

| # | Video | Channel | Length | Why, and what to look for |
| --- | --- | --- | --- | --- |
| 1 | [Lighting & Styling Breakdown for Skincare Product Shoot](https://www.youtube.com/watch?v=WM78JenzGAc) | Amanda Campeanu | 6:22 | What good looks like: a real skincare shoot, light by light. |
| 2 | [Nano Banana AI prompts for beauty brands](https://www.youtube.com/watch?v=VFXeOdQEMCs) | Amanda Campeanu | 6:06 | The same photographer turning craft into prompts, and where AI does not help. |
| 3 | [Keeping product text consistent with Nano Banana Pro and Kling 3.0 Omni](https://www.youtube.com/watch?v=XLHTLJhzDyQ) | Magnific | 6:08 | The label problem, from a tool maker: which motion settings keep text, and where it still fails. |
| 4 | [Kling 4.0 vs Seedance 2.5 — Best AI Video Generator in 2026?](https://www.youtube.com/watch?v=YH1LLoBPx0Y) | Dom the AI Tutor | 9:47 | The two leading video models on 11 identical prompts. At 8:47, a cosmetic-bottle test of label legibility. |
| 5 | [I Tested Seedance 2.5 for Product Ads](https://www.youtube.com/watch?v=y6Zw5WFs62k) | Thomas Lundström | 8:42 | Seedance on product ads; at 1:52, locking the environment. Sponsored. |
| 6 | [How to Use Google Flow (Step-by-Step Tutorial)](https://www.youtube.com/watch?v=0vQ7UEe7rLg) | Kevin Stratvert | 9:15 | Google's Veo inside Flow, building a commercial from storyboard to edit. |
| 7 | [Mastering AI Video: 42 Camera Movement Vocabulary for Prompts](https://www.youtube.com/watch?v=HOjCT6TxlHM) | AI Shot Studio | 10:16 | A visual dictionary of camera moves: dolly, push-in, orbit, macro. |
| 8 | [Introducing Manus Video Editor](https://www.youtube.com/watch?v=OSaWc0sBspA) | Manus AI | 0:53 | The official demo of the editor she will finish films in. |

**Optional, by topic:**

| Topic | Video | Channel | Length |
| --- | --- | --- | --- |
| Ranking of all video models | [AI Video Generators Ranked from Worst to Best (2026)](https://www.youtube.com/watch?v=v6bqRIjwddE) | Youri van Hofwegen | 19:13 |
| Seedance, skincare | [How to Create Skincare Commercials with AI – Seedance 2.5 Ep. 03](https://www.youtube.com/watch?v=kKILF7Zx_OE) | AI Tech Pro | 6:14 |
| Seedance, deep prompting | [Seedance 2.5 is an ABSOLUTE MONSTER - Master it in 20 minutes](https://www.youtube.com/watch?v=UxwV16jDglA) | Dan Kieft | 23:09 |
| Veo, start and end frames | [Mastering Start and End Frames in Google Flow (2026)](https://www.youtube.com/watch?v=Qg0VG_qqxww) | AI Mind Revolution | 19:48 |
| Kling 4.0, what is new | [Kling 4.0 AI Video Generator: First Look](https://www.youtube.com/watch?v=nXlryGZLrg4) | JSFILMZ | 14:05 |
| Higgsfield, beauty ads | [I Created 10+ Beauty Ads in 1 Hour](https://www.youtube.com/watch?v=fmgVm-fxPDM) | Higgsfield AI (vendor) | 20:14 |
| A real paid skincare job | [How I Created an AI Skincare Ad for an Upwork Client](https://www.youtube.com/watch?v=1O8lbB01-nU) | Finaltouch | 17:47 |
| Manus 2.0 overview | [Introducing Manus 2.0](https://www.youtube.com/watch?v=hZVH-y1atWw) | Manus AI | 2:47 |
| Fixing the real logo back in | [AI Product Image Problem Solved – Keep Logo & Text Same](https://www.youtube.com/watch?v=WQ_XUm9-Rr0) | Designshala | 8:25 |
| Where product AI fails | [Why Your AI Product Images Are Failing](https://www.youtube.com/watch?v=R7Eml0ttQtg) | Escapism | 25:43 |
| UGC holding a product | [How To Make Realistic AI UGC That Holds Your Product](https://www.youtube.com/watch?v=ikMdmEvMtmk) | Ads with Cami | 8:17 |
| Lighting words for prompts | [The Ultimate Guide to Cinematic Lighting (20 Prompts)](https://www.youtube.com/watch?v=RCHw0PtE92M) | Dom the AI Tutor | 10:23 |
| Product lighting for film | [Product Lighting – Commercial Cinematography 101](https://www.youtube.com/watch?v=kjv-n7CeBNY) | Aputure | 7:41 |
| MikoxAI, realism | [Hyper-Realistic AI Images with Nano Banana Pro](https://www.youtube.com/watch?v=_D-7SamsJdY) | Miko | 10:23 |
| MikoxAI, UGC | [How to Make Viral AI UGC Ads in 2026](https://www.youtube.com/watch?v=x_TAoTi3ras) | Miko | 15:28 |

Sol's Portuguese version has its own core list: five Brazilian videos and two short English ones with Portuguese auto-subtitles (55 min), plus five Brazilian channels to follow.

## Glossary

The words people in this world use without explaining them, with the Portuguese she will hear on Brazilian channels.

| Term | What it means | Em português |
| --- | --- | --- |
| Model | The AI engine itself (Seedance, Veo, Nano Banana). Platforms rent several. | modelo |
| Platform | A site or app that gives access to several models, with presets (Higgsfield, Manus, Freepik). | plataforma |
| Prompt | The written instruction. | prompt |
| Text-to-image / text-to-video | A picture or clip made from words alone. | texto para imagem / vídeo |
| Image-to-video | A clip that starts from a picture you give. The main way to control a film. | imagem para vídeo |
| Reference image | A picture the model must follow (a face, a style, a product). | imagem de referência |
| Start and end frame | The first and last pictures of a clip; the model fills the motion between. | quadro inicial e final |
| Inpainting / outpainting | Repainting a part of a picture / extending it beyond its edges. | inpainting / expandir |
| Upscale | Making a picture or video larger and sharper. AI upscalers repaint detail, labels included. | ampliar / upscale |
| Consistency | Keeping the same face, product or style across many pictures. | consistência |
| Seed | The random number behind a result. Same seed + same prompt = a similar result. | seed / semente |
| Aspect ratio | The frame's shape: 9:16 vertical, 4:5 feed, 1:1 square, 16:9 wide. | proporção |
| Credits | The currency most platforms charge in; video costs far more than images. | créditos |
| Packshot | A clean photo of the product alone, usually on white. | packshot / foto still |
| Key visual (KV) | The campaign's main picture; everything else follows its world. | key visual |
| Chroma stand-in | A flat blue (or green) object standing where the product will go, so the real one can be laid on top. | embalagem azul / chroma |
| Composite | Laying one image over another by code or Photoshop, without redrawing it. | composição / aplicar |
| UGC | "User-generated content": the selfie-style ad where a person holds the product and talks. | UGC |
| Lip-sync | Making a face's mouth match a voice. | sincronia labial |
| B-roll | Supporting shots with no talking: rain, hair, a street, hands. | b-roll / planos de apoio |
| Cut / cutdown | A shorter version of the film for ads (6 s, 15 s). | corte |
| BT.709 | The colour standard phones expect. A wrongly tagged file shows the pack's colours shifted. | BT.709 |
| Provenance (C2PA) | Hidden marks in a file saying it was made with AI; Meta reads them. | proveniência |

## Self-test: ten questions

If she can answer eight of these without looking, she knows more than most people selling AI content in Brazil.

1. Why do AI models misspell product labels, and why is it worse in video?
2. What is a chroma stand-in, and what exact words go in the prompt?
3. After the real pack is laid in, why is "edit image" forbidden on that picture?
4. What is the difference between a model and a platform? Name two of each.
5. Which camera move is safest for a premium product film, and which one breaks a label?
6. What does image-to-video with a start and end frame let you control?
7. What does the label check catch, and what can it miss?
8. Why does she never write "the images are yours" in a contract?
9. Name four things she never makes for a beauty brand.
10. A brand sends a new label after approval. What happens?

**Answers.**

1. They repaint the product instead of copying it, and small letters get guessed; in video it is repainted in every frame.
2. A flat blue product placed where the real one goes. *"The whole bottle including the cap in flat matte chroma blue, no text, no logo, no glare."*
3. Those tools repaint the whole picture, label included.
4. A model is the engine (Seedance, Veo, Nano Banana, Kling); a platform gives access to several (Higgsfield, Manus, Freepik).
5. A slow push-in is safest; an orbit turns the pack and breaks the text.
6. Where the clip starts and ends, so the model only invents the motion between.
7. It catches a redrawn, garbled, distorted or recoloured label. It can miss one look-alike letter in tiny print, so a person always looks at 100%.
8. The law names a person as author and AI elements may not be protected; she sells an exclusive licence, a rights transfer and a promise not to reuse.
9. Before-and-after; treatment or cure claims; a synthetic person giving a testimonial; a face like a real person (also: lab coats, ingredients not on the label, ads aimed at children).
10. The brand signs a new product sheet naming the new file, and the pack is applied again from that file.
