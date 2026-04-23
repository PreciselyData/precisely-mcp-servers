"""Property risk GraphQL API methods (9 tools)."""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class PropertyRiskMixin:
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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_property_data] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_property_data] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Property data error: {e}")
            return self._build_error("Property data", e)

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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_property_attributes_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_property_attributes_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Property attributes error: {e}")
            return self._build_error("Property attributes", e)

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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_replacement_cost_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_replacement_cost_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Replacement cost error: {e}")
            return self._build_error("Replacement cost", e)

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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_flood_risk_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_flood_risk_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Flood risk error: {e}")
            return self._build_error("Flood risk", e)

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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_wildfire_risk_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_wildfire_risk_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Wildfire risk error: {e}")
            return self._build_error("Wildfire risk", e)

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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_property_fire_risk] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_property_fire_risk] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Fire risk error: {e}")
            return self._build_error("Fire risk", e)

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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_earth_risk] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_earth_risk] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Earthquake risk error: {e}")
            return self._build_error("Earthquake risk", e)

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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_coastal_risk] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_coastal_risk] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Coastal risk error: {e}")
            return self._build_error("Coastal risk", e)

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
                "variables": {"address": address, "country": country},
            }
            logger.debug(f"[get_historical_weather_risk] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_historical_weather_risk] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Historical weather risk error: {e}")
            return self._build_error("Historical weather risk", e)
