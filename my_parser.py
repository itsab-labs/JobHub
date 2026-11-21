# packages from the python universe :-) ----------
import argparse
from pathlib import Path

# own modules ------------------------------------------
#nothing yet

def parse_options(argv=None):

    parser = argparse.ArgumentParser(description="Suche nach Stellenanzeigen.",
                                     epilog="Beispiel: python main.py --job Softwareentwickler",
                                     prog="JobHub (c) Basti xD")

    input_group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s v0.1"
    )

    input_group.add_argument(
        "--jobs", "-j",
        type=str,
        metavar="JOB",
        help="jobdescription, e.g. --job 'DevOps'",
    )
    input_group.add_argument(
        "--config",
        type=Path,
        metavar="config.json",
        help="Suchkriterien aus einer JSON-Datei laden.",
    )

    parser.add_argument(
        "--exclude", "--excl",
        type=str,
        metavar="EXCLUDE",
        help="Exclude certain words from the job description, e.g. --exclude 'Python'\n"
             " if there are more than on word, separate them by a blanc," 
             "e.g. --exclude 'Python Java'",
    )

    parser.add_argument(
        "--location", "-l",
        type=str,
        metavar="LOCATION",
        help="Location to search for jobs, e.g. --location 'Wien'",
    )

    parser.add_argument(
        "--distance", "-d",
        type=int,
        metavar="DISTANCE in km",
        help="Distance in kilometers to search for jobs, e.g. --distance 50",
    )

    parser.add_argument(
        "--country", "-c",
        type=str,
        choices=("at", "de", "fr", "es", "it", "gb"), #longterm: gb, us, au, be, br, ca, ch, in, mx, nl, nz, pl, sg, za
        default="at",
        help="Country to search for jobs, e.g. --country at",
    )

    parser.add_argument(
        "--salary_min", "-s",
        type=int,
        help="Minimum salary in EUR, e.g. --salary_min 50000",
    )

    parser.add_argument(
        "--full_time_only", "--fto",
        action="store_true",
        help=f"Only show full time jobs, e.g. --full_time_only, default: %(default)s",
    )

    parser.add_argument(
        "--max_days_old", "--mdo",
        type=int,
        metavar="DAYS",
        default=30,
        help="Maximum days old of the job description, default: %(default)s",
    )

    options = parser.parse_args(argv)

    if options.distance is not None:
        if options.town is None:
            parser.error("--distance darf nur zusammen mit --town angegeben werden.")
        if options.distance < 0:
            parser.error("--distance darf nicht negativ sein.")

    return options