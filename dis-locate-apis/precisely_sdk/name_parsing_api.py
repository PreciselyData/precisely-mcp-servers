import requests
from typing import Optional, Dict, Any
from precisely_sdk.server import mcp

from precisely_sdk.api_client import get_default_client


@mcp.tool()
def parse_name(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse Personal & Business Name into Components.

    --------
    Required Payload Structure:
    {
        "name": "Jack and Daniel Smith",       # REQUIRED
        "options": {                           # OPTIONAL
            "parseNaturalOrderPersonalNames": true,
            "parseReverseOrderPersonalNames": true,
            "parseConjoinedNames": true,
            "parseBusinessNames": true
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): Payload as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Name parsing response containing
    """
    client = get_default_client()
    
    url = f"{client.base_url}/v1/names/parse"
    headers = client.get_headers()
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()
