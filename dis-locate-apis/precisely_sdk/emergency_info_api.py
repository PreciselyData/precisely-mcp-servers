import requests
from typing import Optional, Dict, Any
from precisely_sdk.server import mcp

from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()


@mcp.tool()
def psap_address(client, json_data: Dict[str, Any], x_request_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve PSAP Contact Details Using Address Input.
    
    Required Payload Structure:
    {
    "address": {                                    #Required
        "addressLines": [
        "860 White Plains Road Trumbull CT 06611, USA"
        ],
        "admin1": "Connecticut",
        "admin2": "Trumbull",
        "city": "Trumbull",
        "borough": "",
        "suburb": "",
        "postalCode": "06611",
        "postalCodeExt": "",
        "placeName": ""
    }
    }
        """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/emergency-info/psap/address"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def psap_location(client, json_data: Dict[str, Any], x_request_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve PSAP Contact Details Using Location Input.

    Required Payload Structure:
    {
        "location": {
            "coordinates": [-73.22344, 41.23443]
        }
    }
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/emergency-info/psap/location"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def psap_ahj_address(client, json_data: Dict[str, Any], x_request_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve PSAP+AHJ Contact Details Using Address Input.

    Required Payload Structure:
        {
    "address": {                        #Required
        "addressLines": [
        "860 White Plains Road Trumbull CT 06611, USA"
        ],
        "admin1": "Connecticut",
        "admin2": "Trumbull",
        "city": "Trumbull",
        "borough": "",
        "suburb": "",
        "postalCode": "06611",
        "postalCodeExt": "",
        "placeName": ""
    }
    }
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/emergency-info/psap-ahj/address"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def psap_ahj_location(client, json_data: Dict[str, Any], x_request_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve PSAP+AHJ Contact Details Using Location Input.

    Required Payload Structure:
    {
        "location": {
            "coordinates": [-73.22344, 41.23443]
        }
    }
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   

    url = f"{client.base_url}/v1/emergency-info/psap-ahj/location"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def psap_ahj_fccid(client, fcc_id: str, x_request_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve PSAP+AHJ Contact Details Using FCC ID.

    Required Parameter:
    - fcc_id: FCC ID as string.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )   
    
    url = f"{client.base_url}/v1/emergency-info/psap-ahj/fccid"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    params = {"fccId": fcc_id}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
