#!/usr/bin/env python3
"""Add anthropic/claude-haiku-5-5 (specs from Anthropic docs, 2026-10-28) to the local Prime Agent model catalog. Safe to re-run."""
import copy, json, shutil, sys
from pathlib import Path

CATALOG = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / ".prime/agent/models/provider-model-catalog.v1.json"
NEW_ID = "claude-haiku-5-5"
NEW_ENTRY = {
    "id": "claude-haiku-5-5",
    "name": "Claude Haiku 5.5",
    "api": "anthropic-messages",
    "provider": "anthropic",
    "baseUrl": "https://api.anthropic.com",
    "reasoning": True,
    "thinkingLevelMap": {"minimal": None, "low": "low", "medium": "medium", "high": "high", "xhigh": "xhigh", "max": "max"},
    "input": ["text", "image"],
    "cost": {"input": 0.1, "output": 0.5, "cacheRead": 0.01, "cacheWrite": 0.125},
    "contextWindow": 1000000,
    "maxTokens": 128000,
}


def models(o):
    if isinstance(o, list):
        if any(isinstance(m, dict) and "id" in m for m in o):
            yield o
        for v in o:
            yield from models(v)
    elif isinstance(o, dict):
        for v in o.values():
            yield from models(v)


def is_anthropic(m, model_id):
    return m.get("id") == model_id and m.get("provider") == "anthropic"


data = json.loads(CATALOG.read_text())
for lst in models(data["payload"]):
    for i, m in enumerate(lst):
        if is_anthropic(m, NEW_ID):
            if m == NEW_ENTRY:
                print("already installed"); sys.exit(0)
            shutil.copy(CATALOG, CATALOG.with_suffix(".json.bak"))
            lst[i] = copy.deepcopy(NEW_ENTRY)
            CATALOG.write_text(json.dumps(data))
            print("updated entry. Restart the daemon: pkill -f 'prime-agent --mode daemon'")
            sys.exit(0)
for lst in models(data["payload"]):
    for i, m in enumerate(lst):
        if is_anthropic(m, "claude-sonnet-5-5"):
            shutil.copy(CATALOG, CATALOG.with_suffix(".json.bak"))
            lst.insert(i + 1, copy.deepcopy(NEW_ENTRY))
            CATALOG.write_text(json.dumps(data))
            print("installed. Restart the daemon: pkill -f 'prime-agent --mode daemon'")
            sys.exit(0)
sys.exit("could not find the anthropic model list; open Prime Agent once to download the catalog")
