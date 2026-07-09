"""Routing API methods."""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class RoutingMixin:
    """Routing endpoints for matrix, directions, and reachable-area requests."""

    def calculate_travel_time_and_distance(
        self,
        request_body: Dict[str, Any],
        option: str = "flexible",
        x_request_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """POST /v1/matrix/location

        Computes ETA and distance matrix for origin/destination sets.
        """
        try:
            url = f"{self.base_url}/v1/matrix/location"
            params = {"option": option}
            headers = {}
            if x_request_id:
                headers["X-Request-Id"] = x_request_id

            logger.debug(f"[calculate_travel_time_and_distance] POST {url}")
            logger.debug(f"[calculate_travel_time_and_distance] Params: {params}")
            response = self.session.post(url, params=params, json=request_body, headers=headers)
            logger.debug(f"[calculate_travel_time_and_distance] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Travel matrix error: {e}")
            return self._build_error("Calculate travel matrix", e)

    def calculate_route_directions(
        self,
        request_body: Dict[str, Any],
        option: str = "flexible",
        x_request_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """POST /v1/direction/location

        Computes route details between origin/destination with optional waypoints.
        """
        try:
            url = f"{self.base_url}/v1/direction/location"
            params = {"option": option}
            headers = {}
            if x_request_id:
                headers["X-Request-Id"] = x_request_id

            logger.debug(f"[calculate_route_directions] POST {url}")
            logger.debug(f"[calculate_route_directions] Params: {params}")
            response = self.session.post(url, params=params, json=request_body, headers=headers)
            logger.debug(f"[calculate_route_directions] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Route directions error: {e}")
            return self._build_error("Calculate route directions", e)

    def calculate_reachable_area(
        self,
        x_request_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """GET /v1/isochrone/location

        Calculate reachable area boundaries for a single start location.
        """
        try:
            url = f"{self.base_url}/v1/isochrone/location"
            headers = {}
            if x_request_id:
                headers["X-Request-Id"] = x_request_id

            params = {k: v for k, v in kwargs.items() if v is not None}

            logger.debug(f"[calculate_reachable_area] GET {url}")
            logger.debug(f"[calculate_reachable_area] Params: {params}")
            response = self.session.get(url, params=params, headers=headers)
            logger.debug(f"[calculate_reachable_area] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Reachable area error: {e}")
            return self._build_error("Calculate reachable area", e)
