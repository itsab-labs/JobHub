# JobHub – Roadmap bis Version 0.1

Stand: 30. September 2026  
Projekt: Aus MovieHub wird JobHub.  
Zweck: Nicht-kommerzielles Portfolio-Projekt und persönliches Helferlein für die Jobsuche, später schrittweise erweiterbar.

## 1. Ziel und Rahmen

**Version 0.1 kann eine echte Job-API abfragen, Stellenanzeigen in PostgreSQL speichern, neue von bereits bekannten Anzeigen unterscheiden und die Ergebnisse mit Flask im Browser anzeigen.**

Der Start bleibt klein: eine Datenquelle, ein lokaler Nutzer, manuell gestartete Imports. Suchbegriff und Ort sind frei wählbar. Die Anwendung soll früh nutzbar werden und gleichzeitig Python, SQL, APIs, Tests und einen nachvollziehbaren Datenfluss demonstrieren.

Annahmen:

- Python kann auf deinem Entwicklungsrechner installiert und verwendet werden.
- PostgreSQL ist lokal verfügbar oder wird vor MS3 eingerichtet. Dafür sind gegebenenfalls Installationsrechte nötig; die Einschränkungen deines Arbeitsrechners werden hier nicht als Entwicklungsumgebung vorausgesetzt.
- Zugang, Datenfelder, Limits sowie zulässige Speicherung und Darstellung der ersten API sind noch zu prüfen. Jooble und Adzuna sind Kandidaten, keine bereits zugesagten Integrationen.
- Die genannten Projektbefehle und Funktionen sind Zielbeispiele. Dieses Dokument ist ein Umsetzungsplan, keine bereits lauffähige Anwendung.

### Was „neu“ hier bedeutet

| Begriff | Bedeutung in Version 0.1 |
|---|---|
| Neu | Die Kombination aus Quelle und externer Job-ID war vor diesem Import noch nicht gespeichert. |
| Bekannt | Dieselbe Kombination wurde früher bereits gespeichert. |
| Neue Jobs des letzten erfolgreichen Imports | Jobs, deren erster Import diesem Durchlauf entspricht. Diese Liste bleibt bis zum nächsten erfolgreichen Import nachvollziehbar. |
| Noch nicht angesehen | Späterer persönlicher Nutzerstatus; wird in Version 0.1 noch nicht erfasst. |
| Gleiche Stelle aus zwei Quellen | In Version 0.1 möglicherweise zwei Datensätze; quellübergreifende Deduplizierung folgt später. |

Eine bereits bekannte Anzeige kann geändert worden sein. „Bekannt“ bedeutet deshalb nicht „unverändert“. Auch ist `first_seen_at` dein erster Fundzeitpunkt, nicht das Veröffentlichungsdatum.

## 2. Meilensteine im Überblick

| Meilenstein | Greifbares Ergebnis |
|---|---|
| MS0 – Grundgerüst | Projekt, Konfiguration und Testaufruf stehen. |
| MS1 – Erste API | Dein Python-Code lädt echte Stellenanzeigen herunter. |
| MS2 – Normalisierung | API-Antworten werden in ein kleines internes Job-Format übersetzt. |
| MS3 – PostgreSQL | Jobs werden dauerhaft gespeichert; Wiederholungen erzeugen keine zusätzlichen Zeilen. |
| MS4 – Import-Workflow | Ein CLI-Aufruf verbindet API, Normalisierung, Datenbank und Importstatistik. |
| MS5 – Flask | Du siehst gespeicherte Jobs und neue Treffer im Browser. |
| MS6 – Version 0.1 abschließen | Ablauf, einfache Filter, Tests und Dokumentation sind reproduzierbar. |

Arbeite die Meilensteine nacheinander ab. Tests gehören zum jeweiligen Meilenstein, nicht in eine separate Schlussphase. Flask passt direkt nach dem funktionierenden Import; für einen früheren sichtbaren Erfolg darf nach MS3 bereits eine einfache Jobliste entstehen.

