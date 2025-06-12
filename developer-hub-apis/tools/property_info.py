"""
Property Information Service API function calling tools.

This module provides comprehensive function calling tools for the Precisely APIs Property Information Service,
including property attribute retrieval, parcel boundary operations, and batch processing.
"""

import os
from typing import Dict, Any, List, Optional, Union
import com.precisely.apis
from com.precisely.apis.api import property_information_service_api
from com.precisely.apis.model.property_info_address_request import PropertyInfoAddressRequest
from com.precisely.apis.model.property_info_preferences import PropertyInfoPreferences
from com.precisely.apis.model.matched_address import MatchedAddress
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp

def setup_api_client():
    """Set up and configure the Precisely API client with OAuth authentication."""
    api_key = PRECISELY_API_KEY
    api_secret = PRECISELY_API_SECRET

    if not api_key or not api_secret:
        raise ValueError("PRECISELY_API_KEY and PRECISELY_API_SECRET environment variables are required")
    
    configuration = com.precisely.apis.Configuration(
        host="https://api.precisely.com"
    )
    configuration.username = api_key
    configuration.password = api_secret
    
    api_client = com.precisely.apis.ApiClient(configuration)
    return property_information_service_api.PropertyInformationServiceApi(api_client)


def validate_address(address: str) -> bool:
    """Validate if address is not empty or None."""
    return address is not None and str(address).strip() != ""


def validate_coordinates(longitude: Union[str, float], latitude: Union[str, float]) -> bool:
    """Validate longitude and latitude coordinates."""
    try:
        lon = float(longitude)
        lat = float(latitude)
        return -180 <= lon <= 180 and -90 <= lat <= 90
    except (ValueError, TypeError):
        return False


def validate_precisely_id(precisely_id: str) -> bool:
    """Validate if precisely_id is not empty or None."""
    return precisely_id is not None and str(precisely_id).strip() != ""



def extract_response_data(api_response, response_type: str = "unknown") -> Dict[str, Any]:
    """Extract and structure response data from API response."""
    try:
        if hasattr(api_response, 'to_dict'):
            response_data = api_response.to_dict()
        else:
            response_data = api_response
        
        return {
            "success": True,
            "data": response_data,
            "response_type": response_type,
            "message": f"Successfully retrieved {response_type}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_type": response_type,
            "message": f"Failed to extract {response_type} data"
        }


@mcp.tool()
def get_parcel_boundary_by_address(address: str) -> Dict[str, Any]:
    """
    Get property parcel boundary by address.
    
    Args:
        address (str): Free form address text
        
    Returns:
        Dict containing success status, parcel boundary data, or error message
    """
    try:
        if not validate_address(address):
            return {
                "success": False,
                "error": "Address is required and cannot be empty",
                "response_type": "parcel_boundary",
                "message": "Invalid address provided"
            }
        
        api = setup_api_client()
        response = api.get_parcel_boundary_by_address(address=address)
        return extract_response_data(response, "parcel_boundary")
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_type": "parcel_boundary",
            "message": "Failed to get parcel boundary by address"
        }


@mcp.tool()
def get_parcel_boundary_by_location(longitude: Union[str, float], latitude: Union[str, float]) -> Dict[str, Any]:
    """
    Get property parcel boundary by location coordinates.
    
    Args:
        longitude (Union[str, float]): Longitude of location
        latitude (Union[str, float]): Latitude of location
        
    Returns:
        Dict containing success status, parcel boundary data, or error message
    """
    try:
        if not validate_coordinates(longitude, latitude):
            return {
                "success": False,
                "error": "Valid longitude (-180 to 180) and latitude (-90 to 90) are required",
                "response_type": "parcel_boundary",
                "message": "Invalid coordinates provided"
            }
        
        api = setup_api_client()
        response = api.get_parcel_boundary_by_location(
            longitude=str(longitude),
            latitude=str(latitude)
        )
        return extract_response_data(response, "parcel_boundary")
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_type": "parcel_boundary",
            "message": "Failed to get parcel boundary by location"
        }


@mcp.tool()
def get_parcel_boundary_by_precisely_id(precisely_id: str) -> Dict[str, Any]:
    """
    Get property parcel boundary by PreciselyID.
    
    Args:
        precisely_id (str): Precisely ID
        
    Returns:
        Dict containing success status, parcel boundary data, or error message
    """
    try:
        if not validate_precisely_id(precisely_id):
            return {
                "success": False,
                "error": "PreciselyID is required and cannot be empty",
                "response_type": "parcel_boundary",
                "message": "Invalid PreciselyID provided"
            }
        
        api = setup_api_client()
        response = api.get_parcel_boundary_by_precisely_id(precisely_id=precisely_id)
        return extract_response_data(response, "parcel_boundary")
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_type": "parcel_boundary",
            "message": "Failed to get parcel boundary by PreciselyID"
        }


