"""
Geocoding & Address Tools Module
Contains 9 tools for geocoding, address verification, autocomplete, and address parsing
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401

_AUTOCOMPLETE_ADDRESS_SCHEMA = {
    "type": "object",
    "description": "Partial address input for autocomplete suggestions.",
    "properties": {
        "addressLines": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Partial street address text to autocomplete (e.g., ['1700 District'])."
        },
        "country": {
            "type": "string",
            "description": "Values per ISO 3166-1 standard for country codes (alpha-2, alpha-3, or numeric format) e.g. USA, US or 840"
        },
        "city": {"type": "string", "description": "Optional city to narrow suggestions."},
        "admin1": {"type": "string", "description": "Optional state/province abbreviation to narrow suggestions."},
        "postalCode": {"type": "string", "description": "Optional postal code to narrow suggestions."}
    },
    "required": ["addressLines", "country"]
}

_AUTOCOMPLETE_PREFERENCES_SCHEMA = {
    "type": "object",
    "description": "Preferences for controlling autocomplete behavior.",
    "properties": {
        "maxResults": {
            "type": "integer",
            "description": "Maximum number of suggestions to return.",
            "default": 5,
            "minimum": 1,
            "maximum": 25
        },
    }
}


def get_tools() -> list[Tool]:
    """Returns list of geocoding and address tool definitions"""
    return [
        Tool(
            name="geocode",
            description=(
                "Convert a free-text street address into geographic coordinates (latitude/longitude) "
                "and a structured address record including PB_KEY/PreciselyID. "
                "Use this tool when you need lat/lon from a human-readable address string. "
                "Do NOT use for reverse lookup (coordinates → address) — use reverse_geocode instead. "
                "Do NOT use when you already have a Precisely key like PB_KEY — use lookup instead. "
                "Do NOT use when address validation and standardization is the goal — use verify_address instead "
                "Output: Object with latitude, longitude, standardized address components "
                "(street number, street name, city, state, postal code), and confidence/match quality indicators, other details."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "Full or partial street address string (e.g., '42 Valley Of The Sun Dr, Fairplay, CO 80440')."
                    },
                    "country": {
                        "type": "string",
                        "description": "Values per ISO 3166-1 standard for country codes (alpha-2, alpha-3, or numeric format) e.g., USA, US or 840.",
                        "default": "USA"
                    }
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="reverse_geocode",
            description=(
                "Convert geographic coordinates (latitude, longitude) into a nearest matching street address. "
                "Use this tool when you have a lat/lon pair and need a human-readable address. "
                "Do NOT use when you have a text address — use geocode instead. "
                "Do NOT use when you need structured data beyond the address (e.g., property info)"
                "Output: Object with the nearest matching standardized address (street, city, state, postal code, country), "
                "distance from the input coordinate to the matched address, other details."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "lat": {
                        "type": "number",
                        "description": "Latitude in decimal degrees (e.g., 39.5501).",
                        "minimum": -90,
                        "maximum": 90
                    },
                    "lon": {
                        "type": "number",
                        "description": "Longitude in decimal degrees (e.g., -105.9999).",
                        "minimum": -180,
                        "maximum": 180
                    },
                    "country": {
                        "type": "string",
                        "description": "Name of country in ISO 3166-1 Alpha-2 or Alpha-3 format, or a common name of the country e.g. USA.",
                        "default": "USA"
                    }
                },
                "required": ["lat", "lon"]
            }
        ),
        Tool(
            name="verify_address",
            description=(
                "Verify, standardize, and correct a postal address. "
                "Checks whether the address is deliverable, corrects formatting/spelling, "
                "and returns the standardized form including postal code and address components. "
                "Use this tool when address quality, deliverability, or standardization is the goal. "
                "Do NOT use if you only need coordinates — use geocode instead "
                "(geocode is optimized for coordinate resolution, verify_address is optimized for postal validation). "
                "Do NOT use for non-postal spatial queries — use geocode or spatial tools instead.\n\n"
                "Output: Object with standardized address components, deliverability indicators, and match confidence."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "Address string to verify and standardize (e.g., '1600 Pennsylvania Ave, Washington DC')."
                    },
                    "country": {
                        "type": "string",
                        "description": "Values per ISO 3166-1 standard for country codes (alpha-2, alpha-3, or numeric format) e.g. USA, US or 840.",
                        "default": "USA"
                    }
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="autocomplete",
            description=(
                "Return ranked address autocomplete suggestions for a partial address string. "
                "Returns up to maxResults matching addresses. "
                "Suitable for full street address completion (house number + street + city). "
                "Do NOT use for postal code-only or city-only completion — use autocomplete_postal_city instead. "
                "Do NOT use for one-time full address resolution — use geocode or verify_address instead. "
                "For lower-latency consider autocomplete_v2 instead.\n\n"
                "Output: Array of address suggestion strings with structured address components "
                "(addressLine, city, state, postal code, country)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": _AUTOCOMPLETE_ADDRESS_SCHEMA,
                    "preferences": _AUTOCOMPLETE_PREFERENCES_SCHEMA
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="autocomplete_postal_city",
            description=(
                "Return autocomplete suggestions for postal codes and city names — not full street addresses. "
                "Use when a user is typing a ZIP code, postal code, or city name and you want to offer matching city/postal combinations. "
                "Do NOT use for full street address completion — use autocomplete or autocomplete_v2 instead. "
                "Output: Array of postal/city suggestion objects with postal code, city name, state, and country."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {
                        "type": "object",
                        "description": "Postal or city query object.",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "Lookup type. Use 'POSTAL' for postal suggestions, and 'CITY' for city suggestions.",
                                "enum": ["POSTAL", "CITY"]
                            },
                            "postAddress": {
                                "type": "string",
                                "description": "Partial postal code or city name to complete (e.g., '12180' or 'Bos')."
                            },
                            "country": {
                                "type": "string",
                                "description": "Name of country in ISO 3166-1 Alpha-2 or Alpha-3 format, or a common name of the country e.g. USA.",
                            }
                        },
                        "required": ["postAddress", "country"]
                    },
                    "preferences": _AUTOCOMPLETE_PREFERENCES_SCHEMA
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="autocomplete_v2",
            description=(
                "Return ranked address autocomplete suggestions using the V2 (express) engine, "
                "which is faster and optimized for lower latency. "
                "Use when latency is critical and the user is providing a full street address. "
                "Do NOT use for postal code or city-only completion — use autocomplete_postal_city instead.\n\n"
                "Output: Array of address suggestion objects with structured components "
                "(street, city, state, postal code, country)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": _AUTOCOMPLETE_ADDRESS_SCHEMA,
                    "preferences": _AUTOCOMPLETE_PREFERENCES_SCHEMA
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="lookup",
            description=(
                "Retrieve full address record(s) by one or more Precisely keys (internal system identifiers). "
                "Precisely keys are opaque string keys (e.g., 'P0000GL41OME') that uniquely identify a location "
                "in the Precisely data platform. "
                "Use this tool when you already have a Precisely key obtained from a prior call like geocode, ogc_collection_items, others. "
                "Do NOT use if you only have a human-readable address — use geocode instead. "
                "Supports batch lookup of multiple keys in a single call.\n\n"
                "Output: Array of full address records (one per key), each containing standardized address components, "
                "coordinates, and associated metadata."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "keys": {
                        "type": "array",
                        "description": "List of Precisely key objects to resolve.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "key": {
                                    "type": "string",
                                    "description": "Value for the given Key e.g., 'P0000GL41OME'."
                                },
                                "country": {
                                    "type": "string",
                                    "description": "Name of country in ISO 3166-1 Alpha-2 or Alpha-3 format, or a common name of the country e.g. USA."
                                },
                                "type": {
                                    "type": "string",
                                    "description": "Key type identifier.",
                                    "enum": ["PB_KEY", "GNAF_PID", "UDPRN", "UPRN", "EIR_CODE"]
                                }
                            },
                            "required": ["key", "country", "type"]
                        },
                        "minItems": 1
                    },
                    "preferences": {
                        "type": "object",
                        "description": "Optional preferences for controlling the returned fields."
                    }
                },
                "required": ["keys"]
            }
        ),
        Tool(
            name="parse_address",
            description=(
                "Parse a single free-text address string into its individual structural components: "
                "house number, street name, street type, unit, city, state, postal code, and country. "
                "Use this tool when you need to decompose an address into parts for data processing or validation. "
                "Do NOT use if you need coordinates — use geocode instead. "
                "Do NOT use for multiple addresses in one call — use parse_address_batch instead.\n\n"
                "Output: Object with individual address components extracted from the input string "
                "(addressNumber, streetName, streetType, unitDesignator, unitValue, city, admin1, postalCode, country)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "Full address string to parse (e.g., '1700 District Ave #300, Burlington, MA 01803')."
                    }
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="parse_address_batch",
            description=(
                "Parse multiple free-text address strings into their individual structural components in a single batch call. "
                "Each address is decomposed into house number, street name, street type, unit, city, state, postal code, and country. "
                "Use this tool when you have two or more addresses to parse (more efficient than repeated parse_address calls). "
                "Do NOT use for a single address — use parse_address instead. "
                "Maximum batch size: 10 addresses per call.\n\n"
                "Output: Array of parsed address objects (one per input), each with individual components "
                "(addressNumber, streetName, streetType, unitDesignator, city, admin1, postalCode, country). "
                "Each result includes the 'id' field from the corresponding input for correlation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "addresses": {
                        "type": "array",
                        "description": "List of address strings to parse. Maximum 10 per call.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "description": "Client-supplied identifier to correlate this input with its output (e.g., '1')."
                                },
                                "address": {
                                    "type": "string",
                                    "description": "Full address string to parse (e.g., '123 Main St, Boston, MA 02101')."
                                }
                            },
                            "required": ["address"]
                        },
                        "minItems": 1,
                        "maxItems": 10
                    }
                },
                "required": ["addresses"]
            }
        ),
    ]

