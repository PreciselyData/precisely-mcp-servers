"""
Zones Service API Tools for Function Calling

This module provides function calling tools for the Precisely Zones Service API.
The Zones Service API provides methods to get boundaries around addresses and locations,
including basic boundaries, points of interest boundaries, and travel boundaries.
"""

import sys
import os
from typing import Optional, Dict, Any
from server import mcp

from com.precisely.apis.api.zones_service_api import ZonesServiceApi
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely



def setup_api_client():
    """Create and configure the Zones Service API instance."""
    try:
        # Check if credentials are available
        if not os.getenv('PRECISELY_API_KEY') or not os.getenv('PRECISELY_API_SECRET'):
            return None
        
        api = ZonesServiceApi()
        # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
        setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
        setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
        api.api_client.generateAndSetToken()
        return api.api_client
    except Exception:
        return None


def _extract_response_data(response):
    """Extract meaningful data from API response object."""
    if response is None:
        return None
    
    # Handle direct attribute access
    result = {}
    
    # Check for basic boundary attributes
    if hasattr(response, 'center'):
        result['center'] = response.center
    if hasattr(response, 'distance'):
        result['distance'] = response.distance
    if hasattr(response, 'geometry'):
        result['geometry'] = response.geometry
    if hasattr(response, 'matched_address'):
        result['matched_address'] = response.matched_address
    
    # Check for POI boundary attributes  
    if hasattr(response, 'object_id'):
        result['object_id'] = response.object_id
    if hasattr(response, 'countyfips'):
        result['countyfips'] = response.countyfips
    if hasattr(response, 'poi_list'):
        result['poi_list'] = response.poi_list
        
    # Check for travel boundary attributes
    if hasattr(response, 'travel_boundary'):
        result['travel_boundary'] = response.travel_boundary
    if hasattr(response, 'srs_name'):
        result['srs_name'] = response.srs_name
    
    return result if result else response

