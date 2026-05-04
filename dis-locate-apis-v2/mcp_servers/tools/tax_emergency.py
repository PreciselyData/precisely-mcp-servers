"""
Tax & Emergency Tools Module
Contains 5 tools for tax jurisdiction lookups and emergency (911/PSAP) services
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401

def get_tools() -> list[Tool]:
    """Returns list of tax and emergency tool definitions"""
    return [
        # Tax jurisdiction tool (1 consolidated tool replacing lookup_by_address/addresses/location/locations)
        Tool(
            name="lookup_tax_jurisdiction",
            description="""Look up US tax jurisdictions (state, county, and other codes) for one or more addresses or geographic coordinates in a single call.

Supports four usage patterns through one consistent interface:
  - Single address:    input_type='address', records=[{addressLines: ['123 Main St, Boston, MA']}]
  - Multiple addresses: input_type='address', records=[{...}, {...}]
  - Single coordinate: input_type='location', records=[{longitude: -71.0589, latitude: 42.3601}]
  - Multiple coordinates: input_type='location', records=[{...}, {...}]

Batch and single records use the same tool — pass 1 item for single lookup, N items for batch.
Only works for locations within the United States.

Output: For a single record, returns one tax jurisdiction object. For multiple records, returns an array of tax jurisdiction objects, one per input record. Each object contains tax type codes and full names (state, county, etc.).""",
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
        # Emergency services (1 consolidated tool replacing psap_address/psap_location/psap_ahj_address/psap_ahj_location/psap_ahj_fccid)
        Tool(
            name="find_emergency_services",
            description="""Find the PSAP (Public Safety Answering Point / 911 dispatch center) and optionally the AHJ (Authority Having Jurisdiction) for a US location.

Provide exactly one of:
  - address: a structured US street address
  - location: geographic coordinates [longitude, latitude]
  - fcc_id: an FCC-assigned PSAP identifier (from a prior call)

Set include_ahj=false to retrieve only PSAP data (lighter response). Default is true (returns both PSAP and AHJ). FCC ID lookups always include AHJ regardless of the flag.

Only works for locations within the United States.

Output: Object with PSAP name, phone, fccId, and (when AHJ is included) an array of AHJ records with agency name, type, phone, and other details.

Example — by address (PSAP only):
  address={"addressLines": ["860 White Plains Road"], "city": "Trumbull", "admin1": "CT", "postalCode": "06611"}, include_ahj=false

Example — by address (PSAP + AHJ):
  address={"addressLines": ["860 White Plains Road"], "city": "Trumbull", "admin1": "CT", "postalCode": "06611"}

Example — by coordinates (PSAP only):
  location={"coordinates": [-71.0589, 42.3601]}, include_ahj=false

Example — by coordinates (PSAP + AHJ):
  location={"coordinates": [-71.0589, 42.3601]}

Example — by FCC ID:
  fcc_id="1404"
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {
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
                    },
                    "location": {
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
                    },
                    "fcc_id": {
                        "type": "string",
                        "description": (
                            "The FCC-assigned PSAP identifier (e.g., '1404'). "
                            "Obtain this value from a prior find_emergency_services call."
                        )
                    },
                    "include_ahj": {
                        "type": "boolean",
                        "default": True,
                        "description": (
                            "When true (default), returns both PSAP and AHJ data. "
                            "When false, returns only PSAP data (lighter response). "
                            "Ignored when fcc_id is provided (FCC ID lookup always includes AHJ)."
                        )
                    }
                },
                "oneOf": [
                    {"required": ["address"]},
                    {"required": ["location"]},
                    {"required": ["fcc_id"]}
                ]
            }
        ),
    ]

