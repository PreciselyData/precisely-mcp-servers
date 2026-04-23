"""Tax jurisdiction and emergency (PSAP) API methods."""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class TaxEmergencyMixin:
    def lookup_by_address(self, address: Dict, preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup tax jurisdiction by address"""
        try:
            url = f"{self.base_url}/v1/geo-tax/address"
            json_data = {"address": address, "preferences": preferences or {}}
            logger.debug(f"[lookup_by_address] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup_by_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tax jurisdiction by address error: {e}")
            return self._build_error("Tax jurisdiction by address", e)

    def lookup_by_addresses(self, addresses: List[Dict], preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup tax jurisdiction for multiple addresses"""
        try:
            url = f"{self.base_url}/v1/geo-tax/address/batch"
            json_data = {"addresses": addresses, "preferences": preferences or {}}
            logger.debug(f"[lookup_by_addresses] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup_by_addresses] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tax jurisdiction by addresses error: {e}")
            return self._build_error("Tax jurisdiction by addresses", e)

    def lookup_by_location(self, location: Dict, preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup tax jurisdiction by location"""
        try:
            url = f"{self.base_url}/v1/geo-tax/location"
            json_data = {"location": location, "preferences": preferences or {}}
            logger.debug(f"[lookup_by_location] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup_by_location] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tax jurisdiction by location error: {e}")
            return self._build_error("Tax jurisdiction by location", e)

    def lookup_by_locations(self, locations: List[Dict], preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Lookup tax jurisdiction for multiple locations"""
        try:
            url = f"{self.base_url}/v1/geo-tax/location/batch"
            json_data = {"locations": locations, "preferences": preferences or {}}
            logger.debug(f"[lookup_by_locations] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[lookup_by_locations] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tax jurisdiction by locations error: {e}")
            return self._build_error("Tax jurisdiction by locations", e)

    def lookup_tax_jurisdiction(self, input_type: str, records: List[Dict], preferences: Dict = None, **kwargs) -> Dict[str, Any]:
        """Consolidated tax jurisdiction lookup: single or batch, address or coordinate input.

        Args:
            input_type: 'address' or 'location'
            records: list of address dicts or location dicts (length >= 1)
            preferences: optional lookup preferences
        """
        VALID_INPUT_TYPES = {"address", "location"}
        if input_type not in VALID_INPUT_TYPES:
            return {
                "error": (
                    f"Invalid input_type '{input_type}'. "
                    f"Must be one of: {sorted(VALID_INPUT_TYPES)}. "
                    "Use 'address' when records contain street addresses, "
                    "or 'location' when records contain longitude/latitude coordinates."
                )
            }
        if not records or not isinstance(records, list):
            return {"error": "records must be a non-empty list."}

        if input_type == "address":
            for i, rec in enumerate(records):
                if not isinstance(rec, dict) or "addressLines" not in rec:
                    return {
                        "error": (
                            f"records[{i}] is missing required field 'addressLines'. "
                            "Each address record must include: "
                            '{"addressLines": ["..."], "city": "...", "admin1": "...", "postalCode": "..."}'
                        )
                    }
            try:
                if len(records) == 1:
                    return self.lookup_by_address(address=records[0], preferences=preferences)
                return self.lookup_by_addresses(addresses=records, preferences=preferences)
            except Exception as e:
                logger.error(f"Tax jurisdiction lookup error: {e}")
                return self._build_error("Tax jurisdiction lookup", e)

        # input_type == "location"
        for i, rec in enumerate(records):
            if not isinstance(rec, dict) or "longitude" not in rec or "latitude" not in rec:
                return {
                    "error": (
                        f"records[{i}] is missing 'longitude' or 'latitude'. "
                        "Each location record must include: "
                        '{"longitude": <number>, "latitude": <number>}'
                    )
                }
            if not isinstance(rec["longitude"], (int, float)) or not isinstance(rec["latitude"], (int, float)):
                return {
                    "error": f"records[{i}]: longitude and latitude must be numeric values."
                }
        try:
            if len(records) == 1:
                return self.lookup_by_location(location=records[0], preferences=preferences)
            return self.lookup_by_locations(locations=records, preferences=preferences)
        except Exception as e:
            logger.error(f"Tax jurisdiction lookup error: {e}")
            return self._build_error("Tax jurisdiction lookup", e)

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
            return self._build_error("PSAP address", e)

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
            return self._build_error("PSAP location", e)

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
            return self._build_error("PSAP AHJ address", e)

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
            return self._build_error("PSAP AHJ location", e)

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
            return self._build_error("PSAP AHJ FCC ID", e)
