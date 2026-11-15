"""
Datei: main.py

Status: Version 0.1 pre alpha :-)

Does: Adzuna API Calls
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

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
)


# .env neben dieser Python-Datei laden.
load_dotenv(Path(__file__).resolve().parent / ".env")

#-----------------------------------------
def search_jobs_adzuna():
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise ValueError("Adzuna credentials are missing from the .env-file.")

    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"

    # Diese Parameter senden wir immer.
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": JOB_SEARCHED,
        "results_per_page": RESULTS_PER_PAGE,
        "content-type": "application/json",
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
    if COMPANY is not None:
        params["company"] = COMPANY

    response = requests.get(
        url,
        params=params,
        headers={"Accept": "application/json"},
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise ValueError("The API response does not contain a valid list of jobs.")

    jobs = []

    for result in data["results"]:
        if not isinstance(result, dict):
            raise ValueError("A job needs to be in the dictionary format.")
        elif not result.get("id"):
            raise ValueError("A job must have a valid job ID.")

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
            raise ValueError(f"Required field '{key}' missing.")
        return None

    if not isinstance(value, str):
        raise ValueError(f"Field '{key}' needs to be a string.")

    value = value.strip()

    if not value:
        if required:
            raise ValueError(f"Required field '{key}' is empty.")
        return None

    return value

#-----------------------------------------
def get_object(data, key):
    value = data.get(key)

    if value is None:
        return {}

    if not isinstance(value, dict):
        raise ValueError(f"Field '{key}' needs to be in the dictionary format.")

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

    raise ValueError("Field 'salary_is_predicted' has to contain 0 or 1.")

#-----------------------------------------
def get_number(data, key):
    value = data.get(key)

    if value is None:
        return None

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Field '{key}' needs to be a number.")

    return value