# adzuna --------------------

JOB_SEARCHED = "DevOps"
COUNTRY = "at" # ISO 8601 country code of the country of interest
RESULTS_PER_PAGE = 5

# Optionale Suchfilter
# https://developer.adzuna.com/activedocs#/default/search
LOCATION = "Wien"       # None = ganz Österreich
DISTANCE_KM = 20        # Umkreis; nur zusammen mit LOCATION
SALARY_MIN = None      # Zum Beispiel 40000
FULL_TIME_ONLY = True  # True = nur Vollzeit; False = kein Filter
SORT_BY = None # bspw. salary
DISTANCE = None # default: 5 km
MAX_DAYS_OLD = None # non default set
COMPANY = None # This may be returned in a Adzuna::API::Response::Company object when a job is returned.