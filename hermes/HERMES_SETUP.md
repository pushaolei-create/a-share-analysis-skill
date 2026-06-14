# Hermes Setup

This guide assumes your Hermes runtime is the NemoHermes / NemoClaw flavor exposed through an OpenAI-compatible API.

## What To Configure

Hermes should be given:

1. A strong system prompt.
2. Access to the skill files in this repository.
3. A retrieval or file-loading rule that prioritizes:
   - `SKILL.md`
   - `references/analysis_framework.md`
   - `references/data_and_compliance.md`
   - `references/trading_playbook.md`

## Recommended System Prompt Strategy

Use `hermes/system-prompt.txt` as the base system prompt.

The prompt is designed to make Hermes:

- separate facts, estimates, and opinions
- verify time-sensitive market data before claiming it
- use the trading playbook only as a filter, not as a guarantee engine
- provide triggers, invalidation, and risk framing

## If You Run NemoHermes

The local endpoint is typically:

```text
http://127.0.0.1:8642/v1
```

Health check:

```text
http://127.0.0.1:8642/health
```

Common lifecycle commands mentioned by the local NemoHermes docs:

```powershell
nemohermes onboard
nemohermes my-hermes status
nemohermes my-hermes logs --follow
openshell forward start --background 8642 my-hermes
```

## How To Feed The Skill To Hermes

You have three workable options:

1. Mount or copy this repository into the Hermes sandbox and point your loader at the files directly.
2. Paste the contents of `SKILL.md` plus the three reference files into your Hermes knowledge base.
3. Use `hermes/system-prompt.txt` as the stable instruction layer and keep the reference files in retrieval.

Option 3 is the cleanest when Hermes supports prompt plus retrieval.

## Minimum File Set

If Hermes cannot load the whole repository, use these files first:

1. `SKILL.md`
2. `references/trading_playbook.md`
3. `references/analysis_framework.md`
4. `references/data_and_compliance.md`
