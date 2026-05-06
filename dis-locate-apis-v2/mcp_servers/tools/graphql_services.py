"""
GraphQL Services Tools Module
Contains 22 tools for property, demographics, risk, and advanced GraphQL queries
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401

_ADDRESS_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "address": {
            "type": "string",
            "description": "Full street address string (e.g., '2755 Milwaukee St, Denver, CO 80238')."
        },
        "country": {
            "type": "string",
            "description": "Country identifier — accepts ISO 3166-1 alpha-2, alpha-3, numeric, or full name e.g., 'US', 'USA', '840', 'United States'.",
            "default": "US"
        }
    },
    "required": ["address"]
}

_GRAPHQL_DATA_SCHEMA = {
    "type": "object",
    "description": "GraphQL request payload with 'query' (GraphQL query string) and 'variables' (variable values).",
    "properties": {
        "query": {
            "type": "string",
            "description": "GraphQL query string. Must use only the tested safe fields documented in the tool description."
        },
        "variables": {
            "type": "object",
            "description": "GraphQL variable values matching the variables declared in the query."
        }
    },
    "required": ["query", "variables"]
}


def get_tools() -> list[Tool]:
    """Returns list of GraphQL services tool definitions"""
    return [
    # Property & Risk tools (9 tools)
    Tool(
        name="get_property_data",
        description="""Retrieve a comprehensive consolidated property record for a US address, including property
attributes (size, year built, bedrooms, bathrooms), assessed/market value, building characteristics.
Use this tool when you need a broad property overview in a single call.
Do NOT use if you only need specific attribute categories — use
get_property_attributes_by_address (physical attributes only),
get_replacement_cost_by_address (replacement cost only),
get_buildings_by_address (building footprint/structure only), or
get_parcels_by_address (parcel/land data only) for narrower, faster responses.
Only works for US addresses.

Output: Comprehensive property record with attributes, valuation, building characteristics.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_property_attributes_by_address",
        description="""Retrieve physical property attributes for a US address: bedrooms, bathrooms, square footage,
lot size, year built.
Do NOT use if you need a full property overview — use get_property_data instead.
Do NOT use for valuation data — use get_replacement_cost_by_address instead.
Do NOT use for risk assessments — use the specific risk tools (get_flood_risk_by_address, etc.).
Only works for US addresses.

Output: Object with physical property attributes including bedroom/bathroom counts, square
footage, lot size, year built.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_replacement_cost_by_address",
        description="""Retrieve the estimated replacement cost (cost to rebuild) for a property at a US address,
including a confidence code.
Do NOT use if you need general property attributes — use get_property_attributes_by_address instead.
Do NOT use if you need market/assessed value — replacement cost only reflects reconstruction cost.
Only works for US addresses.

Output: Object with estimated replacement cost value and confidence code.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_flood_risk_by_address",
        description="""Retrieve flood risk assessment data for a US address, including FEMA flood zone classification,
map effective and revision dates, and other risk indicators.
Use this tool when you need to assess flood exposure for a property.
Do NOT use if you need wildfire, fire, earthquake, coastal, or weather risk —
use the corresponding specific risk tool instead.
Only works for US addresses.

Output: Object with FEMA flood zone code, address elevation, distances to 100-year and
500-year flood zones, elevation profile to nearest waterbody, distance to nearest waterbody.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_wildfire_risk_by_address",
        description="""Retrieve wildfire risk assessment data for a US address, including risk rankings, risk
description, and other contributing factor ratings.
Use this tool when you need to assess wildfire exposure for a property.
Do NOT use if you need flood, fire (structural), earthquake, coastal, or weather risk —
use the corresponding specific risk tool instead.
Only works for US addresses.

Output: Object with overall risk ranking, risk description for both baseline and extreme
models, individual component ratings (severity, frequency, damage, community, vegetation,
burn probability, ember risk, proximity factors, etc.) for each model, wildland-urban interface
distance, distances to high/very-high/extreme risk zones, and nearest historical fire
perimeter details.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_property_fire_risk",
        description="""Retrieve fire station proximity data for a US address, including response time and distance
data for the three nearest fire stations. This tool covers fire department proximity and
response times — not wildfire risk.
Do NOT use if you need wildfire risk — use get_wildfire_risk_by_address instead.
Do NOT use if you need flood, earthquake, coastal, or weather risk.
Only works for US addresses.

Output: Object with ID, type, drive times, and drive distance for each of the three nearest
fire stations. Also includes distance to nearest water body in feet.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_earth_risk",
        description="""Retrieve earthquake risk data for a US address, including historical earthquake event counts,
nearest fault details, and seismic site classification.
Use this tool when you need to assess earthquake/seismic exposure for a property.
Do NOT use if you need flood, wildfire, fire (structural), coastal, or weather risk —
use the corresponding specific risk tool instead.
Only works for US addresses.

