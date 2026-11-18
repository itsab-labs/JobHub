import json

from config import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, LOCALES_DIR, LANGUAGE

def load_translations(lang):
    path = LOCALES_DIR / f"{lang}.json"

    with path.open(encoding="utf-8") as file:
        return json.load(file)

def translate(key, *, lang=LANGUAGE, **values):
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    # Zuerst in der gewünschten Sprache suchen.
    text = load_translations(lang).get(key)

    # Fehlende oder leere Übersetzung: Deutsch versuchen.
    if text is None or not text.strip():
        text = load_translations(DEFAULT_LANGUAGE).get(key)

    # Auch auf Deutsch nicht vorhanden: Schlüssel sichtbar machen.
    if text is None or not text.strip():
        return f"[{key}]"

    # Eventuelle Platzhalter mit übergebenen Werten befüllen.
    return text.format(**values)