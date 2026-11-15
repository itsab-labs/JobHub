"""
Datei: main.py

Status: Version 0.1 pre alpha :-)
"""

# packages from the python universe :-) ----------
import requests
import os
import sys

# own modules ------------------------------------------
from adzuna_api_call import search_jobs_adzuna
from config import *

# main ---------------------------------------------------
if __name__ == '__main__':
    try:
        jobs = search_jobs_adzuna()

    except requests.exceptions.Timeout:
        raise SystemExit("The request timed out.") from None

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code
        print(f"HTTP-Error: {status}", file=sys.stderr)

        try:
            error_data = error.response.json()
        except ValueError:
            error_data = None
            print("Response is not valid JSON.", file=sys.stderr)
            print(error.response.text[:1500], file=sys.stderr)

        if isinstance(error_data, dict):
            print("JSON keys:", list(error_data), file=sys.stderr)
            description = error_data.get("display")
            documentation = error_data.get("doc")
            exception = error_data.get("exception")
            print(f"display: {description!r}", file=sys.stderr)
            print(f"doc: {documentation!r}", file=sys.stderr)
            print(f"exception: {exception!r}", file=sys.stderr)

        if status == 400:
            message = "Incorrect parameters"
        elif status == 404:
            message = "Resource could not be found"
        elif status == 410:
            message = "Authorisation failed."
        elif status == 429:
            message = "API rate limit exceeded. Please try again later."
        elif status >= 500:
            message = "A server error occurred on the provider's side."
        else:
            message = "The API request failed."
        raise SystemExit(f"{message} (HTTP-Status: {status})") from None

    except requests.exceptions.RequestException:
        raise SystemExit(
            "The request failed or the response is not valid JSON."
        ) from None

    except ValueError as error:
        raise SystemExit(str(error)) from None

    print(f"Job searched:")
    print(f"{JOB_SEARCHED} | Country: {COUNTRY} | Town: {LOCATION} | Salary:  {SALARY_MIN} ")
    print(f"Distance (km): {DISTANCE_KM} | Salary_min: {SALARY_MIN} | Full time only: {FULL_TIME_ONLY}")
    print(f"Sort by: {SORT_BY} | Max days old: {MAX_DAYS_OLD} | Company: {COMPANY}")

    print()

    for job in jobs:
        if not jobs:
            print("No matching jobs found.")
            break
        print(f"{job['external_id']} | {job['title']}")
        print(f"{job['company']} | {job['location']}")
        print(job["url"])
        print()

        print()  # Leerzeile zwischen den Jobs