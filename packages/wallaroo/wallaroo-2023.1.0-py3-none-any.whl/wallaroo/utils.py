import os

ARROW_ENABLED = "ARROW_ENABLED"


def is_arrow_enabled():
    return os.getenv(ARROW_ENABLED, "false").lower() == "true"
