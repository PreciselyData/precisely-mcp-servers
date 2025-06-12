"""
Address Verification functions using Precisely APIs SDK.
Functions for validating and verifying mailing addresses.
"""

import json
import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.address_verification_service_api import AddressVerificationServiceApi
from com.precisely.apis.exceptions import ApiException

# Model imports
from com.precisely.apis.model.validate_mailing_address_request import ValidateMailingAddressRequest
from com.precisely.apis.model.validate_mailing_address_input import ValidateMailingAddressInput
from com.precisely.apis.model.validate_mailing_address_input_row import ValidateMailingAddressInputRow
from com.precisely.apis.model.validate_mailing_address_options import ValidateMailingAddressOptions
from com.precisely.apis.model.validate_mailing_address_premium_request import ValidateMailingAddressPremiumRequest
from com.precisely.apis.model.validate_mailing_address_pro_request import ValidateMailingAddressProRequest
from com.precisely.apis.model.validate_mailing_address_uscanapi_request import ValidateMailingAddressUSCANAPIRequest
from com.precisely.apis.model.get_city_state_province_api_request import GetCityStateProvinceAPIRequest
from com.precisely.apis.model.get_city_state_province_api_input import GetCityStateProvinceAPIInput
from com.precisely.apis.model.get_city_state_province_api_input_row import GetCityStateProvinceAPIInputRow
from com.precisely.apis.model.get_postal_codes_api_request import GetPostalCodesAPIRequest
from com.precisely.apis.model.get_postal_codes_api_input import GetPostalCodesAPIInput
from com.precisely.apis.model.get_postal_codes_api_input_row import GetPostalCodesAPIInputRow
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely

from server import mcp
def _get_api_client():
    """Create and configure the Address Verification API instance."""
    api = AddressVerificationServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api

