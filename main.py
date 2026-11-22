"""
Datei: main.py

Status: Version 0.1 pre alpha :-)
"""
import json
# packages from the python universe :-) ----------
from pathlib import Path
from argparse import Namespace

# own modules ------------------------------------------
from adzuna_api_call import search_jobs_adzuna
from errors import JobHubError
from translations import translate
import my_parser
from config import VORLAGE_COMPACT_FULL, DEFAULT_COUNTRY, SUPPORTED_COUNTRIES, SEARCH_DEFAULTS
from json_config import load_search_config

# main ---------------------------------------------------
def main():
    args = my_parser.parse_options()
    print(f"arguments delivered: {args}\n")

    if args.create_job_template is not None:
        filename = args.filename or Path("template_generated.json")
        write_template(args.create_job_template, filename)
        return

    try:
        if args.load_config_file is not None:
            config = load_search_config(args.load_config_file)
            args = Namespace(**config)

        jobs = search_jobs_adzuna(args)

    except JobHubError as error:
        text = translate(error.message_key, **error.values)
        raise SystemExit(f"{error.source}: {text} [{error.code}]")

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


def write_template(template_type: str, filename: Path):
    if template_type == "compact_full":
        with filename.open("x", encoding="utf-8") as file:
            json.dump(VORLAGE_COMPACT_FULL, file, indent=4, ensure_ascii=False)

# muss IMMER ganz am Ende stehen - sonst erkennt python die ganzen anderen funktionen nicht
if __name__ == '__main__':
    main()