import requests
from typing import Optional, Dict, Any
from precisely_sdk.server import mcp

from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()


@mcp.tool()
def verify_email(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform Single Email Verification.

    --------
    Required Payload Structure:
    {
        "email": "example@email.com"  # REQUIRED
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body as shown above.
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Email verification response

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/emails/verify"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def verify_batch_emails(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform Batch Email Verification (max 10 emails per request).

    --------
    Required Payload Structure:
    {
        "emails": [                       # REQUIRED
            {"id": "1", "email": "test1@email.com"},  # REQUIRED
            {"id": "2", "email": "test2@email.com"}
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body as shown above.
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Batch verification response

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   
    
    url = f"{client.base_url}/v1/emails/verify/batch"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()
