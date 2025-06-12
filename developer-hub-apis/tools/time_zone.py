"""
Timezone functions using Precisely APIs SDK.
Functions for getting timezone information by location and address.
"""

import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.time_zone_service_api import TimeZoneServiceApi
from com.precisely.apis.exceptions import ApiException
from com.precisely.apis.model.timezone_address_request import TimezoneAddressRequest
from com.precisely.apis.model.timezone_location_request import TimezoneLocationRequest
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the TimeZone Service API instance."""
    api = TimeZoneServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api

@mcp.tool()
def get_timezone_by_location(
    timestamp: str,
    longitude: str,
    latitude: str
) -> Dict[str, Any]:
    """
    Get timezone information for a specific location and timestamp.
    
    Args:
        timestamp (str): Timestamp in milliseconds
        longitude (str): Longitude of the location
        latitude (str): Latitude of the location
    
    Returns:
        dict: Timezone information or error details
    """
    try:
        api_instance = _get_api_client()
        
        # Call API
        response = api_instance.get_timezone_by_location(
            timestamp=timestamp,
            longitude=longitude,
            latitude=latitude
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
def get_timezone_by_address(
    timestamp: str,
    address: str,
    match_mode: Optional[str] = None,
    country: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get timezone information for a specific address and timestamp.
    
    Args:
        timestamp (str): Timestamp in milliseconds
        address (str): The address to be searched
        match_mode (str, optional): Match modes determine the leniency used to make a match 
                                   between the input address and the reference data (Default is relaxed)
        country (str, optional): Country ISO code (Default is USA)
    
    Returns:
        dict: Timezone information or error details
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters, filtering out None values
        params = {}
        if match_mode is not None:
            params['match_mode'] = match_mode
        if country is not None:
            params['country'] = country
        
        # Call API
        response = api_instance.get_timezone_by_address(
            timestamp=timestamp,
            address=address,
            **params
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
def batch_timezone_by_location(locations: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Get timezone information for multiple locations in batch.
    
    Args:
        locations (List[Dict]): List of location dictionaries, each containing:
                               - timestamp: Timestamp in milliseconds
                               - longitude: Longitude coordinate
                               - latitude: Latitude coordinate
    
    Returns:
        dict: Batch timezone results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create timezone location request object
        # Note: You'll need to check the actual structure of TimezoneLocationRequest
        # This is a best guess based on the API pattern
        request = TimezoneLocationRequest(locations=locations)
        
        # Call API
        response = api_instance.get_batch_timezone_by_location(
            timezone_location_request=request
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
def batch_timezone_by_address(addresses: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Get timezone information for multiple addresses in batch.
    
    Args:
        addresses (List[Dict]): List of address dictionaries, each containing:
                               - timestamp: Timestamp in milliseconds
                               - address: The address to be searched
                               - match_mode (optional): Match mode
                               - country (optional): Country ISO code
    
    Returns:
        dict: Batch timezone results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create timezone address request object
        # Note: You'll need to check the actual structure of TimezoneAddressRequest
        # This is a best guess based on the API pattern
        request = TimezoneAddressRequest(addresses=addresses)
        
        # Call API
        response = api_instance.get_timezone_by_address_batch(
            timezone_address_request=request
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


# Convenience functions for common use cases

@mcp.tool()
def get_current_timezone_by_location(longitude: str, latitude: str) -> Dict[str, Any]:
    """
    Get current timezone information for a location.
    
    Args:
        longitude (str): Longitude of the location
        latitude (str): Latitude of the location
    
    Returns:
        dict: Current timezone information or error details
    """
    import time
    current_timestamp = str(int(time.time() * 1000))  # Current time in milliseconds
    
    return get_timezone_by_location(
        timestamp=current_timestamp,
        longitude=longitude,
        latitude=latitude
    )


@mcp.tool()
def get_current_timezone_by_address(address: str, country: Optional[str] = None) -> Dict[str, Any]:
    """
    Get current timezone information for an address.
    
    Args:
        address (str): The address to be searched
        country (str, optional): Country ISO code
    
    Returns:
        dict: Current timezone information or error details
    """
    import time
    current_timestamp = str(int(time.time() * 1000))  # Current time in milliseconds
    
    return get_timezone_by_address(
        timestamp=current_timestamp,
        address=address,
        country=country
    )


