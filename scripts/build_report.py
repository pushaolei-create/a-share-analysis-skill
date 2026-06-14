#!/usr/bin/env python3
"""Build a Markdown A-share analysis report from structured JSON data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SECTION_ORDER = [
    ("summary", "Summary"),
    ("market_context", "Market Context"),
    ("company_profile", "Company Profile"),
    ("fundamentals", "Fundamentals"),
    ("valuation", "Valuation"),
    ("technical_context", "Technical Context"),
    ("catalysts", "Catalysts"),
    ("risks", "Risks"),
    ("scenarios", "Scenarios"),
    ("sources", "Sources"),
]


def as_lines(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item not in (None, "")]
    if isinstance(value, dict):
        return [f"**{key}**: {val}" for key, val in value.items() if val not in (None, "")]
    return [str(value)]


def render_section(title: str, value: Any) -> str:
    lines = as_lines(value)
    if not lines:
        return ""
    body = "\n".join(f"- {line}" for line in lines)
    return f"## {title}\n\n{body}\n"


def build_report(data: dict[str, Any]) -> str:
    title = data.get("title") or "A-Share Analysis Report"
    subject = data.get("subject")
    as_of = data.get("as_of")
    header_bits = [f"# {title}"]
    if subject:
        header_bits.append(f"**Subject**: {subject}")
    if as_of:
        header_bits.append(f"**As of**: {as_of}")

    sections = []
    used = set()
    for key, title_text in SECTION_ORDER:
        section = render_section(title_text, data.get(key))
        if section:
            sections.append(section)
            used.add(key)

    extra = {
        key: val
        for key, val in data.items()
        if key not in used and key not in {"title", "subject", "as_of"}
    }
    if extra:
        sections.append(render_section("Additional Data", extra))

    disclaimer = (
        "## Disclaimer\n\n"
        "This report is for research and discussion only and is not individualized financial advice.\n"
    )
    return "\n\n".join(header_bits) + "\n\n" + "\n\n".join(sections + [disclaimer])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to input JSON data.")
    parser.add_argument("--output", required=True, help="Path to output Markdown report.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    data = json.loads(input_path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit("Input JSON must be an object.")

    output_path.write_text(build_report(data), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