## 3. MS0 – JobHub vorbereiten

**Ziel:** Eine kleine, verständliche Grundlage schaffen, ohne bereits alle späteren Schichten auszubauen.

### ToDos

- [X] MovieHub-Code sichern, etwa durch einen Git-Tag oder einen separaten Branch. Verwendbare Hilfsfunktionen wie Logging gezielt übernehmen.
- [X] JobHub als neues Projekt oder klar getrennten Projektbereich anlegen; eine Repository-Umbenennung ist keine Voraussetzung für den ersten API-Call.
- [X] Virtuelle Python-Umgebung einrichten.
- [X] Anfangs `requests`, `python-dotenv` und `pytest` installieren; `psycopg` und Flask erst bei ihrem Meilenstein ergänzen.
- [X] Abhängigkeiten in `requirements.txt` dokumentieren.
- [X] `.gitignore` für `.env`, virtuelle Umgebung, Cache-Dateien und lokale Logs anlegen.
- [X] `.env.example` mit Platzhaltern erstellen.
- [X] README mit Zweck, Startumfang und Entwicklungsstart anlegen.
- [X] `pytest` ausführen können; einen ersten fachlichen Test mit MS1 hinzufügen.

### Mögliche Struktur

| Pfad | Aufgabe |
|---|---|
| `jobhub/__init__.py` | Python-Paket, später Flask-App-Factory |
| `jobhub/config.py` | Konfiguration prüfen und bereitstellen |
| `jobhub/api_client.py` | Erste API abrufen |
| `jobhub/models.py` | Internes Job-Format |
| `jobhub/normalizer.py` | Antwortfelder übersetzen und prüfen |
| `jobhub/database.py` | SQL-Abfragen und Verbindungen |
| `jobhub/importer.py` | Importablauf koordinieren |
| `jobhub/__main__.py` | CLI-Einstieg |
| `jobhub/web.py`, `jobhub/templates/` | Später Flask-Routen und HTML |
| `sql/001_initial.sql` | Erstes Datenbankschema |
| `tests/`, `tests/fixtures/` | Tests und synthetische API-Antworten |

Lege Dateien erst an, wenn sie eine Aufgabe erhalten. Für den ersten API-Call reichen wenige Module; die Tabelle beschreibt die spätere V0.1-Struktur.

Beispiel `.env.example`:

```dotenv
JOB_API_KEY=replace_me
DATABASE_URL=postgresql://jobhub:replace_me@localhost:5432/jobhub
TEST_DATABASE_URL=postgresql://jobhub_test:replace_me@localhost:5432/jobhub_test
```

Variablennamen und Authentifizierung werden an die ausgewählte API angepasst. Echte Zugangsdaten gehören ausschließlich in die lokale Konfiguration.

### Definition of Done

- [X] Projektzweck und nächster Schritt sind im README verständlich.
- [X] Die virtuelle Umgebung funktioniert und Abhängigkeiten sind dokumentiert.
- [X] Konfigurationsbeispiele enthalten keine echten Zugangsdaten.
- [X] Alte MovieHub-Funktionen müssen nicht gestartet werden, um an JobHub zu arbeiten.

## 4. MS1 – Erste echte Jobs per API herunterladen

**Ziel:** Ein echter Suchaufruf liefert Jobs im Terminal. Noch keine Datenbank und keine Webseite nötig.

### ToDos

- [X] Genau einen Anbieter auswählen: Zugang, Verfügbarkeit für Österreich/Deutschland, Job-ID, Suchparameter und Beispielantwort prüfen.
- [ ] Limits sowie Vorgaben für Speicherung, Anzeige und Quellenverlinkung in der offiziellen Dokumentation prüfen und knapp festhalten.
- [X] Registrierung beziehungsweise API-Zugang abschließen, sofern erforderlich.
- [X] Einen manuellen Testaufruf mit einem kleinen Suchumfang ausführen.
- [X] API-Client mit explizitem Timeout implementieren.
- [X] Fehlenden API-Key vor dem Request mit einer verständlichen Meldung erkennen.
- [X] HTTP-Fehler, Timeout und ungültiges JSON als nachvollziehbare Fehler behandeln.
- [ ] Falls vorhanden: Pagination verstehen, erste Seitenbegrenzung bewusst festlegen und dokumentieren.
- [ ] Nur relevante Ergebnisfelder im Terminal ausgeben; keine Schlüssel, Header oder unbereinigten Request-URLs loggen.

