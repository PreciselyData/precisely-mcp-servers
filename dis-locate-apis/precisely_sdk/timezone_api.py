import requests
from typing import Optional, Dict, Any
from precisely_sdk.server import mcp

from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()


@mcp.tool()
def timezone_addresses(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve timezone information for address input.

    --------
    Required Payload Structure:
    {
        "addresses": [                   # REQUIRED
            {
                "timestamp": 1691138974831,  # REQUIRED (UTC timestamp in milliseconds)
                "address": {
                    "id": "1",               # REQUIRED (unique identifier for request)
                    "addressLines": ["950 Josephine Street Denver CO 80204"],  # REQUIRED
                    "country": "USA"         # REQUIRED (ISO2/ISO3 country code)
                }
            }
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request payload as above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Timezone response containing
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/timezone/address"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def timezone_locations(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve timezone information for coordinates input.

    --------
    Required Payload Structure:
    {
        "locations": [                   # REQUIRED
            {
                "id": "1",                  # REQUIRED (unique identifier for request)
                "timestamp": 1691138974831, # REQUIRED (UTC timestamp in milliseconds)
                "geometry": {
                    "coordinates": [-89.398528, 40.633125]  # REQUIRED [longitude, latitude]
                }
            }
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request payload as above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Timezone response containing
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   
    
    url = f"{client.base_url}/v1/timezone/location"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()
