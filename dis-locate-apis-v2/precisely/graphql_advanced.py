"""Advanced GraphQL API methods (6 tools — 5 LLM-constructed + 1 curated datalink query)."""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Curated historical sales query — full deed + loan field set
# ---------------------------------------------------------------------------

_METADATA_FIELDS = "pageNumber pageCount totalPages count vintage"

_HISTORICAL_SALES_FIELDS = (
    # Core IDs
    "historicalPropertyAttributeID propertyAttributeID "
    "preciselyID parentPreciselyID plinkID "
    # Seller parties
    "sellerFirstName sellerLastName sellerIDCode { value description } "
    "seller2FirstName seller2LastName seller2IDCode { value description } "
    "sellerMailAddress sellerMailCity sellerMailState sellerMailPostalCode "
    # Buyer parties
    "buyerFirstName buyerLastCorporationName buyerIDCode { value description } "
    "buyer2FirstName buyer2LastCorporationName buyer2IDCode { value description } "
    "buyerVestCode { value description } "
    "buyerMailCareOf buyerMailAddress buyerMailCity buyerMailState buyerMailPostalCode "
    # Property identifiers
    "addressLine city state postalCode postalCodeExtension "
    "propertyAPN apnSequence { value description } fips "
    "propertyUseCode { value description } "
    # Deed / recording
    "deedDocumentTypeCode { value description } "
    "interFamily recordingDate recordersBookNumber recordersPageNumber recordersDocumentNumber "
    "partialInterestTransferred { value description } "
    # Legal description
    "legalLotCode { value description } "
    "legalLotNumbers legalBlock legalSection legalDistrict legalLandLot legalUnit "
    "legalCityTownshipMunicipality legalSubdivisionName legalPhaseNumber legalTractNumber "
    "legalShortDescription legalSectionTownshipRangeMeridian "
    "legalDescriptionCode { value description } "
    # Transaction financials
    "recordersMapReference deedTransactionType { value description } "
    "recorderDocumentNumber contractDate salesPriceUSD salesPriceCode { value description } "
    "cityTransferTax stateTransferTax totalTransferTax "
    # Loan / mortgage
    "lenderName lenderType { value description } "
    "loanAmountUSD loanType { value description } financingType { value description } "
    "initialRate dueDate loanAmountSecondUSD "
    "adjustableRateRider { value description } adjustableRateIndex { value description } "
    "changeIndex rateChangeFrequency { value description } "
    "interestRateAdjustableMaximum interestRateAdjustableMinimum interestRateMaximum "
    "interestOnlyPeriod interestRate { value description } "
    "fixedChangeDateYear fixedChangeFullDateMonthDay "
    "prepaymentRider { value description } prepaymentTermPenalty "
    "titleCompanyName realEstateOwnedFlag { value description } distressedSaleFlag "
    "loanOriginatorOrganizationIDNumber loanOrganizationName "
    "mortgageBrokerNMLSID mortgageBroker loanOfficerNMLSID loanOfficerName "
    "loanTransactionType { value description }"
)


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
    # Curated datalink helper — address OR id+queryType
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
        """Shared implementation for curated datalink tools."""
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

    def get_historical_sales(
        self,
        address: str | None = None,
        id: str | None = None,
        queryType: str | None = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get full deed and loan history for a property by address or ID."""
        try:
            return self._call_datalink(
                "get_historical_sales",
                "historicalSales",
                _HISTORICAL_SALES_FIELDS,
                address,
                id,
                queryType,
            )
        except Exception as e:
            logger.error(f"Historical sales error: {e}")
            return self._build_error("Historical sales", e)
