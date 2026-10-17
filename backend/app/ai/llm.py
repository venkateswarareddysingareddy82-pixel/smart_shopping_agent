"""Thin, replaceable LLM client (Anthropic or any OpenAI-compatible API) using plain HTTP."""
import json
import logging

import httpx

from ..config import settings

log = logging.getLogger("llm")


class LLMUnavailable(Exception):
    pass


def available() -> bool:
    return settings.ai_enabled


def complete(system: str, messages: list[dict], max_tokens: int = 700, temperature: float = 0.3) -> str:
    """messages: [{"role": "user"|"assistant", "content": str}]. Raises LLMUnavailable on any problem."""
    if not settings.ai_enabled:
        raise LLMUnavailable("AI_API_KEY not set")
    try:
        with httpx.Client(timeout=settings.AI_TIMEOUT) as client:
            if settings.AI_PROVIDER == "openai":
                base = (settings.AI_BASE_URL or "https://api.openai.com/v1").rstrip("/")
                r = client.post(f"{base}/chat/completions",
                                headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
                                json={"model": settings.AI_MODEL, "max_tokens": max_tokens, "temperature": temperature,
                                      "messages": [{"role": "system", "content": system}, *messages]})
                r.raise_for_status()
                return r.json()["choices"][0]["message"]["content"].strip()
            base = (settings.AI_BASE_URL or "https://api.anthropic.com").rstrip("/")
            r = client.post(f"{base}/v1/messages",
                            headers={"x-api-key": settings.AI_API_KEY, "anthropic-version": "2023-06-01",
                                     "content-type": "application/json"},
                            json={"model": settings.AI_MODEL, "max_tokens": max_tokens, "temperature": temperature,
                                  "system": system, "messages": messages})
            r.raise_for_status()
            return "".join(b.get("text", "") for b in r.json().get("content", []) if b.get("type") == "text").strip()
    except Exception as exc:  # network, auth, quota, parsing...
        log.warning("LLM call failed: %s", exc)
        raise LLMUnavailable(str(exc)) from exc


def complete_json(system: str, user: str, max_tokens: int = 400) -> dict:
    text = complete(system, [{"role": "user", "content": user}], max_tokens=max_tokens, temperature=0)
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(text[text.index("{"): text.rindex("}") + 1])
    except Exception as exc:
        raise LLMUnavailable(f"bad JSON from model: {exc}") from exc
