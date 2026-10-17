"""Language registry + text helpers (number parsing, normalisation)."""
import re
import unicodedata

from .lexicon import ABOVE_KW, EN_NUMBERS, FAMILY_WORDS, MULTIPLIERS

LANGUAGES = {
    "en": {"name": "English", "native": "English", "speech": "en-IN"},
    "te": {"name": "Telugu", "native": "తెలుగు", "speech": "te-IN"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "speech": "hi-IN"},
    "ta": {"name": "Tamil", "native": "தமிழ்", "speech": "ta-IN"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "speech": "kn-IN"},
    "ml": {"name": "Malayalam", "native": "മലയാളം", "speech": "ml-IN"},
    "bn": {"name": "Bengali", "native": "বাংলা", "speech": "bn-IN"},
    "mr": {"name": "Marathi", "native": "मराठी", "speech": "mr-IN"},
}


def normalize_lang(code: str | None) -> str:
    code = (code or "en").lower().split("-")[0]
    return code if code in LANGUAGES else "en"


def normalize_text(text: str) -> str:
    """Lower-case, convert any Unicode digits to ASCII, drop zero-width joiners."""
    out = []
    for ch in unicodedata.normalize("NFC", text or ""):
        if ch in "\u200c\u200d\u200b":
            continue
        if ch.isdecimal() and not ch.isascii():
            out.append(str(unicodedata.digit(ch)))
        else:
            out.append(ch)
    return "".join(out).lower()


def has_keyword(text: str, kw: str) -> bool:
    kw = normalize_text(kw)
    if kw.isascii() and kw.strip().replace(" ", "").replace("'", "").replace("-", "").isalnum():
        return re.search(r"(?<![a-z0-9])" + re.escape(kw.strip()) + r"(?:s|es)?(?![a-z0-9])", text) is not None
    return kw in text


def longest_match(text: str, words: list[str]) -> int:
    best = 0
    for w in words:
        if has_keyword(text, w):
            best = max(best, len(normalize_text(w).strip()))
    return best


_mult_alt = "|".join(sorted((re.escape(normalize_text(k)) for k in MULTIPLIERS), key=len, reverse=True))
_NUM_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(" + _mult_alt + r")?(?![a-z])")
_FAM_AFTER = re.compile(r"(\d+)\s*(?:" + "|".join(re.escape(normalize_text(w)) for w in FAMILY_WORDS if w != "family of") + ")")
_FAM_OF = re.compile(r"family of (\d+|" + "|".join(EN_NUMBERS) + ")")


def parse_numbers(text: str) -> dict:
    """Extract budget and family size from a message. Works with 20k, 20 వేల, 2 lakh, ₹15,000 ..."""
    t = normalize_text(text)
    result = {"max_price": None, "min_price": None, "family_size": None}
    fam = _FAM_AFTER.search(t) or _FAM_OF.search(t)
    if fam:
        g = fam.group(1)
        result["family_size"] = int(g) if g.isdigit() else EN_NUMBERS.get(g)
    spans_used = [fam.span()] if fam else []
    amounts = []
    for m in _NUM_RE.finditer(t):
        if any(a <= m.start() < b for a, b in spans_used):
            continue
        value = float(m.group(1).replace(",", ""))
        mult = MULTIPLIERS.get(m.group(2) or "", 1) if m.group(2) else 1
        value *= mult
        if value >= 500:  # smaller numbers are quantities / sizes, not budgets
            amounts.append(int(value))
    if amounts:
        above = any(normalize_text(w) in t for w in ABOVE_KW)
        if above:
            result["min_price"] = amounts[0]
        else:
            result["max_price"] = amounts[0]
    return result
