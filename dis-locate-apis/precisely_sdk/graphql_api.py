import requests
from typing import Optional, Dict, Any, List, Union
from precisely_sdk.api_client import get_default_client

from precisely_sdk.server import mcp


@mcp.tool()
def get_addresses_detailed(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Detailed Address Information by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetAddressesDetailed($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 10) {
                  metadata {
                    pageNumber
                    pageCount
                    totalPages
                    count
                    vintage
                  }
                  data {
                    preciselyID
                    addressNumber
                    streetName
                    unitType
                    unit
                    city
                    admin1ShortName
                    postalCode
                    postalCodeExtension
                    locationCode { value description }
                    geographyID
                    latitude
                    longitude
                    parentPreciselyID
                    propertyType { value description }
                    fips
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
        dict: Detailed address information

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()



@mcp.tool()
def get_parcel_by_owner_detailed(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Detailed Parcels by Owner Information.

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
                        metadata {
                            pageNumber
                            pageCount
                            totalPages
                            count
                            vintage
                        }
                        data {
                            parcelID
                            fips
                            geographyID
                            apn
                            parcelArea
                            longitude
                            latitude
                            elevation
                        }
                    }
                }
            }
        ''',
        "variables": {
            "id": "12345",                    # OPTIONAL - Owner ID or search term
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
        dict: Detailed parcels owned by the specified owner

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

# ADDITIONAL FUNCTIONS FOR RELATIONSHIP QUERIES

@mcp.tool()
def get_address_family(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Address Family (Related Addresses) by PreciselyID.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetAddressFamily($id: String!, $queryType: QueryType!) {
              getById(id: $id, queryType: $queryType) {
                addresses {
                  data {
                    preciselyID
                    addressFamily(pageNumber: 1, pageSize: 20) {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        preciselyID
                        addressNumber
                        streetName
                        unitType
                        unit
                        city
                        admin1ShortName
                        postalCode
                        propertyType { value description }
                        parentPreciselyID
                      }
                    }
                  }
                }
              }
            }
        ''',
        "variables": {
            "id": "12345",                    # REQUIRED - PreciselyID
            "queryType": "PRECISELY_ID"       # REQUIRED - ID type
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Address family (related addresses) data

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
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
    Get Coastal Risk Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetCoastalRisk($address: String!, $country: String) {
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
        dict: Coastal risk data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_crime_index_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Crime Index Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetCrimeIndex($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    crimeIndex {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        blockGroupCode
                        compositeIndexNational
                        violentCrimeIndexNational
                        robberyIndexNational
                        rapeIndexNational
                        aggravatedAssaultIndexNational
                        murderIndexNational
                        propertyCrimeIndexNational
                        arsonIndexNational
                        burglaryIndexNational
                        motorVehicleTheftIndexNational
                        larcenyTheftIndexNational
                        compositeCrimeCategory { value description }
                        violentCrimeCategory { value description }
                        robberyCategory { value description }
                        rapeCategory { value description }
                        aggravatedAssaultCategory { value description }
                        murderCategory { value description }
                        propertyCrimeCategory { value description }
                        arsonCategory { value description }
                        burglaryCategory { value description }
                        motorVehicleTheftCategory { value description }
                        larcenyTheftCategory { value description }
                        compositeIndexState
                        violentCrimeIndexState
                        robberyIndexState
                        rapeIndexState
                        aggravatedAssaultIndexState
                        murderIndexState
                        propertyCrimeIndexState
                        arsonIndexState
                        burglaryIndexState
                        motorVehicleTheftIndexState
                        larcenyTheftIndexState
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
        dict: Crime index data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_psyte_geodemographics_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get PSYTE Geodemographics Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetPsyteGeodemographics($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    psyteGeodemographics {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        censusBlock
                        censusBlockGroup
                        censusBlockPopulation
                        censusBlockHouseholds
                        PSYTEGroupCode
                        PSYTECategoryCode
                        PSYTESegmentCode { value description }
                        householdIncomeVariable { value description }
                        propertyValueVariable { value description }
                        propertyTenureVariable { value description }
                        propertyTypeVariable { value description }
                        urbanRuralVariable { value description }
                        adultAgeVariable { value description }
                        householdCompositionVariable { value description }
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
        dict: PSYTE geodemographics data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_ground_view_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Ground View Demographics Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetGroundView($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    groundView {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        censusBlockGroup
                        censusBlockGroupArea
                        censusBlockGroupPopulation
                        censusBlockGroupPopulationForecast5Y
                        percentPopulationUnder5yearsPercent
                        percentPopulation5to9yearsPercent
                        percentPopulation10to14yearsPercent
                        percentPopulation15to19yearsPercent
                        percentPopulation20to24yearsPercent
                        percentPopulation25to29yearsPercent
                        percentPopulation30to34yearsPercent
                        percentPopulation35to39yearsPercent
                        percentPopulation40to44yearsPercent
                        percentPopulation45to49yearsPercent
                        percentPopulation50to54yearsPercent
                        percentPopulation55to59yearsPercent
                        percentPopulation60to64yearsPercent
                        percentPopulation65to69yearsPercent
                        percentPopulation70to74yearsPercent
                        percentPopulation75to79yearsPercent
                        percentPopulation80to84yearsPercent
                        percentPopulation85plusyearsPercent
                        maritalStatusNeverMarriedPercent
                        maritalStatusNowMarriedPercent
                        maritalStatusSeparatedPercent
                        maritalStatusWidowedPercent
                        maritalStatusDivorcedPercent
                        homeWorkers16yearsAndOverPercent
                        educationHighSchoolGraduatePercent
                        educationAssociatesDegreePercent
                        educationBachelorsDegreePercent
                        educationMastersDegreePercent
                        educationProfessionalSchoolDegreePercent
                        educationDoctorateDegreePercent
                        unemployedPercent
                        industryAgricultureForestryFishingHuntingMiningPercent
                        industryConstructionPercent
                        industryManufacturingPercent
                        industryWholesaleTradePercent
                        industryRetailTradePercent
                        industryTransportationandUtilitiesPercent
                        industryInformationPercent
                        industryFinancialActivitiesPercent
                        industryProfessionalScientificManagementPercent
                        industryServicePercent
                        industryLeisureandHospitalityPercent
                        industryOtherServicesPercent
                        industryPublicAdministrationPercent
                        occupationWhiteCollarPercent
                        occupationBlueCollarPercent
                        censusBlockGroupHouseholds
                        censusBlockGroupHouseholdsForecast5Y
                        households1personPercent
                        households2personPercent
                        households3personPercent
                        households4personPercent
                        households5personPercent
                        households6personPercent
                        households7plusPersonPercent
                        ownerOccupiedHousingUnitsPercent
                        renterOccupiedHousingUnitsPercent
                        households1vehiclePercent
                        households2vehiclesPercent
                        households3vehiclesPercent
                        households4vehiclesPercent
                        households5plusVehiclesPercent
                        averageVehiclesPerHousehold
                        averageRent
                        averageHomeValue
                        householdIncomeUnder10kPercent
                        householdIncome10kto15kPercent
                        householdIncome15kto20kPercent
                        householdIncome20kto25kPercent
                        householdIncome25kto30kPercent
                        householdIncome30kto35kPercent
                        householdIncome35kto40kPercent
                        householdIncome40kto45kPercent
                        householdIncome45kto50kPercent
                        householdIncome50kto60kPercent
                        householdIncome60kto75kPercent
                        householdIncome75kto100kPercent
                        householdIncome100kto125kPercent
                        householdIncome125kto150kPercent
                        householdIncome150kto200kPercent
                        householdIncome200kplusPercent
                        averageHouseholdIncome
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
        dict: Ground View demographics data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_replacement_cost_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Replacement Cost Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetReplacementCost($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                replacementCost(pageNumber: 1, pageSize: 10) {
                  metadata {
                    pageNumber
                    pageCount
                    totalPages
                    count
                    vintage
                  }
                  data {
                    propertyAttributeID
                    preciselyID
                    parentPreciselyID
                    plinkID
                    replacementCostUSD
                    replacementCostConfidenceCode
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
        dict: Replacement cost data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_property_attributes_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Property Attributes Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetPropertyAttributes($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                propertyAttributes(pageNumber: 1, pageSize: 10) {
                  metadata {
                    pageNumber
                    pageCount
                    totalPages
                    count
                    vintage
                  }
                  data {
                    propertyAttributeID
                    preciselyID
                    parentPreciselyID
                    plinkID
                    owner
                    owner2
                    ownerType { value description }
                    propertyCategory { value description }
                    standardizedLandUseCode { value description }
                    yearBuilt
                    effectiveYearBuilt
                    buildingSquareFootage
                    livingSquareFootage
                    bedroomCount
                    bathroomCount { value description }
                    roomCount
                    poolType { value description }
                    totalAssessedValue
                    landAssessedValue
                    improvementAssessedValue
                    totalMarketValue
                    landMarketValue
                    improvementMarketValue
                    saleAmount
                    saleCode { value description }
                    assessmentRecordingDate
                    priorSaleDate
                    priorSaleAmount
                    taxAmount
                    taxYear
                    propertyAreaAcres
                    propertyAreaSquareFootage
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
        dict: Property attributes data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_neighborhoods_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Neighborhood Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetNeighborhoods($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                neighborhoods {
                  neighborhood(pageNumber: 1, pageSize: 5) {
                    metadata {
                      pageNumber
                      pageCount
                      totalPages
                      count
                      vintage
                    }
                    data {
                      neighborhoodID
                      neighborhoodName
                      bikeScore
                      driveScore
                      publicTransitScore
                      walkability { value description }
                      averageSingleFamilyResidencePriceUSD
                      residentialSalesTrend { value description }
                      residentialSalesPriceTrend { value description }
                      averageYearBuilt
                      averageBedrooms
                      averageBathrooms
                      averageLivingSpaceSquareFootage
                      poolPercentage
                      averageLotSizeAcres
                      singleFamilyResidencePercent
                      commercialProperties
                      singleFamilyProperties
                      condominiums
                      duplex
                      apartment
                      lender
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
        dict: Neighborhood data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_schools_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Schools Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetSchools($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                schools {
                  college(pageNumber: 1, pageSize: 10) {
                    metadata {
                      pageNumber
                      pageCount
                      totalPages
                      count
                      vintage
                    }
                    data {
                      universityID
                      universityName
                      campusName
                    }
                  }
                  schoolDistrict(pageNumber: 1, pageSize: 10) {
                    metadata {
                      pageNumber
                      pageCount
                      totalPages
                      count
                      vintage
                    }
                    data {
                      schoolDistrictID
                      schoolDistrictName
                    }
                  }
                  schoolAttendanceZone(pageNumber: 1, pageSize: 10) {
                    metadata {
                      pageNumber
                      pageCount
                      totalPages
                      count
                      vintage
                    }
                    data {
                      schoolAttendanceZoneID
                      schoolAttendanceZoneName
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
        dict: Schools data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_buildings_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Building Information by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetBuildings($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                buildings(pageNumber: 1, pageSize: 10) {
                  metadata {
                    pageNumber
                    pageCount
                    totalPages
                    count
                    vintage
                  }
                  data {
                    buildingID
                    buildingType { value description }
                    ubid
                    fips
                    geographyID
                    longitude
                    latitude
                    elevation
                    maximumElevation
                    minimumElevation
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
        dict: Building information for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_parcels_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Parcel Information by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetParcels($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                parcels(pageNumber: 1, pageSize: 10) {
                  metadata {
                    pageNumber
                    pageCount
                    totalPages
                    count
                    vintage
                  }
                  data {
                    parcelID
                    fips
                    geographyID
                    apn
                    parcelArea
                    longitude
                    latitude
                    elevation
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
        dict: Parcel information for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_places_nearby(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Places (Points of Interest) Nearby an Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetPlacesNearby($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                places(pageNumber: 1, pageSize: 20) {
                  metadata {
                    pageNumber
                    pageCount
                    totalPages
                    count
                    vintage
                  }
                  data {
                    PBID
                    pointOfInterestID
                    preciselyID
                    parentPreciselyID
                    businessName
                    brandName
                    tradeName
                    franchiseName
                    countryIsoAlpha3Code
                    localityName
                    city
                    admin2
                    admin1
                    admin1ShortName
                    addressNumber
                    streetName
                    postalCode
                    formattedAddress
                    addressLine1
                    addressLine2
                    longitude
                    latitude
                    georesult { value description }
                    georesultConfidence { value description }
                    countryCallingCode
                    phone
                    fax
                    email
                    web
                    open24Hours { value description }
                    lineOfBusiness
                    sic1
                    sic2
                    sic8
                    sic8Description
                    altIndustryCode { value description }
                    miCode
                    tradeDivision
                    groupName
                    mainClass
                    subClass
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
        dict: Places (points of interest) near the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
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
            query GetPropertyFireRisk($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    propertyFireRisk {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
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
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_earth_risk(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Earth Risk (Earthquake) Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetEarthRisk($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    earthRisk {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        preciselyID
                        countOfEarthquakeMagnitude0Events
                        countOfEarthquakeMagnitude1Events
                        countOfEarthquakeMagnitude2Events
                        countOfEarthquakeMagnitude3Events
                        countOfEarthquakeMagnitude4Events
                        countOfEarthquakeMagnitude5Events
                        countOfEarthquakeMagnitude6Events
                        countOfEarthquakeMagnitude7Events
                        countOfEventsEarthquakeMagnitude0
                        countOfEventsEarthquakeMagnitude1
                        countOfEventsEarthquakeMagnitude2
                        countOfEventsEarthquakeMagnitude3
                        countOfEventsEarthquakeMagnitude4
                        countOfEventsEarthquakeMagnitude5
                        countOfEventsEarthquakeMagnitude6
                        countOfEventsEarthquakeMagnitude7
                        nameOfNearestFault
                        distanceToNearestFaultMiles
                        offsetFeet
                        faultType
                        faultSlipDirectionCode { value description }
                        faultAge
                        faultAngle
                        faultDipDirection
                        pmlZoneGrade
                        nehrpClassification { value description }
                        nehrpCode { value description }
                        newMadridFaultDistanceMiles
                      } 
                    }
                  }
                }
              }
            }
        ''',
        "variables": {
            "address": "123 Main St, San Francisco, CA 94102",  # REQUIRED - Address to search for
            "country": "US"                                     # OPTIONAL - Country code
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Earth risk (earthquake) data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_wildfire_risk_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Wildfire Risk Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetWildfireRisk($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    wildfireRisk {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        preciselyID
                        geometryID
                        stateAbbreviation
                        blockFIPS
                        geometryType { value description }
                        aggregationModel { value description }
                        riskDescription { baseLineModel extremeModel }
                        overallRiskRanking { baseLineModel extremeModel }
                        severityRating { baseLineModel extremeModel }
                        frequencyRating { baseLineModel extremeModel }
                        communityRating { baseLineModel extremeModel }
                        damageRating { baseLineModel extremeModel }
                        mitigationRating { baseLineModel extremeModel }
                        urbanConflagrationRating { baseLineModel extremeModel }
                        intensityRating { baseLineModel extremeModel }
                        crownFireRating { baseLineModel extremeModel }
                        windSpeedRating { baseLineModel extremeModel }
                        emberCastMagnitudeRating { baseLineModel extremeModel }
                        burnProbabilityRating { baseLineModel extremeModel }
                        historicFirePerimeterRating { baseLineModel extremeModel }
                        emberIgniteProbabilityRating { baseLineModel extremeModel }
                        powerLineDistanceRating { baseLineModel extremeModel }
                        structureDensityRating { baseLineModel extremeModel }
                        windAlignedRoadsRating { baseLineModel extremeModel }
                        addressPointToRoadDistanceRating { baseLineModel extremeModel }
                        vegetationCoverRating { baseLineModel extremeModel }
                        historicalLossRating { baseLineModel extremeModel }
                        insectDiseaseVegetationRating { baseLineModel extremeModel }
                        nearestFirestationDistanceRating { baseLineModel extremeModel }
                        nearestWaterbodyDistanceRating { baseLineModel extremeModel }
                        topographicRating { baseLineModel extremeModel }
                        burnableLandRating { baseLineModel extremeModel }
                        structureThreat { baseLineModel extremeModel }
                        houseToHouseThreat { baseLineModel extremeModel }
                        uniqueIdentifier
                        firePerimeterAcres
                        firePerimeterAgency
                        firePerimeterYear
                        firePerimeterName
                        firePerimeterDate
                        distanceToWildlandUrbanInterfaceFeet
                        distanceToExtremeRisk { baseLineModel extremeModel }
                        distanceToHighRiskFeet { baseLineModel extremeModel }
                        distanceToVeryHighRiskFeet { baseLineModel extremeModel }
                      } 
                    }
                  }
                }
              }
            }
        ''',
        "variables": {
            "address": "123 Main St, Los Angeles, CA 90210",  # REQUIRED - Address to search for
            "country": "US"                                   # OPTIONAL - Country code
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Wildfire risk data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_flood_risk_by_address(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Flood Risk Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetFloodRisk($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    floodRisk {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        preciselyID
                        floodID
                        femaMapPanelIdentifier
                        floodZoneMapType
                        stateFIPS
                        floodZoneBaseFloodElevationFeet
                        floodZone
                        additionalInformation
                        baseFloodElevationFeet
                        communityNumber
                        communityStatus
                        mapEffectiveDate
                        letterOfMapRevisionDate
                        letterOfMapRevisionCaseNumber
                        floodHazardBoundaryMapInitialDate
                        floodInsuranceRateMapInitialDate
                        addressLocationElevationFeet
                        year100FloodZoneDistanceFeet
                        year500FloodZoneDistanceFeet
                        elevationProfileToClosestWaterbodyFeet
                        distanceToNearestWaterbodyFeet
                        nameOfNearestWaterbody
                      } 
                    }
                  }
                }
              }
            }
        ''',
        "variables": {
            "address": "123 Main St, New Orleans, LA 70112",  # REQUIRED - Address to search for
            "country": "US"                                   # OPTIONAL - Country code
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Flood risk data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_historical_weather_risk(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Historical Weather Risk Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetHistoricalWeatherRisk($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    historicalWeatherRisk {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        preciselyID
                        countOfHailEventsH5
                        rangeOfHailEventsH5
                        hailRiskLevel
                        countOfTornadoEventsF2
                        rangeOfTornadoEventsF2
                        tornadoRiskLevel
                        countOfHurricaneEvents
                        rangeOfHurricaneEvents
                        countOfWindEventsW9
                        rangeOfWindEventsW9
                        windRiskLevel
                      } 
                    }
                  }
                }
              }
            }
        ''',
        "variables": {
            "address": "123 Main St, Oklahoma City, OK 73102",  # REQUIRED - Address to search for
            "country": "US"                                     # OPTIONAL - Country code
        }
    }

    Parameters:
        client (ApiClient): Initialized Precisely ApiClient instance.
        json_data (dict): GraphQL query and variables as shown above.
        x_request_id (Optional[str]): Optional request ID (max 38 chars).

    Returns:
        dict: Historical weather risk data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()
    headers["Content-Type"] = "application/json"
    if x_request_id:
        headers["X-Request-Id"] = x_request_id

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_serviceability(
    client,
    json_data: Dict[str, Any],
    x_request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Serviceability Data by Address.

    --------
    Required Payload Structure:
    {
        "query": '''
            query GetServiceability($address: String!, $country: String) {
              getByAddress(address: $address, country: $country) {
                addresses(pageNumber: 1, pageSize: 1) {
                  data {
                    preciselyID
                    serviceability {
                      metadata {
                        pageNumber
                        pageCount
                        totalPages
                        count
                        vintage
                      }
                      data {
                        serviceabilityID
                        preciselyID
                        residentialBusinessIndicator { value description }
                        serviceableAddress
                        standardizedLandUseValues { value description }
                        genealogy { value description }
                        genealogyCount
                        buildingDesignation { value description }
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
        dict: Serviceability data for the specified address

    Raises:
        requests.HTTPError: For 4xx/5xx responses.
    """
    client = get_default_client()
    
    url = f"{client.base_url}/data-graph/graphql"
    headers = client.get_headers()