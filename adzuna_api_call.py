"""
Datei: adzuna_api_call.py

Status: Version 0.1 alpha :-)

Does: Adzuna API Calls

Offene ToDos:
- große funktion etwas entschlacken
"""
# packages from the python universe :-) ----------
import os
from pathlib import Path
import requests
from dotenv import load_dotenv
import sys

# own modules ------------------------------------------
from errors import JobHubError



from config import (
    JOB_SEARCHED,
    COUNTRY,
    RESULTS_PER_PAGE,
    LOCATION,
    DISTANCE_KM,
    SALARY_MIN,
    FULL_TIME_ONLY,
    SORT_BY,
    MAX_DAYS_OLD,
    COMPANY,
    WHAT_EXCLUDE,
)


# .env neben dieser Python-Datei laden.
load_dotenv(Path(__file__).resolve().parent / ".env")

#-----------------------------------------
def search_jobs_adzuna():
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise JobHubError(source="adzuna", code="missing_credentials")

    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": JOB_SEARCHED,
        "results_per_page": RESULTS_PER_PAGE
    }

    if LOCATION:
        params["where"] = LOCATION
        if DISTANCE_KM is not None:
            params["distance"] = DISTANCE_KM
    if SALARY_MIN is not None:
        params["salary_min"] = SALARY_MIN
    if FULL_TIME_ONLY:
        params["full_time"] = "1"
    if SORT_BY is not None:
        params["sort_by"] = SORT_BY
    if MAX_DAYS_OLD is not None:
        params["max_days_old"] = MAX_DAYS_OLD
    # auskommentiert, da company aktuell fehler wirft - selbst auf testseite von adzuna selbst
    # if COMPANY is not None:
    #     params["company"] = COMPANY
    if WHAT_EXCLUDE is not None:
        params["what_exclude"] = WHAT_EXCLUDE

    try:
        response = requests.get(
            url,
            params=params,
            headers={"Accept": "application/json"},
            timeout=10,
        )
        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise JobHubError(source="adzuna", code="timeout")

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code

        try:
            error_data = error.response.json()
        except ValueError:
            error_data = None
            print(error.response.text[:1500], file=sys.stderr)
            raise JobHubError(source="adzuna", code="adzuna_non_valid_json")

        if isinstance(error_data, dict):
            print("JSON keys:", list(error_data), file=sys.stderr)
            description = error_data.get("display")
            documentation = error_data.get("doc")
            exception = error_data.get("exception")
            print(f"display: {description!r}", file=sys.stderr)
            print(f"doc: {documentation!r}", file=sys.stderr)
            print(f"exception: {exception!r}", file=sys.stderr)

        raise JobHubError(source="adzuna", code=status)

    except requests.exceptions.RequestException:
        raise JobHubError(source="adzuna", code="request_failed_or_non_valid")

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise JobHubError(source="adzuna", code="adzuna_non_valid_json") from error

    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise JobHubError(source="adzuna", code="api_repsonse_not_valid_list_of_jobs")

    jobs = []

    for result in data["results"]:
        if not isinstance(result, dict):
            raise JobHubError(source="adzuna", code="dict_format_necessary")
        elif not result.get("id"):
            raise JobHubError(source="adzuna", code="valid_job_id_necessary")

        company = get_object(result, "company")
        location = get_object(result, "location")

        job = {
            "source": "adzuna",
            "external_id": get_text(result, "id", required=True),
            "title": get_text(result, "title", required=True),
            "url": get_text(result, "redirect_url", required=True),
            "company": get_text(company, "display_name"),
            "location": get_text(location, "display_name"),
            "contract_time": get_text(result, "contract_time"),
            "created_by_provider": get_text(result, "created"),
            "description_excerpt": get_text(result, "description"),
            "salary_min": get_number(result, "salary_min"),
            "salary_max": get_number(result, "salary_max"),
            "salary_is_predicted": get_prediction_flag(result),
        }

        jobs.append(job)

    return jobs

#-----------------------------------------
def get_text(data, key, *, required=False):
    value = data.get(key)

    if value is None:
        if required:
            raise JobHubError(source="adzuna", code="adzuna_required_field_missing", field=key)
        return None

    if not isinstance(value, str):
        raise JobHubError(source="adzuna", code="adzuna_field_not_string", field=key)

    value = value.strip()

    if not value:
        if required:
            raise JobHubError(source="adzuna", code="adzuna_required_field_is_empty", field=key)
        return None

    return value

#-----------------------------------------
def get_object(data, key):
    value = data.get(key)

    if value is None:
        return {}

    if not isinstance(value, dict):
        raise JobHubError(source="adzuna", code="adzuna_field_not_dictionary", field=key)

    return value

#-----------------------------------------
def get_prediction_flag(data):
    value = data.get("salary_is_predicted")

    if value is None:
        return None

    if isinstance(value, (str, int)) and not isinstance(value, bool):
        if value in ("0", 0):
            return False
        if value in ("1", 1):
            return True

    raise JobHubError(source="adzuna", code="adzuna_field_salary_is_predicted_not_boolean")

#-----------------------------------------
def get_number(data, key):
    value = data.get(key)

    if value is None:
        return None

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise JobHubError(source="adzuna", code="adzuna_field_not_number", field=key)

    return value