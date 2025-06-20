import requests
from typing import Optional, Dict, Any
from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()

from precisely_sdk.server import mcp

@mcp.tool()
def parse_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse Single-Line Address into Structured Components.

    --------
    Required Payload Structure:
    {
        "address": "1700 district ave #300 burlington, ma"  # REQUIRED
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Parsed address components

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

    url = f"{client.base_url}/v1/address/parse"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def parse_address_batch(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse Batch of Addresses into Structured Components (max 10 addresses per request).

    --------
    Required Payload Structure:
    {
        "addresses": [                 # REQUIRED
            {"id": "1", "address": "1700 district ave #300 burlington, ma"},  # REQUIRED
            {"id": "2", "address": "170 district ave burlington, ma"}
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Parsed address responses

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
    
    url = f"{client.base_url}/v1/address/parse/batch"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()
