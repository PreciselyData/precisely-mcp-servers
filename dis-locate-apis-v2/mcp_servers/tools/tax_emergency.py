"""
Tax & Emergency Tools Module
Contains 9 tools for tax jurisdiction lookups and PSAP (911) services
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401

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
    }
}

_PSAP_LOCATION_SCHEMA = {
    "type": "object",
    "description": "Geographic coordinates for PSAP lookup.",
    "properties": {
        "coordinates": {
            "type": "array",
            "items": {"type": "number"},
            "description": "Coordinates as [longitude, latitude] (e.g., [-71.0589, 42.3601]). WGS 84 datum/EPSG:4326 coordinate system.",
            "minItems": 2,
            "maxItems": 2
        }
    },
    "required": ["coordinates"]
}


def get_tools() -> list[Tool]:
    """Returns list of tax and emergency tool definitions"""
    return [
        # Tax jurisdiction tool (1 consolidated tool replacing lookup_by_address/addresses/location/locations)
        Tool(
            name="lookup_tax_jurisdiction",
            description=(
                "Look up US tax jurisdictions (state, county, and other codes) "
                "for one or more addresses or geographic coordinates in a single call.\n\n"
                "Supports four usage patterns through one consistent interface:\n"
                "  - Single address:    input_type='address', records=[{addressLines: ['123 Main St, Boston, MA']}]\n"
                "  - Multiple addresses: input_type='address', records=[{...}, {...}]\n"
                "  - Single coordinate: input_type='location', records=[{longitude: -71.0589, latitude: 42.3601}]\n"
                "  - Multiple coordinates: input_type='location', records=[{...}, {...}]\n\n"
                "Batch and single records use the same tool — pass 1 item for single lookup, N items for batch.\n"
                "Only works for locations within the United States.\n\n"
                "Output: For a single record, returns one tax jurisdiction object. "
                "For multiple records, returns an array of tax jurisdiction objects, one per input record. "
                "Each object contains tax type codes and full names "
                "(state, county, etc.)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "input_type": {
                        "type": "string",
                        "enum": ["address", "location"],
                        "description": (
                            "Discriminator for record type. "
                            "Use 'address' when records contain street addresses. "
                            "Use 'location' when records contain longitude/latitude coordinates."
                        )
                    },
                    "records": {
                        "type": "array",
                        "minItems": 1,
                        "description": (
                            "List of one or more input records to look up. "
                            "When input_type is 'address', each item is an address object with addressLines. "
                            "When input_type is 'location', each item is a coordinate object with longitude and latitude."
                        ),
                        "items": {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "title": "Address Record",
                                    "description": "Use when input_type is 'address'.",
                                    "properties": {
                                        "addressLines": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "Street address lines (e.g., ['123 Main St, Boston, MA'] or ['123 Main St', 'Boston, MA 02101']).",
                                            "minItems": 1
                                        },
                                        "city": {"type": "string", "description": "City name (e.g., 'Boston')."},
                                        "admin1": {"type": "string", "description": "State abbreviation (e.g., 'MA')."},
                                        "postalCode": {"type": "string", "description": "ZIP or postal code (e.g., '02101')."},
                                    },
                                    "required": ["addressLines"]
                                },
                                {
                                    "type": "object",
                                    "title": "Location Record",
                                    "description": "Use when input_type is 'location'.",
                                    "properties": {
                                        "longitude": {
                                            "type": "number",
                                            "description": "Longitude in decimal degrees (e.g., -71.0589). Valid range: -180 to 180.",
                                            "minimum": -180,
                                            "maximum": 180
                                        },
                                        "latitude": {
                                            "type": "number",
                                            "description": "Latitude in decimal degrees (e.g., 42.3601). Valid range: -90 to 90.",
                                            "minimum": -90,
                                            "maximum": 90
                                        }
                                    },
                                    "required": ["longitude", "latitude"]
                                }
                            ]
                        }
                    }
                },
                "required": ["input_type", "records"]
            }
        ),
        # PSAP/Emergency services tools (5 tools)
        Tool(
            name="psap_address",
            description=(
                "Retrieve the PSAP (Public Safety Answering Point / 911 dispatch center) responsible for a given US address. "
                "Returns the PSAP name, phone number, fccId, and other information. "
                "Use this tool when you need to identify the correct 911 call center for a street address. "
                "Do NOT use if you also need AHJ (Authority Having Jurisdiction) data — use psap_ahj_address instead. "
                "Do NOT use if you have coordinates rather than an address — use psap_location instead. "
                "Only works for addresses within the United States.\n\n"
                "Output: Object with PSAP information."
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
                "Returns the PSAP name, phone number, fccId, and other information. "
                "Use this tool when you have a coordinate pair (longitude, latitude) and need to identify the 911 center. "
                "Do NOT use if you also need AHJ (Authority Having Jurisdiction) data — use psap_ahj_location instead. "
                "Do NOT use if you have a street address rather than coordinates — use psap_address instead. "
                "Only works for coordinates within the United States.\n\n"
                "Output: Object with PSAP information."
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
                "Output: Object with PSAP name, phone, fccId, AHJ names "
                "and other details."
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
                "Output: Object with PSAP name, phone, fccId, AHJ names "
                "and other details."
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
                "Output: Object with PSAP name, phone, fccID, AHJ names and other details for the specified FCC ID."
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

