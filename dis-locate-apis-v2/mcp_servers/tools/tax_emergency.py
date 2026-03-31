"""
Tax & Emergency Tools Module
Contains 10 tools for tax jurisdiction lookups and PSAP (911) services
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of tax and emergency tool definitions"""
    return [
        # Tax jurisdiction tools (4 tools)
        Tool(
            name="lookup_by_address",
            description="Lookup tax jurisdiction by address. Example: {'address': {'addressLines': ['123 Main St, Boston, MA']}}",
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
            name="lookup_by_addresses",
            description="Get tax jurisdictions for multiple addresses. Example: {'addresses': [{'addressLines': ['2001 Main St, Eagle Butte, SD 57625']}, {'addressLines': ['2520 Columbia House Blvd #108, Vancouver, WA 98661']}], 'preferences': {}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "addresses": {"type": "array", "items": {"type": "object", "properties": {"addressLines": {"type": "array", "items": {"type": "string"}}}}},
                    "preferences": {"type": "object"}
                },
                "required": ["addresses"]
            }
        ),
        Tool(
            name="lookup_by_location",
            description="Lookup tax jurisdiction by coordinates. Example: {'location': {'longitude': -71.0589, 'latitude': 42.3601}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {"type": "object"},
                    "preferences": {"type": "object"}
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="lookup_by_locations",
            description="Find tax jurisdictions for multiple coordinates. Example: {'locations': [{'longitude': -98.401796, 'latitude': 34.688726}, {'longitude': -92.9036, 'latitude': 34.8192}], 'preferences': {}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "locations": {"type": "array", "items": {"type": "object", "properties": {"longitude": {"type": "number"}, "latitude": {"type": "number"}}}},
                    "preferences": {"type": "object"}
                },
                "required": ["locations"]
            }
        ),
        # PSAP/Emergency services tools (5 tools)
        Tool(
            name="psap_address",
            description="Get PSAP (911) by address. Example: {'address': {'addressLines': ['860 White Plains Road'], 'city': 'Trumbull', 'admin1': 'CT', 'postalCode': '06611'}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "object"}
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="psap_location",
            description="Get PSAP by coordinates. Example: {'location': {'coordinates': [-71.0589, 42.3601]}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {"type": "object"}
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="psap_ahj_address",
            description="Get PSAP+AHJ by address. Example: {'address': {'addressLines': ['860 White Plains Road'], 'city': 'Trumbull', 'admin1': 'CT', 'postalCode': '06611'}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {"type": "object"}
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="psap_ahj_location",
            description="Get PSAP+AHJ by coordinates. Example: {'location': {'coordinates': [-71.0589, 42.3601]}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {"type": "object"}
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="psap_ahj_fccid",
            description="Get PSAP+AHJ by FCC ID. Example: {'fcc_id': '1404'}",
            inputSchema={
                "type": "object",
                "properties": {
                    "fcc_id": {"type": "string"}
                },
                "required": ["fcc_id"]
            }
        ),
    ]

