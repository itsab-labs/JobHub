from pathlib import Path

#general stuff
LANGUAGE = "de"
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = {"de", "en"}
LOCALES_DIR = Path(__file__).resolve().parent / "locales"

#default-values to be safe
DEFAULT_COUNTRY = "at"
SEARCH_DEFAULTS = {
    "country": DEFAULT_COUNTRY,
    "location": None,
    "distance": None,
    "salary_min": None,
    "full_time_only": False,
    "max_days_old": 30,
    "exclude": None,
}


#other stuff
SUPPORTED_COUNTRIES = ["at", "de", "fr", "es", "it", "gb", "us", "au", "be", "br", "ca", "ch", "in", "mx", "nl", "nz", "pl", "sg", "za"]

# adzuna --------------------
RESULTS_PER_PAGE = 3

VORLAGE_COMPACT_FULL = {
    "jobs": "DevOps",
    "country": "at",
    "location": "Wien",
    "distance": 20,
    "salary_min": 4000,
    "full_time_only": False,
    "max_days_old": 30,
    "exclude": "Java C# Softwareentwicklung",
}