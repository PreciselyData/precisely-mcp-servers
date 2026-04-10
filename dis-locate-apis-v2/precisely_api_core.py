"""
Precisely API Core Module for MCP Server
Production-ready module containing the PreciselyAPI class for MCP server use.
Pure API functionality with minimal dependencies.
"""

import json
import base64
import requests
from typing import Dict, List, Any
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import traceback
import uuid

# Load environment variables (override=True ensures fresh values)
load_dotenv(override=True)

# Configure logging with a unique identifier
log_uuid = str(uuid.uuid4())[:8]
log_file = f"logs/app_{log_uuid}.log"

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
    ]
)

logger = logging.getLogger(__name__)
logger.info("Precisely API Core module loaded for MCP Server")

class PreciselyAPI:
    """Precisely API client for direct integration with correct payload structures"""
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = None):
        self.api_key = api_key
        self.api_secret = api_secret
        # Use environment variable if base_url not provided
        self.base_url = base_url or os.getenv("PRECISELY_BASE_URL", "https://api.cloud.precisely.com")
        self.session = requests.Session()
        # Use proper authentication format from SDK
        import base64
        credentials = f"{api_key}:{api_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.session.headers.update({
            "Authorization": f"Apikey {encoded}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _validate_graphql_response(self, result: Dict[str, Any], method_name: str) -> Dict[str, Any]:
        """Validate a GraphQL response for errors. GraphQL returns HTTP 200 even on errors."""
        if "errors" in result:
            errors = result["errors"]
            error_messages = [e.get("message", str(e)) for e in errors]
            logger.error(f"[{method_name}] GraphQL errors: {error_messages}")
            if "data" in result and result["data"]:
                # Partial success: return data with error info
                result["graphql_errors"] = error_messages
                result["completeness"] = "partial"
                return result
            return {"error": "; ".join(error_messages), "error_type": "permanent", "graphql_errors": errors}
        return result
    
    def geocode(self, address: str, **kwargs) -> Dict[str, Any]:
        """Convert address to coordinates using correct payload structure"""
        try:
            url = f"{self.base_url}/v1/geocode"
            
            json_data = {
                "preferences": {
                    "maxResults": kwargs.get("maxResults", 1),
                    "returnAllInfo": kwargs.get("returnAllInfo", True),
                    "clientLocale": kwargs.get("clientLocale", "en_US")
                },
                "addresses": [
                    {
                        "addressId": "1",
                        "addressLines": [address],
                        "country": kwargs.get("country", "USA")
                    }
                ]
            }

            logger.debug(f"[geocode] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[geocode] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            return {"error": str(e)}
    
    def reverse_geocode(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        """Convert coordinates to address using correct payload structure"""
        try:
            url = f"{self.base_url}/v1/reverse-geocode"
            
            json_data = {
                "preferences": {
                    "maxResults": kwargs.get("maxResults", 1),
                    "returnAllInfo": kwargs.get("returnAllInfo", True),
                    "clientLocale": kwargs.get("clientLocale", "en_US")
                },
                "locations": [
                    {
                        "addressId": "1",
                        "longitude": lon,
                        "latitude": lat,
                        "country": kwargs.get("country", "USA")
                    }
                ]
            }
            
            logger.debug(f"[reverse_geocode] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[reverse_geocode] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Reverse geocoding error: {e}")
            return {"error": str(e)}
    
    def verify_address(self, address: str, **kwargs) -> Dict[str, Any]:
        """Verify and standardize address using correct payload structure"""
        try:
            url = f"{self.base_url}/v1/verify"
            
            json_data = {
                "preferences": {
                    "returnAllInfo": kwargs.get("returnAllInfo", True),
                    "clientLocale": kwargs.get("clientLocale", "en_US")
                },
                "addresses": [
                    {
                        "addressId": "1",
                        "addressLines": [address],
                        "country": kwargs.get("country", "USA")
                    }
                ]
            }
            
            logger.debug(f"[verify_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[verify_address] Raw response: {response.text}")

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Address verification error: {e}")
            return {"error": str(e)}
    
    def get_property_data(self, address: str, country: str = "US") -> Dict[str, Any]:
        """Get comprehensive property information via GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            
            json_data = {
                "query": '''
                    query GetPropertyData($address: String!, $country: String) {
                      getByAddress(address: $address, country: $country) {
                        addresses(pageNumber: 1, pageSize: 1) {
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
                        propertyAttributes(pageNumber: 1, pageSize: 1) {
                          data {
                            propertyAttributeID
                            preciselyID
                            yearBuilt
                            buildingSquareFootage
                            livingSquareFootage
                            bedroomCount
                            bathroomCount { value description }
                            roomCount
                            poolType { value description }
                            totalAssessedValue
                            totalMarketValue
                            saleAmount
                            propertyAreaAcres
                            propertyAreaSquareFootage
                          }
                        }
                        buildings(pageNumber: 1, pageSize: 1) {
                          data {
                            buildingID
                            buildingType { value description }
                            buildingArea
                          }
                        }
                      }
                    }
                ''',
                "variables": {
                    "address": address,
                    "country": country
                }
            }
            logger.debug(f"[get_property_data] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_property_data] Raw response: {response.text}")

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Property data error: {e}")
            return {"error": str(e)}
    
    def get_crime_index(self, address: str, country: str = "US") -> Dict[str, Any]:
        """Get crime index data"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            
            json_data = {
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
                                compositeIndexNational
                                violentCrimeIndexNational
                                propertyCrimeIndexNational
                                compositeCrimeCategory { value description }
                                violentCrimeCategory { value description }
                                propertyCrimeCategory { value description }
                              }
                            }
                          }
                        }
                      }
                    }
                ''',
                "variables": {
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_crime_index] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_crime_index] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Crime index error: {e}")
            return {"error": str(e)}
    
    def get_demographics(self, address: str, country: str = "US") -> Dict[str, Any]:
        """Get demographic and lifestyle data"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            
            json_data = {
                "query": '''
                    query GetDemographics($address: String!, $country: String) {
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
                                PSYTESegmentCode { value description }
                                householdIncomeVariable { value description }
                                propertyValueVariable { value description }
                                adultAgeVariable { value description }
                                householdCompositionVariable { value description }
                              }
                            }
                            groundView {
                              metadata {
                                pageNumber
                                pageCount
                                totalPages
                                count
                                vintage
                              }
                              data {
                                censusBlockGroupPopulation
                                averageHouseholdIncome
                                educationBachelorsDegreePercent
                                educationHighSchoolGraduatePercent
                                averageHomeValue
                                averageRent
                              }
                            }
                          }
                        }
                      }
                    }
                ''',
                "variables": {
                    "address": address,
                    "country": country
                }
            }
            logger.debug(f"[get_demographics] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_demographics] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Demographics error: {e}")
            return {"error": str(e)}
    
    def parse_address(self, address: str, **kwargs) -> Dict[str, Any]:
        """Parse a single-line address into structured components"""
        try:
            url = f"{self.base_url}/v1/address/parse"
            
            json_data = {
                "address": address
            }
            
            logger.debug(f"[parse_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[parse_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Parse address error: {e}")
            return {"error": str(e)}
    
    def parse_address_batch(self, addresses: List[Dict], **kwargs) -> Dict[str, Any]:
        """Parse a batch of addresses into structured components"""
        try:
            url = f"{self.base_url}/v1/address/parse/batch"
            
            json_data = {
                "addresses": addresses
            }
            
            logger.debug(f"[parse_address_batch] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[parse_address_batch] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Parse address batch error: {e}")
            return {"error": str(e)}
    
    def verify_email(self, email: str, **kwargs) -> Dict[str, Any]:
        """Verify a single email address"""
        try:
            url = f"{self.base_url}/v1/emails/verify"
            json_data = {"email": email}
            
            logger.debug(f"[verify_email] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[verify_email] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Email verification error: {e}")
            return {"error": str(e)}
    
    def verify_batch_emails(self, emails: List, **kwargs) -> Dict[str, Any]:
        """Verify a batch of email addresses - accepts either strings or objects"""
        try:
            url = f"{self.base_url}/v1/emails/verify/batch"
            
            # Convert string emails to objects if needed
            processed_emails = []
            for email in emails:
                if isinstance(email, str):
                    processed_emails.append({"email": email})
                elif isinstance(email, dict):
                    # If it's already an object, ensure it has the right format
                    if "email" in email:
                        processed_emails.append(email)
                    else:
                        # Try to find email-like keys
                        email_value = None
                        for key, value in email.items():
                            if "email" in key.lower() or "@" in str(value):
                                email_value = value
                                break
                        if email_value:
                            processed_emails.append({"email": email_value})
                        else:
                            logger.warning(f"Could not extract email from object: {email}")
                            
            json_data = {"emails": processed_emails}
            
            logger.debug(f"[verify_batch_emails] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[verify_batch_emails] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Batch email verification error: {e}")
            return {"error": str(e)}

    def get_neighborhoods_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get neighborhood information for an address using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_neighborhoods_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_neighborhoods_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Neighborhoods error: {e}")
            return {"error": str(e)}
    
    def get_schools_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get school information for an address using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
                "query": '''
                    query 
                    ($address: String!, $country: String) {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_schools_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_schools_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Schools error: {e}")
            return {"error": str(e)}
    
    def get_buildings_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get building information for an address using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_buildings_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_buildings_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Buildings error: {e}")
            return {"error": str(e)}
    
    def get_parcels_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get parcel information for an address using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_parcels_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_parcels_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Parcels error: {e}")
            return {"error": str(e)}
    
    def get_coastal_risk(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get coastal risk for a property"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_coastal_risk] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_coastal_risk] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Coastal risk error: {e}")
            return {"error": str(e)}
    
    def get_earth_risk(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get earthquake risk for a property"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_earth_risk] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_earth_risk] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Earthquake risk error: {e}")
            return {"error": str(e)}
    
    def get_property_fire_risk(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get fire risk for a property"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_property_fire_risk] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_property_fire_risk] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Fire risk error: {e}")
            return {"error": str(e)}
    
    def get_wildfire_risk_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get wildfire risk for a property by address"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_wildfire_risk_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_wildfire_risk_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Wildfire risk error: {e}")
            return {"error": str(e)}
    
    def get_flood_risk_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get flood risk for a property by address"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_flood_risk_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_flood_risk_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Flood risk error: {e}")
            return {"error": str(e)}
    
    def get_historical_weather_risk(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get historical weather risk for a property"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_historical_weather_risk] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_historical_weather_risk] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Historical weather risk error: {e}")
            return {"error": str(e)}
    
    def get_psyte_geodemographics_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get Psyte geodemographics by address using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_psyte_geodemographics_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_psyte_geodemographics_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Psyte geodemographics error: {e}")
            return {"error": str(e)}
    
    def get_ground_view_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get ground view demographics by address using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
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
                                percentPopulation25to29yearsPercent
                                percentPopulation65to69yearsPercent
                                maritalStatusNeverMarriedPercent
                                maritalStatusNowMarriedPercent
                                homeWorkers16yearsAndOverPercent
                                educationHighSchoolGraduatePercent
                                educationBachelorsDegreePercent
                                unemployedPercent
                                censusBlockGroupHouseholds
                                ownerOccupiedHousingUnitsPercent
                                renterOccupiedHousingUnitsPercent
                                averageVehiclesPerHousehold
                                averageRent
                                averageHomeValue
                                averageHouseholdIncome
                              }
                            }
                          }
                        }
                      }
                    }
                ''',
                "variables": {
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_ground_view_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_ground_view_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ground view error: {e}")
            return {"error": str(e)}
    
    def get_replacement_cost_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get replacement cost by address using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
                "query": '''
                    query GetReplacementCost($address: String!, $country: String) {
                      getByAddress(address: $address, country: $country) {
                        replacementCost(pageNumber: 1, pageSize: 10) {
                          metadata { vintage }
                          data { 
                            propertyAttributeID 
                            preciselyID 
                            replacementCostUSD 
                            replacementCostConfidenceCode 
                          }
                        }
                      }
                    }
                ''',
                "variables": {
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_replacement_cost_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_replacement_cost_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Replacement cost error: {e}")
            return {"error": str(e)}
    
    def get_property_attributes_by_address(self, address: str, country: str = "US", **kwargs) -> Dict[str, Any]:
        """Get property attributes by address using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = {
                "query": '''
                    query GetPropertyAttributes($address: String!, $country: String) {
                      getByAddress(address: $address, country: $country) {
                        propertyAttributes(pageNumber: 1, pageSize: 10) {
                          metadata { vintage }
                          data { 
                            propertyAttributeID 
                            preciselyID 
                            bedroomCount 
                            bathroomCount { value description }
                            roomCount 
                            yearBuilt
                            buildingSquareFootage
                            livingSquareFootage
                          }
                        }
                      }
                    }
                ''',
                "variables": {
                    "address": address,
                    "country": country
                }
            }
            
            logger.debug(f"[get_property_attributes_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_property_attributes_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Property attributes error: {e}")
            return {"error": str(e)}
    
    def psap_address(self, address: Dict, **kwargs) -> Dict[str, Any]:
        """Retrieve PSAP contact details using address input
        
        Required address structure:
        {
            "addressLines": ["860 White Plains Road Trumbull CT 06611, USA"],
            "admin1": "Connecticut",
            "admin2": "Trumbull",
            "city": "Trumbull",
            "postalCode": "06611"
        }
        """
        try:
            url = f"{self.base_url}/v1/emergency-info/psap/address"
            json_data = {"address": address}
            
            logger.debug(f"[psap_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[psap_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"PSAP address error: {e}")
            return {"error": str(e)}
    
    def psap_location(self, location: Dict, **kwargs) -> Dict[str, Any]:
        """Retrieve PSAP contact details using location input
        
        Required location structure:
        {
            "coordinates": [-73.22344, 41.23443]  # [longitude, latitude]
        }
        """
        try:
            url = f"{self.base_url}/v1/emergency-info/psap/location"
            json_data = {"location": location}
            
            logger.debug(f"[psap_location] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[psap_location] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"PSAP location error: {e}")
            return {"error": str(e)}
    
    def psap_ahj_address(self, address: Dict, **kwargs) -> Dict[str, Any]:
        """Retrieve PSAP+AHJ contact details using address input
        
        Required address structure:
        {
            "addressLines": ["860 White Plains Road Trumbull CT 06611, USA"],
            "admin1": "Connecticut",
            "admin2": "Trumbull",
            "city": "Trumbull",
            "postalCode": "06611"
        }
        """
        try:
            url = f"{self.base_url}/v1/emergency-info/psap-ahj/address"
            json_data = {"address": address}
            
            logger.debug(f"[psap_ahj_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[psap_ahj_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"PSAP AHJ address error: {e}")
            return {"error": str(e)}
    
    def psap_ahj_location(self, location: Dict, **kwargs) -> Dict[str, Any]:
        """Retrieve PSAP+AHJ contact details using location input
        
        Required location structure:
        {
            "coordinates": [-73.22344, 41.23443]  # [longitude, latitude]
        }
        """
        try:
            url = f"{self.base_url}/v1/emergency-info/psap-ahj/location"
            json_data = {"location": location}
            
            logger.debug(f"[psap_ahj_location] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[psap_ahj_location] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"PSAP AHJ location error: {e}")
            return {"error": str(e)}
    
    def psap_ahj_fccid(self, fcc_id: str, **kwargs) -> Dict[str, Any]:
        """Retrieve PSAP+AHJ contact details using FCC ID"""
        try:
            url = f"{self.base_url}/v1/emergency-info/psap-ahj/fccid"
            params = {"fccId": fcc_id}
            
            logger.debug(f"[psap_ahj_fccid] Request params: {params}")
            response = self.session.get(url, params=params)
            logger.debug(f"[psap_ahj_fccid] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"PSAP AHJ FCC ID error: {e}")
            return {"error": str(e)}
    
    def autocomplete(self, address: Dict, preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Address autocomplete suggestions"""
        try:
            url = f"{self.base_url}/v1/autocomplete"
            json_data = {
                "address": address,
                "preferences": preferences or {}
            }
            
            logger.debug(f"[autocomplete] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[autocomplete] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Autocomplete error: {e}")
            return {"error": str(e)}
    
    def autocomplete_postal_city(self, address: Dict, preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Autocomplete postal city API"""
        try:
            url = f"{self.base_url}/v1/autocomplete/postal-city"
            json_data = {
                "address": address,
                "preferences": preferences or {}
            }
            
            logger.debug(f"[autocomplete_postal_city] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[autocomplete_postal_city] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Autocomplete postal city error: {e}")
            return {"error": str(e)}
    
    def autocomplete_v2(self, address: Dict, preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Express autocomplete API (V2)"""
        try:
            url = f"{self.base_url}/v1/express-autocomplete"
            json_data = {
                "address": address,
                "preferences": preferences or {}
            }
            
            logger.debug(f"[autocomplete_v2] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[autocomplete_v2] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Autocomplete v2 error: {e}")
            return {"error": str(e)}
    
    def lookup(self, keys: List[Dict], preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup address details by PreciselyID"""
        try:
            url = f"{self.base_url}/v1/lookup"
            json_data = {
                "keys": keys,
                "preferences": preferences or {}
            }
            
            logger.debug(f"[lookup] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Lookup error: {e}")
            return {"error": str(e)}
    
    def lookup_by_address(self, address: Dict, preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup tax jurisdiction by address"""
        try:
            url = f"{self.base_url}/v1/geo-tax/address"
            json_data = {
                "address": address,
                "preferences": preferences or {}
            }
            
            logger.debug(f"[lookup_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tax jurisdiction by address error: {e}")
            return {"error": str(e)}
    
    def lookup_by_addresses(self, addresses: List[Dict], preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup tax jurisdiction for multiple addresses"""
        try:
            url = f"{self.base_url}/v1/geo-tax/address/batch"
            json_data = {
                "addresses": addresses,
                "preferences": preferences or {}
            }
            
            logger.debug(f"[lookup_by_addresses] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup_by_addresses] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tax jurisdiction by addresses error: {e}")
            return {"error": str(e)}
    
    def lookup_by_location(self, location: Dict, preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup tax jurisdiction by location"""
        try:
            url = f"{self.base_url}/v1/geo-tax/location"
            json_data = {
                "location": location,
                "preferences": preferences or {}
            }
            
            logger.debug(f"[lookup_by_location] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup_by_location] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tax jurisdiction by location error: {e}")
            return {"error": str(e)}
    
    def lookup_by_locations(self, locations: List[Dict], preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup tax jurisdiction for multiple locations"""
        try:
            url = f"{self.base_url}/v1/geo-tax/location/batch"
            json_data = {
                "locations": locations,
                "preferences": preferences or {}
            }
            
            logger.debug(f"[lookup_by_locations] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup_by_locations] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tax jurisdiction by locations error: {e}")
            return {"error": str(e)}
    
    def geo_locate_ip_address(self, ip_address: str, **kwargs) -> Dict[str, Any]:
        """Geolocate an IP address"""
        try:
            url = f"{self.base_url}/v1/geolocation/ip-address"
            params = {"ipAddress": ip_address}
            
            logger.debug(f"[geo_locate_ip_address] Request params: {params}")
            response = self.session.get(url, params=params)
            logger.debug(f"[geo_locate_ip_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"IP geolocation error: {e}")
            return {"error": str(e)}
    
    def geo_locate_wifi_access_point(self, wifi_data: Dict, **kwargs) -> Dict[str, Any]:
        """Geolocate a WiFi access point"""
        try:
            url = f"{self.base_url}/v1/geolocation/access-point"
            json_data = wifi_data
            
            logger.debug(f"[geo_locate_wifi_access_point] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[geo_locate_wifi_access_point] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"WiFi geolocation error: {e}")
            return {"error": str(e)}
    
    def get_addresses_detailed(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get detailed addresses using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            
            logger.debug(f"[get_addresses_detailed] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_addresses_detailed] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(response.json(), "get_addresses_detailed")
        except Exception as e:
            logger.error(f"Detailed addresses error: {e}")
            return {"error": str(e)}
    
    def get_parcel_by_owner_detailed(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get parcel by owner (detailed) using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            
            logger.debug(f"[get_parcel_by_owner_detailed] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_parcel_by_owner_detailed] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(response.json(), "get_parcel_by_owner_detailed")
        except Exception as e:
            logger.error(f"Parcel by owner detailed error: {e}")
            return {"error": str(e)}
    
    def get_address_family(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get address family using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            
            logger.debug(f"[get_address_family] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_address_family] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(response.json(), "get_address_family")
        except Exception as e:
            logger.error(f"Address family error: {e}")
            return {"error": str(e)}
    
    def get_serviceability(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get serviceability via GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            
            logger.debug(f"[get_serviceability] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_serviceability] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(response.json(), "get_serviceability")
        except Exception as e:
            logger.error(f"Serviceability error: {e}")
            return {"error": str(e)}
    
    def get_places_by_address(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get places (points of interest) by address via GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            
            logger.debug(f"[get_places_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_places_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(response.json(), "get_places_by_address")
        except Exception as e:
            logger.error(f"Places by address error: {e}")
            return {"error": str(e)}

    def get_by_spatial(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Run getBySpatial query via GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data

            logger.debug(f"[get_by_spatial] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_by_spatial] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(response.json(), "get_by_spatial")
        except Exception as e:
            logger.error(f"Get by spatial error: {e}")
            return {"error": str(e)}
    
    def parse_name(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Parse a name"""
        try:
            url = f"{self.base_url}/v1/names/parse"
            json_data = data
            
            logger.debug(f"[parse_name] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[parse_name] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Name parsing error: {e}")
            return {"error": str(e)}
    
    def validate_phone(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Validate a phone number"""
        try:
            url = f"{self.base_url}/v1/phone-numbers/validate"
            json_data = data
            
            logger.debug(f"[validate_phone] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[validate_phone] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Phone validation error: {e}")
            return {"error": str(e)}
    
    def validate_batch_phones(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Validate a batch of phone numbers"""
        try:
            url = f"{self.base_url}/v1/phone-numbers/validate/batch"
            json_data = data
            
            logger.debug(f"[validate_batch_phones] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[validate_batch_phones] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Batch phone validation error: {e}")
            return {"error": str(e)}
    
    def timezone_addresses(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get timezone for addresses"""
        try:
            url = f"{self.base_url}/v1/timezone/address"
            json_data = data
            
            logger.debug(f"[timezone_addresses] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[timezone_addresses] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Timezone addresses error: {e}")
            return {"error": str(e)}
    
    def timezone_locations(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get timezone for locations"""
        try:
            url = f"{self.base_url}/v1/timezone/location"
            json_data = data
            
            logger.debug(f"[timezone_locations] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[timezone_locations] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Timezone locations error: {e}")
            return {"error": str(e)}

    # ========================================
    # Spatial Analysis APIs
    # ========================================

    def find_nearest_candidates(self, tableName: str, attributes: list, location: dict, withinDistance: str, **kwargs) -> Dict[str, Any]:
        """Identifies the nearest locations or points of interest to a specified geometry or address based on distance or defined criteria, returning the spatial features in distance order with the distance value.

        Args:
            tableName (str): Name of the table containing the spatial data.
            attributes (list): Comma separated list of column names of enrich table to be included in the response. "*" can be used to specify all columns.
            location (dict): input for which spatial analysis is to be done. Can be a geometry or address
            withinDistance (str): The distance to search around the geometry.
            **kwargs: Additional keyword arguments passed to the API.
                attributeFilter (str): specifies filter on scalar attributes
                distanceAttributeName (str): The name of the distance attribute between input geometry and target geometry. Default value is "distance".
                maxFeatures (int): Maximum number of features returned against each geometry. Default value is 10 and minimum value is 1.
                uomAttributeName (str): Custom name of parameter showing unit of measurement for distance between input and target geometry. Default value is "uom".
                inputPointAttributeName (str): Custom name of parameter indicating point on input geometry which was used to calculate the distance. Default value is "inputPoint".
                targetPointAttributeName (str): Custom name of parameter indicating point on target geometry which was used to calculate the distance. Default value is "targetPoint".
                bearingAttributeName (str): Custom name of parameter for bearing value. Default value is "bearing".
                sortBy (str): Defines the attribute by which the results should be sorted.
                sortOrder (str): Specifies the order of sorting.
                limit (int): Specifies the maximum number of results to return.
                offset (int): Specifies the number of records to skip.

        Returns:
            Dict[str, Any]: GeoJSON FeatureCollection with keys 'type' (str), 'features' (list of Feature objects
                with properties and geometry), 'responseParameters' (dict with recordsMatched, recordsReturned),
                and 'Metadata' (list of attribute definitions with name and type).

        Example:
            find_nearest_candidates(
                tableName="/risks/flood_risk",
                attributes=["statecode", "type", "mapname"],
                location={"format": "WKT", "value": "MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211)))"},
                withinDistance="10 mi",
                attributeFilter="id > 100",
                distanceAttributeName="dist",
                maxFeatures=2,
                uomAttributeName="unit",
                inputPointAttributeName="ip",
                targetPointAttributeName="tp",
                bearingAttributeName="bearingAngle"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/findNearest"
            params = {}
            for p in ["sortBy", "sortOrder", "limit", "offset"]:
                if p in kwargs:
                    params[p] = kwargs[p]
            json_data = {"tableName": tableName, "attributes": attributes, "location": location, "withinDistance": withinDistance}
            for k in ["attributeFilter", "distanceAttributeName", "maxFeatures", "uomAttributeName", "inputPointAttributeName", "targetPointAttributeName", "bearingAttributeName"]:
                if k in kwargs:
                    json_data[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[find_nearest_candidates] POST {url}")
            logger.debug(f"[find_nearest_candidates] Request params: {params}")
            logger.debug(f"[find_nearest_candidates] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data, params=params, headers=headers)
            logger.debug(f"[find_nearest_candidates] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Find nearest candidates error: {e}")
            return {"error": str(e)}

    def search_at_location(self, tableName: str, attributes: list, location: dict, **kwargs) -> Dict[str, Any]:
        """Searches for locations or points of interest within or intersecting a defined geographic area(geometry or address) or a buffer around a specified location.

        Args:
            tableName (str): Name of the table containing the spatial data.
            attributes (list): Comma separated list of column names of enrich table to be included in the response. "*" can be used to specify all columns.
            location (dict): input for which spatial analysis is to be done. Can be a geometry or address
            **kwargs: Additional keyword arguments passed to the API.
                attributeFilter (str): specifies filter on scalar attributes
                spatialOperation (str): The type of spatial query. Possible values are: intersects, within, contains. Default value is "intersects".
                bufferDistance (str): Distance by which the input geometry will be extrapolated.
                sortBy (str): Defines the attribute by which the results should be sorted.
                sortOrder (str): Specifies the order of sorting.
                limit (int): Specifies the maximum number of results to return.
                offset (int): Specifies the number of records to skip.

        Returns:
            Dict[str, Any]: GeoJSON FeatureCollection with keys 'type' (str), 'features' (list of Feature objects
                with properties and geometry), 'responseParameters' (dict with recordsMatched, recordsReturned),
                and 'Metadata' (list of attribute definitions with name and type).

        Example:
            search_at_location(
                tableName="/risks/flood_risk",
                attributes=["statecode", "type", "mapname"],
                location={"format": "WKT", "value": "MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211)))"},
                spatialOperation="INTERSECTS",
                attributeFilter="id > 100",
                bufferDistance="10 mi"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/searchAtLocation"
            params = {}
            for p in ["sortBy", "sortOrder", "limit", "offset"]:
                if p in kwargs:
                    params[p] = kwargs[p]
            json_data = {"tableName": tableName, "attributes": attributes, "location": location}
            for k in ["attributeFilter", "spatialOperation", "bufferDistance"]:
                if k in kwargs:
                    json_data[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[search_at_location] POST {url}")
            logger.debug(f"[search_at_location] Request params: {params}")
            logger.debug(f"[search_at_location] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data, params=params, headers=headers)
            logger.debug(f"[search_at_location] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Search at location error: {e}")
            return {"error": str(e)}

    def overlap(self, tableName: str, attributes: list, location: dict, uom: str, **kwargs) -> Dict[str, Any]:
        """Identifies spatial intersections between a specified geometry or address in a chosen Enrich spatial table returning the overlap geometry with the percentage and area of overlap.

        Args:
            tableName (str): Name of the table containing the spatial data.
            attributes (list): Comma separated list of column names of enrich table to be included in the response. "*" can be used to specify all columns, will only include scalar columns
            location (dict): input for which spatial analysis is to be done. Can be a geometry or address
            uom (str): Unit of measurement used to return intersection length/area
            **kwargs: Additional keyword arguments passed to the API.
                attributeFilter (str): specifies filter on scalar attributes
                areaAttributeName (str): Custom name of intersection area parameter when intersection area is polygon. Default value is "intersectionArea".
                lengthAttributeName (str): Custom name of intersection length parameter when intersection area is linestring. Default value is "intersectionLength".
                percentTargetAttributeName (str): Custom name of parameter indicating percentage of overlap with target geometry. Default value is "percentageOfTarget".
                percentInputAttributeName (str): Custom name of parameter indicating percentage of overlap with input geometry. Default value is "percentageOfInput".
                uomAttributeName (str): Custom name of unit of measurement parameter. Default value is "uom".
                bufferDistance (str): Distance by which the input geometry will be extrapolated.
                limit (int): Specifies the maximum number of results to return.
                offset (int): Specifies the number of records to skip.

        Returns:
            Dict[str, Any]: GeoJSON FeatureCollection with keys 'type' (str), 'features' (list of Feature objects
                with properties including overlap area/length/percentage and geometry), 'responseParameters'
                (dict with recordsMatched, recordsReturned), and 'Metadata' (list of attribute definitions).

        Example:
            overlap(
                tableName="/properties/buildings",
                location={"format": "WKT", "value": "POLYGON ((-74.01316 40.700479, -74.012028 40.700479, -74.012028 40.701403, -74.01316 40.701403, -74.01316 40.700479))"},
                attributes=["fips"],
                uom="m",
                attributeFilter="elevation > 0",
                areaAttributeName="overlappedArea",
                lengthAttributeName="overlappedLength",
                percentTargetAttributeName="targetOverlapPercentage",
                percentInputAttributeName="inputOverlapPercentage",
                uomAttributeName="measurementUnit",
                bufferDistance="2 km"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/overlap"
            params = {}
            for p in ["limit", "offset"]:
                if p in kwargs:
                    params[p] = kwargs[p]
            json_data = {"tableName": tableName, "attributes": attributes, "location": location, "uom": uom}
            for k in ["attributeFilter", "areaAttributeName", "lengthAttributeName", "percentTargetAttributeName", "percentInputAttributeName", "uomAttributeName", "bufferDistance"]:
                if k in kwargs:
                    json_data[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[overlap] POST {url}")
            logger.debug(f"[overlap] Request params: {params}")
            logger.debug(f"[overlap] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data, params=params, headers=headers)
            logger.debug(f"[overlap] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Overlap error: {e}")
            return {"error": str(e)}

    def get_spatial_products(self, **kwargs) -> Dict[str, Any]:
        """Get a list of available Enrich Data products along with their metadata such as product family, applicable geographic area, vintage, available layers, appropriate zoom levels for display and styles to use.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: List of product metadata objects, each with keys 'productId' (str), 'productName' (str),
                'productFamily' (str), 'vintage' (str), 'geography' (str), and 'layers' (list of layer objects
                with layerId, displayName, featureTable, recommendedStyle, etc.).

        Example:
            get_spatial_products()
        """
        try:
            url = f"{self.base_url}/v1/spatial/products"
            logger.debug(f"[get_spatial_products] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[get_spatial_products] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Get spatial products error: {e}")
            return {"error": str(e)}

    def list_spatial_tables(self, **kwargs) -> Dict[str, Any]:
        """This endpoint retrieves a list of spatial tables from database

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: List of table name strings (e.g., ["/properties/buildings", "/risks/flood_risk", ...]).

        Example:
            list_spatial_tables()
        """
        try:
            url = f"{self.base_url}/v1/spatial/tables"
            logger.debug(f"[list_spatial_tables] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[list_spatial_tables] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"List spatial tables error: {e}")
            return {"error": str(e)}

    def get_table_metadata(self, tableName: str, **kwargs) -> Dict[str, Any]:
        """This endpoint retrieves a metadata information of a specific/given table from database

        Args:
            tableName (str): Name of table for which metadata request will be executed
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: Table metadata object with keys 'tableName' (str), 'geometryType' (str),
                'numberOfRows' (int), 'columns' (list of ColumnDetail objects with columnName, description,
                dataType), 'xMin' (float), 'xMax' (float), 'yMin' (float), 'yMax' (float).

        Example:
            get_table_metadata(tableName="risks/flood_risk")
        """
        try:
            # Remove leading slash if present for URL construction
            table_path = tableName.lstrip('/')
            url = f"{self.base_url}/v1/spatial/tables/{table_path}/metadata"
            logger.debug(f"[get_table_metadata] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[get_table_metadata] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Get table metadata error: {e}")
            return {"error": str(e)}

    def summarize(self, tableName: str, location: Dict, aggregateColumns: Dict, **kwargs) -> Dict[str, Any]:
        """Generates detailed data summaries within a user defined region(geometry or address), including total, average, minimum and maximum values for data such as population.

        Args:
            tableName (str): Name of the table containing the spatial data.
            location (dict): Input for which spatial analysis is to be done. Can be a geometry or address.
            aggregateColumns (dict): Columns to be aggregated and corresponding aggregation operations to be performed. Possible values are: min, max, avg, sum, median.
            **kwargs: Additional keyword arguments passed to the API.
                attributeFilter (str): specifies filter on scalar attributes
                spatialOperation (str): The type of spatial operation. Possible values are: intersects, within. Default value is "intersects".
                proportionalCalculation (bool): Determines if proportional calculations should be applied. Only applicable where the spatialOperation parameter is "intersects".
                bufferDistance (str): Distance by which the input geometry will be extrapolated.

        Returns:
            Dict[str, Any]: GeoJSON FeatureCollection with keys 'type' (str), 'features' (list of Feature objects
                with aggregated summary properties such as column_MIN, column_MAX, column_AVG, column_SUM,
                column_MEDIAN, and count).

        Example:
            summarize(
                tableName="/risks/historical_weather_windgrid",
                aggregateColumns={"w11": ["min", "max", "avg", "sum"], "w10": ["min", "max", "sum", "avg", "median"]},
                location={"format": "WKT", "value": "GEOMETRYCOLLECTION (MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211))), LINESTRING (-121.756899 37.653383, -121.158302 37.304645, -121.690998 37.120906))"},
                spatialOperation="intersects",
                attributeFilter="grid_id > 0",
                proportionalCalculation=True,
                bufferDistance="10 mi"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/summarize"
            json_data = {"tableName": tableName, "location": location, "aggregateColumns": aggregateColumns}
            for k in ["attributeFilter", "spatialOperation", "proportionalCalculation", "bufferDistance"]:
                if k in kwargs:
                    json_data[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[summarize] POST {url}")
            logger.debug(f"[summarize] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data, headers=headers)
            logger.debug(f"[summarize] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Summarize error: {e}")
            return {"error": str(e)}

    # ========================================
    # OGC Features APIs
    # ========================================

    def ogc_landing_page(self, **kwargs) -> Dict[str, Any]:
        """The landing page provides links to essential API resources, including:
- **API Definition:** A machine-readable specification of the API.
- **Conformance Declaration:** A list of standards that the API conforms to.
- **Feature Collections:** Information and links to the available feature collections in the dataset.

Use this endpoint to quickly navigate and explore the API's capabilities.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: LandingPageResponse with keys 'title' (str), 'description' (str),
                and 'links' (list of Link objects with href, rel, type, title).

        Example:
            ogc_landing_page()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/"
            logger.debug(f"[ogc_landing_page] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_landing_page] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC landing page error: {e}")
            return {"error": str(e)}

    def ogc_api_definition(self, **kwargs) -> Dict[str, Any]:
        """This endpoint retrieves the complete OpenAPI definition for the API. The response is a machine-readable specification that describes all available endpoints, request/response schemas, and security configurations.

- **Format:** The API definition conforms to the OpenAPI 3.0.1 standard.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: Complete OpenAPI 3.0.1 definition as a JSON object with keys 'openapi' (str),
                'info' (dict), 'servers' (list), 'paths' (dict), and 'components' (dict).

        Example:
            ogc_api_definition()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/api"
            # Required header per "Landing Page" endpoint response
            headers = {"Accept": "application/vnd.oai.openapi+json;version=3.0"}
            logger.debug(f"[ogc_api_definition] GET {url}")
            response = self.session.get(url, headers=headers)
            logger.debug(f"[ogc_api_definition] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC API definition error: {e}")
            return {"error": str(e)}

    def ogc_functions(self, **kwargs) -> Dict[str, Any]:
        """This endpoint returns a list of available spatial functions within the API.
- **Purpose:** Provides supported spatial functions that can be used for querying features.
- **Function Metadata:** Includes function names, argument types, and return types.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: FunctionResponse with key 'functions' (list of Function objects,
                each with 'name' (str), 'arguments' (list of type arrays), and 'returns' (list of str)).

        Example:
            ogc_functions()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/functions"
            logger.debug(f"[ogc_functions] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_functions] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC functions error: {e}")
            return {"error": str(e)}

    def ogc_conformance(self, **kwargs) -> Dict[str, Any]:
        """This endpoint returns the conformance declaration for the API. The conformance declaration is a list of all conformance classes specified in a standard that the server adheres to. It helps clients determine whether the API meets the required standards and their own requirements.

- **Purpose:** Provides a comprehensive list of conformance classes to verify the API's compliance with OGC API standards and additional specifications.
- **Standards:** Includes OGC API conformance classes and any extra specifications the API supports.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: ConformancePageResponse with key 'conformsTo' (list of conformance class URI strings).

        Example:
            ogc_conformance()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/conformance"
            logger.debug(f"[ogc_conformance] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_conformance] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC conformance error: {e}")
            return {"error": str(e)}

    def ogc_collections(self, **kwargs) -> Dict[str, Any]:
        """This endpoint returns the list of feature collections available on the server. Each collection represents a spatial dataset that can be queried and provides essential metadata, including:

- **Collection ID:** A unique identifier for the spatial dataset.
- **Title and Description:** Optional details that describe the collection.
- **Spatial and Temporal Extents:** Indicators of the geographical and time-based coverage of the data.
- **Coordinate Reference Systems (CRS):** A list of supported CRS, with the first being the default (typically WGS 84).
- **Links:** Navigational links to access the collection’s items (e.g., `/collections/{collectionId}/items`).

This resource is designed to help clients discover available geospatial datasets and understand the structure of each collection before making queries.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: CollectionsResponse with keys 'links' (list of Link objects) and
                'collections' (list of CollectionsInfo objects with id, title, description, itemType, links).

        Example:
            ogc_collections()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections"
            logger.debug(f"[ogc_collections] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_collections] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collections error: {e}")
            return {"error": str(e)}

    def ogc_collection(self, collectionId: str, **kwargs) -> Dict[str, Any]:
        """This resource describes the feature collection identified in the path.

Information about the feature collection with id `{collectionId}` is provided. The response contains:

- A link to the items in the collection (path `/collections/{collectionId}/items`, relation: items).
- A unique local identifier for the collection.
- A list of coordinate reference systems (CRS) in which geometries may be returned; the first CRS is the default (typically WGS 84 with axis order longitude/latitude).
- An optional title and description for the collection.
- An optional spatial and temporal extent derived from the data.
- An optional indicator of the item type (default is 'feature').

        Args:
            collectionId (str): Unique identifier of the collection.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: CollectionIdResponse with keys 'id' (str), 'title' (str), 'description' (str),
                'itemType' (str), and 'links' (list of Link objects with href, rel, type, title).

        Example:
            ogc_collection(collectionId="properties/buildings")
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}"
            logger.debug(f"[ogc_collection] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_collection] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collection error: {e}")
            return {"error": str(e)}

    def ogc_collection_schema(self, collectionId: str, **kwargs) -> Dict[str, Any]:
        """This resource provides the schema for a specified feature collection. The schema defines the structure of the collection and includes details such as field names, data types, formats, and descriptions.

The **collection id** is a unique identifier used to reference a specific dataset. When you provide a collection id, the response includes:

- **Field Names:** Names of each attribute in the collection.
- **Data Types & Formats:** The expected data type (e.g., string, integer, double) and format for each field.
- **Descriptions:** Explanatory details for each attribute to clarify its purpose.
- **Geospatial Data Types:** Specific spatial types for any geospatial attributes, along with the default coordinate reference system.

This information is essential for validating client queries and constructing dynamic interfaces.

        Args:
            collectionId (str): Unique identifier of the collection.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: DescribeCollectionResponse with keys '$schema' (str), '$id' (str),
                'type' (str), 'title' (str), 'description' (str), and 'properties' (dict of field name
                to SchemaProperties with title, description, format).

        Example:
            ogc_collection_schema(collectionId="properties/buildings")
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}/schema"
            logger.debug(f"[ogc_collection_schema] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_collection_schema] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collection schema error: {e}")
            return {"error": str(e)}

    def ogc_collection_queryables(self, collectionId: str, **kwargs) -> Dict[str, Any]:
        """This resource returns the queryable properties for a specific collection identified by its unique id. Queryable properties provide detailed metadata for each attribute available in the collection that can be used to filter queries. The response includes information such as:

- **Field Names:** The names of the attributes in the collection.
- **Descriptions:** A description of each attribute to clarify its purpose and usage.
- **Formats:** The data types or formats (e.g., string, number, geospatial) of each attribute.
- **Geospatial Data Types:** Specific spatial types for attributes that support geospatial queries.

This metadata is essential for clients to build dynamic query interfaces and validate their requests against the collection's schema.

        Args:
            collectionId (str): Unique identifier of the collection.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: QueryableResponse (JSON Schema) with keys '$schema' (str), '$id' (str),
                'type' (str), 'title' (str), 'description' (str), 'properties' (dict of queryable
                field name to PropertyInfo with title, description, format), and 'additionalProperties' (bool).

        Example:
            ogc_collection_queryables(collectionId="properties/buildings")
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}/queryables"
            logger.debug(f"[ogc_collection_queryables] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_collection_queryables] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collection queryables error: {e}")
            return {"error": str(e)}

    def ogc_collection_items(self, collectionId: str, **kwargs) -> Dict[str, Any]:
        """Fetch features of the feature collection with id `{collectionId}`.

Every feature in a dataset belongs to a collection. A dataset may consist of multiple feature collections, each representing a group of features that share a common schema and type.

The **collection id** is a unique identifier for the spatial dataset and is used to reference a specific collection within the API.

Additional capabilities include:
- **Filtering:** Supports attribute-based filtering using CQL (Common Query Language).
- **Pagination:** Use `limit` and `offset` parameters to paginate results.
- **Spatial Queries:**
  - **Bounding Box (bbox):** Retrieve features within a rectangular spatial extent (`minX, minY, maxX, maxY`).
  - **Spatial Filters:** Support for `contains`, `intersects`, and `within` (OGC Filter Encoding).

        Args:
            collectionId (str): Unique identifier of the collection.
            **kwargs: Additional keyword arguments passed to the API.
                limit (str): Number of items to return (max: 10,000).
                offset (str): Offset for pagination.
                bbox (str): Bounding box for spatial filtering (minX, minY, maxX, maxY).
                filter (str): Filter query in CQL format.

        Returns:
            Dict[str, Any]: FeatureCollectionResponse (GeoJSON) with keys 'type' (str), 'features'
                (list of Feature objects with properties, geometry, and optional id), 'timeStamp' (str),
                and 'links' (list of Link objects for pagination).

        Example:
            ogc_collection_items(collectionId="properties/buildings", limit=100, offset=0)
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}/items"
            params = {}
            for k in ["limit", "offset", "bbox", "filter"]:
                if k in kwargs:
                    params[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[ogc_collection_items] GET {url}")
            logger.debug(f"[ogc_collection_items] Request params: {params}")
            response = self.session.get(url, params=params, headers=headers)
            logger.debug(f"[ogc_collection_items] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collection items error: {e}")
            return {"error": str(e)}

    def ogc_feature_by_id(self, collectionId: str, featureId: str, **kwargs) -> Dict[str, Any]:
        """Retrieves a single feature in GeoJSON format,

        Args:
            collectionId (str): Unique collection identifier
            featureId (str): Unique feature identifier
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: FeatureCollectionResponse (GeoJSON) with keys 'type' (str), 'features'
                (list containing the single Feature with properties, geometry, and id), 'timeStamp' (str),
                and 'links' (list of Link objects).

        Example:
            ogc_feature_by_id(collectionId="properties/buildings", featureId="1")
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}/items/{featureId}"
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[ogc_feature_by_id] GET {url}")
            response = self.session.get(url, headers=headers)
            logger.debug(f"[ogc_feature_by_id] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC feature by ID error: {e}")
            return {"error": str(e)}

    # ========================================
    # WMS (Web Map Service) APIs
    # ========================================

    def wms_get_request(self, **kwargs) -> Dict[str, Any]:
        """Processes WMS requests: GetCapabilities, GetMap, GetFeatureInfo. WMS service errors (ServiceExceptionReport) with HTTP 2xx are raised as exceptions and returned as {"error": <xml>}.

        Args:
            **kwargs: Additional keyword arguments passed to the API.
                REQUEST (str): WMS request type
                SERVICE (str): Service type
                VERSION (str): WMS version
                crs (str): crs
                srs (str): srs
                BBOX (str): BBOX
                width (str): width
                height (str): height
                layers (str): layers
                Info_Format (str): Info_Format
                QUERY_LAYERS (str): QUERY_LAYERS
                I (str): I
                J (str): J
                X (str): X
                Y (str): Y
                Feature_Count (str): Feature_Count
                PIXELSEARCHRADIUS (str): PIXELSEARCHRADIUS
                STYLES (str): STYLES
                FORMAT (str): FORMAT
                TRANSPARENT (str): TRANSPARENT
                BGCOLOR (str): BGCOLOR
                RESOLUTION (str): RESOLUTION
                EXCEPTIONS (str): EXCEPTIONS

        Returns:
            Dict[str, Any]: For GetMap success: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).
                For GetCapabilities success: Dict with keys 'xml' (str), 'content_type' (str).
                For GetFeatureInfo success: JSON response dict, or Dict with keys 'xml' (str), 'content_type' (str) for XML info_format.
                On any error (HTTP 4xx/5xx or WMS ServiceException): Dict with key 'error' (str) containing the error detail or ServiceExceptionReport XML.

        Example:
            wms_get_request(REQUEST="GetCapabilities", SERVICE="WMS", VERSION="1.3.0")
        """
        try:
            url = f"{self.base_url}/v1/spatial/wms"
            params = {}
            for k in ["REQUEST", "SERVICE", "VERSION", "crs", "srs", "BBOX", "width", "height", "layers", "Info_Format", "QUERY_LAYERS", "I", "J", "X", "Y", "Feature_Count", "PIXELSEARCHRADIUS", "STYLES", "FORMAT", "TRANSPARENT", "BGCOLOR", "RESOLUTION", "EXCEPTIONS"]:
                if k in kwargs:
                    params[k] = kwargs[k]
            request_type = kwargs.get("REQUEST", "").upper()
            logger.debug(f"[wms_get_request] GET {url}")
            logger.debug(f"[wms_get_request] Request params: {params}")
            # Override Accept header: Various Accept headers will be needed based on "REQUEST" and params
            response = self.session.get(url, params=params, headers={"Accept": "*/*"})
            content_type = response.headers.get("Content-Type", "")
            if "image" in content_type:
                logger.debug(f"[wms_get_request] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wms_get_request] Raw response: {response.text}")
            response.raise_for_status()
            # WMS returns HTTP 200 for service errors; raise for consistent error handling
            if "image" not in content_type and "<ServiceException" in response.text:
                raise ValueError(response.text)
            if request_type == "GETMAP":
                if "image" in content_type:
                    return {
                        "image_base64": base64.b64encode(response.content).decode(),
                        "content_type": content_type,
                        "size_bytes": len(response.content)
                    }
                return {"xml": response.text, "content_type": content_type}
            if request_type == "GETCAPABILITIES":
                return {"xml": response.text, "content_type": content_type}
            if request_type == "GETFEATUREINFO":
                if "json" in content_type:
                    return response.json()
                return {"xml": response.text, "content_type": content_type}
            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMS get request error: {e}")
            return {"error": str(e)}

    def wms_post_get_map(self, **kwargs) -> Dict[str, Any]:
        """Processes WMS GetMap requests using a POST method. Accepts SLD_BODY as a form parameter (URL-encoded JSON). WMS service errors (ServiceExceptionReport) with HTTP 2xx are raised as exceptions and returned as {"error": <xml>}.

        Args:
            **kwargs: Additional keyword arguments passed to the API.
                REQUEST (str): WMS request type
                SERVICE (str): Service type
                VERSION (str): WMS version ('1.3.0' uses crs; '1.1.1' uses srs)
                crs (str): Coordinate reference system for WMS 1.3.0 (e.g. 'CRS:84', 'EPSG:4326', 'EPSG:3857')
                srs (str): Spatial reference system for WMS 1.1.1 (e.g. 'EPSG:4326', 'EPSG:3857')
                BBOX (str): BBOX
                width (str): width
                height (str): height
                layers (str): layers
                STYLES (str): Comma-separated list of style names, one per requested layer. MUST always be supplied. Omitting STYLES entirely causes a server-side StyleNotDefined error.
                FORMAT (str): FORMAT
                TRANSPARENT (str): TRANSPARENT
                DPI (str): DPI hint (accepted by server but silently ignored — has no effect on output).
                MAP_RESOLUTION (str): Map resolution hint (accepted by server but silently ignored — has no effect on output).
                FORMAT_OPTIONS (str): Additional format options e.g. 'dpi:96' (accepted by server but silently ignored — has no effect on output).
                SLD_BODY (str): URL-encoded JSON style definition. Use empty string ('') or omit entirely to use default server styles. NOTE: passing SLD_BODY='{}' (JSON empty object string) causes a server-side InvalidStyleDetails error — always use SLD_BODY='' or omit.

        Returns:
            Dict[str, Any]: On success: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).
                On any error (HTTP 4xx/5xx or WMS ServiceException): Dict with key 'error' (str) containing the error detail or ServiceExceptionReport XML.

        Example:
            wms_post_get_map(
                REQUEST="GetMap",
                SERVICE="WMS",
                VERSION="1.3.0",
                crs="CRS:84",
                BBOX="-122.712622,38.035008,-122.692382,38.045271",
                width="640",
                height="480",
                layers="wildfire_risk",
                FORMAT="image/png",
                STYLES=""
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/wms"
            params = {}
            for k in ["REQUEST", "SERVICE", "VERSION", "crs", "srs", "BBOX", "width", "height", "layers", "STYLES", "FORMAT", "TRANSPARENT"]:
                if k in kwargs:
                    params[k] = kwargs[k]
            form_data = {}
            if "SLD_BODY" in kwargs:
                form_data["SLD_BODY"] = kwargs["SLD_BODY"]
            # Build per-request headers to avoid mutating shared session headers (thread safety)
            headers = dict(self.session.headers)
            headers.pop("Content-Type", None)
            headers["Accept"] = "image/png"
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            logger.debug(f"[wms_post_get_map] POST {url}")
            logger.debug(f"[wms_post_get_map] Request params: {params}")
            response = self.session.post(url, params=params, data=form_data, headers=headers)
            content_type = response.headers.get("Content-Type", "")
            if "image" in content_type:
                logger.debug(f"[wms_post_get_map] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wms_post_get_map] Raw response: {response.text}")
            response.raise_for_status()
            # WMS returns HTTP 200 for service errors; raise for consistent error handling
            if "image" not in content_type and "<ServiceException" in response.text:
                raise ValueError(response.text)
            if "image" in content_type:
                return {
                    "image_base64": base64.b64encode(response.content).decode(),
                    "content_type": content_type,
                    "size_bytes": len(response.content)
                }
            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMS POST GetMap error: {e}")
            return {"error": str(e)}

    # ========================================
    # WMTS (Web Map Tile Service) APIs
    # ========================================

    def wmts_request(self, **kwargs) -> Dict[str, Any]:
        """Use the appropriate parameters based on the request type.

        Args:
            **kwargs: Additional keyword arguments passed to the API.
                Service (str): Specifies the service type (must be `WMTS`).
                Request (str): Defines the request type. Available values : GetCapabilities, GetTile
                Version (str): WMTS version.
                Layer (str): Available layer name via Data or Repository (required for `GetTile`).
                Style (str): Comma-separated list of one rendering style per requested layer(required for `GetTile`).
                TileMatrixSet (str): Tile matrix set to generate tiles for(required for `GetTile`).
                TileMatrix (str): An integer value which will be number of levels or zoom level(required for `GetTile`).
                TileRow (int): An integer value that specifies the row number of the tile you want (required for `GetTile`).
                TileCol (int): An integer value that specifies the column number of the tile you want (required for `GetTile`).
                Format (str): The format in which the map image is to be returned(required for `GetTile`).

        Returns:
            Dict[str, Any]: For GetTile: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).
                For GetCapabilities: Dict with keys 'xml' (str), 'content_type' (str).

        Example:
            wmts_request(Service="WMTS", Request="GetCapabilities")
        """
        try:
            url = f"{self.base_url}/v1/spatial/wmts"
            params = {}
            for k in ["Service", "Request", "Version", "Layer", "Style", "TileMatrixSet", "TileMatrix", "TileRow", "TileCol", "Format"]:
                if k in kwargs:
                    params[k] = kwargs[k]
            logger.debug(f"[wmts_request] GET {url}")
            logger.debug(f"[wmts_request] Request params: {params}")

            response = self.session.get(url, params=params)
            content_type = response.headers.get("Content-Type", "")

            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                logger.debug(f"[wmts_request] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wmts_request] Raw response: {response.text}")

            response.raise_for_status()

            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                return {
                    "image_base64": base64.b64encode(response.content).decode(),
                    "content_type": content_type,
                    "size_bytes": len(response.content)
                }

            if "xml" in content_type.lower() or kwargs.get("Request", "").upper() == "GETCAPABILITIES":
                return {
                    "xml": response.text,
                    "content_type": content_type or "application/xml"
                }

            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMTS request error: {e}")
            return {"error": str(e)}

    def wmts_get_standard_tile(self, Version: str, Layer: str, Style: str, TileMatrixSet: str, TileMatrix: str, TileCol: int, TileRow: int, Format: str, **kwargs) -> Dict[str, Any]:
        """Returns a map tile based on the RESTful encoding for the WMTS service.


        Args:
            Version (str): WMTS version (default is `1.0.0`).
            Layer (str): Available layer name via Data or Repository.
            Style (str): Comma-separated list of one rendering style per requested layer.
            TileMatrixSet (str): Tile matrix set to generate tiles for.
            TileMatrix (str): Level of detail (zoom level).
            TileCol (int): An integer value that specifies the column number of the tile you want.
            TileRow (int): An integer value that specifies the row number of the tile you want.
            Format (str): Image format extension.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).

        Example:
            wmts_get_standard_tile(
                Version="1.0.0",
                Layer="parcels",
                Style="default",
                TileMatrixSet="WorldWebMercatorQuad_0_to_19",
                TileMatrix="17",
                TileCol=31118,
                TileRow=50069,
                Format="png"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/wmts/{Version}/default/tiles/{Layer}/{Style}/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.{Format}"
            logger.debug(f"[wmts_get_standard_tile] GET {url}")
            params = {
                "Version": Version,
                "Layer": Layer,
                "Style": Style,
                "TileMatrixSet": TileMatrixSet,
                "TileMatrix": TileMatrix,
                "TileCol": TileCol,
                "TileRow": TileRow,
                "Format": Format,
            }
            logger.debug(f"[wmts_get_standard_tile] Request params: {params}")

            response = self.session.get(url)
            content_type = response.headers.get("Content-Type", "")

            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                logger.debug(f"[wmts_get_standard_tile] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wmts_get_standard_tile] Raw response: {response.text}")

            response.raise_for_status()

            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                return {
                    "image_base64": base64.b64encode(response.content).decode(),
                    "content_type": content_type,
                    "size_bytes": len(response.content)
                }

            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMTS get standard tile error: {e}")
            return {"error": str(e)}

    def wmts_get_simple_tile(self, Version: str, Layer: str, TileMatrix: str, TileCol: int, TileRow: int, Format: str, **kwargs) -> Dict[str, Any]:
        """Returns a map tile based on the RESTful encoding for the WMTS service.

        Args:
            Version (str): WMTS version (default is `1.0.0`).
            Layer (str): Available layer name via Data or Repository.
            TileMatrix (str): Level of detail (zoom level).
            TileCol (int): An integer value that specifies the column number of the tile you want.
            TileRow (int): An integer value that specifies the row number of the tile you want.
            Format (str): Image format extension.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).

        Example:
            wmts_get_simple_tile(
                Version="1.0.0",
                Layer="parcels",
                TileMatrix="17",
                TileCol=31118,
                TileRow=50069,
                Format="png"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/wmts/{Version}/simpleProfileTile/tiles/{Layer}/{TileMatrix}/{TileCol}/{TileRow}.{Format}"
            logger.debug(f"[wmts_get_simple_tile] GET {url}")
            params = {
                "Version": Version,
                "Layer": Layer,
                "TileMatrix": TileMatrix,
                "TileCol": TileCol,
                "TileRow": TileRow,
                "Format": Format,
            }
            logger.debug(f"[wmts_get_simple_tile] Request params: {params}")

            response = self.session.get(url)
            content_type = response.headers.get("Content-Type", "")

            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                logger.debug(f"[wmts_get_simple_tile] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wmts_get_simple_tile] Raw response: {response.text}")

            response.raise_for_status()

            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                return {
                    "image_base64": base64.b64encode(response.content).decode(),
                    "content_type": content_type,
                    "size_bytes": len(response.content)
                }

            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMTS get simple tile error: {e}")
            return {"error": str(e)}
