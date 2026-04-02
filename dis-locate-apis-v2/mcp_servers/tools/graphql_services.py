"""
GraphQL Services Tools Module
Contains 22 tools for property, demographics, risk, and advanced GraphQL queries
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of GraphQL services tool definitions"""
    return [
    # Property & Risk tools (9 tools)
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
    
    # Demographics & Neighborhoods tools (8 tools)
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

    # Advanced GraphQL tools  (5 tools)
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