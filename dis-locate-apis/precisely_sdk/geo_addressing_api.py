import requests
from typing import Optional, Dict, Any, List
from precisely_sdk.server import mcp
from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()



@mcp.tool()
def autocomplete(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None,
    x_transaction_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Address Autocomplete API (type-ahead search)

    This API provides address autocomplete suggestions globally.

    --------
    Required Payload Structure:
    {
        "preferences": {                # REQUIRED
            "maxResults": 5,            # OPTIONAL (default: system default)
            "returnAllInfo": True,      # OPTIONAL
            "clientLocale": "en_US",    # OPTIONAL
            "customPreferences": {}     # OPTIONAL
        },
        "address": {                    # REQUIRED
            "addressLines": ["350 Jordan"],  # REQUIRED: partial input text
            "country": "USA"                 # REQUIRED: 3-letter or 2-letter country code
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body (see above structure).
        x_request_id (Optional[str]): Optional request ID (max 38 chars).
        x_transaction_id (Optional[str]): Optional transaction grouping ID.

    Returns:
        dict: Autocomplete response object.

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


    url = f"{client.base_url}/v1/autocomplete"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    if x_transaction_id:
        headers["X-Transaction-Id"] = x_transaction_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def autocomplete_postal_city(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None,
    x_transaction_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Autocomplete Postal City API

    Suggests postal codes & city names based on partial input.

    --------
    Required Payload Structure:
    {
        "preferences": {                # REQUIRED
            "maxResults": 5,            # OPTIONAL
            "returnAllInfo": True,      # OPTIONAL
            "clientLocale": "en_US",    # OPTIONAL
            "customPreferences": {}     # OPTIONAL
        },
        "address": {                    # REQUIRED
            "type": "POSTAL",           # REQUIRED
            "postAddress": "12180",     # REQUIRED
            "country": "USA"            # REQUIRED
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body (see above structure).
        x_request_id (Optional[str]): Optional request ID.
        x_transaction_id (Optional[str]): Optional transaction ID.

    Returns:
        dict: Autocomplete Postal City response object.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/autocomplete/postal-city"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    if x_transaction_id:
        headers["X-Transaction-Id"] = x_transaction_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def autocomplete_v2(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None,
    x_transaction_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Express Autocomplete API (V2)

    Faster autocomplete with support for SEARCH_TYPE: ADDRESS, POI, AUTO

    --------
    Required Payload Structure:
    {
        "preferences": {                    # REQUIRED
            "maxResults": 5,                # OPTIONAL
            "returnAllInfo": True,          # OPTIONAL
            "clientLocale": "en_US",        # OPTIONAL
            "customPreferences": {
                "SEARCH_TYPE": "ADDRESS"    # OPTIONAL: ADDRESS/POI/AUTO
            }
        },
        "address": {                        # REQUIRED
            "addressLines": ["350 Jordan"],
            "country": "USA"
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body (see above structure).
        x_request_id (Optional[str]): Optional request ID.
        x_transaction_id (Optional[str]): Optional transaction ID.

    Returns:
        dict: Autocomplete V2 response object.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/express-autocomplete"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id
    if x_transaction_id:
        headers["X-Transaction-Id"] = x_transaction_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def geocode(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Geocode API

    Geocodes address(es) and returns coordinates & standardization.

    --------
    Required Payload Structure:
    {
        "preferences": {              # REQUIRED
            "maxResults": 1,          # OPTIONAL
            "returnAllInfo": True,    # OPTIONAL
            "clientLocale": "en_US"   # OPTIONAL
        },
        "addresses": [                # REQUIRED
            {
                "addressId": "1",     # OPTIONAL ID
                "addressLines": ["1700 District Ave #300 Burlington, MA"],
                "country": "USA"      # REQUIRED
            }
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body (see above structure).
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Geocode response object.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/geocode"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def lookup(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lookup API

    Lookup address details by PreciselyID.

    --------
    Required Payload Structure:
    {
        "preferences": {              # REQUIRED
            "maxResults": 1,          # OPTIONAL
            "returnAllInfo": True,    # OPTIONAL
            "clientLocale": "en_US"   # OPTIONAL
        },
        "keys": [                     # REQUIRED
            {
                "key": "P0000GL41OME", # REQUIRED (PreciselyID)
                "country": "USA",      # REQUIRED
                "type": "PB_KEY"       # REQUIRED
            }
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body (see above structure).
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Lookup response object.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/lookup"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def reverse_geocode(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Reverse Geocode API

    Retrieves nearest address based on coordinates.

    --------
    Required Payload Structure:
    {
        "preferences": {              # REQUIRED
            "maxResults": 1,          # OPTIONAL
            "returnAllInfo": True,    # OPTIONAL
            "clientLocale": "en_US"   # OPTIONAL
        },
        "locations": [                # REQUIRED
            {
                "addressId": "1",     # OPTIONAL ID
                "longitude": -73.7047, # REQUIRED
                "latitude": 42.6822,   # REQUIRED
                "country": "USA"       # REQUIRED
            }
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body (see above structure).
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: Reverse Geocode response object.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/reverse-geocode"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def verify_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Verify API

    Verifies and standardizes input addresses and returns cleaned, validated address data.

    --------
    Required Payload Structure:
    {
        "preferences": {              # OPTIONAL
            "returnAllInfo": True,
            "clientLocale": "en_US"
        },
        "addresses": [                # REQUIRED
            {
                "addressId": "1",     # Optional tracking ID
                "addressLines": ["1700 District Ave #300 Burlington, MA"],
                "country": "USA"      # REQUIRED (e.g., "US", "USA")
            }
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Request body in the expected format.
        x_request_id (Optional[str]): Optional header for traceability.

    Returns:
        dict: Verify response object containing cleaned and validated address results.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/v1/verify"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()
