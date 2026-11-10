# JobHub

JobHub is a personal, non-commercial portfolio project aimed at bringing together job listings from multiple platforms through their APIs.

The long-term plan is to store results in a database, identify duplicate listings, and distinguish newly discovered jobs from those I have already viewed. Further ideas include custom filters that existing job platforms do not offer and analysing job listings over time—for example, to explore technology requirements or advertised salary ranges.

The project is currently at an early stage. These features are future plans; the initial focus is on retrieving listings from a single API and building a small, working foundation.

## Development setup

Use a project-specific Python virtual environment and activate it before running:

```bash
python -m pip install -r requirements.txt
python -m pytest --version
python main.py
```

milestone 2: job retrieval is implemented as well as error handling