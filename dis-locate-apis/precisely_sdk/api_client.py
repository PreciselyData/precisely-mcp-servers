import base64
from typing import Optional, Dict
import os
from dotenv import load_dotenv

# Load environment variables once at module level
load_dotenv()


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


# Centralized client factory
_client_instance = None

def get_default_client() -> ApiClient:
    """
    Get a shared ApiClient instance configured with environment variables.
    
    Returns:
        ApiClient: Configured client instance
    """
    global _client_instance
    
    if _client_instance is None:
        api_key = os.getenv('API_KEY')
        api_secret = os.getenv('API_SECRET')
        base_url = os.getenv('BASE_URL')
        bearer_token = os.getenv('BEARER_TOKEN')
        
        if not base_url:
            raise ValueError("BASE_URL environment variable is required")
        
        if not (api_key or bearer_token):
            raise ValueError("Either API_KEY or BEARER_TOKEN environment variable is required")
        
        _client_instance = ApiClient(
            base_url=base_url,
            api_key=api_key,
            api_secret=api_secret,
            bearer_token=bearer_token
        )
    
    return _client_instance


def reset_client():
    """Reset the shared client instance (useful for testing)"""
    global _client_instance
    _client_instance = None
