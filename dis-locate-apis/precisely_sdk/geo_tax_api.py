import requests
from typing import Optional, Dict, Any
from precisely_sdk.server import mcp

from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()


@mcp.tool()
def lookup_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lookup Tax Jurisdiction by Address.

    --------
    Required Payload Structure:
    {
        "address": {                       # REQUIRED
            "addressLines": ["2001 Main St, Eagle Butte, SD 57625"],  # REQUIRED
            "admin1": "",                  # OPTIONAL
            "admin2": "",                  # OPTIONAL
            "city": "",                    # OPTIONAL
            "postalCode": "",              # OPTIONAL
            "postalCodeExt": ""            # OPTIONAL
        },
        "preferences": {                   # OPTIONAL
            "output": {...},
            "geocoding": {...},
            "matching": {...}
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request payload as shown above.
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Tax jurisdiction response containing
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/geo-tax/address"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def lookup_by_addresses(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lookup Tax Jurisdiction for Multiple Addresses (Batch).

    --------
    Required Payload Structure:
    {
        "addresses": [                      # REQUIRED
            { "addressLines": ["2001 Main St, Eagle Butte, SD 57625"] },
            { "addressLines": ["2520 Columbia House Blvd #108, Vancouver, WA 98661"] }
        ],
        "preferences": {                   # OPTIONAL
            "output": {...},
            "geocoding": {...},
            "matching": {...}
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request payload as shown above.
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Batch tax jurisdiction response containing
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/geo-tax/address/batch"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def lookup_by_location(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lookup Tax Jurisdiction by Coordinates.

    --------
    Required Payload Structure:
    {
        "location": {                # REQUIRED
            "longitude": -98.401796, # REQUIRED
            "latitude": 34.688726    # REQUIRED
        },
        "preferences": {             # OPTIONAL
            "output": {...},
            "geocoding": {...},
            "matching": {...}
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request payload as shown above.
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Tax jurisdiction response containing
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   
    
    url = f"{client.base_url}/v1/geo-tax/location"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def lookup_by_locations(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lookup Tax Jurisdiction for Multiple Coordinates (Batch).

    --------
    Required Payload Structure:
    {
        "locations": [                # REQUIRED
            { "longitude": -98.401796, "latitude": 34.688726 },
            { "longitude": -92.9036, "latitude": 34.8192 }
        ],
        "preferences": {             # OPTIONAL
            "output": {...},
            "geocoding": {...},
            "matching": {...}
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request payload as shown above.
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Batch tax jurisdiction response containing
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   
    
    url = f"{client.base_url}/v1/geo-tax/location/batch"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()
