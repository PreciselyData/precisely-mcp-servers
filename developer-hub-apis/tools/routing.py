"""
Routing Service functions using Precisely APIs SDK.
Functions for accessing route and travel cost matrix information.
"""

import json
import os
from typing import Optional, Dict, Any, List, Union, Tuple
from com.precisely.apis.api.routing_service_api import RoutingServiceApi
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Routing Service API instance."""
    api = RoutingServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api


def _extract_object_data(obj):
    """
    Helper function to extract data from objects into JSON serializable dictionaries.
    
    Args:
        obj: Object to extract data from
        
    Returns:
        dict: Dictionary with extracted data
    """
    if obj is None:
        return None
    
    # If it's already a primitive type that's JSON serializable, return as is
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    
    # If it's a list, process each item
    if isinstance(obj, list):
        return [_extract_object_data(item) for item in obj]
    
    # If it's a dictionary, process each value
    if isinstance(obj, dict):
        return {k: _extract_object_data(v) for k, v in obj.items()}
    
    # Handle custom objects - convert to dict
    result = {}
    
    # Get all attributes of the object
    for attr_name in dir(obj):
        # Skip private attributes and methods
        if attr_name.startswith('_') or callable(getattr(obj, attr_name)):
            continue
        
        # Get the attribute value
        attr_value = getattr(obj, attr_name)
        
        # Extract the value (recursively if needed)
        result[attr_name] = _extract_object_data(attr_value)
    
    return result


@mcp.tool()
def validate_coordinates(latitude, longitude):
    """
    Validate if latitude and longitude are in valid ranges.
    
    Args:
        latitude (float): Latitude to validate
        longitude (float): Longitude to validate
        
    Returns:
        bool: True if coordinates are valid, False otherwise
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        # Check if latitude is in valid range (-90 to 90)
        if not -90 <= lat <= 90:
            return False
        
        # Check if longitude is in valid range (-180 to 180)
        if not -180 <= lon <= 180:
            return False
        
        return True
    except (ValueError, TypeError):
        return False


@mcp.tool()
def validate_optimization_type(optimize_by):
    """
    Validate optimization type.
    
    Args:
        optimize_by (str): Optimization type to validate
        
    Returns:
        bool: True if optimization type is valid, False otherwise
    """
    valid_types = ['time', 'distance']
    
    # Check if None (valid)
    if optimize_by is None:
        return True
    
    # Check if string and in valid_types
    if isinstance(optimize_by, str):
        return optimize_by.lower() in valid_types
    
    # Non-string types are invalid
    return False


@mcp.tool()
def validate_travel_mode(mode):
    """
    Validate travel mode (database).
    
    Args:
        mode (str): Travel mode to validate
        
    Returns:
        bool: True if travel mode is valid, False otherwise
    """
    valid_modes = ['driving', 'walking', 'bicycling', 'transit']
    
    # Check if None (valid)
    if mode is None:
        return True
    
    # Check if string and in valid_modes
    if isinstance(mode, str):
        return mode.lower() in valid_modes
    
    # Non-string types are invalid
    return False


