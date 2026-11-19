from pathlib import Path

#general stuff
LANGUAGE = "de"
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = {"de", "en"}
LOCALES_DIR = Path(__file__).resolve().parent / "locales"

# adzuna --------------------
JOB_SEARCHED = "DevOps"
COUNTRY = "at" #possible countries: gb, us, at, au, be, br, ca, ch, de, es, fr, in, it, mx, nl, nz, pl, sg, za
RESULTS_PER_PAGE = 3

# Optionale Suchfilter
# https://developer.adzuna.com/activedocs#/default/search
LOCATION = "Wien"       # None = ganz Österreich
DISTANCE_KM = None        # Umkreis; nur zusammen mit LOCATION
SALARY_MIN = None      # Zum Beispiel 40000
FULL_TIME_ONLY = True  # True = nur Vollzeit; False = kein Filter
SORT_BY = None # bspw. salary
MAX_DAYS_OLD = None # non default set
COMPANY = None #Mit company="BRZ" liefert Adzuna HTTP 400 und eine allgemeine HTML-Fehlerseite. Ursache ungeklärt. Funktioniert aber nicht mal auf der Testseite von Adzuna selbst (https://developer.adzuna.com/activedocs#/default/search)
WHAT_EXCLUDE = "Java C# Scrum"