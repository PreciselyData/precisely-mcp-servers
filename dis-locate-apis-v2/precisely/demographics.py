"""Demographics GraphQL API methods (8 tools)."""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class DemographicsMixin:
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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_demographics] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_demographics] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Demographics error: {e}")
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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_crime_index] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_crime_index] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Crime index error: {e}")
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
                "variables": {"address": address, "country": country},
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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_ground_view_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_ground_view_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ground view error: {e}")
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
                "variables": {"address": address, "country": country},
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
                    query ($address: String!, $country: String) {
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
                "variables": {"address": address, "country": country},
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
                "variables": {"address": address, "country": country},
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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_parcels_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_parcels_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Parcels error: {e}")
            return {"error": str(e)}
