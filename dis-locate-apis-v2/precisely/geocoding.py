"""Geocoding and address API methods."""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class GeocodingMixin:
    def geocode(self, address: str, **kwargs) -> Dict[str, Any]:
        """Convert address to coordinates using correct payload structure"""
        try:
            url = f"{self.base_url}/v1/geocode"
            json_data = {
                "preferences": {
                    "maxResults": kwargs.get("maxResults", 1),
                    "returnAllInfo": kwargs.get("returnAllInfo", True),
                    "clientLocale": kwargs.get("clientLocale", "en_US"),
                },
                "addresses": [
                    {
                        "addressId": "1",
                        "addressLines": [address],
                        "country": kwargs.get("country", "USA"),
                    }
                ],
            }
            logger.debug(f"[geocode] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[geocode] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            return self._build_error("Geocoding", e)

    def reverse_geocode(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        """Convert coordinates to address using correct payload structure"""
        try:
            url = f"{self.base_url}/v1/reverse-geocode"
            json_data = {
                "preferences": {
                    "maxResults": kwargs.get("maxResults", 1),
                    "returnAllInfo": kwargs.get("returnAllInfo", True),
                    "clientLocale": kwargs.get("clientLocale", "en_US"),
                },
                "locations": [
                    {
                        "addressId": "1",
                        "longitude": lon,
                        "latitude": lat,
                        "country": kwargs.get("country", "USA"),
                    }
                ],
            }
            logger.debug(f"[reverse_geocode] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[reverse_geocode] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Reverse geocoding error: {e}")
            return self._build_error("Reverse geocoding", e)

    def verify_address(self, address: str, **kwargs) -> Dict[str, Any]:
        """Verify and standardize address using correct payload structure"""
        try:
            url = f"{self.base_url}/v1/verify"
            json_data = {
                "preferences": {
                    "returnAllInfo": kwargs.get("returnAllInfo", True),
                    "clientLocale": kwargs.get("clientLocale", "en_US"),
                },
                "addresses": [
                    {
                        "addressId": "1",
                        "addressLines": [address],
                        "country": kwargs.get("country", "USA"),
                    }
                ],
            }
            logger.debug(f"[verify_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[verify_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Address verification error: {e}")
            return self._build_error("Address verification", e)

    def parse_addresses(self, addresses, **kwargs) -> Dict[str, Any]:
        """Parse one or more free-text addresses into structured components.

        Accepts a single address string or a list of address objects.
        Always uses the batch endpoint; a single string is auto-wrapped.

        Args:
            addresses: A single address string (e.g., "1700 District Ave #300, Burlington, MA 01803"),
                or a list of dicts with 'address' (and optional 'id') keys.
                Maximum 10 addresses per call.
        """
        try:
            url = f"{self.base_url}/v1/address/parse/batch"

            # Normalize input → list of {"address": ...} dicts
            if isinstance(addresses, str):
                processed_addresses = [{"address": addresses}]
            elif isinstance(addresses, list):
                processed_addresses = addresses
            else:
                return self._build_error(
                    "Address parsing",
                    ValueError(
                        "'addresses' must be a string (single address) or a list of "
                        "dicts with 'address' key (multiple addresses)."
                    ),
                )

            if not processed_addresses:
                return self._build_error(
                    "Address parsing",
                    ValueError("No addresses provided."),
                )

            json_data = {"addresses": processed_addresses}
            logger.debug(f"[parse_addresses] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[parse_addresses] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Address parsing error: {e}")
            return self._build_error("Address parsing", e)

    def autocomplete_address(
        self,
        address: Dict,
        preferences: Dict = None,
        express: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """Autocomplete addresses, postal codes, or city names.

        Routes to the correct endpoint based on address structure:
        - addressLines present → street address autocomplete (standard or express)
        - postAddress present → postal code / city name autocomplete

        Args:
            address: Address input — either {addressLines, country, ...} for street
                or {postAddress, country, type?} for postal/city.
            preferences: Optional preferences (e.g., maxResults).
            express: When True, uses the faster express engine for street address
                autocomplete. Ignored for postal/city lookups.
        """
        is_street = "addressLines" in address
        is_postal = "postAddress" in address

        if not is_street and not is_postal:
            return {
                "error": {
                    "message": (
                        "Address must contain either 'addressLines' (for street autocomplete) "
                        "or 'postAddress' (for postal/city autocomplete)."
                    ),
                    "error_type": "ValidationError",
                }
            }

        try:
            if is_postal:
                url = f"{self.base_url}/v1/autocomplete/postal-city"
            elif express:
                url = f"{self.base_url}/v1/express-autocomplete"
            else:
                url = f"{self.base_url}/v1/autocomplete"

            json_data = {"address": address, "preferences": preferences or {}}
            logger.debug(f"[autocomplete_address] POST {url}")
            logger.debug(f"[autocomplete_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[autocomplete_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Autocomplete address error: {e}")
            return self._build_error("Autocomplete address", e)

    def lookup(self, keys: List[Dict], preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup address details by PreciselyID"""
        try:
            url = f"{self.base_url}/v1/lookup"
            json_data = {"keys": keys, "preferences": preferences or {}}
            logger.debug(f"[lookup] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Lookup error: {e}")
            return self._build_error("Lookup", e)
