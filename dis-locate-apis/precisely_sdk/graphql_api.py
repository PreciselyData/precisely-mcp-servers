import requests
from typing import Optional, Dict, Any, List, Union
from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()

from precisely_sdk.server import mcp

@mcp.tool()
def get_by_id(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Property Risk Data by ID (PreciselyID, ParcelID, BuildingID, PlaceID, or DUNS_ID).

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetById($id: String!, $queryType: QueryType!) {
                getById(id: $id, queryType: $queryType) {
                    inputID
                    addresses(pageNumber: 1, pageSize: 10) {
                        data {
                            preciselyID
                            addressNumber
                            streetName
                            city
                            admin1ShortName
                            postalCode
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # REQUIRED - The ID to search for
            "queryType": "PRECISELY_ID"      # REQUIRED - One of: PRECISELY_ID, PARCEL_ID, BUILDING_ID, PLACE_ID, DUNS_ID
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Property risk data for the specified ID

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Property Risk Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetByAddress($address: String!, $country: String) {
                getByAddress(address: $address, country: $country) {
                    inputID
                    buildings(pageNumber: 1, pageSize: 10) {
                        data {
                            buildingID
                            buildingType { value description }
                            latitude
                            longitude
                            buildingArea
                        }
                    }
                }
            }
        ''',
        "variables": {
            "address": "123 Main St, Boston, MA 02101",  # REQUIRED - Address to search for
            "country": "US"                              # OPTIONAL - Country code
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Property risk data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_by_text_search(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search Property Risk Data by Text with Location Context.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetByTextSearch(
                $searchText: String!,
                $address: String,
                $postalCode: String,
                $matchType: MatchType,
                $distance: Float,
                $limit: Int,
                $longitude: Float,
                $latitude: Float
            ) {
                getByTextSearch(
                    searchText: $searchText,
                    address: $address,
                    postalCode: $postalCode,
                    matchType: $matchType,
                    distance: $distance,
                    limit: $limit,
                    longitude: $longitude,
                    latitude: $latitude
                ) {
                    places {
                        data {
                            pointOfInterestID
                            businessName
                            city
                            admin1ShortName
                            postalCode
                        }
                    }
                }
            }
        ''',
        "variables": {
            "searchText": "Starbucks",        # REQUIRED - Text to search for
            "address": "Boston, MA",          # OPTIONAL - Address context
            "postalCode": "02101",            # OPTIONAL - Postal code
            "matchType": "EXACT",             # OPTIONAL - EXACT or FUZZY (default: EXACT)
            "distance": 1000.0,               # OPTIONAL - Search radius in meters (default: 1000.0)
            "limit": 50,                      # OPTIONAL - Max results (default: 50)
            "longitude": -71.0589,            # OPTIONAL - Longitude for location context
            "latitude": 42.3601               # OPTIONAL - Latitude for location context
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Places matching the text search criteria

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_parcel_by_owner(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Parcels by Owner Information.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetParcelByOwner(
                $id: String,
                $queryType: QueryType,
                $address: String,
                $distance: Float,
                $limit: Int
            ) {
                getParcelByOwner(
                    id: $id,
                    queryType: $queryType,
                    address: $address,
                    distance: $distance,
                    limit: $limit
                ) {
                    parcels {
                        data {
                            parcelID
                            apn
                            parcelArea
                            latitude
                            longitude
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # OPTIONAL - Owner ID
            "queryType": "PRECISELY_ID",      # OPTIONAL - ID type
            "address": "Boston, MA",          # OPTIONAL - Address context
            "distance": 1000.0,               # OPTIONAL - Search radius (default: 1000.0)
            "limit": 50                       # OPTIONAL - Max results (default: 50)
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Parcels owned by the specified owner

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_by_spatial(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Property Risk Data by Spatial Query (WKT or GeoJSON geometry).

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetBySpatial(
                $wkt: String,
                $geoJson: String,
                $address: String,
                $spatialFunction: SpatialFunction!,
                $inputID: String
            ) {
                getBySpatial(
                    wkt: $wkt,
                    geoJson: $geoJson,
                    address: $address,
                    spatialFunction: $spatialFunction,
                    inputID: $inputID
                ) {
                    inputID
                    addresses(pageNumber: 1, pageSize: 10) {
                        data {
                            preciselyID
                            addressNumber
                            streetName
                            city
                        }
                    }
                    buildings(pageNumber: 1, pageSize: 10) {
                        data {
                            buildingID
                            buildingArea
                        }
                    }
                }
            }
        ''',
        "variables": {
            "wkt": "POLYGON((-71.1 42.3, -71.0 42.3, -71.0 42.4, -71.1 42.4, -71.1 42.3))",  # OPTIONAL - WKT geometry
            "geoJson": null,                           # OPTIONAL - GeoJSON geometry (alternative to WKT)
            "address": "Boston, MA",                   # OPTIONAL - Address context
            "spatialFunction": "INTERSECTS",           # REQUIRED - One of: INTERSECTS, WITHIN, CONTAINS, TOUCHES, OVERLAPS
            "inputID": "search-123"                    # OPTIONAL - Custom input ID
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Property data within the specified geometry

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_flood_risk(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Flood Risk Information for a Property.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetFloodRisk($id: String!, $queryType: QueryType!) {
                getById(id: $id, queryType: $queryType) {
                    addresses {
                        data {
                            preciselyID
                            floodRisk {
                                data {
                                    preciselyID
                                    floodZone
                                    baseFloodElevationFeet
                                    addressLocationElevationFeet
                                    year100FloodZoneDistanceFeet
                                    year500FloodZoneDistanceFeet
                                    nameOfNearestWaterbody
                                    distanceToNearestWaterbodyFeet
                                }
                            }
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # REQUIRED - Property ID
            "queryType": "PRECISELY_ID"       # REQUIRED - ID type
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Flood risk data for the property

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_wildfire_risk(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Wildfire Risk Information for a Property.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetWildfireRisk($id: String!, $queryType: QueryType!) {
                getById(id: $id, queryType: $queryType) {
                    addresses {
                        data {
                            preciselyID
                            wildfireRisk {
                                data {
                                    preciselyID
                                    riskDescription { baseLineModel extremeModel }
                                    overallRiskRanking { baseLineModel extremeModel }
                                    severityRating { baseLineModel extremeModel }
                                    frequencyRating { baseLineModel extremeModel }
                                    communityRating { baseLineModel extremeModel }
                                    damageRating { baseLineModel extremeModel }
                                    mitigationRating { baseLineModel extremeModel }
                                    distanceToWildlandUrbanInterfaceFeet
                                }
                            }
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # REQUIRED - Property ID
            "queryType": "PRECISELY_ID"       # REQUIRED - ID type
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Wildfire risk data for the property

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_property_attributes(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Property Attributes (Tax Assessment Data) for a Property.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetPropertyAttributes($id: String!, $queryType: QueryType!) {
                getById(id: $id, queryType: $queryType) {
                    propertyAttributes {
                        data {
                            propertyAttributeID
                            preciselyID
                            owner
                            owner2
                            propertyCategory { value description }
                            standardizedLandUseCode { value description }
                            yearBuilt
                            buildingSquareFootage
                            bedroomCount
                            bathroomCount { value description }
                            totalAssessedValue
                            totalMarketValue
                            saleAmount
                            assessmentRecordingDate
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # REQUIRED - Property ID
            "queryType": "PRECISELY_ID"       # REQUIRED - ID type
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Property attributes and tax assessment data

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_crime_index(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Crime Index Data for a Property Location.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetCrimeIndex($id: String!, $queryType: QueryType!) {
                getById(id: $id, queryType: $queryType) {
                    addresses {
                        data {
                            preciselyID
                            crimeIndex {
                                data {
                                    blockGroupCode
                                    compositeIndexNational
                                    violentCrimeIndexNational
                                    propertyCrimeIndexNational
                                    compositeCrimeCategory { value description }
                                    violentCrimeCategory { value description }
                                    propertyCrimeCategory { value description }
                                    robberyIndexNational
                                    burglaryIndexNational
                                    motorVehicleTheftIndexNational
                                }
                            }
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # REQUIRED - Property ID
            "queryType": "PRECISELY_ID"       # REQUIRED - ID type
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Crime index data for the property location

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_demographics(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Demographics and Lifestyle Data (PSYTE) for a Property Location.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetDemographics($id: String!, $queryType: QueryType!) {
                getById(id: $id, queryType: $queryType) {
                    addresses {
                        data {
                            preciselyID
                            psyteGeodemographics {
                                data {
                                    censusBlock
                                    censusBlockGroup
                                    censusBlockPopulation
                                    censusBlockHouseholds
                                    PSYTESegmentCode { value description }
                                    householdIncomeVariable { value description }
                                    propertyValueVariable { value description }
                                    urbanRuralVariable { value description }
                                    adultAgeVariable { value description }
                                }
                            }
                            groundView {
                                data {
                                    censusBlockGroup
                                    censusBlockGroupPopulation
                                    averageHouseholdIncome
                                    averageHomeValue
                                    ownerOccupiedHousingUnitsPercent
                                    educationBachelorsDegreePercent
                                    unemployedPercent
                                }
                            }
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # REQUIRED - Property ID
            "queryType": "PRECISELY_ID"       # REQUIRED - ID type
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Demographics and lifestyle data for the property location

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_neighborhood_data(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Neighborhood Data and Market Trends for a Property.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetNeighborhoodData($id: String!, $queryType: QueryType!) {
                getById(id: $id, queryType: $queryType) {
                    neighborhoods {
                        neighborhood {
                            data {
                                neighborhoodID
                                neighborhoodName
                                walkability { value description }
                                bikeScore
                                driveScore
                                publicTransitScore
                                averageSingleFamilyResidencePriceUSD
                                residentialSalesTrend { value description }
                                averageYearBuilt
                                averageBedrooms
                                averageBathrooms
                                averageLivingSpaceSquareFootage
                                poolPercentage
                                averageLotSizeAcres
                            }
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # REQUIRED - Property ID
            "queryType": "PRECISELY_ID"       # REQUIRED - ID type
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Neighborhood data and market trends

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_property_fire_risk(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Property Fire Risk Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetByAddress($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    propertyFireRisk {
                      data {
                        preciselyID
                        incorporatedPlaceCode
                        incorporatedPlaceName
                        firestation1DepartmentID
                        firestation1DepartmentType
                        firestation1ID
                        firestation1DrivetimeAMPeakMinutes
                        firestation1DrivetimePMPeakMinutes
                        firestation1DrivetimeOffPeakMinutes
                        firestation1DrivetimeNightMinutes
                        firestation1DriveDistanceMiles
                        firestation2DepartmentID
                        firestation2DepartmentType
                        firestation2ID
                        firestation2DrivetimeAMPeakMinutes
                        firestation2DrivetimePMPeakMinutes
                        firestation2DrivetimeOffPeakMinutes
                        firestation2DrivetimeNightMinutes
                        firestation2DriveDistanceMiles
                        firestation3DepartmentID
                        firestation3DepartmentType
                        firestation3ID
                        firestation3DrivetimeAMPeakMinutes
                        firestation3DrivetimePMPeakMinutes
                        firestation3DrivetimeOffPeakMinutes
                        firestation3DrivetimeNightMinutes
                        firestation3DriveDistanceMiles
                        nearestWaterBodyDistanceFeet
                      } 
                    }
                  }
                }
              }
            }
        ''',
        "variables": {
            "address": "123 Main St, Boston, MA 02101",  # REQUIRED - Address to search for
            "country": "US"                              # OPTIONAL - Country code
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Property fire risk data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_coastal_risk(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Property Fire Risk Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetByAddress($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    coastalRisk {
                      data {
                         preciselyID
                        waterbodyName
                        nearestWaterbodyCounty
                        nearestWaterbodyState
                        nearestWaterbodyAdjacentName
                        nearestWaterbodyAdjacentType
                        distanceToNearestCoastFeet
                        windpoolDescription
                        category1MinSpeedMPH
                        category1MaxSpeedMPH
                        category1WindDebris
                        category2MinSpeedMPH
                        category2MaxSpeedMPH
                        category2WindDebris
                        category3MinSpeedMPH
                        category3MaxSpeedMPH
                        category3WindDebris
                        category4MinSpeedMPH
                        category4MaxSpeedMPH
                        category4WindDebris
                        category1MinSpeedMPHRec
                        category1MaxSpeedMPHRec
                        category1WindDebrisRec
                        category2MinSpeedMPHRec
                        category2MaxSpeedMPHRec
                        category2WindDebrisRec
                        category3MinSpeedMPHRec
                        category3MaxSpeedMPHRec
                        category3WindDebrisRec
                        category4MinSpeedMPHRec
                        category4MaxSpeedMPHRec
                        category4WindDebrisRec
                      } 
                    }
                  }
                }
              }
            }
        ''',
        "variables": {
            "address": "123 Main St, Boston, MA 02101",  # REQUIRED - Address to search for
            "country": "US"                              # OPTIONAL - Country code
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Property fire risk data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    BASE_URL = os.getenv('BASE_URL')

    client = ApiClient(
        base_url=BASE_URL,
        api_key=API_KEY,
        api_secret=API_SECRET
    )

    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()