"""
Streets Service functions using Precisely APIs SDK.
Functions for intersection lookup and speed limit information.
"""

import os
from typing import Optional, Dict, Any
from com.precisely.apis.api.streets_service_api import StreetsServiceApi
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Streets Service API instance."""
    api = StreetsServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api


@mcp.tool()
def validate_road_class(road_class):
    """
    Validate road class parameter.
    
    Args:
        road_class (str): Road class to validate
        
    Returns:
        bool: True if road class is valid, False otherwise
    """
    valid_classes = ['Major', 'Secondary', 'Other', 'All']
    
    # Check if None (valid)
    if road_class is None:
        return True
    
    # Check if string and in valid_classes
    if isinstance(road_class, str):
        return road_class in valid_classes
    
    return False


@mcp.tool()
def validate_time_unit(time_unit):
    """
    Validate time unit parameter.
    
    Args:
        time_unit (str): Time unit to validate
        
    Returns:
        bool: True if time unit is valid, False otherwise
    """
    valid_units = ['hours', 'minutes', 'seconds', 'milliseconds']
    
    # Check if None (valid)
    if time_unit is None:
        return True
    
    # Check if string and in valid_units
    if isinstance(time_unit, str):
        return time_unit.lower() in valid_units
    
    return False


@mcp.tool()
def validate_distance_unit(distance_unit):
    """
    Validate distance unit parameter.
    
    Args:
        distance_unit (str): Distance unit to validate
        
    Returns:
        bool: True if distance unit is valid, False otherwise
    """
    valid_units = ['feet', 'meter', 'kilometers', 'miles']
    
    # Check if None (valid)
    if distance_unit is None:
        return True
    
    # Check if string and in valid_units
    if isinstance(distance_unit, str):
        return distance_unit.lower() in valid_units
    
    return False


@mcp.tool()
def validate_historic_speed(historic_speed):
    """
    Validate historic speed parameter.
    
    Args:
        historic_speed (str): Historic speed to validate
        
    Returns:
        bool: True if historic speed is valid, False otherwise
    """
    valid_speeds = ['AMPEAK', 'PMPEAK', 'OFFPEAK', 'NIGHT']
    
    # Check if None (valid)
    if historic_speed is None:
        return True
    
    # Check if string and in valid_speeds
    if isinstance(historic_speed, str):
        return historic_speed.upper() in valid_speeds
    
    return False

@mcp.tool()
def get_intersection_by_address(
    address: Optional[str] = None,
    road_class: Optional[str] = None,
    drive_time: Optional[str] = None,
    drive_time_unit: Optional[str] = None,
    search_radius: Optional[str] = None,
    search_radius_unit: Optional[str] = None,
    historic_speed: Optional[str] = None,
    max_candidates: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find the nearest intersection by address.
    
    Args:
        address (str, optional): Address to search near
        road_class (str, optional): Road class filter (Major, Secondary, Other, All)
        drive_time (str, optional): Drive time limit
        drive_time_unit (str, optional): Drive time unit (hours, minutes, seconds, milliseconds)
        search_radius (str, optional): Search radius (default 50 miles)
        search_radius_unit (str, optional): Search radius unit (feet, meter, kilometers, miles)
        historic_speed (str, optional): Traffic flow (AMPEAK, PMPEAK, OFFPEAK, NIGHT)
        max_candidates (str, optional): Maximum candidates to return (default 1)
    
    Returns:
        dict: Intersection information or error details
    """
    try:
        # Validate parameters
        if road_class and not validate_road_class(road_class):
            return {
                "success": False,
                "error": "Invalid road class. Valid values are: Major, Secondary, Other, All"
            }
        
        if drive_time_unit and not validate_time_unit(drive_time_unit):
            return {
                "success": False,
                "error": "Invalid drive time unit. Valid values are: hours, minutes, seconds, milliseconds"
            }
        
        if search_radius_unit and not validate_distance_unit(search_radius_unit):
            return {
                "success": False,
                "error": "Invalid search radius unit. Valid values are: feet, meter, kilometers, miles"
            }
        
        if historic_speed and not validate_historic_speed(historic_speed):
            return {
                "success": False,
                "error": "Invalid historic speed. Valid values are: AMPEAK, PMPEAK, OFFPEAK, NIGHT"
            }
        
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        if address is not None:
            params['address'] = address
        if road_class is not None:
            params['road_class'] = road_class
        if drive_time is not None:
            params['drive_time'] = drive_time
        if drive_time_unit is not None:
            params['drive_time_unit'] = drive_time_unit
        if search_radius is not None:
            params['search_radius'] = search_radius
        if search_radius_unit is not None:
            params['search_radius_unit'] = search_radius_unit
        if historic_speed is not None:
            params['historic_speed'] = historic_speed
        if max_candidates is not None:
            params['max_candidates'] = max_candidates
        
        # Call API
        response = api_instance.get_intersection_by_address(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract intersection information
        if hasattr(response, 'intersection') and response.intersection:
            intersections = []
            for intersection in response.intersection:
                intersection_data = {}
                if hasattr(intersection, 'intersecting_street1'):
                    intersection_data['intersecting_street1'] = intersection.intersecting_street1
                if hasattr(intersection, 'intersecting_street2'):
                    intersection_data['intersecting_street2'] = intersection.intersecting_street2
                if hasattr(intersection, 'road_class1'):
                    intersection_data['road_class1'] = intersection.road_class1
                if hasattr(intersection, 'road_class2'):
                    intersection_data['road_class2'] = intersection.road_class2
                if hasattr(intersection, 'distance'):
                    intersection_data['distance'] = intersection.distance
                if hasattr(intersection, 'distance_unit'):
                    intersection_data['distance_unit'] = intersection.distance_unit
                if hasattr(intersection, 'drive_time'):
                    intersection_data['drive_time'] = intersection.drive_time
                if hasattr(intersection, 'drive_time_unit'):
                    intersection_data['drive_time_unit'] = intersection.drive_time_unit
                
                # Extract intersection address if available
                if hasattr(intersection, 'address') and intersection.address:
                    address_data = {}
                    if hasattr(intersection.address, 'formatted_address'):
                        address_data['formatted_address'] = intersection.address.formatted_address
                    if hasattr(intersection.address, 'main_address_line'):
                        address_data['main_address_line'] = intersection.address.main_address_line
                    if hasattr(intersection.address, 'address_last_line'):
                        address_data['address_last_line'] = intersection.address.address_last_line
                    if hasattr(intersection.address, 'place_name'):
                        address_data['place_name'] = intersection.address.place_name
                    if hasattr(intersection.address, 'area_name1'):
                        address_data['area_name1'] = intersection.address.area_name1
                    if hasattr(intersection.address, 'postal_code'):
                        address_data['postal_code'] = intersection.address.postal_code
                    if hasattr(intersection.address, 'country'):
                        address_data['country'] = intersection.address.country
                    intersection_data['address'] = address_data
                
                # Extract geometry if available
                if hasattr(intersection, 'geometry') and intersection.geometry:
                    geometry_data = {}
                    if hasattr(intersection.geometry, 'coordinates'):
                        geometry_data['coordinates'] = intersection.geometry.coordinates
                    if hasattr(intersection.geometry, 'type'):
                        geometry_data['type'] = intersection.geometry.type
                    intersection_data['geometry'] = geometry_data
                
                intersections.append(intersection_data)
            
            result["data"]["intersections"] = intersections
        
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
def get_intersection_by_location(
    longitude: Optional[str] = None,
    latitude: Optional[str] = None,
    road_class: Optional[str] = None,
    drive_time: Optional[str] = None,
    drive_time_unit: Optional[str] = None,
    search_radius: Optional[str] = None,
    search_radius_unit: Optional[str] = None,
    historic_speed: Optional[str] = None,
    max_candidates: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find the nearest intersection by coordinates.
    
    Args:
        longitude (str, optional): Longitude coordinate
        latitude (str, optional): Latitude coordinate
        road_class (str, optional): Road class filter (Major, Secondary, Other, All)
        drive_time (str, optional): Drive time limit
        drive_time_unit (str, optional): Drive time unit (hours, minutes, seconds, milliseconds)
        search_radius (str, optional): Search radius (default 50 miles)
        search_radius_unit (str, optional): Search radius unit (feet, meter, kilometers, miles)
        historic_speed (str, optional): Traffic flow (AMPEAK, PMPEAK, OFFPEAK, NIGHT)
        max_candidates (str, optional): Maximum candidates to return (default 1)
    
    Returns:
        dict: Intersection information or error details
    """
    try:
        # Validate parameters
        if road_class and not validate_road_class(road_class):
            return {
                "success": False,
                "error": "Invalid road class. Valid values are: Major, Secondary, Other, All"
            }
        
        if drive_time_unit and not validate_time_unit(drive_time_unit):
            return {
                "success": False,
                "error": "Invalid drive time unit. Valid values are: hours, minutes, seconds, milliseconds"
            }
        
        if search_radius_unit and not validate_distance_unit(search_radius_unit):
            return {
                "success": False,
                "error": "Invalid search radius unit. Valid values are: feet, meter, kilometers, miles"
            }
        
        if historic_speed and not validate_historic_speed(historic_speed):
            return {
                "success": False,
                "error": "Invalid historic speed. Valid values are: AMPEAK, PMPEAK, OFFPEAK, NIGHT"
            }
        
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        if longitude is not None:
            params['longitude'] = longitude
        if latitude is not None:
            params['latitude'] = latitude
        if road_class is not None:
            params['road_class'] = road_class
        if drive_time is not None:
            params['drive_time'] = drive_time
        if drive_time_unit is not None:
            params['drive_time_unit'] = drive_time_unit
        if search_radius is not None:
            params['search_radius'] = search_radius
        if search_radius_unit is not None:
            params['search_radius_unit'] = search_radius_unit
        if historic_speed is not None:
            params['historic_speed'] = historic_speed
        if max_candidates is not None:
            params['max_candidates'] = max_candidates
        
        # Call API
        response = api_instance.get_intersection_by_location(**params)
        
        # Convert response to dictionary format (similar to get_intersection_by_address)
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract intersection information
        if hasattr(response, 'intersection') and response.intersection:
            intersections = []
            for intersection in response.intersection:
                intersection_data = {}
                if hasattr(intersection, 'intersecting_street1'):
                    intersection_data['intersecting_street1'] = intersection.intersecting_street1
                if hasattr(intersection, 'intersecting_street2'):
                    intersection_data['intersecting_street2'] = intersection.intersecting_street2
                if hasattr(intersection, 'road_class1'):
                    intersection_data['road_class1'] = intersection.road_class1
                if hasattr(intersection, 'road_class2'):
                    intersection_data['road_class2'] = intersection.road_class2
                if hasattr(intersection, 'distance'):
                    intersection_data['distance'] = intersection.distance
                if hasattr(intersection, 'distance_unit'):
                    intersection_data['distance_unit'] = intersection.distance_unit
                if hasattr(intersection, 'drive_time'):
                    intersection_data['drive_time'] = intersection.drive_time
                if hasattr(intersection, 'drive_time_unit'):
                    intersection_data['drive_time_unit'] = intersection.drive_time_unit
                
                # Extract intersection address if available
                if hasattr(intersection, 'address') and intersection.address:
                    address_data = {}
                    if hasattr(intersection.address, 'formatted_address'):
                        address_data['formatted_address'] = intersection.address.formatted_address
                    if hasattr(intersection.address, 'main_address_line'):
                        address_data['main_address_line'] = intersection.address.main_address_line
                    if hasattr(intersection.address, 'address_last_line'):
                        address_data['address_last_line'] = intersection.address.address_last_line
                    if hasattr(intersection.address, 'place_name'):
                        address_data['place_name'] = intersection.address.place_name
                    if hasattr(intersection.address, 'area_name1'):
                        address_data['area_name1'] = intersection.address.area_name1
                    if hasattr(intersection.address, 'postal_code'):
                        address_data['postal_code'] = intersection.address.postal_code
                    if hasattr(intersection.address, 'country'):
                        address_data['country'] = intersection.address.country
                    intersection_data['address'] = address_data
                
                # Extract geometry if available
                if hasattr(intersection, 'geometry') and intersection.geometry:
                    geometry_data = {}
                    if hasattr(intersection.geometry, 'coordinates'):
                        geometry_data['coordinates'] = intersection.geometry.coordinates
                    if hasattr(intersection.geometry, 'type'):
                        geometry_data['type'] = intersection.geometry.type
                    intersection_data['geometry'] = geometry_data
                
                intersections.append(intersection_data)
            
            result["data"]["intersections"] = intersections
        
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
def get_nearest_speed_limit(path: Optional[str] = None) -> Dict[str, Any]:
    """
    Get speed limit information for a path.
    
    Args:
        path (str, optional): Path coordinates as longitude,latitude pairs separated by semicolons
                             Example: "-122.4194,37.7749;-122.4094,37.7849"
    
    Returns:
        dict: Speed limit information or error details
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters
        params = {}
        if path is not None:
            params['path'] = path
        
        # Call API
        response = api_instance.get_nearest_speed_limit(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract speed limit information
        if hasattr(response, 'speed_limit'):
            result["data"]["speed_limit"] = response.speed_limit
        if hasattr(response, 'speed_limit_unit'):
            result["data"]["speed_limit_unit"] = response.speed_limit_unit
        if hasattr(response, 'road_type'):
            result["data"]["road_type"] = response.road_type
        if hasattr(response, 'road_class'):
            result["data"]["road_class"] = response.road_class
        
        # Extract path points if available
        if hasattr(response, 'path_points') and response.path_points:
            path_points = []
            for point in response.path_points:
                point_data = {}
                if hasattr(point, 'latitude'):
                    point_data['latitude'] = point.latitude
                if hasattr(point, 'longitude'):
                    point_data['longitude'] = point.longitude
                if hasattr(point, 'speed_limit'):
                    point_data['speed_limit'] = point.speed_limit
                if hasattr(point, 'speed_limit_unit'):
                    point_data['speed_limit_unit'] = point.speed_limit_unit
                path_points.append(point_data)
            result["data"]["path_points"] = path_points
        
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


# Convenience functions for common use cases

@mcp.tool()
def find_intersection_near_address(address: str, max_results: int = 1) -> Dict[str, Any]:
    """
    Convenience function to find intersections near an address.
    
    Args:
        address (str): Address to search near
        max_results (int): Maximum number of intersections to return
    
    Returns:
        dict: Intersection information or error details
    """
    return get_intersection_by_address(
        address=address,
        max_candidates=str(max_results)
    )


@mcp.tool()
def find_intersection_near_coordinates(longitude: str, latitude: str, max_results: int = 1) -> Dict[str, Any]:
    """
    Convenience function to find intersections near coordinates.
    
    Args:
        longitude (str): Longitude coordinate
        latitude (str): Latitude coordinate
        max_results (int): Maximum number of intersections to return
    
    Returns:
        dict: Intersection information or error details
    """
    return get_intersection_by_location(
        longitude=longitude,
        latitude=latitude,
        max_candidates=str(max_results)
    )


@mcp.tool()
def get_speed_limit_for_coordinates(longitude: str, latitude: str) -> Dict[str, Any]:
    """
    Convenience function to get speed limit for a single coordinate point.
    
    Args:
        longitude (str): Longitude coordinate
        latitude (str): Latitude coordinate
    
    Returns:
        dict: Speed limit information or error details
    """
    path = f"{longitude},{latitude}"
    return get_nearest_speed_limit(path=path)


