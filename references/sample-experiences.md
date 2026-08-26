# Sample Experiences

This file records reusable observations from the local sample set. It is optional prior knowledge, not a required input for every run. Read it only when the current source/reference pair resembles one of these scan types or when the user asks to use the accumulated sample experience.

The original images and OCR outputs are intentionally kept in the local test directory and are not part of the public repository.

## Sample Inventory

There are four independent sample groups. A later upload labeled Group 04 was byte-for-byte identical to Group 03 and did not add a new layout type.

| Group | Scan type | Reusable profile | Main handling rule |
| --- | --- | --- | --- |
| Initial group | Header, two-column body text, and a flowchart | `two-column-figure-mixed-v1` | Keep the flowchart as a protected visual zone unless figure-aware text replacement is reliable. |
| Group 01 | Two-column body-text page | `two-column-magazine-body-v1` | Use this as the simplest prior for stable columns, header, footer, and ordinary paragraph rerendering. |
| Group 02 | Flowchart/performance figure with lower two-column text | `two-column-figure-mixed-v1` | Do not merge OCR blocks across the figure zone; protect the binding edge and figure geometry. |
| Group 03 | Structured table with lower two-column text | `two-column-table-mixed-v1` | Detect cells first, translate cell by cell, and preserve grid lines and cell geometry. |

## Shared Observations

- The pages are portrait scans with a stable two-column body layout.
- A short header and centered page number are common but must still be detected from the current reference.
- Binding holes or scan shadow form a protected edge region. Text masks must not cover it.
- The reference image is the authority for the current run. These profiles are starting priors only.
- Body text uses pixel-measured wrapping, 40-42 px text, and explicit physical line spacing. Secondary text may use 36 px.
- Lists retain hanging indents so continuation lines align with the first content character.

## How To Use This File

1. Inspect the current reference image first.
2. Select a profile only if the page visibly matches its `applies_when` conditions.
3. Read the selected profile for initial regions and validation checks.
4. Override profile values when the current reference disagrees.
5. If no profile matches, use the base workflow and record the new scan type for later review.

Do not load all profiles or this file by default for a simple run. Do not treat sample-specific coordinates as universal constants.
