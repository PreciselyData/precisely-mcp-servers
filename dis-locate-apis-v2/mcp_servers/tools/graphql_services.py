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
            "description": "ISO 2-letter country code (e.g., 'US', 'GB', 'CA'). Default: 'US'.",
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
        description=(
            "Retrieve a comprehensive consolidated property record for a US address, including "
            "property attributes (size, year built, bedrooms, bathrooms), ownership information, "
            "assessed/market value, building characteristics, and parcel identifiers. "
            "Use this tool when you need a broad property overview in a single call. "
            "Do NOT use if you only need specific attribute categories — "
            "use get_property_attributes_by_address (physical attributes only), "
            "get_replacement_cost_by_address (replacement cost only), "
            "get_buildings_by_address (building footprint/structure only), or "
            "get_parcels_by_address (parcel/land data only) for narrower, faster responses. "
            "Only works for US addresses.\n\n"
            "Output: Comprehensive property record with attributes, ownership, valuation, "
            "building characteristics, and parcel identifiers."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_property_attributes_by_address",
        description=(
            "Retrieve physical property attributes for a US address: "
            "bedrooms, bathrooms, square footage, lot size, year built, construction type, and similar characteristics. "
            "Use this tool when you specifically need physical/structural property attributes. "
            "Do NOT use if you need a full property overview — use get_property_data instead. "
            "Do NOT use for valuation data — use get_replacement_cost_by_address instead. "
            "Do NOT use for risk assessments — use the specific risk tools (get_flood_risk_by_address, etc.). "
            "Only works for US addresses.\n\n"
            "Output: Object with physical property attributes including bedroom/bathroom counts, "
            "square footage, lot size, year built, and construction materials."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_replacement_cost_by_address",
        description=(
            "Retrieve the estimated replacement cost (cost to rebuild) for a property at a US address. "
            "Replacement cost is the estimated expense to reconstruct the building at current labor and material rates, "
            "which is distinct from market value or assessed value. "
            "Use this tool for insurance underwriting, home valuation, or rebuilding cost estimation. "
            "Do NOT use if you need general property attributes — use get_property_attributes_by_address instead. "
            "Do NOT use if you need market/assessed value — replacement cost only reflects reconstruction cost. "
            "Only works for US addresses.\n\n"
            "Output: Object with estimated replacement cost value, cost per square foot, "
            "valuation methodology, and effective date."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_flood_risk_by_address",
        description=(
            "Retrieve flood risk assessment data for a US address, including FEMA flood zone classification, "
            "flood zone description, and risk indicators. "
            "Use this tool when you need to assess flood exposure for a property. "
            "Do NOT use if you need wildfire, fire, earthquake, coastal, or weather risk — "
            "use the corresponding specific risk tool instead. "
            "Only works for US addresses.\n\n"
            "Output: Object with FEMA flood zone code (e.g., AE, X, VE), flood zone description, "
            "community panel number, and flood risk indicators."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_wildfire_risk_by_address",
        description=(
            "Retrieve wildfire risk assessment data for a US address, "
            "including risk score, risk category, and contributing factors. "
            "Use this tool when you need to assess wildfire exposure for a property. "
            "Do NOT use if you need flood, fire (structural), earthquake, coastal, or weather risk — "
            "use the corresponding specific risk tool instead. "
            "Only works for US addresses.\n\n"
            "Output: Object with wildfire risk score, risk category (e.g., low/medium/high/very high), "
            "and contributing environmental risk factors."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_property_fire_risk",
        description=(
            "Retrieve structural/property fire risk assessment data for a US address, "
            "including fire risk score and protection class information. "
            "This tool covers fire risk related to property protection distance from fire stations "
            "and fire department responsiveness — not wildfire risk. "
            "Use this tool for insurance underwriting or fire protection class assessment. "
            "Do NOT use if you need wildfire risk — use get_wildfire_risk_by_address instead. "
            "Do NOT use if you need flood, earthquake, coastal, or weather risk. "
            "Only works for US addresses.\n\n"
            "Output: Object with fire protection class, distance to nearest fire station, "
            "fire risk score, and fire department information."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_earth_risk",
        description=(
            "Retrieve earthquake (seismic) risk assessment data for a US address, "
            "including seismic zone, peak ground acceleration, and risk indicators. "
            "Use this tool when you need to assess earthquake/seismic exposure for a property. "
            "Do NOT use if you need flood, wildfire, fire (structural), coastal, or weather risk — "
            "use the corresponding specific risk tool instead. "
            "Only works for US addresses.\n\n"
            "Output: Object with seismic zone classification, peak ground acceleration value, "
            "and earthquake risk indicators for the property location."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_coastal_risk",
        description=(
            "Retrieve coastal hazard risk assessment data for a US address, "
            "including storm surge, wave action, and coastal erosion risk indicators. "
            "Use this tool for properties near coastlines where coastal storm or erosion risk is relevant. "
            "Do NOT use if you need flood zone (FEMA) risk — use get_flood_risk_by_address instead. "
            "Do NOT use if you need wildfire, earthquake, structural fire, or weather risk. "
            "Only works for US addresses.\n\n"
            "Output: Object with coastal hazard indicators including storm surge risk, "
            "wave action risk, coastal erosion risk, and proximity to coast."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_historical_weather_risk",
        description=(
            "Retrieve historical weather risk data for a US address, "
            "including exposure to severe weather events such as hail, wind, tornado, lightning, and extreme temperature. "
            "Use this tool when you need historical weather hazard information for insurance, underwriting, or risk profiling. "
            "Do NOT use for flood, wildfire, earthquake, fire protection class, or coastal risk "
            "— use the corresponding specific risk tools instead. "
            "Only works for US addresses.\n\n"
            "Output: Object with historical weather risk scores and frequency/severity indicators "
            "for hail, wind, tornado, lightning, and extreme temperature events."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),

    # Demographics & Neighborhoods tools (8 tools)
    Tool(
        name="get_demographics",
        description=(
            "Retrieve a combined demographic profile for a US address, "
            "including both PSYTE geodemographic segmentation and Ground View market segment data. "
            "Returns household income, age distribution, lifestyle segment, and neighborhood characteristics. "
            "Use this tool when you need a broad demographic overview combining both PSYTE and Ground View datasets. "
            "Do NOT use if you only need PSYTE segmentation — use get_psyte_geodemographics_by_address instead. "
            "Do NOT use if you only need Ground View market data — use get_ground_view_by_address instead. "
            "Do NOT use for crime index, neighborhood names, school data, building, or parcel data. "
            "Only works for US addresses.\n\n"
            "Output: Object with PSYTE segment code/name/description and Ground View segment code/name/description "
            "for the neighborhood of the input address."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_crime_index",
        description=(
            "Retrieve crime risk index data for a US address, "
            "including overall crime index and category-level indices "
            "(personal crime, property crime, violent crime). "
            "Crime indices are relative to a national baseline (100 = national average). "
            "Use this tool when you need to assess crime risk for a location. "
            "Do NOT use for weather, flood, fire, earthquake, wildfire, or coastal risk — use the specific risk tools. "
            "Do NOT use for demographic segmentation — use get_demographics or the specific PSYTE/Ground View tools. "
            "Only works for US addresses.\n\n"
            "Output: Object with overall crime index and sub-indices for "
            "personal, property, and violent crime categories relative to the national average."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_psyte_geodemographics_by_address",
        description=(
            "Retrieve PSYTE geodemographic segment classification for a US address. "
            "PSYTE (a Precisely proprietary segmentation system) classifies neighborhoods into lifestyle and "
            "demographic segments based on income, age, household composition, and lifestyle factors. "
            "Use this tool when you specifically need PSYTE segment data for targeting, analysis, or profiling. "
            "Do NOT use if you also need Ground View market segment data — use get_demographics instead "
            "(returns both PSYTE and Ground View in one call). "
            "Do NOT use for crime, risk, building, parcel, or school data. "
            "Only works for US addresses.\n\n"
            "Output: Object with PSYTE segment code, segment name, segment group, "
            "and demographic characteristics for the neighborhood of the input address."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_ground_view_by_address",
        description=(
            "Retrieve Ground View market segment data for a US address. "
            "Ground View is a Precisely market segmentation dataset that classifies "
            "households by purchasing behavior, lifestyle, and consumer characteristics. "
            "Use this tool when you specifically need Ground View segmentation data for market analysis or targeting. "
            "Do NOT use if you also need PSYTE segment data — use get_demographics instead "
            "(returns both PSYTE and Ground View in one call). "
            "Do NOT use for crime, risk, building, parcel, or school data. "
            "Only works for US addresses.\n\n"
            "Output: Object with Ground View segment code, name, and household consumer characteristics "
            "for the area of the input address."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_neighborhoods_by_address",
        description=(
            "Retrieve neighborhood name(s) and boundary information for a US address. "
            "Returns named neighborhood designations (e.g., 'Back Bay', 'SoHo') for the location. "
            "Use this tool when you need the human-readable neighborhood name for display, search, or labeling. "
            "Do NOT use for demographic data — use get_demographics or PSYTE/Ground View tools instead. "
            "Do NOT use for school, building, parcel, or crime data. "
            "Only works for US addresses.\n\n"
            "Output: Object with neighborhood name(s) and associated metadata "
            "(neighborhood type, boundary level) for the input address location."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_schools_by_address",
        description=(
            "Retrieve nearby schools for a US address, including school name, type (elementary/middle/high), "
            "district, enrollment, and distance from the address. "
            "Use this tool when you need school proximity or assignment information for a property. "
            "Do NOT use for demographic, crime, risk, building, or parcel data. "
            "Only works for US addresses.\n\n"
            "Output: Array of nearby school objects, each with school name, type, district name, "
            "enrollment count, grade range, and distance from the input address."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_buildings_by_address",
        description=(
            "Retrieve building footprint and structural characteristics for a US address, "
            "including building geometry, height, area, construction type, and use classification. "
            "Use this tool when you need detailed building structure data (footprint, height, area) "
            "rather than property ownership or valuation data. "
            "Do NOT use if you need full property data (ownership, valuation) — use get_property_data instead. "
            "Do NOT use for parcel/land data — use get_parcels_by_address instead. "
            "Only works for US addresses.\n\n"
            "Output: Object with building footprint geometry, height, floor count, area, "
            "construction type, and use classification for the structure at the input address."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),
    Tool(
        name="get_parcels_by_address",
        description=(
            "Retrieve land parcel (lot) data for a US address, including parcel geometry, "
            "area, APN (Assessor's Parcel Number), FIPS code, and land use classification. "
            "Use this tool when you need parcel/lot data (boundaries, identifiers, land use) "
            "rather than building structure or property ownership information. "
            "Do NOT use if you need full property data (ownership, valuation) — use get_property_data instead. "
            "Do NOT use for building structure data — use get_buildings_by_address instead. "
            "Only works for US addresses.\n\n"
            "Output: Object with parcel geometry, area, APN, FIPS code, land use code, "
            "and parcel identifiers for the property at the input address."
        ),
        inputSchema=_ADDRESS_INPUT_SCHEMA
    ),

    # Advanced GraphQL tools (5 tools)
    Tool(
        name="get_addresses_detailed",
        description=(
            "Retrieve detailed address record(s) from the Precisely address database using a custom GraphQL query. "
            "Allows fine-grained control over which address fields to request. "
            "Use this tool when the standard geocode or lookup tools do not return sufficient detail "
            "and you need to construct a custom GraphQL query. "
            "Do NOT use if a simpler tool (geocode, lookup, verify_address) already covers your need. "
            "Only use the safe, tested fields listed below — other fields may cause 400 errors.\n\n"
            "Safe fields for the 'addresses { data { ... } }' section:\n"
            "  preciselyID, addressNumber, streetName, city, admin1ShortName, postalCode\n\n"
            "Do NOT include: latitude, longitude, fips, geographyID, propertyType\n\n"
            "Output: GraphQL response with address data matching the requested fields. "
            "Structure depends on the query provided."
        ),
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
        description=(
            "Retrieve parcel records by owner, using a PreciselyID, address string, or coordinate, "
            "via a custom GraphQL query. "
            "Supports three query types: PRECISELY_ID (exact ID lookup), ADDRESS (text address), "
            "or LOCATION (coordinate-based). "
            "Use this tool when you need parcel ownership data and require custom field selection. "
            "Do NOT use if get_parcels_by_address already meets your need (simpler interface). "
            "Only use the safe, tested fields listed below.\n\n"
            "Safe fields for the 'parcels { data { ... } }' section:\n"
            "  parcelID, fips, geographyID, apn, parcelArea, longitude, latitude, elevation\n"
            "Always include the metadata section: pageNumber, pageCount, totalPages, count, vintage\n\n"
            "queryType values: PRECISELY_ID | ADDRESS | LOCATION\n\n"
            "Output: GraphQL response with paginated parcel records matching the query. "
            "Includes metadata (pageNumber, totalPages, count, vintage) and parcel data fields."
        ),
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
        description=(
            "Retrieve all addresses associated with the same property or parcel as a given PreciselyID, "
            "via a custom GraphQL query. "
            "Address families include all delivery points sharing a parent location "
            "(e.g., all units in a multi-unit building). "
            "Use this tool when you have a PreciselyID and need to enumerate all related addresses at that property. "
            "Requires queryType = 'PRECISELY_ID'. "
            "Do NOT use with ADDRESS or LOCATION query types — this tool only supports PRECISELY_ID.\n\n"
            "Safe fields for the 'addressFamily { data { ... } }' section:\n"
            "  preciselyID, addressNumber, streetName, city, admin1ShortName, postalCode\n"
            "Always include the metadata section: pageNumber, pageCount, totalPages, count, vintage\n\n"
            "Output: GraphQL response with paginated list of related address records "
            "sharing the same parent property, with pagination metadata."
        ),
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
        description=(
            "Retrieve broadband and utility serviceability information for a US address using a custom GraphQL query. "
            "Returns whether broadband or utility services are available at the address "
            "and the associated service provider records. "
            "Use this tool when you need to check broadband/utility service availability at a property. "
            "Only use the safe, tested fields listed below.\n\n"
            "Safe fields for the 'serviceability { data { ... } }' section:\n"
            "  serviceabilityID, preciselyID, serviceableAddress\n"
            "Always include the metadata section: pageNumber, pageCount, totalPages, count, vintage\n\n"
            "Output: GraphQL response with serviceability records indicating "
            "broadband/utility availability and service provider details for the address."
        ),
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
        description=(
            "Retrieve points of interest (POI) / businesses at or near a US address using a custom GraphQL query. "
            "Returns business names, industry codes, contact information, and location data "
            "for places associated with the address. "
            "Use this tool when you need business/POI data at a given address. "
            "Do NOT use for property, parcel, building, or risk data — use the appropriate property/risk tools instead.\n\n"
            "Available fields in the 'places { data { ... } }' section:\n"
            "  Identity: PBID, pointOfInterestID, preciselyID, parentPreciselyID\n"
            "  Business: businessName, brandName, tradeName, franchiseName\n"
            "  Location: city, admin1, admin1ShortName, postalCode, formattedAddress, longitude, latitude\n"
            "  Contact: phone, fax, email, web\n"
            "  Industry: lineOfBusiness, sic1, sic2, sic8, sic8Description, miCode, tradeDivision, groupName, mainClass, subClass\n"
            "Always include the metadata section: pageNumber, pageCount, totalPages, count, vintage\n\n"
            "Output: GraphQL response with paginated place/POI records "
            "matching the address, with business details and pagination metadata."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "data": _GRAPHQL_DATA_SCHEMA
            },
            "required": ["data"]
        }
    ),
    ]