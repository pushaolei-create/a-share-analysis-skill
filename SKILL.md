---
name: a-share-analysis
description: Analyze mainland China A-share markets, sectors, themes, and listed stocks. Use when Codex needs to assess A-share broad-market conditions, policy and liquidity context, index performance, industry rotation, fund-flow clues, company fundamentals, valuation, catalysts, technical setups, trading plans, risks, or to draft an investment research note for SSE, SZSE, or BSE listed securities.
---

# A-Share Analysis

## Core Workflow

1. Confirm the request scope: market overview, sector or theme, single stock, peer comparison, earnings review, event impact, watchlist, or trading plan.
2. Gather current data before making claims. For anything time-sensitive, browse or use user-provided data; record source names, timestamps, and whether prices are delayed.
3. Read `references/analysis_framework.md` for market, sector, and single-stock analysis structure.
4. Read `references/data_and_compliance.md` when choosing sources, framing uncertainty, or handling financial-advice risk.
5. Read `references/trading_playbook.md` when the user asks about chart patterns, washout behavior, moving-average setups, buy and sell points, intraday T trading, or regime-specific tactics.
6. Produce a balanced report with thesis, evidence, counterarguments, trigger levels, risk controls, and explicit uncertainty.

## Data Discipline

- Prefer official sources for filings, exchange notices, index constituents, trading calendars, and regulatory actions.
- Use market data providers only for quotes, flows, valuation snapshots, consensus, and charts; state that third-party data can differ by provider.
- Do not infer real-time price, volume, limit-up status, northbound flow, margin balance, or announcements from memory.
- Use exact dates for financial periods, filing dates, ex-dividend dates, trading days, and backtests.
- Treat Chinese stock names as ambiguous; verify by ticker and exchange, for example `600519.SH`, `000333.SZ`, or `873001.BJ`.

## Output Standards

For market analysis, include:

- Index performance and breadth.
- Liquidity and policy context.
- Sector or theme rotation.
- Institutional or fund-flow clues.
- Near-term scenarios and risk triggers.

For single-stock analysis, include:

- Company identity, business segments, and listing venue.
- Latest filing or announcement check.
- Revenue, profit, cash-flow, and balance-sheet quality.
- Valuation versus history and peers.
- Catalysts, risks, and what would falsify the thesis.
- Technical context only as supporting evidence unless the user explicitly asks for a trading setup.

For short-term technical analysis, include:

- Regime: trend, range, rebound, distribution, or late-stage blow-off.
- Setup quality: structure, volume behavior, moving-average alignment, and failed-pattern risk.
- Trigger: what confirms entry, add, trim, or exit.
- Defense: invalidation, stop discipline, and position-sizing caveat.

## Optional Report Builder

Use `scripts/build_report.py` when the user provides structured data or when you have assembled data into JSON and want a consistent Markdown report.

```bash
python scripts/build_report.py --input data.json --output report.md
```

The script is intentionally data-provider-neutral. It formats supplied facts; it does not fetch live market data.
