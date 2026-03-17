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
from mcp.types import Tool, TextContent, ImageContent
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

# Tool definitions (71 tools covering all Precisely APIs)
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
    # ========================================
    # Spatial Analysis APIs (7 tools)
    # ========================================
    Tool(
        name="find_nearest_candidates",
        description="""Identifies the nearest locations or points of interest to a specified geometry or address based on distance or defined criteria, returning the spatial features in distance order with the distance value.

Returns: GeoJSON FeatureCollection with features sorted by distance, including distance values, response parameters (recordsMatched, recordsReturned), and metadata.

Example 1 Request (Geometry):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'attributes': ['incremental_s_no', 'state', 'wr_id'], 'location': {'format': 'wkt', 'value': 'LINESTRING (-122.769499 38.005947, -122.773625 37.999047)'}, 'withinDistance': '10 mi', 'distanceAttributeName': 'dist', 'maxFeatures': '5', 'inputPointAttributeName': 'inputPoint', 'targetPointAttributeName': 'targetPoint', 'bearingAttributeName': 'bearing'}

Example 2 Request (Address):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'attributes': ['incremental_s_no', 'state', 'wr_id'], 'location': {'format': 'address', 'value': 'POINT REYES STATION CA', 'country': 'United States'}, 'withinDistance': '10 mi', 'distanceAttributeName': 'dist', 'maxFeatures': '5', 'inputPointAttributeName': 'inputPoint', 'targetPointAttributeName': 'targetPoint', 'bearingAttributeName': 'bearing'}""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the table containing spatial data (e.g., '/risks/flood_risk')"},
                "attributes": {"type": "array", "items": {"type": "string"}, "description": "Comma separated list of column names of enrich table to be included in the response. '*' can be used to specify all columns, will only include scalar columns."},
                "location": {"type": "object", "description": "Input geometry or address for spatial analysis. Supported formats: wkt, geojson, lonlat, address. If format is 'address', country field is mandatory."},
                "withinDistance": {"type": "string", "description": "Distance within which nearest features will be searched (e.g., '10 mi', '5 km')"},
                "distanceAttributeName": {"type": "string", "description": "Custom name of distance parameter."},
                "maxFeatures": {"type": "integer", "description": "Maximum number of features returned against each geometry. Default value is 10 and minimum value is 1.", "default": 10, "minimum": 1},
                "uomAttributeName": {"type": "string", "description": "Custom name of unit of measurement parameter."},
                "inputPointAttributeName": {"type": "string", "description": "Custom name of point on input from which distance is calculated."},
                "targetPointAttributeName": {"type": "string", "description": "Custom name of point on target from which distance is calculated."},
                "bearingAttributeName": {"type": "string", "description": "Custom name of bearing angle between input and target point."},
                "attributeFilter": {"type": "string", "description": "specifies filter on scalar attributes"},
                "sortBy": {"type": "string", "description": "Column name to sort by."},
                "sortOrder": {"type": "string", "description": "Sort order: 'ASC' or 'DESC'."},
                "limit": {"type": "integer", "description": "Specifies the maximum number of results to return."},
                "offset": {"type": "integer", "description": "Specifies the number of records to skip."}
            },
            "required": ["tableName", "location", "withinDistance", "attributes"]
        }
    ),
    Tool(
        name="search_at_location",
        description="""Searches for locations or points of interest within or intersecting a defined geographic area(geometry or address) or a buffer around a specified location.

Returns: GeoJSON FeatureCollection with matching features, response parameters (recordsMatched, recordsReturned), and metadata.

Example 1 Request (Geometry):
{'spatialOperation': 'WITHIN', 'tableName': '/risks/flood_risk', 'attributes': ['statecode', 'type', 'mapname', 'incremental_s_no'], 'location': {'format': 'wkt', 'value': 'MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211)))'}, 'bufferDistance': '10 mi'}

Example 2 Request (Address):
{'spatialOperation': 'WITHIN', 'tableName': '/properties/parcels', 'attributes': ['prclid'], 'location': {'format': 'address', 'value': '1 GLOBAL VW, TROY NY 12180-8371, UNITED STATES OF AMERICA', 'country': 'USA'}, 'bufferDistance': '1 km'}""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the table containing spatial data (e.g., '/risks/flood_risk')"},
                "attributes": {"type": "array", "items": {"type": "string"}, "description": "Comma separated list of column names of enrich table to be included in the response. '*' can be used to specify all columns, will only include scalar columns."},
                "location": {"type": "object", "description": "Input geometry or address for spatial analysis. Supported formats: wkt, geojson, lonlat, address. If format is 'address', country field is mandatory."},
                "spatialOperation": {"type": "string", "description": "Spatial operation to perform. Supported values: intersects, within, contains. Default is 'intersects'."},
                "bufferDistance": {"type": "string", "description": "Distance by which the input geometry will be extrapolated (e.g., '100 m', '2 km')."},
                "attributeFilter": {"type": "string", "description": "specifies filter on scalar attributes"},
                "sortBy": {"type": "string", "description": "Column name to sort by."},
                "sortOrder": {"type": "string", "description": "Sort order: 'ASC' or 'DESC'."},
                "limit": {"type": "integer", "description": "Specifies the maximum number of results to return."},
                "offset": {"type": "integer", "description": "Specifies the number of records to skip."}
            },
            "required": ["tableName", "attributes", "location"]
        }
    ),
    Tool(
        name="overlap",
        description="""Identifies spatial intersections between a specified geometry or address in a chosen Enrich spatial table returning the overlap geometry with the percentage and area of overlap.

Returns: GeoJSON FeatureCollection with overlap geometry, intersection area/length, and percentage of overlap with both target and input geometries.

Example 1 Request (Geometry):
{'tableName': '/risks/historical_weather_hurricanelines_world', 'uom': 'mi', 'attributes': ['stormname', 'windspeed'], 'location': {'format': 'wkt', 'value': 'POLYGON ((-74.286804 40.515887, -74.292297 40.478292, -73.66333 40.560765, -73.737488 40.839788, -74.002533 40.909361, -74.286804 40.515887))'}, 'totalAttributeName': 'tc'}

Example 2 Request (Address):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'uom': 'mi', 'attributes': ['state', 'riskdesc'], 'location': {'format': 'address', 'value': '1 Global View Troy NY', 'country': 'USA'}, 'bufferDistance': '5 km'}""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the table containing spatial data (e.g., '/properties/buildings', '/risks/flood_risk')"},
                "attributes": {"type": "array", "items": {"type": "string"}, "description": "Comma separated list of column names of enrich table to be included in the response. '*' can be used to specify all columns; will only include scalar columns."},
                "location": {"type": "object", "description": "Input geometry or address for spatial analysis. Supported formats: wkt, geojson, lonlat, address. If format is 'address', country field is mandatory."},
                "uom": {"type": "string", "description": "Unit of measurement used to return intersection length/area (e.g., 'm')"},
                "areaAttributeName": {"type": "string", "default": "intersectionArea", "description": "Custom name of intersection area parameter when intersection area is polygon. Default: 'intersectionArea'."},
                "lengthAttributeName": {"type": "string", "default": "intersectionLength", "description": "Custom name of intersection length parameter when intersection area is linestring. Default: 'intersectionLength'."},
                "percentTargetAttributeName": {"type": "string", "default": "percentageOfTarget", "description": "Custom name of parameter indicating percentage of overlap with target geometry. Default: 'percentageOfTarget'."},
                "percentInputAttributeName": {"type": "string", "default": "percentageOfInput", "description": "Custom name of parameter indicating percentage of overlap with input geometry. Default: 'percentageOfInput'."},
                "uomAttributeName": {"type": "string", "default": "uom", "description": "Custom name of unit of measurement parameter. Default: 'uom'."},
                "bufferDistance": {"type": "string", "description": "Distance by which the input geometry will be extrapolated (e.g., '100 m', '2 km')."},
                "attributeFilter": {"type": "string", "description": "specifies filter on scalar attributes"},
                "limit": {"type": "integer", "description": "Specifies the maximum number of results to return."},
                "offset": {"type": "integer", "description": "Specifies the number of records to skip."}
            },
            "required": ["tableName", "attributes", "location", "uom"]
        }
    ),
    Tool(
        name="get_spatial_products",
        description="""Get a list of available Enrich Data products along with their metadata such as product family, applicable geographic area, vintage, available layers, appropriate zoom levels for display and styles to use.

Returns: List of product metadata objects with productId, productName, productFamily, vintage, geography, and layers (including layerId, displayName, featureTable, recommendedStyle).

Example Request: https://api.cloud.precisely.com/v1/spatial/products""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="list_spatial_tables",
        description="""This endpoint retrieves a list of spatial tables from database.

Returns: List of spatial table names available in the database.

Example Request: https://api.cloud.precisely.com/v1/spatial/tables""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="get_table_metadata",
        description="""This endpoint retrieves a metadata information of a specific/given table from database.

Returns: Object with table name, columns and their description and type, bounding box in case of spatial table, and row count.

Example Request: https://api.cloud.precisely.com/v1/spatial/tables/properties/buildings/metadata""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the table for which the metadata needs to be described (e.g., 'properties/buildings', 'risks/flood_risk')"}
            },
            "required": ["tableName"]
        }
    ),
    Tool(
        name="summarize",
        description="""Generates detailed data summaries within a user defined region(geometry or address), including total, average, minimum and maximum values for data such as population.

Returns: Summary statistics with aggregate values (min, max, avg, sum, median) for specified columns within the defined region.

Example 1 Request (Geometry, Intersects):
{'spatialOperation': 'INTERSECTS', 'tableName': '/risks/historical_weather_windgrid', 'aggregateColumns': {'w9': ['min', 'max', 'avg', 'sum']}, 'location': {'format': 'wkt', 'value': 'GEOMETRYCOLLECTION (MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211))), LINESTRING (-121.756899 37.653383, -121.158302 37.304645, -121.690998 37.120906))'}, 'proportionalCalculation': true}

Example 2 Request (Address, Intersects):
{'spatialOperation': 'INTERSECTS', 'tableName': '/risks/flood_risk', 'location': {'format': 'address', 'value': '1 Global View Troy NY', 'country': 'USA'}, 'aggregateColumns': {'id': ['min', 'max', 'avg', 'sum']}, 'proportionalCalculation': true, 'bufferDistance': '10 km'}

Example 3 Request (Geometry, Within):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'location': {'format': 'WKT', 'value': 'POLYGON ((-122.766919 38.031512, -122.766919 38.051864, -122.741314 38.051864, -122.741314 38.031512, -122.766919 38.031512))'}, 'spatialOperation': 'within', 'proportionalCalculation': false, 'aggregateColumns': {'INTENSITY': ['min', 'MAX', 'avg', 'sum', 'MEDIAN'], 'DAMAGE': ['min', 'max', 'SUM', 'avg', 'MEDIAN']}}

Example 4 Request (Address, Within):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'location': {'format': 'address', 'value': '1 Global View Troy NY', 'country': 'USA'}, 'spatialOperation': 'within', 'proportionalCalculation': false, 'bufferDistance': '10 km', 'aggregateColumns': {'INTENSITY': ['min', 'MAX', 'avg', 'sum', 'MEDIAN'], 'DAMAGE': ['min', 'max', 'SUM', 'avg', 'MEDIAN']}}""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the table containing spatial data (e.g., '/risks/historical_weather_windgrid')"},
                "aggregateColumns": {"type": "object", "description": "Dictionary of column names mapped to lists of aggregate functions. Supported functions: min, max, avg, sum, median."},
                "location": {"type": "object", "description": "Input geometry or address for spatial analysis. Supported formats: wkt, geojson, lonlat, address. If format is 'address', country field is mandatory."},
                "spatialOperation": {"type": "string", "description": "Spatial operation to perform. Supported values: intersects, within. Default value is 'intersects'."},
                "proportionalCalculation": {"type": "boolean", "description": "Whether to use proportional calculation. Only applicable when the spatialOperation parameter is 'intersects'"},
                "bufferDistance": {"type": "string", "description": "Distance by which the input geometry will be extrapolated (e.g., '100 m', '2 km')."},
                "attributeFilter": {"type": "string", "description": "specifies filter on scalar attributes"}
            },
            "required": ["tableName", "location", "aggregateColumns"]
        }
    ),
    # ========================================
    # OGC Features APIs (10 tools)
    # ========================================
    Tool(
        name="ogc_landing_page",
        description="""The landing page provides links to essential API resources, including:
- **API Definition:** A machine-readable specification of the API.
- **Conformance Declaration:** A list of standards that the API conforms to.
- **Feature Collections:** Information and links to the available feature collections in the dataset.

Use this endpoint to quickly navigate and explore the API's capabilities.

Returns: Object with links array.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_api_definition",
        description="""This endpoint retrieves the complete OpenAPI definition for the API. The response is a machine-readable specification that describes all available endpoints, request/response schemas, and security configurations.

- **Format:** The API definition conforms to the OpenAPI 3.0.1 standard.

Returns: OpenAPI 3.0.1 specification document describing all available endpoints.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/api""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_functions",
        description="""This endpoint returns a list of available spatial functions within the API.
- **Purpose:** Provides supported spatial functions that can be used for querying features.
- **Function Metadata:** Includes function names, argument types, and return types.

Returns: List of available spatial functions with function names, argument types, and return types.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/functions""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_conformance",
        description="""This endpoint returns the conformance declaration for the API. The conformance declaration is a list of all conformance classes specified in a standard that the server adheres to. It helps clients determine whether the API meets the required standards and their own requirements.

- **Purpose:** Provides a comprehensive list of conformance classes to verify the API's compliance with OGC API standards and additional specifications.
- **Standards:** Includes OGC API conformance classes and any extra specifications the API supports.

Returns: Conformance declaration listing all conformance classes the server adheres to.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/conformance""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_collections",
        description="""This endpoint returns the list of feature collections available on the server. Each collection represents a spatial dataset that can be queried and provides essential metadata, including:

- **Collection ID:** A unique identifier for the spatial dataset.
- **Title and Description:** Optional details that describe the collection.
- **Spatial and Temporal Extents:** Indicators of the geographical and time-based coverage of the data.
- **Coordinate Reference Systems (CRS):** A list of supported CRS, with the first being the default (typically WGS 84).
- **Links:** Navigational links to access the collection’s items (e.g., `/collections/{collectionId}/items`).

This resource is designed to help clients discover available geospatial datasets and understand the structure of each collection before making queries.

Returns: List of feature collections with metadata including collection IDs, titles, descriptions, and links.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_collection",
        description="""This resource describes the feature collection identified in the path.

Information about the feature collection with id `{collectionId}` is provided. The response contains:

- A link to the items in the collection (path `/collections/{collectionId}/items`, relation: items).
- A unique local identifier for the collection.
- A list of coordinate reference systems (CRS) in which geometries may be returned; the first CRS is the default (typically WGS 84 with axis order longitude/latitude).
- An optional title and description for the collection.
- An optional spatial and temporal extent derived from the data.
- An optional indicator of the item type (default is 'feature').

Returns: Collection metadata including id, title, description, and links to items/schema.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "Unique identifier of the collection (e.g., 'properties/buildings')"}
            },
            "required": ["collectionId"]
        }
    ),
    Tool(
        name="ogc_collection_schema",
        description="""This resource provides the schema for a specified feature collection. The schema defines the structure of the collection and includes details such as field names, data types, formats, and descriptions.

The **collection id** is a unique identifier used to reference a specific dataset. When you provide a collection id, the response includes:

- **Field Names:** Names of each attribute in the collection.
- **Data Types & Formats:** The expected data type (e.g., string, integer, double) and format for each field.
- **Descriptions:** Explanatory details for each attribute to clarify its purpose.
- **Geospatial Data Types:** Specific spatial types for any geospatial attributes, along with the default coordinate reference system.

This information is essential for validating client queries and constructing dynamic interfaces.

Returns: JSON describing the collection structure with field names, data types, formats, and descriptions.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/schema""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "Unique identifier of the collection (e.g., 'properties/buildings')"}
            },
            "required": ["collectionId"]
        }
    ),
    Tool(
        name="ogc_collection_queryables",
        description="""This resource returns the queryable properties for a specific collection identified by its unique id. Queryable properties provide detailed metadata for each attribute available in the collection that can be used to filter queries. The response includes information such as:

- **Field Names:** The names of the attributes in the collection.
- **Descriptions:** A description of each attribute to clarify its purpose and usage.
- **Formats:** The data types or formats (e.g., string, number, geospatial) of each attribute.
- **Geospatial Data Types:** Specific spatial types for attributes that support geospatial queries.

This metadata is essential for clients to build dynamic query interfaces and validate their requests against the collection's schema.

Returns: Queryable properties with metadata for each filterable attribute in the collection.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/queryables""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "Unique identifier of the collection (e.g., 'properties/buildings')"}
            },
            "required": ["collectionId"]
        }
    ),
    Tool(
        name="ogc_collection_items",
        description="""Fetch features of the feature collection with id `{collectionId}`.

Every feature in a dataset belongs to a collection. A dataset may consist of multiple feature collections, each representing a group of features that share a common schema and type.

The **collection id** is a unique identifier for the spatial dataset and is used to reference a specific collection within the API.

Additional capabilities include:
- **Filtering:** Supports attribute-based filtering using CQL (Common Query Language).
- **Pagination:** Use `limit` and `offset` parameters to paginate results.
- **Spatial Queries:**
  - **Bounding Box (bbox):** Retrieve features within a rectangular spatial extent (`minX, minY, maxX, maxY`).
  - **Spatial Filters:** Support for `contains`, `intersects`, and `within` (OGC Filter Encoding).

Returns: GeoJSON FeatureCollection with features matching the query, and pagination links.

Example 1 Request (Items without additional parameters): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items

Example 2 Request (Items with limit): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?limit=5

Example 3 Request (Items with offset): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?limit=5&offset=10

Example 4 Request (Items with bbox): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?bbox=-74.013219,40.702976,-74.01162,40.70357&limit=100

Example 5 Request (Items with filter and s_contains): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?filter=s_contains(GEOM,POINT (-74.011728 40.701114))&limit=100

Example 6 Request (Items with filter and s_within): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?filter=s_within(GEOM,POLYGON ((-74.009523 40.703347, -74.010445 40.704257, -74.011078 40.704062, -74.011127 40.703363, -74.010526 40.702822, -74.009523 40.703347)))&limit=100

Example 7 Request (Items with filter and s_intersects): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?filter=s_intersects(GEOM,POLYGON ((-74.009523 40.703347, -74.010445 40.704257, -74.011078 40.704062, -74.011127 40.703363, -74.010526 40.702822, -74.009523 40.703347)))&limit=100

Example 8 Request (Items with filter and = operator): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?filter=bldgid%3D'B000CTPA4MY1'""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "The unique identifier for the feature collection (e.g., 'properties/buildings')"},
                "limit": {"type": "string", "description": "Number of features to return. Default: 10."},
                "offset": {"type": "string", "description": "Number of features to skip. Default: 0."},
                "bbox": {"type": "string", "description": "Bounding box for spatial filtering (minX, minY, maxX, maxY) (e.g., '-74.2,40.8,-73.9,40.9')"},
                "filter": {"type": "string", "description": "Filter query in CQL format. (e.g., type = 'residential'"}
            },
            "required": ["collectionId"]
        }
    ),
    Tool(
        name="ogc_feature_by_id",
        description="""Retrieves a single feature in GeoJSON format,

Returns: GeoJSON FeatureCollection with geometry and properties of the feature(s).

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items/1""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "The unique identifier for the feature collection (e.g., 'properties/buildings')"},
                "featureId": {"type": "string", "description": "The unique identifier for the feature within the collection (e.g., '1')"}
            },
            "required": ["collectionId", "featureId"]
        }
    ),
    # ========================================
    # WMS (Web Map Service) APIs (2 tools)
    # ========================================
    Tool(
        name="wms_get_request",
        description="""Processes WMS requests: GetCapabilities, GetMap, GetFeatureInfo.

Returns: For GetMap success: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int). For GetCapabilities success: Dict with 'xml' (str), 'content_type' (str). For GetFeatureInfo success: JSON dict. On any error (auth, invalid params, or WMS ServiceException): Dict with 'error' (str) containing the error or ServiceExceptionReport XML.

