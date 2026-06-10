"""Advanced GraphQL API methods (8 tools — 5 LLM-constructed + 3 curated datalink queries)."""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Curated GeoX query templates (address mode)
# ---------------------------------------------------------------------------

_GEOX_PROPERTY_FIELDS = """
                buildingID footprintID centerLongitude centerLatitude coordinateReferenceSystem
                footprintAreaSquareFootage yearBuilt occupancy occupancyOfClosestBuildings
                landUseDescription maximumBuildingHeightFeet minimumGroundHeightFeet
                numberOfStories squareFootage poolCount poolEnclosureCount
                temporaryPoolCount trampolineCount numberOfBuildingsInParcel
                imageDate modelRunDate""".strip()

_GEOX_ROOF_FIELDS = """
                buildingID footprintID centerLongitude centerLatitude coordinateReferenceSystem
                roofType flatAreaSquareFootage hipAreaSquareFootage
                roofMaterial roofCondition rustAreaSquareFootage pondingAreaSquareFootage
                tarpEvidence discolorationAreaSquareFootage solarPanelAreaSquareFootage
                airConditionerCount imageDate modelRunDate""".strip()

_GEOX_VEGETATION_FIELDS = """
                buildingID footprintID centerLongitude centerLatitude coordinateReferenceSystem
                treeOverhangPercent distanceToTreeFeet distanceToShrubFeet distanceToVegetationFeet
                treeZone1Percent treeZone2Percent treeZone3Percent treeZone4Percent
                shrubZone1Percent shrubZone2Percent shrubZone3Percent shrubZone4Percent
                vegetationZone1Percent vegetationZone2Percent vegetationZone3Percent vegetationZone4Percent
                imageDate modelRunDate""".strip()

_METADATA_FIELDS = "pageNumber pageCount totalPages count vintage"


class GraphQLAdvancedMixin:
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
            return self._build_error("Detailed addresses", e)

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
            return self._build_error("Parcel by owner detailed", e)

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
            return self._build_error("Address family", e)

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
            return self._build_error("Serviceability", e)

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
            return self._build_error("Places by address", e)

    # ------------------------------------------------------------------
    # Curated datalink helpers — address OR id+queryType
    # ------------------------------------------------------------------

    def _call_datalink(
        self,
        tool_name: str,
        gql_field: str,
        data_fields: str,
        address: str | None,
        entity_id: str | None,
        query_type: str | None,
    ) -> Dict[str, Any]:
        """Shared implementation for curated datalink GeoX tools."""
        has_address = bool(address)
        has_id_mode = bool(entity_id and query_type)

        if has_address and has_id_mode:
            raise ValueError(
                f"[{tool_name}] Provide only one lookup mode: either 'address' or both 'id' and 'queryType', not both."
            )
        if not has_address and not has_id_mode:
            raise ValueError(
                f"[{tool_name}] Must provide either 'address' or both 'id' and 'queryType'."
            )

        if has_address:
            json_data = {
                "query": (
                    f"query Get{gql_field}ByAddress($address: String!) {{"
                    f" getByAddress(address: $address) {{"
                    f" {gql_field} {{"
                    f" metadata {{ {_METADATA_FIELDS} }}"
                    f" data {{ {data_fields} }}"
                    f" }} }} }}"
                ),
                "variables": {"address": address},
            }
        else:
            json_data = {
                "query": (
                    f"query Get{gql_field}ById($id: String!, $queryType: QueryType!) {{"
                    f" getById(id: $id, queryType: $queryType) {{"
                    f" {gql_field} {{"
                    f" metadata {{ {_METADATA_FIELDS} }}"
                    f" data {{ {data_fields} }}"
                    f" }} }} }}"
                ),
                "variables": {"id": entity_id, "queryType": query_type},
            }

        url = f"{self.base_url}/data-graph/graphql"
        logger.debug(f"[{tool_name}] Request payload: {json.dumps(json_data, indent=2)}")
        response = self.session.post(url, json=json_data)
        logger.debug(f"[{tool_name}] Raw response: {response.text}")
        response.raise_for_status()
        return self._validate_graphql_response(response.json(), tool_name)

    def get_datalink_geox_property(
        self,
        address: str | None = None,
        id: str | None = None,
        queryType: str | None = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get Data Link GeoX Property by address or by ID. Premium: 5+ credits/call."""
        try:
            return self._call_datalink(
                "get_datalink_geox_property",
                "datalinkGeoXProperty",
                _GEOX_PROPERTY_FIELDS,
                address,
                id,
                queryType,
            )
        except Exception as e:
            logger.error(f"Data Link GeoX Property error: {e}")
            return self._build_error("Data Link GeoX Property", e)

    def get_datalink_geox_roof(
        self,
        address: str | None = None,
        id: str | None = None,
        queryType: str | None = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get Data Link GeoX Roof by address or by ID. Premium: 7+ credits/call."""
        try:
            return self._call_datalink(
                "get_datalink_geox_roof",
                "datalinkGeoXRoof",
                _GEOX_ROOF_FIELDS,
                address,
                id,
                queryType,
            )
        except Exception as e:
            logger.error(f"Data Link GeoX Roof error: {e}")
            return self._build_error("Data Link GeoX Roof", e)

    def get_datalink_geox_vegetation(
        self,
        address: str | None = None,
        id: str | None = None,
        queryType: str | None = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get Data Link GeoX Vegetation by address or by ID. Premium: 3+ credits/call."""
        try:
            return self._call_datalink(
                "get_datalink_geox_vegetation",
                "datalinkGeoXVegetation",
                _GEOX_VEGETATION_FIELDS,
                address,
                id,
                queryType,
            )
        except Exception as e:
            logger.error(f"Data Link GeoX Vegetation error: {e}")
            return self._build_error("Data Link GeoX Vegetation", e)
