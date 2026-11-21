"""
Datei: main.py

Status: Version 0.1 pre alpha :-)
"""

# packages from the python universe :-) ----------
import argparse
from pathlib import Path

# own modules ------------------------------------------
from adzuna_api_call import search_jobs_adzuna
from errors import JobHubError
from translations import translate
#from config import JOB_SEARCHED, COUNTRY, LOCATION, SALARY_MIN, DISTANCE_KM, FULL_TIME_ONLY, SORT_BY, MAX_DAYS_OLD, COMPANY, WHAT_EXCLUDE
import my_parser

# main ---------------------------------------------------
def main():
    args = my_parser.parse_options()
    print(args)

    try:
        jobs = search_jobs_adzuna(
            args
        )
    except JobHubError as error:
        text = translate(error.message_key, **error.values)
        raise SystemExit(
            f"{error.source}: {text} [{error.code}]"
        )

    print(translate("job_searched_criteria"))
    print(f"{translate("job_title_searched")} {args.jobs} | {translate("country")} {args.country} | {translate("town")} {args.location}")
    print(f"{translate("distance_km")} {args.distance} | {translate("salary_min")} {args.salary_min} | {translate("full_time_only")} {args.full_time_only}")
    print(f"{translate("max_days_old")} {args.max_days_old} | {translate("what_exclude")} {args.exclude}")
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