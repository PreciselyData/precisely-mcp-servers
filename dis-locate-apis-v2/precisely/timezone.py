"""Timezone API methods."""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class TimezoneMixin:
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
            return self._build_error("Timezone addresses", e)

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
            return self._build_error("Timezone locations", e)