Example 1 GetCapabilities Request:
https://api.cloud.precisely.com/v1/Spatial/WMS?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetCapabilities

Example 2 GetMap Request (WMS version 1.1.1, SRS parameter for EPSG:4326, Axis order lon-lat for BBOX):
https://api.cloud.precisely.com/v1/Spatial/WMS?VERSION=1.1.1&SERVICE=WMS&REQUEST=GetMap&SRS=EPSG:4326&BBOX=-30,20,50,80&WIDTH=400&HEIGHT=300&Layers=World&STYLES=AreaStyleGreen&FORMAT=image/png

Example 3 GetMap Request (WMS version 1.3.0, CRS parameter for CRS:84, Axis order lon-lat for BBOX):
https://api.cloud.precisely.com/v1/Spatial/WMS?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetMap&CRS=CRS:84&BBOX=-30,20,50,80&WIDTH=400&HEIGHT=300&Layers=World&STYLES=AreaStyleGreen&FORMAT=image/png

Example 4 GetMap Request (WMS version 1.3.0, CRS parameter for EPSG:4326, Axis order lat-lon for BBOX):
https://api.cloud.precisely.com/v1/Spatial/WMS?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetMap&CRS=EPSG:4326&BBOX=20,-30,80,50&WIDTH=400&HEIGHT=300&Layers=World&STYLES=AreaStyleGreen&FORMAT=image/png