@mcp.tool()
def validate_mailing_address(
    address_line1,
    city=None,
    state_province=None,
    postal_code=None,
    country=None,
    address_line2=None,
    firm_name=None,
    output_casing="M"
):
    """
    Validate a mailing address using Precisely's standard validation service.
    
    Args:
        address_line1 (str): The first line of the address (required)
        city (str, optional): The city name
        state_province (str, optional): The state or province
        postal_code (str, optional): The postal code
        country (str, optional): The country
        address_line2 (str, optional): The second line of the address
        firm_name (str, optional): The firm or company name
        output_casing (str, optional): Output casing format ("U"=Upper, "M"=Mixed, "L"=Lower)
    
    Returns:
        dict: API response with validation results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create address row - filter out None values to avoid type errors
        address_data = {
            "address_line1": address_line1
        }
        
        # Only add optional parameters if they're not None
        if city is not None: address_data["city"] = city
        if state_province is not None: address_data["state_province"] = state_province
        if postal_code is not None: address_data["postal_code"] = postal_code
        if country is not None: address_data["country"] = country
        if address_line2 is not None: address_data["address_line2"] = address_line2
        if firm_name is not None: address_data["firm_name"] = firm_name
        
        address_row = ValidateMailingAddressInputRow(**address_data)
        
        # Create input with address rows
        address_input = ValidateMailingAddressInput(row=[address_row])
        
        # Create options
        options = ValidateMailingAddressOptions(output_casing=output_casing)
        
        # Create request
        request = ValidateMailingAddressRequest(
            input=address_input,
            options=options
        )
        
        # Call API
        response = api_instance.validate_mailing_address(request)
        
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
def validate_mailing_address_premium(
    address_line1,
    city=None,
    state_province=None,
    postal_code=None,
    country=None,
    address_line2=None,
    firm_name=None
):
    """
    Validate a mailing address using Precisely's premium validation service.
    
    Args:
        address_line1 (str): The first line of the address (required)
        city (str, optional): The city name
        state_province (str, optional): The state or province
        postal_code (str, optional): The postal code
        country (str, optional): The country
        address_line2 (str, optional): The second line of the address
        firm_name (str, optional): The firm or company name
    
    Returns:
        dict: API response with premium validation results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create request with address data based on API structure
        address_data = {
            "address_line1": address_line1
        }
        
        # Only add optional parameters if they're not None
        if city is not None: address_data["city"] = city
        if state_province is not None: address_data["state_province"] = state_province
        if postal_code is not None: address_data["postal_code"] = postal_code
        if country is not None: address_data["country"] = country
        if address_line2 is not None: address_data["address_line2"] = address_line2
        if firm_name is not None: address_data["firm_name"] = firm_name
        
        request = ValidateMailingAddressPremiumRequest(
            input={
                "row": [address_data]
            }
        )
        
        # Call API
        response = api_instance.validate_mailing_address_premium(request)
        
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
def validate_mailing_address_pro(
    address_line1,
    city=None,
    state_province=None,
    postal_code=None,
    country=None,
    address_line2=None,
    firm_name=None
):
    """
    Validate a mailing address using Precisely's professional validation service.
    
    Args:
        address_line1 (str): The first line of the address (required)
        city (str, optional): The city name
        state_province (str, optional): The state or province
        postal_code (str, optional): The postal code
        country (str, optional): The country
        address_line2 (str, optional): The second line of the address
        firm_name (str, optional): The firm or company name
    
    Returns:
        dict: API response with professional validation results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create request with address data based on API structure
        address_data = {
            "address_line1": address_line1
        }
        
        # Only add optional parameters if they're not None
        if city is not None: address_data["city"] = city
        if state_province is not None: address_data["state_province"] = state_province
        if postal_code is not None: address_data["postal_code"] = postal_code
        if country is not None: address_data["country"] = country
        if address_line2 is not None: address_data["address_line2"] = address_line2
        if firm_name is not None: address_data["firm_name"] = firm_name
        
        request = ValidateMailingAddressProRequest(
            input={
                "row": [address_data]
            }
        )
        
        # Call API
        response = api_instance.validate_mailing_address_pro(request)
        
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
def validate_mailing_address_uscan(
    address_line1,
    city=None,
    state_province=None,
    postal_code=None,
    country=None,
    address_line2=None,
    firm_name=None
):
    """
    Validate a US/Canada mailing address with RDI and DPV functionality.
    
    Args:
        address_line1 (str): The first line of the address (required)
        city (str, optional): The city name
        state_province (str, optional): The state or province
        postal_code (str, optional): The postal code
        country (str, optional): The country
        address_line2 (str, optional): The second line of the address
        firm_name (str, optional): The firm or company name
    
    Returns:
        dict: API response with US/Canada validation results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create request with address data based on API structure
        address_data = {
            "address_line1": address_line1
        }
        
        # Only add optional parameters if they're not None
        if city is not None: address_data["city"] = city
        if state_province is not None: address_data["state_province"] = state_province
        if postal_code is not None: address_data["postal_code"] = postal_code
        if country is not None: address_data["country"] = country
        if address_line2 is not None: address_data["address_line2"] = address_line2
        if firm_name is not None: address_data["firm_name"] = firm_name
        
        request = ValidateMailingAddressUSCANAPIRequest(
            input={
                "row": [address_data]
            }
        )
        
        # Call API
        response = api_instance.validate_mailing_address_uscan(request)
        
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
def get_city_state_province(postal_code, country=None):
    """
    Get city and state/province for a given postal code (US and Canada).
    
    Args:
        postal_code (str): The postal code (required)
        country (str, optional): The country code
    
    Returns:
        dict: API response with city/state/province information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create request based on API structure
        data = {
            "postal_code": postal_code
        }
        
        # Only add country if it's not None
        if country is not None: 
            data["country"] = country
            
        request = GetCityStateProvinceAPIRequest(
            input={
                "row": [data]
            }
        )
        
        # Call API
        response = api_instance.get_city_state_province(request)
        
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
def get_postal_codes(city, state_province=None, country=None):
    """
    Get postal codes for a given city and state/province.
    
    Args:
        city (str): The city name (required)
        state_province (str, optional): The state or province
        country (str, optional): The country code
    
    Returns:
        dict: API response with postal code information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create request based on API structure  
        data = {
            "city": city
        }
        
        # Only add optional parameters if they're not None
        if state_province is not None:
            data["state_province"] = state_province
        if country is not None:
            data["country"] = country
            
        request = GetPostalCodesAPIRequest(
            input={
                "row": [data]
            }
        )
        
        # Call API
        response = api_instance.get_postal_codes(request)
        
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
