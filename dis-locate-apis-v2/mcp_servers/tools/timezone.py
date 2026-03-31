"""
Timezone Tools Module
Contains 2 tools for timezone lookups by address and coordinates
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of timezone tool definitions"""
    return [
        Tool(
            name="timezone_addresses",
            description="Get timezone for addresses. Example: {'data': {'addresses': [{'timestamp': 1691138974831, 'address': {'id': '1', 'addressLines': ['1700 District Ave, Burlington, MA'], 'country': 'USA'}}]}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Object with 'addresses' array containing address objects with timestamp, id, addressLines, and country"}
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="timezone_locations",
            description="Get timezone for coordinates. Example: {'data': {'locations': [{'id': '1', 'timestamp': 1691138974831, 'geometry': {'coordinates': [-71.0589, 42.3601]}}]}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Object with 'locations' array containing location objects with id, timestamp, and geometry.coordinates [lon, lat]"}
                },
                "required": ["data"]
            }
        ),
    ]