### Zielbeispiel

```python
response = client.search_jobs(query="DevOps", location="Wien", max_pages=1)
```

```text
Suche: DevOps · Wien
Abgerufen: 12 Anzeigen aus 1 Seite

Platform Engineer
Beispiel GmbH · Wien
https://example.org/jobs/123
```

Die Zahl „abgerufen“ ist nicht automatisch die Gesamtzahl der verfügbaren Treffer. Begrenzte Seiten und Suchparameter beschränken deine Datengrundlage.

### Tests

- [ ] Erfolgreiche Mock-Antwort liefert die erwarteten Ergebnisse.
- [ ] Leere Trefferliste liefert eine leere Liste statt eines Fehlers.
- [ ] HTTP 410 wird als Zugangsfehler verständlich gemeldet.
- [ ] HTTP 429 meldet ein Rate Limit; keine endlosen Wiederholungen.
- [ ] HTTP 500 und Timeout führen zu einem kontrollierten Fehler.
- [ ] Ungültiges JSON beziehungsweise unerwartete Antwortstruktur wird erkannt.
- [ ] Falls verwendet: Zweite Seite wird korrekt angefordert, Seitenlimit wird eingehalten.

**Teststrategie:** HTTP-Aufrufe in automatisierten Tests mocken, zum Beispiel mit `unittest.mock` oder pytest-`monkeypatch`. Der echte API-Call ist ein separater manueller Funktionstest und kein notwendiger Bestandteil jedes Testlaufs.

### Definition of Done

- [ ] Ein dokumentierter Aufruf lädt echte Jobs herunter und zeigt Titel sowie Original-Link.
- [ ] Die relevanten Fehlerfälle sind automatisiert getestet.
- [ ] Tests benötigen keinen API-Key und erreichen keine echte Job-API.
- [ ] Es ist bekannt, welche gelieferten Inhalte JobHub speichern und darstellen darf.

## 5. MS2 – Einfaches internes Job-Format

**Ziel:** Datenbank und Oberfläche arbeiten mit deinen Feldnamen, unabhängig vom Antwortformat des Anbieters.

### ToDos

- [ ] Kleines Modell definieren, beispielsweise als Python-`dataclass`.
- [ ] Normalizer für die erste Quelle schreiben.
- [ ] Externe IDs in einen konsistenten Texttyp überführen; keine Annahme, dass sie immer Zahlen sind.
- [ ] Pflichtfelder und optionale Felder festlegen.
- [ ] Fehlende optionale Angaben als `None` behandeln.
- [ ] Veröffentlichungsdatum nur übernehmen, wenn es verlässlich interpretiert werden kann; fehlende Zeitzonen nicht stillschweigend erraten.
- [ ] Synthetische Antwortbeispiele als Test-Fixtures speichern.

### Beispielmodell

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Job:
    source: str
    external_id: str
    title: str
    url: str
    company: str | None = None
    location_text: str | None = None
    salary_raw: str | None = None
    published_at: datetime | None = None