@mcp.tool()
def get_route_by_address(start_address, end_address, **kwargs):
    """
    Get route information between two addresses.
    
    Args:
        start_address (str): Starting address (required)
        end_address (str): Ending address (required)
        **kwargs: Optional parameters including:
            - db (str): Mode of commute (driving, walking, etc.)
            - country (str): 3 Digit ISO country code
            - intermediate_addresses (str): List of intermediate addresses
            - optimize_by (str): Optimize by 'time' or 'distance'
            - return_distance (str): Whether to return distance
            - distance_unit (str): Unit for distance (m, km, mi, etc.)
            - return_time (str): Whether to return time
            - time_unit (str): Unit for time (min, h, s, etc.)
            - major_roads (str): Whether to include only major roads
        
    Returns:
        dict: API response with route information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters
        params = {
            'start_address': start_address,
            'end_address': end_address
        }
        
        # Add additional parameters if provided
        params.update(kwargs)
        
        # Call the API
        response = api_instance.get_route_by_address(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": _extract_object_data(response)
        }
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


@mcp.tool()
def get_route_by_location(start_latitude, start_longitude, end_latitude, end_longitude, **kwargs):
    """
    Get route information between two coordinates.
    
    Args:
        start_latitude (float): Latitude of starting point (required)
        start_longitude (float): Longitude of starting point (required)
        end_latitude (float): Latitude of ending point (required)
        end_longitude (float): Longitude of ending point (required)
        **kwargs: Optional parameters including:
            - db (str): Mode of commute (driving, walking, etc.)
            - intermediate_points (str): Intermediate points in 'Lat,Long,coordsys' format
            - optimize_by (str): Optimize by 'time' or 'distance'
            - return_distance (str): Whether to return distance
            - distance_unit (str): Unit for distance (m, km, mi, etc.)
            - return_time (str): Whether to return time
            - time_unit (str): Unit for time (min, h, s, etc.)
            - major_roads (str): Whether to include only major roads
        
    Returns:
        dict: API response with route information or error information
    """
    try:
        # Validate coordinates
        if not validate_coordinates(start_latitude, start_longitude):
            return {
                "success": False,
                "error": "Invalid start coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
            
        if not validate_coordinates(end_latitude, end_longitude):
            return {
                "success": False,
                "error": "Invalid end coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
        
        api_instance = _get_api_client()
        
        # Format coordinates as required by the API: 'Lat,Long,coordsys'
        start_point = f"{start_latitude},{start_longitude}"
        end_point = f"{end_latitude},{end_longitude}"
        
        # Prepare parameters
        params = {
            'start_point': start_point,
            'end_point': end_point
        }
        
        # Add additional parameters if provided
        params.update(kwargs)
        
        # Call the API
        response = api_instance.get_route_by_location(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": _extract_object_data(response)
        }
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


@mcp.tool()
def get_travel_cost_matrix_by_address(start_addresses, end_addresses, **kwargs):
    """
    Get travel cost matrix (distances and times) between multiple addresses.
    
    Args:
        start_addresses (Union[str, List[str]]): Starting addresses (required)
        end_addresses (Union[str, List[str]]): Ending addresses (required)
        **kwargs: Optional parameters including:
            - country (str): 3 Digit ISO country code
            - db (str): Mode of commute (driving, walking, etc.)
            - optimize_by (str): Optimize by 'time' or 'distance'
            - return_distance (str): Whether to return distance
            - distance_unit (str): Unit for distance (m, km, mi, etc.)
            - return_time (str): Whether to return time
            - time_unit (str): Unit for time (min, h, s, etc.)
            - major_roads (str): Whether to include only major roads
            - return_optimal_routes_only (str): Whether to return only optimal routes
        
    Returns:
        dict: API response with travel cost matrix or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Handle list of addresses by joining them with semicolons
        if isinstance(start_addresses, list):
            start_addresses = ";".join(start_addresses)
        
        if isinstance(end_addresses, list):
            end_addresses = ";".join(end_addresses)
        
        # Prepare parameters
        params = {
            'start_addresses': start_addresses,
            'end_addresses': end_addresses
        }
        
        # Add additional parameters if provided
        params.update(kwargs)
        
        # Call the API
        response = api_instance.get_travel_cost_matrix_by_address(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": _extract_object_data(response)
        }
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


@mcp.tool()
def get_travel_cost_matrix_by_location(start_points, end_points, **kwargs):
    """
    Get travel cost matrix (distances and times) between multiple coordinate pairs.
    
    Args:
        start_points (Union[str, List[Tuple[float, float]]]): Starting points (required)
            Either a string in API format or a list of (lat, long) tuples
        end_points (Union[str, List[Tuple[float, float]]]): Ending points (required)
            Either a string in API format or a list of (lat, long) tuples
        **kwargs: Optional parameters including:
            - db (str): Mode of commute (driving, walking, etc.)
            - optimize_by (str): Optimize by 'time' or 'distance'
            - return_distance (str): Whether to return distance
            - distance_unit (str): Unit for distance (m, km, mi, etc.)
            - return_time (str): Whether to return time
            - time_unit (str): Unit for time (min, h, s, etc.)
            - major_roads (str): Whether to include only major roads
            - return_optimal_routes_only (str): Whether to return only optimal routes
        
    Returns:
        dict: API response with travel cost matrix or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Convert list of coordinate tuples to API format string if needed
        if isinstance(start_points, list):
            # Validate each coordinate pair
            for lat, lon in start_points:
                if not validate_coordinates(lat, lon):
                    return {
                        "success": False,
                        "error": f"Invalid start coordinate: ({lat}, {lon}). Latitude must be between -90 and 90, longitude between -180 and 180."
                    }
            
            # Format: "lat1,lon1;lat2,lon2;..."
            start_points = ";".join([f"{lat},{lon}" for lat, lon in start_points])
        
        if isinstance(end_points, list):
            # Validate each coordinate pair
            for lat, lon in end_points:
                if not validate_coordinates(lat, lon):
                    return {
                        "success": False,
                        "error": f"Invalid end coordinate: ({lat}, {lon}). Latitude must be between -90 and 90, longitude between -180 and 180."
                    }
            
            # Format: "lat1,lon1;lat2,lon2;..."
            end_points = ";".join([f"{lat},{lon}" for lat, lon in end_points])
        
        # Prepare parameters
        params = {
            'start_points': start_points,
            'end_points': end_points
        }
        
        # Add additional parameters if provided
        params.update(kwargs)
        
        # Call the API
        response = api_instance.get_travel_cost_matrix_by_location(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": _extract_object_data(response)
        }
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }
