"""
Tax & Emergency Tools Module
Contains 9 tools for tax jurisdiction lookups and PSAP (911) services
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401

_ADDRESS_SCHEMA = {
    "type": "object",
    "description": "Structured address object.",
    "properties": {
        "addressLines": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Street address lines (e.g., ['123 Main St, Boston, MA'] or ['123 Main St', 'Boston, MA']).",
            "minItems": 1
        },
        "city": {"type": "string", "description": "City name."},
        "admin1": {"type": "string", "description": "State abbreviation (e.g., 'MA')."},
        "postalCode": {"type": "string", "description": "ZIP or postal code."},
        "country": {"type": "string", "description": "ISO 3-letter country code. Default: 'USA'."}
    },
    "required": ["addressLines"]
}

_PSAP_ADDRESS_SCHEMA = {
    "type": "object",
    "description": "Structured US address for PSAP lookup.",
    "properties": {
        "addressLines": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Street address lines (e.g., ['860 White Plains Road']).",
            "minItems": 1
        },
        "city": {"type": "string", "description": "City name (e.g., 'Trumbull')."},
        "admin1": {"type": "string", "description": "State abbreviation (e.g., 'CT')."},
        "postalCode": {"type": "string", "description": "ZIP code (e.g., '06611')."},
        "country": {"type": "string", "description": "ISO 3-letter country code. Default: 'USA'."}
    },
    "required": ["addressLines"]
}

_PSAP_LOCATION_SCHEMA = {
    "type": "object",
    "description": "Geographic coordinates for PSAP lookup.",
    "properties": {
        "coordinates": {
            "type": "array",
            "items": {"type": "number"},
            "description": "Coordinates as [longitude, latitude] (e.g., [-71.0589, 42.3601]).",
            "minItems": 2,
            "maxItems": 2
        }
    },
    "required": ["coordinates"]
}

_TAX_PREFERENCES_SCHEMA = {
    "type": "object",
    "description": "Optional preferences for tax jurisdiction lookup behavior.",
    "properties": {
        "returnLatLong": {"type": "boolean", "description": "Whether to include the resolved latitude/longitude in the response."},
        "useGeoTaxTables": {"type": "boolean", "description": "Whether to use GeoTAX-specific tables for lookup."}
    }
}


def get_tools() -> list[Tool]:
    """Returns list of tax and emergency tool definitions"""
    return [
        # Tax jurisdiction tools (4 tools)
        Tool(
            name="lookup_by_address",
            description=(
                "Look up the tax jurisdictions that apply to a single US address. "
                "Returns state, county, township, municipal, school district, and other tax type codes "
                "for the most precise geographic match available. "
                "Use this tool when you have a single address and need to determine applicable tax codes. "
                "Do NOT use for multiple addresses — use lookup_by_addresses instead (one batch call is more efficient). "
                "Do NOT use for coordinate-based lookup — use lookup_by_location instead. "
                "Only works for addresses within the United States.\n\n"
                "Output: Object containing tax jurisdiction identifiers and full names "
                "(state, county, municipal, school district, etc.) for the resolved address."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": _ADDRESS_SCHEMA,
                    "preferences": _TAX_PREFERENCES_SCHEMA
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="lookup_by_addresses",
            description=(
                "Look up tax jurisdictions for multiple US addresses in a single batch call. "
                "Returns state, county, township, municipal, school district, and other tax type codes for each address. "
                "Use this tool when you have two or more addresses and need tax jurisdiction data "
                "(more efficient than repeated lookup_by_address calls). "
                "Do NOT use for a single address — use lookup_by_address instead. "
                "Do NOT use for coordinate-based lookup — use lookup_by_locations instead. "
                "Only works for addresses within the United States.\n\n"
                "Output: Array of tax jurisdiction objects, one per input address, each containing "
                "tax codes and full names (state, county, municipal, school district, etc.)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "addresses": {
                        "type": "array",
                        "description": "List of addresses to look up tax jurisdictions for.",
                        "items": _ADDRESS_SCHEMA,
                        "minItems": 2
                    },
                    "preferences": _TAX_PREFERENCES_SCHEMA
                },
                "required": ["addresses"]
            }
        ),
        Tool(
            name="lookup_by_location",
            description=(
                "Look up the tax jurisdiction for a single geographic coordinate (longitude/latitude) within the United States. "
                "Returns state, county, township, municipal, school district, and other tax codes for the location. "
                "Use this tool when you have coordinates (e.g., from a GPS or geocoder) and need tax jurisdiction data. "
                "Do NOT use for address-based lookup — use lookup_by_address instead. "
                "Do NOT use for multiple coordinates — use lookup_by_locations instead (one batch call is more efficient). "
                "Only works for coordinates within the United States.\n\n"
                "Output: Object containing tax jurisdiction identifiers and full names for the given coordinate location."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "object",
                        "description": "Geographic coordinate for the tax jurisdiction lookup.",
                        "properties": {
                            "longitude": {
                                "type": "number",
                                "description": "Longitude in decimal degrees (e.g., -71.0589).",
                                "minimum": -180,
                                "maximum": 180
                            },
                            "latitude": {
                                "type": "number",
                                "description": "Latitude in decimal degrees (e.g., 42.3601).",
                                "minimum": -90,
                                "maximum": 90
                            }
                        },
                        "required": ["longitude", "latitude"]
                    },
                    "preferences": _TAX_PREFERENCES_SCHEMA
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="lookup_by_locations",
            description=(
                "Look up tax jurisdictions for multiple geographic coordinates (longitude/latitude) in a single batch call. "
                "Returns state, county, township, municipal, school district, and other tax codes for each location. "
                "Use this tool when you have two or more coordinate pairs and need tax jurisdiction data "
                "(more efficient than repeated lookup_by_location calls). "
                "Do NOT use for a single coordinate — use lookup_by_location instead. "
                "Do NOT use for address-based lookup — use lookup_by_addresses instead. "
                "Only works for coordinates within the United States.\n\n"
                "Output: Array of tax jurisdiction objects, one per input coordinate, each containing "
                "tax codes and full names (state, county, municipal, school district, etc.)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "locations": {
                        "type": "array",
                        "description": "List of coordinate pairs to look up tax jurisdictions for.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "longitude": {
                                    "type": "number",
                                    "description": "Longitude in decimal degrees.",
                                    "minimum": -180,
                                    "maximum": 180
                                },
                                "latitude": {
                                    "type": "number",
                                    "description": "Latitude in decimal degrees.",
                                    "minimum": -90,
                                    "maximum": 90
                                }
                            },
                            "required": ["longitude", "latitude"]
                        },
                        "minItems": 2
                    },
                    "preferences": _TAX_PREFERENCES_SCHEMA
                },
                "required": ["locations"]
            }
        ),
        # PSAP/Emergency services tools (5 tools)
        Tool(
            name="psap_address",
            description=(
                "Retrieve the PSAP (Public Safety Answering Point / 911 dispatch center) responsible for a given US address. "
                "Returns the PSAP name, phone number, and jurisdiction information. "
                "Use this tool when you need to identify the correct 911 call center for a street address. "
                "Do NOT use if you also need AHJ (Authority Having Jurisdiction) data — use psap_ahj_address instead. "
                "Do NOT use if you have coordinates rather than an address — use psap_location instead. "
                "Only works for addresses within the United States.\n\n"
                "Output: Object with PSAP name, contact phone number, and jurisdiction boundary information."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": _PSAP_ADDRESS_SCHEMA
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="psap_location",
            description=(
                "Retrieve the PSAP (Public Safety Answering Point / 911 dispatch center) responsible for a given geographic coordinate. "
                "Returns the PSAP name, phone number, and jurisdiction information for the location. "
                "Use this tool when you have a coordinate pair (longitude, latitude) and need to identify the 911 center. "
                "Do NOT use if you also need AHJ (Authority Having Jurisdiction) data — use psap_ahj_location instead. "
                "Do NOT use if you have a street address rather than coordinates — use psap_address instead. "
                "Only works for coordinates within the United States.\n\n"
                "Output: Object with PSAP name, contact phone number, and jurisdiction boundary information."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "location": _PSAP_LOCATION_SCHEMA
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="psap_ahj_address",
            description=(
                "Retrieve combined PSAP (Public Safety Answering Point / 911 dispatch center) and "
                "AHJ (Authority Having Jurisdiction) data for a given US address in a single call. "
                "PSAP identifies the emergency dispatch center; AHJ identifies the regulatory and code authority for the location. "
                "Use this tool when you need both PSAP and AHJ information for an address. "
                "Do NOT use if you only need PSAP data — use psap_address instead (lighter response). "
                "Do NOT use if you have coordinates rather than an address — use psap_ahj_location instead. "
                "Do NOT use if lookup is by FCC ID — use psap_ahj_fccid instead. "
                "Only works for addresses within the United States.\n\n"
                "Output: Object with PSAP details (name, phone, jurisdiction) and AHJ details "
                "(authority name, NPA NXX, jurisdiction code)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": _PSAP_ADDRESS_SCHEMA
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="psap_ahj_location",
            description=(
                "Retrieve combined PSAP (Public Safety Answering Point / 911 dispatch center) and "
                "AHJ (Authority Having Jurisdiction) data for a given geographic coordinate in a single call. "
                "Use this tool when you have a coordinate pair (longitude, latitude) and need both PSAP and AHJ information. "
                "Do NOT use if you only need PSAP data — use psap_location instead (lighter response). "
                "Do NOT use if you have a street address rather than coordinates — use psap_ahj_address instead. "
                "Do NOT use if lookup is by FCC ID — use psap_ahj_fccid instead. "
                "Only works for coordinates within the United States.\n\n"
                "Output: Object with PSAP details (name, phone, jurisdiction) and AHJ details "
                "(authority name, NPA NXX, jurisdiction code)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "location": _PSAP_LOCATION_SCHEMA
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="psap_ahj_fccid",
            description=(
                "Retrieve PSAP (Public Safety Answering Point / 911 dispatch center) and "
                "AHJ (Authority Having Jurisdiction) details for a PSAP identified by its FCC (Federal Communications Commission) ID. "
                "Use this tool only when you already have a specific FCC PSAP ID and need its full record. "
                "Do NOT use if you are starting from an address — use psap_ahj_address instead. "
                "Do NOT use if you are starting from coordinates — use psap_ahj_location instead. "
                "FCC IDs are obtained from prior psap_address, psap_location, or related calls. "
                "Only works for US PSAP entities.\n\n"
                "Output: Object with PSAP details (name, phone, jurisdiction) and AHJ details for the specified FCC ID."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "fcc_id": {
                        "type": "string",
                        "description": "The FCC-assigned PSAP identifier (e.g., '1404'). "
                                       "Obtain this value from a prior psap_address or psap_location call."
                    }
                },
                "required": ["fcc_id"]
            }
        ),
    ]

