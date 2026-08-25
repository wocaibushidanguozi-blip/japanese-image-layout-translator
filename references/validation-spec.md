# Validation Specification

Blocking checks:

- no text block exceeds its assigned content bounds;
- no text block runs below the canvas;
- no rendered blocks overlap unless explicitly allowed;
- no Japanese residue remains inside replaced text masks;
- masks do not cover protected non-text regions;
- output dimensions and format match the manifest.

Warnings may include small reference drift, low OCR confidence, or an unclassified text role. A warning does not make `final.png` invalid, but it must remain in `report.json`.

The report should identify each issue with a stable block ID and a suggested correction, so the next loop iteration can target the affected block instead of rerunning the entire page blindly.

