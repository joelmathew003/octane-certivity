"""One structured-output call to Claude, with usage and cost bookkeeping."""

from __future__ import annotations

import json
import os
import threading
from collections import Counter
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
MODEL = "claude-opus-5-5"
MAX_TOKENS = 64000
# claude-opus-5-5, dollars per million tokens; 5-minute cache writes are 1.25x input
PRICE_PER_MILLION = {
    "input_tokens": 4.00,
    "output_tokens": 20.00,
    "cache_read_input_tokens": 0.20,
    "cache_creation_input_tokens": 5.00,
}

usage: Counter[str] = Counter()
_usage_lock = threading.Lock()
_client: anthropic.Anthropic | None = None


def load_env(path: Path = ROOT / ".env") -> None:
    """KEY=VALUE lines from .env, without overriding variables that are already set."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and not key.startswith("#") and value.strip() and key.strip() not in os.environ:
            os.environ[key.strip()] = value.strip().strip("\"'")


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        load_env()
        _client = anthropic.Anthropic()
    return _client


def ask_json(system: str, content: list[dict], schema: dict, *, effort: str = "high") -> dict:
    """Send one user turn and return the JSON object the model writes, validated by the API against `schema`."""
    with client().beta.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": content}],
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        response = stream.get_final_message()
    with _usage_lock:
        for key in PRICE_PER_MILLION:
            usage[key] += getattr(response.usage, key, 0) or 0
    if response.stop_reason == "refusal":
        raise RuntimeError(f"request declined: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError(f"output hit max_tokens={MAX_TOKENS}; the JSON is incomplete")
    text = next(block.text for block in response.content if block.type == "text")
    return json.loads(text)


def cost_dollars() -> float:
    return sum(usage[key] * price / 1_000_000 for key, price in PRICE_PER_MILLION.items())
