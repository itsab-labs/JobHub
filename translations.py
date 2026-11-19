import json

from config import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, LOCALES_DIR, LANGUAGE
from functools import lru_cache

@lru_cache(maxsize=None)
def load_translations(lang):
    path = LOCALES_DIR / f"{lang}.json"

    with path.open(encoding="utf-8") as file:
        return json.load(file)

def translate(key, *, lang=LANGUAGE, **values):
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    text = load_translations(lang).get(key)

    if text is None or not text.strip():
        text = load_translations(DEFAULT_LANGUAGE).get(key)

    if text is None or not text.strip():
        return f"[{key}]"

    return text.format(**values)