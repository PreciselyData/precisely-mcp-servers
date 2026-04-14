"""IP and WiFi geolocation API methods."""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class GeolocationMixin:
    def geo_locate_ip_address(self, ip_address: str, **kwargs) -> Dict[str, Any]:
        """Geolocate an IP address"""
        try:
            url = f"{self.base_url}/v1/geolocation/ip-address"
            params = {"ipAddress": ip_address}
            logger.debug(f"[geo_locate_ip_address] Request params: {params}")
            response = self.session.get(url, params=params)
            logger.debug(f"[geo_locate_ip_address] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"IP geolocation error: {e}")
            return {"error": str(e)}

    def geo_locate_wifi_access_point(self, wifi_data: Dict, **kwargs) -> Dict[str, Any]:
        """Geolocate a WiFi access point"""
        try:
            url = f"{self.base_url}/v1/geolocation/access-point"
            json_data = wifi_data
            logger.debug(f"[geo_locate_wifi_access_point] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[geo_locate_wifi_access_point] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"WiFi geolocation error: {e}")
            return {"error": str(e)}
