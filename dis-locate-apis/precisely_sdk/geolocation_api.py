import requests
from typing import Optional, Dict, Any
from precisely_sdk.server import mcp

from precisely_sdk.api_client import get_default_client


@mcp.tool()
def geo_locate_ip_address(
    client,
    ip_address: str,
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Geolocate by IP Address.

    --------
    Required Payload Structure:
    (Sent as query parameter)
    ipAddress: "<IP_ADDRESS>"  # REQUIRED (example: "54.86.242.73")

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        ip_address (str): REQUIRED IP address to lookup.
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: IP geolocation response containing
    """
    client = get_default_client()
    
    url = f"{client.base_url}/v1/geolocation/ip-address"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    params = {"ipAddress": ip_address}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def geo_locate_wifi_access_point(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Geolocate using WiFi Access Point(s).

    --------
    Required Payload Structure:
    {
        "servingCell": {               # REQUIRED
            "mac": "00:22:75:10:d5:91",    # REQUIRED
            "ssid": "",                    # OPTIONAL
            "rssi": "-90",                 # OPTIONAL
            "speed": "500"                 # OPTIONAL
        },
        "otherCells": [                 # OPTIONAL
            {
                "mac": "00:22:75:10:d5:91",  # REQUIRED
                "ssid": "",                  # OPTIONAL
                "rssi": "-90",               # OPTIONAL
                "speed": "100"               # OPTIONAL
            }
        ]
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Payload as shown above.
        x_request_id (Optional[str]): Optional request ID.

    Returns:
        dict: WiFi geolocation response containing
    """
    client = get_default_client()
    
    url = f"{client.base_url}/v1/geolocation/access-point"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()
