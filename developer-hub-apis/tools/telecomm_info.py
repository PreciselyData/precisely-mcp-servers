"""
Telecomm Info Service functions using Precisely APIs SDK.
Functions for getting rate center and telecommunications information.
"""
import os
from typing import Optional, Dict, Any
from com.precisely.apis.api.telecomm_info_service_api import TelecommInfoServiceApi
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Telecomm Info Service API instance."""
    api = TelecommInfoServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api


@mcp.tool()
def validate_country_code(country):
    """
    Validate country code parameter.
    
    Args:
        country (str): Country code to validate
        
    Returns:
        bool: True if country code is valid, False otherwise
    """
    valid_countries = ['USA', 'CAN']
    
    # Check if None (valid)
    if country is None:
        return True
    
    # Check if string and in valid_countries
    if isinstance(country, str):
        return country.upper() in valid_countries
    
    return False


@mcp.tool()
def validate_area_code_info(area_code_info):
    """
    Validate area code info parameter.
    
    Args:
        area_code_info (str): Area code info to validate
        
    Returns:
        bool: True if area code info is valid, False otherwise
    """
    valid_values = ['True', 'False']
    
    # Check if None (valid)
    if area_code_info is None:
        return True
    
    # Check if string and in valid_values
    if isinstance(area_code_info, str):
        return area_code_info in valid_values
    
    return False


@mcp.tool()
def validate_level(level):
    """
    Validate level parameter.
    
    Args:
        level (str): Level to validate
        
    Returns:
        bool: True if level is valid, False otherwise
    """
    valid_levels = ['basic', 'detail']
    
    # Check if None (valid)
    if level is None:
        return True
    
    # Check if string and in valid_levels
    if isinstance(level, str):
        return level.lower() in valid_levels
    
    return False

@mcp.tool()
def get_rate_center_by_address(
    address: Optional[str] = None,
    country: Optional[str] = None,
    area_code_info: Optional[str] = None,
    level: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get rate center information by address.
    
    Args:
        address (str, optional): The address to be searched
        country (str, optional): 3 letter ISO code of the country (USA, CAN)
        area_code_info (str, optional): Include area code info (True, False)
        level (str, optional): Level of detail (basic, detail)
    
    Returns:
        dict: Rate center information or error details
    """
    try:
        # Validate parameters
        if country and not validate_country_code(country):
            return {
                "success": False,
                "error": "Invalid country code. Valid values are: USA, CAN"
            }
        
        if area_code_info and not validate_area_code_info(area_code_info):
            return {
                "success": False,
                "error": "Invalid area code info. Valid values are: True, False"
            }
        
        if level and not validate_level(level):
            return {
                "success": False,
                "error": "Invalid level. Valid values are: basic, detail"
            }
        
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        if address is not None:
            params['address'] = address
        if country is not None:
            params['country'] = country
        if area_code_info is not None:
            params['area_code_info'] = area_code_info
        if level is not None:
            params['level'] = level
        
        # Call the API
        response = api_instance.get_rate_center_by_address(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract rate center information
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
        
        # Extract rate center data
        if hasattr(response, 'rate_center') and response.rate_center:
            rate_center = {}
            if hasattr(response.rate_center, 'name'):
                rate_center['name'] = response.rate_center.name
            if hasattr(response.rate_center, 'type'):
                rate_center['type'] = response.rate_center.type
            if hasattr(response.rate_center, 'lata'):
                rate_center['lata'] = response.rate_center.lata
            if hasattr(response.rate_center, 'incumbent_local_exchange_carrier'):
                rate_center['incumbent_local_exchange_carrier'] = response.rate_center.incumbent_local_exchange_carrier
            if hasattr(response.rate_center, 'area_codes') and response.rate_center.area_codes:
                area_codes = []
                for area_code in response.rate_center.area_codes:
                    area_code_data = {}
                    if hasattr(area_code, 'area_code'):
                        area_code_data['area_code'] = area_code.area_code
                    if hasattr(area_code, 'type'):
                        area_code_data['type'] = area_code.type
                    area_codes.append(area_code_data)
                rate_center['area_codes'] = area_codes
            result["data"]["rate_center"] = rate_center
        
        # Extract coordinate information if available
        if hasattr(response, 'geometry') and response.geometry:
            geometry = {}
            if hasattr(response.geometry, 'coordinates') and response.geometry.coordinates:
                geometry['coordinates'] = response.geometry.coordinates
            if hasattr(response.geometry, 'type'):
                geometry['type'] = response.geometry.type
            result["data"]["geometry"] = geometry
        
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
def get_rate_center_by_location(
    longitude: Optional[str] = None,
    latitude: Optional[str] = None,
    area_code_info: Optional[str] = None,
    level: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get rate center information by coordinates.
    
    Args:
        longitude (str, optional): Longitude of the location
        latitude (str, optional): Latitude of the location
        area_code_info (str, optional): Include area code info (True, False)
        level (str, optional): Level of detail (basic, detail)
    
    Returns:
        dict: Rate center information or error details
    """
    try:
        # Validate parameters
        if area_code_info and not validate_area_code_info(area_code_info):
            return {
                "success": False,
                "error": "Invalid area code info. Valid values are: True, False"
            }
        
        if level and not validate_level(level):
            return {
                "success": False,
                "error": "Invalid level. Valid values are: basic, detail"
            }
        
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        if longitude is not None:
            params['longitude'] = longitude
        if latitude is not None:
            params['latitude'] = latitude
        if area_code_info is not None:
            params['area_code_info'] = area_code_info
        if level is not None:
            params['level'] = level
        
        # Call the API
        response = api_instance.get_rate_center_by_location(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract telecomm info list (the main data structure)
        if hasattr(response, 'telecomm_info_list') and response.telecomm_info_list:
            telecomm_info = []
            for info in response.telecomm_info_list:
                info_data = {}
                if hasattr(info, 'company_name'):
                    info_data['company_name'] = info.company_name
                if hasattr(info, 'ocn'):
                    info_data['ocn'] = info.ocn
                if hasattr(info, 'ocn_category'):
                    info_data['ocn_category'] = info.ocn_category
                if hasattr(info, 'npa'):
                    info_data['npa'] = info.npa
                if hasattr(info, 'nxx'):
                    info_data['nxx'] = info.nxx
                if hasattr(info, 'start_range'):
                    info_data['start_range'] = info.start_range
                if hasattr(info, 'end_range'):
                    info_data['end_range'] = info.end_range
                if hasattr(info, 'lata'):
                    info_data['lata'] = info.lata
                if hasattr(info, 'area_name4'):
                    info_data['area_name4'] = info.area_name4
                telecomm_info.append(info_data)
            result["data"]["telecomm_info_list"] = telecomm_info
        
        # Extract rate center data if available
        if hasattr(response, 'rate_center') and response.rate_center:
            rate_center = {}
            if hasattr(response.rate_center, 'name'):
                rate_center['name'] = response.rate_center.name
            if hasattr(response.rate_center, 'type'):
                rate_center['type'] = response.rate_center.type
            if hasattr(response.rate_center, 'lata'):
                rate_center['lata'] = response.rate_center.lata
            if hasattr(response.rate_center, 'incumbent_local_exchange_carrier'):
                rate_center['incumbent_local_exchange_carrier'] = response.rate_center.incumbent_local_exchange_carrier
            if hasattr(response.rate_center, 'area_codes') and response.rate_center.area_codes:
                area_codes = []
                for area_code in response.rate_center.area_codes:
                    area_code_data = {}
                    if hasattr(area_code, 'area_code'):
                        area_code_data['area_code'] = area_code.area_code
                    if hasattr(area_code, 'type'):
                        area_code_data['type'] = area_code.type
                    area_codes.append(area_code_data)
                rate_center['area_codes'] = area_codes
            result["data"]["rate_center"] = rate_center
        
        # Extract coordinate information if available
        if hasattr(response, 'geometry') and response.geometry:
            geometry = {}
            if hasattr(response.geometry, 'coordinates') and response.geometry.coordinates:
                geometry['coordinates'] = response.geometry.coordinates
            if hasattr(response.geometry, 'type'):
                geometry['type'] = response.geometry.type
            result["data"]["geometry"] = geometry
        
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
def get_detailed_rate_center_by_address(address: str, country: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed rate center information by address with area codes.
    
    Args:
        address (str): The address to be searched
        country (str, optional): Country code (USA, CAN)
    
    Returns:
        dict: Detailed rate center information or error details
    """
    return get_rate_center_by_address(
        address=address,
        country=country,
        area_code_info="True",
        level="detail"
    )


@mcp.tool()
def get_detailed_rate_center_by_location(longitude: str, latitude: str) -> Dict[str, Any]:
    """
    Get detailed rate center information by coordinates with area codes.
    
    Args:
        longitude (str): Longitude of the location
        latitude (str): Latitude of the location
    
    Returns:
        dict: Detailed rate center information or error details
    """
    return get_rate_center_by_location(
        longitude=longitude,
        latitude=latitude,
        area_code_info="True",
        level="detail"
    )


@mcp.tool()
def get_area_codes_by_address(address: str, country: Optional[str] = None) -> Dict[str, Any]:
    """
    Get area codes for a specific address.
    
    Args:
        address (str): The address to be searched
        country (str, optional): Country code (USA, CAN)
    
    Returns:
        dict: Area code information or error details
    """
    result = get_rate_center_by_address(
        address=address,
        country=country,
        area_code_info="True",
        level="basic"
    )
    
    # Extract just the area codes if successful
    if result.get('success') and 'rate_center' in result.get('data', {}):
        rate_center = result['data']['rate_center']
        if 'area_codes' in rate_center:
            return {
                "success": True,
                "data": {
                    "area_codes": rate_center['area_codes'],
                    "address": result['data'].get('matched_address', {})
                }
            }
    
    return result


@mcp.tool()
def get_area_codes_by_location(longitude: str, latitude: str) -> Dict[str, Any]:
    """
    Get area codes for specific coordinates.
    
    Args:
        longitude (str): Longitude of the location
        latitude (str): Latitude of the location
    
    Returns:
        dict: Area code information or error details
    """
    result = get_rate_center_by_location(
        longitude=longitude,
        latitude=latitude,
        area_code_info="True",
        level="basic"
    )
    
    # Extract just the area codes if successful
    if result.get('success') and 'rate_center' in result.get('data', {}):
        rate_center = result['data']['rate_center']
        if 'area_codes' in rate_center:
            return {
                "success": True,
                "data": {
                    "area_codes": rate_center['area_codes'],
                    "coordinates": result['data'].get('geometry', {})
                }
            }
    
    return result


