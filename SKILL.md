---
name: japanese-image-layout-translator
description: Translate Japanese text in an image into Chinese and rebuild the image using a supplied layout reference. Use for Japanese-to-Chinese image translation where preserving coordinates, columns, spacing, typography, and PNG output matters.
metadata:
  short-description: Rebuild Japanese images in Chinese with reference-matched layout
---

# Japanese Image Layout Translator

Use this skill for image translation jobs with two inputs:

- `input`: the Japanese source image.
- `reference`: the golden layout reference image.

The target is a Chinese PNG that preserves the source image's non-text visual content and follows the reference image's layout. Do not use character-count wrapping or an external translation API.

## Operating Model

Codex performs translation and visual decisions in the current task. Local scripts perform deterministic work: image inspection, OCR, masking, font measurement, rendering, and validation. A script must never claim success when its required image dependency or OCR engine is unavailable.

Start by running:

```bash
python3 scripts/run_pipeline.py \
  --input /path/to/source.png \
  --reference /path/to/reference.png \
  --output-dir /path/to/output \
  --dry-run
```

The current repository version provides the dry-run contract only. It is intentionally dependency-free. When image executors are added, preserve the same manifest and report contract.

## Required Workflow

1. Inspect the reference before choosing output dimensions or typography. Record canvas ratio, column count, content bounds, margins, paragraph gaps, and text hierarchy.
2. OCR the source while preserving text-block coordinates, reading order, confidence, orientation, and list markers. Keep headers, footers, captions, and references as separate roles.
3. Translate each block into natural Chinese while preserving block identity, list structure, numbers, URLs, citations, and intentional line breaks.
4. Build masks only from detected text regions. Do not cover nearby headers, page numbers, charts, rules, textures, or illustrations.
5. Render with pixel-based measurement using the selected font and `ImageDraw.textlength` (or an equivalent font metric). CJK text may wrap per glyph; Latin words, URLs, numbers, and punctuation need token-aware handling.
6. Preserve list hanging indents. The continuation line begins at the first content character, not at the list marker.
7. Run bounded visual validation. Check width overflow, bottom overflow, block overlap, Japanese residue, mask damage, and reference-layout drift.
8. If validation fails, revise only the affected blocks or layout parameters and rerender. Use at most the configured iteration limit, defaulting to 4. Stop early when all blocking checks pass.
9. Save the final PNG, the run manifest, the validation report, and intermediate drafts. A failed run must be explicit and must retain its report.

## Default Layout Policy

Use these as defaults only when the reference analysis does not provide a better value:

- Standard canvas: `2480 x 3508` only when A4 normalization is requested; otherwise preserve the source aspect ratio.
- Body font size: `40` to `42` px.
- Secondary text: `36` px.
- Render spacing: `25` px.
- Paragraph gap: `40` px.
- Anchor: top-left.
- PNG save: lossless PNG; `optimize=False` and a low compression level are acceptable performance settings.

Do not force these values when they visibly conflict with the reference. Record any override in the manifest.

## Loop Contract

The loop is a bounded correction loop, not a network retry loop:

```text
analyze -> translate -> mask -> render -> validate
                         ^                 |
                         +-- revise ------+
```

Each iteration must produce a report with blocking issues and the affected block IDs. If an iteration does not improve the blocking issue, stop and report the failure instead of looping indefinitely.

## Output Contract

The output directory must contain:

```text
manifest.json       # inputs, options, detected capabilities, chosen layout
report.json         # per-iteration checks and final status
draft-01.png        # produced only when the renderer is available
...
final.png           # produced only after a passing validation
```

Never include credentials, raw API keys, or private source material in a published Skill repository.

