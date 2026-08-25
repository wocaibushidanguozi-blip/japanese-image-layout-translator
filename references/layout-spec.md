# Layout Specification

The reference image is the source of layout truth. Before rendering, record these fields in `manifest.json`:

```json
{
  "canvas": {"width": 0, "height": 0, "aspect_ratio": 0},
  "columns": 1,
  "content_bounds": {"left": 0, "top": 0, "right": 0, "bottom": 0},
  "margins": {"left": 0, "right": 0, "top": 0, "bottom": 0},
  "paragraph_gap_px": 40,
  "body_font_px": 40,
  "body_spacing_px": 25,
  "secondary_font_px": 36
}
```

Use normalized coordinates while analyzing and convert to output pixels only after the output canvas is selected. This prevents a reference at a different resolution from changing the intended proportions.

Do not infer a column merely from a large empty region. Confirm it from repeated text-block alignment. Keep decorative elements outside the text mask.

