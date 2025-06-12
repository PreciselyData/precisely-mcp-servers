"""
Schools Service functions using Precisely APIs SDK.
Functions for accessing schools information, including nearby schools search by address and location.
"""

import json
import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.schools_service_api import SchoolsServiceApi
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Schools Service API instance."""
    api = SchoolsServiceApi()
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
def validate_education_level(ed_level):
    """
    Validate education level for schools API.
    
    Args:
        ed_level (str): Education level to validate
        
    Returns:
        bool: True if education level is valid, False otherwise
    """
    valid_levels_public = ['P', 'M', 'H', 'O']  # Primary, Middle, High, Mixed Grades for public schools
    valid_levels_private = ['E', 'S', 'O']      # Elementary, Secondary, Others mixed grades for private schools
    valid_levels = valid_levels_public + valid_levels_private
    
    # Check if None (valid)
    if ed_level is None:
        return True
    
    # Check if string and in valid_levels
    if isinstance(ed_level, str) and len(ed_level) == 1:
        return ed_level.upper() in valid_levels
    
    # Invalid input
    return False


@mcp.tool()
def validate_school_type(school_type):
    """
    Validate school type for schools API.
    
    Args:
        school_type (str): School type to validate
        
    Returns:
        bool: True if school type is valid, False otherwise
    """
    valid_types = ['PRI', 'PUB']  # Private, Public
    
    # Check if None (valid)
    if school_type is None:
        return True
    
    # Check if string and in valid_types
    if isinstance(school_type, str):
        return school_type.upper() in valid_types
    
    # Invalid input
    return False


@mcp.tool()
def validate_school_sub_type(school_sub_type):
    """
    Validate school sub-type for schools API.
    
    Args:
        school_sub_type (str): School sub-type to validate
        
    Returns:
        bool: True if school sub-type is valid, False otherwise
    """
    valid_sub_types = ['C', 'M', 'A', 'R', 'I', 'L', 'P', 'V', 'U', 'S']
    # Charter, Magnet, Alternative, Regular, Indian, Military, Reportable Program, Vocational, Unknown, Special Education
    
    # Check if None (valid)
    if school_sub_type is None:
        return True
    
    # Check if string and in valid_sub_types
    if isinstance(school_sub_type, str) and len(school_sub_type) == 1:
        return school_sub_type.upper() in valid_sub_types
    
    # Invalid input
    return False


@mcp.tool()
def validate_gender(gender):
    """
    Validate gender filter for schools API.
    
    Args:
        gender (str): Gender filter to validate
        
    Returns:
        bool: True if gender filter is valid, False otherwise
    """
    valid_genders = ['C', 'F', 'M']  # Coed, All Females, All Males
    
    # Check if None (valid)
    if gender is None:
        return True
    
    # Check if string and in valid_genders
    if isinstance(gender, str) and len(gender) == 1:
        return gender.upper() in valid_genders
    
    # Invalid input
    return False


@mcp.tool()
def validate_travel_mode(travel_mode):
    """
    Validate travel mode for schools API.
    
    Args:
        travel_mode (str): Travel mode to validate
        
    Returns:
        bool: True if travel mode is valid, False otherwise
    """
    valid_modes = ['walking', 'driving']
    
    # Check if None (valid)
    if travel_mode is None:
        return True
    
    # Check if string and in valid_modes
    if isinstance(travel_mode, str):
        return travel_mode.lower() in valid_modes
    
    # Invalid input
    return False


@mcp.tool()
def validate_unit(unit, unit_type):
    """
    Validate units for schools API.
    
    Args:
        unit (str): Unit value to validate
        unit_type (str): Type of unit to validate (distance or time)
        
    Returns:
        bool: True if unit is valid, False otherwise
    """
    distance_units = ['feet', 'kilometers', 'miles', 'meters']
    time_units = ['minutes', 'hours', 'seconds', 'milliseconds']
    
    # Check if None (valid)
    if unit is None:
        return True
    
    # Check if string and in appropriate unit list
    if isinstance(unit, str):
        if unit_type == 'distance':
            return unit.lower() in distance_units
        elif unit_type == 'time':
            return unit.lower() in time_units
    
    # Invalid input
    return False


@mcp.tool()
def get_schools_by_address(address, **kwargs):
    """
    Get nearby schools information for a specific address.
    
    Args:
        address (str): Free form address text (required)
        **kwargs: Optional parameters including:
            - ed_level (str): Education level code
            - school_type (str): School type code (PRI or PUB)
            - school_sub_type (str): School sub-type code
            - gender (str): Gender filter code (C, F, M)
            - assigned_schools_only (str): Whether to include only assigned schools (Y/N)
            - district_schools_only (str): Whether to include only district schools (Y/N)
            - search_radius (str): Search radius
            - search_radius_unit (str): Search radius unit
            - travel_time (str): Travel time
            - travel_time_unit (str): Travel time unit
            - travel_distance (str): Travel distance
            - travel_distance_unit (str): Travel distance unit
            - travel_mode (str): Travel mode (walking, driving)
            - max_candidates (str): Maximum number of results
        
    Returns:
        dict: API response with nearby schools information or error information
    """
    try:
        # Validate parameters if provided
        if 'ed_level' in kwargs and not validate_education_level(kwargs['ed_level']):
            return {
                "success": False,
                "error": "Invalid education level. Valid values for public schools: P (Primary), M (Middle), H (High), O (Mixed). Valid values for private schools: E (Elementary), S (Secondary), O (Others)."
            }
        
        if 'school_type' in kwargs and not validate_school_type(kwargs['school_type']):
            return {
                "success": False,
                "error": "Invalid school type. Valid values are PRI (Private) and PUB (Public)."
            }
        
        if 'school_sub_type' in kwargs and not validate_school_sub_type(kwargs['school_sub_type']):
            return {
                "success": False,
                "error": "Invalid school sub-type. Valid values are C (Charter), M (Magnet), A (Alternative), R (Regular), I (Indian), L (Military), P (Reportable Program), V (Vocational), U (Unknown), S (Special Education)."
            }
        
        if 'gender' in kwargs and not validate_gender(kwargs['gender']):
            return {
                "success": False,
                "error": "Invalid gender filter. Valid values are C (Coed), F (All Females), M (All Males)."
            }
        
        if 'travel_mode' in kwargs and not validate_travel_mode(kwargs['travel_mode']):
            return {
                "success": False,
                "error": "Invalid travel mode. Valid values are walking and driving."
            }
        
        if 'search_radius_unit' in kwargs and not validate_unit(kwargs['search_radius_unit'], 'distance'):
            return {
                "success": False,
                "error": "Invalid search radius unit. Valid values are feet, kilometers, miles, meters."
            }
        
        if 'travel_time_unit' in kwargs and not validate_unit(kwargs['travel_time_unit'], 'time'):
            return {
                "success": False,
                "error": "Invalid travel time unit. Valid values are minutes, hours, seconds, milliseconds."
            }
        
        if 'travel_distance_unit' in kwargs and not validate_unit(kwargs['travel_distance_unit'], 'distance'):
            return {
                "success": False,
                "error": "Invalid travel distance unit. Valid values are feet, kilometers, miles, meters."
            }
        
        # Check for required travel_mode when travel_distance or travel_time is specified
        if ('travel_distance' in kwargs or 'travel_time' in kwargs) and 'travel_mode' not in kwargs:
            return {
                "success": False,
                "error": "Travel mode is required when travel_distance or travel_time is specified."
            }
        
        api_instance = _get_api_client()
        
        # Prepare parameters
        params = {'address': address}
        
        # Add additional parameters if provided
        params.update(kwargs)
        
        # Call the API
        response = api_instance.get_schools_by_address(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract matched address information
        if hasattr(response, 'matched_address') and response.matched_address:
            matched_address = {}
            if hasattr(response.matched_address, 'formatted_address'):
                matched_address['formatted_address'] = response.matched_address.formatted_address
            if hasattr(response.matched_address, 'main_address_line'):
                matched_address['main_address_line'] = response.matched_address.main_address_line
            if hasattr(response.matched_address, 'address_last_line'):
                matched_address['address_last_line'] = response.matched_address.address_last_line
            if hasattr(response.matched_address, 'place_name'):
                matched_address['place_name'] = response.matched_address.place_name
            if hasattr(response.matched_address, 'area_name1'):
                matched_address['area_name1'] = response.matched_address.area_name1
            if hasattr(response.matched_address, 'postal_code'):
                matched_address['postal_code'] = response.matched_address.postal_code
            if hasattr(response.matched_address, 'country'):
                matched_address['country'] = response.matched_address.country
            result["data"]["matched_address"] = matched_address
        
        # Extract schools information
        if hasattr(response, 'school') and response.school:
            schools = []
            for school in response.school:
                school_data = {}
                if hasattr(school, 'name'):
                    school_data['name'] = school.name
                if hasattr(school, 'id'):
                    school_data['id'] = school.id
                if hasattr(school, 'type'):
                    school_data['type'] = school.type
                if hasattr(school, 'sub_type'):
                    school_data['sub_type'] = school.sub_type
                if hasattr(school, 'education_level'):
                    school_data['education_level'] = school.education_level
                if hasattr(school, 'grade_range'):
                    school_data['grade_range'] = school.grade_range
                if hasattr(school, 'low_grade'):
                    school_data['low_grade'] = school.low_grade
                if hasattr(school, 'high_grade'):
                    school_data['high_grade'] = school.high_grade
                if hasattr(school, 'enrollment'):
                    school_data['enrollment'] = school.enrollment
                if hasattr(school, 'student_teacher_ratio'):
                    school_data['student_teacher_ratio'] = school.student_teacher_ratio
                if hasattr(school, 'gender'):
                    school_data['gender'] = school.gender
                if hasattr(school, 'distance'):
                    school_data['distance'] = school.distance
                if hasattr(school, 'distance_unit'):
                    school_data['distance_unit'] = school.distance_unit
                if hasattr(school, 'travel_time'):
                    school_data['travel_time'] = school.travel_time
                if hasattr(school, 'travel_time_unit'):
                    school_data['travel_time_unit'] = school.travel_time_unit
                
                # Extract school address if available
                if hasattr(school, 'address') and school.address:
                    address_data = {}
                    if hasattr(school.address, 'formatted_address'):
                        address_data['formatted_address'] = school.address.formatted_address
                    if hasattr(school.address, 'main_address_line'):
                        address_data['main_address_line'] = school.address.main_address_line
                    if hasattr(school.address, 'address_last_line'):
                        address_data['address_last_line'] = school.address.address_last_line
                    if hasattr(school.address, 'place_name'):
                        address_data['place_name'] = school.address.place_name
                    if hasattr(school.address, 'area_name1'):
                        address_data['area_name1'] = school.address.area_name1
                    if hasattr(school.address, 'postal_code'):
                        address_data['postal_code'] = school.address.postal_code
                    if hasattr(school.address, 'country'):
                        address_data['country'] = school.address.country
                    school_data['address'] = address_data
                
                # Extract coordinate information if available
                if hasattr(school, 'geometry') and school.geometry:
                    geometry_data = {}
                    if hasattr(school.geometry, 'coordinates') and school.geometry.coordinates:
                        geometry_data['coordinates'] = school.geometry.coordinates
                    if hasattr(school.geometry, 'type'):
                        geometry_data['type'] = school.geometry.type
                    school_data['geometry'] = geometry_data
                
                schools.append(school_data)
            
            result["data"]["schools"] = schools
        
        # Extract school district information
        if hasattr(response, 'school_district') and response.school_district:
            district_data = {}
            if hasattr(response.school_district, 'name'):
                district_data['name'] = response.school_district.name
            if hasattr(response.school_district, 'id'):
                district_data['id'] = response.school_district.id
            if hasattr(response.school_district, 'type'):
                district_data['type'] = response.school_district.type
            result["data"]["school_district"] = district_data
        
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
