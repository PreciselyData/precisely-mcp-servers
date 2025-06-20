import requests
from typing import Optional, Dict, Any
from precisely_sdk.server import mcp

from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()


@mcp.tool()
def validate_phone(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform Single Phone Number Verification.

    --------
    Required Payload Structure:
    {
        "phoneNumber": "7063062767",   # REQUIRED
        "country": "US"                # OPTIONAL (ISO2/ISO3 country code)
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Phone verification response containing
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/phone-numbers/validate"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def validate_batch_phones(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform Batch Phone Number Verification (max 10 phone numbers).

    --------
    Required Payload Structure:
    {
        "phoneNumbers": [                    # REQUIRED
            { "id": "1", "phoneNumber": "7063062767", "country": "US" },  # REQUIRED
            { "id": "2", "phoneNumber": "767425446", "country": "SWE" }   # REQUIRED
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Phone verification response containing
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   
    
    url = f"{client.base_url}/v1/phone-numbers/validate/batch"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()
