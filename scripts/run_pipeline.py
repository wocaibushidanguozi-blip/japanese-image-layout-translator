#!/usr/bin/env python3
"""Dependency-free orchestration contract for the image translation Skill.

This first version validates inputs and simulates the bounded loop. Real OCR,
translation handoff, masking, rendering, and validation executors can be
connected later without changing the manifest/report shape.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the image translation pipeline contract")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-iterations", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def capability_snapshot() -> dict[str, bool]:
    return {
        "python": True,
        "tesseract": shutil.which("tesseract") is not None,
        "pillow": importlib.util.find_spec("PIL") is not None,
        "opencv": importlib.util.find_spec("cv2") is not None,
        "renderer": importlib.util.find_spec("PIL") is not None and importlib.util.find_spec("cv2") is not None,
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.max_iterations < 1:
        raise SystemExit("--max-iterations must be at least 1")

    input_path = args.input.expanduser().resolve()
    reference_path = args.reference.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    missing_inputs = [str(path) for path in (input_path, reference_path) if not path.is_file()]
    capabilities = capability_snapshot()
    manifest = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "dry-run" if args.dry_run else "contract-only",
        "inputs": {"input": str(input_path), "reference": str(reference_path)},
        "options": {"max_iterations": args.max_iterations},
        "capabilities": capabilities,
        "platform": {"system": platform.system(), "release": platform.release(), "python": sys.version.split()[0]},
        "layout": {"body_font_px": [40, 42], "secondary_font_px": 36, "spacing_px": 25, "paragraph_gap_px": 40},
    }
    write_json(output_dir / "manifest.json", manifest)

    issues: list[dict[str, str]] = []
    if missing_inputs:
        issues.append({"code": "missing_input", "severity": "blocking", "detail": "; ".join(missing_inputs)})
    if not capabilities["pillow"] or not capabilities["opencv"]:
        issues.append({"code": "image_dependencies_unavailable", "severity": "blocking", "detail": "Pillow and OpenCV executors are not connected yet"})
    if not args.dry_run:
        issues.append({"code": "renderer_not_connected", "severity": "blocking", "detail": "Run with --dry-run until image executors are added"})

    iterations = [{"iteration": 1, "status": "blocked", "issues": issues}]
    report = {
        "schema_version": 1,
        "status": "blocked" if issues else "passed",
        "max_iterations": args.max_iterations,
        "iterations": iterations,
        "final_artifact": None,
        "next_action": "Connect image executors and provide source/reference images" if issues else "Write final.png",
    }
    write_json(output_dir / "report.json", report)

    print(json.dumps({"status": report["status"], "manifest": str(output_dir / "manifest.json"), "report": str(output_dir / "report.json")}, ensure_ascii=False))
    return 0 if args.dry_run else 2


if __name__ == "__main__":
    raise SystemExit(main())
