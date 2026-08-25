# Translation Specification

Translation is block-based. Every source block keeps a stable ID through OCR, translation, rendering, and validation.

Preserve:

- headings and hierarchy;
- list markers and hanging-indent structure;
- numerals, units, dates, URLs, citations, and names;
- captions and footnotes as separate roles;
- deliberate emphasis when it can be represented by the selected font.

Do not invent content to fill empty space. If OCR confidence is low or a glyph is ambiguous, record it in the report and ask for review rather than silently guessing.