Output: Object with historical earthquake event counts by magnitude level, nearest fault
distance, type, age etc., and NEHRP site classification and code.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_coastal_risk",
        description="""Retrieve coastal wind and hurricane risk data for a US address, including proximity to
coastline, wind pool territory, and hurricane wind speed/debris classifications.
Use this tool for properties near coastlines where hurricane or coastal wind risk is relevant.
Do NOT use if you need flood zone (FEMA) risk — use get_flood_risk_by_address instead.
Do NOT use if you need wildfire, earthquake, structural fire, or weather risk.
Only works for US addresses.

Output: Object with distance to nearest coastline, nearest waterbody, adjacent waterbody,
wind pool description, hurricane wind speeds, and wind-borne debris zone classifications.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_historical_weather_risk",
        description="""Retrieve historical weather risk data for a US address, including exposure to severe weather
events such as hail, wind, tornado, and hurricane.
Use this tool when you need historical weather hazard information for insurance, underwriting,
or risk profiling.
Do NOT use for flood, wildfire, earthquake, fire protection class, or coastal risk —
use the corresponding specific risk tools instead.
Only works for US addresses.

Output: Object with risk level classifications for hail, tornado, wind, and hurricane event
count and range.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),

    # Demographics & Neighborhoods tools (8 tools)
    Tool(
        name="get_demographics",
        description="""Retrieve a combined demographic profile for a US address, including both PSYTE geodemographic
segmentation and Ground View census demographics. Returns lifestyle segment classification and
key census block group statistics.
Use this tool when you need a broad demographic overview combining both PSYTE and Ground View datasets.
Do NOT use if you only need PSYTE segmentation — use get_psyte_geodemographics_by_address instead.
Do NOT use if you only need Ground View statistics — use get_ground_view_by_address instead.
Do NOT use for crime index, neighborhood names, school data, building, or parcel data.
Only works for US addresses.

Output: Object with PSYTE segment code and description, household income, property value,
adult age, household composition variables from PSYTE, census block group statistics like
average household income, education percentages, average home value, rent.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_crime_index",
        description="""Retrieve national crime index values for a US address, including overall composite, violent
crime and property crime, and their respective level and descriptions.
Use this tool when you need to assess crime risk for a location.
Do NOT use for weather, flood, fire, earthquake, wildfire, or coastal risk —
use the specific risk tools.
Do NOT use for demographic segmentation — use get_demographics or the specific PSYTE/Ground View tools.
Only works for US addresses.

Output: Object with composite, violent crime, and property crime national index values,
and categories, descriptions for each.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_psyte_geodemographics_by_address",
        description="""Retrieve PSYTE geodemographic segment classification for a US address. PSYTE (a Precisely
proprietary segmentation system) classifies neighborhoods into lifestyle and demographic
segments based on income, age, household composition, and lifestyle factors.
Use this tool when you specifically need PSYTE segment data for targeting, analysis, or profiling.
Do NOT use if you also need Ground View market segment data — use get_demographics instead
(returns both PSYTE and Ground View in one call).
Do NOT use for crime, risk, building, parcel, or school data.
Only works for US addresses.

Output: Object with PSYTE segment code, segment name, segment group, and demographic
characteristics for the neighborhood of the input address.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_ground_view_by_address",
        description="""Retrieve Ground View census block group demographic statistics for a US address. Ground View
is a Precisely dataset providing census-derived population, housing, education, employment,
and economic statistics at the census block group level.
Use this tool when you specifically need Ground View demographic statistics.
Do NOT use if you also need PSYTE segment data — use get_demographics instead
(returns both PSYTE and Ground View in one call).
Do NOT use for crime, risk, building, parcel, or school data.
Only works for US addresses.

Output: Object with census block group demographic statistics including population age
distribution percentages, marital status percentages, education percentages, unemployment
rate, owner/renter occupied percentages, average vehicles per household, average rent,
average home value, and average household income.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_neighborhoods_by_address",
        description="""Retrieve neighborhood profile data for a US address, including neighborhood name,
walkability/mobility scores, and real estate market characteristics.
Use this tool when you need neighborhood-level data including mobility scores, property prices,
sales trends, or property type breakdown.
Do NOT use for demographic data — use get_demographics or PSYTE/Ground View tools instead.
Do NOT use for school, building, parcel, or crime data.
Only works for US addresses.

Output: Object with neighborhood name and ID, walkability/bike/transit/drive scores, average
single-family residence price and sales trend direction, average property year built, bedrooms,
bathrooms, living square footage, lot size, pool percentage, single-family residence percentage,
and counts of commercial, single-family, condo, duplex, and apartment properties.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_schools_by_address",
        description="""Retrieve school district, attendance zone, and nearby college information for a US address.
Use this tool when you need to identify which schools and districts serve an address.
Do NOT use for demographic, crime, risk, building, or parcel data.
Only works for US addresses.

Output: Object with three sections: nearby college/university (ID and name), schoolDistrict
(district ID and name), and schoolAttendanceZone (ID and name, where names identify the
assigned K-12 schools). Note: individual school type, enrollment count, grade range, and
distance to school are not returned.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_buildings_by_address",
        description="""Retrieve building data for a US address, including building type, area, elevation, longitude,
latitude, and geography ID.
Use this tool when you need building-level data (type, area, elevation) rather than property
ownership or valuation data.
Do NOT use if you need full property data (ownership, valuation) — use get_property_data instead.
Do NOT use for parcel/land data — use get_parcels_by_address instead.
Only works for US addresses.

Output: Object with building ID, UBID (universal building ID), building type (e.g.,
Residential, Commercial), FIPS code, geography ID, coordinates, elevation, and building area.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_parcels_by_address",
        description="""Retrieve land parcel (lot) data for a US address, including parcel area, APN (Assessor's
Parcel Number), FIPS code, longitude, latitude, and geography ID.
Use this tool when you need parcel/lot identifiers and area rather than building structure
or property ownership information.
Do NOT use if you need full property data (ownership, valuation) — use get_property_data instead.
Do NOT use for building structure data — use get_buildings_by_address instead.
Only works for US addresses.

Output: Object with parcel ID, FIPS code, geography ID, APN, parcel area, coordinates, and
elevation for the parcel at the input address.""",
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),

    # Advanced GraphQL tools (5 tools)
    Tool(
        name="get_addresses_detailed",
        description="""Retrieve detailed address record(s) from the Precisely address database using a custom GraphQL
query. Allows fine-grained control over which address fields to request.
Use this tool when the standard geocode or lookup tools do not return sufficient detail and
you need to construct a custom GraphQL query.
Do NOT use if a simpler tool (geocode, lookup, verify_address) already covers your need.
Only use the safe, tested fields listed below — other fields may cause 400 errors.

Safe fields for the 'addresses { data { ... } }' section:
  preciselyID, addressNumber, streetName, city, admin1ShortName, postalCode

Example request:
{'data': {
  'query': 'query GetAddressDetailed($address: String!, $country: String) { getByAddress(address: $address, country: $country) { addresses { data { preciselyID addressNumber streetName city admin1ShortName postalCode } } } }',
  'variables': {'address': '42 Valley Of The Sun Dr, Fairplay, CO 80440', 'country': 'US'}
}}

Output: GraphQL response with address data matching the requested fields. Structure depends on the query provided.""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": _GRAPHQL_DATA_SCHEMA
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="get_parcel_by_owner_detailed",
        description="""Retrieve parcel records by owner via a custom GraphQL query. Supports two query modes:
  1. By ID: provide 'id' and 'queryType' (one of: PRECISELY_ID, PARCEL_ID, BUILDING_ID, PLACE_ID, DUNS_ID)
  2. By address: provide 'address' string only — do NOT pass queryType or id variables

This tool does NOT support coordinate-based lookups.
Do NOT use if get_parcels_by_address already meets your need (simpler interface).
Only use the safe, tested fields listed below.

Safe fields for the 'parcels { data { ... } }' section:
  parcelID, fips, geographyID, apn, parcelArea, longitude, latitude, elevation
Always include the metadata section: pageNumber, pageCount, totalPages, count, vintage

Output: GraphQL response with paginated parcel records matching the query. Includes metadata
(pageNumber, totalPages, count, vintage) and parcel data fields.

Example 1 — By PreciselyID (uses queryType + id):
{'data': {
  'query': 'query GetParcelByOwner($id: String, $queryType: QueryType, $address: String, $distance: Float, $limit: Int) { getParcelByOwner(id: $id, queryType: $queryType, address: $address, distance: $distance, limit: $limit) { parcels { metadata { pageNumber pageCount totalPages count vintage } data { parcelID fips geographyID apn parcelArea longitude latitude elevation } } } }',
  'variables': {'id': 'P0000GL41OME', 'queryType': 'PRECISELY_ID', 'address': 'Boston, MA', 'distance': 1000.0, 'limit': 50}
}}

Example 2 — By address (NO queryType, NO id — omit both):
{'data': {
  'query': 'query GetParcelByOwner($address: String, $distance: Float, $limit: Int) { getParcelByOwner(address: $address, distance: $distance, limit: $limit) { parcels { metadata { pageNumber pageCount totalPages count vintage } data { parcelID fips geographyID apn parcelArea longitude latitude elevation } } } }',
  'variables': {'address': '123 Main St, Boston, MA', 'distance': 1000.0, 'limit': 50}
}}""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": _GRAPHQL_DATA_SCHEMA
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="get_address_family",
        description="""Retrieve all addresses associated with the same property or parcel as a given PreciselyID,
via a custom GraphQL query. Address families include all delivery points sharing a parent
location (e.g., all units in a multi-unit building).
Use this tool when you have a PreciselyID and need to enumerate all related addresses at
that property. Requires queryType = 'PRECISELY_ID'.
Do NOT use with ADDRESS or LOCATION query types — this tool only supports PRECISELY_ID.

Safe fields for the 'addressFamily { data { ... } }' section:
  preciselyID, addressNumber, streetName, city, admin1ShortName, postalCode
Always include the metadata section: pageNumber, pageCount, totalPages, count, vintage

Output: GraphQL response with paginated list of related address records sharing the same
parent property, with pagination metadata.

Example request:
{'data': {
  'query': 'query GetAddressFamily($id: String!, $queryType: QueryType!) { getById(id: $id, queryType: $queryType) { addresses { data { preciselyID addressFamily(pageNumber: 1, pageSize: 20) { metadata { pageNumber pageCount totalPages count vintage } data { preciselyID addressNumber streetName city admin1ShortName postalCode } } } } } }',
  'variables': {'id': 'P0000GL41OME', 'queryType': 'PRECISELY_ID'}
}}""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": _GRAPHQL_DATA_SCHEMA
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="get_serviceability",
        description="""Retrieve broadband and utility serviceability information for a US address using a custom
GraphQL query. Returns whether broadband or utility services are available at the address
and the associated service provider records.
Use this tool when you need to check broadband/utility service availability at a property.
Only use the safe, tested fields listed below.

Safe fields for the 'serviceability { data { ... } }' section:
  serviceabilityID, preciselyID, serviceableAddress
Always include the metadata section: pageNumber, pageCount, totalPages, count, vintage

Output: GraphQL response with serviceability records containing serviceabilityID, preciselyID,
and a serviceableAddress flag ('YES'/'NO') indicating whether the address is serviceable.

Example request:
{'data': {
  'query': 'query GetServiceability($address: String!, $country: String) { getByAddress(address: $address, country: $country) { addresses(pageNumber: 1, pageSize: 1) { data { preciselyID serviceability { metadata { pageNumber pageCount totalPages count vintage } data { serviceabilityID preciselyID serviceableAddress } } } } } }',
  'variables': {'address': '2755 Milwaukee St, Denver, 80238 CO', 'country': 'US'}
}}""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": _GRAPHQL_DATA_SCHEMA
            },
            "required": ["data"]
        }
    ),
    Tool(
        name="get_places_by_address",
        description="""Retrieve points of interest (POI) / businesses at or near a US address using a custom GraphQL
query. Returns business names, industry codes, contact information, and location data for
places associated with the address.
Use this tool when you need business/POI data at a given address.
Do NOT use for property, parcel, building, or risk data — use the appropriate property/risk
tools instead.

Available fields in the 'places { data { ... } }' section:
  Identity: PBID, pointOfInterestID, preciselyID, parentPreciselyID
  Business: businessName, brandName, tradeName, franchiseName
  Location: countryIsoAlpha3Code, localityName, city, admin2, admin1, admin1ShortName
  Address: addressNumber, streetName, postalCode, formattedAddress, addressLine1, addressLine2
  Coordinates: longitude, latitude
  Georesult: georesult { value description }, georesultConfidence { value description }
  Contact: countryCallingCode, phone, fax, email, web
  Hours: open24Hours { value description }
  Industry: lineOfBusiness, sic1, sic2, sic8, sic8Description, altIndustryCode { value description }, miCode, tradeDivision, groupName, mainClass, subClass
Always include the metadata section: pageNumber, pageCount, totalPages, count, vintage

Output: GraphQL response with paginated place/POI records matching the address, with business
details and pagination metadata.

Example request:
{'data': {
  'query': 'query GetPlacesByAddress($address: String!, $country: String) { getByAddress(address: $address, country: $country) { places(pageNumber: 1, pageSize: 20) { metadata { pageNumber pageCount totalPages count vintage } data { PBID pointOfInterestID preciselyID parentPreciselyID businessName brandName tradeName franchiseName countryIsoAlpha3Code localityName city admin2 admin1 admin1ShortName addressNumber streetName postalCode formattedAddress addressLine1 addressLine2 longitude latitude georesult { value description } georesultConfidence { value description } countryCallingCode phone fax email web open24Hours { value description } lineOfBusiness sic1 sic2 sic8 sic8Description altIndustryCode { value description } miCode tradeDivision groupName mainClass subClass } } } }',
  'variables': {'address': '123 Main St, Boston, MA 02101', 'country': 'US'}
}}""",
        inputSchema={
            "type": "object",
            "properties": {
                "data": _GRAPHQL_DATA_SCHEMA
            },
            "required": ["data"]
        }
    ),
    ]