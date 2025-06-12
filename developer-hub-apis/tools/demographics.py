"""
Demographics functions using Precisely APIs SDK.
Functions for retrieving demographic data for locations, addresses, and boundaries.
"""

import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.demographics_service_api import DemographicsServiceApi
from com.precisely.apis.exceptions import ApiException
from com.precisely.apis.model.demographics_advanced_request import DemographicsAdvancedRequest
from com.precisely.apis.model.demographics_advanced_preferences import DemographicsAdvancedPreferences
from com.precisely.apis.model.demographics_geometry import DemographicsGeometry

from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely

from server import mcp
def _get_api_client():
    """Create and configure the Demographics Service API instance."""
    api = DemographicsServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api

@mcp.tool()
def get_demographics_by_address(
    address: str,
    country: Optional[str] = None,
    profile: Optional[str] = None,
    filter: Optional[str] = None,
    value_format: Optional[str] = None,
    variable_level: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get demographic data for a specific address.
    
    Args:
        address (str): The address to get demographics for (required)
        country (str, optional): Country name or ISO code
        profile (str, optional): Pre-defined profile for sorting results (Top5Ascending, Top5Descending, etc.)
        filter (str, optional): Filter to specific demographic themes
        value_format (str, optional): Format for values (percent or count)
        variable_level (str, optional): Level of demographic facts to include
    
    Returns:
        dict: Demographic data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        params['address'] = address
        if country is not None: params['country'] = country
        if profile is not None: params['profile'] = profile
        if filter is not None: params['filter'] = filter
        if value_format is not None: params['value_format'] = value_format
        if variable_level is not None: params['variable_level'] = variable_level
        
        # Call API
        response = api_instance.get_demographics_by_address(**params)
        
        return {
            "success": True,
            "data": response.to_dict() if hasattr(response, 'to_dict') else response
        }
        
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
def get_demographics_by_location(
    latitude: str,
    longitude: str,
    profile: Optional[str] = None,
    filter: Optional[str] = None,
    value_format: Optional[str] = None,
    variable_level: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get demographic data for a specific location using latitude and longitude.
    
    Args:
        latitude (str): Latitude coordinate (required)
        longitude (str): Longitude coordinate (required)
        profile (str, optional): Pre-defined profile for sorting results (Top5Ascending, Top5Descending, etc.)
        filter (str, optional): Filter to specific demographic themes
        value_format (str, optional): Format for values (percent or count)
        variable_level (str, optional): Level of demographic facts to include
    
    Returns:
        dict: Demographic data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        params['latitude'] = latitude
        params['longitude'] = longitude
        if profile is not None: params['profile'] = profile
        if filter is not None: params['filter'] = filter
        if value_format is not None: params['value_format'] = value_format
        if variable_level is not None: params['variable_level'] = variable_level
        
        # Call API
        response = api_instance.get_demographics_by_location(**params)
        
        return {
            "success": True,
            "data": response.to_dict() if hasattr(response, 'to_dict') else response
        }
        
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
def get_demographics_by_boundary_ids(
    boundary_ids: List[str],
    profile: Optional[str] = None,
    filter: Optional[str] = None,
    value_format: Optional[str] = None,
    variable_level: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get demographic data for specific boundary IDs.
    
    Args:
        boundary_ids (list): List of boundary IDs (required)
        profile (str, optional): Pre-defined profile for sorting results (Top5Ascending, Top5Descending, etc.)
        filter (str, optional): Filter to specific demographic themes
        value_format (str, optional): Format for values (percent or count)
        variable_level (str, optional): Level of demographic facts to include
    
    Returns:
        dict: Demographic data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Join boundary IDs with comma
        boundary_ids_str = ','.join(boundary_ids)
        
        # Prepare parameters, filtering out None values
        params = {}
        params['boundary_ids'] = boundary_ids_str
        if profile is not None: params['profile'] = profile
        if filter is not None: params['filter'] = filter
        if value_format is not None: params['value_format'] = value_format
        if variable_level is not None: params['variable_level'] = variable_level
        
        # Call API
        response = api_instance.get_demographics_by_boundary_ids(**params)
        
        return {
            "success": True,
            "data": response.to_dict() if hasattr(response, 'to_dict') else response
        }
        
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
def get_demographics_basic(
    address: Optional[str] = None,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
    search_radius: Optional[str] = None,
    search_radius_unit: Optional[str] = None,
    travel_time: Optional[str] = None,
    travel_time_unit: Optional[str] = None,
    travel_distance: Optional[str] = None,
    travel_distance_unit: Optional[str] = None,
    travel_mode: Optional[str] = None,
    country: Optional[str] = None,
    profile: Optional[str] = None,
    filter: Optional[str] = None,
    include_geometry: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get basic demographic data with flexible search options.
    
    Args:
        address (str, optional): The address to get demographics for
        latitude (str, optional): Latitude coordinate
        longitude (str, optional): Longitude coordinate
        search_radius (str, optional): Radius to search within
        search_radius_unit (str, optional): Unit for search radius (feet, miles, meters, kilometers)
        travel_time (str, optional): Travel time to search within
        travel_time_unit (str, optional): Unit for travel time (minutes, hours)
        travel_distance (str, optional): Travel distance to search within
        travel_distance_unit (str, optional): Unit for travel distance (feet, miles, meters, kilometers)
        travel_mode (str, optional): Mode of transportation (driving, walking)
        country (str, optional): Country name or ISO code
        profile (str, optional): Pre-defined profile for sorting results
        filter (str, optional): Filter to specific demographic themes
        include_geometry (str, optional): Whether to include geometries in response (true, false)
    
    Returns:
        dict: Demographic data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Ensure we have either address or coordinates
        if not address and not (latitude and longitude):
            return {
                "success": False,
                "error": "Either address or both latitude and longitude must be provided"
            }
            
        # Prepare parameters, filtering out None values
        params = {}
        if address is not None: params['address'] = address
        if longitude is not None: params['longitude'] = longitude
        if latitude is not None: params['latitude'] = latitude
        if search_radius is not None: params['search_radius'] = search_radius
        if search_radius_unit is not None: params['search_radius_unit'] = search_radius_unit
        if travel_time is not None: params['travel_time'] = travel_time
        if travel_time_unit is not None: params['travel_time_unit'] = travel_time_unit
        if travel_distance is not None: params['travel_distance'] = travel_distance
        if travel_distance_unit is not None: params['travel_distance_unit'] = travel_distance_unit
        if travel_mode is not None: params['travel_mode'] = travel_mode
        if country is not None: params['country'] = country
        if profile is not None: params['profile'] = profile
        if filter is not None: params['filter'] = filter
        if include_geometry is not None: params['include_geometry'] = include_geometry
        
        # Call API
        response = api_instance.get_demographics_basic(**params)
        
        return {
            "success": True,
            "data": response.to_dict() if hasattr(response, 'to_dict') else response
        }
        
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
def get_demographics_advanced(
    geometry: Dict[str, Any],
    preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get advanced demographic data with custom geometry and preferences.
    
    Args:
        geometry (dict): Geometry specification for the area to analyze
        preferences (dict, optional): Advanced preferences for demographic data
    
    Returns:
        dict: Demographic data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create demographics geometry object
        demographics_geometry = DemographicsGeometry(**geometry)
        
        # Create advanced preferences if provided
        demographics_preferences = None
        if preferences is not None:
            demographics_preferences = DemographicsAdvancedPreferences(**preferences)
        
        # Create request
        request = DemographicsAdvancedRequest(
            geometry=demographics_geometry,
            preferences=demographics_preferences
        )
        
        # Call API
        response = api_instance.get_demographics_advanced(demographics_advanced_request=request)
        
        return {
            "success": True,
            "data": response.to_dict() if hasattr(response, 'to_dict') else response
        }
        
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


