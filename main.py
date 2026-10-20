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
        raise SystemExit("Die Anfrage hat zu lange gedauert.") from None

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code
        print(f"HTTP-Fehler: {status}")

        try:
            error_data = error.response.json()
        except ValueError:
            error_data = None

        if isinstance(error_data, dict):
            description = error_data.get("display")
            string_documentation_adzuna = error_data.get("doc")

            if isinstance(description, str):
                #Zugangsdaten vor der Ausgabe entfernen.
                for name in ("ADZUNA_APP_ID", "ADZUNA_APP_KEY"):
                    secret = os.getenv(name)
                    if secret:
                        description = description.replace(secret, "[ENTFERNT]")

                print(f"Adzuna Fehlermeldung (Original): {description}")
                print(f"Documentation: {string_documentation_adzuna}")


        if status == 400:
            message = "Ungültige Suchparameter."
        elif status == 404:
            message = "Ressource nicht gefunden."
        elif status == 410:
            message = "Authorisierung fehlgeschlagen."
        elif status == 429:
            message = "API-Limit erreicht. Bitte später erneut versuchen."
        elif status >= 500:
            message = "Beim Anbieter ist ein Serverfehler aufgetreten."
        else:
            message = "Die API-Anfrage ist fehlgeschlagen."
        raise SystemExit(f"{message} (HTTP-Status: {status})") from None

    except requests.exceptions.RequestException:
        raise SystemExit(
            "Die Anfrage ist fehlgeschlagen oder die Antwort ist kein gültiges JSON."
        ) from None

    except ValueError as error:
        raise SystemExit(str(error)) from None

    print(f"Suche: {JOB_SEARCHED} | Land: {COUNTRY} | Stadt: {LOCATION} | Gehalt:  {SALARY_MIN} ")
    print(f"Abgerufen: {len(jobs)} Jobs\n")

    # for job in jobs:
    #     print(f"{job['id']} | {job['title']}")
    #     print(f"{job['company']} | {job['location']}")
    #     print(job["url"])
    #     print()

    for job in jobs:
        for key, value in job.items():
            print(f"{key}: {value}")

        print()  # Leerzeile zwischen den Jobs