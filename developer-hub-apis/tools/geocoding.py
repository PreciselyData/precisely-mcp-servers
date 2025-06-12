"""
Geocoding functions using Precisely APIs SDK.
Functions for forward and reverse geocoding.
"""

import os
from typing import Optional, Dict, Any
from com.precisely.apis.api.geocode_service_api import GeocodeServiceApi
from com.precisely.apis.exceptions import ApiException
from com.precisely.apis.model.geocode_request import GeocodeRequest
from com.precisely.apis.model.reverse_geocode_request import ReverseGeocodeRequest
from com.precisely.apis.model.points import Points

from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely

from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely

from server import mcp
def _get_api_client():
    """Create and configure the Geocode Service API instance."""
    api = GeocodeServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api

@mcp.tool()
def forward_geocode(
    main_address: str,
    country: Optional[str] = None,
    match_mode: Optional[str] = None,
    fallback_geo: Optional[str] = None,
    fallback_postal: Optional[str] = None,
    max_candidates: Optional[str] = None,
    street_offset: Optional[str] = None,
    street_offset_units: Optional[str] = None,
    corner_offset: Optional[str] = None,
    corner_offset_units: Optional[str] = None,
    remove_accent_marks: Optional[str] = None,
    datapack_bundle: str = "premium"
) -> Dict[str, Any]:
    """
    Perform forward geocoding for an address.
    
    Args:
        main_address (str): Single line address input
        country (str, optional): Country name or ISO code
        match_mode (str, optional): Match mode (Standard, Relaxed, etc.)
        fallback_geo (str, optional): Whether to use geographic fallbacks
        fallback_postal (str, optional): Whether to use postal fallbacks
        max_candidates (str, optional): Maximum number of candidates to return
        street_offset (str, optional): Offset distance from street segments
        street_offset_units (str, optional): Units for street offset
        corner_offset (str, optional): Distance to offset street end points
        corner_offset_units (str, optional): Units for corner offset
        remove_accent_marks (str, optional): Whether to suppress accents
        datapack_bundle (str, optional): Data package bundle (basic, premium, advanced)
    
    Returns:
        dict: Geocoding results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        if main_address is not None: params['main_address'] = main_address
        if country is not None: params['country'] = country
        if match_mode is not None: params['match_mode'] = match_mode
        if fallback_geo is not None: params['fallback_geo'] = fallback_geo
        if fallback_postal is not None: params['fallback_postal'] = fallback_postal
        if max_candidates is not None: params['max_cands'] = max_candidates
        if street_offset is not None: params['street_offset'] = street_offset
        if street_offset_units is not None: params['street_offset_units'] = street_offset_units
        if corner_offset is not None: params['corner_offset'] = corner_offset
        if corner_offset_units is not None: params['corner_offset_units'] = corner_offset_units
        if remove_accent_marks is not None: params['remove_accent_marks'] = remove_accent_marks
        
        # Call API
        response = api_instance.geocode(datapack_bundle, **params)
        
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
def reverse_geocode(
    latitude: str,
    longitude: str,
    country: Optional[str] = None,
    match_mode: Optional[str] = None,
    max_candidates: Optional[str] = None,
    street_offset: Optional[str] = None,
    street_offset_units: Optional[str] = None,
    datapack_bundle: str = "premium"
) -> Dict[str, Any]:
    """
    Perform reverse geocoding for a latitude/longitude point.
    
    Args:
        latitude (str): Latitude coordinate
        longitude (str): Longitude coordinate
        country (str, optional): Country name or ISO code
        match_mode (str, optional): Match mode (Standard, Relaxed, etc.)
        max_candidates (str, optional): Maximum number of candidates to return
        street_offset (str, optional): Offset distance from street segments
        street_offset_units (str, optional): Units for street offset
        datapack_bundle (str, optional): Data package bundle (basic, premium, advanced)
    
    Returns:
        dict: Reverse geocoding results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        params['x'] = longitude  # Note: x = longitude, y = latitude
        params['y'] = latitude
        if country is not None: params['country'] = country
        if match_mode is not None: params['match_mode'] = match_mode
        if max_candidates is not None: params['max_cands'] = max_candidates
        if street_offset is not None: params['street_offset'] = street_offset
        if street_offset_units is not None: params['street_offset_units'] = street_offset_units
        
        # Call API
        response = api_instance.reverse_geocode(datapack_bundle, **params)
        
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
def batch_geocode(addresses: list) -> Dict[str, Any]:
    """
    Perform batch geocoding for multiple addresses.
    
    Args:
        addresses (list): List of address dictionaries, each containing address information
    
    Returns:
        dict: Batch geocoding results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create geocode request object
        request = GeocodeRequest(addresses=addresses)
        
        # Call API
        response = api_instance.geocode_batch("premium", geocode_request=request)
        
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
def batch_reverse_geocode(points: list) -> Dict[str, Any]:
    """
    Perform batch reverse geocoding for multiple points.
    
    Args:
        points (list): List of point dictionaries, each containing lat/lon coordinates
    
    Returns:
        dict: Batch reverse geocoding results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create Points objects
        points_objects = []
        for point in points:
            # Ensure we have both latitude and longitude
            if 'latitude' in point and 'longitude' in point:
                point_obj = Points(
                    coordinates=[point['longitude'], point['latitude']]  # Note: [lon, lat] order
                )
                points_objects.append(point_obj)
        
        # Create reverse geocode request
        request = ReverseGeocodeRequest(points=points_objects)
        
        # Call API
        response = api_instance.reverse_geocod_batch("premium", reverse_geocode_request=request)
        
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


