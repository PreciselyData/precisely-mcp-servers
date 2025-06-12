"""
PSAP 911 Service functions using Precisely APIs SDK.
Functions for accessing Public Safety Answering Points (PSAP) and Authorities Having Jurisdiction (AHJ) information.
"""

import json
import os
from typing import Optional, Dict, Any
from com.precisely.apis.api.psap_911_service_api import PSAP911ServiceApi
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the PSAP 911 Service API instance."""
    api = PSAP911ServiceApi()
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
def get_psap_by_address(address):
    """
    Get PSAP (Public Safety Answering Point) information for a specific address.
    
    Args:
        address (str): The address to search for PSAP information (required)
        
    Returns:
        dict: API response with PSAP information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.get_psapby_address(address=address)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract PSAP information
        if hasattr(response, 'psap') and response.psap:
            # Convert the PSAP object to a JSON-serializable dictionary
            psap_dict = _extract_object_data(response.psap)
            if psap_dict:
                result["data"]["psap"] = psap_dict
        
        # Extract additional metadata if available
        for attr in ['status', 'total_psaps_found']:
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
def get_psap_by_location(latitude, longitude):
    """
    Get PSAP (Public Safety Answering Point) information for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        
    Returns:
        dict: API response with PSAP information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Call the API
        response = api_instance.get_psapby_location(latitude=lat_str, longitude=lon_str)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract PSAP information
        if hasattr(response, 'psap') and response.psap:
            # Convert the PSAP object to a JSON-serializable dictionary
            psap_dict = _extract_object_data(response.psap)
            if psap_dict:
                result["data"]["psap"] = psap_dict
        
        # Extract additional metadata if available
        for attr in ['status', 'total_psaps_found']:
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
def get_ahj_psap_by_address(address):
    """
    Get AHJ (Authorities Having Jurisdiction) and PSAP information for a specific address.
    
    Args:
        address (str): The address to search for AHJ and PSAP information (required)
        
    Returns:
        dict: API response with AHJ and PSAP information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.get_ahj_plus_psapby_address(address=address)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract AHJ information
        if hasattr(response, 'ahj_list') and response.ahj_list:
            ahj_list = []
            
            for ahj in response.ahj_list:
                # Convert the AHJ object to a JSON-serializable dictionary
                ahj_dict = _extract_object_data(ahj)
                if ahj_dict:
                    ahj_list.append(ahj_dict)
            
            if ahj_list:
                result["data"]["ahj_list"] = ahj_list
        
        # Extract PSAP information
        if hasattr(response, 'psap') and response.psap:
            # Convert the PSAP object to a JSON-serializable dictionary
            psap_dict = _extract_object_data(response.psap)
            if psap_dict:
                result["data"]["psap"] = psap_dict
        
        # Extract additional metadata if available
        for attr in ['status', 'total_psaps_found']:
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
def get_ahj_psap_by_location(latitude, longitude):
    """
    Get AHJ (Authorities Having Jurisdiction) and PSAP information for a specific location.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
        
    Returns:
        dict: API response with AHJ and PSAP information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Convert coordinates to strings as required by the API
        lat_str = str(latitude)
        lon_str = str(longitude)
        
        # Call the API
        response = api_instance.get_ahj_plus_psapby_location(latitude=lat_str, longitude=lon_str)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract AHJ information
        if hasattr(response, 'ahj_list') and response.ahj_list:
            ahj_list = []
            
            for ahj in response.ahj_list:
                # Convert the AHJ object to a JSON-serializable dictionary
                ahj_dict = _extract_object_data(ahj)
                if ahj_dict:
                    ahj_list.append(ahj_dict)
            
            if ahj_list:
                result["data"]["ahj_list"] = ahj_list
        
        # Extract PSAP information
        if hasattr(response, 'psap') and response.psap:
            # Convert the PSAP object to a JSON-serializable dictionary
            psap_dict = _extract_object_data(response.psap)
            if psap_dict:
                result["data"]["psap"] = psap_dict
        
        # Extract additional metadata if available
        for attr in ['status', 'total_psaps_found']:
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
def search_ahj_psap_by_fcc_id(fcc_id):
    """
    Get AHJ (Authorities Having Jurisdiction) and PSAP information by FCC ID.
    
    Args:
        fcc_id (str): The FCC ID to search for AHJ and PSAP information (required)
        
    Returns:
        dict: API response with AHJ and PSAP information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.search_by_fcc_id(fcc_id=fcc_id)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract AHJ information
        if hasattr(response, 'ahj_list') and response.ahj_list:
            ahj_list = []
            
            for ahj in response.ahj_list:
                # Convert the AHJ object to a JSON-serializable dictionary
                ahj_dict = _extract_object_data(ahj)
                if ahj_dict:
                    ahj_list.append(ahj_dict)
            
            if ahj_list:
                result["data"]["ahj_list"] = ahj_list
        
        # Extract PSAP information
        if hasattr(response, 'psap') and response.psap:
            # Convert the PSAP object to a JSON-serializable dictionary
            psap_dict = _extract_object_data(response.psap)
            if psap_dict:
                result["data"]["psap"] = psap_dict
        
        # Extract additional metadata if available
        for attr in ['status', 'total_psaps_found']:
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
def validate_fcc_id(fcc_id):
    """
    Validate if the FCC ID is in a valid format.
    
    Args:
        fcc_id (str): FCC ID to validate
        
    Returns:
        bool: True if FCC ID is valid, False otherwise
    """
    if not fcc_id:
        return False
    
    # FCC IDs typically have alphanumeric format
    return isinstance(fcc_id, str) and len(fcc_id) > 0


@mcp.tool()
def get_emergency_service_info(address=None, latitude=None, longitude=None, fcc_id=None):
    """
    Get emergency service information using the most appropriate method based on provided parameters.
    
    Args:
        address (str, optional): Address to search
        latitude (float, optional): Latitude coordinate
        longitude (float, optional): Longitude coordinate
        fcc_id (str, optional): FCC ID
        
    Returns:
        dict: API response with emergency service information or error information
    """
    # Validate inputs and determine which method to use
    if fcc_id and validate_fcc_id(fcc_id):
        return search_ahj_psap_by_fcc_id(fcc_id)
    elif address:
        return get_ahj_psap_by_address(address)
    elif latitude is not None and longitude is not None:
        if validate_coordinates(latitude, longitude):
            return get_ahj_psap_by_location(latitude, longitude)
        else:
            return {
                "success": False,
                "error": "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            }
    else:
        return {
            "success": False,
            "error": "Insufficient or invalid parameters. Please provide a valid address, coordinates, or FCC ID."
        }
