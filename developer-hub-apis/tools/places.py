"""
Places Service functions using Precisely APIs SDK.
Functions for retrieving points of interest and places data.
"""

import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.places_service__api import PlacesServiceApi
from com.precisely.apis.exceptions import ApiException
from com.precisely.apis.model.poiby_geometry_request import POIByGeometryRequest
from com.precisely.apis.model.poi_count_request import PoiCountRequest
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Places Service API instance."""
    api = PlacesServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api


@mcp.tool()
def get_category_code_metadata() -> Dict[str, Any]:
    """
    Retrieve the category code metadata for points of interest.
    
    Returns:
        dict: Category code metadata or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call API
        response = api_instance.get_category_code_metadata()
        
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
def get_poi_by_id(poi_id: str) -> Dict[str, Any]:
    """
    Retrieve a point of interest by its unique identifier.
    
    Args:
        poi_id (str): The unique identifier for the POI
    
    Returns:
        dict: POI data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call API
        response = api_instance.get_poiby_id(id=poi_id)
        
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
def get_pois_by_address(
    address: str,
    country: Optional[str] = None,
    name: Optional[str] = None,
    type_code: Optional[str] = None,
    category_code: Optional[str] = None,
    sic_code: Optional[str] = None,
    max_candidates: Optional[str] = None,
    search_radius: Optional[str] = None,
    search_radius_unit: Optional[str] = None,
    travel_time: Optional[str] = None,
    travel_time_unit: Optional[str] = None,
    travel_distance: Optional[str] = None,
    travel_distance_unit: Optional[str] = None,
    travel_mode: Optional[str] = None,
    sort_by: Optional[str] = None,
    fuzzy_on_name: Optional[str] = None,
    page: Optional[str] = None,
    match_mode: Optional[str] = None,
    specific_match_on: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find points of interest near a specific address.
    
    Args:
        address (str): The address to search near
        country (str, optional): Country name or ISO code
        name (str, optional): Name of the POI to search for
        type_code (str, optional): Type of POI to search for
        category_code (str, optional): Category code of the POI
        sic_code (str, optional): SIC code of the POI
        max_candidates (str, optional): Maximum number of results to return
        search_radius (str, optional): Radius to search within
        search_radius_unit (str, optional): Unit for search radius
        travel_time (str, optional): Travel time to search within
        travel_time_unit (str, optional): Unit for travel time
        travel_distance (str, optional): Travel distance to search within
        travel_distance_unit (str, optional): Unit for travel distance
        travel_mode (str, optional): Mode of transportation
        sort_by (str, optional): How to sort results
        fuzzy_on_name (str, optional): Whether to use fuzzy matching on names
        page (str, optional): Page number for paginated results
        match_mode (str, optional): Match mode (Standard, Relaxed, etc.)
        specific_match_on (str, optional): Specific field to match on
    
    Returns:
        dict: POI data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        params['address'] = address
        if country is not None: params['country'] = country
        if name is not None: params['name'] = name
        if type_code is not None: params['type'] = type_code
        if category_code is not None: params['category_code'] = category_code
        if sic_code is not None: params['sic_code'] = sic_code
        if max_candidates is not None: params['max_candidates'] = max_candidates
        if search_radius is not None: params['search_radius'] = search_radius
        if search_radius_unit is not None: params['search_radius_unit'] = search_radius_unit
        if travel_time is not None: params['travel_time'] = travel_time
        if travel_time_unit is not None: params['travel_time_unit'] = travel_time_unit
        if travel_distance is not None: params['travel_distance'] = travel_distance
        if travel_distance_unit is not None: params['travel_distance_unit'] = travel_distance_unit
        if travel_mode is not None: params['travel_mode'] = travel_mode
        if sort_by is not None: params['sort_by'] = sort_by
        if fuzzy_on_name is not None: params['fuzzy_on_name'] = fuzzy_on_name
        if page is not None: params['page'] = page
        if match_mode is not None: params['match_mode'] = match_mode
        if specific_match_on is not None: params['specific_match_on'] = specific_match_on
        
        # For debugging
        try:
            # Call API
            response = api_instance.get_pois_by_address(**params)
            
            return {
                "success": True,
                "data": response.to_dict() if hasattr(response, 'to_dict') else response
            }
        except ApiException as api_error:
            return {
                "success": False,
                "error": f"API Error: {api_error.status} - {api_error.reason}",
                "details": api_error.body if hasattr(api_error, 'body') else str(api_error),
                "params": params
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
def get_pois_by_location(
    latitude: str,
    longitude: str,
    country: Optional[str] = None,
    name: Optional[str] = None,
    type_code: Optional[str] = None,
    category_code: Optional[str] = None,
    sic_code: Optional[str] = None,
    max_candidates: Optional[str] = None,
    search_radius: Optional[str] = None,
    search_radius_unit: Optional[str] = None,
    travel_time: Optional[str] = None,
    travel_time_unit: Optional[str] = None,
    travel_distance: Optional[str] = None,
    travel_distance_unit: Optional[str] = None,
    travel_mode: Optional[str] = None,
    sort_by: Optional[str] = None,
    fuzzy_on_name: Optional[str] = None,
    page: Optional[str] = None,
    match_mode: Optional[str] = None,
    specific_match_on: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find points of interest near a specific location.
    
    Args:
        latitude (str): Latitude coordinate
        longitude (str): Longitude coordinate
        country (str, optional): Country name or ISO code
        name (str, optional): Name of the POI to search for
        type_code (str, optional): Type of POI to search for
        category_code (str, optional): Category code of the POI
        sic_code (str, optional): SIC code of the POI
        max_candidates (str, optional): Maximum number of results to return
        search_radius (str, optional): Radius to search within
        search_radius_unit (str, optional): Unit for search radius
        travel_time (str, optional): Travel time to search within
        travel_time_unit (str, optional): Unit for travel time
        travel_distance (str, optional): Travel distance to search within
        travel_distance_unit (str, optional): Unit for travel distance
        travel_mode (str, optional): Mode of transportation
        sort_by (str, optional): How to sort results
        fuzzy_on_name (str, optional): Whether to use fuzzy matching on names
        page (str, optional): Page number for paginated results
        match_mode (str, optional): Match mode (Standard, Relaxed, etc.)
        specific_match_on (str, optional): Specific field to match on
    
    Returns:
        dict: POI data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        params['latitude'] = latitude
        params['longitude'] = longitude
        if country is not None: params['country'] = country
        if name is not None: params['name'] = name
        if type_code is not None: params['type'] = type_code
        if category_code is not None: params['category_code'] = category_code
        if sic_code is not None: params['sic_code'] = sic_code
        if max_candidates is not None: params['max_candidates'] = max_candidates
        if search_radius is not None: params['search_radius'] = search_radius
        if search_radius_unit is not None: params['search_radius_unit'] = search_radius_unit
        if travel_time is not None: params['travel_time'] = travel_time
        if travel_time_unit is not None: params['travel_time_unit'] = travel_time_unit
        if travel_distance is not None: params['travel_distance'] = travel_distance
        if travel_distance_unit is not None: params['travel_distance_unit'] = travel_distance_unit
        if travel_mode is not None: params['travel_mode'] = travel_mode
        if sort_by is not None: params['sort_by'] = sort_by
        if fuzzy_on_name is not None: params['fuzzy_on_name'] = fuzzy_on_name
        if page is not None: params['page'] = page
        if match_mode is not None: params['match_mode'] = match_mode
        if specific_match_on is not None: params['specific_match_on'] = specific_match_on
        
        # Call API
        response = api_instance.get_pois_by_location(**params)
        
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
def get_poi_count(
    country: str,
    category_code: str,
    level: Optional[str] = None,
    count_type: Optional[str] = None,
    geometry: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get count of points of interest by category and geographic area.
    
    Args:
        country (str): Country to search within
        category_code (str): Category code to count
        level (str, optional): Geographic level to aggregate counts
        count_type (str, optional): Type of count to perform
        geometry (dict, optional): Geometry to filter POIs
    
    Returns:
        dict: POI count data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create request object with required parameters
        request = PoiCountRequest(country=country, category_code=category_code)
        
        # Use setattr for optional parameters if provided
        if level is not None:
            setattr(request, 'level', level)
        if count_type is not None:
            setattr(request, 'count_type', count_type)
        if geometry is not None:
            setattr(request, 'geometry', geometry)
        
        # Call API - specifying content_type header as required by the API
        response = api_instance.get_pois_count(
            content_type="application/json",
            poi_count_request=request
        )
        
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
def get_pois_by_geometry(
    geometry: Dict[str, Any],
    country: Optional[str] = None,
    name: Optional[str] = None,
    type_code: Optional[str] = None,
    category_code: Optional[str] = None,
    sic_code: Optional[str] = None,
    max_candidates: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find points of interest within a custom geometry.
    
    Args:
        geometry (dict): Geometry object defining the search area
        country (str, optional): Country name or ISO code
        name (str, optional): Name of the POI to search for
        type_code (str, optional): Type of POI to search for
        category_code (str, optional): Category code of the POI
        sic_code (str, optional): SIC code of the POI
        max_candidates (str, optional): Maximum number of results to return
    
    Returns:
        dict: POI data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create request object with geometry
        request = POIByGeometryRequest(geometry=geometry)
        
        # Use setattr for optional parameters if provided
        if country is not None:
            setattr(request, 'country', country)
        if name is not None:
            setattr(request, 'name', name)
        if type_code is not None:
            setattr(request, 'type', type_code)
        if category_code is not None:
            setattr(request, 'category_code', category_code)
        if sic_code is not None:
            setattr(request, 'sic_code', sic_code)
        if max_candidates is not None:
            setattr(request, 'max_candidates', max_candidates)
        
        # Call API
        response = api_instance.get_pois_by_geometry(poiby_geometry_request=request)
        
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
def search_pois(
    search_text: str,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
    search_on_name_only: Optional[str] = None,
    search_radius: Optional[str] = None,
    search_radius_unit: Optional[str] = None,
    travel_time: Optional[str] = None,
    travel_time_unit: Optional[str] = None,
    travel_distance: Optional[str] = None,
    travel_distance_unit: Optional[str] = None,
    travel_mode: Optional[str] = None,
    country: Optional[str] = None,
    area_name1: Optional[str] = None,
    area_name3: Optional[str] = None,
    postcode1: Optional[str] = None,
    postcode2: Optional[str] = None,
    ip_address: Optional[str] = None,
    auto_detect_location: Optional[str] = None,
    type_code: Optional[str] = None,
    category_code: Optional[str] = None,
    sic_code: Optional[str] = None,
    max_candidates: Optional[str] = None,
    sort_by: Optional[str] = None,
    match_mode: Optional[str] = None,
    specific_match_on: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for points of interest by text and optional location.
    
    Args:
        search_text (str): Text to search for
        latitude (str, optional): Latitude coordinate
        longitude (str, optional): Longitude coordinate
        search_on_name_only (str, optional): Whether to search only on name
        search_radius (str, optional): Radius to search within
        search_radius_unit (str, optional): Unit for search radius
        travel_time (str, optional): Travel time to search within
        travel_time_unit (str, optional): Unit for travel time
        travel_distance (str, optional): Travel distance to search within
        travel_distance_unit (str, optional): Unit for travel distance
        travel_mode (str, optional): Mode of transportation
        country (str, optional): Country name or ISO code
        area_name1 (str, optional): State/province
        area_name3 (str, optional): City/town
        postcode1 (str, optional): Postal code
        postcode2 (str, optional): Extended postal code
        ip_address (str, optional): IP address for geolocation
        auto_detect_location (str, optional): Whether to auto-detect location
        type_code (str, optional): Type of POI to search for
        category_code (str, optional): Category code of the POI
        sic_code (str, optional): SIC code of the POI
        max_candidates (str, optional): Maximum number of results to return
        sort_by (str, optional): How to sort results
        match_mode (str, optional): Match mode (Standard, Relaxed, etc.)
        specific_match_on (str, optional): Specific field to match on
    
    Returns:
        dict: POI data or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        params['search_text'] = search_text
        if latitude is not None: params['latitude'] = latitude
        if longitude is not None: params['longitude'] = longitude
        if search_on_name_only is not None: params['search_on_name_only'] = search_on_name_only
        if search_radius is not None: params['search_radius'] = search_radius
        if search_radius_unit is not None: params['search_radius_unit'] = search_radius_unit
        if travel_time is not None: params['travel_time'] = travel_time
        if travel_time_unit is not None: params['travel_time_unit'] = travel_time_unit
        if travel_distance is not None: params['travel_distance'] = travel_distance
        if travel_distance_unit is not None: params['travel_distance_unit'] = travel_distance_unit
        if travel_mode is not None: params['travel_mode'] = travel_mode
        if country is not None: params['country'] = country
        if area_name1 is not None: params['area_name1'] = area_name1
        if area_name3 is not None: params['area_name3'] = area_name3
        if postcode1 is not None: params['postcode1'] = postcode1
        if postcode2 is not None: params['postcode2'] = postcode2
        if ip_address is not None: params['ip_address'] = ip_address
        if auto_detect_location is not None: params['auto_detect_location'] = auto_detect_location
        if type_code is not None: params['type'] = type_code
        if category_code is not None: params['category_code'] = category_code
        if sic_code is not None: params['sic_code'] = sic_code
        if max_candidates is not None: params['max_candidates'] = max_candidates
        if sort_by is not None: params['sort_by'] = sort_by
        if match_mode is not None: params['match_mode'] = match_mode
        if specific_match_on is not None: params['specific_match_on'] = specific_match_on
        
        # Call API with the correct method name
        response = api_instance.pois_autocomplete(**params)
        
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

