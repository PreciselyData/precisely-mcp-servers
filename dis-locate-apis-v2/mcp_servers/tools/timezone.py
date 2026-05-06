"""
Timezone Tools Module
Contains 1 tool for timezone lookups by address or coordinates
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of timezone tool definitions"""
    return [
        Tool(
            name="get_timezones",
            description="""Look up the timezone for one or more addresses or geographic coordinates (longitude, latitude), including UTC offset and DST status, at a specific UTC point in time. Returns the IANA timezone name (e.g., 'America/New_York'), UTC offset in hours and minutes, and whether daylight saving time (DST) is in effect at the given timestamp. Provide either 'addresses' (when you have street addresses) or 'locations' (when you have coordinate pairs) — not both. Supports multiple entries in a single call.

Output: Array of timezone result objects (one per input), each containing the IANA timezone ID, UTC offset, DST status, and the input id for correlation.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "addresses": {
                        "type": "array",
                        "description": "List of addresses to resolve timezone for. Provide this OR 'locations', not both.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "integer",
                                    "description": (
                                        "UTC timestamp in milliseconds for which to evaluate timezone/DST status "
                                        "(e.g., 1691138974831). If omitted, the current server time is used."
                                    )
                                },
                                "address": {
                                    "type": "object",
                                    "description": "Structured address object.",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "Client-supplied identifier to correlate this input with its output (e.g., '1')."
                                        },
                                        "addressLines": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "Street address lines (e.g., ['1700 District Ave, Burlington, MA']).",
                                            "minItems": 1
                                        },
                                        "country": {
                                            "type": "string",
                                            "description": "ISO 3166-1 compliant country code (alpha-2, alpha-3, or numeric). (e.g., 'USA')."
                                        }
                                    },
                                    "required": ["country"]
                                }
                            },
                            "required": ["timestamp", "address"]
                        },
                        "minItems": 1
                    },
                    "locations": {
                        "type": "array",
                        "description": "List of coordinate pairs to resolve timezone for. Provide this OR 'addresses', not both.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "description": "Client-supplied identifier to correlate this input with its output (e.g., '1')."
                                },
                                "timestamp": {
                                    "type": "integer",
                                    "description": (
                                        "UTC timestamp in milliseconds for which to evaluate timezone/DST status "
                                        "(e.g., 1691138974831). If omitted, the current server time is used."
                                    )
                                },
                                "geometry": {
                                    "type": "object",
                                    "description": "GeoJSON-style geometry object with coordinates.",
                                    "properties": {
                                        "coordinates": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "description": "Coordinates as [longitude, latitude] WGS 84 datum/EPSG:4326 coordinate system (e.g., [-71.0589, 42.3601]).",
                                            "minItems": 2,
                                            "maxItems": 2
                                        }
                                    },
                                    "required": ["coordinates"]
                                }
                            },
                            "required": ["timestamp", "geometry"]
                        },
                        "minItems": 1
                    }
                },
                "oneOf": [
                    {"required": ["addresses"]},
                    {"required": ["locations"]}
                ]
            }
        ),
    ]