Example 5 GetFeatureInfo Request:
https://api.cloud.precisely.com/v1/spatial/wms?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetFeatureInfo&CRS=EPSG:4326&BBOX=29.19367847889249035,-98.56156199862394374,29.35037762857998089,-98.33146912069426548&WIDTH=400&HEIGHT=300&LAYERS=wildfire_risk&INFO_FORMAT=application/json&QUERY_LAYERS=wildfire_risk&I=1&J=1&PIXELSEARCHRADIUS=10""",
        inputSchema={
            "type": "object",
            "properties": {
                "REQUEST": {"type": "string", "description": "The WMS request type: GetCapabilities, GetMap, or GetFeatureInfo"},
                "SERVICE": {"type": "string", "description": "Service type. Always 'WMS'."},
                "VERSION": {"type": "string", "description": "WMS version. Supported: '1.1.1', '1.3.0'."},
                "crs": {"type": "string", "description": "Coordinate reference system (WMS 1.3.0). 'EPSG:3857', 'EPSG:4326' or 'CRS:84'"},
                "srs": {"type": "string", "description": "Spatial reference system (WMS 1.1.1) 'EPSG:3857', 'EPSG:4326' or 'CRS:84'"},
                "BBOX": {"type": "string", "description": "The area to be mapped, specified as four comma-separated numbers: 'min_x,min_y,max_x,max_y'. Order's dependent on SRS or CRS (e.g., '-30,20,50,80')."},
                "width": {"type": "string", "description": "Width of the map image in pixels."},
                "height": {"type": "string", "description": "Height of the map image in pixels."},
                "layers": {"type": "string", "description": "Comma-separated list of layer names to display."},
                "STYLES": {"type": "string", "description": "Comma-separated list of one rendering style per requested layer. A style is required for each layer requested. STYLES=Style1,,Style3"},
                "FORMAT": {"type": "string", "description": "Output format of map image (e.g., 'image/png')."},
                "TRANSPARENT": {"type": "string", "description": "Whether the map background is transparent, 'TRUE' or 'FALSE'. Default is FALSE."},
                "Info_Format": {"type": "string", "description": "Format for GetFeatureInfo response (e.g., 'application/json')."},
                "QUERY_LAYERS": {"type": "string", "description": "Comma-separated list of layers to query for GetFeatureInfo."},
                "I": {"type": "string", "description": "X pixel coordinate for GetFeatureInfo (WMS 1.3.0)."},
                "J": {"type": "string", "description": "Y pixel coordinate for GetFeatureInfo (WMS 1.3.0)."},
                "X": {"type": "string", "description": "X pixel coordinate for GetFeatureInfo (WMS 1.1.1)."},
                "Y": {"type": "string", "description": "Y pixel coordinate for GetFeatureInfo (WMS 1.1.1)."},
                "Feature_Count": {"type": "string", "description": "Maximum number of features returned for GetFeatureInfo."},
                "PIXELSEARCHRADIUS": {"type": "string", "description": "Pixel search radius for GetFeatureInfo."},
                "BGCOLOR": {"type": "string", "description": "Background color for the map image."},
                "RESOLUTION": {"type": "string", "description": "Resolution of the map image."},
                "EXCEPTIONS": {"type": "string", "description": "Format for exception reporting."}
            },
            "required": ["REQUEST", "SERVICE", "VERSION"]
        }
    ),
    Tool(
        name="wms_post_get_map",
        description="""Processes WMS GetMap requests using a POST method. Accepts SLD_BODY as a form parameter (URL-encoded JSON).

Returns: On success: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int). On any error (auth, invalid params, or WMS ServiceException): Dict with 'error' (str) containing the error or ServiceExceptionReport XML.

Example 1 Post Request for one layer:
POST https://api.cloud.precisely.com/v1/spatial/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=37.78662956646336823%2C-122.2745967175037549%2C37.81410536165775227%2C-122.2403683391127061&CRS=EPSG%3A4326&WIDTH=1062&HEIGHT=853&LAYERS=buildings&STYLES=&FORMAT=image%2Fpng&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&TRANSPARENT=TRUE
Content-Type: application/x-www-form-urlencoded
BODY: SLD_BODY=<URL-encoded JSON style definition>

Example 2 Post Request for two layers:
POST https://api.cloud.precisely.com/v1/spatial/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=37.78662956646336823%2C-122.2745967175037549%2C37.81410536165775227%2C-122.2403683391127061&CRS=EPSG%3A4326&WIDTH=1062&HEIGHT=853&LAYERS=buildings,address_fabric&STYLES=&FORMAT=image%2Fpng&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&TRANSPARENT=TRUE
Content-Type: application/x-www-form-urlencoded
BODY: SLD_BODY=<URL-encoded JSON style definition for multiple layers>""",
        inputSchema={
            "type": "object",
            "properties": {
                "REQUEST": {"type": "string", "description": "The WMS request type. Always 'GetMap' for this endpoint."},
                "SERVICE": {"type": "string", "description": "Service type. Always 'WMS'."},
                "VERSION": {"type": "string", "description": "WMS version (e.g., '1.3.0')."},
                "crs": {"type": "string", "description": "Coordinate reference system (e.g., 'EPSG:4326', 'CRS:84')."},
                "BBOX": {"type": "string", "description": "Bounding box coordinates."},
                "width": {"type": "string", "description": "Width of the map image in pixels."},
                "height": {"type": "string", "description": "Height of the map image in pixels."},
                "layers": {"type": "string", "description": "Comma-separated list of layer names."},
                "STYLES": {"type": "string", "description": "Comma-separated list of style names."},
                "FORMAT": {"type": "string", "description": "Output format (e.g., 'image/png')."},
                "TRANSPARENT": {"type": "string", "description": "Whether the map background is transparent ('TRUE' or 'FALSE')."},
                "SLD_BODY": {"type": "string", "description": "Proprietary Precisely JSON style definition for customizing layer appearance. URL-encoded when sent."},
            },
            "required": ["REQUEST", "SERVICE", "VERSION", "crs", "BBOX", "width", "height", "layers", "FORMAT"]
        }
    ),
    # ========================================
    # WMTS (Web Map Tile Service) APIs (3 tools)
    # ========================================
    Tool(
        name="wmts_request",
        description="""Use the appropriate parameters based on the request type.

This tool handles WMTS operations via the KVP (Key-Value Pair) query parameter interface. Use Request=GetCapabilities to retrieve the service XML document listing all available layers, tile matrix sets, zoom levels, and supported formats. Use Request=GetTile to retrieve a map tile image by specifying Layer, Style, TileMatrixSet, TileMatrix, TileRow, TileCol, and Format.

Returns: For GetCapabilities: Dict with 'xml' (str) containing the capabilities XML document and 'content_type' (str). For GetTile: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).

Example 1 GetCapabilities Request:
https://api.cloud.precisely.com/v1/spatial/wmts?SERVICE=WMTS&REQUEST=GetCapabilities&ACCEPTVERSIONS={version}""",
        inputSchema={
            "type": "object",
            "properties": {
                "Service": {"type": "string", "description": "Service type. Always 'WMTS'."},
                "Request": {"type": "string", "description": "The WMTS request type: GetCapabilities or GetTile."},
                "Version": {"type": "string", "description": "WMTS version (e.g., '1.0.0')."},
                "Layer": {"type": "string", "description": "Layer name for GetTile request."},
                "Style": {"type": "string", "description": "Style name for GetTile request."},
                "TileMatrixSet": {"type": "string", "description": "Tile matrix set identifier for GetTile request."},
                "TileMatrix": {"type": "string", "description": "Tile matrix (zoom level) for GetTile request."},
                "TileRow": {"type": "integer", "description": "Tile row for GetTile request."},
                "TileCol": {"type": "integer", "description": "Tile column for GetTile request."},
                "Format": {"type": "string", "description": "Output format for GetTile. 'image/png' or 'application/vnd.mapbox-vector-tile'"}
            },
            "required": ["Service", "Request"]
        }
    ),
    Tool(
        name="wmts_get_standard_tile",
        description="""Returns a map tile based on the RESTful encoding for the WMTS service.

Returns: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int) containing the requested map tile.

Example Request: https://api.cloud.precisely.com/v1/spatial/wmts/1.0.0/default/tiles/wildfire_risk/default/WorldWebMercatorQuad_0_to_19/12/1190/1550.png""",
        inputSchema={
            "type": "object",
            "properties": {
                "Version": {"type": "string", "description": "WMTS version (e.g., '1.0.0')."},
                "Layer": {"type": "string", "description": "Layer name (e.g., 'parcels', 'wildfire_risk')."},
                "Style": {"type": "string", "description": "Style name. Comma-separated list of one rendering style per requested layer (e.g., 'default')."},
                "TileMatrixSet": {"type": "string", "description": "Tile matrix set identifier (e.g., 'WorldWebMercatorQuad_0_to_19')."},
                "TileMatrix": {"type": "string", "description": "Tile matrix (zoom level)."},
                "TileCol": {"type": "integer", "description": "Tile column number."},
                "TileRow": {"type": "integer", "description": "Tile row number."},
                "Format": {"type": "string", "description": "Output format. 'png' or 'mvt'"}
            },
            "required": ["Version", "Layer", "Style", "TileMatrixSet", "TileMatrix", "TileCol", "TileRow", "Format"]
        }
    ),
    Tool(
        name="wmts_get_simple_tile",
        description="""Returns a map tile based on the RESTful encoding for the WMTS service.

Use this tool when you do NOT need to specify Style or TileMatrixSet.

Returns: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int) containing the requested map tile.

Example Request: https://api.cloud.precisely.com/v1/spatial/wmts/1.0.0/simpleProfileTile/tiles/wildfire_risk/12/1190/1550.png""",
        inputSchema={
            "type": "object",
            "properties": {
                "Version": {"type": "string", "description": "WMTS version (e.g., '1.0.0')."},
                "Layer": {"type": "string", "description": "Layer name (e.g., 'parcels', 'wildfire_risk')."},
                "TileMatrix": {"type": "string", "description": "Tile matrix (zoom level)."},
                "TileCol": {"type": "integer", "description": "Tile column number."},
                "TileRow": {"type": "integer", "description": "Tile row number."},
                "Format": {"type": "string", "description": "Output format. 'png' or 'mvt'"}
            },
            "required": ["Version", "Layer", "TileMatrix", "TileCol", "TileRow", "Format"]
        }
    ),
]

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all 71 Precisely API tools"""
    return TOOLS

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent]:
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
        
        # Handle image/binary responses (Maps & Tiling APIs)
        if isinstance(result, dict) and result.get("image_base64"):
            return [ImageContent(
                type="image",
                data=result["image_base64"],
                mimeType=result.get("content_type", "image/png")
            )]
        
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
    logger.info(f"71 tools available")
    
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
    logger.info(f"71 tools available")
    
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
