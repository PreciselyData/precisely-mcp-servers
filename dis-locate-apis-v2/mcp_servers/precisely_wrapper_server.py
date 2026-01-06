"""
Precisely MCP Server - Wrapper Architecture
Uses the PreciselyAPI class from precisely_api_core_clean module
Supports both stdio (default) and Streamable HTTP transports
"""
import asyncio
import sys
import os
import argparse
import contextlib
from pathlib import Path
from typing import Any, Dict, Optional
from collections.abc import AsyncIterator
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import logging
from dotenv import load_dotenv

# HTTP Transport imports (optional - loaded only when needed)
HTTP_AVAILABLE = False
try:
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    from starlette.applications import Starlette
    from starlette.routing import Mount
    from starlette.types import Receive, Scope, Send
    import uvicorn
    HTTP_AVAILABLE = True
except ImportError:
    pass  # HTTP transport not available - stdio only

# Add parent directory to path to import from precisely_api_core.py
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import the PreciselyAPI class from the core module
from precisely_api_core import PreciselyAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("precisely-mcp-wrapper")

# Load environment variables (override=True ensures fresh values)
load_dotenv(override=True)
API_KEY = os.getenv("PRECISELY_API_KEY")
API_SECRET = os.getenv("PRECISELY_API_SECRET")
BASE_URL = "https://api.cloud.precisely.com"

# Initialize the PreciselyAPI core module
precisely_api = PreciselyAPI(API_KEY, API_SECRET, BASE_URL)

# Create MCP server
app = Server("precisely-complete-mcp")

