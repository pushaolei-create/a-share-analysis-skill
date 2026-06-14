# A-Share Analysis Skill

Codex skill for mainland China A-share market analysis, sector rotation analysis, single-stock research, and short-term technical trading review.

## What It Includes

- `SKILL.md`: the core skill entry point
- `references/analysis_framework.md`: market, sector, and single-stock analysis framework
- `references/data_and_compliance.md`: source selection and compliance notes
- `references/trading_playbook.md`: distilled short-term trading playbook
- `scripts/build_report.py`: Markdown report builder from structured JSON

## Main Capabilities

- A-share broad market analysis
- Sector and theme rotation analysis
- Single-stock fundamental and valuation review
- Technical setup review for breakouts, pullbacks, reversals, washouts, and moving-average behavior
- Buy-point, trim-point, and invalidation framing

## Use In Codex

Place this folder under:

```text
C:\Users\Administrator\.codex\skills\a-share-analysis
```

Then invoke it with:

```text
$a-share-analysis
```

## Hermes Integration

If you want to use this as a knowledge pack or system prompt source for a Hermes agent, see:

- `hermes/HERMES_SETUP.md`
- `hermes/system-prompt.txt`

## Notes

This repository focuses on reusable analysis structure and trading heuristics. It does not fetch live market data by itself, and it should not be treated as individualized financial advice.
