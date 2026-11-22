# packages from the python universe :-) ----------
import argparse
from pathlib import Path

# own modules ------------------------------------------
# nothing

def parse_options(argv=None):

    parser = argparse.ArgumentParser(description="Suche nach Stellenanzeigen.",
                                     epilog="Beispiel: python main.py --job Softwareentwickler",
                                     prog="JobHub (c) Basti xD")

    input_group_01 = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s v0.1"
    )

    input_group_01.add_argument(
        "--jobs", "-j",
        type=str,
        metavar="JOB",
        help="jobdescription, e.g. --job 'DevOps'",
    )
    input_group_01.add_argument(
        "--load_config_file", "--lcf",
        type=Path,
        metavar="config.json",
        help="Suchkriterien aus einer JSON-Datei laden.",
    )
    input_group_01.add_argument(
        "--create_job_template", "--cjt",
        help="Create a job template (json) to be read-in. different versions available",
        nargs="?",
        const="compact_full",
        choices=("compact_full",),
    )

    parser.add_argument(
        "--filename",
        type=Path,
        help="filename for the chosen template"
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
        choices=("at", "de", "fr", "es", "it", "gb", "us", "au", "be", "br", "ca", "ch", "in", "mx", "nl", "nz", "pl", "sg", "za"),
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
        if options.location is None:
            parser.error("--distance darf nur zusammen mit --location angegeben werden.")
        if options.distance < 0:
            parser.error("--distance darf nicht negativ sein.")

    if options.filename is None and options.create_job_template is not None:
        parser.error("--create_job_template requires --filename.")

    return options

def parse_config_file_content(config) -> bool:
    pass