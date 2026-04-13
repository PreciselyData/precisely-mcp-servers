"""Load and validate environment configuration."""

import logging
import os
import sys

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_config() -> dict:
    """Load credentials from .env and validate they are present.

    Returns a dict with keys: api_key, api_secret, base_url.
    Exits with code 1 if required credentials are missing.
    """
    load_dotenv(override=True)

    api_key = os.getenv("PRECISELY_API_KEY")
    api_secret = os.getenv("PRECISELY_API_SECRET")
    base_url = os.getenv("PRECISELY_BASE_URL", "https://api.cloud.precisely.com")

    if not api_key or not api_secret:
        logger.critical(
            "PRECISELY_API_KEY and PRECISELY_API_SECRET must be set. "
            "Copy .env.template to .env and fill in your credentials."
        )
        sys.exit(1)

    return {"api_key": api_key, "api_secret": api_secret, "base_url": base_url}
