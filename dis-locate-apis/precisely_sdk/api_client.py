import base64
from typing import Optional, Dict


class ApiClient:
    """
    Precisely API Client.

    Supports both API Key Auth (ApiKeyAuth) and Bearer Token Auth (bearerAuth).
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        bearer_token: Optional[str] = None
    ):
        """
        Initialize the client.

        Args:
            base_url (str): The Precisely API base URL (e.g., https://api.cloud.precisely.com)
            api_key (Optional[str]): Your Precisely API key (used for ApiKeyAuth)
            api_secret (Optional[str]): Your Precisely API secret (used for ApiKeyAuth with secret)
            bearer_token (Optional[str]): OAuth 2.0 Bearer token (used for bearerAuth)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.api_secret = api_secret
        self.bearer_token = bearer_token

    def get_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Construct authentication headers.

        Args:
            custom_headers (Optional[Dict[str, str]]): Any extra headers you want to pass.

        Returns:
            Dict[str, str]: Full request headers including authentication.
        """
        headers = {"Content-Type": "application/json"}

        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        elif self.api_key and self.api_secret:
            credentials = f"{self.api_key}:{self.api_secret}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Apikey {encoded}"
        elif self.api_key:
            headers["Authorization"] = f"Apikey {self.api_key}"

        if custom_headers:
            headers.update(custom_headers)

        return headers
