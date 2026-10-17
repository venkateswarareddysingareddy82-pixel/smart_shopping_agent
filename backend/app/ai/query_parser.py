"""understand_user_query(): natural language (any supported language) -> structured shopping intent."""
import logging

from . import llm
from .language import has_keyword, longest_match, normalize_text, parse_numbers
from .lexicon import CAT_KW, FEAT_KW, INTENT_KW
from .prompts import CATEGORY_HINT, UNDERSTAND_SYSTEM

log = logging.getLogger("parser")
VALID_FEATS = set(FEAT_KW)
INTENTS = {"search", "compare", "explain", "which", "cheaper", "gift", "guide", "greet", "info"}


def _rule_parse(message: str, brands: list[str]) -> dict:
    t = normalize_text(message)
    best_cat, best_len = None, 0
    for slug, words in CAT_KW.items():
        n = longest_match(t, words)
        if n > best_len:
            best_cat, best_len = slug, n
    feats = [f for f, words in FEAT_KW.items() if any(has_keyword(t, w) for w in words)]
    maybe_cameras = best_cat is None and feats == ["camera"]  # bare "camera": a camera product unless context says otherwise
    nums = parse_numbers(message)
    found_brands = [b for b in brands if b and normalize_text(b) in t]

    def hit(key):
        return any(has_keyword(t, w) for w in INTENT_KW[key])

    if hit("guide"):
        intent = "guide"
    elif hit("gift"):
        intent = "gift"
    elif hit("compare"):
        intent = "compare"
    elif hit("explain"):
        intent = "explain"
    elif hit("cheaper"):
        intent = "cheaper"
    elif best_cat is None and hit("elder"):
        intent = "info"
    elif best_cat is None and hit("which"):
        intent = "which"
    elif best_cat is None and hit("greet") and len(t) < 30 and not feats and not nums["max_price"]:
        intent = "greet"
    else:
        intent = "search"
    return {"intent": intent, "category": best_cat, "max_price": nums["max_price"], "min_price": nums["min_price"],
            "brands": found_brands, "features": feats, "family_size": nums["family_size"],
            "use_case": ", ".join(feats), "elderly_question": hit("elder"), "maybe_cameras": maybe_cameras}


def understand_user_query(message: str, lang: str = "en", brands: list[str] | None = None,
                          categories: list[str] | None = None) -> dict:
    """Uses the LLM when an API key is configured; always falls back to the offline rule parser."""
    parsed = _rule_parse(message, brands or [])
    parsed["source"] = "rules"
    if llm.available():
        try:
            system = UNDERSTAND_SYSTEM.format(category_hint=CATEGORY_HINT.format(slugs=", ".join(categories or CAT_KW)))
            data = llm.complete_json(system, message)
            if data.get("intent") in INTENTS:
                parsed["intent"] = data["intent"]
            if data.get("category") in (categories or CAT_KW):
                parsed["category"] = data["category"]
            for key in ("max_price", "min_price", "family_size"):
                if isinstance(data.get(key), (int, float)) and data[key] > 0:
                    parsed[key] = int(data[key])
            feats = [f for f in data.get("features") or [] if f in VALID_FEATS]
            if feats:
                parsed["features"] = feats
            if data.get("brands"):
                parsed["brands"] = [b for b in data["brands"] if isinstance(b, str)][:3]
            if data.get("use_case"):
                parsed["use_case"] = str(data["use_case"])[:80]
            parsed["source"] = "ai"
        except llm.LLMUnavailable:
            parsed["ai_failed"] = True
    return parsed