@mcp.tool()
def get_property_attributes_by_address(address: str, attributes: Optional[str] = None) -> Dict[str, Any]:
    """
    Get property attributes by address.
    
    Args:
        address (str): Free form address text
        attributes (Optional[str]): Case-insensitive comma separated values of property attributes
        
    Returns:
        Dict containing success status, property attributes data, or error message
    """
    try:
        if not validate_address(address):
            return {
                "success": False,
                "error": "Address is required and cannot be empty",
                "response_type": "property_attributes",
                "message": "Invalid address provided"
            }
        
        api = setup_api_client()
        kwargs = {"address": address}
        if attributes:
            kwargs["attributes"] = attributes
            
        response = api.get_property_attributes_by_address(**kwargs)
        return extract_response_data(response, "property_attributes")
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_type": "property_attributes",
            "message": "Failed to get property attributes by address"
        }


@mcp.tool()
def get_property_attributes_by_address_batch(addresses: List[str], attributes: Optional[str] = None) -> Dict[str, Any]:
    """
    Get property attributes for multiple addresses in batch.
    
    Args:
        addresses (List[str]): List of addresses to process
        attributes (Optional[str]): Case-insensitive comma separated values of property attributes
        
    Returns:
        Dict containing success status, property attributes data, or error message
    """
    try:
        if not addresses or len(addresses) == 0:
            return {
                "success": False,
                "error": "At least one address is required",
                "response_type": "property_attributes_batch",
                "message": "Empty address list provided"
            }
        
        # Validate addresses
        valid_addresses = []
        for addr in addresses:
            if validate_address(addr):
                valid_addresses.append(addr)
        
        if not valid_addresses:
            return {
                "success": False,
                "error": "No valid addresses provided",
                "response_type": "property_attributes_batch",
                "message": "All addresses are invalid or empty"
            }
        
        api = setup_api_client()
        
        # Create MatchedAddress objects from strings
        matched_addresses = []
        for addr in valid_addresses:
            matched_address = MatchedAddress(formatted_address=addr)
            matched_addresses.append(matched_address)
        
        # Create preferences
        preferences = PropertyInfoPreferences()
        if attributes:
            preferences.attributes = attributes
        
        # Create the request object
        request = PropertyInfoAddressRequest(
            preferences=preferences,
            addresses=matched_addresses
        )
        
        response = api.get_property_attributes_by_address_batch(request)
        return extract_response_data(response, "property_attributes_batch")
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_type": "property_attributes_batch",
            "message": "Failed to get property attributes by address batch"
        }


# Convenience functions for common use cases

@mcp.tool()
def get_property_with_validation(address: str, attributes: Optional[str] = None) -> Dict[str, Any]:
    """
    Get property attributes with enhanced validation and error handling.
    
    Args:
        address (str): Address to search for
        attributes (Optional[str]): Specific attributes to retrieve
        
    Returns:
        Dict containing success status, property data, or detailed error message
    """
    if not address or str(address).strip() == "":
        return {
            "success": False,
            "error": "Address cannot be empty or None",
            "response_type": "property_attributes_validated",
            "message": "Validation failed: empty address"
        }
    
    return get_property_attributes_by_address(address.strip(), attributes)


@mcp.tool()
def search_properties_with_boundaries(addresses: List[str]) -> Dict[str, Any]:
    """
    Search for property boundaries for multiple addresses.
    
    Args:
        addresses (List[str]): List of addresses to search
        
    Returns:
        Dict containing aggregated boundary results
    """
    if not addresses:
        return {
            "success": False,
            "error": "Address list cannot be empty",
            "response_type": "property_boundaries_batch",
            "message": "No addresses provided for boundary search"
        }
    
    results = []
    errors = []
    
    for address in addresses:
        if validate_address(address):
            result = get_parcel_boundary_by_address(address)
            if result["success"]:
                results.append({
                    "address": address,
                    "boundary_data": result["data"]
                })
            else:
                errors.append({
                    "address": address,
                    "error": result["error"]
                })
        else:
            errors.append({
                "address": address,
                "error": "Invalid or empty address"
            })
    
    return {
        "success": len(results) > 0,
        "data": {
            "successful_boundaries": results,
            "failed_addresses": errors,
            "total_processed": len(addresses),
            "successful_count": len(results),
            "failed_count": len(errors)
        },
        "response_type": "property_boundaries_batch",
        "message": f"Processed {len(addresses)} addresses, {len(results)} successful, {len(errors)} failed"
    }


# Main function calling tools list
PROPERTY_INFO_TOOLS = [
    get_parcel_boundary_by_address,
    get_parcel_boundary_by_location,
    get_parcel_boundary_by_precisely_id,
    get_property_attributes_by_address,
    get_property_attributes_by_address_batch,
    get_property_with_validation,
    search_properties_with_boundaries
]

# Export all functions
__all__ = [
    'get_parcel_boundary_by_address',
    'get_parcel_boundary_by_location', 
    'get_parcel_boundary_by_precisely_id',
    'get_property_attributes_by_address',
    'get_property_attributes_by_address_batch',
    'get_property_with_validation',
    'search_properties_with_boundaries',
    'setup_api_client',
    'validate_address',
    'validate_coordinates',
    'validate_precisely_id',
    'extract_response_data',
    'PROPERTY_INFO_TOOLS'
]