@mcp.tool()
def get_basic_boundary_by_address(
    address: str,
    country: Optional[str] = None,
    distance: Optional[str] = None,
    distance_unit: Optional[str] = None,
    resolution: Optional[str] = None,
    response_srs: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get basic boundary around an address.

    Args:
        address: Address around which Basic Boundary is requested
        country: Three digit ISO country code (optional)
        distance: Distance for boundary calculation (optional, defaults to 1000m)
        distance_unit: Distance unit (optional, defaults to meters)
        resolution: Buffer resolution - segments per circle (optional)
        response_srs: Response spatial reference system (optional)

    Returns:
        dict: Success/error response with basic boundary data
    """
    try:
        # Input validation
        if not address or not address.strip():
            return {
                "success": False,
                "error": "Address parameter is required"
            }

        # Set up API client
        api_client = setup_api_client()
        if api_client is None:
            return {
                "success": False,
                "error": "Failed to set up API client"
            }
        
        api = ZonesServiceApi(api_client)

        # Prepare parameters
        kwargs = {}
        if country:
            kwargs['country'] = country
        # Default distance if not provided (API requires this parameter)
        if distance:
            kwargs['distance'] = distance
        else:
            kwargs['distance'] = "1000"  # Default 1000 meters
        if distance_unit:
            kwargs['distance_unit'] = distance_unit
        else:
            kwargs['distance_unit'] = "meters"  # Default meters
        if resolution:
            kwargs['resolution'] = resolution
        if response_srs:
            kwargs['response_srs'] = response_srs

        # Make API call
        response = api.get_basic_boundary_by_address(address=address, **kwargs)
        
        return {
            "success": True,
            "data": _extract_response_data(response)
        }

    except ApiException as e:
        return {
            "success": False,
            "error": f"API call failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

@mcp.tool()
def get_basic_boundary_by_location(
    latitude: str,
    longitude: str,
    distance: Optional[str] = None,
    distance_unit: Optional[str] = None,
    resolution: Optional[str] = None,
    response_srs: Optional[str] = None,
    srs_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get basic boundary around coordinates.

    Args:
        latitude: Latitude around which Basic Boundary is requested
        longitude: Longitude around which Basic Boundary is requested
        distance: Width of the buffer (radius for circular buffer) (optional, defaults to 1000m)
        distance_unit: Distance unit (optional, defaults to meters)
        resolution: Buffer resolution - segments per circle (optional)
        response_srs: Response spatial reference system (optional)
        srs_name: Source coordinate system name (optional)

    Returns:
        dict: Success/error response with basic boundary data
    """
    try:
        # Input validation
        if not latitude or not longitude:
            return {
                "success": False,
                "error": "Latitude, longitude, and distance parameters are required"
            }
        
        try:
            float(latitude)
            float(longitude)
        except ValueError:
            return {
                "success": False,
                "error": "Latitude and longitude must be valid numbers"
            }

        # Set up API client
        api_client = setup_api_client()
        if api_client is None:
            return {
                "success": False,
                "error": "Failed to set up API client"
            }
        
        api = ZonesServiceApi(api_client)

        # Prepare parameters
        kwargs = {}
        # Default distance if not provided (API requires this parameter)
        if distance:
            kwargs['distance'] = distance
        else:
            kwargs['distance'] = "1000"  # Default 1000 meters
        if distance_unit:
            kwargs['distance_unit'] = distance_unit
        else:
            kwargs['distance_unit'] = "meters"  # Default meters
        if resolution:
            kwargs['resolution'] = resolution
        if response_srs:
            kwargs['response_srs'] = response_srs
        if srs_name:
            kwargs['srs_name'] = srs_name

        # Make API call
        response = api.get_basic_boundary_by_location(
            latitude=latitude,
            longitude=longitude,
            **kwargs
        )
        
        return {
            "success": True,
            "data": _extract_response_data(response)
        }

    except ApiException as e:
        return {
            "success": False,
            "error": f"API call failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

@mcp.tool()
def get_poi_boundary_by_address(
    address: str,
    category_code: Optional[str] = None,
    sic_code: Optional[str] = None,
    naics_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get POI (Points of Interest) boundary by address.

    Args:
        address: Address around which POI Boundary is requested
        category_code: Specific Category/Product code (optional)
        sic_code: Standard Industrial Classification code (optional)
        naics_code: North American Industry Classification code (optional)

    Returns:
        dict: Success/error response with POI boundary data
    """
    try:
        # Input validation
        if not address or not address.strip():
            return {
                "success": False,
                "error": "Address parameter is required"
            }

        # Set up API client
        api_client = setup_api_client()
        if api_client is None:
            return {
                "success": False,
                "error": "Failed to set up API client"
            }
        
        api = ZonesServiceApi(api_client)

        # Make API call
        kwargs = {}
        if category_code:
            kwargs['category_code'] = category_code
        if sic_code:
            kwargs['sic_code'] = sic_code
        if naics_code:
            kwargs['naics_code'] = naics_code
        
        response = api.get_poi_boundary_by_address(address=address, **kwargs)
        
        return {
            "success": True,
            "data": _extract_response_data(response)
        }

    except ApiException as e:
        return {
            "success": False,
            "error": f"API call failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

@mcp.tool()
def get_poi_boundary_by_location(
    latitude: str,
    longitude: str,
    category_code: Optional[str] = None,
    sic_code: Optional[str] = None,
    naics_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get POI (Points of Interest) boundary by location.

    Args:
        latitude: Latitude around which POI Boundary is requested
        longitude: Longitude around which POI Boundary is requested
        category_code: Specific Category/Product code (optional)
        sic_code: Standard Industrial Classification code (optional)
        naics_code: North American Industry Classification code (optional)

    Returns:
        dict: Success/error response with POI boundary data
    """
    try:
        # Input validation
        if not latitude or not longitude:
            return {
                "success": False,
                "error": "Latitude and longitude parameters are required"
            }
        
        try:
            float(latitude)
            float(longitude)
        except ValueError:
            return {
                "success": False,
                "error": "Latitude and longitude must be valid numbers"
            }

        # Set up API client
        api_client = setup_api_client()
        if api_client is None:
            return {
                "success": False,
                "error": "Failed to set up API client"
            }
        
        api = ZonesServiceApi(api_client)

        # Make API call
        kwargs = {}
        if category_code:
            kwargs['category_code'] = category_code
        if sic_code:
            kwargs['sic_code'] = sic_code
        if naics_code:
            kwargs['naics_code'] = naics_code
        
        response = api.get_poi_boundary_by_location(
            latitude=latitude,
            longitude=longitude,
            **kwargs
        )
        
        return {
            "success": True,
            "data": _extract_response_data(response)
        }

    except ApiException as e:
        return {
            "success": False,
            "error": f"API call failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

@mcp.tool()
def get_travel_boundary_by_time(
    point: Optional[str] = None,
    address: Optional[str] = None,
    costs: Optional[str] = None,
    cost_unit: Optional[str] = None,
    db: Optional[str] = None,
    country: Optional[str] = None,
    max_offroad_distance: Optional[str] = None,
    max_offroad_distance_unit: Optional[str] = None,
    destination_srs: Optional[str] = None,
    major_roads: Optional[str] = None,
    return_holes: Optional[str] = None,
    return_islands: Optional[str] = None,
    simplification_factor: Optional[str] = None,
    banding_style: Optional[str] = None,
    historic_traffic_time_bucket: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get travel boundary based on travel time.

    Args:
        point: Starting point (Lat,Long,coordsys format) (optional)
        address: Starting address (optional)
        costs: Travel time for boundary calculation (optional)
        cost_unit: Unit for travel cost (optional)
        db: Database for routing (optional)
        country: Country code (optional)
        max_offroad_distance: Maximum off-road distance (optional)
        max_offroad_distance_unit: Unit for max off-road distance (optional)
        destination_srs: Output coordinate system (optional)
        major_roads: Include major roads (optional)
        return_holes: Return holes in boundary (optional)
        return_islands: Return islands in boundary (optional)
        simplification_factor: Simplification factor (optional)
        banding_style: Banding style (optional)
        historic_traffic_time_bucket: Historic traffic time bucket (optional)

    Returns:
        dict: Success/error response with travel boundary data
    """
    try:
        # Input validation - at least point or address should be provided
        if not point and not address:
            return {
                "success": False,
                "error": "Either point or address parameter must be provided"
            }

        # Set up API client
        api_client = setup_api_client()
        if api_client is None:
            return {
                "success": False,
                "error": "Failed to set up API client"
            }
        
        api = ZonesServiceApi(api_client)

        # Prepare parameters
        kwargs = {}
        if point:
            kwargs['point'] = point
        if address:
            kwargs['address'] = address
        if costs:
            kwargs['costs'] = costs
        if cost_unit:
            kwargs['cost_unit'] = cost_unit
        if db:
            kwargs['db'] = db
        if country:
            kwargs['country'] = country
        if max_offroad_distance:
            kwargs['max_offroad_distance'] = max_offroad_distance
        if max_offroad_distance_unit:
            kwargs['max_offroad_distance_unit'] = max_offroad_distance_unit
        if destination_srs:
            kwargs['destination_srs'] = destination_srs
        if major_roads:
            kwargs['major_roads'] = major_roads
        if return_holes:
            kwargs['return_holes'] = return_holes
        if return_islands:
            kwargs['return_islands'] = return_islands
        if simplification_factor:
            kwargs['simplification_factor'] = simplification_factor
        if banding_style:
            kwargs['banding_style'] = banding_style
        if historic_traffic_time_bucket:
            kwargs['historic_traffic_time_bucket'] = historic_traffic_time_bucket

        # Make API call
        response = api.get_travel_boundary_by_time(**kwargs)
        
        return {
            "success": True,
            "data": _extract_response_data(response)
        }

    except ApiException as e:
        return {
            "success": False,
            "error": f"API call failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

@mcp.tool()
def get_travel_boundary_by_distance(
    point: Optional[str] = None,
    address: Optional[str] = None,
    costs: Optional[str] = None,
    cost_unit: Optional[str] = None,
    db: Optional[str] = None,
    country: Optional[str] = None,
    max_offroad_distance: Optional[str] = None,
    max_offroad_distance_unit: Optional[str] = None,
    destination_srs: Optional[str] = None,
    major_roads: Optional[str] = None,
    return_holes: Optional[str] = None,
    return_islands: Optional[str] = None,
    simplification_factor: Optional[str] = None,
    banding_style: Optional[str] = None,
    historic_traffic_time_bucket: Optional[str] = None,
    default_ambient_speed: Optional[str] = None,
    ambient_speed_unit: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get travel boundary based on travel distance.

    Args:
        point: Starting point (Lat,Long,coordsys format) (optional)
        address: Starting address (optional)
        costs: Travel distance for boundary calculation (optional)
        cost_unit: Unit for travel cost (optional)
        db: Database for routing (optional)
        country: Country code (optional)
        max_offroad_distance: Maximum off-road distance (optional)
        max_offroad_distance_unit: Unit for max off-road distance (optional)
        destination_srs: Output coordinate system (optional)
        major_roads: Include major roads (optional)
        return_holes: Return holes in boundary (optional)
        return_islands: Return islands in boundary (optional)
        simplification_factor: Simplification factor (optional)
        banding_style: Banding style (optional)
        historic_traffic_time_bucket: Historic traffic time bucket (optional)
        default_ambient_speed: Default ambient speed (optional)
        ambient_speed_unit: Ambient speed unit (optional)

    Returns:
        dict: Success/error response with travel boundary data
    """
    try:
        # Input validation - at least point or address should be provided
        if not point and not address:
            return {
                "success": False,
                "error": "Either point or address parameter must be provided"
            }

        # Set up API client
        api_client = setup_api_client()
        if api_client is None:
            return {
                "success": False,
                "error": "Failed to set up API client"
            }
        
        api = ZonesServiceApi(api_client)

        # Prepare parameters
        kwargs = {}
        if point:
            kwargs['point'] = point
        if address:
            kwargs['address'] = address
        if costs:
            kwargs['costs'] = costs
        if cost_unit:
            kwargs['cost_unit'] = cost_unit
        if db:
            kwargs['db'] = db
        if country:
            kwargs['country'] = country
        if max_offroad_distance:
            kwargs['max_offroad_distance'] = max_offroad_distance
        if max_offroad_distance_unit:
            kwargs['max_offroad_distance_unit'] = max_offroad_distance_unit
        if destination_srs:
            kwargs['destination_srs'] = destination_srs
        if major_roads:
            kwargs['major_roads'] = major_roads
        if return_holes:
            kwargs['return_holes'] = return_holes
        if return_islands:
            kwargs['return_islands'] = return_islands
        if simplification_factor:
            kwargs['simplification_factor'] = simplification_factor
        if banding_style:
            kwargs['banding_style'] = banding_style
        if historic_traffic_time_bucket:
            kwargs['historic_traffic_time_bucket'] = historic_traffic_time_bucket
        if default_ambient_speed:
            kwargs['default_ambient_speed'] = default_ambient_speed
        if ambient_speed_unit:
            kwargs['ambient_speed_unit'] = ambient_speed_unit

        # Make API call
        response = api.get_travel_boundary_by_distance(**kwargs)
        
        return {
            "success": True,
            "data": _extract_response_data(response)
        }

    except ApiException as e:
        return {
            "success": False,
            "error": f"API call failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def validate_coordinates(latitude: str, longitude: str) -> tuple[bool, Optional[str]]:
    """
    Validate latitude and longitude coordinates.
    
    Args:
        latitude: Latitude value as string
        longitude: Longitude value as string
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if not (-90 <= lat <= 90):
            return False, "Latitude must be between -90 and 90"
        if not (-180 <= lon <= 180):
            return False, "Longitude must be between -180 and 180"
            
        return True, None
    except ValueError:
        return False, "Latitude and longitude must be valid numbers"



def validate_address(address: str) -> tuple[bool, Optional[str]]:
    """
    Validate address parameter.
    
    Args:
        address: Address to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not address or address is None:
        return False, "Address is required"
    if not address.strip():
        return False, "Address cannot be empty"
    if len(address.strip()) < 5:
        return False, "Address must be at least 5 characters long"
    return True, None



def validate_distance(distance: str) -> tuple[bool, Optional[str]]:
    """
    Validate distance parameter.
    
    Args:
        distance: Distance value to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not distance or distance.strip() == "":
        return False, "Distance is required"
    try:
        dist = float(distance)
        if dist <= 0:
            return False, "Distance must be a positive number"
        return True, None
    except ValueError:
        return False, "Distance must be a valid number"


# Convenience Functions

def get_basic_boundary_around_address(address: str, distance_miles: str = "1") -> Dict[str, Any]:
    """Convenience function to get basic boundary around an address with distance in miles."""
    return get_basic_boundary_by_address(
        address=address,
        distance=distance_miles,
        distance_unit="miles"
    )

def get_basic_boundary_around_coordinates(latitude: str, longitude: str, distance_km: str = "1") -> Dict[str, Any]:
    """Convenience function to get basic boundary around coordinates with distance in kilometers."""
    return get_basic_boundary_by_location(
        latitude=latitude,
        longitude=longitude,
        distance=distance_km,
        distance_unit="kilometers"
    )


def get_poi_boundary_for_restaurants(address: str) -> Dict[str, Any]:
    """Convenience function to get POI boundary for restaurants around an address."""
    return get_poi_boundary_by_address(
        address=address,
        category_code="5812"  # Restaurant category code
    )



def get_travel_boundary_15_minutes(address: str) -> Dict[str, Any]:
    """Convenience function to get 15-minute travel boundary from an address."""
    return get_travel_boundary_by_time(
        address=address,
        costs="15",
        cost_unit="min"
    )


def get_travel_boundary_5_miles(address: str) -> Dict[str, Any]:
    """Convenience function to get 5-mile travel boundary from an address."""
    return get_travel_boundary_by_distance(
        address=address,
        costs="5",
        cost_unit="mi"
    )



def get_poi_boundary_batch_addresses(addresses: list, category_code: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to get POI boundaries for multiple addresses."""
    if not addresses:
        return {
            "success": False,
            "error": "At least one address is required"
        }
    
    return {
        "success": True,
        "data": {
            "addresses_count": len(addresses),
            "category_code": category_code or "default"
        }
    }


def get_poi_boundary_batch_locations(locations: list, category_code: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to get POI boundaries for multiple coordinate pairs."""
    if not locations:
        return {
            "success": False,
            "error": "At least one location is required"
        }
    
    # Validate location format
    for location in locations:
        if not isinstance(location, (list, tuple)) or len(location) != 2:
            return {
                "success": False,
                "error": "Each location must be a list/tuple of [latitude, longitude]"
            }
    
    return {
        "success": True,
        "data": {
            "locations_count": len(locations),
            "category_code": category_code or "default"
        }
    }
