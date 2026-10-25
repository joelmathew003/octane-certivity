"""Structured-output calls to Claude (one turn, or a tool loop), with usage and cost bookkeeping."""

from __future__ import annotations

import json
import os
import threading
from collections import Counter
from collections.abc import Callable
from pathlib import Path

import anthropic
# the SDK streams over httpx2: a connection dropped mid-stream surfaces as its TransportError, not as an APIError
from httpx2 import TransportError

REPO_ROOT = Path(__file__).resolve().parents[2]
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


def load_env(path: Path = REPO_ROOT / ".env") -> None:
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

import time


def _send(system: str, messages: list[dict], schema: dict, effort: str, tools: list[dict] | None = None, retries: int = 4):
    """One streamed request whose final answer must match `schema`; its usage is added to the totals."""
    last_err = None
    for attempt in range(retries):
        try:
            with client().beta.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system,
                messages=messages,
                output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
                **({"tools": tools} if tools else {}),
            ) as stream:
                response = stream.get_final_message()
            break
        except (anthropic.APIConnectionError, anthropic.RateLimitError, anthropic.InternalServerError, TransportError) as exc:
            last_err = exc
            if attempt == retries - 1:
                raise
            time.sleep(2 * (attempt + 1))
    else:
        raise last_err or RuntimeError("Failed to get response after retries")

    with _usage_lock:
        for key in PRICE_PER_MILLION:
            usage[key] += getattr(response.usage, key, 0) or 0
    if response.stop_reason == "refusal":
        raise RuntimeError(f"request declined: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError(f"output hit max_tokens={MAX_TOKENS}; the JSON is incomplete")
    return response


def _answer(response) -> dict:
    return json.loads(next(block.text for block in response.content if block.type == "text"))


def ask_json(system: str, content: list[dict], schema: dict, *, effort: str = "high") -> dict:
    """Send one user turn and return the JSON object the model writes, validated by the API against `schema`."""
    return _answer(_send(system, [{"role": "user", "content": content}], schema, effort))


def ask_json_with_tools(system: str, content: list[dict], schema: dict, tools: list[dict],
                        call_tool: Callable[[str, dict], str], *, effort: str = "high", max_turns: int = 8,
                        last_turn_note: str | None = None) -> dict:
    """ask_json, but the model may first call client tools: call_tool(name, input) runs one and returns its text.

    The results go back in the next turn until the model answers. With last_turn_note, that text joins the tool
    results before the last allowed turn, so the model answers instead of running out of turns.
    """
    messages = [{"role": "user", "content": content}]
    for turn in range(1, max_turns + 1):
        response = _send(system, messages, schema, effort, tools)
        if response.stop_reason != "tool_use":
            return _answer(response)
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            try:
                output, failed = call_tool(block.name, block.input), False
            except Exception as error:  # reported to the model, which can recover
                output, failed = f"Error: {error}", True
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": output, "is_error": failed})
        if last_turn_note and turn == max_turns - 1:
            results.append({"type": "text", "text": last_turn_note})
        messages += [{"role": "assistant", "content": response.content}, {"role": "user", "content": results}]
    raise RuntimeError(f"no answer after {max_turns} turns")


def cost_dollars() -> float:
    return sum(usage[key] * price / 1_000_000 for key, price in PRICE_PER_MILLION.items())
