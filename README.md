# Claude Haiku 5.5 for Prime Agent

Prime Agent's model catalog does not list `anthropic/claude-haiku-5-5` yet. This adds it locally.

## Install

    curl -fsSL https://raw.githubusercontent.com/GorianSt/prime-agent-haiku-5-5/main/install.py | python3

Then restart the daemon so it reloads the catalog:

    pkill -f "prime-agent --mode daemon"

Start Prime Agent again. Check: `rlm.find_models("haiku")` lists `anthropic/claude-haiku-5-5`.

## Use

    await rlm.spawn("task", name="researcher", model="anthropic/claude-haiku-5-5", thinking="low")

## Notes
- Needs an Anthropic key with access to the model.
- Specs come from Anthropic's docs (models overview, pricing, launch post; Oct 2026): 1M context, 128K max output, adaptive thinking with effort levels.
- Cost in the catalog is the low tier (prompts up to 100K tokens): $0.10 in / $0.50 out per MTok, cache read $0.01, cache write $0.125. Prompts over 100K cost more ($0.50 / $2.50), so cost displays can under-report on long prompts.
- A catalog refresh can remove the entry. Re-run the installer (safe to repeat).
- Remove once Prime Agent ships the model officially. Backup: `provider-model-catalog.v1.json.bak`.