# Tool definitions (49 tools covering all Precisely APIs)
TOOLS = [
    # Geocoding & Address (9 tools)
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
    
    # Property & Risk (12 tools)
    Tool(
        name="get_property_data",
        description="Get property information. Example: {'address': '42 Valley Of The Sun Dr, Fairplay, CO 80440', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_property_attributes_by_address",
        description="Get property attributes (bedrooms, bathrooms, etc). Example: {'address': '2755 Milwaukee St, Denver, 80238 CO', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_replacement_cost_by_address",
        description="Get property replacement cost. Example: {'address': '2755 Milwaukee St, Denver, 80238 CO', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_flood_risk_by_address",
        description="Get flood risk by address. Example: {'address': '2755 Milwaukee St, Denver, 80238 CO', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_wildfire_risk_by_address",
        description="Get wildfire risk by address. Example: {'address': '2755 Milwaukee St, Denver, 80238 CO', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_property_fire_risk",
        description="Get property fire risk. Example: {'address': '123 Main St, Boston, MA', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_earth_risk",
        description="Get earthquake risk. Example: {'address': '123 Main St, San Francisco, CA', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_coastal_risk",
        description="Get coastal risk. Example: {'address': '123 Ocean Ave, Miami, FL', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_historical_weather_risk",
        description="Get historical weather risk. Example: {'address': '123 Main St, Boston, MA', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    
    # Demographics & Neighborhoods (6 tools)
    Tool(
        name="get_demographics",
        description="Get demographic data (PSYTE + Ground View). Example: {'address': '456 Oak Avenue, Denver, CO 80203', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_crime_index",
        description="Get crime index data. Example: {'address': '42 Valley Of The Sun Dr, Fairplay, CO 80440', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_psyte_geodemographics_by_address",
        description="Get PSYTE geodemographics. Example: {'address': '123 Main St, Boston, MA', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_ground_view_by_address",
        description="Get ground view demographics. Example: {'address': '999 Lake Shore Drive, Chicago, IL', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_neighborhoods_by_address",
        description="Get neighborhood information. Example: {'address': '123 Main St, Boston, MA', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_schools_by_address",
        description="Get nearby schools. Example: {'address': '2755 Milwaukee St, Denver, 80238 CO', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_buildings_by_address",
        description="Get building information. Example: {'address': '123 Main St, Boston, MA', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    Tool(
        name="get_parcels_by_address",
        description="Get parcel information. Example: {'address': '2755 Milwaukee St, Denver, 80238 CO', 'country': 'US'}",
        inputSchema={
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "country": {"type": "string", "default": "US"}
            },
            "required": ["address"]
        }
    ),
    
    # Tax & Emergency (10 tools)
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
    
    # Geolocation (2 tools)
    Tool(
        name="geo_locate_ip_address",
        description="Geolocate IP address. Example: {'ip_address': '8.8.8.8'}",
        inputSchema={
            "type": "object",
            "properties": {
                "ip_address": {"type": "string"}
            },
            "required": ["ip_address"]
        }
    ),
    Tool(
        name="geo_locate_wifi_access_point",
        description="Geolocate WiFi access point. Example: {'wifi_data': {'servingCell': {'mac': '00:22:75:10:d5:91', 'rssi': '-90'}}}",
        inputSchema={
            "type": "object",
            "properties": {
                "wifi_data": {"type": "object"}
            },
            "required": ["wifi_data"]
        }
    ),
    
    # Email & Phone & Name (6 tools)
    Tool(
        name="verify_email",
        description="Verify single email. Example: {'email': 'john.doe@company.com'}",
        inputSchema={
            "type": "object",
            "properties": {
                "email": {"type": "string"}
            },
            "required": ["email"]
        }
    ),
    Tool(
        name="verify_batch_emails",
        description="Verify multiple emails (max 10). Example: {'emails': [{'id': '1', 'email': 'john@company.com'}, {'id': '2', 'email': 'jane@company.com'}]}",
        inputSchema={
            "type": "object",
            "properties": {
                "emails": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "email": {"type": "string"}}}}
            },
            "required": ["emails"]
        }
    ),
    Tool(
        name="parse_name",
        description="Parse name into components. Example: {'data': {'name': 'John Robert Smith'}}",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "Object with 'name' field containing full name to parse"}
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="validate_phone",
        description="Validate phone number. Example: {'data': {'phoneNumber': '4144654885', 'country': 'US'}}",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "object"}
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="validate_batch_phones",
        description="Validate multiple phones (max 10). Example: {'data': {'phoneNumbers': [{'id': '1', 'phoneNumber': '3035551234', 'country': 'US'}, {'id': '2', 'phoneNumber': '7205559999', 'country': 'US'}]}}",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "Object with 'phoneNumbers' array containing phone objects with id, phoneNumber, and country fields"}
            },
            "required": ["data"]
        }
    ),
    
    # Timezone (2 tools)
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
    
    # Advanced GraphQL (4 tools)
    Tool(
        name="get_addresses_detailed",
        description="""Get detailed address information using custom GraphQL query.
        
Example request:
{'data': {
  'query': 'query GetAddressDetailed($address: String!, $country: String) { getByAddress(address: $address, country: $country) { addresses { data { preciselyID addressNumber streetName city admin1ShortName postalCode } } } }',
  'variables': {'address': '42 Valley Of The Sun Dr, Fairplay, CO 80440', 'country': 'US'}
}}

IMPORTANT: Use ONLY these tested fields in the query:
- Core fields (SAFE): preciselyID, addressNumber, streetName, city, admin1ShortName, postalCode
- Do NOT add: latitude, longitude, fips, geographyID, propertyType (may cause 400 errors)
- Stick to the example query structure for best results""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "GraphQL query object with 'query' and 'variables' fields"}
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="get_parcel_by_owner_detailed",
        description="""Get parcel information by owner using GraphQL query. Query by PreciselyID, address, or coordinates.
        
Example request (by PreciselyID):
{'data': {
  'query': 'query GetParcelByOwner($id: String, $queryType: QueryType, $address: String, $distance: Float, $limit: Int) { getParcelByOwner(id: $id, queryType: $queryType, address: $address, distance: $distance, limit: $limit) { parcels { metadata { pageNumber pageCount totalPages count vintage } data { parcelID fips geographyID apn parcelArea longitude latitude elevation } } } }',
  'variables': {'id': 'P0000GL41OME', 'queryType': 'PRECISELY_ID', 'address': 'Boston, MA', 'distance': 1000.0, 'limit': 50}
}}

Query types: PRECISELY_ID, ADDRESS, LOCATION

IMPORTANT: Use ONLY these tested fields in the parcels data section:
- Core fields (SAFE): parcelID, fips, geographyID, apn, parcelArea, longitude, latitude, elevation
- Always include metadata section: pageNumber, pageCount, totalPages, count, vintage
- Stick to the example query structure for best results""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "GraphQL query with variables: id (string), queryType (PRECISELY_ID|ADDRESS|LOCATION), address (string), distance (float), limit (int)"}
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="get_address_family",
        description="""Get related addresses for a given PreciselyID using GraphQL query.
        
Example request:
{'data': {
  'query': 'query GetAddressFamily($id: String!, $queryType: QueryType!) { getById(id: $id, queryType: $queryType) { addresses { data { preciselyID addressFamily(pageNumber: 1, pageSize: 20) { metadata { pageNumber pageCount totalPages count vintage } data { preciselyID addressNumber streetName city admin1ShortName postalCode } } } } } }',
  'variables': {'id': 'P0000GL41OME', 'queryType': 'PRECISELY_ID'}
}}

Query types: PRECISELY_ID (required)
Returns: All addresses related to the same property/location

IMPORTANT: Use ONLY these tested fields in the addressFamily data section:
- Core fields (SAFE): preciselyID, addressNumber, streetName, city, admin1ShortName, postalCode
- Always include metadata section: pageNumber, pageCount, totalPages, count, vintage
- Stick to the example query structure for best results""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "GraphQL query with variables: id (string, required), queryType (must be 'PRECISELY_ID')"}
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="get_serviceability",
        description="""Get broadband/utility serviceability information using GraphQL query.
        
