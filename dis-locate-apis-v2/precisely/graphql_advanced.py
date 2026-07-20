"""Advanced GraphQL API methods (LLM constructs queries directly)."""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class GraphQLAdvancedMixin:
    def get_addresses_detailed(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get detailed addresses using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            logger.debug(
                f"[get_addresses_detailed] Request payload: {json.dumps(json_data, indent=2)}"
            )
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_addresses_detailed] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(
                response.json(), "get_addresses_detailed"
            )
        except Exception as e:
            logger.error(f"Detailed addresses error: {e}")
            return self._build_error("Detailed addresses", e)

    def get_parcel_by_owner_detailed(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get parcel by owner (detailed) using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            logger.debug(
                f"[get_parcel_by_owner_detailed] Request payload: {json.dumps(json_data, indent=2)}"
            )
            response = self.session.post(url, json=json_data)
            logger.debug(
                f"[get_parcel_by_owner_detailed] Raw response: {response.text}"
            )
            response.raise_for_status()
            return self._validate_graphql_response(
                response.json(), "get_parcel_by_owner_detailed"
            )
        except Exception as e:
            logger.error(f"Parcel by owner detailed error: {e}")
            return self._build_error("Parcel by owner detailed", e)

    def get_address_family(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get address family using GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            logger.debug(
                f"[get_address_family] Request payload: {json.dumps(json_data, indent=2)}"
            )
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_address_family] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(
                response.json(), "get_address_family"
            )
        except Exception as e:
            logger.error(f"Address family error: {e}")
            return self._build_error("Address family", e)

    def get_serviceability(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get serviceability via GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            logger.debug(
                f"[get_serviceability] Request payload: {json.dumps(json_data, indent=2)}"
            )
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_serviceability] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(
                response.json(), "get_serviceability"
            )
        except Exception as e:
            logger.error(f"Serviceability error: {e}")
            return self._build_error("Serviceability", e)

    def get_places_by_address(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Get places (points of interest) by address via GraphQL"""
        try:
            url = f"{self.base_url}/data-graph/graphql"
            json_data = data
            logger.debug(
                f"[get_places_by_address] Request payload: {json.dumps(json_data, indent=2)}"
            )
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_places_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(
                response.json(), "get_places_by_address"
            )
        except Exception as e:
            logger.error(f"Places by address error: {e}")
            return self._build_error("Places by address", e)

    def get_datalink_dun_bradstreet(
        self,
        address: str | None = None,
        id: str | None = None,
        queryType: str | None = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get Data Link Dun & Bradstreet by address OR by ID via curated GraphQL."""
        try:
            has_address = bool(address)
            has_id_mode = bool(id and queryType)

            if has_address == has_id_mode:
                raise ValueError(
                    "Provide exactly one mode: either 'address' or both 'id' and 'queryType'."
                )

            url = f"{self.base_url}/data-graph/graphql"

            if has_address:
                json_data = {
                    "query": """
                                                query GetDatalinkDunBradstreetByAddress($address: String!) {
                                                    getByAddress(address: $address) {
                                                        datalinkDunAndBradstreet {
                                                            metadata {
                                                                pageNumber
                                                                pageCount
                                                                totalPages
                                                                count
                                                                vintage
                                                            }
                                                            data {
                                                                placeId
                                                                vintage
                                                                linkId
                                                                linkIdVintage
                                                                linkIdType
                                                                preciselyId
                                                                preciselyIdVintage
                                                                parentPreciselyId
                                                            }
                                                        }
                                                    }
                                                }
                                        """,
                    "variables": {"address": address},
                }
            else:
                json_data = {
                    "query": """
                                                query GetDatalinkDunBradstreetById($id: String!, $queryType: QueryType!) {
                                                    getById(id: $id, queryType: $queryType) {
                                                        datalinkDunAndBradstreet {
                                                            metadata {
                                                                pageNumber
                                                                pageCount
                                                                totalPages
                                                                count
                                                                vintage
                                                            }
                                                            data {
                                                                placeId
                                                                vintage
                                                                linkId
                                                                linkIdVintage
                                                                linkIdType
                                                                preciselyId
                                                                preciselyIdVintage
                                                                parentPreciselyId
                                                            }
                                                        }
                                                    }
                                                }
                                        """,
                    "variables": {"id": id, "queryType": queryType},
                }

            logger.debug(
                f"[get_datalink_dun_bradstreet] Request payload: {json.dumps(json_data, indent=2)}"
            )
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_datalink_dun_bradstreet] Raw response: {response.text}")
            response.raise_for_status()
            return self._validate_graphql_response(
                response.json(), "get_datalink_dun_bradstreet"
            )
        except Exception as e:
            logger.error(f"Data Link Dun & Bradstreet error: {e}")
            return self._build_error("Data Link Dun & Bradstreet", e)
