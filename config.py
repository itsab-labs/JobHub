from pathlib import Path

#general stuff
LANGUAGE = "de"
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = {"de", "en"}
LOCALES_DIR = Path(__file__).resolve().parent / "locales"

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