```

Beispiel einer **fiktiven** API-Antwort, nicht das zugesagte Schema eines konkreten Anbieters:

```json
{
  "id": 123,
  "job_title": "Platform Engineer",
  "employer": "Beispiel GmbH",
  "location": "Wien / Hybrid",
  "link": "https://example.org/jobs/123"
}
```

Daraus wird:

```python
Job(
    source="example_api",
    external_id="123",
    title="Platform Engineer",
    company="Beispiel GmbH",
    location_text="Wien / Hybrid",
    url="https://example.org/jobs/123",
    salary_raw=None,
)
```

### Tests

- [ ] Felder werden korrekt zugeordnet.
- [ ] Fehlendes Gehalt oder fehlende Firma verursacht keinen Absturz.
- [ ] Fehlende beziehungsweise leere Pflichtfelder werden erkannt.
- [ ] Job-Link ist eine zulässige HTTP-/HTTPS-URL.
- [ ] Dokumentierte Datumsformate werden korrekt verarbeitet.

Für V0.1 darf ein ungültiger Pflichtdatensatz den Import mit einer konkreten Fehlermeldung abbrechen. Einzelne fehlerhafte Anzeigen zu überspringen und gesondert zu zählen ist eine spätere Erweiterung. Wähle zunächst einen klaren, getesteten Ablauf.

**Noch nicht nötig:** Geocoding, Gehaltsextraktion, Skill-Erkennung oder eine vollständige Rohdatenhistorie. Gespeicherte API-Rohdaten können später bei erneuter Normalisierung helfen, sofern die Bedingungen des Anbieters das erlauben.

### Definition of Done

- [ ] Repräsentative Antworten werden zuverlässig in `Job`-Objekte übersetzt.
- [ ] Optionale und ungültige Felder sind getestet.
- [ ] Der restliche Anwendungscode benötigt keine anbieterspezifischen JSON-Feldnamen.

## 6. MS3 – PostgreSQL und „neu oder bekannt?“

**Ziel:** Zwei kleine Tabellen reichen für dauerhafte Jobs und nachvollziehbare Imports. Direkte SQL-Abfragen mit `psycopg` passen zum SQL-Lernziel; ein ORM ist zunächst optional.

### ToDos

- [ ] PostgreSQL auf dem Entwicklungsrechner bereitstellen.
- [ ] Datenbank `jobhub` und passenden Datenbanknutzer einrichten.
- [ ] Separate Testdatenbank einrichten; Tests dürfen Entwicklungsdaten nicht löschen.
- [ ] `psycopg` installieren und eine Verbindung testen.
- [ ] Schema in einer SQL-Datei ablegen und dokumentieren, wie es eingerichtet wird.
- [ ] Jobs anhand `(source, external_id)` eindeutig machen.
- [ ] Neue Datensätze einfügen; bekannte Datensätze aktualisieren.
- [ ] `first_seen_at` und `first_seen_run_id` bei Aktualisierungen unverändert lassen.
- [ ] `last_seen_at` bei erneutem Fund aktualisieren.
- [ ] Transaktionen verwenden und SQL-Werte über Parameter übergeben.

### Beispiel für ein kleines Schema

```sql
CREATE TABLE import_runs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source TEXT NOT NULL,
    query TEXT NOT NULL,
    location_query TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMPTZ,
    fetched_jobs INTEGER NOT NULL DEFAULT 0,
    unique_jobs INTEGER NOT NULL DEFAULT 0,
    new_jobs INTEGER NOT NULL DEFAULT 0,
    known_jobs INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('running', 'succeeded', 'failed')),
    error_message TEXT
);