Example request:
{'data': {
  'query': 'query GetServiceability($address: String!, $country: String) { getByAddress(address: $address, country: $country) { addresses(pageNumber: 1, pageSize: 1) { data { preciselyID serviceability { metadata { pageNumber pageCount totalPages count vintage } data { serviceabilityID preciselyID serviceableAddress } } } } } }',
  'variables': {'address': '2755 Milwaukee St, Denver, 80238 CO', 'country': 'US'}
}}

Returns: Broadband and utility service availability at the address

IMPORTANT: Use ONLY these tested fields in the serviceability data section:
- Core fields (SAFE): serviceabilityID, preciselyID, serviceableAddress
- Always include metadata section: pageNumber, pageCount, totalPages, count, vintage
- Stick to the example query structure for best results""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "GraphQL query with variables: address (string), country (string, default 'US')"}
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="get_places_by_address",
        description="""Get places (points of interest) by address using GraphQL query.
        
Example request:
{'data': {
  'query': 'query GetPlacesByAddress($address: String!, $country: String) { getByAddress(address: $address, country: $country) { places(pageNumber: 1, pageSize: 20) { metadata { pageNumber pageCount totalPages count vintage } data { PBID pointOfInterestID preciselyID parentPreciselyID businessName brandName tradeName franchiseName countryIsoAlpha3Code localityName city admin2 admin1 admin1ShortName addressNumber streetName postalCode formattedAddress addressLine1 addressLine2 longitude latitude georesult { value description } georesultConfidence { value description } countryCallingCode phone fax email web open24Hours { value description } lineOfBusiness sic1 sic2 sic8 sic8Description altIndustryCode { value description } miCode tradeDivision groupName mainClass subClass } } } }',
  'variables': {'address': '123 Main St, Boston, MA 02101', 'country': 'US'}
}}

Returns: Places (points of interest) of the specified address including business information, contact details, and industry codes.

Available fields in places data section:
- Identity: PBID, pointOfInterestID, preciselyID, parentPreciselyID
- Business: businessName, brandName, tradeName, franchiseName
- Location: countryIsoAlpha3Code, localityName, city, admin2, admin1, admin1ShortName
- Address: addressNumber, streetName, postalCode, formattedAddress, addressLine1, addressLine2
- Coordinates: longitude, latitude
- Georesult: georesult { value description }, georesultConfidence { value description }
- Contact: countryCallingCode, phone, fax, email, web
- Hours: open24Hours { value description }
- Industry: lineOfBusiness, sic1, sic2, sic8, sic8Description, altIndustryCode { value description }, miCode, tradeDivision, groupName, mainClass, subClass
- Always include metadata section: pageNumber, pageCount, totalPages, count, vintage""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "GraphQL query with variables: address (string, required), country (string, default 'US')"}
            },
            "required": ["data"]
        }
    ),
]

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all 49 Precisely API tools"""
    return TOOLS

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Execute Precisely API tool by calling the corresponding method from the core module
    """
    try:
        # Get the method from PreciselyAPI class
        if not hasattr(precisely_api, name):
            return [TextContent(type="text", text=f'{{"error": "Unknown tool: {name}"}}')]
        
        method = getattr(precisely_api, name)
        
        # Call the method with unpacked arguments
        # The core API methods are synchronous, so we run them in executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: method(**arguments))
        
        # Return result as JSON string
        import json
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f'{{"error": "{str(e)}"}}')]

# ============================================
# TRANSPORT: STDIO (default)
# ============================================
async def run_stdio():
    """Run the server using stdio transport (for Claude Desktop, VS Code, etc.)"""
    logger.info("Starting Precisely MCP Server with stdio transport")
    logger.info(f"49 tools available")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


# ============================================
# TRANSPORT: STREAMABLE HTTP
# ============================================
def create_http_app(json_response: bool = True, stateless: bool = True) -> "Starlette":
    """
    Create a Starlette app with Streamable HTTP transport.
    
    Args:
        json_response: If True, return JSON responses. If False, use SSE streams.
        stateless: If True, no session persistence (recommended for scalability).
    
    Returns:
        Starlette ASGI application
    """
    if not HTTP_AVAILABLE:
        raise ImportError(
            "HTTP transport requires additional dependencies. "
            "Install with: pip install starlette uvicorn sse-starlette"
        )
    
    # Create session manager wrapping our Server instance
    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,  # Set to EventStore impl for resumability
        json_response=json_response,
        stateless=stateless,
    )

    # ASGI handler that delegates to session manager
    async def handle_streamable_http(scope: "Scope", receive: "Receive", send: "Send") -> None:
        await session_manager.handle_request(scope, receive, send)

    # Lifespan context manager for proper startup/shutdown
    @contextlib.asynccontextmanager
    async def lifespan(starlette_app: "Starlette") -> "AsyncIterator[None]":
        async with session_manager.run():
            logger.info("Streamable HTTP server started")
            try:
                yield
            finally:
                logger.info("Streamable HTTP server shutting down")

    # Create Starlette app
    starlette_app = Starlette(
        debug=False,
        routes=[
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,
    )

    return starlette_app


def run_http(host: str = "127.0.0.1", port: int = 8000):
    """Run the server using Streamable HTTP transport."""
    logger.info(f"Starting Precisely MCP Server with HTTP transport")
    logger.info(f"Endpoint: http://{host}:{port}/mcp")
    logger.info(f"49 tools available")
    
    starlette_app = create_http_app(
        json_response=True,  # Simpler client integration
        stateless=True,      # Better scalability
    )
    
    uvicorn.run(starlette_app, host=host, port=port, log_level="info")


# ============================================
# MAIN ENTRY POINT
# ============================================
def main():
    """Main entry point with transport selection."""
    parser = argparse.ArgumentParser(
        description="Precisely MCP Server - Location Intelligence APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # stdio transport (default, for Claude Desktop)
  python precisely_wrapper_server.py

  # HTTP transport (for LangChain, LlamaIndex, web clients)
  python precisely_wrapper_server.py --transport http --port 8000

  # HTTP with custom host (for remote access)
  python precisely_wrapper_server.py --transport http --host 0.0.0.0 --port 8080
"""
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type: stdio (default) or http"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP host (default: 127.0.0.1, use 0.0.0.0 for remote access)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP port (default: 8000)"
    )
    
    args = parser.parse_args()
    
    if args.transport == "http":
        run_http(host=args.host, port=args.port)
    else:
        asyncio.run(run_stdio())


if __name__ == "__main__":
    main()
