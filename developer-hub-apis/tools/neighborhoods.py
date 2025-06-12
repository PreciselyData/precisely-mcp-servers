"""
Neighborhoods functions using Precisely APIs SDK.
Functions for identifying neighborhoods and places based on geographic coordinates.
"""

import json
import os
from typing import Optional, Dict, Any
from com.precisely.apis.api.neighborhoods_service__api import NeighborhoodsServiceApi
from com.precisely.apis.exceptions import ApiException

from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely

from server import mcp
def _get_api_client():
    """Create and configure the Neighborhoods API instance."""
    api = NeighborhoodsServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api


@mcp.tool()
def get_place_by_location(latitude=None, longitude=None, level_hint=None):
    """
    Get neighborhood/place information for a specific location.
    
    Args:
        latitude (str, optional): Latitude of the location
        longitude (str, optional): Longitude of the location  
        level_hint (str, optional): Numeric code of geographic hierarchy level (1-6)
                                   1 = Country level
                                   2 = State/Province level
                                   3 = County level
                                   4 = City level
                                   5 = Neighborhood level
                                   6 = Sub-neighborhood level
    
    Returns:
        dict: API response with neighborhood/place information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters
        kwargs = {}
        if latitude is not None:
            kwargs['latitude'] = str(latitude)
        if longitude is not None:
            kwargs['longitude'] = str(longitude)
        if level_hint is not None:
            kwargs['level_hint'] = str(level_hint)
        
        # Call the API
        response = api_instance.get_place_by_location(**kwargs)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract place information
        if hasattr(response, 'place_name') and response.place_name:
            result["data"]["place_name"] = response.place_name
            
        if hasattr(response, 'location') and response.location:
            location_dict = {}
            if hasattr(response.location, 'latitude') and response.location.latitude:
                location_dict['latitude'] = response.location.latitude
            if hasattr(response.location, 'longitude') and response.location.longitude:
                location_dict['longitude'] = response.location.longitude
            if location_dict:
                result["data"]["location"] = location_dict
        
        # Extract additional response fields
        for attr in ['level', 'hierarchy_level', 'area_type', 'place_type']:
            if hasattr(response, attr) and getattr(response, attr) is not None:
                result["data"][attr] = getattr(response, attr)
        
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
def get_neighborhood_by_coordinates(latitude, longitude, level_hint=5):
    """
    Get neighborhood information for specific coordinates with neighborhood-level detail.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        level_hint (int, optional): Geographic hierarchy level, defaults to 5 (neighborhood level)
    
    Returns:
        dict: API response with neighborhood information or error information
    """
    return get_place_by_location(
        latitude=latitude,
        longitude=longitude,
        level_hint=level_hint
    )


@mcp.tool()
def get_city_by_coordinates(latitude, longitude):
    """
    Get city information for specific coordinates.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
    
    Returns:
        dict: API response with city information or error information
    """
    return get_place_by_location(
        latitude=latitude,
        longitude=longitude,
        level_hint=4  # City level
    )


@mcp.tool()
def get_detailed_place_hierarchy(latitude, longitude):
    """
    Get detailed place hierarchy information by calling multiple levels.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
    
    Returns:
        dict: Combined response with all hierarchy levels or error information
    """
    try:
        result = {
            "success": True,
            "data": {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "hierarchy": {}
            }
        }
        
        # Get information for different hierarchy levels
        levels = {
            "country": 1,
            "state": 2,
            "county": 3,
            "city": 4,
            "neighborhood": 5,
            "sub_neighborhood": 6
        }
        
        for level_name, level_code in levels.items():
            place_response = get_place_by_location(
                latitude=latitude,
                longitude=longitude,
                level_hint=level_code
            )
            
            if place_response.get("success"):
                result["data"]["hierarchy"][level_name] = place_response.get("data", {})
            else:
                # If one level fails, include the error but continue
                result["data"]["hierarchy"][level_name] = {
                    "error": place_response.get("error", "Unknown error")
                }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


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
def validate_level_hint(level_hint):
    """
    Validate if level_hint is in valid range.
    
    Args:
        level_hint (int): Level hint to validate
        
    Returns:
        bool: True if level_hint is valid (1-6), False otherwise
    """
    try:
        level = int(level_hint)
        return 1 <= level <= 6
    except (ValueError, TypeError):
        return False


@mcp.tool()
def get_place_with_validation(latitude, longitude, level_hint=None):
    """
    Get place information with input validation.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        level_hint (int, optional): Geographic hierarchy level (1-6)
    
    Returns:
        dict: API response with place information or error information
    """
    # Validate coordinates
    if not validate_coordinates(latitude, longitude):
        return {
            "success": False,
            "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
        }
    
    # Validate level_hint if provided
    if level_hint is not None and not validate_level_hint(level_hint):
        return {
            "success": False,
            "error": "Invalid level_hint. Must be an integer between 1 and 6."
        }
    
    return get_place_by_location(
        latitude=latitude,
        longitude=longitude,
        level_hint=level_hint
    )


@mcp.tool()
def search_neighborhoods_nearby(latitude, longitude, radius_levels=None):
    """
    Search for neighborhoods at different hierarchy levels around a location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        radius_levels (list, optional): List of hierarchy levels to search, defaults to [4,5,6]
    
    Returns:
        dict: API response with neighborhood information at different levels
    """
    if radius_levels is None:
        radius_levels = [4, 5, 6]  # City, neighborhood, sub-neighborhood
    
    try:
        result = {
            "success": True,
            "data": {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "places": {}
            }
        }
        
        for level in radius_levels:
            if validate_level_hint(level):
                place_response = get_place_by_location(
                    latitude=latitude,
                    longitude=longitude,
                    level_hint=level
                )
                
                level_name = {
                    1: "country",
                    2: "state",
                    3: "county", 
                    4: "city",
                    5: "neighborhood",
                    6: "sub_neighborhood"
                }.get(level, f"level_{level}")
                
                if place_response.get("success"):
                    result["data"]["places"][level_name] = place_response.get("data", {})
                else:
                    result["data"]["places"][level_name] = {
                        "error": place_response.get("error", "Unknown error")
                    }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }
