"""
Geocoding & Address Tools Module
Contains 9 tools for geocoding, address verification, autocomplete, and address parsing
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of geocoding and address tool definitions"""
    return [
        Tool(
            name="geocode",
            description="Convert address to coordinates. Example: {'address': '42 Valley Of The Sun Dr, Fairplay, CO 80440', 'country': 'USA'}",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "country": {"type": "string", "default": "USA"}
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="reverse_geocode",
            description="Convert coordinates to address. Example: {'lat': 39.5501, 'lon': -105.9999, 'country': 'USA'}",
            inputSchema={
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                    "country": {"type": "string", "default": "USA"}
                },
                "required": ["lat", "lon"]
            }
        ),
        Tool(
            name="verify_address",
            description="Verify and standardize address. Example: {'address': '1600 Pennsylvania Ave, Washington DC', 'country': 'USA'}",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "country": {"type": "string", "default": "USA"}
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="autocomplete",
            description="Address autocomplete suggestions. Example: {'address': {'addressLines': ['1700 District'], 'country': 'USA'}, 'preferences': {'maxResults': 5}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "object"},
                    "preferences": {"type": "object"}
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="autocomplete_postal_city",
            description="Autocomplete postal codes and cities. Example: {'address': {'type': 'POSTAL', 'postAddress': '12180', 'country': 'USA'}, 'preferences': {'maxResults': 5}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "object"},
                    "preferences": {"type": "object"}
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="autocomplete_v2",
            description="Express autocomplete (V2). Example: {'address': {'addressLines': ['350 Jordan'], 'country': 'USA'}, 'preferences': {'maxResults': 5}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "object"},
                    "preferences": {"type": "object"}
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="lookup",
            description="Lookup address by PreciselyID. Example: {'keys': [{'key': 'P0000GL41OME', 'country': 'USA', 'type': 'PB_KEY'}]}",
            inputSchema={
                "type": "object",
                "properties": {
                    "keys": {"type": "array", "items": {"type": "object", "properties": {"key": {"type": "string"}, "country": {"type": "string"}, "type": {"type": "string"}}}},
                    "preferences": {"type": "object"}
                },
                "required": ["keys"]
            }
        ),
        Tool(
            name="parse_address",
            description="Parse single address. Example: {'address': '1700 District Ave #300, Burlington, MA 01803'}",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "string"}
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="parse_address_batch",
            description="Parse multiple addresses (max 10). Example: {'addresses': [{'id': '1', 'address': '123 Main St, Boston, MA 02101'}, {'id': '2', 'address': '456 Oak Ave, Denver, CO 80203'}]}",
            inputSchema={
                "type": "object",
                "properties": {
                    "addresses": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "address": {"type": "string"}}}}
                },
                "required": ["addresses"]
            }
        ),
    ]

