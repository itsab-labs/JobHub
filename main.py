"""
Datei: main.py

Status: Version 0.1 pre alpha :-)

Leitlinien fürs Portfolio:
- Erst korrekt, dann wartbar, dann performant.
- Speichere Daten – berechne Statistiken.
- Wenn eine Funktion schwer zu testen ist, hat sie oft zu viele Aufgaben.
- Nicht vorsorglich aufteilen, sondern Funktionen dann aufteilen, wenn es unübersichtlich wird.

To Do:
- ersten API Aufruf meistern
"""

# packages from the python universe :-) ----------
import requests
import os

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
        print(f"HTTP-Error: {status}")

        try:
            error_data = error.response.json()
        except ValueError:
            error_data = None

        if isinstance(error_data, dict):
            description = error_data.get("display")
            string_documentation_adzuna = error_data.get("doc")

            if isinstance(description, str):
                for name in ("ADZUNA_APP_ID", "ADZUNA_APP_KEY"):
                    secret = os.getenv(name)
                    if secret:
                        description = description.replace(secret, "[REMOVED]")

                print(f"Adzuna Error Message (Original): {description}")
                print(f"Documentation: {string_documentation_adzuna}")

        if status == 400:
            message = "Invalid search parameters."
        elif status == 404:
            message = "Ressource not found."
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

    print(f"Job searched: {JOB_SEARCHED} | Country: {COUNTRY} | Town: {LOCATION} | Salary:  {SALARY_MIN} ")

    # for job in jobs:
    #     print(f"{job['id']} | {job['title']}")
    #     print(f"{job['company']} | {job['location']}")
    #     print(job["url"])
    #     print()

    for job in jobs:
        for key, value in job.items():
            print(f"{key}: {value}")

        print()  # Leerzeile zwischen den Jobs