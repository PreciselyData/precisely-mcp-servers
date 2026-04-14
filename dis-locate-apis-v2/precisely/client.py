"""
Base Precisely API client: session setup, authentication, shared helpers.
"""

import base64
import logging
import os
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)


class BaseClient:
    """Handles session creation, authentication, and shared GraphQL validation."""

    def __init__(self, api_key: str, api_secret: str, base_url: str = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url or os.getenv(
            "PRECISELY_BASE_URL", "https://api.cloud.precisely.com"
        )
        self.session = requests.Session()
        credentials = f"{api_key}:{api_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.session.headers.update(
            {
                "Authorization": f"Apikey {encoded}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def with_bearer_token(self, token: str) -> "BaseClient":
        """Return a copy of this client that authenticates with a Bearer token."""
        instance = object.__new__(self.__class__)
        instance.api_key = None
        instance.api_secret = None
        instance.base_url = self.base_url
        instance.session = requests.Session()
        instance.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        return instance

    def _validate_graphql_response(
        self, result: Dict[str, Any], method_name: str
    ) -> Dict[str, Any]:
        """Validate a GraphQL response for errors. GraphQL returns HTTP 200 even on errors."""
        if "errors" in result:
            errors = result["errors"]
            error_messages = [e.get("message", str(e)) for e in errors]
            logger.error(f"[{method_name}] GraphQL errors: {error_messages}")
            if "data" in result and result["data"]:
                result["graphql_errors"] = error_messages
                result["completeness"] = "partial"
                return result
            return {
                "error": "; ".join(error_messages),
                "error_type": "permanent",
                "graphql_errors": errors,
            }
        return result