CREATE TABLE jobs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source TEXT NOT NULL,
    external_id TEXT NOT NULL,
    title TEXT NOT NULL,
    company TEXT,
    location_text TEXT,
    url TEXT NOT NULL,
    salary_raw TEXT,
    published_at TIMESTAMPTZ,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_seen_run_id BIGINT NOT NULL REFERENCES import_runs(id),
    UNIQUE (source, external_id)
);
```

`first_seen_run_id` verbindet einen Job mit dem Import, bei dem er erstmals gespeichert wurde. So braucht die erste Version keine zusätzliche Tabelle für jeden einzelnen Wiederfund.

### Verhalten anhand eines Beispiels

| Durchlauf | Gelieferte IDs | Neu | Bekannt | Zeilen in `jobs` |
|---|---|---:|---:|---:|
| 1 | A, B, C | 3 | 0 | 3 |
| 2 | A, B, C | 0 | 3 | 3 |
| 3 | A, B, C, D | 1 | 3 | 4 |

Wenn sich der Titel von B ändert, wird B aktualisiert und bleibt bekannt. Dass eine Anzeige nicht erneut geliefert wird, beweist dagegen nicht, dass sie geschlossen ist: Sie kann außerhalb der Suchergebnisse oder der abgerufenen Seiten liegen.

### Umsetzungshinweis

`UNIQUE` ist die Absicherung in der Datenbank. Für „einfügen oder aktualisieren“ eignet sich `INSERT … ON CONFLICT`. Eine leicht nachvollziehbare Variante für den zunächst einzigen Importprozess:

1. `INSERT … ON CONFLICT DO NOTHING RETURNING id` ausführen.
2. Wurde eine ID zurückgegeben: neuer Job.
3. Andernfalls: vorhandenen Job aktualisieren und als bekannt zählen.

Beide Schritte gehören in eine Transaktion. Gleichzeitige Imports sind vorerst nicht vorgesehen; ihre Koordination folgt erst bei Bedarf.

### Integrationstests mit echter PostgreSQL-Testdatenbank

- [ ] Erster Import speichert drei Jobs.
- [ ] Wiederholter Import erzeugt keine weiteren Zeilen und meldet null neue Jobs.
- [ ] Veränderte Daten eines bekannten Jobs werden aktualisiert.
- [ ] Ein zusätzlicher Job erhöht die Anzahl um genau eins.
- [ ] Erstfundzeitpunkt und erster Import bleiben unverändert; letzter Fundzeitpunkt wird aktualisiert.
- [ ] Gleiche externe ID bei einer anderen Quelle ist ein separater Datensatz.
- [ ] Ein Datenbankfehler führt zum Rollback der betroffenen Importtransaktion.

### Definition of Done

- [ ] Jobs überleben einen Neustart der Anwendung.
- [ ] Die Wiederholung desselben Imports liefert zuverlässig `0 neu`.
- [ ] Die Datenbank selbst verhindert doppelte Quell-IDs.
- [ ] Integrationstests laufen auf einer getrennten Datenbank und hinterlassen dort einen definierten Zustand.

## 7. MS4 – Ein vollständiger Importbefehl

**Ziel:** Ein Aufruf führt die gesamte Verarbeitung aus und liefert verständliche Zahlen.

### ToDos

- [ ] CLI-Befehl für Suchbegriff, Ort und Seitenlimit implementieren.
- [ ] API-Client, Normalizer und Speicherung im Importer verbinden.
- [ ] Importdurchlauf mit Quelle und Suchparametern erfassen.
- [ ] Doppelte `(source, external_id)` innerhalb einer Antwort vor der Speicherung zusammenführen, beispielsweise mit „letzter Datensatz gewinnt“.
- [ ] API-Abruf und Normalisierung vor der Datenbank-Schreibtransaktion abschließen.
- [ ] Erfolgreiche Jobspeicherung und Abschlussstatistik gemeinsam committen.
- [ ] Bei einem Fehler Jobspeicherung zurückrollen und den Durchlauf separat als fehlgeschlagen abschließen, sofern die Datenbank erreichbar ist.
- [ ] Nicht erreichte Datenbank und verbliebene `running`-Durchläufe als erkennbare Fehler behandeln; kein falsches Erfolgssignal.
- [ ] Verständliche Logs und Exit-Code ergänzen: `0` bei Erfolg, ungleich `0` bei Fehler.

### Zielbefehl und Ausgabe

```bash
python -m jobhub import --query "DevOps" --location "Wien" --max-pages 2
```

```text
Import #7: erfolgreich
Suche: DevOps · Wien

