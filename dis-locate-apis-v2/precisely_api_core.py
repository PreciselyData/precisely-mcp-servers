"""
Precisely API Core Module for MCP Server
Production-ready module containing the PreciselyAPI class for MCP server use.
Pure API functionality with minimal dependencies.
"""

import json
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
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.cloud.precisely.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
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
            return response.json()
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
            return response.json()
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
            return response.json()
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
            return response.json()
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
            return response.json()
        except Exception as e:
            logger.error(f"Places by address error: {e}")
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

