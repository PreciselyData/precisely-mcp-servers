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
            return {"error": str(e)}

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
            return {"error": str(e)}

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
            return {"error": str(e)}

    def parse_address(self, address: str, **kwargs) -> Dict[str, Any]:
        """Parse a single-line address into structured components"""
        try:
            url = f"{self.base_url}/v1/address/parse"
            json_data = {"address": address}
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
            json_data = {"addresses": addresses}
            logger.debug(f"[parse_address_batch] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[parse_address_batch] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Parse address batch error: {e}")
            return {"error": str(e)}

    def autocomplete(self, address: Dict, preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Address autocomplete suggestions"""
        try:
            url = f"{self.base_url}/v1/autocomplete"
            json_data = {"address": address, "preferences": preferences or {}}
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
            json_data = {"address": address, "preferences": preferences or {}}
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
            json_data = {"address": address, "preferences": preferences or {}}
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
            json_data = {"keys": keys, "preferences": preferences or {}}
            logger.debug(f"[lookup] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Lookup error: {e}")
            return {"error": str(e)}
