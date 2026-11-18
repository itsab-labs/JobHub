"""
Datei: main.py

Status: Version 0.1 pre alpha :-)
"""

# packages from the python universe :-) ----------
# nothing yet

# own modules ------------------------------------------
from adzuna_api_call import search_jobs_adzuna
from errors import JobHubError
from translations import translate
from config import JOB_SEARCHED, COUNTRY, LOCATION, SALARY_MIN, DISTANCE_KM, FULL_TIME_ONLY, SORT_BY, MAX_DAYS_OLD, COMPANY, WHAT_EXCLUDE

# main ---------------------------------------------------
def main():
    try:
        jobs = search_jobs_adzuna()
    except JobHubError as error:
        text = translate(error.message_key, **error.values)
        raise SystemExit(
            f"{error.source}: {text} [{error.code}]"
        )

    print(translate("job_searched_criteria"))
    print(f"{translate("job_title_searched")} {JOB_SEARCHED} | {translate("country")} {COUNTRY} | {translate("town")} {LOCATION} | {translate("salary")}  {SALARY_MIN} ")
    print(f"{translate("distance_km")} {DISTANCE_KM} | {translate("salary_min")} {SALARY_MIN} | {translate("full_time_only")} {FULL_TIME_ONLY}")
    print(f"{translate("sort_by")} {SORT_BY} | {translate("max_days_old")} {MAX_DAYS_OLD} | {translate("company")} {COMPANY}")
    print(f"{translate("what_exclude")} {WHAT_EXCLUDE}")
    print()

    if not jobs:
        print(f"{translate("no_matching_jobs_found")}")
        return

    for job in jobs:
        print(f"{job['external_id']} | {job['title']}")
        print(f"{job['company']} | {job['location']}")
        print(job["url"])
        print()

        print()  # Leerzeile zwischen den Jobs

if __name__ == '__main__':
    main()