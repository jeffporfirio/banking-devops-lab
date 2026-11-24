import logging
import os
import sys


def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    numeric_level = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format=(
            "%(asctime)s %(levelname)s "
            "[%(name)s] %(message)s"
        ),
        stream=sys.stdout,
        force=True
    )

    logging.getLogger("werkzeug").setLevel(numeric_level)