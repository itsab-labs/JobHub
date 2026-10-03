import logging
from pathlib import Path

from config import ROOT_LOG_LEVEL, CONSOLE_LOG_LEVEL, FILE_LOG_LEVEL

def get_log_level(level_name: str) -> int:
    level = logging.getLevelName(level_name.upper())

    if not isinstance(level, int):
        raise ValueError(f"Invalid log level: {level_name}")

    return level

def configure_logging(log_file: str | Path = "moviehub.log") -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(
        get_log_level(ROOT_LOG_LEVEL)
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(
        get_log_level(CONSOLE_LOG_LEVEL)
    )

    file_handler = logging.FileHandler(
        log_file,
        mode="w", # Overwrite the log file on each run
        encoding="utf-8"
    )
    file_handler.setLevel(
        get_log_level(FILE_LOG_LEVEL)
    )

    console_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(funcName)s:%(lineno)d | %(message)s"
    )

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)