Gelieferte Datensätze:        84
Eindeutige Quell-IDs:         82
Doppelt in dieser Antwort:    2
Neu gespeichert:             13
Bereits bekannt:             69
```

Für einen erfolgreichen Durchlauf gilt: `unique_jobs = new_jobs + known_jobs`. Die abgerufene Zahl enthält dagegen auch Wiederholungen innerhalb der Antwort. Ein leerer erfolgreicher Import meldet überall null.

### Ablauf-Tests

- [ ] Mock-API liefert A, B, C: drei neue Jobs.
- [ ] Dieselbe Antwort erneut: null neue, drei bekannte Jobs.
- [ ] Antwort liefert aktualisiertes B und zusätzlich D: ein neuer, drei bekannte Jobs; B ist aktualisiert.
- [ ] Antwort enthält A zweimal: ein gespeicherter Job und nachvollziehbare Statistik.
- [ ] API- oder Normalisierungsfehler hinterlässt keine neuen Jobzeilen.
- [ ] Ein Datenbankfehler hinterlässt keine teilweise gespeicherten Importergebnisse.
- [ ] Leere Antwort ist erfolgreich und löscht keine früher gespeicherten Jobs.
- [ ] CLI gibt bei Fehlern einen Fehlercode und eine verständliche Meldung zurück.

### Definition of Done

- [ ] Der Import funktioniert mit einem echten API-Zugang.
- [ ] Wiederholung ist ohne zusätzliche Datensätze möglich.
- [ ] Importstatistik stimmt mit dem Datenbankinhalt überein.
- [ ] Der automatisierte Ablauf-Test nutzt eine Mock-API und echte PostgreSQL-Testdatenbank.
- [ ] Erfolg und Fehlschlag sind in CLI und `import_runs` unterscheidbar.

## 8. MS5 – Gespeicherte Jobs mit Flask anzeigen

**Ziel:** Ein frühes, sichtbares Ergebnis. Flask liest zunächst ausschließlich die Datenbank; beim Öffnen einer Seite wird keine externe Job-API aufgerufen.

### ToDos

- [ ] Flask installieren und eine kleine App erstellen, beispielsweise über `create_app()`.
- [ ] Dashboard `/` mit Jobanzahl und letztem erfolgreichen Import bauen.
- [ ] Jobliste `/jobs` mit Titel, Firma, Ort, Erstfund und Original-Link bauen.
- [ ] Detailseite `/jobs/<id>` ergänzen.
- [ ] Ansicht „Neue Jobs im letzten erfolgreichen Import“ anbieten.
- [ ] Nach Erstfund absteigend sortieren und Listenlänge begrenzen beziehungsweise paginieren.
- [ ] Verständliche Anzeige für leere Datenbank und null neue Treffer ergänzen.
- [ ] Fehlgeschlagenen letzten Versuch getrennt vom letzten erfolgreichen Import anzeigen.
- [ ] Fehlende Job-ID mit HTTP 404 behandeln.
- [ ] Einfaches HTML/CSS verwenden und externe Inhalte als Text ausgeben; ungeprüftes HTML nicht mit `|safe` freischalten.

### Beispiel für die Oberfläche

> **JobHub**  
> 82 gespeicherte Jobs  
> Letzter erfolgreicher Import: 30.09.2026, 08:15  
> 13 neue Jobs in diesem Import
>
> **Platform Engineer**  
> Beispiel GmbH · Wien / Hybrid  
> Gehalt: nicht angegeben  
> Erstmals gefunden: 30.09.2026  
> [Details] [Originalanzeige]

### SQL-Beispiel: neue Jobs des letzten erfolgreichen Imports

```sql
SELECT id, title, company, location_text, url, first_seen_at
FROM jobs
WHERE first_seen_run_id = (
    SELECT id
    FROM import_runs
    WHERE status = 'succeeded'
    ORDER BY finished_at DESC, id DESC
    LIMIT 1
)
ORDER BY first_seen_at DESC, id DESC;
```

Ohne erfolgreichen Import liefert diese Abfrage keine Zeilen. Ein späterer erfolgreicher Import mit null neuen Jobs zeigt entsprechend eine leere Neuliste; ältere Jobs bleiben in der vollständigen Jobliste erreichbar.

### Flask-Tests

- [ ] Dashboard und Jobliste liefern HTTP 200.
- [ ] Ein vorhandener Job hat eine Detailseite; eine unbekannte ID liefert HTTP 404.
- [ ] Titel, Firma und Original-Link eines Testjobs erscheinen korrekt.
- [ ] Die Neuliste enthält genau die Erstfunde des letzten erfolgreichen Imports.
- [ ] Ein fehlgeschlagener Import verdrängt die letzte erfolgreiche Neuliste nicht.
- [ ] Leere Listen werden verständlich dargestellt.
- [ ] HTML in einem fremden Jobtitel wird als Text maskiert dargestellt.

Beispiel mit Flasks Test-Client:

```python
def test_unknown_job_returns_404(client):
    response = client.get("/jobs/999999")
    assert response.status_code == 404
