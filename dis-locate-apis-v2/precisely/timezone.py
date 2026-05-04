"""Timezone API methods."""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class TimezoneMixin:
    def get_timezones(self, addresses: List[Dict] = None, locations: List[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Look up timezones by addresses or geographic coordinates.

        Accepts either an addresses array or a locations array (not both).
        Routes to the correct API endpoint based on which input is provided.

        Args:
            addresses: List of address objects with timestamp and address
                (addressLines, country, optional id). Uses /v1/timezone/address.
            locations: List of location objects with id, timestamp, and geometry
                (coordinates as [lon, lat]). Uses /v1/timezone/location.
        """
        try:
            if addresses and locations:
                return self._build_error(
                    "Get timezones",
                    ValueError("Provide either 'addresses' or 'locations', not both."),
                )

            if addresses:
                url = f"{self.base_url}/v1/timezone/address"
                json_data = {"addresses": addresses}
            elif locations:
                url = f"{self.base_url}/v1/timezone/location"
                json_data = {"locations": locations}
            else:
                return self._build_error(
                    "Get timezones",
                    ValueError("Provide either 'addresses' or 'locations'."),
                )

            logger.debug(f"[get_timezones] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[get_timezones] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Get timezones error: {e}")
            return self._build_error("Get timezones", e)
