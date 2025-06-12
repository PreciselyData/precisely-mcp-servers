"""
Risks Service functions using Precisely APIs SDK.
Functions for accessing various risk-related information, including crime, earthquake, fire, and flood risks.
"""

import json
import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.risks_service_api import RisksServiceApi
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Risks Service API instance."""
    api = RisksServiceApi()
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
def validate_risk_type(risk_type):
    """
    Validate risk type for crime risk API.
    
    Args:
        risk_type (str): Risk type to validate
        
    Returns:
        bool: True if risk type is valid, False otherwise
    """
    valid_types = ['all', 'general', 'personal', 'property']
    
    # Check if None (valid)
    if risk_type is None:
        return True
    
    # Check if string and in valid_types
    if isinstance(risk_type, str):
        return risk_type.lower() in valid_types
    
    # Non-string types are invalid
    return False


@mcp.tool()
def get_crime_risk_by_address(address, risk_type=None, include_geometry=False):
    """
    Get crime risk information for a specific address.
    
    Args:
        address (str): The address to get crime risk for (required)
        risk_type (str, optional): The type of risk to return
                                  Valid values: 'all', 'general', 'personal', 'property'
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with crime risk information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters
        kwargs = {'address': address}
        if risk_type is not None:
            kwargs['type'] = risk_type
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_crime_risk_by_address(**kwargs)
        
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
def get_crime_risk_by_location(latitude, longitude, risk_type=None, include_geometry=False):
    """
    Get crime risk information for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        risk_type (str, optional): The type of risk to return
                                  Valid values: 'all', 'general', 'personal', 'property'
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with crime risk information or error information
    """
    try:
        # Validate coordinates
        if not validate_coordinates(latitude, longitude):
            return {
                "success": False,
                "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
        
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Prepare parameters
        kwargs = {'longitude': lon_str, 'latitude': lat_str}
        if risk_type is not None:
            kwargs['type'] = risk_type
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_crime_risk_by_location(**kwargs)
        
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
def get_earthquake_history(latitude, longitude, start_date=None, end_date=None, radius=None, minimal_magnitude=None):
    """
    Get earthquake history for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        start_date (str, optional): Start date for earthquake history (YYYY-MM-DD format)
        end_date (str, optional): End date for earthquake history (YYYY-MM-DD format)
        radius (float, optional): Radius in miles for search area
        minimal_magnitude (float, optional): Minimal magnitude of earthquake to include
        
    Returns:
        dict: API response with earthquake history information or error information
    """
    try:
        # Validate coordinates
        if not validate_coordinates(latitude, longitude):
            return {
                "success": False,
                "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
        
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Prepare parameters
        kwargs = {'longitude': lon_str, 'latitude': lat_str}
        if start_date is not None:
            kwargs['start_date'] = start_date
        if end_date is not None:
            kwargs['end_date'] = end_date
        if radius is not None:
            kwargs['radius'] = str(radius)
        if minimal_magnitude is not None:
            kwargs['minimal_magnitude'] = str(minimal_magnitude)
        
        # Call the API
        response = api_instance.get_earthquake_history(**kwargs)
        
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
def get_earthquake_risk_by_address(address, include_geometry=False):
    """
    Get earthquake risk information for a specific address.
    
    Args:
        address (str): The address to get earthquake risk for (required)
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with earthquake risk information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters
        kwargs = {'address': address}
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_earthquake_risk_by_address(**kwargs)
        
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
def get_earthquake_risk_by_location(latitude, longitude, include_geometry=False):
    """
    Get earthquake risk information for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with earthquake risk information or error information
    """
    try:
        # Validate coordinates
        if not validate_coordinates(latitude, longitude):
            return {
                "success": False,
                "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
        
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Prepare parameters
        kwargs = {'longitude': lon_str, 'latitude': lat_str}
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_earthquake_risk_by_location(**kwargs)
        
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
def get_fire_history(latitude, longitude, start_date=None, end_date=None, radius=None):
    """
    Get fire history for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        start_date (str, optional): Start date for fire history (YYYY-MM-DD format)
        end_date (str, optional): End date for fire history (YYYY-MM-DD format)
        radius (float, optional): Radius in miles for search area
        
    Returns:
        dict: API response with fire history information or error information
    """
    try:
        # Validate coordinates
        if not validate_coordinates(latitude, longitude):
            return {
                "success": False,
                "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
        
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Prepare parameters
        kwargs = {'longitude': lon_str, 'latitude': lat_str}
        if start_date is not None:
            kwargs['start_date'] = start_date
        if end_date is not None:
            kwargs['end_date'] = end_date
        if radius is not None:
            kwargs['radius'] = str(radius)
        
        # Call the API
        response = api_instance.get_fire_history(**kwargs)
        
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
def get_fire_risk_by_address(address, include_geometry=False):
    """
    Get fire risk information for a specific address.
    
    Args:
        address (str): The address to get fire risk for (required)
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with fire risk information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters
        kwargs = {'address': address}
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_fire_risk_by_address(**kwargs)
        
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
def get_fire_risk_by_location(latitude, longitude, include_geometry=False):
    """
    Get fire risk information for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with fire risk information or error information
    """
    try:
        # Validate coordinates
        if not validate_coordinates(latitude, longitude):
            return {
                "success": False,
                "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
        
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Prepare parameters
        kwargs = {'longitude': lon_str, 'latitude': lat_str}
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_fire_risk_by_location(**kwargs)
        
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
def get_flood_risk_by_address(address, include_geometry=False):
    """
    Get flood risk information for a specific address.
    
    Args:
        address (str): The address to get flood risk for (required)
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with flood risk information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters
        kwargs = {'address': address}
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_flood_risk_by_address(**kwargs)
        
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
def get_flood_risk_by_location(latitude, longitude, include_geometry=False):
    """
    Get flood risk information for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with flood risk information or error information
    """
    try:
        # Validate coordinates
        if not validate_coordinates(latitude, longitude):
            return {
                "success": False,
                "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
        
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Prepare parameters
        kwargs = {'longitude': lon_str, 'latitude': lat_str}
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_flood_risk_by_location(**kwargs)
        
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
def get_distance_to_coast_by_address(address, unit=None, include_geometry=False):
    """
    Get distance to coast information for a specific address.
    
    Args:
        address (str): The address to get distance to coast for (required)
        unit (str, optional): The unit of measurement (feet, kilometers, miles, meters)
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with distance to coast information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters
        kwargs = {'address': address}
        if unit is not None:
            kwargs['unit'] = unit
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_distance_to_coast_by_address(**kwargs)
        
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
def get_distance_to_coast_by_location(latitude, longitude, unit=None, include_geometry=False):
    """
    Get distance to coast information for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        unit (str, optional): The unit of measurement (feet, kilometers, miles, meters)
        include_geometry (bool, optional): Whether to include geometry information
        
    Returns:
        dict: API response with distance to coast information or error information
    """
    try:
        # Validate coordinates
        if not validate_coordinates(latitude, longitude):
            return {
                "success": False,
                "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
        
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Prepare parameters
        kwargs = {'longitude': lon_str, 'latitude': lat_str}
        if unit is not None:
            kwargs['unit'] = unit
        if include_geometry is not None:
            kwargs['include_geometry'] = include_geometry
        
        # Call the API
        response = api_instance.get_distance_to_coast_by_location(**kwargs)
        
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
