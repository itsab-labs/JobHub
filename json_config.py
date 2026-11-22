# json_config.py

import json

from config import DEFAULT_COUNTRY, SUPPORTED_COUNTRIES, SEARCH_DEFAULTS
from errors import JobHubError


def config_error(code, **values):
    # Spart es uns, bei jedem Fehler dieselbe Quelle anzugeben.
    return JobHubError(source="json_config", code=code, **values)


def validate_search_config(config):
    # Auch eine Liste oder null wäre gültiges JSON.
    # Für ein Suchprofil brauchen wir aber ein Objekt: {...}.
    if not isinstance(config, dict):
        raise config_error("json_config_not_object")

    # Unbekannte Felder melden. Sonst würde z. B. ein Tippfehler wie
    # "locaton" unbemerkt dazu führen, dass der Ortsfilter fehlt.
    allowed_fields = set(SEARCH_DEFAULTS) | {"jobs"}
    unknown_fields = sorted(config.keys() - allowed_fields)

    if unknown_fields:
        raise config_error(
            "json_config_unknown_fields",
            fields=", ".join(unknown_fields),
        )

    # Erst die Standards kopieren, dann die Werte aus der Datei
    # darüberlegen. Auch false, 0 und null werden dabei übernommen.
    settings = SEARCH_DEFAULTS.copy()
    settings.update(config)

    # jobs ist Pflicht. Fehlend und null sind hier beide ungültig.
    if settings.get("jobs") is None:
        raise config_error("json_config_missing_jobs")

    # jobs, location und exclude müssen Text sein, sofern sie gesetzt sind.
    # location und exclude dürfen None sein; jobs wurde oben schon geprüft.
    for field in ("jobs", "location", "exclude"):
        value = settings[field]

        if value is None:
            continue

        if not isinstance(value, str) or not value.strip():
            raise config_error("json_config_invalid_text", field=field)

        settings[field] = value.strip()

    # Beim Land bedeutet auch ein ausdrücklich gesetztes null:
    # Verwende das Standardland.
    if settings["country"] is None:
        settings["country"] = DEFAULT_COUNTRY

    country = settings["country"]
    if not isinstance(country, str) or country not in SUPPORTED_COUNTRIES:
        raise config_error(
            "json_config_invalid_country",
            country=country,
            allowed=", ".join(SUPPORTED_COUNTRIES),
        )

    # Zahlenfilter sind entweder null (= kein Filter) oder ganze Zahlen ab 0.
    # type(value) is int schließt true und false ausdrücklich aus:
    # isinstance(value, int) würde boolesche Werte in Python mit akzeptieren.
    for field in ("distance", "salary_min", "max_days_old"):
        value = settings[field]

        if value is not None and (type(value) is not int or value < 0):
            raise config_error("json_config_invalid_integer", field=field)

    # Nur echtes JSON-true oder -false ist erlaubt. "false" ist ein String.
    if not isinstance(settings["full_time_only"], bool):
        raise config_error("json_config_invalid_boolean", field="full_time_only")

    # Auch 0 zählt als angegebene Entfernung und braucht deshalb einen Ort.
    if settings["distance"] is not None and settings["location"] is None:
        raise config_error("json_config_missing_location")

    return settings


def load_search_config(path):
    # argparse liefert für --load_config_file bereits ein Path-Objekt.
    try:
        with path.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except (OSError, UnicodeDecodeError) as error:
        raise config_error(
            "json_config_read_failed", filename=str(path)
        ) from error
    except json.JSONDecodeError as error:
        raise config_error(
            "json_config_non_valid_json",
            filename=str(path),
            line=error.lineno,
            column=error.colno,
        ) from error

    # Erst wenn die Datei lesbar und syntaktisch gültig ist,
    # prüfen wir, ob ihr Inhalt eine brauchbare Suchkonfiguration ist.
    return validate_search_config(config)