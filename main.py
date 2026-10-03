"""
Datei: main.py

Aufgabe: Steuert den Programmablauf.

Status: Version 0.1 pre alpha :-)

Leitlinien fürs Portfolio:
- Erst korrekt, dann wartbar, dann performant.
- Speichere Daten – berechne Statistiken.
- Wenn eine Funktion schwer zu testen ist, hat sie oft zu viele Aufgaben.
- Nicht vorsorglich aufteilen, sondern Funktionen dann aufteilen, wenn es unübersichtlich wird.

To Do:
Daten einlesen und erste fünf Zeilen ausgeben
"""

# packages from the python universe :-) ----------
from json import JSONDecodeError
import logging

# my own written moduls -------------
from logging_config import configure_logging


logger = logging.getLogger(__name__)

def main():
   pass

if __name__ == '__main__':
    configure_logging() #to be sure, there's only one handler, even if main is imported by another module
    main()