```

Die `client`-Fixture richtet eine Test-App mit getrennten Testdaten ein. Für diese Tests muss kein echter Webserver laufen.

### Definition of Done

- [ ] Du öffnest JobHub lokal im Browser und siehst die importierten Anzeigen.
- [ ] Neue Jobs des letzten erfolgreichen Imports sind direkt erreichbar.
- [ ] Originalanzeigen lassen sich öffnen.
- [ ] Seitenaufrufe funktionieren ohne erneuten API-Aufruf.
- [ ] Kernseiten und zentrale Anzeigezustände sind getestet.

## 9. MS6 – Version 0.1 nutzbar abschließen

**Ziel:** Den kleinen Kern abrunden und reproduzierbar machen, bevor neue Features dazukommen.

### ToDos

- [ ] Einfache Textsuche über gespeicherte Titel und Firmen ergänzen.
- [ ] Optional einen Textfilter für `location_text` anbieten; ausdrücklich noch kein verlässlicher Radiusfilter.
- [ ] Zwischen vollständiger Liste und neuen Jobs des letzten erfolgreichen Imports umschalten können.
- [ ] Aktive Filter im Browser sichtbar machen; Filterwerte parametrisiert an SQL übergeben.
- [ ] Einrichtung, Datenbankschema, Import, Webstart und Tests im README dokumentieren.
- [ ] Testabhängigkeiten und Testdatenbank-Konfiguration dokumentieren.
- [ ] Screenshots und ein kurzes Datenfluss-Beispiel für das Portfolio ergänzen.
- [ ] Bekannte Grenzen festhalten: eine Quelle, begrenzte Suche, keine vollständige Marktabdeckung, keine quellübergreifende Deduplizierung.
- [ ] Version `v0.1.0` markieren, sobald die Abschlusskriterien erfüllt sind.

**Nicht erforderlich für V0.1:** Import per Webbutton, gespeicherte Suchprofile, Gehaltsfilter, Lesezeichen und Accounts. Ein manueller CLI-Import plus lesende Webseite ist bereits ein vollständiger erster Stand. Ein Importbutton kann danach folgen; er sollte bei später längeren Imports an einen Hintergrundprozess übergeben.

### Gesamte Definition of Done für V0.1

- [ ] Eine dokumentierte Suche lädt echte Jobs aus genau einer API.
- [ ] Anzeigen werden in PostgreSQL gespeichert und bei erneutem Fund aktualisiert.
- [ ] Derselbe Datenbestand zweimal importiert ergibt beim zweiten Mal null neue Jobs.
- [ ] Ein zusätzlicher Quell-Datensatz ergibt genau einen neuen Job.
- [ ] Fehlgeschlagene Imports erzeugen keinen scheinbar vollständigen Erfolg.
- [ ] Flask zeigt vollständige Liste, neue Treffer und Jobdetails.
- [ ] Unit-, Datenbank- und Flask-Tests prüfen die wesentlichen Verhaltensweisen.
- [ ] Keine automatisierten Tests benötigen echte API-Zugänge.
- [ ] Einrichtung und Grenzen sind nachvollziehbar dokumentiert.
- [ ] Zugangsdaten sind nicht versioniert.

## 10. Spätere Meilensteine – vorerst nur grob

| Ausbau | Nutzen / Anlass | Kleines Abschlussziel |
|---|---|---|
| Suchprofile | Wiederkehrende Suchen bequem ausführen | Mehrere gespeicherte Suchen manuell starten |
| Lesezeichen und Bewerbungsstatus | Interessante Jobs organisieren | Merken, Bewerbung geplant, beworben, Notizen |
| Zweite API | Mehr Quellen und Normalisierung erproben | Zweiter Client nutzt dasselbe interne Modell |
| Deduplizierung zwischen Quellen | Gleiche Stelle nicht mehrfach bearbeiten | Nachvollziehbare Regeln mit Testfällen; unsichere Treffer nicht blind zusammenführen |
| Bessere Standortfilter | Umkreis und Remote besser behandeln | Ortsdaten normalisieren und unbekannte Orte sichtbar lassen |
| Gehaltsfilter | Angaben vergleichen | Zeitraum, Währung, Arbeitszeit und Mindest-/Angebotsgehalt unterscheiden; keine pauschale Jahreshochrechnung ohne Annahmen |
| Druckansicht / Export | Anzeige für die Bewerbung festhalten | Saubere Druckansicht für zulässig gespeicherte Inhalte |
| Worker / Scheduler | Imports regelmäßig ausführen | Separater Importprozess, begrenzte Wiederholungen und Schutz gegen parallele Durchläufe |
| Docker / Compose | Umgebung reproduzierbar starten | Web, Datenbank und gegebenenfalls Worker gemeinsam starten |
| CI | Änderungen automatisch prüfen | Unit- und PostgreSQL-Integrationstests bei Push |
| Prometheus | Zuverlässigkeit wiederkehrender Imports messen | Importdauer, Fehler, neue Jobs und Zeitpunkt des letzten Erfolgs erfassen |
| Grafana | Betriebszustand sichtbar machen | Dashboard für Importerfolg, Fehler und Dauer |
| Backups / Wiederherstellung | Gespeicherte Arbeit schützen | Backup erstellen und Wiederherstellung ausprobieren |
| Mehrere Nutzer | Andere Personen sinnvoll einbeziehen | Eigene Suchprofile, Notizen und Jobzustände mit getesteter Zugriffstrennung |
| KI / semantische Suche | Lange Anzeigen aufbereiten und ähnliche Stellen finden | Kleine evaluierte Funktion, die Unsicherheit und Quellenbezug erhält |

Diese Reihenfolge bleibt anpassbar. Für dein Platform-/System-/DevOps-Portfolio dürfen Docker, CI und Monitoring nach dem funktionierenden Kern früh folgen; dafür müssen nicht erst sämtliche Produktfeatures fertig sein.

## 11. Die nächsten drei konkreten Arbeitsschritte

1. **MS0 minimal abschließen:** Projekt, virtuelle Umgebung, Konfigurationsdateien und README.
2. **Eine API auswählen und manuell testen:** Zugang, erlaubte Datenverwendung, Suchaufruf und Beispielantwort klären.
3. **Den kleinen Client samt Tests bauen:** echter Treffer im Terminal, Mock-Tests für Erfolg, leere Antwort, Timeout und HTTP-Fehler.

Der erste Erfolg ist erreicht, sobald eine echte Stellenanzeige durch deinen Python-Code läuft. Danach folgt der zweite: zweimal importieren und zuverlässig erkennen, was bereits bekannt ist. Die Flask-Ansicht macht diesen funktionierenden Kern sichtbar.

## 12. Offizielle technische Referenzen

- [Flask: Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/) – Test-Client und Fixtures.
- [PostgreSQL: INSERT](https://www.postgresql.org/docs/current/sql-insert.html) – `ON CONFLICT` und `RETURNING`.
- [pytest: Monkeypatching / Mocking](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) – externe Aufrufe in Tests ersetzen.

Die Referenzen wurden für die technischen Beispiele geprüft. API-spezifische Endpoints, Feldnamen und Limits werden erst mit der Auswahl des Anbieters ergänzt.
